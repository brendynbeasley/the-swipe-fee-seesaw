# Methods review: Rochet and Tirole (2003)

- **Paper:** Jean-Charles Rochet and Jean Tirole, "Platform Competition in Two-Sided Markets," *Journal of the
  European Economic Association* 1(4), June 2003, pp. 990–1029.
- **Statistical focus:** the price-structure formula of Proposition 1 (eqs. 1–5) and the comparative statics of
  Proposition 5, which together imply that capping one side's price raises the other side's price by part of the
  cut; and the classification of fifteen industries' business models in Table 1, the paper's only evidence.
- **Review standard:** internal consistency of the formal results, explicitness of assumptions, and the testability
  of predictions, with the evidence in Section 7 judged against ordinary standards for documenting empirical claims.
- **What was read:** the full published text in a copy carrying the journal's page headers, hosted on a University
  of Granada faculty page. Sections 1, 2, 3.3–3.4, 4, 6, 7 and 8 were read in full; Section 5 was read for the
  statement of Proposition 6; the Appendix proofs were not read. I did not search for, and do not cite, any
  published correction.

## Methods summary

### Research design

A formal model. Buyers and sellers each draw a private per-transaction benefit, join a platform if the benefit
exceeds the platform's per-transaction price, and transaction volume is the product of the two sides'
quasi-demands, $`D^B(p^B)\,D^S(p^S)`$. The paper solves for prices under a private monopoly, a Ramsey planner, two
competing for-profit platforms and two competing nonprofit associations, then extends to fixed fees (Section 6).
Section 7 illustrates the results with seven short case studies.

### Sampling strategy

Does not apply to the model. The case studies and Table 1 are chosen as illustrations; no selection rule is given.

### Sample size

Does not apply to the model. Table 1 lists fifteen products in five groups; Section 7 has seven case studies.

### Inclusion and exclusion criteria

Not stated for Table 1 or Section 7. Footnote 1 explains a few entries not discussed further (social gatherings,
real estate, shopping malls, coupon books, browsers).

### Independent and dependent variables

In the model, prices $`p^B, p^S`$ are chosen; volumes and profits are outcomes; elasticities $`\eta^B, \eta^S`$,
the own-brand elasticity $`\eta^B_o`$, the singlehoming index $`\sigma`$, and the cost $`c`$ are primitives. The
case studies have no measured variables.

### Statistical methods

None. The "statistics" are first-order conditions and comparative statics under stated assumptions. Log-concavity
of $`D^B`$ and $`D^S`$ is assumed for Proposition 1 and Proposition 5(1); independence of buyer and seller
benefits gives the multiplicative volume (footnote 8 notes the general case); Proposition 5(2) needs an extra
regularity condition; Proposition 6 needs a Hotelling specification and a second-order condition.

### Reported effect sizes

None estimated. Proposition 6 gives closed forms for linear demands, and Section 7 cites a few industry figures
(below).

### Confidence intervals

Do not apply. No estimates are reported.

### p-values

Do not apply.

### Missing data treatment

Does not apply. The case-study figures are cited to trade press without discussion of coverage.

### Stated limitations

