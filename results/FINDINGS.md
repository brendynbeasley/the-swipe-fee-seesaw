# Rochet and Tirole (2003) on the Durbin cap: findings

## In plain English

Rochet and Tirole's theory says that a card network sets two prices for each swipe, one for the store and one for
the shopper, and that if a regulator cuts one, the network raises the other by part of the cut. In October 2011
federal law cut the store's price on debit cards issued by banks with $10 billion or more in assets.

- **The store's price fell by half and stayed down.** Covered banks such as JPMorgan Chase, Bank of America and
  Wells Fargo went from about 50 cents a swipe to 24 cents in the last quarter of 2011 and about 23 cents ever since.
  Small exempt banks kept collecting 43 cents, and 51 cents by 2024.
- **The shopper's price barely moved on average.** Deposit-account fees at covered banks rose by about $5 a year per
  account relative to small banks in 2012 and 2013, roughly a fifth of the roughly $25 per account the banks lost
  in swipe revenue. That estimate cannot be told apart from zero, but it is clearly less than full recovery.
- **The small average rise rests on Wells Fargo.** Its fee per account rose $19, but its service charges rose only
  3% while its reported accounts fell from 109 million to 79 million. Without Wells Fargo the account-weighted
  estimate is negative. TD Bank raised its service charges outright; Bank of America, U.S. Bancorp and PNC collected
  less per account in 2013 than in 2010.
- **Over ten years the recovered share drifts up to about 37%, with wide uncertainty, and it too depends on Wells Fargo.**

A friendlier tour is in the [README](../README.md); the method and test statistics are in
[TECHNICAL.md](../TECHNICAL.md).

## Key to the labels

*Covered* = holding company with $10 billion or more of insured-bank assets at the end of 2010, subject to the
Regulation II cap. *Exempt* = $1 billion to $10 billion. *Fee per account* = annual service charges on deposit
accounts divided by year-end deposit accounts, in dollars. *Fee per $1,000 deposits* = service charges per $1,000
of domestic deposits. *dual* = signature (dual-message) networks; *single* = PIN (single-message) networks; *all* =
all networks. *beta* = covered-minus-exempt difference relative to 2010 from a regression with group and year fixed
effects; *se* = standard error clustered by holding company. *lost_per_account* = interchange covered issuers gave
up per deposit account at covered groups, relative to the 50-cent pre-cap fee. *rho* = offset ratio, the
account-weighted beta divided by lost_per_account; *rho_lo*, *rho_hi* = 95% interval; *z_rho_eq_1* = z statistic
for full recovery. Dollar amounts in `_bn` columns are billions; `_m` columns are millions. In
`largest_covered_banks.csv`, *service_charges* = annual service charges on deposit accounts, in billions of
dollars, and a blank 2019 fee means the group's panel ended at a merger or reporting break, and
BB&T's 2019 figure is Truist after the SunTrust merger.

## Every table

### `price_structure_2009.csv`

| transaction | merchant_price_pS | cardholder_price_pB | total_price | issuer_cost_c | margin | lerner | implied_total_elasticity | implied_eta_S | implied_eta_B | merchant_price_over_cost | avg_purchase | fee_share_of_purchase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All debit | 0.431 | -0.040 | 0.391 | 0.077 | 0.314 | 0.803 | 1.245 | 1.373 | -0.127 | 5.594 | 38.18 | 0.011 |
| Signature (dual-message) | 0.550 |  |  | 0.078 |  |  |  |  |  | 7.045 |  |  |
| PIN (single-message) | 0.235 |  |  | 0.047 |  |  |  |  |  | 5.010 |  |  |

### `interchange_by_group.csv`

