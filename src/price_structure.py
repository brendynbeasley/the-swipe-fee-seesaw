"""The two prices of a debit card swipe, from the Federal Reserve's Regulation II data.

Rochet and Tirole (2003) say a payment platform chooses a price *structure*: how much of
the total price per transaction it collects from the merchant (p_S) and how much from the
cardholder (p_B). This script reads the Federal Reserve Board's published debit card
statistics and builds:

    1. the 2009 price structure of a US debit transaction, before any regulation, with the
       elasticities that Rochet and Tirole's Proposition 1 would need to rationalize it;
    2. the merchant-side price (average interchange fee per transaction) for capped
       ("covered") and uncapped ("exempt") issuers, 2009 to 2024;
    3. the interchange revenue covered issuers gave up each year once the cap took effect
       on October 1, 2011, which account_fees.py compares with what they raised from
       depositors.

Inputs (committed in data/raw/):
    regiireportsdata.xls     Fed tables behind the biennial interchange fee reports
    Avg_IF_by_PCN.csv        Fed average interchange fee by network, covered vs exempt
    fed_report_quotes.csv    a few figures quoted from the text of the Fed reports

Run from the repository root:
    python src/price_structure.py
"""

import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

# Covered issuers' average fee before the cap is the 50 cents the Fed's 2011 report gives for
# January-September 2011; the script checks it against the Fed's tables.
PRE_CAP_PERIOD = "2011 Jan-Sep"
FIRST_FULL_CAP_YEAR = 2012


def load_quotes():
    q = pd.read_csv(RAW / "fed_report_quotes.csv").set_index("item")["value"]
    print(f"Loaded {len(q)} figures quoted from the Fed reports")
    return q


def read_report_table(xls, sheet):
    """Return one Fed report table as (row label -> list of cells) plus its two header rows."""
    t = xls[sheet]
    years = t.iloc[1].ffill().tolist()
    cols = t.iloc[2].tolist()
    return t, years, cols


def report_value(t, years, cols, row_label, year, col_prefix):
    """Find the cell for a row label, a year header and a column header prefix."""
    labels = [str(s).strip().replace("\n", " ") for s in t.iloc[:, 0]]
    rows = [i for i, s in enumerate(labels) if s.startswith(row_label)]
    for j in range(1, t.shape[1]):
        y = str(years[j]).strip()
        c = str(cols[j]).replace("\n", " ")
        if re.match(rf"^{re.escape(str(year))}\d?$", y) and c.startswith(col_prefix):
            return float(t.iloc[rows[0], j])
    raise KeyError((row_label, year, col_prefix))


def parse_network_csv():
    """Average interchange fee and covered share for each year, issuer group and network type."""
    rows = list(csv.reader(open(RAW / "Avg_IF_by_PCN.csv", encoding="latin-1")))
    starts = [(i, c) for i, c in enumerate(rows[1]) if i > 0 and c.strip()]
    wanted = {"All Networks": "all", "Dual-message": "dual", "Single-message": "single"}
    out = []
    for k, (start, label) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(rows[1])
        m = re.match(r"(\d{4})", label)
        if label.startswith("October"):
            period = "2011 Q4"
        elif label.startswith("January"):
            period = "2011 Jan-Sep"
        else:
            period = m.group(1)
        group = None
        for c in range(start, end):
            if rows[2][c].strip():
                group = rows[2][c].split()[0].lower()  # exempt / covered / all
            head = rows[3][c]
            for r in rows[4:]:
                name = re.sub(r"\d+$", "", r[0].strip())
                if name not in wanted or c >= len(r):
                    continue
                cell = r[c].replace("$", "").replace("%", "").strip()
                if cell in ("", "NA"):
                    continue
                if head.startswith("Average inte"):
                    out.append(dict(period=period, group=group, network=wanted[name],
                                    measure="fee", value=float(cell)))
                elif head.startswith("% of total num"):
                    out.append(dict(period=period, group=group, network=wanted[name],
                                    measure="share_number", value=float(cell) / 100))
    df = pd.DataFrame(out)
    print(f"Parsed {len(df)} values from Avg_IF_by_PCN.csv covering {df.period.nunique()} periods")
    return df


