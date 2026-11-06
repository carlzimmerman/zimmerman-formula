# QX5 iter a2: class a's lead on Coma UDGs: LEAD ALIVE (still CLUSTER-SET, not a pass)

Criteria 51ef07f3cc, a post-result test declared in ../AMENDMENTS.md. Kappa = 1/2 FITTED; not theory closed.
Script qx5_a2.py (imports d10_solver read-only, reads S1's per-galaxy CSV/JSON). Outputs qx5_a2.*, qx5_a2_MUTATE.*.

| Footing | F = 1 (v3s, S1) | F_med (X-COP median) | F_max (X-COP largest) | F for mean 0 |
|---|---|---|---|---|
| canonical | +2.581 ln (+1.12 dex), z +4.28 | F 4.09: +1.668 (+0.72 dex), z +2.76 | F 5.67: +1.402 (+0.61 dex), z +2.32 | 26.4 |
| alt | +2.481 (+1.08 dex), z +4.11 | F 3.66: +1.600 (+0.70 dex), z +2.65 | F 5.06: +1.333 (+0.58 dex), z +2.21 | 21.7 |

By the frozen line (|z| < 3 at F_med on both footings) the lead is **ALIVE**. Read plainly, though:
- the lead moves the UDGs toward the data by 0.40 dex, but they still sit +0.6 to +0.7 dex high;
- it survives only because S1's systematic error is large (sigma_tot 0.60 ln);
- zeroing the UDG mean would need F = 22-26, which is 5-6 times what X-COP needs.

So one F(|Phi|/c^2) does not serve both X-COP and Coma's members. The tension is 2.2-2.8 sigma, not yet a kill.

Known answer: F = 1 reproduces S1's mean exactly (|d| = 0). MUTATE F = 30 drives the mean to -0.13 / -0.31 ln: BITES.
Scope: S1's static Plummer-in-uniform-field model, 9 admitted UDGs, E-W estimator, sigma_sys taken from S1.
