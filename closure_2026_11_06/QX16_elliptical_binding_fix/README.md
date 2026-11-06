# QX16: elliptical late-binding bug, fixed forward: NO LABEL CHANGES

Criteria: FROZEN_CRITERIA.md (7de1a2733f; on origin as a059f24e13), committed alone. One amendment, A1, was made
before any rerun number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## The bug and the fix

`QX5_cluster_terms/qx5.py` `ellipticals()` built `Mtot` and `Mbar` as lambdas inside the row loop. Late binding
gave 6 of the 7 Humphrey+2006 ellipticals NGC6482's mass model. Each galaxy's own `Re` was used, but the masses
were all NGC6482's. The fix binds each row's values through default arguments (commit 5958c0d7b2). Original
outputs are untouched. Every rerun is in `fixed_outputs/<lane path>/*_FIXED.{json,out}`.

- U1 as frozen compared Mtot(1e9 kpc) with Mvir. That test was ill-posed: an NFW mass grows as ln r. It printed
  FAIL (u1_check.out, kept). Amendment A1 replaced it with Mtot(Rvir) = Mvir. Fixed code: PASS, rel <= 2.5e-4, Mbar
  rel <= 4.8e-9, 7 distinct values (u1_check_A1.out). Unfixed code: FAIL (u1_check_A1_UNFIXED.out).
- MUTATE / reproduction: the unfixed qx5.py, run in the scratch mirror, reproduces the record's qx5.json and qx5.out
  byte for byte. The mirror runs the record's own scripts unchanged.
- K1: every gate that does not use ellipticals is unchanged to the printed digit: X-COP base, groups base, SPARC,
  KiDS. Where a groups prediction moved (QX12 iter_2), it moved because its threshold is set by the galaxy maximum,
  and that maximum includes the ellipticals.

## What changed

The plain-law residual of the 7 ellipticals (mean log M_obs/M_law at 2/4/8 Re) is now **+0.210 canonical and
+0.189 alt**. The record had +0.083 / +0.065. With their own mass models, the law under-predicts these X-ray
ellipticals by about 0.2 dex. Most lanes grade the ellipticals as a SHIFT from this baseline, so their labels hold.

| Lane | Gate / quantity | Old | Fixed | Old label | Fixed label |
|---|---|---|---|---|---|
| QX5 (all classes) | ellipticals base E (canon / alt) | +0.083 / +0.065 | +0.210 / +0.189 | - | - |
| QX5 class a | P prediction X-COP (canon) | +0.222/0.243, F 2.16 | -0.152/0.186, F 5.82 | DEAD | DEAD |
| QX5 class a | K (with X-COP) groups (canon) | [-0.043, +0.110] | [-0.078, +0.073] | DEAD | DEAD |
| QX5 class b | P prediction X-COP (canon / alt) | +0.205 / +0.213 | -0.244 / -0.238; ellipticals recheck True -> False | DEAD | DEAD |
| QX5 class d | K ellipticals recheck | True | False | DEAD | DEAD |
| QX5 class e | - | - | unchanged | DEAD-BY-GROUPS / DEAD | same |
| QX5 MUTATE, gcut 0.01 | controls / labels | - | label lines identical | DEAD | DEAD |
| QX7 iter_4 | baselines E; G7 is a shift | 0.083 / 0.065 | 0.210 / 0.189; .out identical | FAIL (clusters), window 270 | same |
| QX10 iter_2 | G7 shift (C1-C4) | -0.0001 to -0.0039 | -0.0002 to -0.0043 | KILLED (G6) | KILLED (G6) |
| QX10 iter_2 MUTATE | M2 G7 | -4.2e-07 | -4.6e-07 | BITES | BITES |
| QX12 iter_1 | max galaxy depth; gap to hot | 1.87e5 (km/s)^2; ratio 32.5 / 33.4 | 3.54e5; ratio 17.1 / 17.7 | ALIVE (statics) | ALIVE (statics) |
| QX12 iter_2 | b_t; groups (traces baryons) canon | 7.84e-7; [-0.279, -0.097] | 1.774e-6; [-0.233, -0.052] | FAIL | FAIL |
| QX12 iter_2 | X-COP prediction | -0.075/0.110, -0.097/0.127 | unchanged | FAIL | FAIL |
| QX12 iter_3 | c_min canonical (alt) | 246.5 (246.5) | 230.0 (246.5); X-COP/groups predictions unchanged | FAIL | FAIL |
| QX13 | c_min; convergence fraction | 132.32; 0.88 / 0.84 | 132.32; 0.91 / 0.88 | FAIL | FAIL |

## Reading

- No label in QX5, QX7 iter_4, QX10, QX12 or QX13 changes. The cluster and CMB rows of CLOSURE_FINAL.md stand.
- QX12 iter_1's conservative depth gap between galaxies and hot systems halves, from 32-33x to 17-18x. It still
  separates them, and its label holds.
- QX12 iter_2's near miss stays a FAIL. The groups over-boost is smaller (0.05-0.23 dex, previously 0.10-0.28)
  because the galaxy-set threshold is higher.
- **New fact, outside the cluster/CMB rows.** On their published NFW+stars masses (Kroupa M*/L) the plain a0 law
  under-predicts the 7 Humphrey+2006 X-ray ellipticals by about 0.2 dex at 2-8 Re on both footings. Other lanes
  that graded ellipticals with their own code are not affected by this bug. QX7 iter_2/3 read the TSV with no
  lambda; QX6 and QX5 iter_a2 do not use the ellipticals. Whether 0.2 dex is a law failure or a stellar-M/L choice
  (Kroupa vs the X-ray-fitted ups_fit) is not graded here.

## Not covered

Lanes outside the affected list are not re-run. qx10_i2_hydro and ka4b are not re-run because they do not use
`EL`.