| period | all_all | all_covered | all_exempt | dual_all | dual_covered | dual_exempt | single_all | single_covered | single_exempt |
|---|---|---|---|---|---|---|---|---|---|
| 2009 | 0.430 |  |  | 0.550 |  |  | 0.230 |  |  |
| 2011 Jan-Sep | 0.480 | 0.510 | 0.440 | 0.570 | 0.580 | 0.530 | 0.330 | 0.340 | 0.320 |
| 2011 Q4 | 0.300 | 0.240 | 0.430 | 0.330 | 0.240 | 0.510 | 0.260 | 0.230 | 0.310 |
| 2012 | 0.310 | 0.240 | 0.430 | 0.330 | 0.250 | 0.510 | 0.260 | 0.240 | 0.300 |
| 2013 | 0.300 | 0.230 | 0.430 | 0.330 | 0.230 | 0.500 | 0.250 | 0.240 | 0.280 |
| 2014 | 0.310 | 0.230 | 0.430 | 0.340 | 0.230 | 0.500 | 0.250 | 0.240 | 0.260 |
| 2015 | 0.300 | 0.230 | 0.430 | 0.340 | 0.230 | 0.510 | 0.240 | 0.240 | 0.260 |
| 2016 | 0.300 | 0.230 | 0.420 | 0.330 | 0.230 | 0.510 | 0.240 | 0.240 | 0.260 |
| 2017 | 0.300 | 0.230 | 0.430 | 0.340 | 0.220 | 0.520 | 0.240 | 0.240 | 0.250 |
| 2018 | 0.310 | 0.230 | 0.440 | 0.340 | 0.220 | 0.540 | 0.240 | 0.240 | 0.250 |
| 2019 | 0.310 | 0.230 | 0.440 | 0.340 | 0.220 | 0.540 | 0.240 | 0.240 | 0.250 |
| 2020 | 0.330 | 0.230 | 0.480 | 0.370 | 0.220 | 0.600 | 0.250 | 0.240 | 0.260 |
| 2021 | 0.340 | 0.230 | 0.520 | 0.390 | 0.230 | 0.640 | 0.250 | 0.240 | 0.270 |
| 2022 | 0.340 | 0.230 | 0.520 | 0.380 | 0.220 | 0.640 | 0.250 | 0.240 | 0.270 |
| 2023 | 0.340 | 0.230 | 0.510 | 0.370 | 0.220 | 0.620 | 0.250 | 0.240 | 0.270 |
| 2024 | 0.340 | 0.230 | 0.510 | 0.370 | 0.220 | 0.610 | 0.250 | 0.240 | 0.260 |

### `lost_interchange.csv`

| year | covered_transactions_bn | covered_fee | pre_cap_fee | fee_cut | lost_interchange_bn | source |
|---|---|---|---|---|---|---|
| 2012 | 33.18 | 0.240 | 0.500 | 0.260 | 8.626 | Fed Table 1 x covered share; fee from network file |
| 2013 | 33.76 | 0.233 | 0.500 | 0.267 | 9.012 | Fed Tables 3 and 5 |
| 2014 | 35.55 | 0.233 | 0.500 | 0.267 | 9.478 | Fed Tables 3 and 5 |
| 2015 | 38.05 | 0.232 | 0.500 | 0.268 | 10.21 | Fed Tables 3 and 5 |
| 2016 | 40.80 | 0.230 | 0.500 | 0.270 | 11.01 | Fed Tables 3 and 5 |
| 2017 | 43.22 | 0.229 | 0.500 | 0.271 | 11.73 | Fed Tables 3 and 5 |
| 2018 | 46.51 | 0.228 | 0.500 | 0.272 | 12.67 | Fed Tables 3 and 5 |
| 2019 | 49.89 | 0.227 | 0.500 | 0.273 | 13.64 | Fed Tables 3 and 5 |
| 2020 | 49.18 | 0.229 | 0.500 | 0.271 | 13.32 | Fed Tables 3 and 5 |
| 2021 | 56.19 | 0.230 | 0.500 | 0.270 | 15.17 | Fed Tables 3 and 5 |
| 2022 | 58.05 | 0.229 | 0.500 | 0.271 | 15.74 | Fed Tables 3 and 5 |
| 2023 | 61.67 | 0.227 | 0.500 | 0.273 | 16.81 | Fed Tables 3 and 5 |

### `sample_counts.csv`

| rule | dropped_covered | dropped_exempt |
|---|---|---|
| 2010 fee per account outside $10-$400, or under 10,000 accounts | 12 | 39 |
| not present, without a break, in every year 2010-2013 | 8 | 85 |
| banks without service-charge data hold over 5% of accounts | 2 | 4 |
| crossed the $10 billion line while in the panel | 2 | 37 |
| kept | 51 | 290 |

