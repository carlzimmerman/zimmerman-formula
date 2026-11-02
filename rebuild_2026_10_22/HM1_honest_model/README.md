# HM1_honest_model: NO VERDICT AS FROZEN, because K4 failed. The numbers read FAILS on S, Tl, LT, G, K, X, Ln, Dw, IC [GAS-CONDITIONAL] [RESPONSE-DEPENDENT]. The measured response makes the native shape worse on clusters: G-OUT-M3 +4.41 to +4.60, keys 12 to 10, X-COP from pass to fail

Criteria: `FROZEN_CRITERIA.md` (3bd02214d4), committed alone first. `hm1_clusters.py`, `hm1_def.py`, `hm1_tail.py`, `hm1_gal.py`, `hm1_spx.py`, `hm1_kn1.py`, `hm1_op1.py`, `hm1_weigh.py`, `hm1_ng80proxy.py`, `hm1_read.py`; numbers in `hm1.out`, `hm1_results.json`. Other lanes read only. kappa = 1/2 FITTED, unused. EM1's M200 line is fitted, in every galaxy row. No a0 in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** the galaxy rows were on record. Retiring anything is the owner's decision. No Argon proposal was read or used.

## Why no verdict
K4 asked M_c(r_ta) after / before within 1e-3 on every cluster. It's over in 46 of 652 cluster-h cells, up to 9.5 %; read one grid step past r_ta, 75 cells, up to 16 %. Those are mostly low-mass clusters (26, 18, 2 by tercile) whose native shape closes in a thin shell at r_ta, where the response moves shells past each other. So the "held" I froze isn't exactly held there. **AMENDMENT A1, post-result:** return that mass as a shell at r_ta. Max |dZ| over all keys 0.001, X-COP unchanged, same failing keys. So it doesn't drive any number below. A1 doesn't restore a verdict, as in OE1. All other checks pass.

## C5 on FG1's lines, canonical, primary: frozen map, f_Q 0.872 Blumenthal, BCG as CN1, gas +0.005, f* 0.034
| Line | Status | Numbers |
|---|---|---|
| S | **FAIL** | Y 0.44/0.41, rms 0.0726/0.0710 [HM1, = SP3] |
| Tl | **FAIL** | +0.29/+0.25 [HM1, = SP3] |
| LT | **FAIL** | +0.236/+0.226 [HM1, = SP3] |
| G | **FAIL** | Z +2.08, ABOVE LAW, not contracted, as OP3 [HM1, = SP3]. FC1's map +1.91 passes, Y 0.39/0.37 |
| K | **FAIL** | 10 of 15: G-MID-T2, G-MID-T3, G-OUT-M2, G-OUT-M3, G-OUT-Mall; M3 +4.60, +4.25 [HM1] |
| X | **FAIL** | +0.058, 0.093 [HM1]; f* 0.0615 +0.0504, 0.088, a miss by 0.0004 |
| Ln | **FAIL** | class LAW, dchi2 +357.9, alt +387.2 (f 0: +366.0) [HM1] |
| Dw | **FAIL** | +9.92, +5.07, +3.76, +3.38, +2.73 (f 0: +10.63, +5.18, +4.08, +4.63, +3.49) [HM1] |
| MW | PASS | FEASIBLE IN PRIORS, 11 cells [HM1, = SP3] |
| DM | PASS | r 1.080, n 28 [HM1, = SP3]. CFG577's Jeans 5-7 % would take it to about 1.14 and out |
| IC | **FAIL** | E -0.372, Z -4.9 [HM1], LITTLE THINGS' row, ND1's sE |

Nothing is NOT GRADED. The lines aren't independent, so no count ranks this against FG1's candidates.

