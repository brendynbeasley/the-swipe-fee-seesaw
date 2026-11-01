"""Did banks raise the cardholder side when the merchant side was capped?

Rochet and Tirole (2003): a platform that must cut the price on one side of the market
raises the price on the other side. With the log-concave demand they assume, the rise is
a fraction rho of the cut, 0 < rho <= 1. The test here uses the Durbin Amendment's debit
interchange cap (Regulation II, October 1, 2011), which applied only to issuers with $10
billion or more in assets. The cardholder price is a bank's service charges on deposit
accounts per deposit account, from FDIC call report data.

    1. Difference in differences, covered banking groups vs exempt groups of $1-10 billion,
       2010-2019, with group and year fixed effects, standard errors clustered by group.
    2. A pre-trend check on service charges per $1,000 of domestic deposits, 2006-2019.
    3. rho by year: the account-weighted fee increase divided by the interchange revenue
       lost per covered deposit account (from results/lost_interchange.csv).
    4. The largest covered banks by name.

Inputs: data/raw/fdic_q4_2006_2023.csv.gz (fetched from the FDIC BankFind API if missing)
        results/lost_interchange.csv (run src/price_structure.py first)

Run from the repository root:
    python src/account_fees.py
"""

import json
import time
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"
FDIC_FILE = RAW / "fdic_q4_2006_2023.csv.gz"
FDIC_FIELDS = ("CERT,REPDTE,NAMEFULL,NAMEHCR,RSSDHCR,RSSDID,STALP,BKCLASS,SPECGRP,ASSET,DEPDOM,"
               "ISERCHG,DEPSMB,DEPLGB")

THRESHOLD = 10e6        # Regulation II: $10 billion of consolidated assets (FDIC reports $ thousands)
SMALLEST = 1e6          # control groups start at $1 billion, as in Kay, Manuszak & Vojtech (2014)
TREAT_YEAR = 2010       # coverage set on assets at the end of 2010, the year before the cap
YEARS = range(2010, 2020)        # deposit accounts are reported for every bank from 2010
CORE_YEARS = range(2010, 2014)   # every group must be present through the first two capped years
COUNT_BREAK = 0.40      # a year-on-year change in accounts 40% beyond the change in deposits
PRE_YEARS = range(2006, 2020)    # deposits-based outcome reaches further back
FEE_BAND = (10, 400)    # 2010 fee per account; drops card, custody and online-only groups
MIN_ACCOUNTS = 10_000
MAX_UNREPORTED = 0.05   # drop a group if banks without service-charge data hold >5% of its accounts
WINSOR = 0.01
CREDIT_CARD_SPECGRP = 3  # FDIC asset-concentration group for credit card banks
# The largest banks, dropped in one robustness check (Citigroup is already outside the sample)
LARGEST = {1039502, 1073757, 1120754, 1951350}  # JPMorgan Chase, Bank of America, Wells Fargo, Citigroup
WELLS_FARGO = 1120754   # dropped alone in a second check: its reported accounts fell 27% in 2010-13
WINDOWS = {"2011": [2011], "2012-13": [2012, 2013], "2014-16": [2014, 2015, 2016],
           "2017-19": [2017, 2018, 2019]}

# Display names for regulatory top holders (RSSD ID -> name a reader knows)
DISPLAY = {1039502: "JPMorgan Chase", 1073757: "Bank of America", 1120754: "Wells Fargo",
           1951350: "Citigroup", 1119794: "U.S. Bancorp", 1069778: "PNC",
           1238565: "TD Bank (Toronto-Dominion)", 1131787: "SunTrust", 1074156: "BB&T",
           3242838: "Regions", 1070345: "Fifth Third", 3833526: "Citizens (owned by RBS)",
           1068025: "KeyCorp", 2277860: "Capital One", 1037003: "M&T", 1068191: "Huntington",
           1391237: "BBVA Compass", 1857108: "HSBC USA", 1199844: "Comerica",
           3594612: "Marshall & Ilsley", 1027004: "Zions", 1231333: "BMO Harris",
           1231968: "First Hawaiian / Bank of the West (BNP Paribas)", 2961897: "Union Bank (MUFG)",
           1239254: "Santander (Sovereign)"}