def price_structure_2009(xls, quotes):
    """Rochet-Tirole Proposition 1 applied to the 2009 debit transaction."""
    t4, y4, c4 = read_report_table(xls, "4")
    t13, y13, c13 = read_report_table(xls, "13")
    p_s = report_value(t4, y4, c4, "All transactions", 2009, "Fee per")
    p_s_sig = report_value(t4, y4, c4, "Dual-message networks", 2009, "Fee per")
    p_s_pin = report_value(t4, y4, c4, "Single-message networks", 2009, "Fee per")
    cost = report_value(t13, y13, c13, "All transactions", 2009, "All cove")
    cost_sig = report_value(t13, y13, c13, "Dual-message debit transactions2", 2009, "All cove")
    cost_pin = report_value(t13, y13, c13, "Single-message debit transactions2", 2009, "All cove")
    rewards = quotes["rewards_per_txn_2009"]
    t1, y1, c1 = read_report_table(xls, "1")
    ticket = report_value(t1, y1, c1, "All transactions", 2009, "Average")
    share = report_value(t4, y4, c4, "All transactions", 2009, "Fee as")
    print(f"2009: average purchase ${ticket:.2f}, interchange {share:.2%} of the purchase")
    rows = []
    for label, ps, c in [("All debit", p_s, cost), ("Signature (dual-message)", p_s_sig, cost_sig),
                         ("PIN (single-message)", p_s_pin, cost_pin)]:
        # Cardholder rewards are reported only for all debit, so Proposition 1 is applied there;
        # for signature and PIN the table shows the merchant price against issuer cost only.
        full = label == "All debit"
        p_b = -rewards if full else np.nan
        total = ps + p_b if full else np.nan
        margin = total - c if full else np.nan
        rows.append(dict(
            transaction=label,
            merchant_price_pS=ps,
            cardholder_price_pB=p_b,
            total_price=total,
            issuer_cost_c=c,
            margin=margin,
            lerner=margin / total,
            implied_total_elasticity=total / margin,
            implied_eta_S=ps / margin,
            implied_eta_B=p_b / margin,
            merchant_price_over_cost=ps / c,
            avg_purchase=ticket if full else np.nan,
            fee_share_of_purchase=share if full else np.nan,
        ))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "price_structure_2009.csv", index=False)
    print("Wrote price_structure_2009.csv")
    return df


def interchange_series(net):
    """Merchant-side price by issuer group, 2009-2024."""
    fee = net[net.measure == "fee"].pivot_table(index="period", columns=["network", "group"],
                                                values="value")
    fee.columns = [f"{n}_{g}" for n, g in fee.columns]
    order = ["2009", "2011 Jan-Sep", "2011 Q4"] + [str(y) for y in range(2012, 2025)]
    fee = fee.reindex([p for p in order if p in fee.index])
    fee.index.name = "period"
    fee.to_csv(OUT / "interchange_by_group.csv")
    print(f"Wrote interchange_by_group.csv ({len(fee)} periods)")
    return fee