### `fee_means_by_group.csv`

| covered | year | mean_fee | weighted_fee | groups | accounts_m |
|---|---|---|---|---|---|
| 0 | 2010 | 76.58 | 75.98 | 290 | 26.86 |
| 0 | 2011 | 71.92 | 71.56 | 290 | 26.81 |
| 0 | 2012 | 69.53 | 68.67 | 290 | 27.14 |
| 0 | 2013 | 69.38 | 68.19 | 290 | 27.40 |
| 0 | 2014 | 67.26 | 66.59 | 269 | 26.37 |
| 0 | 2015 | 65.21 | 64.48 | 253 | 25.19 |
| 0 | 2016 | 64.92 | 65.13 | 240 | 24.26 |
| 0 | 2017 | 64.08 | 64.93 | 219 | 22.74 |
| 0 | 2018 | 62.84 | 64.97 | 203 | 22.38 |
| 0 | 2019 | 63.00 | 65.11 | 189 | 22.00 |
| 1 | 2010 | 90.83 | 80.14 | 51 | 328.34 |
| 1 | 2011 | 85.32 | 72.94 | 51 | 332.73 |
| 1 | 2012 | 85.45 | 75.66 | 51 | 326.26 |
| 1 | 2013 | 85.14 | 79.26 | 51 | 311.18 |
| 1 | 2014 | 83.34 | 77.58 | 50 | 314.84 |
| 1 | 2015 | 81.32 | 77.53 | 46 | 310.79 |
| 1 | 2016 | 81.34 | 78.95 | 44 | 313.72 |
| 1 | 2017 | 77.83 | 79.53 | 42 | 316.34 |
| 1 | 2018 | 75.71 | 77.16 | 41 | 320.14 |
| 1 | 2019 | 74.00 | 74.64 | 38 | 264.63 |

### `did_windows.csv`