def fetch_fdic():
    """Download fourth-quarter financials for every FDIC-insured institution, 2006-2023."""
    rows = []
    for y in range(2006, 2024):
        offset = 0
        while True:
            url = (f"https://api.fdic.gov/banks/financials?filters=REPDTE:{y}1231"
                   f"&fields={FDIC_FIELDS}&limit=10000&offset={offset}&format=json")
            d = json.load(urllib.request.urlopen(url, timeout=120))
            got = [x["data"] for x in d["data"]]
            rows += got
            offset += len(got)
            if offset >= d["meta"]["total"] or not got:
                break
        print(f"  fetched {y}: {offset} institutions")
        time.sleep(0.5)
    df = pd.DataFrame(rows).drop(columns=["ID"], errors="ignore")
    df.to_csv(FDIC_FILE, index=False, compression="gzip")


def load_fdic():
    if not FDIC_FILE.exists():
        print("FDIC file missing; fetching from api.fdic.gov")
        fetch_fdic()
    d = pd.read_csv(FDIC_FILE)
    d["year"] = d.REPDTE // 10000
    hcr = d.RSSDHCR.fillna(0).astype(int)
    d["group"] = np.where(hcr > 0, "H" + hcr.astype(str), "C" + d.CERT.astype(str))
    d["rssd_hc"] = hcr
    d["accounts"] = d.DEPSMB + d.DEPLGB
    print(f"Loaded {len(d):,} bank-years, {d.CERT.nunique():,} institutions, "
          f"{d.year.min()}-{d.year.max()}")
    return d


def build_groups(d):
    """Aggregate banks to their regulatory top holder, one row per group-year."""
    assets = d.groupby(["group", "year"]).ASSET.sum().rename("assets")
    all_acc = d.groupby(["group", "year"]).accounts.sum().rename("accounts_all")
    noncard = d[d.SPECGRP != CREDIT_CARD_SPECGRP]
    noncard_acc = noncard.groupby(["group", "year"]).accounts.sum().rename("accounts_noncard")
    use = noncard[noncard.ISERCHG.notna()]
    print(f"Bank-years with service-charge data, not credit card banks: {len(use):,} "
          f"(dropped {len(d) - len(use):,})")
    g = use.groupby(["group", "year"]).agg(
        service_charges=("ISERCHG", "sum"), accounts=("accounts", lambda s: s.sum(min_count=1)),
        deposits=("DEPDOM", "sum"), rssd_hc=("rssd_hc", "first"))
    big = use.sort_values("ASSET").groupby(["group", "year"]).tail(1).set_index(["group", "year"])
    g["name"] = big.NAMEHCR.fillna(big.NAMEFULL)
    g = g.join(assets).join(all_acc).join(noncard_acc).reset_index()
    g["unreported_share"] = 1 - g.accounts / g.accounts_noncard
    g["fee_per_account"] = g.service_charges * 1000 / g.accounts          # dollars per year
    g["fee_per_1000_dep"] = g.service_charges / g.deposits * 1000          # dollars per $1,000
    return g


def select_sample(g):
    base = g[g.year == TREAT_YEAR].set_index("group")
    keep = base[base.assets >= SMALLEST].copy()
    print(f"Groups with assets of $1 billion or more at end-{TREAT_YEAR}: {len(keep)}")
    keep["covered"] = (keep.assets >= THRESHOLD).astype(int)
    steps = [
        ("2010 fee per account outside $10-$400, or under 10,000 accounts",
         keep.fee_per_account.between(*FEE_BAND) & (keep.accounts >= MIN_ACCOUNTS)),
    ]
    panel = g[g.group.isin(keep.index) & g.year.isin(YEARS)].dropna(subset=["fee_per_account"])
    panel = panel[panel.accounts > 0].sort_values(["group", "year"])
    # End a group's panel at its first gap or its first account-count break (a year in which
    # the number of accounts moves 40% more than deposits, a reporting change, not a merger)
    gap = panel.groupby("group").year.diff()
    jump = (np.log(panel.accounts).groupby(panel.group).diff()
            - np.log(panel.deposits).groupby(panel.group).diff()).abs()
    bad = (gap > 1) | (jump > np.log(1 + COUNT_BREAK))
    cut = bad.groupby(panel.group).cummax()
    print(f"  ended {panel[bad].group.nunique()} group panels early at a gap or an account-count "
          f"break, dropping {int(cut.sum())} group-years")
    panel = panel[~cut]
    core = panel[panel.year.isin(CORE_YEARS)].groupby("group").size()
    steps.append(("not present, without a break, in every year 2010-2013",
                  keep.index.to_series().map(core).fillna(0) == len(CORE_YEARS)))
    worst = panel.groupby("group").unreported_share.max()
    steps.append(("banks without service-charge data hold over 5% of accounts",
                  keep.index.to_series().map(worst).fillna(1) <= MAX_UNREPORTED))
    a_max = panel.groupby("group").assets.max()
    a_min = panel[panel.year >= 2011].groupby("group").assets.min()
    stays = np.where(keep.covered == 1, keep.index.to_series().map(a_min) >= THRESHOLD,
                     keep.index.to_series().map(a_max) < THRESHOLD)
    steps.append(("crossed the $10 billion line while in the panel", pd.Series(stays, keep.index)))
    mask = pd.Series(True, keep.index)
    rows = []
    for why, ok in steps:
        drop = mask & ~ok
        rows.append(dict(rule=why, dropped_covered=int(keep.covered[drop].sum()),
                         dropped_exempt=int((1 - keep.covered[drop]).sum())))
        print(f"  drop {drop.sum():4d} ({rows[-1]['dropped_covered']} covered): {why}")
        mask &= ok
    kept = keep[mask]
    rows.append(dict(rule="kept", dropped_covered=int(kept.covered.sum()),
                     dropped_exempt=int((1 - kept.covered).sum())))
    pd.DataFrame(rows).to_csv(OUT / "sample_counts.csv", index=False)
    print(f"Kept {len(kept)} groups: {kept.covered.sum()} covered, {(1 - kept.covered).sum()} exempt")
    return kept, panel[panel.group.isin(kept.index)]


