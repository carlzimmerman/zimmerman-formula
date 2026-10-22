# A44 mutations

Three, each run as `A44_MUTATE=<name> python3 a44_checks.py`, each writing its own
`a44_MUTATE_<name>.out` / `a44_results_MUTATE_<name>.json` and each exiting **1**. The unmutated run exits 0
with 22/22.

## M1 — `system`: the catchment denominator replaced by the system's own cosmic share

`FRET_GAL` is set to 1.00, so `N = 5.364/f_ret` collapses to `N = 5.364` — the record's excluded model. The
`E(53.64)` model becomes `E(5.364)` and the per-bin census block is untouched (it has its own `f_ret`).

| check | unmutated | mutated |
|---|---|---|
| K9 catchment share fits where the system share fails | +1.1 vs +197.0 | **+197.0 vs +197.0** (FAIL) |
| K8b u required by the data | 0.96 | **none — Δχ² never reaches 4** (FAIL) |
| total | 22/22 | **20/22, exit 1** |

What it proves: the entire resolution of the NO-EDGE tension rides on the factor `5.364/f_ret`, not on any
property of the profile. With the system denominator the "catchment" model is literally the excluded model,
Δχ² = +197.0 to the digit.

## M2 — `nostep`: the A29 step switched off

In the u-scan the step factor is forced to `u_eff = 1`, so every point of the S3 curve is the no-step
phantom. The step's effect on the fit disappears while its reported `u` label does not, which is exactly the
failure mode the check exists to catch.

| check | unmutated | mutated |
|---|---|---|
| K8 A29 step at u = 0.4716 is excluded | +94.8 | **+1.1** (FAIL) |
| K8b u required by the data | 0.96 | **none** (FAIL) |
| total | 22/22 | **20/22, exit 1** |

What it proves: the +94.8 penalty is caused by the step's suppressed amplitude inside `r_sp`, not by any
other part of the model; remove the step and the fit returns to the no-edge value.

## M3 — `nobias`: the `(1+K)` shear correction dropped

Both the data vector and the covariance are left uncorrected (no division by `(1+K)`).

| check | unmutated | mutated |
|---|---|---|
| K2 no-edge reference = 83.86 | 83.86 | **83.50** (FAIL) |
| K3 CFG801 reproduction = +197.0 / +753.0 | +197.0 / +753.0 | **+199.6 / +757.9** (FAIL) |
| K3b alt reproduction = +234.0 / +813.0 | +234.0 / +813.0 | **+236.9 / +817.4** (FAIL) |
| total | 22/22 | **19/22, exit 1** |

What it proves: the +197 / +753 anchor is a property of the published, bias-corrected Brouwer+21 product.
Dropping one multiplicative correction moves the anchor by 2.6 / 4.9 in Δχ² — small, but larger than the
0.5 / 1.0 tolerance that makes "we reproduce the record" a meaningful statement, and it is the only
mutation that moves the anchors themselves rather than a downstream model.
