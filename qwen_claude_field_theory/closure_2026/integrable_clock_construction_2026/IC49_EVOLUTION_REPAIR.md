# IC49: canonical deviations remove the large finite-time interface error

Status: OPEN. Same action and finite-patch boundary prescription as IC46.

Write each canonical grid field as F(x,t)=F_initial(x)+delta F(x,t), with x
the fixed offset from the moving interface. The background is time independent
in these coordinates, so delta F obeys the inherited moving-grid RHS exactly.
Its spatial derivatives are the analytic initial-polynomial derivatives plus
collocation derivatives of delta F. No canonical or interface projection is
performed. Algebraic constitutive evaluations still reconstruct float64 F;
this is not an arbitrary-precision evolution scheme.

Three runs at width 3e-5 reach dimensionless time 2e-7:

| nodes | dt | maximum reaction magnitude | maximum momentum residual | maximum conditional gradient-jump residual |
|---|---|---|---|---|
| 7 | 1e-8 | 1.72e-10 | 1.82e-14 | 5.30e-9 |
| 7 | 5e-9 | 3.04e-10 | 1.84e-14 | 9.37e-9 |
| 9 | 5e-9 | 9.91e-10 | 1.84e-14 | 3.06e-8 |

Maximum lapse residual across runs is 6.30e-10; maximum inactive-clock
residual is 1.32e-9. IC47's reaction reached 9.43e-5 on the nine-node run.
IC49 removes this large discrepancy through the entire tested time interval.
These are dimensionless diagnostics with the inherited normalization.

The remaining residuals do not decrease monotonically with refinement, so no
convergence order or continuum solution is certified. Nor does the very short
interval demonstrate long-time stability, a physical branch of definite
reaction sign, a global boundary problem, full Dirac closure or a final theory.

Next calculation: a precision-controlled longer evolution, with a complete
branch-inequality check and error budget for the remaining metric/constitutive
operations. The initial Taylor endpoint prescription must eventually be
replaced or justified by a well-posed global boundary problem.

## Commands and outcomes

From repository root:

```
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic49_deviation_evolution.py > /tmp/ic49_results.json
```

Exit 0, all three runs complete. Output preserved as `ic49_results.json`.

From this directory:

```
python3 -m unittest test_ic49_deviation_evolution
```

Exit 0, one test passes. It checks first and second derivatives with a nonzero
cubic deviation and checks the fallback for an unrelated array. It would fail
if the derivative implementation froze the initial solution. Original IC46
tests and failure evidence remain unchanged; they do not test this subclass.

The inherited symbolic action and initial-data dependencies remain necessary
for reproduction. Mathbox computation-audit scope: numerical repair supported
by bounded calculations, without claiming theory closure or empirical proof.