def winsorize(s):
    lo, hi = s.quantile([WINSOR, 1 - WINSOR])
    return s.clip(lo, hi)


def event_study(df, y, years, base, weight=None):
    """Two-way fixed effects with covered x year dummies, clustered by group."""
    df = df.copy()
    terms = []
    for t in years:
        if t != base:
            df[f"d{t}"] = df.covered * (df.year == t)
            terms.append(f"d{t}")
    f = f"{y} ~ {' + '.join(terms)} + C(group) + C(year)"
    if weight:
        m = smf.wls(f, df, weights=df[weight])
    else:
        m = smf.ols(f, df)
    r = m.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.group)[0]})
    out = [dict(year=base, beta=0.0, se=0.0)]
    out += [dict(year=int(t[1:]), beta=r.params[t], se=r.bse[t]) for t in terms]
    pre = [t for t in terms if int(t[1:]) < base]
    p_pre = float(r.f_test(" = 0, ".join(pre) + " = 0").pvalue) if pre else np.nan
    return pd.DataFrame(out).sort_values("year"), p_pre, int(r.nobs)


def windows_did(df, y, weight=None):
    df = df.copy()
    terms = []
    for k, (name, ys) in enumerate(WINDOWS.items()):
        df[f"w{k}"] = df.covered * df.year.isin(ys)
        terms.append((f"w{k}", name))
    f = f"{y} ~ {' + '.join(t for t, _ in terms)} + C(group) + C(year)"
    m = smf.wls(f, df, weights=df[weight]) if weight else smf.ols(f, df)
    r = m.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.group)[0]})
    return [dict(window=n, beta=r.params[t], se=r.bse[t], p=r.pvalues[t]) for t, n in terms]


