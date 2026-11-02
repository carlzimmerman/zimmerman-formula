# TM2_time_lag_memory: no candidate. Fixed-frame memory is dead on the Bullet at every tau, both footings, in every frame tried. Along galaxy worldlines, scalar memory is dead too. Stored vector memory (W2) is the one reading that gets peaks and sign, misses main mass at k fit (Z +3.9 to +4.0), and PASSES only at k about 7-10 with a fitted tau of 300-600 Myr. Stored per star, orbits erase it and relaxed clusters fail; stored on the mean flow, discs spin up in about 1.4-2.7 Gyr. **K1 failed as frozen**, so by the frozen rule the labels below are not a clean verdict; cause diagnosed, see Checks

Asked as "TM1"; `TM1_tethered_medium` holds that id, so this is TM2. Criteria `FROZEN_CRITERIA.md` (f278973e0b), committed alone first. `AMENDMENT_A1.md` (1c4e067611) written after the first numbers, before its own. Scripts `tm2_map.py` (Bullet), `tm2_relaxed.py` (X-COP, keys, discs, self-force), `tm2_mg1.py` (merger rows), `tm2_verify.py` (A1, fresh code), `tm2_k1diag.py`; numbers in their `.out`, `.json`, twins `_MUTATE`. **Not blind.** A description: no action, no field equation. Histories come from simulations with massive halos, used as kinematics only; a term like this need not produce them. The cold sector stays retired; nothing here reinstates it. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## The hard catch, computed
Which theory? Memory at past gas positions in a fixed frame is one. Memory transported along galaxy worldlines is another. Memory along *gas* worldlines stays on gas and isn't a third option.
- **Fixed frame:** the galaxies lead their gas, so past gas lies behind present gas, farther from the galaxies. Position or sign fails in **968 of 968** F cells on all histories and frames. The rest frame of either subcluster fixes that subcluster and loses the other, at R-dyn, 300, 1200 Myr, canonical: main-rest dkappa +0.14 to +0.18 main, -0.32 to -0.48 sub; sub-rest -0.11 to -0.21 main, +0.18 to +0.24 sub. One frame can't ride with both.
- **Worth saying:** F2 at 1200 Myr has about the right amount: M300 3.74, 2.49 (Z +0.5, +0.6), ratio 0.67. It sits in the wrong place: main peak (380, 60), sub on its gas, dkappa -0.28, -0.60. Same as UX6's lesson, amount right, place wrong.

## Bullet, history P, canonical. Observed: peaks on galaxies, M300 3.5, 2.3 (1e14), ratio 0.66. Alt within about 0.3 Z; every cell in `tm2_map.out`
| Form | rule | peak main, sub: Z | dkappa m, s | M300 (Z) | ratio | class | label |
|---|---|---|---|---|---|---|---|
| F1 | R-dyn, k fit | -3.88, -3.47 | -0.32, -0.79 | 4.77 (+2.4), 2.29 (0.0) | 0.48 | FAIL | **DEAD** all rules |
| F2 | 1200 Myr, k fit | -0.44 (guard fails), -3.47 | -0.28, -0.60 | 3.74 (+0.5), 2.49 (+0.6) | 0.67 | FAIL | **DEAD** all rules |
| W1 | 600 Myr, k fit | -3.88, -4.10 | -0.40, -0.75 | 4.96 (+2.8), 2.10 (-0.6) | 0.42 | FAIL | **DEAD** all rules |
| W3 | 300 Myr, k fit | -2.81, -1.43 | +0.05, +0.28 | 5.22 (+3.3), 1.34 (-2.8) | 0.26 | FAIL | **DEAD** all rules |
| **W2** | 300 Myr, k fit | -0.44, -1.43 | +0.19, +0.38 | **5.62 (+4.0)**, 2.48 (+0.5) | 0.44 | FAIL | **WOUNDED** |
| **W2** | 600 Myr, k fit | 0.00, -1.43 | +0.25, +0.58 | **5.54 (+3.9)**, 2.05 (-0.7) | 0.37 | FAIL | **WOUNDED** |
| W2 | 300 Myr, pi^2 | -1.09, -1.43 | +0.12, +0.26 | 4.46 (+1.8), 2.03 (-0.8) | 0.46 | **PASS** | as above |
| W2 | 600 Myr, pi^2 | 0.00, -1.43 | +0.17, +0.41 | 4.40 (+1.7), 1.71 (-1.7) | 0.39 | **PASS** | as above |
| W2 | R-dyn, pi^2 | +1.35 (no local max), -1.43 | +0.14, +0.28 | 4.42 (+1.8), 1.69 (-1.8) | 0.38 | FAIL | **DEAD** |
| W2 | R-dyn2, pi^2 | 0.00, -1.21 | +0.20, +0.50 | 4.31 (+1.6), 1.29 (-2.9) | 0.30 | TENSION | WOUNDED |
| W2 | c/a0, pi^2 | 0.00, -1.21 | +0.21, +0.52 | 4.29 (+1.5), 1.22 (-3.1) | 0.29 | FAIL | WOUNDED |

