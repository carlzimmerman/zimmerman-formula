# PASS — W2 numerical closure at the graded radius, both footings

Tier 1 lane 1. Criteria `6c710ea048`, committed alone before the new solves.
This is a new radius-specific test, not an amendment of V3X. Only Q2 at
100 Saturn radii is graded; 1/10-radius values remain diagnostics.
Kappa = 1/2 FITTED; not theory closed. L_star=24 pc FITTED.

| quantity | canonical | alt | frozen line |
|---|---:|---:|---:|
| finest Q2, s^-2 | 1.62001880e-34 | 1.37884667e-34 | abs <=9e-27 |
| Richardson Q2, s^-2 | 1.60864790e-34 | 1.36859365e-34 | — |
| Richardson/finest minus1 | -0.00701899 | -0.00743593 | abs <0.02 |
| observed order50/60/70 | 1.93443 | 1.65100 | 1.5..2.5 |
| extrapolated N/F | 0.99993591 | 0.99972053 | within0.05 of1 |
| K1 known answer, max relative error | 1.88217e-7 | 7.79776e-8 | <=1e-6 |
| K2 independent solver agreement | 2.63750e-7 | 2.22762e-7 | <=1e-6 |
| K3 shift sensitivity | 3.70608e-7 | 3.92189e-7 | <=1e-6 |

All twelve main checks passed separately on both footings. The four
production grids are40/64,50/80,60/96,70/112, with30/48 for known answers
and30/48,40/64 for independent COLAMD solves. Maximum main residual is
2.109e-14. Sixteen solves took632 seconds in total; peak child RSS596 MB,
below the frozen1 GB line. All inputs remained hash-identical.

## Control: the physical/reference checks bite, convergence remains UNDECIDED

The separate screening-off mutation runs all four production grids on each
footing, retaining the screened24pc reference. It fails the actual physical
band and reference checks on both footings, not an injected failure flag.

| control | canonical | alt |
|---|---:|---:|
| finest Q2, s^-2 | 3.48534165e-26 | 3.90991239e-26 |
| all-grid physical-band ratios | 3.87260..3.87895 | 4.34435..4.34982 |
| Richardson N/F | 2.16588e8 | 2.85400e8 |
| Richardson relative change | -0.00028063 | -0.00073120 |

The mutant's last differences do not shrink monotonically; the last-three
observed order is undefined. Consequently its own strict label is
**UNDECIDED**, and its failed checks are shrinking, observed_order, routeF,
physical_band. The modest range across these grids is not a substitute for
the frozen convergence condition. No new converged unscreened exclusion is
claimed. The control does demonstrate that the main calculation's physical
and independent-reference gates reject the screening-off outputs.
All mutant residuals are below1.567e-12; peak238 MB; eight solves573 seconds.

## Reproduce and resume

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ31_w2_graded_radius/run.py --resume
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ31_w2_graded_radius/run.py --mutate --resume
```

Main exits0; control exits1. Both were checked after completion using their
source-hashed checkpoints. For fresh solves use a clean checkout without
generated main/mutate directories and omit --resume; preserve live results.
The first invocation used --max-tasks1, wrote one durable rung and exited75;
the main invocation resumed that rung and completed. SIGTERM also requests
a safe yield; an interrupted child may need its current rung repeated.
`first_checkpoint.out`, `main.out`, `mutate.out` and resume logs preserve the
execution history. The child memory watchdog requires access to process RSS.
Raw per-rung JSON, final margins and dependency/software hashes are included.

This closes the new graded-radius numerical test. It does not promote the
ungraded near-origin diagnostics, regrade the entire Cassini field grid, or
close relativistic tensor/constraint health. Next, if unscreened convergence
is pursued, freeze an extraction/precision study of its irregular last-grid
differences before adding new grids; the historical V3X verdict stays intact.
