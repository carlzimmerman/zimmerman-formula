# AN1 v3: NO VERDICT, numbers only. K11 missed. 61 of 68 rows fold first, 5 never collapse, 2 reach z = 0 oscillating; none settles

Rerun under `AMENDMENT_A3.md` (021852d304), post-result, not blind. Replaces the first publication's fold table. Reduced system only: spherical, Q0 infinite, quadratic K, K_B <= 0.078, one peak, baryons stopped by hand. It doesn't say the class fails in 3D, and it doesn't say the class works anywhere.

## Why no verdict
K11 (no single-shell runaway, line 0.02, set in A3) reads 0.52 to 0.91 on the P1 rows and 0.037 on the top-hat at 1e15, N 300. Its P1 reads fall with N. A peaked profile's inner shells lead on their own, so the line may be wrong for P1, but that isn't tested, and the line stands as frozen. Every other check passes: K0-K6, K7, K8, K10, K12.
- K10: dust sphere z 1.3617, code within 4.6e-4 in t, both masses, N 300 and 1200. Linear-interpolation MUTATE fails it (z 2.93).
- K12: fails without step rejection (6822 km/s out for 100 in). Passes with it.
- K9: sign flip fails K3 (`an1_v3_k9.out`). Run alone, because the full MUTATE job stalled in K12 and was stopped.

## Rows, N 1500, strict line
| Label | Count | Which |
|---|---|---|
| FOLD FIRST | 61 | all others |
| NO COLLAPSE | 5 | K_B 0.078 at mu <= 1 (1e12), mu <= 0.1 (1e15) |
| OSCILLATING, defined to z = 0 | 2 | 1e15, mu 0.0156, both footings; flagged QUADRATIC K LAPSES |
| SETTLED | 0 | |
| UNRESOLVED | 0 | |

Fold z, P1, A1, K_B 0, canonical:
| mu /Mpc | 1e12 | 1e15 |
|---|---|---|
| 1.24e8 | 1.361 | 1.361 |
| 2.04e4 | 1.361 | 1.360 |
| 56.6 | 1.158 | 1.342, r 19 kpc |
| 10 | 0.436 | 1.213, r 77 kpc |
| 1 | 0.022 | 0.398 |
| 0.1 | 0.009 | 0.004 |
| 0.0156 | 0.009 | none, oscillating |

**Correction to the 14-row side test:** 1e15 at mu 0.1 does fold, at z 0.004 to 0.007, inside 0.3 kpc. Those times and radii are grid-limited; the status isn't. The verification set (N 3000, half step, moved boundary, 1/4 tolerance) changes no label on any row, so no row is "not settled numerically". Fold z moves up to 50 % between settings at z < 0.01, and r_fold isn't converged.

## Reads at z = 0, the only rows defined there
1e15, mu 0.0156, P1, A1; both footings carry the quadratic-K flag, so they can't carry a positive claim alone. Canonical:
| | 0.3 R500 | 0.7 R500 | R500 |
|---|---|---|---|
| M_d / M_b | 0.124 | 0.262 | 0.361 |
| M_d / M_ph | 0.017 | 0.026 | 0.032 |
| (M_d - M_ph) / M_b | -7.39 | -9.82 | -11.02 |
| X-COP window, per gas | 4.3-6.7 | 2.1-3.9 | 0.7-2.3 |

Far outside the window, with the wrong sign. The field has gathered about 3 % of the law's phantom mass inside R500, so a defined solution at z = 0 here isn't a well that delivers the law. The window is per gas and the read per baryon; that doesn't change the sign. K_B's NO COLLAPSE rows reach z = 0 with a central shell that never turned around (C_min about 0.58): nothing formed.

State at the fold, not a comparison (frozen section 6): 1e12 at mu 0.1, z 0.009, M_d / M_b 0.026 at 2.2 R_d and 0.101 at R_last, with M_d - M_ph -11.8 and -21.0 M_b.

## Held start, placed on the static branch
| Row | 1 % kick | 10 % kick |
|---|---|---|
| 1e12, mu 0.1 | HOLDS 14 Gyr (N 2400, R_out x 2 too) | INNER FOLD at r about 20 kpc: 2.9 Gyr, 6.0 Gyr with R_out x 2 |
| 1e15, mu 0.1 | HOLDS 14 Gyr (same) | OUTER WALL CELL about 3.2 Gyr |
| 1e12, mu 1 | OUTER WALL CELL 6-8.5 Gyr | same, 2.4-2.6 Gyr |
| 1e15, mu 1 | OUTER WALL CELL 0.13-0.16 Gyr | 0.07 Gyr; R_out x 2 has no static branch, NOT RUN |

So at mu 0.1 the static branch is stable against small kicks, but collapse from a start doesn't reach it. That gap is the reduced system's result. The mu 1 events sit on the outer boundary: a wall artefact, or at least not a read of the interior.

## For AN2
The sphere reference is now z 1.361, K10-checked, on floors. AN2's S0 sphere figure stands, and its AN1 reference column at low mu is replaced by this table. AN2 itself stays NO VERDICT and its rows remain unrun.

kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired: nothing here reinstates it. No LCDM input. Standing obstacles untouched: H1 ghost, planets screen, K_B runaway, static cluster shape, X14 completion. Not theory closed. Nothing here says the data favour the framework.