W3 sits between UX6's N1 and N2 as it must, ratio 0.25-0.29. Its best margin is 3.05. W2's gain over W3 is that it keeps more of the sub.

## Tau window, or none, with margins
**At k fit, the frozen grade: none.** Every W2 cell fails, on all 7 histories, both footings; nearest miss margin 3.36 (alt, c/a0), and it's main's mass. BULLET PASS is earned by no rule. No derived tau passes at any k tried: c/a0 fails at pi^2 on sub mass, R-dyn on main peak; R-dyn2 reads TENSION at pi^2.
**Post-result (A1), counted: one fitted tau, and k moved off X-COP's fit.** Fresh code, 10 kpc, scan 7 to 20 in 0.5, so 7 is the scan's edge, not a found limit:
| tau Myr | PASS k, canonical (alt) | PASS or TENSION k, canonical (alt) |
|---|---|---|
| 150 | none (none): sub dkappa about 0 | none (none) |
| 300 | 7.0-10.0 (7.5-11.0) | 7.0-11.5 (7.0-13.0) |
| 600 | 9.5-10.0 (9.87-11.0) | 7.0-12.0 (7.0-13.0) |
| 1200 | none (none) | 7.5-12.0 (7.5-13.0) |
| 5000 | none (none) | 10.5-12.0 (10.5-13.5) |

k fit is 13.29 (14.25). CU1: 7-cluster bootstrap 11.3-13.7 (12.1-14.7), single clusters 8.7-18.1. At pi^2: X-COP fails, +0.065, 0.106 (+0.080), keys 12 of 15. If HSE is 0.12 dex high, CU1's refit is k 8.38, inside the window, X-COP by construction, keys 11 of 15. So **Bullet's k and X-COP's k overlap only at the edge of the error or under an HSE bias nobody here measured.** At pi^2 other histories hold: tau 300 PASS on t150, p2, b256, q40, TENSION on t260; tau 600 PASS on t260, p2, q40, on t150 canonical only (alt TENSION), TENSION on b256. Gas x 2 doesn't help at k fit: main stays +3.7 to +4.3. Boxcar kernel at k fit: all FAIL.

## Why W2 isn't a survivor: three transports, each closes a door
W2 stores a vector, more than a scalar memory, and I missed that when freezing: Part B first averaged |g_gas|. A1.2 ran it.
1. **Stored per star, parallel-transported. Relaxed clusters fail.** Past vectors rotate on orbits and cancel. m_v against tau/t_dyn: 0.43, 0.81; 1.2, 0.41; 3.2, 0.09. At 300 Myr m_v 0.16 to 0.77 from x 0.1 to 0.7, so X-COP k UX3 +0.197, 0.250 and k refit 29.5 still rms 0.187, FAIL; beta 0.5 same. Keys 8 of 15. And the Bullet with that factor: F-like, peaks fail in all cells, canonical and alt (`tm2_verify.out`). t_dyn there uses one velocity, 1500 km/s, PROVISIONAL. This form is dead.
2. **On the mean stellar flow, parallel. Relaxed unchanged, discs spin up.** A relaxed cluster's mean flow is zero, so it reads as UX3. Discs do something new: radial term x 1/(1 + (V tau/R)^2), which reads the law, even rms 0.187 at 300 Myr, 0.186 at 600, canonical; **better than UX3's 0.223**. But the same stored vectors pull forward along the orbit. At k UX3, spin-up time V/a_t: **median 1.4 Gyr at 300 Myr, 2.7 at 600**, 5 % 0.33, 0.63; 80 %, 76 % of SPARC points under 10 Gyr. That's an estimate on rotation-curve points, not a disc model, but it's short against disc ages, and I count it as failed.
3. **On the mean flow, rotating with it.** Not computed separately: no torque, m = 1, so discs read UX3's unswitched row, DISC BREAK, and C1's switch would be needed, whose pass carries no evidence (UX3). Bullet row as above. This is the only unclosed reading. It owes the k gap, a transport law and an action.

