# FR3_retention_independent: W FAVOURED on the frozen primary, but a second HSC reading contradicts it. Through FR1's grader the line overshoots: PARTLY [X-COP LOST] as frozen, 4 of 15 keys. Part B UNDECIDED

Criteria: `FROZEN_CRITERIA.md` (d56ce53b3a), committed alone first. Scripts `fr3_parse.py`, `fr3.py`, `fr3_diag.py` (post-result), `fr3_y.py`, `fr3_grade.py`, `fr3_read.py`. Downloads in `data/`, gitignored, logged in `FETCH_LOG.md`. **Not blind.** **This reinstates nothing: the cold sector stays retired by the owner.** Galaxies untouched. kappa = 1/2 FITTED, unused. Cold dark energy, never a particle. No a0 in the cold sector. Not theory closed. Nothing here says the data favour the framework.

## Primary: Okabe+25 WL masses x eRASS1 gas
41 clusters, z <= 0.5, binned on eRASS1 gas (lg 12.75-13.58), never on WL mass. Linear ratio of means, eq. 17 applied.

| | x = lg M500 | lg Y500, gas only, h 0.7 | D_H | D_W |
|---|---|---|---|---|
| **Primary** | 14.388 | **-0.362** | **-0.216 (-4.4 sigma)** | **-0.012 (-0.2)** |
| No eq. 17 | 14.406 | -0.374 | -0.232 | -0.028 |
| Bin on count-rate rank | 14.419 | -0.333 | -0.194 | +0.009 |
| Without poor-fit (N 38) | 14.410 | -0.378 | -0.237 | -0.033 |
| Unmeasured as M = 0 (N 42) | 14.380 | -0.356 | -0.209 | -0.004 |
| Without the dz 0.139 cluster | 14.386 | -0.359 | -0.213 | -0.008 |
| Gas 12.75-13.2 (N 19) | 14.243 | -0.402 | -0.225 | -0.013 |
| Gas 13.2-13.58 (N 22) | 14.501 | -0.339 | -0.218 | -0.018 |
| Gas above 13.58 (N 15) | 14.826 | -0.168 | -0.119 | +0.067 |

Budget, dex: bootstrap on D 0.034-0.036, aperture 0.001 (delta is +0.003), half eq. 17 0.006, selection 0.031, shear + photo-z 0.015 (my judgement). Total on D_H 0.049, D_W 0.050.

**Why this isn't independent of everything.** The gas is the keys' gas, by design. No KiDS shear in the mass. But <M_WL> sits only +0.027 dex from eRASS1's catalogue M500, whose calibration includes HSC, so this agrees with the catalogue mass scale partly by shared lensing. HSC and KiDS share some equatorial sky; LSS overlap not sized. Eq. 17 is Okabe's mock, adopted.

## The other tables disagree
- **Umetsu x E16: W ANCHOR FAILS.** N 21, x 14.064, lg Y -0.211 ± 0.063; FR1's XXL line there -0.485 (+3.2 sigma), H -0.217 (+0.1), W -0.436 (+3.6). M500MT row -0.235 at 14.124. Umetsu's mean mass is 0.35 ± 0.07 dex below the mass from E16's r500MT on the same clusters, so **W's low anchor was largely that calibration.**
- **So two HSC readings differ:** Okabe x eRASS1 -0.40 at x 14.24, Umetsu x E16 -0.21 at x 14.06, W-like and H-like. Different clusters, different gas, same shear survey family. **XXL and eRASS1 share no clusters** (0 joined), so I can't test it per cluster. GS4's E16 gas offset is +0.094 ± 0.088 (7 clusters). Siegel+25's unexplained 40 % gap, noted in FR2, looks like the same thing. **This is the main thing not settled, and W FAVOURED should be read with it.** W as a line is still not vindicated: the primary matches W's number while W's anchor fails on better masses.
- **HIFLUGCS: NO STEP NEEDED as frozen, thin.** No gas column, so eRASS1 gas: N 27, b +0.134 ± 0.074. But the label moves with choices: NFWFreeze with pointed gas (N 42) b -0.018 ± 0.060, which would read STEP; other extrapolations b +0.006 to -0.17, some with lg M up to 16.28 (extrapolation failures). Y at 14.34 spans -0.04 to -0.23 by extrapolation alone, against H -0.156. Hydrostatic extrapolation is itself a 0.2 dex term. Not a clean support for H's slope.
- **eFEDS, report only:** N 164, x 14.30, lg Y -0.428, H -0.165, W -0.374. M from count rate, so partly built in, not a test.

## Part B: carry R500 to R200 from ACT y: UNDECIDED
601 clusters, lg Mg 13.1-13.6, z 0.05-0.30, Y500 S/N 18.5. Y200/Y500 1.52 ± 0.04 (Arnaud shape would be 1.325, read for scale). **lg carry +0.075 ± 0.015 boot ± 0.033 tau**, CIB-deprojected +0.076. Against +0.031: 1.2 sigma; +0.062: 0.4 sigma. Isothermal +0.033, no pedestal +0.064.
Assumptions: T(r) self-similar from X-COP via hydrostatic balance, tau 0.77 ± 0.14, not measured at this mass; stars ignored. **Two-halo not separated: biased high by an unmeasured amount.** The T(r) term and the two-halo term both exceed the gap, so this can't choose. eRASS1 catalogue R500 sets the scale.

