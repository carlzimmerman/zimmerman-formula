# BK1 AMENDMENT A1: target budget fixed, before any search

From `bk1_budget.py`, `bk1_budget.json`, by FROZEN_CRITERIA's procedure, and answering the owner's 11-02 line on tolerances: total error stated per target, acceptance at 2 sigma, Z for every hit, look-elsewhere, scrambled control at the same tolerance, no widening after a result, both readings if a budget changes.

| Target | canonical value, stat, sys, **sigma** | alt | sigma/value | Flag | Second reading sigma |
|---|---|---|---|---|---|
| K | 13.287, 2.10, HSE 2.45 (k at HSE - 0.12 dex 8.38), **3.23** | 14.251, 2.28, 2.74 (8.78), **3.56** | 24 %, 25 % | BLUNT | with HSC 1.7: 5.66, 6.13 |
| D8 | 7.56, 1.03, 1.40, **1.74** | 7.18, **1.74** | 23 %, 24 % | BLUNT, band value | 3.17, 3.06 |
| D5 | 5.37, 0.79, 1.05, **1.31** | 4.93, **1.31** | 24 %, 27 % | BLUNT, band value | 2.29, 2.17 |
| XR | 5.350, stat NOT MEASURED, sys 2.71 %, **0.145** | same | 2.7 % | understated: no statistical term | 0.154 (1 %, PROVISIONAL) |
| RHO | 2.249e-27, as XR, **6.09e-29** | same | 2.7 % | understated, as XR | 6.49e-29 |
| FQ | 0.946, 0.15, 0.037, **0.154** | one sim set | 16 % | BLUNT; contains 1 | none |
| T | lg 12.29, **0.05 dex** combined | canonical only | 12 % | window, not a measured sigma | none |

No target here is error-free. The two thinnest budgets are XR, RHO (missing stat) and T (a window read as 2 sigma).

Row count: 6 x 2 + T = 13 rows, or 25 counting alphabets A and B. FROZEN says x15. I keep 15 as frozen and report what 25 would change (log2(25/15) = 0.74 bits less).
