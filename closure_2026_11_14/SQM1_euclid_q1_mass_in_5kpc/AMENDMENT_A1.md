# SQM1 AMENDMENT A1 (POST HOC; committed alone, before any graded number is computed)

2026-11-14. Criteria d91049bd52. Script 5eced7de93. As-frozen run d2b3746304.

## What happened

The as-frozen run stopped at known answer K3 (exit 3, NOT EVALUABLE; no graded number was computed or printed).
K3 asked that the projected law machinery at a0 -> 0 return `Y L x M2D_frac(R5)` to 1e-5. It returned 9.9e-4.

## Cause (diagnostic `sqm1_k3_diagnostic.py`, output committed with the as-frozen run)

The gap does not move with the quadrature (400 vs 3000 nodes) or the cut-off (rmax 1e6 vs 1e9 kpc), to 1e-10. It is
the Prugniel-Simien deprojection that EUC1's code uses (`M3D_frac`): an approximation to the exact Abel deprojection of
a Sersic profile, good to about 1e-3 (here -2.4e-4 at R_e, -9.9e-4 at 1.59 R_e, -1.2e-3 at 2 R_e for n = 4; under
6.2e-4 for n = 6). The criteria's 1e-5 tolerance was a design error: it tested the deprojection formula's accuracy,
not the projection code. 1e-3 relative is 0.0004 dex, against a 0.042 dex amplitude band (2 sigma).

## Change (the only one)

K3 tolerance 1e-5 -> 2e-3 (relative). Nothing else changes: no input, form, bracket, sigma or word rule. Outputs of the
amended run are written as `sqm1_A1*.{out,json}`; the mutation and null twins compare against `sqm1_A1_results.json`.
The as-frozen label stays on the record: NOT EVALUABLE (a known answer failed by a tolerance design error).