## Grade through FR1's path, gas +0.005 (grader row, no route claim)
| Row | keys | G-OUT-M3, h 0.672, 0.686 | Z_tot | chi^2 | X-COP mean, rms | reach |
|---|---|---|---|---|---|---|
| H (FR1, reproduced) | 14 | +3.48, +3.09 | +2.77, +2.46 | 20 | +0.024, 0.072 PASS | 0.31-0.47 |
| **R anchored, LABEL ROW** (a -0.335, b +0.245 in lg M) | **4** | **-2.54, -2.70** | -2.03, -2.15 | 38-44 | **-0.112, 0.130 FAIL** | 2.9-3.6 |
| R own fit (a -0.287, b +0.193; SE b 0.115, over the 0.10 gate) | 11 | -1.21, -1.40 | -0.97, -1.12 | 18-21 | -0.099, 0.120 FAIL | 2.3-2.9 |
| R + 0.044 | 9 | -1.12, -1.33 | -0.89, -1.06 | 21-24 | -0.084, 0.107 FAIL | 2.3-2.8 |
| R - 0.044 | 4 | -4.06, -4.17 | -3.24, -3.32 | 65-74 | -0.139, 0.154 FAIL | 3.5-4.4 |
| R + y carry +0.075, reported | 8 | -1.18, -1.36 | -0.94, -1.09 | 26-30 | -0.070, 0.096 FAIL | 2.3-2.9 |

f* doesn't move G-OUT-M3. **Label: PARTLY [X-COP LOST] as frozen, and the word misleads:** reach over 1 means overshoot, more than the keys want, not part of the way. No row passes 15 of 15 and X-COP. Own-fit row clears M3 and fails on 4 other keys.

X-COP's masses are hydrostatic and the line is lensing-tied, so its failure restates the mass-method gap, not a new test. Label row's anchored slope sits 0.09 under the measured bin above lg Mg 13.58 where M3 now lands (model lg M500 14.61), which the own-fit row shows matters by about 1.3 in Z.

**Budget dependence, disclosed.** Frozen mock term gives sigma_tot 0.031. I added a mass-function selection term (alpha 1.8, my estimate, not named in the criteria) after the freeze; it gives 0.044, over FR1's 0.04 gate, which would read **NO INDEPENDENT MEASUREMENT**. The H/W label doesn't change either way. Tagged.

## G13 and EM1, report only
FR1 found H inside 0.07 dex of EM1 at lg M200 13.5-14.4. On line R with M3's carry, R minus EM1 is -0.17 to -0.29 at lg M_b 14 to 13. So on this mass scale that overlap goes away; on H it stays. It rests on the H/W question above. Not a grade.

## Checks
K1 FR1's H row through my driver, per key and X-COP, both f*: |d| 0, PASS. K2 78 rows, 72 with mass, 76 of 78 match (the two missing are misassociated), catalogue M500 vs R500 0.0001 dex, table row counts: PASS. K3 injected H, W recovered: bias -0.0035, -0.0036, sd 0.05, 0.03, PASS. K4 map geometry 7e-11 pix; injected y 1.004, 0.996: PASS. FR1's own internal checks reran PASS. MUTATE (a) bin on WL mass: D_H -0.216 to -0.125, label UNDECIDED, BITES, so the Eddington treatment matters. (b) slope flip: X-COP -0.407, 172 cells unsolved, BITES. Off-cluster y: S/N -0.4, BITES.

## Errors and departures, disclosed
- K2c's |dz| line was my script's: one cluster at 0.139 (Okabe 0.490, eRASS1 0.351) kept as frozen; dropping it moves lg Y 0.003. Reworded to allow one after it failed first.
- Mass-function term added after the freeze, above.
- Line R's bootstrap 500, not 2000 (fit cost).
- Okabe's Table E.1 parsed from PDF text; Umetsu units read from the paper by look-up (`FETCH_LOG.md`).
- Shear + photo-z 0.015 is my judgement. Umetsu's ±5 % as stated by them.

## Expectation on record
Between H and W near Akino 55 %: wrong, on W at the primary. W FAVOURED 20 %: got it. NO INDEPENDENT MEASUREMENT 65 %: not as frozen, by the added term yes. Part B UNDECIDED 75 %: yes. HIFLUGCS NOT MEASURED 50 %: no, thinly. Umetsu W ANCHOR FAILS 45 %: yes.

Natural next step, not done: a one-survey mass on a sample with both XXL-type and eRASS1 gas. eROSITA's half doesn't reach XXL-N; XMM of eRASS1 HSC clusters might. kappa = 1/2 FITTED. Not theory closed.
