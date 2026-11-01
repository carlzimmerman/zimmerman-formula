# DR3_thin_disc_monopole: NOT HALVED, MOVES, for Blumenthal and Gnedin. The true disc monopole lowers the response by about 10 % in spirals and leaves the 150–250 km/s bins near where they were. SPARC's line stays failed

Criteria: `FROZEN_CRITERIA.md` (ca7006d189), committed alone first. `dr3.py`, `dr3_tail_add.py`, `dr3_read.py`, `dr3_gasinv.py`, `dr3_ur3.py`, `dr3.out`, `dr3_ur3.out`, `dr3_*results.json`, `dr3_ur3.json`. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** NR3, UR1, UR2, UR3, RM1 and LC1 were read. The first run stopped on an undefined constant in my tail before any number.

## The claim against the record
- **The force is already there.** SPARC's GB comes from V_disk, V_gas, V_bul, which are midplane forces from the measured profiles. No "+18 %" is left to add.
- **"All response runs use spherical M_b" is wrong in detail.** SPARC, DiskMass and the Milky Way take v² r/G, which is neither spherical mass nor the monopole. Over the exponential's monopole it is 0.76 at 0.5 R_d, 1.05 at 1, 1.32 at 2.2, 1.25 at 5 and 1.06 at 10. So the idea has a real target, about 15–20 % of M_b in spirals at 2–4 R_d.
- **RM1** named disc geometry only as a proposal its envelope covers. No lane had run this.

## Grades, NR3 MEDIAN's inputs, canonical, f★ 0.034
| Row | Υ A/B | rms A | tilt A/B | Υ 150–200, 200–250 (A) | Υ low bins 20–60, 60–100 (A) | Groups Z | LITTLE THINGS A/B |
|---|---|---|---|---|---|---|---|
| EM1, off | 0.75/0.76 | 0.0690 | +0.59/+0.59 | 0.57, 0.62 | 1.20, 1.18 | +1.47 | +0.153/+0.147 |
| EM1, Blumenthal = NR3 | 0.35/0.36 | 0.0670 | +0.17/+0.18 | 0.30, 0.365 | 0.495, 0.53 | +1.50 | +0.116/+0.109 |
| **DR3, Blumenthal (primary)** | **0.33/0.33** | **0.0645** | **−0.01/−0.02** | **0.32, 0.365** | **0.315, 0.35** | **+1.50** | **+0.116/+0.109** |
| EM1, Gnedin | 0.42/0.42 | 0.0632 | +0.21/+0.22 | 0.35, 0.425 | 0.545, 0.60 | +1.50 | +0.125/+0.119 |
| **DR3, Gnedin (primary)** | **0.44/0.44** | **0.0616** | **+0.16/+0.18** | **0.38, 0.445** | **0.655, 0.56** | **+1.50** | **+0.125/+0.119** |
| EXP stars, Blumenthal | 0.35/0.35 | 0.0639 | −0.01/−0.01 | 0.31, 0.365 | 0.315, 0.39 | +1.50 | +0.116/+0.109 |
| Gas as now, Blumenthal | 0.37/0.37 | 0.0646 | +0.16/+0.16 | 0.31, 0.37 | 0.50, 0.52 | +1.50 | +0.116/+0.109 |
| DR3 × LC1's f_Q 0.872, Blumenthal | 0.37/0.38 | 0.0629 | +0.04/+0.04 | 0.34, 0.39 | 0.385, 0.41 | +1.49 | +0.121/+0.114 |

Keys and X-COP don't move: 14/15, G-IN-Mall failing, X-COP −0.097, 0.146 (Blumenthal) and −0.102, 0.152 (Gnedin). They have no disc. Groups and LITTLE THINGS are identical to the off rows (K5). The f_Q row changes keys' predictions slightly, still 14, X-COP −0.106, 0.150.

## Frozen label
**Blumenthal: NOT HALVED, MOVES. Gnedin: NOT HALVED, MOVES.** The half line needed Υ ≥ 0.40 and 0.4325 (Blumenthal), ≥ 0.425 and 0.4625 (Gnedin). They read 0.32, 0.365 and 0.38, 0.445. Gaps to 0.50 go from 0.20, 0.135 to 0.18, 0.135, and from 0.15, 0.075 to 0.12, 0.055. Baseline 0.30 is the grid floor, so the 150–200 gap is understated. Every row fails Υ and LITTLE THINGS. **The claim "cuts the pinch in half" fails.**

My expectation held on the label but not on the sum: I wrote Blumenthal Υ 0.38–0.40, and it reads 0.33. The primary lowered the low bins, which I did not expect.

## Stress after the result: the low bins are the gas shape, not the idea. No line moved
The primary's tilt of −0.01 looks like a pass, so I checked it. Compare "gas as now", tilt +0.16: the change comes from my exponential gas, which is by hand and has no root in 74 of 175 galaxies (x = 2 used; 4 more kept V_gas). HI that is flat inside is not exponential.

So, added after these numbers and not in the criteria: `dr3_gasinv.py` inverts SPARC's own V_gas into a nonnegative thin-ring profile, total pinned to 1.33 M_HI. On an exponential at SPARC-like sampling it recovers M(<R) within 7 % at the first points and 3 % beyond 1 R_d, biased high.

