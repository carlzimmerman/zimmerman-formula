# AN2 diagnostic SG, result: shapes carry 2-3 points less grid error than the sphere, so AN2's own-sphere shifts are restated. Grid-corrected, every shape folds before AN1's sphere. Diagnostic only; AN2 stays NO VERDICT, no label changes.

Note `SHAPE_GRID_NOTE.md` (b8d3f94818), frozen before any run. Data `shape_grid.jsonl`. Pure dust, eta 0.05, L = 8 q_t, canonical, TSC. Not blind.

## Runs (t_q in Gyr)
| Key, shape | Exact dust | 64^3 | 128^3 | e_s at 64 | e_s at 128 | Order | Fold |
|---|---|---|---|---|---|---|---|
| 1e12 A | 4.116 | 5.557 | 4.632 | +35.0 % | **+12.5 %** | 1.48 | filament |
| 1e12 B | 3.709 | 5.133 | 4.211 | +38.4 % | **+13.5 %** | 1.50 | sheet |
| 1e15 A | 4.449 | 6.011 | 5.015 | +35.1 % | **+12.7 %** | 1.46 | filament (point at 128) |
| 1e15 B | 4.225 | 5.692 | 4.752 | +34.7 % | **+12.5 %** | 1.48 | filament |
| sphere (SL D0) | 4.702 | 6.561 | 5.435 | +39.5 % | +15.6 % | 1.34 | point |

## Read by the frozen rule
- **e_s against the sphere's 15.6 %:** 3.1, 2.1, 2.9 and 3.1 points smaller. Two of four are over 3 points, so by the rule AN2's shifts are restated against exact dust.
- **Order:** 1.46-1.50 for the shapes against 1.34 for the sphere, within 0.3: the same.
- **Errors fall toward the exact value** at every shape, so the homogeneous reference holds and the restatement applies.
- **My expectation (e_s about 12-13 %) held.**

## Restated shifts (shape against sphere)
| Key, shape | S0 dust | AN2 rows, own sphere | Pure dust, own sphere (G0 / D0) | Rows, grid-corrected |
|---|---|---|---|---|
| 1e12 A | −12.5 % | −13.1 % | −14.8 % | −10.7 % |
| 1e12 B | −21.1 % | −18.9 % | −22.5 % | −17.4 % |
| 1e15 A | −5.4 % | −7.6 % | −7.7 % | **−5.3 %** |
| 1e15 B | −10.1 % | −12.5 % | −12.6 % | **−10.0 %** |

Grid-corrected = rows' t_q / (1 + e_s at 128), shape and sphere each with its own e_s. At 1e15, where hold barely acts, the corrected shifts land on S0's dust ellipsoid to 0.1 points. The own-sphere comparison overstated the shapes by 1.4-2.5 points in pure dust.

## Hold term on shapes (rows / G0 − 1 at 128, read only)
1e12: A +16.6 %, B +19.7 %, against the sphere's +14.4 %. 1e15: +0.3 %, +0.3 %, against +0.15 %. At 1e12 hold delays the more elongated peak more, so the 1e12 corrected shifts are 2-4 points smaller than dust's.

## Against AN1's 1D reference, grid-corrected (a read, not a label)
1e12 A 4.80 vs 5.277 (−9.0 %), B 4.44 (−15.9 %); 1e15 A 4.46 vs 4.701 (−5.1 %), B 4.24 (−9.9 %). Every shape folds before AN1's sphere. AN2's "1e15 A LATER than AN1 by 7.0 %" is the grid's error, not the field's. This uses a correction fixed after the rows ran, from 128^3 alone, so it states what the frozen section 9 would read, not what it does read.

## Compute
8 runs, nice 15, one thread, two at a time, started when load fell under 16 (2026-11-04 15:00-15:27 UTC). 64^3 84-87 CPU s, 1.2-1.3 GB; 128^3 645-728 CPU s, 1.39 GB, over the 1 GB target.

kappa = 1/2 FITTED. Canonical only, footings not pooled. A gravitating field, never a particle. The cold sector stays retired. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