def run_did(g, kept, panel):
    panel = panel.copy()
    panel["covered"] = panel.group.map(kept.covered)
    panel["w2010"] = panel.group.map(kept.accounts)
    panel["fee"] = winsorize(panel.fee_per_account)
    print(f"Panel: {len(panel)} group-years; fee per account winsorized at 1%/99%")
    means = panel.groupby(["covered", "year"]).apply(
        lambda x: pd.Series({"mean_fee": x.fee.mean(),
                             "weighted_fee": np.average(x.fee, weights=x.w2010),
                             "groups": len(x), "accounts_m": x.accounts.sum() / 1e6}),
        include_groups=False).reset_index()
    means.to_csv(OUT / "fee_means_by_group.csv", index=False)

    es = []
    for label, w in [("unweighted", None), ("account-weighted", "w2010")]:
        e, _, n = event_study(panel, "fee", YEARS, TREAT_YEAR, w)
        e["weights"] = label
        e["n"] = n
        es.append(e)
    es = pd.concat(es)
    es.to_csv(OUT / "event_study_fee_per_account.csv", index=False)

    panel["log_fee"] = np.log(panel.fee)
    panel["fee_dep"] = winsorize(panel.fee_per_1000_dep)
    no_big = panel[~panel.rssd_hc.isin(LARGEST)]
    no_wf = panel[panel.rssd_hc != WELLS_FARGO]
    specs = [("fee per account ($/yr)", "fee", panel),
             ("log fee per account", "log_fee", panel),
             ("fee per account, without JPMorgan Chase, Bank of America, Wells Fargo", "fee", no_big),
             ("fee per account, without Wells Fargo", "fee", no_wf),
             ("fee per $1,000 of domestic deposits", "fee_dep", panel)]
    rows = []
    for name, y, df in specs:
        for label, w in [("unweighted", None), ("account-weighted", "w2010")]:
            for r in windows_did(df, y, w):
                rows.append(dict(outcome=name, weights=label, groups=df.group.nunique(),
                                 covered_groups=df[df.covered == 1].group.nunique(), **r))

    # Pre-trend check on a measure available before 2010
    dep = g[g.group.isin(kept.index) & g.year.isin(PRE_YEARS)].dropna(subset=["fee_per_1000_dep"])
    full = dep.groupby("group").size()
    dep = dep[dep.group.map(full) == len(PRE_YEARS)].copy()
    dep["covered"] = dep.group.map(kept.covered)
    dep["w2010"] = dep.group.map(kept.accounts)
    dep["fee_dep"] = winsorize(dep.fee_per_1000_dep)
    pre_rows = []
    for label, w in [("unweighted", None), ("account-weighted", "w2010")]:
        e, p_pre, n = event_study(dep, "fee_dep", PRE_YEARS, TREAT_YEAR, w)
        e["weights"] = label
        e["pretrend_p"] = p_pre
        e["groups"] = dep.group.nunique()
        pre_rows.append(e)
        print(f"Deposits-based event study ({label}): {dep.group.nunique()} groups, "
              f"joint test of 2006-2009 = 0, p = {p_pre:.3f}")
    pd.concat(pre_rows).to_csv(OUT / "event_study_fee_per_deposits.csv", index=False)
    did = pd.DataFrame(rows)
    did.to_csv(OUT / "did_windows.csv", index=False)
    print(did.round(3).to_string(index=False))
    return panel, es, did


def offset_ratio(g, es, did, panel):
    """rho_t = fee increase per covered account / interchange lost per covered account."""
    lost = pd.read_csv(OUT / "lost_interchange.csv").set_index("year")
    retail = g[(g.assets >= THRESHOLD) & g.fee_per_account.between(*FEE_BAND)]
    cov = retail.groupby("year").accounts_noncard.sum()
    w = es[es.weights == "account-weighted"].set_index("year")
    rows = []
    for y in range(2012, 2020):
        per_acc = lost.loc[y, "lost_interchange_bn"] * 1e9 / cov[y]
        b, se = w.loc[y, "beta"], w.loc[y, "se"]
        sample_acc = panel[(panel.covered == 1) & (panel.year == y)].accounts.sum()
        rows.append(dict(year=y, lost_interchange_bn=lost.loc[y, "lost_interchange_bn"],
                         covered_accounts_all_m=cov[y] / 1e6, lost_per_account=per_acc,
                         fee_increase_per_account=b, fee_increase_se=se,
                         rho=b / per_acc, rho_lo=(b - 1.96 * se) / per_acc,
                         rho_hi=(b + 1.96 * se) / per_acc,
                         z_rho_eq_0=b / se, z_rho_eq_1=(b - per_acc) / se,
                         sample_covered_accounts_m=sample_acc / 1e6,
                         extra_fees_sample_bn=b * sample_acc / 1e9))
    df = pd.DataFrame(rows)
    pooled = []
    main = did[(did.outcome == "fee per account ($/yr)") & (did.weights == "account-weighted")]
    for name, ys in [("2012-13", [2012, 2013]), ("2014-16", [2014, 2015, 2016]),
                     ("2017-19", [2017, 2018, 2019])]:
        r = main[main.window == name].iloc[0]
        L = df[df.year.isin(ys)].lost_per_account.mean()
        pooled.append(dict(year=name, lost_interchange_bn=df[df.year.isin(ys)].lost_interchange_bn.sum(),
                           lost_per_account=L, fee_increase_per_account=r.beta,
                           fee_increase_se=r.se, rho=r.beta / L, rho_lo=(r.beta - 1.96 * r.se) / L,
                           rho_hi=(r.beta + 1.96 * r.se) / L, z_rho_eq_0=r.beta / r.se,
                           z_rho_eq_1=(r.beta - L) / r.se))
    df = pd.concat([df, pd.DataFrame(pooled)], ignore_index=True)
    df.to_csv(OUT / "offset_ratio.csv", index=False)
    print(df.round(3).to_string(index=False))
    return df