| outcome | weights | groups | covered_groups | window | beta | se | p |
|---|---|---|---|---|---|---|---|
| fee per account ($/yr) | unweighted | 341 | 51 | 2011 | -0.845 | 2.393 | 0.724 |
| fee per account ($/yr) | unweighted | 341 | 51 | 2012-13 | 1.591 | 2.884 | 0.581 |
| fee per account ($/yr) | unweighted | 341 | 51 | 2014-16 | 2.846 | 3.518 | 0.419 |
| fee per account ($/yr) | unweighted | 341 | 51 | 2017-19 | 1.972 | 4.274 | 0.645 |
| fee per account ($/yr) | account-weighted | 341 | 51 | 2011 | -2.783 | 3.177 | 0.381 |
| fee per account ($/yr) | account-weighted | 341 | 51 | 2012-13 | 4.870 | 6.240 | 0.435 |
| fee per account ($/yr) | account-weighted | 341 | 51 | 2014-16 | 9.801 | 11.04 | 0.375 |
| fee per account ($/yr) | account-weighted | 341 | 51 | 2017-19 | 11.01 | 11.78 | 0.350 |
| log fee per account | unweighted | 341 | 51 | 2011 | -0.006 | 0.029 | 0.832 |
| log fee per account | unweighted | 341 | 51 | 2012-13 | 0.022 | 0.040 | 0.589 |
| log fee per account | unweighted | 341 | 51 | 2014-16 | 0.054 | 0.047 | 0.252 |
| log fee per account | unweighted | 341 | 51 | 2017-19 | 0.039 | 0.060 | 0.514 |
| log fee per account | account-weighted | 341 | 51 | 2011 | -0.059 | 0.040 | 0.143 |
| log fee per account | account-weighted | 341 | 51 | 2012-13 | 0.089 | 0.092 | 0.329 |
| log fee per account | account-weighted | 341 | 51 | 2014-16 | 0.166 | 0.166 | 0.317 |
| log fee per account | account-weighted | 341 | 51 | 2017-19 | 0.182 | 0.179 | 0.312 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | unweighted | 338 | 48 | 2011 | -0.768 | 2.497 | 0.758 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | unweighted | 338 | 48 | 2012-13 | 1.455 | 3.003 | 0.628 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | unweighted | 338 | 48 | 2014-16 | 2.560 | 3.611 | 0.478 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | unweighted | 338 | 48 | 2017-19 | 1.439 | 4.419 | 0.745 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | account-weighted | 338 | 48 | 2011 | -1.593 | 3.254 | 0.624 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | account-weighted | 338 | 48 | 2012-13 | 0.793 | 4.546 | 0.862 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | account-weighted | 338 | 48 | 2014-16 | 1.239 | 4.961 | 0.803 |
| fee per account, without JPMorgan Chase, Bank of America, Wells Fargo | account-weighted | 338 | 48 | 2017-19 | -1.617 | 6.740 | 0.810 |
| fee per account, without Wells Fargo | unweighted | 340 | 50 | 2011 | -0.808 | 2.434 | 0.740 |
| fee per account, without Wells Fargo | unweighted | 340 | 50 | 2012-13 | 1.264 | 2.914 | 0.664 |
| fee per account, without Wells Fargo | unweighted | 340 | 50 | 2014-16 | 2.164 | 3.504 | 0.537 |
| fee per account, without Wells Fargo | unweighted | 340 | 50 | 2017-19 | 1.151 | 4.263 | 0.787 |
| fee per account, without Wells Fargo | account-weighted | 340 | 50 | 2011 | -2.709 | 4.664 | 0.561 |
| fee per account, without Wells Fargo | account-weighted | 340 | 50 | 2012-13 | -1.788 | 4.527 | 0.693 |
| fee per account, without Wells Fargo | account-weighted | 340 | 50 | 2014-16 | -3.397 | 4.981 | 0.495 |
| fee per account, without Wells Fargo | account-weighted | 340 | 50 | 2017-19 | -4.067 | 4.755 | 0.392 |
| fee per $1,000 of domestic deposits | unweighted | 341 | 51 | 2011 | -0.396 | 0.096 | 0.000 |
| fee per $1,000 of domestic deposits | unweighted | 341 | 51 | 2012-13 | -0.412 | 0.135 | 0.002 |
| fee per $1,000 of domestic deposits | unweighted | 341 | 51 | 2014-16 | -0.481 | 0.174 | 0.006 |
| fee per $1,000 of domestic deposits | unweighted | 341 | 51 | 2017-19 | -0.475 | 0.219 | 0.030 |
| fee per $1,000 of domestic deposits | account-weighted | 341 | 51 | 2011 | -0.994 | 0.195 | 0.000 |
| fee per $1,000 of domestic deposits | account-weighted | 341 | 51 | 2012-13 | -0.992 | 0.256 | 0.000 |
| fee per $1,000 of domestic deposits | account-weighted | 341 | 51 | 2014-16 | -0.892 | 0.406 | 0.028 |
| fee per $1,000 of domestic deposits | account-weighted | 341 | 51 | 2017-19 | -0.925 | 0.307 | 0.003 |

### `event_study_fee_per_account.csv`

| year | beta | se | weights | n |
|---|---|---|---|---|
| 2010 | 0 | 0 | unweighted | 2998 |
| 2011 | -0.845 | 2.395 | unweighted | 2998 |
| 2012 | 1.670 | 2.824 | unweighted | 2998 |
| 2013 | 1.511 | 3.095 | unweighted | 2998 |
| 2014 | 2.448 | 3.279 | unweighted | 2998 |
| 2015 | 3.584 | 3.646 | unweighted | 2998 |
| 2016 | 2.535 | 4.024 | unweighted | 2998 |
| 2017 | 3.038 | 4.252 | unweighted | 2998 |
| 2018 | 1.779 | 4.491 | unweighted | 2998 |
| 2019 | 0.989 | 4.420 | unweighted | 2998 |
| 2010 | 0 | 0 | account-weighted | 2998 |
| 2011 | -2.783 | 3.180 | account-weighted | 2998 |
| 2012 | 2.834 | 4.473 | account-weighted | 2998 |
| 2013 | 6.906 | 8.446 | account-weighted | 2998 |
| 2014 | 8.039 | 10.76 | account-weighted | 2998 |
| 2015 | 10.03 | 10.92 | account-weighted | 2998 |
| 2016 | 11.61 | 11.65 | account-weighted | 2998 |
| 2017 | 12.56 | 11.72 | account-weighted | 2998 |
| 2018 | 10.00 | 11.00 | account-weighted | 2998 |
| 2019 | 10.45 | 12.94 | account-weighted | 2998 |

