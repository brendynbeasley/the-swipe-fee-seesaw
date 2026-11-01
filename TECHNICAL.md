# Technical notes

This is the technical companion to the [README](README.md). Every number below is written by the two scripts in
`src/` into `results/*.csv`; [results/FINDINGS.md](results/FINDINGS.md) reproduces every table.

## The original study

Jean-Charles Rochet and Jean Tirole, "Platform Competition in Two-Sided Markets," *Journal of the European Economic
Association* 1(4), June 2003, pp. 990–1029. The paper is theoretical and has no data. Its headline result
(Proposition 1, eqs. 1–5) is that a monopoly platform charging per-transaction prices $`p^B`$ and $`p^S`$ sets the
total by a Lerner rule in the summed elasticity and splits it by the elasticities themselves:

```math
p^B + p^S - c = \frac{p^B}{\eta^B} = \frac{p^S}{\eta^S}, \qquad \frac{p - c}{p} = \frac{1}{\eta^B + \eta^S}
```

Propositions 3, 4 and 7 extend the formula to competing platforms, nonprofit associations and fixed fees, and
Proposition 5 gives the comparative statics behind the test here: with log-concave demand, a shift that raises the
seller price (marquee buyers) lowers the buyer price, and the reverse. Section 7 applies the theory to credit and debit cards, offers only casual
evidence, and leaves econometric tests of its implications to future work.

## Headline results

| | Estimate | Standard error | 95% interval |
|---|---|---|---|
| Covered issuers' interchange fee, Jan–Sep 2011 → Q4 2011 | $0.50 → $0.24 | | |
| Interchange lost by covered issuers, 2012 | $8.63 billion | | |
| Interchange lost per covered deposit account, 2012–13 average | $25.47 | | |
| Fee per account, covered − exempt, 2012–13, account-weighted | +$4.87 | 6.24 | |
| Same, unweighted | +$1.59 | 2.88 | |
| Offset ratio $`\rho`$, 2012–13 | 0.19 | | −0.29 to 0.67 |
| Test of $`\rho = 1`$, 2012–13 | z = −3.30 | | |
| Offset ratio $`\rho`$, 2017–19 | 0.37 | | −0.41 to 1.15 |

The merchant-side price fell by half at covered banks. The cardholder-side price, measured as service charges per
deposit account, rose by an amount that is not distinguishable from zero and is distinguishable from full recovery
in 2012–13. The long-run estimate is larger and less precise. The positive weighted estimates come from Wells Fargo,
whose service charges rose 3% (from $4.92 billion to $5.08 billion, 2010 to 2013) while its reported deposit
accounts fell from 108.6 million to 78.8 million; without Wells Fargo every weighted window estimate is negative.
Service charges per $1,000 of deposits fell at covered banks relative to exempt banks in every window.

## Data

All files were downloaded on November 1, 2026 and are committed in `data/raw/`.

| File | Source | Used for |
|---|---|---|
| `regiireportsdata.xls` | Federal Reserve Board, data behind the biennial Regulation II interchange fee reports (federalreserve.gov/paymentsystems/files/) | Transactions, interchange revenue and fee per transaction (Tables 1, 3, 4, 5); issuer ACS cost (Table 13) |
| `Avg_IF_by_PCN.csv` | Federal Reserve Board, average debit interchange fee by payment card network | Covered and exempt fee per transaction and covered share of transactions, 2009–2024 |
| `fed_report_quotes.csv` | Text of the Board's 2009 report (June 2011) and 2011 report (March 5, 2013) | Rewards per transaction (4 cents), covered issuers' pre-cap fee (50 cents), the cap's terms |
| `fdic_q4_2006_2023.csv.gz` | FDIC BankFind Suite, `api.fdic.gov/banks/financials`, fourth-quarter reports | Service charges on deposit accounts (ISERCHG), deposit account counts (DEPSMB + DEPLGB), domestic deposits, assets, top holder (RSSDHCR), asset-concentration group (SPECGRP) |

`src/account_fees.py` refetches the FDIC file if it is missing (18 API calls, about a minute).

## Method

Rules fixed before estimating, with one revision noted.

- The unit is the regulatory top holder (RSSDHCR), or the bank itself if it has none. Assets are summed over all
  insured subsidiaries.
- Covered means summed assets of $10 billion or more at the end of 2010. The comparison group is $1–10 billion.
  Groups that cross $10 billion while in the panel are dropped.
- Credit card banks (SPECGRP = 3) are excluded from the sums. Groups with 2010 service charges per account outside
  $10–$400, or under 10,000 accounts, are dropped as non-retail.
- A group must be present in every year 2010–2013. Its panel ends at its first gap or first year in which log
  accounts move more than log(1.4) beyond log deposits. Groups where banks without service-charge data hold more
  than 5% of accounts are dropped.
- The outcome is winsorized at 1%/99%. Post-period windows are 2011 (cap from October 1), 2012–13, 2014–16 and
  2017–19.
- Revision. A first pass measured unreported accounts against all subsidiaries, which dropped JPMorgan Chase for its
  credit card bank, and required presence through 2019 with no truncation. I corrected the first, replaced the second
  with the 2010–2013 presence rule and truncation, and added the account-count break rule before looking at the new
  estimates. The first pass reached the same conclusion, a weighted 2012–13 estimate well short of full recovery
  and not distinguishable from zero.