| Row, measured gas | Υ A/B | rms A | tilt A/B | Υ 150–200, 200–250 (A) | Υ 20–60, 60–100 (A / B) | LITTLE THINGS A/B | label on the frozen rule |
|---|---|---|---|---|---|---|---|
| Blumenthal | 0.36/0.37 | 0.0646 | +0.05/+0.09 | 0.31, 0.365 | 0.355, 0.43 / 0.41, 0.49 | +0.116/+0.109 | NO MOVE |
| Gnedin | 0.45/0.45 | 0.0619 | +0.18/+0.19 | 0.38, 0.445 | 0.605, 0.60 / 0.625, 0.62 | +0.125/+0.119 | NOT HALVED, MOVES |
| Blumenthal × f_Q 0.872 | 0.40/0.40 | 0.0630 | +0.15/+0.16 | 0.34, 0.39 | 0.53, 0.53 / 0.545, 0.54 | +0.121/+0.114 | not labelled |

Inverted gas inside 1 R_d is 3.6 × V_gas² r/G (median), because V_gas² is small or negative there. So a true inner gas mass is real, and it does contract dwarfs harder. **The tilt on Blumenthal does clear with measured gas (+0.05/+0.09), but by pulling dwarfs down to spirals' low Υ, not by lifting spirals.** The low bins scatter between backgrounds (0.355 vs 0.41), so that tilt is soft. It's a reading, not a pass.

## Effective response, (Q_DR3 − 1)/(Q_off − 1), Υ 0.5, background A
| V_flat | n | r₀ | 2 R_d | 3 R_d | 4 R_d | M_b ratio, 2–4 R_d |
|---|---|---|---|---|---|---|
| 20–60 | 12 | 0.86 | 0.90 | 0.90 | 0.80 | 0.88, 0.83, 0.74 |
| 60–100 | 35 | 1.01 | 1.07 | 0.87 | 0.79 | 1.00, 0.83, 0.71 |
| 100–150 | 23 | 0.88 | 0.93 | 0.82 | 0.78 | 0.87, 0.76, 0.73 |
| 150–200 | 25 | 0.85 | 0.90 | 0.87 | 0.85 | 0.84, 0.80, 0.78 |
| 200–250 | 18 | 0.91 | 0.93 | 0.90 | 0.90 | 0.88, 0.83, 0.84 |
| 250–400 | 10 | 0.87 | 0.91 | 0.89 | 0.88 | 0.84, 0.80, 0.78 |

So DR3 is about RM1's family G at f 0.9, which there reads bins 0.30, 0.38: the same size of effect. The bins can't halve at this strength: RM1 needs f near 0.5 for 0.40, 0.47.

## LC1: consistent, and they are different factors
LC1's Q Blumenthal already uses its Kuzmin disc's true monopole (reproduced exactly on all nine seeds, same-seed particles). So **f_Q 0.872 [0.54, 1.07] is on top of the monopole, not the monopole itself.** Live against v² r/G of the same disc: **0.78 [0.48, 0.96]**. Same disc, monopole over rotation-mass response: 0.90 Kuzmin, 0.83 exponential. DR3 on SPARC's spirals at 2–4 R_d: **0.90, inside LC1's range.** So LC1's zoom includes this geometry, DR3 is consistent with it, and the factors stack: 0.78 ≈ 0.90 × 0.87. The honest stacked row is DR3 × 0.872: Υ 0.37/0.38, fail. LC1's earlier SPARC carry put 0.872 on rotation mass, which leaves out this factor. One mass, gravity only, NFW start instead of the smooth core, so this is a read-across, not a grade.

## UR3, read across (`dr3_ur3.out`). Doesn't enter the label
| Mode | DiskMass r at 1.5 h_R, off → on | Υ_K on | Milky Way box, off → on | McMillan V_c, K_z on |
|---|---|---|---|---|
| Blumenthal | 1.071 → **1.080 [1.053, 1.167], REACHED** | 0.286 | V+K ONLY → **FEASIBLE IN PRIORS**, 5 cells, 1 in prior, D 0.98 | 245.7, 79.5 |
| Gnedin | 1.118 → 1.156 [1.111, 1.242], NOT REACHED | 0.357 | FEASIBLE IN PRIORS → same, 17 cells, 6 in prior, D 0.73 | 229.7, 74.9 |

The in-prior Blumenthal cell is R_d 2.60, M★ 4.90e10, V_c 238, K_z 66.1. **UR3's Blumenthal SPLIT goes away:** both weighings are reached, narrowly, on one cell, and CFG577's Jeans integral (+5–7 %) would still move 1.080 outside 1.1. UR3's stress still governs: both weigh inner cold mass, not the response, and NFW with no response does about as well. SPARC's Υ doesn't follow.

## Limits
Stress rows use a soft thin-ring kernel, biased high in M by a few %. Gas in the primary is shaped by hand. Scale height ignored. Spherical cold response kept. EM1 fitted, core shape by hand. KiDS not run; Local Group not run.

## Checks
K1 DR3 off equals NR3 MEDIAN: EM1 off and Blumenthal rows, |d| 0. K2 integrator 2.4e-6. K3 Freeman as above. K4 SB integrated over L[3.6]: median 0.946 (16–84: 0.844, 0.992). K5 preds, X-COP, groups, LITTLE THINGS |d| 0. MUTATE monopole × 2: Υ 0.33 → 0.30, bins 0.30, 0.30, bites. DR3 Blumenthal rerun in the stress process, |d| 0. UR3 reproduced with the monopole off, |d| 0, classes same.

κ = ½ FITTED. Not theory closed.
