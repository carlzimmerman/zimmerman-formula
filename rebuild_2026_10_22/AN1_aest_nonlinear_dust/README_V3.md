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

## Reads at z = 0: the oscillating rows (the K_B rows are in the addition below)
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

So at mu 0.1 the static branch holds 14 Gyr against a small radial kick (radial modes only; it doesn't touch H1's ghost), but collapse from a start doesn't reach it. That gap is the reduced system's result. The mu 1 events sit on the outer boundary: a wall artefact, or at least not a read of the interior.

## For AN2
The sphere reference is now z 1.361, K10-checked, on floors. AN2's S0 sphere figure stands, and its AN1 reference column at low mu is replaced by this table. AN2 itself stays NO VERDICT and its rows remain unrun.

## Addition: what the text above left out
**All seven rows defined to z = 0.** Every one of them has barely any baryons on the measured profile: fraction stopped on it 0.001 at most, against M_b(<R500) 8.7e12 at best and the measured 1.19e14. So none is a cluster or a galaxy at z = 0, and no comparison below is a pass.

| Row (canonical) | Label | M_d / M_b / M_ph at R_test | M_d / M_ph | (M_d - M_ph) / M_b | Flag |
|---|---|---|---|---|---|
| 1e15, mu 0.0156 | OSCILLATING | 3.13e12 / 8.69e12 / 9.89e13 | 0.032 | -11.0 | K lapses |
| 1e12, mu 0.0156, K_B 0.078 | NO COLLAPSE | 3.08e7 / 8.29e7 / 8.45e9 | 0.0036 | -102 | K lapses |
| 1e12, mu 0.1, K_B 0.078 | NO COLLAPSE | 3.08e7 / 8.30e7 / 8.46e9 | 0.0036 | -102 | |
| 1e12, mu 1, K_B 0.078 | NO COLLAPSE | 3.31e7 / 8.74e7 / 8.68e9 | 0.0038 | -99 | |
| 1e15, mu 0.0156, K_B 0.078 | NO COLLAPSE | 1.39e12 / 2.44e12 / 5.35e13 | 0.026 | -21.3 | K lapses |
| 1e15, mu 0.1, K_B 0.078 | NO COLLAPSE | 1.48e12 / 2.52e12 / 5.43e13 | 0.027 | -21.0 | |

Alt, 1e15 mu 0.0156: 3.21e12 / 9.01e12 / 1.11e14, 0.029, -12.0. R_test is R_last at 1e12, R500 at 1e15.

- **X22, A8, D4.** The 1e12 rows read M_d - M_ph below X22's tolerated 0.035 and 0.0049 only because it's negative and no disc formed (M_b 8e7, disc 6.7e10). That doesn't meet the need. A8 has no pass line; these rows contract nothing because nothing fell.
- **X-COP and LM1's 8 x and 5 x gas.** No row is inside any window, and all have the wrong sign. M_d / M_b at R500 is 0.36-0.59, while LM1's map needs about 5 x gas. The read is per baryon on the row's own M_b, and that gas isn't in place.
- **No win to set H1 beside.** For the record: this start doesn't charge suppressed growth before z_i (frozen as generous), and H1's ghost stands. The NO COLLAPSE rows come from that generous start.

**Q0_need, P1 A1 canonical, /Mpc, all shells, then outside 1 kpc.** 1e12: 3.3, 0.026 (mu 0.0156); 3.2, 0.026 (0.1); 2.9, 0.028 (1); 3.5, 0.045 (10); 2.4, 0.062 (56.6); 9.6, 0.098 (2.04e4); 300, 0.091 (1.24e8). 1e15: 0.0091, 0.0091; 0.24, 0.039; 0.090, 0.090; 0.031, 0.027; 0.125, 0.079; 17.6, 0.66; 297, 0.60. Against C7's Q0 = 0.1: the all-shell read is over it in all 1e12 rows, set by the innermost cells at the fold. Outside 1 kpc only the 1e15 floors are over. All rows in `an1_v3_rows.jsonl`. The seven z = 0 rows read at most 0.0093, so they are inside.

**K11's miss, a look after it, rescuing nothing** (`diag_v3/k11_diag.py`). Exact dust shells predict 0.93 at 1e12, N 300, where the run reads 0.91. At N 1200 they predict 0.34 and the run reads 0.54. At 1e15 the comparison fails: the shells reach the focus before the read. So differential focus explains some of it. Whether it all does stays open. My hand estimate when I set the line was wrong by about 25x: I took the first shell's offset, not the fifth's. The line isn't changed.

**Departures, all of them.**
- Wall overshoot was found here, not in the brief. It drove the first publication's and the side test's low-mu radii (r 1.27 kpc, N-dependent, first shell at +1361 km/s). Step rejection is a new numeric tolerance, 1e-3, tested at 2.5e-4.
- `fix.py` was incomplete in three ways (A3 section 2). Stop radii now use mid-q mass. Fold reader takes any closing cell.
- K12 was added beyond the brief and developed on a trial first.
- A3's stop-rule change (no lift to r_f) never fired: count 0 on all 68 rows.
- Fold-time and first-shell traces were seen before A3 was committed, on side-test rows, at N up to 2400.
- Budget counted in CPU seconds; no row reached it. Total 232 CPU s for 68 rows, RSS 0.08 GB. Newton warnings 0 of 68, though K12's extreme bounce gives 7165 warnings at N 1200 (its result still passes).
- The frozen-line z is kept per row in the jsonl. The verification set ran on each non-fold row and fold rows under z 0.05.
- `an1_v3.py`'s full `--mutate` job didn't finish; K9 was run alone (`an1_v3_k9.out`).
- K_B rows and P2 are canonical only, as frozen.

**Not run.** Finite Q0, non-quadratic K, 3D, angular momentum, any completion, baryon pressure, grading against SPARC or X-COP data.

kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired: nothing here reinstates it. No LCDM input. Standing obstacles untouched: H1 ghost, planets screen, K_B runaway, static cluster shape, X14 completion. Not theory closed. Nothing here says the data favour the framework.
