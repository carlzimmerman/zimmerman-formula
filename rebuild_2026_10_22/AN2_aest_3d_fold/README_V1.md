# AN2_aest_3d_fold: NO VERDICT. Two frozen engine checks failed (KZ, KE2); S0 ran, the 16 S1 rows were not run or read

**Plain statement.** This lane has no answer yet on whether a non-spherical peak reaches the well before its first fold. S0 is a dust-limit read: an ellipsoid's first axis collapses earlier than the sphere at both masses. The 3D engine can't yet time a fold to its frozen lines, so by the frozen order the rows stayed unread, and I stopped to report rather than run them. Numbers only; no label.

Criteria `FROZEN_CRITERIA.md` (cfc462ec68), alone first. `AMENDMENT_A1.md` post-miss, before any row. Not blind. kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired: nothing here reinstates it. No LCDM input in a grade. Not theory closed. Nothing here says the data favour the framework.

## S0: homogeneous ellipsoid, dust limit, AN1's d0 = 0.2030 (reads, no grade)
| Mass | nu, xbar | Shape | e, p | Axis ratio | z first axis | t Gyr |
|---|---|---|---|---|---|---|
| both | | sphere | 0, 0 | 1 | 1.361 | 4.645 |
| 1e12 | 1.74, 2.42 | A | 0.164, 0.006 | 1.71 | 1.591 | 4.066 |
| 1e12 | | B | 0.259, 0.038 | 2.64 | 1.784 | 3.664 |
| 1e15 | 7.28, 5.43 | A | 0.081, 0.000 | 1.28 | 1.455 | 4.395 |
| 1e15 | | B | 0.138, 0.002 | 1.55 | 1.544 | 4.174 |

No external tide, no baryons, no hold term. It doesn't speak to low mu.

## Checks
| Id | Result | Line | |
|---|---|---|---|
| KN BBKS memory | norm within 2.4e-6 of 1 at x 1, 2, 3, 5 | 1e-3 | pass |
| KD det, tracker | first run **6.2e-3, missed**; after A1 1.0e-4. Held core det 1.2e-9 doesn't fire; fold fires on the right step and plane; transient rejected; shapes right | 2e-3 | pass only after A1 |
| KC L1's check | AQUAL 3.4e-4, 3.5e-4; baryon 3.7e-4, 4.1e-4; field net 5.9e-3, 7.9e-3 (can, alt); reproduces L1's | 0.01 | pass |
| **KZ plane wave, 64^3** | **t +2.60 %**, dust and floor hold alike | 5e-3 | **FAIL** |
| KE1 ellipsoid, two integrations | 1.3e-7 | 1e-6 | pass |
| **KE2 engine vs ODE, 96^3** | **t +9.8 %**, sheet | 3 % | **FAIL** |
| KR SIGTERM resume | 0 | 1e-10 | pass |
| KM MUTATE | KC and KD fail, as they must | | pass |
| KT, KB, KE, KG | **not run** | | |

**Diagnostics, outside the frozen sizes, none rescues a check.**
- KZ at eta 0.0125, 64^3: +2.61 %. So it isn't the timestep.
- KZ at 128^3, eta 0.05: **-3.31 %.** The sign flips with N, so it isn't simple softening, which would only delay. Likely, not shown: the spectral gradient copied from L1 rings on a density spike near a caustic, and softening adds to that. A particle crosses its last cell in about dx/(v t) of a Hubble time, roughly 10 % here, so a force error in that cell has this size.
- KE2 at 128^3: +2.47 %, inside the line at a size the line doesn't name.

**Why it matters.** S0's shifts in t run from 5 % to 21 %, and the engine's fold-time error here is 2.5-10 %, of either sign. So 1e15's small shift couldn't be read at this grid. The lines were my own estimates, and 5e-3 was too tight for a cell-sized fold in a PM; I don't loosen them after a miss.

## Open question for the reference column: not resolved
S0's dust sphere folds at z 1.36. AN1's strict floors fold at z 2.93 (1e12), which I reproduced at N 300 (2.932), and 2.82 (1e15), and AN1's 1e15 at mu 56.6 at z 1.63. AN1 calls the floors dust-like. My one probe, removing baryons from AN1's run, moved the fold to z 0.06, but that probe also removes their gravity, so it separates nothing. **Something beyond dust sets those AN1 times, probably the baryon stop rule; not diagnosed.** It bears on a NO LATER comparison at 1e15 mu 56.6, because shapes A and B could read LATER in dust alone: t 4.39, 4.17 against 1.05 x 3.978 = 4.18.

## Departures and first-run failures, all of them
- KD: first-run miss, test changed (A1). That record was deleted from `an2_checks.jsonl` when I reran; its value survives in the `frozen_form_err_centroid` field.
- Held-core and integrator faults (A1). First S0 and KE1 returned no collapse at rtol 1e-10.
- A sed error tried to tidy S0's ODE wording in section 11 of the criteria and did nothing; the frozen text stands as committed. The form used is a_i''/a_i = OL H0^2 - 4 pi G rho_bar (1/3 + delta b_i/2).
- KD and KR were rerun after a memory rewrite of the tracker; KZ, KE2 and KC at their frozen sizes predate it. KZ's diagnostic shows no change.
- Frozen section 8 lets rows be computed for numbers after a failure. The brief says checks must pass before rows are read. I took the stricter reading and computed none.
- Memory: 1.94 GB RSS at KE2 96^3 before the rewrite, 1.42 GB at 128^3 after, dust mode. **Over the 1 GB target as RSS;** footprint wasn't measured, and hold rows would add Anderson history.

## Limits, for any later run
K_B = 0 only. Reduced system: Q0 -> infinity, quadratic K, one deterministic peak, baryons stopped by hand. No discs resolved. Cells 114 kpc (1e12), 1.14 Mpc (1e15) comoving at 128^3; R_last about one cell at z 2. Shape comes from the record's dust-limit spectrum, not derived here; BBKS's formula is from memory, checked only by KN.

## Not run
All 16 S1 rows; e = 0 rows; KT, KB, KE, KG; S2, S3; any completion; anything past a fold.

## Files
`an2.py`, `an2_checks.py`, `an2_checks.jsonl`, `an2_checks_MUTATE.jsonl`, `an2_shapes.json`.
