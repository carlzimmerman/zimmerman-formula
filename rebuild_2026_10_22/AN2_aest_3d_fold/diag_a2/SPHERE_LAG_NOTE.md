# AN2 diagnostic SL: why the 3D sphere folds 16-18 % after AN1. Frozen before any run. POST-RESULT, NOT BLIND

Owner's go, 2026-11-03. A diagnostic, not a grade: AN2 stays NO VERDICT and no label changes. Lines of AN2 section 8 are untouched.

## Known before running
- Rows' e = 0 at 128^3, eta 0.05, canonical: 1e12 mu 56.6 folds at 6.216 Gyr, 1e15 mu 56.6 at 5.443. AN1 v3 t_ref: 5.277, 4.701.
- Homogeneous dust sphere at AN1's d0 = 0.2030 (S0's ODE): 4.645 Gyr. With the box mean of the Gaussian taken out, as the engine's IC does (mean/d0 = 0.0082 at L = 8 q_t): **4.702 Gyr**. Computed today with `an2_checks.ellipsoid`, the same at both masses. So AN1's 1e15 mu 56.6 reference is the dust value to 0.02 %, and the 3D lag is the engine's, not AN1's, at 1e15. At 1e12 AN1 itself sits 12 % after dust.
- KG's G2 (shape A, 1e15 mu 56.6): 6.023, 5.312, 5.028 Gyr at 64, 96, 128.

## Runs (e = 0, eta 0.05, L = 8 q_t, canonical, both masses unless marked)
| Id | Change from the rows | N |
|---|---|---|
| D0 | pure dust: field force = Newton, **no baryon stop** | 64, 128 |
| D1 | dust, baryon stop as in the rows | 128 |
| D2 | hold on, no baryon stop | 128 |
| D3 | as D0, CIC deposit and interpolation instead of TSC | 128 |
| D4 | as the rows | 160 |

Output `diag_a2/sphere_lag.jsonl`. Same engine, same tracker, same t_q. Run with nice 15, one thread, two jobs at most, 67.5 CPU min cap per run.

## Reading rule, fixed now
- D0 against 4.702 Gyr is the engine's error in pure dust at that N. If D0 at 128 is within 3 %, the grid and the kernel aren't the cause.
- A factor is called **a cause** if switching it alone moves t_q at 128 by more than 3 % of t, toward the rows' value: baryon stop (D1 against D0), hold term (D2 against D0), kernel (D3 against D0).
- D4 against the rows' 128 gives the resolution trend for the full engine. Under 3 % from 128 to 160 counts as settled at that N, as a read.
- If the causes found don't add up to the gap within 3 % of t, the rest is stated as unexplained.

## Expectation, before any number
D0 near 4.7, within a few percent. Most of the gap from the baryon stop: pinned baryons stop adding mass at the centre. The hold term adds force, which would make the fold earlier, so it can't be the lag's source at 1e15. Not confident at 1e12, where AN1 is itself 12 % after dust.

kappa = 1/2 FITTED. Footings not pooled; canonical only here. A gravitating field, never a particle. The cold sector stays retired. Not theory closed. Nothing here says the data favour the framework.