## Relaxed clusters and discs, per form
| | X-COP (k UX3 fixed) | Keys | Discs |
|---|---|---|---|
| F, COM | identity, unchanged | 14, 10 | unswitched: **DISC BREAK** |
| F, moving v 300 at R-dyn, 300 Myr | -0.014, 0.088 and -0.012, 0.087, PASS | not run, near m = 1 | R-dyn **BREAK**; 300 Myr **PASS** canonical, alt fails at k fit, passes at pi^2: **better**. A switch by motion |
| F, c/a0, v 300 | +0.137, FAIL; refit 24.8 FAIL unseen | | PASS, because the term is gone |
| W scalar, R-dyn, 300, 1200 | PASS; m 0.93-1.05 | 14, 10, OUT-all -2.7 to -2.8; no change from UX3 | m = 1, K10 reproduces; epicycle 10 % changes nothing: **DISC BREAK**, same not better |
| W scalar + gas growth, c/a0 | factor 0.31, +0.261, FAIL; refit k 45 PASS | | |
| W scalar, c/a0, stars once gas | | | rms **0.71 to 0.79**, far **worse** |
| W scalar + C1 | | | PASS, by construction |

**Self-force, F2:** a moving body chases nothing, it's pulled back by its own past. Cluster, 500 km/s: stopping time **0.15 to 0.29 Gyr**, both footings. Disc, 300 km/s: 3 to 17 Gyr. So F's disc improvement is bought with drag and breaks Galilean invariance. W is Galilean on a steady flow.

**Causality:** retarded by construction; max transport 4870 km/s, v/c 0.016, K7. Light-cone kernels give no lag at this size: v r/c is 9 kpc per Mpc at 2700 km/s, and a uniformly moving source's retarded field points at its present position, so box^-1 can't do this. Timelike memory needs a preferred frame (F) or a unit flow (W): DR4's listed cost, with a stored vector on top. No action written.

## MG1's rows, pair model, PROVISIONAL, ages PROXY except Bullet and Musket Ball
dkappa > 0 at the 8 GAL primary rows, k fit, both footings:
| | R-dyn | 50 | 200 | 1000 | 5000 Myr |
|---|---|---|---|---|---|
| F2 | 0 FAILS | 0 | 0 | 0 | 0 |
| W2 | 3 FAILS | 0 | 3 | 7 HOLDS | 8 HOLDS |

Post-result at pi^2: W2 at 300 Myr 4 (alt 3) FAILS; 600, 6 HOLDS; 1000, 7 (alt 6); 5000, 8; R-dyn 1.
**Memory fades, and that's the one new test.** R-dyn is dead in general. Musket Ball S at its published 1.1 (+1.3, -0.4) Gyr: W2 dkappa -0.49 at R-dyn, -0.06 at 1000 Myr, +0.18 at 5000; pi^2 -0.17 at 600, -0.07 at 1000, +0.11 at 5000. ZwCl 0008 E at PROXY 411 Myr: -0.87, +0.47, +0.77. **So old mergers want tau above about 1-2 Gyr; the Bullet's PASS is at 300-600; from 1200 Myr up the Bullet reads TENSION at best, sub short.** Bullet's PASS and Musket Ball don't overlap; a TENSION window does. Sign at long tau is near construction, as MG1 warned. Musket Ball's age error is large and one row is one row.