## Cluster cells (`hm1.out` has all 34)
| Gas, f*, row | keys | G-OUT-M3, h 0.672, 0.686 | X-COP |
|---|---|---|---|
| +0.005, 0.034, f 0, none (= ZN4) | 12 | +4.41, +4.07 | +0.013, 0.075 PASS |
| **+0.005, 0.034, f_Q, BCG (PRIMARY)** | **10** | **+4.60, +4.25** | **+0.058, 0.093 FAIL** |
| +0.005, 0.034, f_Q, none | 10 | +4.61, +4.26 | same |
| +0.005, 0.034, Blumenthal, BCG | 10 | +4.63, +4.28 | +0.066, 0.098 FAIL |
| +0.005, 0.034, Gnedin, BCG | 10 | +4.61, +4.26 | +0.055, 0.091 FAIL |
| +0.005, 0.034, f_Q, BCG, CN1's F, reported | 12 | +4.36, +4.03 | +0.040, 0.082 PASS, M_c(r_ta) not held |
| +0.005, 0.0615, f_Q, BCG | 12 | +4.33, +3.99 | +0.0504, 0.088 FAIL |
| +0.005, 0.0615, Gnedin, BCG | 12 | +4.33, +4.00 | +0.047, 0.086 PASS |
| +0.111, 0.034, f_Q, BCG, reported only | 15 | +1.78, +1.57 | +0.058, 0.093 FAIL |
| +0.111, 0.0615, f_Q, BCG, reported only | 15 | +1.43, +1.24 | +0.0504, 0.088 FAIL |

Joint chi^2, primary, four cells: 40.3, 42.6, 36.0, 38.5 for 15, p 4e-4 to 2e-3, all JOINT FAIL; f 0 was 35.9, 38.2, 31.9, 34.2. R is M3A1's, from the f 0 row, applied to the response rows. Z_tot on G-OUT-M3: +3.67, +3.38, +3.45, +3.18; f 0 +3.51, +3.24, +3.29, +3.03.

**Tags.** [GAS-CONDITIONAL]: K's failure goes at +0.111, and X doesn't, so even there it isn't a pass at f* 0.034; the verdict stays on GS4. [RESPONSE-DEPENDENT]: at f* 0.0615 Gnedin's X passes and f_Q's misses, by a hair. BCG changes nothing: |dZ| about 0.01-0.02.

**Why worse.** The response is outward at every radius on this shape: M_f/M_0 0.77, 0.82, 0.88, 0.91, 0.96, 0.99 at 0.05, 0.15, 0.3, 0.46, 1, 2 Mpc. It takes cold mass out of X-COP's window and out of the shear's enclosed mass, and helps only G-IN. Because M0(r_ta) sits under the budget (below), F = Mb/M0(r_ta) is above the cosmic ratio, so more radii lie on the outward side than in UR1's row. CN1's F moves it back: X passes, keys as ZN4. That's a real dependence on what "budget" means here. I froze M0's own, and hold it as primary.

So on the clusters this row is worse than no response. On the weighings it's the reverse: no response fails MW and DiskMass, and f_Q passes both. That's the same tension as OP3, now with clusters on it.

## Galaxies, other rows
| Row | Y | tilt | LT | groups | IC |
|---|---|---|---|---|---|
| tot, off | 0.84/0.81 | +0.55/+0.56 | +0.304/+0.290 | +2.08 | -4.1 |
| **tot, f_Q** | **0.44/0.41** | **+0.29/+0.25** | **+0.236/+0.226** | **+2.08** | **-4.9** |
| FC1, off | 0.75/0.69 | +0.58/+0.59 | +0.283/+0.269 | +1.91 | -4.4 |
| FC1, f_Q | 0.39/0.37 | +0.20/+0.15 | +0.219/+0.208 | +1.91 | -5.2 |
| tot, Blumenthal | 0.39/0.38 | +0.27/+0.23 | +0.225/+0.215 | +2.08 | -5.1 |
| tot, Gnedin | 0.41/0.40 | +0.17/+0.12 | +0.256/+0.245 | +2.08 | -4.8 |
| tot, f_Q, ng 80 proxy, not a grade | 0.45/0.43 | +0.31/+0.28 | +0.236/+0.226 | +2.08 | -4.9 |

Gnedin's row clears tilt but not Y. Native reads no eta, so NR2 doesn't enter this row. KiDS: FC1's map +345.9. Local Group's response is small, as OP3 said.