def lost_interchange(xls, net, fee, quotes):
    """Interchange revenue covered issuers gave up each year, relative to the pre-cap fee."""
    t1, y1, c1 = read_report_table(xls, "1")
    t3, y3, c3 = read_report_table(xls, "3")
    t5, y5, c5 = read_report_table(xls, "5")
    pre = quotes["covered_fee_2011_jan_sep"]
    # Check: the Jan-Sep 2011 all-issuer fee (Table 5) split by the exempt share and exempt fee
    all_pre = report_value(t5, y5, c5, "All transactions", "2011: Q1-Q3", "Fee per")
    ex_share = net.query("period == @PRE_CAP_PERIOD and network == 'all' and group == 'exempt' "
                         "and measure == 'share_number'").value.iloc[0]
    implied = (all_pre - ex_share * fee.loc[PRE_CAP_PERIOD, "all_exempt"]) / (1 - ex_share)
    print(f"Covered issuers' fee before the cap: ${pre:.2f} (Fed report text); implied by Table 5 "
          f"and the exempt share: ${implied:.3f}; network file, rounded: "
          f"${fee.loc[PRE_CAP_PERIOD, 'all_covered']:.2f}")
    share = net[(net.measure == "share_number") & (net.network == "all") & (net.group == "covered")]
    share = share.set_index("period")["value"]
    rows = []
    for y in range(FIRST_FULL_CAP_YEAR, 2024):
        try:
            n_cov = report_value(t3, y3, c3, "Covered transactions", y, "Number")
            f = report_value(t5, y5, c5, "Covered transactions", y, "Fee per")
            how = "Fed Tables 3 and 5"
        except (KeyError, ValueError):
            n_cov = np.nan
        if not np.isfinite(n_cov):
            n_cov = report_value(t1, y1, c1, "All transactions", y, "Number") * share[str(y)]
            f = fee.loc[str(y), "all_covered"]
            how = "Fed Table 1 x covered share; fee from network file"
        rows.append(dict(year=y, covered_transactions_bn=n_cov, covered_fee=f, pre_cap_fee=pre,
                         fee_cut=pre - f, lost_interchange_bn=n_cov * (pre - f), source=how))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "lost_interchange.csv", index=False)
    print(f"Wrote lost_interchange.csv: {len(df)} years, "
          f"{df.lost_interchange_bn.iloc[0]:.2f} bn dollars in {FIRST_FULL_CAP_YEAR}")
    return df


def cap_level(fee_ticket, quotes):
    return quotes["cap_fixed"] + quotes["cap_ad_valorem"] * fee_ticket + quotes["cap_fraud_adjustment"]


def plot_interchange(fee, quotes):
    xs = list(range(len(fee)))
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.plot(xs, fee["all_exempt"], marker="o", color="#b5651d", label="Exempt issuers (under $10 billion)")
    ax.plot(xs, fee["all_covered"], marker="o", color="#1f5f8b", label="Covered issuers ($10 billion and up)")
    ax.plot(xs, fee["all_all"], color="#888888", ls="--", lw=1, label="All issuers")
    cap = cap_level(38.0, quotes)
    ax.axhline(cap, color="#1f5f8b", lw=0.8, ls=":")
    ax.text(len(xs) - 1, cap + 0.012, "cap on a $38 purchase, with fraud adjustment", ha="right", fontsize=8, color="#1f5f8b")
    ax.axvline(1.5, color="#444444", lw=0.8)
    ax.text(1.55, 0.62, "cap takes effect\nOct 1, 2011", fontsize=8, va="top")
    ax.set_xticks(xs)
    ax.set_xticklabels([p.replace(" Jan-Sep", "\nJan-Sep").replace(" Q4", "\nQ4") for p in fee.index],
                       fontsize=7)
    ax.set_ylabel("Average interchange fee per transaction ($)")
    ax.set_ylim(0, 0.65)
    ax.set_title("What the merchant side pays on a debit card swipe", fontsize=11)
    ax.legend(fontsize=8, loc="lower left", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "interchange_by_group.png", dpi=160)
    plt.close(fig)
    print("Wrote interchange_by_group.png")


def main():
    OUT.mkdir(exist_ok=True)
    quotes = load_quotes()
    xls = pd.read_excel(RAW / "regiireportsdata.xls", sheet_name=None, header=None)
    print(f"Loaded regiireportsdata.xls: {len(xls)} tables")
    ps = price_structure_2009(xls, quotes)
    print(ps.round(3).to_string(index=False))
    net = parse_network_csv()
    fee = interchange_series(net)
    print(fee.round(3).to_string())
    lost = lost_interchange(xls, net, fee, quotes)
    print(lost.round(3).to_string(index=False))
    plot_interchange(fee, quotes)


if __name__ == "__main__":
    main()
