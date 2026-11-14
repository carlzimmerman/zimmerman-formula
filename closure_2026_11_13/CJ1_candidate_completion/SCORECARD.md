# CJ1 SCORECARD: every tested row against the completed form

2026-11-13. The completed form is form B (PAPER72 v1.2, rules 1 to 5) with rule 6 filled by the crossing-speed joint
(`COMPLETED_FORM.md`). It is NOT ADOPTED, and a completed statement is not a confirmed one. This file grades nothing
new: each row quotes its lanes' committed words, frozen word first and post hoc words marked, and then says what that
row says about the completed form. No lane label or number changes here and no lane is relabelled. Footings are
canonical / alt, never pooled; a single word means both footings. Cold dark energy is a gravitating field component, not
a particle. Nothing here says the data favour the framework. Every quoted word is checked verbatim against its
committed file by `cj1_audit.py` (output `cj1_audit.out`, which also lists each file's path).

Updated 2026-11-13 by the lead after RRL1 and FRZ5 landed: rows 21, 22, 27 and 28, the counts and the three lists. No other row changes. Row 28's word for the completed form is the lead's placement. CJ1's first commit is e3b5114d3f (origin 76634be68d);
its audit then read 108 of 108, and read 110 of 110 after that update.

Updated again 2026-11-13 by the lead after the blind DSC1R landed: rows 7 and 8, the counts and the three lists. Both
new words for the completed form are the lead's placements, made the same way in both directions: a hit the blind
build does not confirm becomes NO POWER, and a fail the blind build does not confirm becomes DEPENDS ON AN UNTESTED
ASSUMPTION. The audit read 112 of 112.

Updated a third time 2026-11-13 by the lead after EUC16 landed: row 39 and one line of the last list. The word for the
completed form does not change. The audit read 113 of 113.

Updated a fourth time 2026-11-13 by the lead after FRZ6 landed: row 22, the counts and the lists. Row 22's word for the
completed form is the lead's placement of FRZ6's frozen label, which is a hit awaiting a blind re-grade. The audit read
115 of 115.

Updated a fifth time 2026-11-13 by the lead after the blind FRZ6R landed: row 22 and the lists. FRZ6R reads NO VERDICT as
frozen and so does not confirm FRZ6's label; its numbers are under the gate and its control fails. Row 22's word is kept
by the rule already used in row 11 (a blind NO VERDICT that does not contradict the first lane leaves the word and marks
it unconfirmed). The audit reads 116 of 116.

Words for the completed form (fixed list): PASSES / FAILS / FAILS ON COVERAGE ONLY / PASSES TRIVIALLY (the form equals
the reference there) / EQUALS THE LAW (unchanged by rule 6: the form gives the law's own layout there, so the row's
verdict on the law carries over) / NO POWER / DEPENDS ON AN UNTESTED ASSUMPTION / NOT GRADED FOR THIS FORM.
"Blind re-grade" means a lane built blind to the row's first lane; "yes" says nothing about whether it confirmed.

| # | row | lanes | word as frozen (post hoc) | power | completed form | blind re-grade | note |
|---|---|---|---|---|---|---|---|
| **Rotation curves** | | | | | | | |
| 1 | SPARC rotation curves | PD1, JNT2, JNT2R | PD1 "PASS: rms 0.0563 (line 0.0660)"; JNT2 G3 "EQUAL TO THE LAW (0 above)" | yes | EQUALS THE LAW | yes (JNT2R: "175 / 175 by (a), L") | 0 of 175 above v* (largest Vflat 332 km/s). A pass of the law, not of rule 6. |
| 2 | Solar System | PD1 (PAPER72 table) | "Solar System & pass, carried & PD1" | yes | EQUALS THE LAW | no | Carried, not recomputed. |
| 3 | What is not baryons, by shape | SHP1 | "THE LAW'S SHAPE ON ROTATION CURVES" | fragile | EQUALS THE LAW | no | Fails at disc mass-to-light 0.3 or 0.8. |
| 4 | Massive SPARC spirals (above v_stiff, below v*) | JNT1, JNT1R | JNT1 "NO VERDICT / JOINT COMPLETE ON POWERED ROWS [1.25, 2]" (for the v_stiff split); JNT1R "REFERENCE FAILS AT THE RECORD SHARE [L2 shape; L3 scatter], FRAGILE", beside it "THE LAW FITS, FRAGILE"; alt "THE LAW FAILS [L2 shape], FRAGILE" on 2 galaxies | fragile / no | EQUALS THE LAW | yes (JNT1R; its own file says its agreement with JNT1's reading is not fully blind) | All 9 / 2 are below v*, so the candidate gives them the law, which fits on canonical (fragile); alt has 2 galaxies, no power. SRJ2's split gave them the reference, which fails. |
| **High-redshift discs** | | | | | | | |
| 5 | RC100 coverage at 2.2 R_e | JNT2, JNT2R (line from SRH1) | "JOINT FAILS ON G2 (coverage)" in both builds | coverage line; data no power | FAILS ON COVERAGE ONLY | yes (JNT2R, same word, FRAGILE) | 10 / 2 discs at z 2.10 to 2.52 above v*(z), covered 90 / 98 of 100 at every f. 2 v* restores coverage and breaks the forest. |
| 6 | RC100 discs under the reference layout | SRJ3, SRJ4 | "NO VERDICT (no power) / NO VERDICT (no power)" (both lanes) | no | NO POWER | no | One point per disc cannot tell the reference, half of it or the law apart. The 10 / 2 are inside SRJ2's 31 / 22. |
| 7 | Resolved z about 2 discs above v* | DSC1, DSC1R | DSC1 "JOINT'S STATEMENT HOLDS ON THE RESOLVED DISCS, FRAGILE" (canonical); alt "NO POWER (fewer than three discs above)"; DSC1R "NO POWER, FRAGILE" (both footings, as frozen and under its post hoc A1) | no (DSC1R) | NO POWER | yes (DSC1R; did not confirm) | 3 / 2 discs. At the record's halo: DSC1 A 0.670 [0.250, 1.175], DSC1R 0.590 [-0.13, 1.58] (canonical). The whole difference is how many digitised points count as independent (DSC1 all of them; DSC1R one per 0.6 arcsec beam); at the paper's two per beam A = 0 sits just outside (0.610 [0.040, 1.335]). DSC1R's word flips in 8 / 6 of 12 brackets, both ways. |
| 8 | Resolved discs below v* | DSC1, DSC1R | DSC1 "LAW FAILS BELOW, FRAGILE" (both); DSC1R "LAW HOLDS BELOW, FRAGILE" (both, as frozen and under A1) | fragile | DEPENDS ON AN UNTESTED ASSUMPTION | yes (DSC1R; opposite word) | 4 / 5 discs at z 0.85 to 1.6 (alt adds zC 406690). In both builds a free reference halo at A about 1.25 to 1.57 fits better than the law (DSC1R canonical chi2 207.8 vs 252.9) and the law beats baryons alone by far; the two words differ only by the decision line. Every layout is rejected in absolute terms. Turns on baryon mass and the count of independent points. |
| 9 | ALPAKA ring curves | ALP1, ALP1R | ALP1 "NO POWER / NO POWER"; ALP1R "NO VERDICT (TW-N and TW-D do not bite)", reading NO POWER | no | NO POWER | yes (ALP1R, same reading) | Baryons alone overshoot the discs above v*; 2 to 5 rings; gas-mass conversion, sizes and beam block it. |
| 10 | ALMA limit on one disc | U4L1 | "NO LABEL" (A1: NO TENSION) | no | NO POWER | no | One disc excludes no model. |
| **Lensing** | | | | | | | |
| 11 | KiDS early-type lenses at 1.6 R_h (G4) | SRH1, SRH1R, JNT2, JNT2R | SRH1 "WINDOW EMPTY" (its history); SRH1R "NO VERDICT"; JNT2 "cannot see f (SRH1R)" | fragile | PASSES | yes (SRH1R: NO VERDICT; did not confirm) | 0 lenses above v*. Fails at f 0.75 and 1 (+2.003 / +2.037 at f 1), passes from 1.25; sets the lower edge of f. SRH1R's build passes at f 0.05 and 0. |
| 12 | KiDS by type, neighbours modelled | KO2 | "NO VERDICT for late types and NO VERDICT for early types" | no | NOT GRADED FOR THIS FORM | no | Graded against form B's truncated halo, not a halo ending at f R_fold. |
| 13 | KiDS host-free lenses | ONE1 | "KiDS host-free: PASSES / PASSES" | fragile | NOT GRADED FOR THIS FORM | no | At PD1's share; does not separate form B from the law. |
| **Clusters and groups** | | | | | | | |
| 14 | X-COP amount, one-sided ceiling | RB1, XCV1, JNT2, JNT2R | RB1 "NOT FALSIFIED (ONE-SIDED)"; XCV1 "NO VERDICT" (post hoc AT THE CEILING); JNT2 "TRIVIAL (all 7 above)" | yes, one-sided | PASSES TRIVIALLY | yes (JNT2R, TRIVIAL) | All 7 above v*; the R500 bracket fails (1.057) for the reference and the joint alike. |
| 15 | X-COP amount, two-sided | PD1, RB1 | PD1 "FAIL +0.16"; RB1 "the two-sided amount gate stays FAIL as PD1 graded it" | yes | FAILS | no | Rule 6 does not touch it: X-COP keeps form B's reference layout. |
| 16 | X-COP radial shape | RB1, SRJ1, JNT2, JNT2R | RB1 "NO VERDICT under the frozen KA-2" (post hoc A1: CONSISTENT); SRJ1 "JOINT FAILS ON CLUSTERS, FRAGILE (R500 aperture)" (unsplit, f 1) | yes | PASSES TRIVIALLY | yes (JNT2R, TRIVIAL) | Passes only as the reference does, under RB1's post hoc A1. With 2 v*, 6 / 7 clusters take the law and the shape fails. |
| 17 | Groups, f_ret at R500 | RB1, JNT2, JNT2R | JNT2 "law in 19 / 20"; JNT2R "groups q at R500 (NO POWER)" | no | NO POWER | yes (JNT2R) | q 0.651 / 0.654; passes under the reference, the law and every f. |
| 18 | Groups to turnaround | GO1, GO2 | GO2 "NOT EVALUABLE [r_ta NOT REACHED]"; GO1 NOT EVALUABLE | no | NO POWER | no | The stack does not reach turnaround. |
| 19 | The Bullet | RB1 | "CONSISTENT [STRIPPING-DEPENDENT]" | fragile | DEPENDS ON AN UNTESTED ASSUMPTION | no | Passes only if the subcluster's stripped gas is counted; nothing measures it. |
| 20 | Outer cluster shear | ZN4, FR1 (PAPER72 table) | PAPER72 "FAIL, about 3$\sigma$ with systematics"; ZN4 "X-COP ONLY" on measured gas; FR1 "NOT RETENTION" | yes | FAILS | no | Carried from PAPER72's table; rule 6 leaves clusters on the reference these lanes graded. On X-COP's own gas scale ZN4's class passes. |
| **The forest** | | | | | | | |
| 21 | Forest at matter level | FRZ1, FRZ1R, FZS1, JNT2, JNT2R | FRZ1 "FOREST ROW FAILS" (full layout); FZS1 "FOREST ROW FAILS, FRAGILE" (unsplit settled); JNT2 "TRIVIAL to f 2" | yes | PASSES TRIVIALLY | yes (JNT2R, trivial to f 2) | The split hands a third to two thirds of the haloes to the reference. At f 3: JNT2 1.99 / 6.43, JNT2R "17.6 / 29.2 FAIL". FRZ5 (post hoc A1): with the gas template refit the full layout's matter-level number falls from 9916 / 9009 to 118 / 107, and only with the smoothing at its floor. |
| 22 | Forest at flux level | FRZ3, FRZ3R, FRZ4, FRZ5, FRZ6, FRZ6R, SRF1, SRF1R | FRZ4 "FOREST ROW FAILS AT FLUX LEVEL" (full layout, f = inf) and "NO VERDICT (known answer e fails)" (unsplit f 1, 2, 3); SRF1 "NO VERDICT / NO VERDICT (canonical / alt)"; SRF1R "As frozen: NO VERDICT / NO VERDICT"; FRZ5 "NO VERDICT (a twin does not bite)" (post hoc A1: "FOREST ROW FAILS AFTER REFIT", full layout); FRZ6 "FOREST ROW HOLDS AT FLUX LEVEL" (split, f 2, canonical) and "FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lambda_P x 0.5)" (split, f 2 alt and f 3 on both); the blind FRZ6R "As frozen: NO VERDICT for every case on both footings." | fragile | PASSES | yes for the unsplit family (SRF1R; NO VERDICT) and for the split (FRZ6R; NO VERDICT as frozen; did not confirm the label) | The full law layout is dead at flux level. FRZ6 ran the v* split at flux level with 12 seeds at z 2.2: 0.196 / 0.257 at f 2 and 1.144 / 1.434 at f 3 against the gate 4 (0.50 / 0.65 and 2.04 / 2.50 with twice the seed error added); f 1.25 is below what the build resolves (NO VERDICT); halving the gas smoothing scale crosses the gate in three of the four holds; its control fails again only under its post hoc A1. A hit; a hold here means not excluded. The blind FRZ6R (own estimator, 4 seeds per bin) reads 0.024 / 0.029 at f 2 and 0.572 / 0.691 at f 3, every split case under the gate with twice its error, and its control FAILS (323.0 / 395.8); its label is NO VERDICT because the twin that removes the boundary does not bite, so the hold is not confirmed as a label and is not contradicted. Unsplit f 1 / 2 read 0.10 / 0.11 and 0.50 / 0.41, ungraded. FRZ5: the record's gate fits no gas parameter; with an amplitude, a tilt and a smoothing per redshift bin refit, the full layout falls from 269 / 288 to 23.0 / 23.9 (gate 4) and unsplit f 3 from 2.20 / 2.04 to 0.78 / 0.76, ungraded. |
| **Cosmology and amplitude** | | | | | | | |
| 23 | CMB peaks, CMB lensing, growth | CO1, CO2 | CO1 "ROWS HOLD / ROWS HOLD" (amended; as frozen "NO VERDICT / NO VERDICT"); CO2 pinned CMB lensing -0.30 sigma | yes, not independent | PASSES TRIVIALLY | no | Linear content is the cold reference; the share is fitted to the CMB. |
| 24 | Matter-power redistribution | CO1, HLF1 | HLF1 "NO VERDICT / NO VERDICT (canonical / alt)" (post hoc A1: ROWS HOLD WITH THE OWN LIST) | no | NOT GRADED FOR THIS FORM | no | Not computed with the v* split. |
| 25 | Weak-lensing amplitude | CO2, KL1, BX1, LWB1, LWB1R | CO2 "AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA"; KL1 "As frozen: NO VERDICT / NO VERDICT."; BX1 "NO VERDICT (canonical) / NO VERDICT (alt)" (post hoc AMPLITUDE CONSISTENT); LWB1R "AMPLITUDE CONSISTENT, FRAGILE" | yes | NOT GRADED FOR THIS FORM | yes (LWB1R) | JNT2 does not address it; the tension is the one any cold component fitted to the CMB carries. |
| 26 | Flat a0 at z 2.33 | AZ2, AZ2R | AZ2 "As frozen: NO VERDICT / NO VERDICT" (A2: FLAT HOLDS); AZ2R "FLAT HOLDS / EXPANSION-MODEL DEPENDENT" | no | EQUALS THE LAW | yes (AZ2R) | The candidate holds a0 constant; does not separate from LCDM. |
| **The Milky Way** (log M_b about 10.7: R_fold 169 kpc today, so R_set at least 211 kpc; every row below is inside it) | | | | | | | |
| 27 | Halo stars directly, 20 to 80 kpc | RAW1, HOT1, LMC1, MWT1, MWT2 | RAW1 "FAILS HOT, FRAGILE"; MWT1 "FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST"; MWT2 "NO POWER"; HOT1 "CLUMPED"; LMC1 "NO LABEL" | fragile | DEPENDS ON AN UNTESTED ASSUMPTION | no | The tracer slope beyond the sample's reach (row 28 measures it). MWT2, ungraded: 30 to 40 kpc holds a cold lump; the smooth part passes when it is set aside. |
| 28 | Halo stars with the slope measured from RR Lyrae | RRL1 | "MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]" (all four framework cases; robust only on the rotation-curve stellar mass, alt) | fragile | FAILS | no | Pan-STARRS1 RR Lyrae: slope 5.29 inside 39.0 kpc, 3.93 beyond. With it the hot 30 to 40 kpc bin passes in every case (census 1.205 -> 1.052 / 1.155 -> 1.008) and 40 to 55 kpc turns cold (0.857 / 0.820) for every smooth model, DESI's NFW included. The outer slope moves from 3.35 to 4.20 with the cuts and the shape reverses without the Sagittarius mask; a single slope (4.77) removes the fail on alt. |
| 29 | DESI shape-measuring curves | NMB1, NIM2, RG1 | NMB1 "PASSES"; NIM2 canonical census "FAILS LOW" | fragile | EQUALS THE LAW | yes (RG1 "REPRODUCED" for NMB1; shares inputs) | NIM2 awaits a re-grade. |
| 30 | Outer masses, 100 kpc and beyond | PLT1, SAT1, EFC1, RG1 | PLT1 "PASSES, FRAGILE" (field) / PASSES (no field); SAT1 "ANISOTROPY LOWERS IT, NOT ENOUGH"; EFC1 "CONVENTION-DEPENDENT" | fragile | EQUALS THE LAW | yes (RG1) | Under the owner's actual-field reading the no-field rows are the framework's, and they pass. |
| 31 | DESI DR2 enclosed-mass profile | DW1 | "9 of 12" | yes | EQUALS THE LAW | no | The extrapolated M200c fails. |
| 32 | Inner stellar mass the curve needs | MWI1, RCF1, STM1 | MWI1 "SUPPLIED BY 1 OF 5" | yes | EQUALS THE LAW | yes (RG1) | The need is above every published central value. |
| 33 | Hot halo gas | MWG1, HG2 | "ROTATION CURVE NOT SUPPLIED" | fragile | EQUALS THE LAW | yes (RG1, MWG1) | Hot gas does not supply the curve. |
| 34 | LMC reflex | RFX1 | "REFLEX WITHIN THE BOUND, FRAGILE" | fragile | EQUALS THE LAW | no | A one-sided bound. |
| **Dwarfs and wide binaries** | | | | | | | |
| 35 | MW ultra-faints, M31 bright dwarfs | RB2, DG1, DSB1, CRACK-1 | RB2 "B FAILS HIGH / B FAILS HIGH"; DG1 "DOES NOT SURVIVE" (data-side regrade); DSB1 amended "lane NO POWER"; CRACK-1 "FAILS THE PAIR" | fragile | FAILS | yes (DSB1, blind; amended NO POWER) | Rule 6 does not touch them (far below v*, inside their fold): form B's fail stays. Medians stay high. |
| 36 | DF2, DF4, NGC 147, IC 1613 | RB2, NH2 | RB2 "B FAILS ON THE HOSTED ROWS"; NH2 "Label as frozen: NO VERDICT / NO VERDICT" (post hoc DF4 "TIDES CANNOT REACH") | yes | FAILS | no | Rule 6 does not touch them: form B's fail stays. |
| 37 | Coma UDGs, MW classical dwarfs | RB2, DSB1 | "B CONSISTENT / B CONSISTENT" | no (DSB1) | PASSES | yes (DSB1: NO POWER) | Inside the interval only with the systematics budget; rule 6 does not touch them. |
| 38 | Wide binaries (Gaia DR4, due 2026-12-02) | CW1, DR4MAP | DR4MAP "Governing for the adopted theory (wide binaries only)" | no (data not out) | EQUALS THE LAW | no | Can kill the adopted theory, cannot confirm it. |
| **Strong lenses** | | | | | | | |
| 39 | Euclid lenses at the law's ceiling | EUC1, EUC12, EUC13, EUC13R, EUC2, EUC3, EUC9, EUC10, EUC11, EUC14, EUC15, EUC16 | EUC1 "NO VERDICT / NO VERDICT (canonical / alt)"; EUC13R "NO VERDICT"; EUC15 "EARLY READING, NOT A GATE"; EUC16 "EUC1-F graded for the first time", NO VERDICT on both footings | no | EQUALS THE LAW | yes (EUC13R, same word) | 26 / 0 of 6,173 lenses above v* (LNJ1). EUC16 certified 11 source redshifts (5 on a single line) and graded the gate: median boost +0.405 [+0.137, +0.589] / +0.385 [+0.121, +0.574] against the hold line 0.15 and the fail line 0.25, so NO VERDICT with the centre on the failing side. The certified lenses read about 0.13 heavier than the whole sample before any source redshift. |
| 40 | Wide lenses break the ceiling | EUC4, EUC4R, EUC6, EUC6R, EUC8, LNJ1 | EUC4 "WIDE LENSES BREAK THE CEILING"; EUC6 "WIDE LENSES SIT IN RICHER ENVIRONMENTS"; LNJ1 "NO POWER, FRAGILE / NO POWER" | yes (data) / no (joint) | DEPENDS ON AN UNTESTED ASSUMPTION | yes (EUC4R, EUC6R, data words; none of LNJ1) | 1 / 0 of 316 wide lenses above v*; the break is not the switch. The form needs group mass along the sightline that no lane has counted. |
| 41 | Wide-lens extra mass as hot gas | ESZ1, EXR1, EXR1R, EXR2 | ESZ1 "ONLY A CUSP IS LEFT"; EXR1 "Frozen word: NOT EVALUABLE / NOT EVALUABLE" (post hoc EXCLUDED) | no | EQUALS THE LAW | yes (EXR1R, same frozen word) | A question about the law on the stars. |
| **The constants** | | | | | | | |
| 42 | kappa = 1/2 | KAP1, OUT4 | KAP1 "KAPPA NOT DERIVED"; OUT4 "KAPPA NOT DERIVED (FITTED)" | - | NOT GRADED FOR THIS FORM | no | FITTED; v* is linear in it through a0. |
| 43 | The share 5.41 | R541A to R541E, CO2 | R541A "EXCLUDED / EXCLUDED"; R541B "TRADES / TRADES" | - | NOT GRADED FOR THIS FORM | no | FITTED; v* goes as 1 / (1 + X). |
| 44 | f | JNT2, JNT2R | JNT2 "[1.25, 3] canonical and [1.25, 2] alt"; lead's note "window without the coverage line is [1.25, 2] in both builds on both footings" | - | NOT GRADED FOR THIS FORM | yes (JNT2R) | Reported, not graded. Lower edge from row 11; upper edge from the forest at f 3, not agreed on canonical. |
| 45 | R_fold | FLD1 | "DOES NOT / DOES NOT" | - | NOT GRADED FOR THIS FORM | no | A construction: radial shells, point mass, cold start at z 10. Today's fold falls 1.3 to 5.4 times short of the KiDS windows. |

## Counts

Canonical: EQUALS THE LAW 14; NOT GRADED FOR THIS FORM 8; NO POWER 6; FAILS 5; PASSES TRIVIALLY 4; DEPENDS ON AN UNTESTED ASSUMPTION 4; PASSES 3; FAILS ON COVERAGE ONLY 1. Total 45.

Alt: EQUALS THE LAW 14; NOT GRADED FOR THIS FORM 8; NO POWER 6; FAILS 5; PASSES TRIVIALLY 4; DEPENDS ON AN UNTESTED ASSUMPTION 4; PASSES 3; FAILS ON COVERAGE ONLY 1. Total 45.

No row differs between the footings after the DSC1R update (row 7 read PASSES canonical / NO POWER alt before it).

## What the form survives with power

- Equal to the law, so these are the law's passes and not evidence for rule 6: SPARC rotation curves (1) and the Solar
  System (2).
- Equal to the reference, so trivial: X-COP's one-sided amount (14), X-COP's radial shape under RB1's post hoc A1 (16),
  the forest at matter level up to f 2 (21), and the CMB, CMB-lensing and growth rows, which are not independent of the
  fitted share (23).
- With fragile power only, and none confirmed by an independent blind re-grade: KiDS early-type lensing at f 1.25 and above (11, a gate SRH1R found cannot see f), the
  9 massive SPARC spirals on the law (4, canonical, JNT1R's reading), NMB1 and PLT1 (29, 30).
- No longer listed: DSC1's hit on three resolved z about 2 discs above v* (7). The blind DSC1R reads NO POWER there.
- New, with fragile power and not confirmed: the forest at flux level for the split at f 2 and f 3 (22, FRZ6). The blind
  FRZ6R reads NO VERDICT as frozen while its numbers sit under the gate.

## What the form fails

- On coverage only, as frozen in both builds: RC100 at z 2.1 to 2.5 (5). The data on those discs have no power (6).
- No longer listed: the law below v* on DSC1's resolved discs (8). The blind DSC1R reads the opposite word; see below.
- On data, fragile, and shared by every smooth model including DESI's NFW: Milky Way halo stars at 40 to 55 kpc once
  the star-count slope is the measured RR Lyrae one (28). The hot 30 to 40 kpc bin of row 27 passes with that slope.
- Untouched by rule 6, so form B's fails stay: X-COP's two-sided amount (15), the outer cluster shear (20, carried), the
  ultra-faints and M31's bright dwarfs (35, fragile under DSB1's blind budget), DF2, DF4, NGC 147 and IC 1613 (36).

## What is undecided, and what would decide it

- RC100's massive z 2 discs and rows 7 and 8: resolved rotation curves beyond about 3 R_1/2 with measured
  gas profiles on both sides of log M_b 11.3 / 11.5 (DSC1). ALPAKA cannot (9): gas conversion, sizes, beam. DSC1R's
  reconciliation adds: beam-forward modelling with each disc's real point-spread function and point covariance, and a
  gas conversion fixed independently, because the answer above v* turns on how many points count as independent.
- The forest at flux level for this split (22): a blind build whose boundary-removed twin bites (FRZ6R's did not), so
  that the hold can be confirmed or refuted as a label; f 1.25, which 12 seeds do not resolve; and beyond that a
  hydrodynamic forest model that sets the smoothing scale, a box of at
  least about 50 Mpc/h, 6 to 18 seeds at z 2.2 (FRZ3R, FRZ4); and f between 2 and 3 run in both builds. FRZ5 adds: the
  gas parameters must be fitted with the layout, not held fixed; refitting them removes about 91 % of the full layout's
  number and still leaves it about 6 times over the gate.
- f itself (44): a lensing gate that can see the settled radius (row 11 cannot, per SRH1R).
- The weak-lensing amplitude and the redistribution rows (24, 25): the split computed through the power spectrum, the
  shear row on reference runs without realisation noise, a refit with neutrino mass.
- Groups (17, 18): a census and lensing mass out to turnaround around groups near v*(0).
- The Bullet (19): the subcluster's gas before the merger.
- The Milky Way halo stars (27, 28): the outer star-count slope beyond about 39 kpc with a Sagittarius stream model and
  a contamination model in place of a band mask and a score cut, and the cold groups at 30 to 55 kpc set aside by a
  frozen rule (RRL1, MWT2).
- Wide lenses (40): the group mass along wide-lens sightlines (members, intragroup gas and light, line of sight).
- Euclid's ceiling (39): many more certified source redshifts than EUC16's 11 (follow-up spectra, or later releases with
  more roll angles); with 11 the gate's interval spans both of its lines.
- Wide binaries (38): Gaia DR4 on 2026-12-02, scored as pre-registered.
- The constants (42, 43): no data row can grade them; a derivation would.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