def names_table(g, kept, panel):
    cov = kept[kept.covered == 1].sort_values("accounts", ascending=False).head(12)
    p = panel.set_index(["group", "year"])
    ex = panel[panel.covered == 0]
    ex_change = {y: (ex[ex.year == y].fee.mean() - ex[ex.year == 2010].fee.mean()) for y in (2013, 2019)}
    rows = []
    for grp, r in cov.iterrows():
        f10, f13, f19 = (p.fee_per_account.get((grp, y), np.nan) for y in (2010, 2013, 2019))
        s10, s13 = (p.service_charges.get((grp, y), np.nan) / 1e6 for y in (2010, 2013))
        a13 = p.accounts.get((grp, 2013), np.nan) / 1e6
        rows.append(dict(bank=DISPLAY.get(int(r.rssd_hc), r["name"]), rssd_hc=int(r.rssd_hc),
                         assets_2010_bn=r.assets / 1e6, accounts_2010_m=r.accounts / 1e6,
                         accounts_2013_m=a13, service_charges_2010_bn=s10,
                         service_charges_2013_bn=s13,
                         fee_2010=f10, fee_2013=f13, fee_2019=f19,
                         change_2010_13=f13 - f10,
                         change_vs_exempt_2010_13=(f13 - f10) - ex_change[2013],
                         change_vs_exempt_2010_19=(f19 - f10) - ex_change[2019]))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "largest_covered_banks.csv", index=False)
    print(f"Exempt groups' mean change in fee per account: 2010-13 {ex_change[2013]:+.2f}, "
          f"2010-19 {ex_change[2019]:+.2f}")
    print(df.round(2).to_string(index=False))
    return df


def plot_event(es):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    for (label, sub), color, dx in zip(es.groupby("weights", sort=False), ["#1f5f8b", "#b5651d"], [-0.08, 0.08]):
        ax.errorbar(sub.year + dx, sub.beta, yerr=1.96 * sub.se, fmt="o-", capsize=3, color=color,
                    label=f"{label}", lw=1.2, ms=4)
    ax.axhline(0, color="#444444", lw=0.8)
    ax.axvline(2011.75, color="#888888", lw=0.8, ls="--")
    ax.text(2011.8, ax.get_ylim()[1] * 0.92, "cap in force\nfrom Oct 2011", fontsize=8, va="top")
    ax.set_xticks(list(YEARS))
    ax.set_ylabel("Covered minus exempt, $ per account per year\n(relative to 2010)")
    ax.set_title("Deposit-account fees at capped banks after the interchange cap", fontsize=11)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "event_study_fee_per_account.png", dpi=160)
    plt.close(fig)
    print("Wrote event_study_fee_per_account.png")


def plot_offset(off):
    o = off[off.year.apply(lambda v: isinstance(v, (int, np.integer)))].copy()
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar(o.year.astype(int), o.lost_per_account, color="#d9d9d9", label="Interchange lost per covered account")
    ax.errorbar(o.year.astype(int), o.fee_increase_per_account, yerr=1.96 * o.fee_increase_se,
                fmt="o", color="#1f5f8b", capsize=3, label="Added deposit fees per account (95% CI)")
    for _, r in o.iterrows():
        ax.text(int(r.year), r.lost_per_account + 1.0, f"{r.rho:.0%}", ha="center", fontsize=8,
                bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.axhline(0, color="#444444", lw=0.8)
    ax.set_xticks(o.year.astype(int))
    ax.set_ylabel("Dollars per deposit account per year")
    ax.set_title("How much of the lost swipe revenue came back from account holders", fontsize=11)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "offset_by_year.png", dpi=160)
    plt.close(fig)
    print("Wrote offset_by_year.png")


def main():
    OUT.mkdir(exist_ok=True)
    if not (OUT / "lost_interchange.csv").exists():
        raise SystemExit("Run src/price_structure.py first")
    d = load_fdic()
    g = build_groups(d)
    kept, panel = select_sample(g)
    panel, es, did = run_did(g, kept, panel)
    off = offset_ratio(g, es, did, panel)
    names_table(g, kept, panel)
    plot_event(es)
    plot_offset(off)


if __name__ == "__main__":
    main()