**ng 80 at 1e12.** No z = 0 table exists: A5's runs stop at z_f, and continuing nine seeds is many CPU-hours on one thread, so I didn't. The proxy carries z_f's ng 80 / ng 64 difference in ln m (-0.11, -0.13, -0.05 at x 0.05, 0.1, 0.2) onto the z = 0 row. It moves Y by +0.01 to +0.02. KiDS uses ZN1's ng 64 tags, as KN1 does.

## The puzzle
**Pred 1.558 is NR3's S-core at f 0 on eRASS1's own gas, 1.566 at +0.005.** Same 109 clusters, same grader, K5 reproduces NR3 to 5e-10. So on +0.005 the S-core reads G-OUT-M3 -0.05 at f 0 and +0.26 with Blumenthal.

**The difference isn't at the band's radii. 92 % of it is cold mass inside R200.**
| r Mpc | 0.05 | 0.1 | 0.2 | 0.3 | 0.46 | 0.7 | 1 | 1.42 | 2.06 | 3 | 4.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| r / R200 | 0.04 | 0.08 | 0.16 | 0.24 | 0.37 | 0.56 | 0.80 | 1.14 | 1.65 | 2.40 | 3.60 |
| M_c native, 1e13 | 0.30 | 0.99 | 3.00 | 5.37 | 9.08 | 14.2 | 19.4 | 24.6 | 30.3 | 36.3 | 41.2 |
| M_c S-core, 1e13 | 0.19 | 1.19 | 5.53 | 10.6 | 17.8 | 26.1 | 33.5 | 41.1 | 49.3 | 57.7 | 66.7 |
| M_c S / native | 0.62 | 1.20 | 1.79 | 1.92 | 1.91 | 1.81 | 1.70 | 1.62 | 1.59 | 1.55 | 1.57 |
| rho S / native | 0.92 | 1.80 | 2.20 | 2.06 | 1.74 | 1.49 | 1.40 | 1.42 | 1.39 | 1.66 | 1.36 |

| Piece of M3's pred | S-core | native | S - native |
|---|---|---|---|
| baryons | 0.176 | 0.175 | 0.000 |
| cold < R200 | 1.239 | 0.759 | **+0.481** |
| cold R200 to 1.42 Mpc | 0.065 | 0.044 | +0.022 |
| cold 1.42-2.06 | 0.100 | 0.071 | +0.029 |
| cold 2.06-3 | -0.003 | -0.001 | -0.002 |
| cold 3 to r_ta | -0.012 | -0.008 | -0.004 |
| total | 1.566 | 1.040 | +0.525 |

**What makes it.** The two rules close differently. S-core puts all of Mfair inside r_ta: M_c(r_ta)/Mfair 1.000, M_c(R200)/Mfair 0.484. Native sets fair share at R200 on the measured gas, then follows the zoom's shape to r_ta, so M_c(R200)/Mfair 0.297 and M_c(r_ta)/Mfair 0.694 [0.641, 0.766]. **Native leaves 0.306 Mfair outside r_ta,** about 2.5e14 for M3's median. The S-core's excess isn't an inner feature: it's near × 1.6-1.9 everywhere outside 0.1 Mpc, peaking at 0.2-0.5 Mpc. Inside 0.1 Mpc the core runs under native.

**X-COP sees the same excess.** S / native at its radii: x 0.1, 136 kpc, 1.2, resid -0.025 vs -0.032; x 0.2-0.7, 270-950 kpc, × 1.7-2, resid -0.18 to -0.20 vs +0.01 to +0.04. So X-COP measures this excess directly, at 0.3-1 Mpc, and rejects it, and M3's lensing needs a good part of it inside about 1.4 Mpc. That's the whole puzzle: one mass excess, wanted by one test and rejected by another, in overlapping enclosed mass.