## What the record already closed
- **X32:** cold sector on the Bullet UNDECIDED, K4 failed. This lane adds no cold anything.
- **UX6:** N2 owed a carrier; this lane is its unfinished item. The carrier here is a transported field on the stellar flow, not a particle, and it's still a carrier in function.
- **CFG726:** merger memory on conserved cold energy FAILS on T-R, T-A, T-E, T-B not run; different mechanism.
- **DR4:** box^-1 R is a potential plus a calendar; a clock needs a timelike flow, a start surface; L3 fails. **CFG70:** memory kernel causal action, scoped NO on the static reaction; memory time doesn't change static statements, which is why a relaxed cluster can't tell. **CFG349:** ratchet along baryon flow, no legal action; L-CTP doesn't conserve momentum, which is W's unpaid bill too. **CFG120, CFG123, CFG153:** Mashhoon-type linear kernel and DW/RR static response, scoped no-go, RR short by 10 dex.
- Background, PROVISIONAL, not used for a number: [Hehl & Mashhoon](https://ar5iv.labs.arxiv.org/html/0812.1059), memory reading of nonlocal gravity; Mashhoon reports GW damping as a cost. Deffayet & Woodard not reread here, carried from the record. Search found no published Bullet test of nonlocal memory; one search, so absence isn't established.

## Histories, PROVISIONAL, via a summariser
[Springel & Farrar](https://ar5iv.arxiv.org/html/astro-ph/0703232): 1.5e15, 1.5e14, f_b 0.17, 180 Myr after passage, bullet centroid about 2600 km/s; c = 3 match about 1420 against passage near 1200. [Mastropietro & Burkert](https://ar5iv.arxiv.org/html/0711.0967): 7.13e14, 1.14e14, b 150, about 0.15 Gyr. [Lage & Farrar](https://ar5iv.arxiv.org/html/1312.0959): 1.91e15, 2.59e14, b 256 +- 35, f_gas 0.19, 0.17. Musket Ball age from [this paper](https://arxiv.org/pdf/1611.07040) citing Dawson 2013; press says 700 Myr. Model frame's D 849 kpc implies 4700 km/s mean in P, above published speeds; measured separation is 720.

## Checks, every failure listed
- **K1 FAILS as frozen:** peak 41 kpc on N1's row, limit 28. M300 within 1e-4, dkappa 0.2 %. A1.1: at 10 kpc with the same code all four W3 limit rows match UX6's peaks exactly and M300 to 1e-4; N1's sub has no local maximum and sits on the window's edge, so its position is grid-set. **Frozen rule says this stops the verdict; I report labels with that stated and the owner can read it as he likes.** K1 not rewritten.
- K2 2e-16 (W3 6e-5). K3 4e-3. K4 -1.4 %. K5 3.37-3.41 GB. K6 PASS, FAIL as required. K7 v/c 0.016. K8 2e-5; m to 1, 3e-4. K9 14, 10. K10 0.208, 0.213. K6c +1.259.
- Fresh W2 code against the grader, P, pi^2, 300 Myr: M300 4.42, 2.01 against 4.46, 2.03 (map sum against surface); labels same.
- **MUTATE:** K1, K2, K6, K7 fail; K8 fails, 12 against 1e-3; K6c fails. Exit 1. **K11 fails on one file as written:** `tm2_map.out` differs in six printed memory lines, RSS 3.37 against 3.41 GB, and nothing else. Every other output, all JSON and all twins rerun byte-identical.

## Errors, disclosed
A first `tm2_relaxed.py` crashed on nodes shorter than the step, before any number; fixed. A1.2's missed vector reading is the big one: had I read only Part B I'd have said W2's relaxed rows hold. Part C's script gained a `TM2_POST` switch after its first run; frozen output byte-identical. In W3 tau_dyn is about each BCG, not the nearest, a small difference from the frozen text. Guessed arXiv numbers on first fetch returned unrelated papers; no numbers taken from them. F's X-COP rows carry m but not the self-force. Scan's 7 is a grid edge.

## Expectation against result
F DEAD 90 %: yes. W2, W3 sign at tau >= t, 75 %: yes from 300, 80. BULLET PASS at any tau 10 %: at k fit no, as frozen; the PASS at pi^2 I didn't foresee, and thought sub mass would stop it; W2's vector form kept the sub. c/a0 fails relaxed or discs 80 %: only with gas growth or stars-as-gas; bare W at c/a0 passes X-COP. W discs not better 85 %: scalar yes; vector no, then torque. F moving better 60 %: yes. Candidate 5 %: none.

## Limits, unfinished
Straight-line histories, no orbit from this term. Plummer, no inclination, a0 at z = 0. Masses a lens reconstruction, 15 % and the position sigma X32's PROVISIONAL. Star flow on the map is one bulk motion per subcluster; internal smear only through m_v's table. Spin-up is an estimate on rotation-curve points, not a disc model. Gas-free dwarfs under W: not run. Reading 3 not run as one system. MG1's proxies as MG1's limits. Nothing second-implemented beyond W2's fresh code, and no candidate to hand one. Needs, not on disk: MG1's named map files; pre-merger gas per subcluster.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