The estimating equations, with standard errors clustered by group:

```math
\begin{aligned}
F_{it} &= \alpha_i + \lambda_t + \sum_{k \neq 2010} \beta_k\, \text{Covered}_i \mathbf{1}[t = k] + \varepsilon_{it} \\
F_{it} &= \alpha_i + \lambda_t + \sum_{w} \beta_w\, \text{Covered}_i \mathbf{1}[t \in w] + \varepsilon_{it}
\end{aligned}
```

The offset ratio divides the account-weighted window estimate by the interchange lost per covered account, where
$`f_t`$ is the covered fee (Fed Table 5, or the network file for 2012), $`N_t`$ covered transactions (Table 3, or
Table 1 times the covered share for 2012), and $`A_t`$ deposit accounts at covered groups whose fee per account is
in the retail band:

```math
L_t = \frac{(0.50 - f_t)\, N_t}{A_t}, \qquad \hat\rho_w = \frac{\hat\beta_w}{\bar L_w}, \qquad \operatorname{se}(\hat\rho_w) = \frac{\operatorname{se}(\hat\beta_w)}{\bar L_w}
```

The 2009 price-structure calculation applies Proposition 1 with $`p^S`$ = 0.431 (Table 4), $`p^B`$ = −0.04 (rewards),
and $`c`$ = 0.077 (Table 13, covered issuers' ACS cost excluding fraud losses).

## Full test statistics

Two-way fixed-effects window estimates, 341 groups (51 covered), 2,998 group-years (`results/did_windows.csv`).

| Outcome | Weights | 2011 | 2012–13 | 2014–16 | 2017–19 |
|---|---|---|---|---|---|
| Fee per account ($) | none | −0.84 (2.39) | 1.59 (2.88) | 2.85 (3.52) | 1.97 (4.27) |
| Fee per account ($) | 2010 accounts | −2.78 (3.18) | 4.87 (6.24) | 9.80 (11.04) | 11.01 (11.78) |
| Log fee per account | none | −0.006 (0.029) | 0.022 (0.040) | 0.054 (0.047) | 0.039 (0.060) |
| Log fee per account | 2010 accounts | −0.059 (0.040) | 0.089 (0.092) | 0.166 (0.166) | 0.182 (0.179) |
| Fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | 2010 accounts | −1.59 (3.25) | 0.79 (4.55) | 1.24 (4.96) | −1.62 (6.74) |
| Fee per account, without Wells Fargo | 2010 accounts | −2.71 (4.66) | −1.79 (4.53) | −3.40 (4.98) | −4.07 (4.76) |
| Fee per $1,000 deposits | none | −0.40 (0.10) | −0.41 (0.14) | −0.48 (0.17) | −0.48 (0.22) |
| Fee per $1,000 deposits | 2010 accounts | −0.99 (0.20) | −0.99 (0.26) | −0.89 (0.41) | −0.93 (0.31) |

Year-by-year offset ratios (`results/offset_ratio.csv`): 2012 0.12 (z for $`\rho`$ = 1 is −4.82), 2013 0.26
(−2.33), 2014 0.30, 2015 0.39, 2016 0.43, 2017 0.44, 2018 0.33, 2019 0.35. None is distinguishable from zero.

Pre-trends. The deposits-based outcome, available from 2006 for 233 groups, rejects equal pre-trends (joint test of
2006–2009 coefficients, p = 0.024 unweighted and p < 0.001 weighted). Covered groups' fees per deposit dollar were
already falling relative to exempt groups into 2010, and fell further as deposits surged at large banks in 2011.
The per-account outcome has no pre-period.

Account-count changes. The break rule catches a one-year jump of 40% beyond deposits. Wells Fargo's accounts fell
27% in all, spread over 2012 and 2013, while its deposits grew, which the rule does not catch; `largest_covered_banks.csv`
reports each large bank's service charges and accounts in 2010 and 2013 so the source of each change is visible,
and the without-Wells Fargo row above shows how much the weighted estimates depend on it.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/price_structure.py
python src/account_fees.py
```

The first script writes the price-structure, interchange and lost-revenue tables and `interchange_by_group.png`; the
second needs `results/lost_interchange.csv` from the first.

## References

- Armstrong, M. (2006). Competition in two-sided markets. *RAND Journal of Economics* 37(3), 668–691.
- Federal Reserve Board (2011). 2009 Interchange Revenue, Covered Issuer Cost, and Covered Issuer and Merchant
  Fraud Loss Related to Debit Card Transactions.
- Federal Reserve Board (2013). 2011 Interchange Fee Revenue, Covered Issuer Costs, and Covered Issuer and Merchant
  Fraud Losses Related to Debit Card Transactions.
- Kay, B., Manuszak, M. D. & Vojtech, C. M. (2014). Bank profitability and debit card interchange regulation: bank
  responses to the Durbin Amendment. Working paper.
- Manuszak, M. D. & Wozniak, K. (2017). The impact of price controls in two-sided markets: evidence from US debit
  card interchange fee regulation. FEDS 2017-074.
- *Ohio v. American Express Co.*, 585 U.S. (2018).
- Rochet, J.-C. & Tirole, J. (2003). Platform competition in two-sided markets. *JEEA* 1(4), 990–1029.
- Weyl, E. G. (2010). A price theory of multi-sided platforms. *American Economic Review* 100(4), 1642–1672.