**Requirement, from these two curves, no fit.** ΔΣ at 1.42-3 Mpc reads M_c(<R)/pi R^2, so location inside 1.4 Mpc hardly matters. Rate 2.56 of pred per unit M_c(<R200)/Mfair.
- **M3 at Z = 2: +0.284 of pred, +0.111 Mfair, 8.9e13. At Z = 0: +0.519, +0.203 Mfair, 16.4e13.** That's 36 % to 66 % of what native holds outside r_ta, so the budget allows it. It means M_c(<R200) × 1.37 to × 1.68, cold over baryons at R200 7.4 to 9.0 against fair share's 5.36. **Fair share at R200 on measured gas has to give.**
- **Where it can go:** outside X-COP's graded reach and inside the band. M3's 0.75 R500 is 0.555 Mpc [0.482, 0.694], so R500 about 0.74 Mpc.
- **Diagnostic, NOT A RULE:** native inside 0.75 R500, max(native, S-core) outside: **15 of 15, M3 +0.82, +0.67, X-COP +0.013, 0.075**, with a step of 0.131 Mfair [0.120, 0.138] at the join, about doubling M_c there. X-COP is unchanged only because it tests inside the join.
- **That diagnostic fails the row just beyond the frozen cut.** X-COP's x = 1 row, post-result, no grade, 7 clusters, about 1.36 Mpc: native -0.037, S-core -0.180. So if X-COP's R500 row is trusted, the mass can't start at 0.75 R500. It has to sit at R500 or beyond: for M3 about 0.74 to 1.42 Mpc, 0.6 to 1.14 R200. By hand from the table, native holds about 9.7e13 there, so the density there has to be × 1.9 to × 2.7, and dlnM/dlnr 1.24 to 1.55 against native's about 0.8, then falling back beyond. A bump in rho r^2 near R200 that neither curve has. Hydrostatic bias at R500 could relax this; RF3 has X-COP without hydrostatic masses UNDETERMINED.
- **The other reading, not a shape at all.** X-COP's R500 is about 1.36 Mpc against M3's 0.74, so about × 6 in mass, and M3A1 has the miss mostly in M3's lighter half (+4.61 vs +1.81). X-COP doesn't test those masses. A normalisation rising toward lower cluster mass, × 1 at X-COP's and × 1.4 to × 1.7 at M3's, would meet both with native's shape. That is the same statement as GS4's gas scale problem (+0.111 gives 15 of 15), and these two curves can't separate shape from mass dependence. Not tested here.
- The response goes the wrong way for this: it lowers M_c by 5 % at 1 Mpc and 3 % at 1.42 Mpc.

## Limits
X-COP rows carry no BCG, as XH1, and F there uses its own gas budget. Groups aren't contracted, as OP3. LC1's f_Q was measured at 1e12 in a smooth disc, and is used here at 1e15, where gas was heated and displaced: an adiabatic response on hot gas is an assumption, as UR1 said, and CN1 notes the sign is doubtful. Dw uses Plummer baryons; LITTLE THINGS clamps shapes below 1e10. 1e13 is ng 64. EM1 is fitted. The bootstrap wasn't run, as frozen: no win. R in the joint test comes from the f 0 row. The x = 1 and hand-arithmetic rows are post-result.

## Expectation on record
FAILS 97 %: as read, with no verdict by my own K4, which I didn't foresee. X failed, I'd said 50 %. Keys 10, I'd said 12-13: wrong, the response pushed G-MID-T2 and G-OUT-M2 over. M3 in my range. Tag fired, I'd said 40 %. Puzzle: budget outside r_ta right, but I expected the action at 1-3 Mpc, and 92 % of it is inside R200.

## Checks
K1 ZN4 preds, X-COP 0, 4 cells. K2 SP3's rows 0. K3 5e-14. **K4 FAIL, above.** K5 S-core vs NR3 5e-10, 2.5e-10 with CN1's F; 3.9e-5 with this lane's F, so UR1's row and this lane's differ by that. K6 KN1 0, OP1 0. K7 sign, as above. Joint vs M3A1 0. MUTATE f x 0.5: M3 +4.50, X-COP +0.035, keys pred up to 0.218, Y 0.60, KiDS +360.4: BITES. Read rerun byte-identical. **My errors, fixed before reading those rows:** first shell split used pieces alone, and the grader's floors hid negative parts, sum 1.064 against 1.040; replaced by OE1's telescoping chain, sums exact. `hm1_read.py` drops only M3A1's n(z) block to build R, whose KiDS column path isn't set here; R checks against M3A1 exactly.

kappa = 1/2 FITTED. Not theory closed.
