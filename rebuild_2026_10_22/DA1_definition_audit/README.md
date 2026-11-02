# DA1_definition_audit: VERDICT MOVES, PARTLY AUDITED, on lines only. Four items read AMBIGUOUS with a grade depending on the reading. No item is plainly a chain error that flips a line. All four candidates still fail at least two lines on every single reading run here

Criteria: `FROZEN_CRITERIA.md` (e3cf19ce9e), `AMENDMENT_A1.md` (c735732a60), committed first. Order of reading: `ORDER_LOG.md`, with its departures. **Not blind.** kappa = 1/2 FITTED. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. FG1's sentence isn't rewritten; the moves below go to the owner. Reading windows other than the chain's are the sources' numbers, not a proposal to change a frozen line.

**What moves, by the frozen rule.** Each is one reading, one at a time:

| Line | Chain | Other reading | Why |
|---|---|---|---|
| C2 K | FAIL 14 of 15, G-IN-Mall -2.05 | PASS 15 of 15, -1.70 | D2: KiDS's bin n(z) in Sigma_crit. Also B = 1. With both, FAIL again, G-OUT-M3 +2.11 |
| K's [GAS-CONDITIONAL] tag | fires, +0.111 gives 15 of 15 | doesn't, at f* 0.034: same aperture +0.092 gives 14 of 15, +2.10; or n(z) at +0.111 gives 13 of 15, +2.58 | D1, D2. K's grade on +0.005 doesn't move |
| C1 S | PASS 0.75/0.76 | FAIL on any window from 0.5 +- 25 % | D4 |
| C3, C4 alt S | FAIL 0.44 | PASS on the same windows | D4. Alt, never pooled |
| C1 (A), C3 MW | WIDE PRIORS ONLY | IN PRIORS | D5: R_d prior read as mass scale or as the review's range. C1 on B stays out |
| C3, C4 S | PASS 0.52 | FAIL 0.47, 0.48 | D6: SPARC's flow distances at native h |
| C2 Tl | FAIL +0.17/+0.18 | PASS +0.12 | D6, same rerun |

**What doesn't move.** GS4's +0.005 stands within convention: at most +0.023, K 12 of 15, G-OUT-M3 +3.97. RM2's contradiction with the measured response stands. Lines left failing whatever the reading among these: C1 LT, Tl, K, Ln, Dw, DM, IC; C2 LT, X, Ln, MW; C3 K, IC; C4 K, Dw, MW, IC. **Readings weren't run in combination, except n(z) with B = 1**, so "at least two" is by inspection of this list. The audit runs both ways: several readings hurt the rule (C1 and C3's K worsens to +5.19, C3 and C4's S fails).

