# AN2 diagnostic P160: does the grid correction predict the 160^3 shape rows? Predictions frozen before any run.

Follows SL (f3f55780f6) and SG (`SHAPE_GRID_RESULT.md`). SG's grid correction was fixed after the rows ran. This tests it forward: predict the full-engine shape rows at 160^3 from 64 and 128 alone, then run. A diagnostic, not a grade: AN2 stays NO VERDICT and no label changes.

## Prediction rule
t(160) = t_row(128) − (t_G0(128) − t_exact) · h · (1 − 0.8^p), where p is the shape's pure-dust order from 64 to 128 (SG), h = t_row(128) / t_G0(128) is the hold factor, and t_exact is the dust ellipsoid with the box mean taken out. The grid error is taken to scale as N^-p and multiply with hold.

Retro check on spheres, already run (SL D4), with the same rule: 1e15 predicted 5.253, ran 5.266 (+0.25 %); 1e12 predicted 5.999, ran 6.042 (+0.7 %).

## Frozen predictions (Gyr; rows as in AN2 S1: hold on, baryon stop, eta 0.05, L = 8 q_t, canonical, TSC, N 160)
| Row | t_row(128) | p | h | **Predicted t(160)** |
|---|---|---|---|---|
| 1e12 A | 5.401 | 1.482 | 1.1661 | **5.232** |
| 1e12 B | 5.039 | 1.505 | 1.1967 | **4.868** |
| 1e15 A | 5.028 | 1.464 | 1.0025 | **4.870** |
| 1e15 B | 4.765 | 1.477 | 1.0027 | **4.616** |

## Reading rule, fixed now
- **PREDICTED** if every row lands within 1 % of its prediction. Then SG's grid-corrected shifts and the "every shape folds before AN1" read stand as the correction's output, still a read and not an AN2 label.
- **MISSED** if any row is off by more than 1 %. Then the correction is called unreliable for that row and SG's corrected numbers for it are withdrawn.
- If a row doesn't fold, or its fold shape changes class (filament, sheet, point), it's reported as is and not counted as a miss of the timing rule.

## Run
`pred160.py`, output `pred160.jsonl`. nice 15, one thread, two at a time, 67.5 CPU min cap. Expected about 2.7 GB and 50 CPU min per run, over the 1 GB target, as SL's D4 was. Started only when the 1-minute load is under 16 and free plus inactive memory is over 8 GB.

kappa = 1/2 FITTED. Canonical only, footings not pooled. A gravitating field, never a particle. The cold sector stays retired. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
