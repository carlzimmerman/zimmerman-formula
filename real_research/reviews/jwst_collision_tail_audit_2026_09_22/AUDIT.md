# Independent audit, 22 September 2026

Exact plan: v8 tau1/4, main1m and positive2m, disjoint prescribed seeds.
Six million actual trajectories over unchanged pinned transport. All six
mode/case expectations pass: main/positive certificates true, same-path T-for-D
negatives false. Physical checks, analytic mean and atom, independent quadrature
F1 calibration retained. Separate marginal95%Clopper-Pearson intervals inresult.
Largest absolute positive/main F1 z-score <.53; mean z-score <1.48.
Shared physical solver, independent statistics and analytic calibration.

| Mode | tau | epsilon | one | two | three or more | multi/one |
|---|---:|---:|---:|---:|---:|---:|
| main | 1.0 | 0.01 | 14572 | 296 | 3 | 0.020519 |
| main | 1.0 | 0.003 | 5343 | 51 | 0 | 0.009545 |
| main | 1.0 | 0.001 | 2094 | 8 | 0 | 0.003820 |
| main | 4.0 | 0.01 | 2872 | 232 | 19 | 0.087396 |
| main | 4.0 | 0.003 | 1050 | 36 | 1 | 0.035238 |
| main | 4.0 | 0.001 | 416 | 6 | 0 | 0.014423 |
| positive | 1.0 | 0.01 | 29093 | 595 | 4 | 0.020589 |
| positive | 1.0 | 0.003 | 10791 | 90 | 0 | 0.008340 |
| positive | 1.0 | 0.001 | 4193 | 16 | 0 | 0.003816 |
| positive | 4.0 | 0.01 | 5748 | 412 | 36 | 0.077940 |
| positive | 4.0 | 0.003 | 2152 | 62 | 2 | 0.029740 |
| positive | 4.0 | 0.001 | 848 | 7 | 0 | 0.008255 |

The finite ratios decline across these thresholds. Few multi-scatter events
at the smallest threshold imply substantial uncertainty; no exponent inferred.
ALL_ORDERS.md supplies a separate self-reviewed analytic bound, not a fit.

Rejected Qwen results: ee65d549 assumes independent radial-angle constraints,
wrong lengths, unseeded draws and hardcoded controls. Its exact cubic claim is
refuted by the explicit e^2 lower-bound family. b0a093e0 uses Poisson counts
and D=.01n, self-estimates F1 and removes failed mean calibration. 95c56d44
uses a scalar outward walk with overshoot and D=T. 2221aeae/683ab837/e56482d0
replace transport, truncate scattering, use T-1 and a placeholder F1.
e941d5ab encodes assumed exponents as numerical formulas and includes the
nonzero ballistic atom in a supposedly vanishing CDF. No runner defect shown.

Scientific status: uniform all-order remainder closed in Codex derivation and
self-review, fresh referee not yet obtained; exact novelty unresolved and
literature overlap recorded inSOURCES.md. No physical law/discovery acceptance.
New tasks: audit that proof and derive radial central-opacity tail; separately
derive selected-sample Laplace moments with fixed core cap and explicit flux.