## Known answers, run before any label
| Check | Result |
|---|---|
| K1, UR3's c row | **DEFINITION WRONG.** Raw zooms, own shell fit: c on r_vir 13.76, on R200 7.25, ratio 1.90; UR3 applies 12.95 with R200. Mass fraction at R0 1.64 x raw. `da1_k1.out` |
| K2, pre-fix template | **DEFINITION WRONG.** `b62559a575~1` reads (A_CAL, s_CAL, run's pred). Own A vs A_CAL: 5.6e-16 on X7's template, 0.235 on the run's. `da1_k2.out` |
| MUTATE, h flipped in D1 | **DEFINITION WRONG.** Identity off by 0.171, exit path separate. `da1_d1_gs4_MUTATE_h.out` |
| Harness | CRG1's code, scratch copy, against ZN4's JSON: max dZ 0.0001. SPARC at k = 1: 0.75/0.76, 0.35/0.36, 0.52, 0.44 as FG1 |

## Items
| Item | Label | Source | Chain | Difference | Effect on graded lines |
|---|---|---|---|---|---|
| **D1 Gas scale** | **AMBIGUOUS. K's grade doesn't depend; the tag does** | eRASS1 (2402.08452, FITS sha256 e79c392e...): gas within R500, metallicity 0.3, mu_e 1.18; R500 from its cosmology run. X-COP (1805.00034): Omega_m 0.3, H0 70, azimuthal median, rho = 0.61 m_p (n_e + n_p) | GS4: same radius by slope 1.19, h 0.70 by D_A^2.5. X-COP +0.111 at each survey's own R500 | h: none, catalogue M500, R500, z imply H0 69.999, Om 0.3000. GS4 rebuilt, +0.005 +- 0.016, N 43 without X-COP. **+0.111 mixes apertures;** at eRASS1's R500, the radius the keys scale at, +0.092. **Abundance:** eRASS1 1.18, X-COP 1.131, 0.018 dex, not in the chain. **Clumping:** X-COP median, others not; not sized | +0.005 to +0.023: 12 of 15, +3.97. Slope 1.58: +0.032, 12 of 15, +3.74. +0.092: 14 of 15, +2.10 at f* 0.034; 15 of 15, +1.76 at 0.0615. +0.092 + 0.018 = about +0.111: 15 of 15 |
| **D2 G-OUT-M3** | **AMBIGUOUS, GRADE DEPENDS: C2's K** | KiDS practice (2402.08456, 2106.11677): Sigma_crit from calibrated bin n(z), per-bin m, contamination from number profiles with obscuration; KiDS fit range 0.5-2.5 Mpc. Standard Delta Sigma, reduced shear | X7: point Z_B in Sigma_crit, Z_B > z_l + 0.2, m -0.01, B = den/den_r below 1 multiplied in. Bins to 3 Mpc. Pred: gas, stars, zoom cold mass to r_ta, no term beyond | **Criteria's wording is reversed:** observed is 1.56, predicted 1.04 (ZN4's JSON). Estimator, physical radii, projection: match. **n(z):** data up 2-25 % by z. **B below 1** isn't a dilution correction. **m:** 2106.11677 prints 0.014, sign not shown | C1, C3 K: +5.19, or +4.83 at B = 1; +5.58 both. C2 K: table above. C4 K: stays failing. Tag at +0.111: 13 of 15 with n(z), 14 with B = 1. m: M3 +4.19 or +4.44, no K flip |
| **D3 Contraction** | **WRONG, NO FLIP** | Primary papers not opened; LC1's frozen form | LC1 f_Q: live vs Blumenthal on the zoom's own cuspy start, r/R_d 2-4. RM2's f: M_0 + f(M_c - M_0) on the smooth core | **Not the same quantity.** On RM2's own start: mass form 0.82 [0.45, 0.98], PZ1 0.85 [0.62, 1.06]; ratio form 0.62 [0.32, 0.83], PZ1 0.62 [0.47, 0.84] (A; B within 0.03). No live run has a cored start | RM2 needs f_hi 0-0.2: still above. RM1 at f 0.8: Upsilon 0.41, tilt +0.23; f 0.6: 0.47, +0.28. Both fail S, Tl as chain |
| **D4 Upsilon line** | **AMBIGUOUS, GRADE DEPENDS: C1 S, C3 and C4 alt S** | [3.6]. 1606.09251: about 0.5 from population models, max-disc about 0.7 in bright galaxies; 1610.08981: 25 % scatter, single value for discs; 1407.1839: 0.47 | CFG4 H2's 0.50-0.80, median per-galaxy Upsilon_disk, bulge x 1.4, all V_flat | Convention matches. **The source's centre is the window's lower edge.** No source read gives 0.80. Sources say weak variation, not none; UL1's bins not re-graded | `da1_d4_d5.out`. 0.375-0.625: C1 FAIL; C3, C4 pass; alts pass; C2 FAIL. 0.25-0.75: C2 PASS, C1 FAIL (0.75/0.76) |
| **D5 Milky Way** | **K_z: WRONG, NO FLIP. Priors: AMBIGUOUS, GRADE DEPENDS: C1 (A), C3 MW** | 1309.0809: total force at 1.1 kpc, eq. 28, 67 exp(-(R-R0)/2.7), fixed R0 - R; mass scale 2.15 +- 0.14. 1602.07702: 2.6 +- 0.5, notes dynamical support for short | 66.4 +- 2.2, h 2.72, line +- 4.4; total at 1.1 kpc, R0 - R held: match. R_d tag 2.38-2.90 (LN16, photometric, 1607.05281) | Refit of the 43 rows: 67.55 +- 2.04, or 67.36 +- 2.26 with 5 %. 66.4 sits about 1 low. **Tag is a light scale; K_z's own paper gives a mass scale** | C1 A's cell R_d 1.93: in priors on all three other readings, M* 7.56e10 in tag. C3's 3 cells: R_d 1.93. C1 B's 70.89 misses 66.4 + 4.4 by 0.09, inside 67.4's line: a wide cell, no flip alone. C2: V+K only, no change. C4: K_z 76.7-80.9, no change. Bovy's R_d itself assumes a disc + halo model |
| **D6 Inherited** | **ASSUMPTION INHERITED, AMBIGUOUS, GRADE DEPENDS: C3, C4 S; C2 Tl. Rows CANNOT CHECK below** | Rows below | | | |

## D6 rows
| Input | Where | Rerun | Effect | Label |
|---|---|---|---|---|
| eRASS1 distances (70, 0.3) | Mgas, R500 | proven from raw, undone by q | none | ASSUMPTION CLEAN |
| **eRASS1 R500, M500** | ΛCDM cosmology run with count-rate scaling; sets aperture, tail start | no raw alternative. Bracket: R500 -0.05, -0.075, -0.10 dex, same gas | G-OUT-M3 +4.66, +4.81, +4.97; 11, 11, 10 of 15. Worse | ASSUMPTION INHERITED, NO FLIP; bracketed |
| **SPARC flow distances, H0 73** (97 of 175) | S, Tl | D x 1.0647 at native h | C1 0.68/0.70, Tl +0.49/+0.53. C2 0.32, Tl +0.12. C3 0.47, alt 0.41. C4 0.48, alt 0.41 | **ASSUMPTION INHERITED, AMBIGUOUS.** 73 is ladder, not ΛCDM; rescaling breaks its match to the TRGB and Cepheid groups. EM1's a, b not refit. `da1_sparc_h0n.out`, check `da1_sparc_k1check.out` |
| X-COP (70, 0.3) | X | all scaled to native D_A, q 1.049 | C1 -0.020, 0.077, PASS (was +0.013, 0.075). C2 -0.129, 0.169, FAIL | ASSUMPTION INHERITED, NO FLIP |
| Ln two-halo, Planck-type conversion | Ln | conversion only, native h, Om | C1 D 432.7 to 431.4, class LAW. C4 ENV-H -461.9 to -460.6 | ASSUMPTION INHERITED, NO FLIP. P_grav itself: CANNOT CHECK |
| Lensing distances, DESI x 101.54/h | K | two h cells carried | M3 +4.41/+4.07 | bracketed, NO FLIP |
| CLASS backgrounds | S_N, zoom ICs | A, B | 0.75/0.76 | Framework-native by record; cold component w about 0, CMB refit. CANNOT CHECK beyond A/B |
| f* 0.034, 0.0615 | K, X | both carried | +4.41, +4.13 | Source census not traced: CANNOT CHECK |
| Ln's h_N 0.679, Om_N 0.3085 vs cluster native | Ln | not run | | CANNOT CHECK, small against D 432 |
| M* tag LN15, McKee column, Eilers, Ou, DiskMass, IC 1613, Dw table, BCG masses, EM1's fit | MW, DM, IC, Dw, K | not traced | | **CANNOT CHECK here** |
| PAPER67's a0(z) band, cold mass from the CMB | not a FG1 line | not rerun | none on FG1 | Not graded here |

## Not verified
- Bin n(z) on Z_B-selected sources is a **bound**. Exact KiDS-form selection needs re-measuring the shear from the 17 GB catalogue, not done. F comes from a one-in-20 cache in another session's scratch (zb.npy sha256 821a4ed6b7a9bb43...), bracketed by whole-bins-only.
- LN16's 2.64 isn't checked in full text: search listing for the paper, value from the chain. Meidt+14 not read. X-COP's and others' clumping isn't sized. m's sign in 2106.11677 unresolved; van den Busch+22's table not read.
- Blumenthal, Gnedin not opened. DESI, KiDS m tables not read. Dw, IC, DM, LT, G definitions outside D1-D6 weren't audited.
- 2402.08452's text as read states no H0; the fiducial comes from the raw columns.

## Run
    python3 -I da1_k1.py; python3 -I da1_d1_xcop.py; python3 -I da1_d1_gs4.py PRIMARY; python3 -I da1_d1_gs4.py MUTATE_h; python3 -I da1_d3.py; python3 -I da1_d4_d5.py
    # with DA1_CRG = a scratch copy of CRG1's v1/*.py, inputs linked, after crg1_zoom, crg1_efe, crg1_clusters; DA1_KIDS = zb, w cache
    python3 -I da1_keys.py; python3 -I da1_k2.py; python3 -I da1_sparc_h0.py; python3 -I da1_ln.py

One thread, nice 15, peak about 200 MB on keys; KiDS and snapshots read by map. Stray items from a first failed launch: two empty dirs and a bytecode dir in CRG1's v1, removed at once, nothing tracked touched. One attempted PDF open raised a save dialog; nothing was saved by me.

kappa = 1/2 FITTED. Not theory closed.