The authors say the basic model fits the credit card market best (Section 2), that their monopoly volume formula
relies on independence of the two sides' benefits (footnote 8), that a rigorous test of implications 3 to 6 is
beyond the paper and that Section 7 is casual empiricism (Section 7), and that they have no hard data for some case
studies (footnote 28). Section 8 lists the conditions under which a market is not two-sided at all (coordinated
purchases, pass-through between the sides).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Monopoly price structure | $`p^B + p^S - c = p^B/\eta^B = p^S/\eta^S`$ | Section 2.1, eq. (1); Prop. 1 | Profit-maximizing per-transaction prices for one platform | That actual platforms set prices this way, or the size of any elasticity |
| Total price level | $`(p - c)/p = 1/\eta`$, $`\eta = \eta^B + \eta^S > 1`$ | Eq. (2); Prop. 1(i) | Lerner rule for the summed elasticity | Anything about competition between platforms |
| Ramsey structure | $`p^B + p^S = c`$; $`(p^B/\eta^B)(V^B/D^B) = (p^S/\eta^S)(V^S/D^S)`$ (bracketed terms) | Eqs. (6)–(7); Prop. 2 | Welfare-maximizing split under budget balance | That private structures are biased in a particular direction |
| Competing proprietary platforms | $`p^B + p^S - c = p^B/\eta^B_o = p^S/(\eta^S/\sigma)`$ | Prop. 3 | Symmetric equilibrium with seller multihoming | Existence or uniqueness outside the symmetric case |
| Competing associations | $`p^B + p^S = c + m`$; $`p^B/(\sigma\eta^B_o) = p^S/\eta^S`$ | Eq. (22); Prop. 4 | Equilibrium with member margin $`m`$ | Efficiency, even as $`m \to 0`$ |
| Comparative statics | Marquee buyers raise $`p^S`$ and lower $`p^B`$; captive buyers do the reverse; more buyer multihoming lowers $`p^S`$ | Prop. 5 | Direction of price changes under log-concave demand | Magnitudes, which depend on demand curvature |
| Linear-demand equivalence | Same structure under monopoly, competing platforms and associations; Ramsey optimal if seller demand is also linear | Prop. 6 | A benchmark case | Generality beyond linear demand |
| Second-order condition | Holds iff $`d/D < (1 + \sqrt{5})/2`$ | Prop. 6(4) | Validity of the linear-demand equilibrium | Behavior outside the Hotelling setup |
| Fixed-fee extension | $`p^B + p^S - c = p^B/[\eta^B_o(1 + \eta^S_N)] = p^S/[\eta^S + \eta^B_S(1 + \eta^S_N)]`$ | Prop. 7 | Robustness to fixed fees with buyer singlehoming | Multihoming with fixed fees |
| Business-model classification | 15 products; loss leader and profit side for each | Table 1 | Conventional wisdom from the trade press | Any measured price, cost or elasticity |
| Card association membership | Over 6,000 bank and nonbank members | Section 7.1 | Size of Visa and MasterCard associations at the time | Pricing behavior |
| Handheld OS market share | Palm about 75% in the US; OS fee about 10% of hardware wholesale price ($5–$15) | Footnote 28 | Context for the operating-system case | A verified price structure (authors say no hard data) |
| Developer kit price | About $600 | Footnote 29 | Context for the text-processing case | Any elasticity |
| PlayStation development seat | About $10,000 per seat | Section 7.4 | Context for console pricing to developers | Causal role in Sony's success |

## Interpretation notes

- Proposition 1 is an accounting identity of optimization, not an empirical claim. Observed prices can always be
  read back into elasticities, as the README does for 2009 debit cards, so the formula alone cannot be rejected
  by price data. Testable content comes from comparative statics such as Proposition 5.
- With a negative cardholder price, as in rewards cards, the implied cardholder elasticity is negative. The
  formula still holds but the reading "the less elastic side pays more" needs care.
- The paper's own payment-card discussion (Section 7.1) predicts that merchant acceptance would become more
  elastic as online debit spread (footnote 18). It does not discuss regulation of the interchange fee, which is
  the setting used in this repository.
- Proposition 6's statement that policy aimed at the price structure is unlikely to be solidly grounded without
  detailed demand information bears directly on the Durbin cap, which set the structure by statute.

## Unanswered questions

- How large is the curvature term $`m'(p)`$ in real platforms, which sets how much of a capped side's cut moves to
  the other side.
- Whether issuer competition (the association model's member margin $`m`$) or platform market power governs
  pass-through in payment cards.
- How the results change when sellers can surcharge, which Section 8 treats only informally.
- How robust the predictions are to the form of user heterogeneity; Weyl (2010, *AER*) argues they depend heavily
  on it.

## Items requiring expert verification

- The proofs of Propositions 5 and 6 in the Appendix, which were not read for this review.
- Whether the regularity condition in Proposition 5(2) is satisfied in plausible payment-card demand systems.
- The figures in footnotes 28 and 29 and Section 7.4, which cite trade press and a dated web page.
- The equation, footnote and section numbers in the extraction table, which were taken from one hosted copy and
  should be checked against the journal's own pagination.

This repository does not reproduce anything in the paper, which has no data. It takes the Proposition 5 mechanism
to US debit cards after the 2011 interchange cap and estimates how much of the merchant-side cut covered banks
recovered from depositors.
