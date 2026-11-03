# WF1_wave_pressure_field: SURVIVES TO gate 1 at m 1e-25 eV and up; gates 2 and 3 fail at the selected m, 1e-25: cluster keys 1 of 15, X-COP rms 0.138, groups Z -8.31

Criteria `FROZEN_CRITERIA.md` (927760960f), committed alone first. `AMENDMENT_A1.md`, nine parts: parts 1, 2, 4-8 before any graded number, part 3 after control lines only, **part 9 after gate 1 and a first selection table**. A classical scalar field beside the a0 law, mass m only. It adopts nothing and reinstates nothing; any adoption is the owner's call. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. A family result on these inputs, not a no-go theorem.

## Gate 1 (`wf1_g1.out`), RF5's line, S - S_min <= 25
| m eV | z_osc | S - S_min, fit | sigma8 | k_half h/Mpc | read |
|---|---|---|---|---|---|
| 1e-26 | 1.5e4 | 2668 screen | 0.382 | 0.11 | not fit, screen over 2000 |
| 3e-26 | 2.6e4 | 104.1 | 0.551 | 0.18 | UNDETERMINED onset, fails even so |
| 1e-25 | 4.8e4 | 17.1 | 0.721 | 0.31 | PASS |
| 3e-25 | 8.4e4 | 2.3 | 0.800 | 0.46 | PASS |
| 1e-24 to 1e-21 | 1.6e5 to 4.9e6 | -0.0 to 0.1 | 0.82 | 0.81 to 18.9 | PASS |

Passes from 1e-25 up, as I expected. Dust from the start with onset read off RF5's window, all onsets for passers inside it.

## Selection, train only (`wf1_select.out`; first table `wf1_select_first.out`)
No m passes both train lines. SPARC train passes only at 1e-25 (rms 0.1671 vs the law's 0.1664), where the field is unbound in 27 of 75 train discs. X-COP train is closest at 1e-25 (-0.047, rms 0.143) and 3e-25 (+0.074, 0.136), and drifts to HF1's +0.19 as m rises and the core shrinks. Chosen 1e-25 by smallest |mean|.

## Gates 2 and 3 at m 1e-25, omega_f 0.11995 (`wf1_RUN_m1e-25_s1.out`), numbers only, canonical (alt beside)
| row | value | line |
|---|---|---|
| X-COP all | -0.049, rms 0.138 (alt -0.078, 0.150) | FAIL, rms |
| X-COP by x 0.1 to 0.7 | -0.242, +0.035, +0.075, 0.000, -0.112 | over-massive at 0.1 and 0.7 |
| Keys | 1 of 15 (alt 0); worst G-OUT-Mall -17.0; DA1 B = 1 and n(z) 2 of 15 | FAIL |
| SPARC | rms 0.0766, Upsilon 0.51, tilt +0.09; SB Z -0.25 | pass (alt Upsilon 0.42 fails, as the law's) |
| LITTLE THINGS | -0.025 | pass |
| Groups | Z -8.31, below the law | FAIL |
| Dwarfs, IC 1613 | the law's: UFD +5.22, IC Z -7.9 | stay with the law |
| Discs, M_f/M_b at R_last | median 0.001; V < 100 km/s 0.000; V > 200 km/s 0.79 | wave exclusion works in small discs only |

So gate 2 fails and gate 3 fails on groups. The field is pushed out of small and medium discs: unbound in 23,357 of 63,380 rows over the whole run. That's the wave scale doing the work, not a cap. But in clusters and groups it's the fair-share envelope that overshoots, as in HF1: the outer keys are over-massive by 13 to 17 sigma.

**Sigma bracket (amended reading, reported):** x 0.5 sinks into the core, X-COP -0.809, keys 0 of 15. x 2 X-COP -0.028 rms 0.246, keys 3 of 15, groups -8.09. No sigma rescues it.

## Controls
CLASS: RF5 limit dplik -0.002; m^(1/2) ratio 2.67 vs 3.16 (30 % line); m x 16 moves k_half x 3.91; K_jeans as frozen FAILED (today's k_J, my error), replaced post-control by k_J at equality (ratio 0.60) and HBG's recalled fit (0.81 vs 0.86, 0.31 vs 0.31), part 3. SP Newtonian: E -0.1627, r_half 3.928 in hbar^2/(G M m^2), virial -0.0003, after the control's own half-cell fix (part 4); m x 16 at fixed mass moves r_half by 16^-2 within 1e-12; grid doubling 1e-5. Law limit X-COP +0.467, 0.476, SPARC 0.0541; fair share within 2e-5; cluster grid doubling within 5e-5. Planted (fair share x 100, m 1e-22) fails gate 3: rms 0.681, Upsilon 0.30.

## Departures and what isn't verified
- Part 9 is post-result: the cluster grid floor moved after HF1's 1 kpc floor was shown to remove a real core. The selection was seen twice.
- The envelope doesn't feel the core's own potential (part 7); 22,699 rows have M_s above 30 % of the share, where this is worst.
- M_s rule (equal velocity) and the envelope-flat-inside-core rule are my readings; the bracket shows sigma matters a lot to clusters.
- Static, spherical; no formation, granule heating or rotation. Whether these states are reached isn't computed.
- Forest: k_half 0.31 h/Mpc at the chosen m, far below the forest's scales, so the suppression there is complete in linear theory. No PM, no verdict, but the warning is severe at 1e-25.
- The MW line in the report is HF1's fermion-cap text and doesn't apply here (prints 0).
- Published forest and dwarf bounds on this family are LambdaCDM-conditional, not used.

## Liabilities
No action couples this field to the a0 law. MW and IC 1613 stay with the law. The Bullet: lambda at 1e-25 and sigma 1000 km/s is about 0.3 Mpc, comparable to the merger scale, so collisionless offsets are not guaranteed here: not computed.