### `event_study_fee_per_deposits.csv`

| year | beta | se | weights | pretrend_p | groups |
|---|---|---|---|---|---|
| 2006 | 0.141 | 0.330 | unweighted | 0.024 | 233 |
| 2007 | 0.349 | 0.294 | unweighted | 0.024 | 233 |
| 2008 | 0.256 | 0.288 | unweighted | 0.024 | 233 |
| 2009 | 0.352 | 0.122 | unweighted | 0.024 | 233 |
| 2010 | 0 | 0 | unweighted | 0.024 | 233 |
| 2011 | -0.462 | 0.102 | unweighted | 0.024 | 233 |
| 2012 | -0.442 | 0.154 | unweighted | 0.024 | 233 |
| 2013 | -0.440 | 0.165 | unweighted | 0.024 | 233 |
| 2014 | -0.451 | 0.186 | unweighted | 0.024 | 233 |
| 2015 | -0.410 | 0.204 | unweighted | 0.024 | 233 |
| 2016 | -0.464 | 0.221 | unweighted | 0.024 | 233 |
| 2017 | -0.361 | 0.226 | unweighted | 0.024 | 233 |
| 2018 | -0.354 | 0.239 | unweighted | 0.024 | 233 |
| 2019 | -0.405 | 0.252 | unweighted | 0.024 | 233 |
| 2006 | 1.933 | 1.100 | account-weighted | 0.000 | 233 |
| 2007 | 2.270 | 0.977 | account-weighted | 0.000 | 233 |
| 2008 | 0.019 | 1.628 | account-weighted | 0.000 | 233 |
| 2009 | 1.076 | 0.238 | account-weighted | 0.000 | 233 |
| 2010 | 0 | 0 | account-weighted | 0.000 | 233 |
| 2011 | -0.928 | 0.198 | account-weighted | 0.000 | 233 |
| 2012 | -0.886 | 0.263 | account-weighted | 0.000 | 233 |
| 2013 | -0.861 | 0.288 | account-weighted | 0.000 | 233 |
| 2014 | -0.782 | 0.431 | account-weighted | 0.000 | 233 |
| 2015 | -0.658 | 0.421 | account-weighted | 0.000 | 233 |
| 2016 | -0.718 | 0.407 | account-weighted | 0.000 | 233 |
| 2017 | -0.683 | 0.350 | account-weighted | 0.000 | 233 |
| 2018 | -0.730 | 0.323 | account-weighted | 0.000 | 233 |
| 2019 | -0.742 | 0.326 | account-weighted | 0.000 | 233 |

### `offset_ratio.csv`

| year | lost_interchange_bn | covered_accounts_all_m | lost_per_account | fee_increase_per_account | fee_increase_se | rho | rho_lo | rho_hi | z_rho_eq_0 | z_rho_eq_1 | sample_covered_accounts_m | extra_fees_sample_bn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2012 | 8.626 | 353.56 | 24.40 | 2.834 | 4.473 | 0.116 | -0.243 | 0.476 | 0.634 | -4.820 | 326.26 | 0.925 |
| 2013 | 9.012 | 339.39 | 26.55 | 6.906 | 8.446 | 0.260 | -0.363 | 0.884 | 0.818 | -2.326 | 311.18 | 2.149 |
| 2014 | 9.478 | 358.20 | 26.46 | 8.039 | 10.76 | 0.304 | -0.493 | 1.101 | 0.747 | -1.712 | 314.84 | 2.531 |
| 2015 | 10.21 | 396.88 | 25.72 | 10.03 | 10.92 | 0.390 | -0.443 | 1.222 | 0.918 | -1.437 | 310.79 | 3.116 |
| 2016 | 11.01 | 404.42 | 27.23 | 11.61 | 11.65 | 0.426 | -0.412 | 1.265 | 0.997 | -1.341 | 313.72 | 3.643 |
| 2017 | 11.73 | 406.95 | 28.81 | 12.56 | 11.72 | 0.436 | -0.361 | 1.233 | 1.072 | -1.387 | 316.34 | 3.973 |
| 2018 | 12.67 | 416.06 | 30.45 | 10.00 | 11.00 | 0.328 | -0.380 | 1.037 | 0.909 | -1.858 | 320.14 | 3.202 |
| 2019 | 13.64 | 459.12 | 29.72 | 10.45 | 12.94 | 0.352 | -0.502 | 1.205 | 0.808 | -1.489 | 264.63 | 2.766 |
| 2012-13 | 17.64 |  | 25.47 | 4.870 | 6.240 | 0.191 | -0.289 | 0.671 | 0.780 | -3.302 |  |  |
| 2014-16 | 30.70 |  | 26.47 | 9.801 | 11.04 | 0.370 | -0.447 | 1.188 | 0.887 | -1.509 |  |  |
| 2017-19 | 38.04 |  | 29.66 | 11.01 | 11.78 | 0.371 | -0.407 | 1.150 | 0.935 | -1.583 |  |  |

### `largest_covered_banks.csv`

| bank | rssd_hc | assets_2010_bn | accounts_2010_m | accounts_2013_m | service_charges_2010_bn | service_charges_2013_bn | fee_2010 | fee_2013 | fee_2019 | change_2010_13 | change_vs_exempt_2010_13 | change_vs_exempt_2010_19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Wells Fargo | 1120754 | 1,155.25 | 108.63 | 78.78 | 4.924 | 5.081 | 45.33 | 64.50 | 71.11 | 19.17 | 26.37 | 39.36 |
| Bank of America | 1073757 | 1,736.82 | 62.79 | 62.75 | 6.542 | 5.248 | 104.19 | 83.64 |  | -20.55 | -13.35 |  |
| JPMorgan Chase | 1039502 | 1,785.48 | 45.56 | 45.79 | 4.650 | 4.469 | 102.06 | 97.59 | 87.80 | -4.467 | 2.733 | -0.684 |
| PNC | 1069778 | 272.42 | 13.00 | 16.59 | 1.140 | 1.032 | 87.65 | 62.20 | 73.08 | -25.44 | -18.24 | -0.991 |
| U.S. Bancorp | 1119794 | 308.47 | 12.74 | 15.89 | 1.265 | 1.208 | 99.32 | 76.04 | 44.53 | -23.29 | -16.09 | -41.21 |
| BB&T | 1074156 | 153.40 | 8.502 | 7.730 | 0.619 | 0.584 | 72.86 | 75.62 | 55.72 | 2.756 | 9.957 | -3.562 |
| Citizens (owned by RBS) | 3833526 | 140.14 | 7.665 | 5.890 | 0.612 | 0.493 | 79.87 | 83.66 |  | 3.791 | 10.99 |  |
| Regions | 3242838 | 128.37 | 7.284 | 6.095 | 0.807 | 0.734 | 110.75 | 120.47 | 114.52 | 9.729 | 16.93 | 17.35 |
| TD Bank (Toronto-Dominion) | 1238565 | 179.90 | 6.662 | 6.723 | 0.700 | 0.930 | 105.06 | 138.28 |  | 33.22 | 40.42 |  |
| Fifth Third | 1070345 | 108.97 | 5.698 | 5.599 | 0.558 | 0.537 | 97.87 | 95.98 | 94.78 | -1.893 | 5.307 | 10.49 |
| Capital One | 2277860 | 199.10 | 5.136 | 13.05 | 0.366 | 0.345 | 71.18 | 26.47 | 18.24 | -44.71 | -37.51 | -39.37 |
| BBVA Compass | 1391237 | 68.13 | 3.340 | 2.248 | 0.289 | 0.221 | 86.66 | 98.47 | 80.39 | 11.81 | 19.01 | 7.298 |
