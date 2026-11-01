# SP3_starting_point FROZEN CRITERIA (2026-11-01). Owner's go relayed: "keep going" on the mechanism push

**Lane id.** Briefed as SP1_starting_point. The prefix SP1 is taken by SP1_sealed_lensing_step and SP2 by SP2_sealed_basin_lensing, so this lane is SP3.

**Not blind.** Most neighbouring numbers are known: OP2, OP3, UR1-UR3, NR3, RET1, TP1, MH1, FG1, ZN2 A1 were read before this was written. kappa = 1/2 FITTED, unused here. No a0 in the cold sector. Cold dark energy, never a particle. Not theory closed. No LCDM inputs in a grade.

## Question
MH1 judged about 50 % that no contraction-undoing process is missing and that the ask comes from the start: EM1's fitted line plus a hand-set core. What start, with what's measured and no fitted number, removes the need to switch off the response? Separately: is the 150-250 km/s trough about halos at all, and where does SPARC's 0.50 come from?

## Record check, read before this file
Grid: shape (hand core, native zoom) x mass rule (EM1, AM1, RET1's E1, C1) x response (off, measured). The on-record cells are listed in the README with their eta. Graded only where the record has no row:

- **Hand core (NR2 medians, Blumenthal as NR3 and RET1 use it):** AM1 off, AM1 Blumenthal: SPARC side. AM1's own grade predates NR2.
- **Native shape (ZN2 A1 tags 1e10-1e14 at z = 0; these don't read eta, so NR2's medians don't enter them):** E1, C1, AM1 with f_Q 0 and 0.872; EM1 with both, for tilt and LITTLE THINGS, which OP3 and ZN2 didn't report. EM1 and AM1's Upsilon are on record and serve as checks. Extra row, declared now: FAIR200 on native, both f_Q, because fair share is the only mass rule with no fitted number and no provisional SN input. Not in the owner's grid, reported beside it.
- **Direct weighing by UR3's method, new on every row but EM1 hand core:** DiskMass r and Milky Way box class for all cells above, hand-core rows on an S table rebuilt at NR2's medians. EM1 native with the zoom table replaces UR3's stress, which carried c 12.95 across masses by hand.

## Rules
- Response measured on native: f_Q 0.872 (LC1), as OP3: M = M0 + f_Q (M_f - M0), X39's contract. On the hand core: Blumenthal, as NR3, RET1.
- E1, C1: RET1's own tabulated lines lg M200(lg M_b), linear interpolation, per background, unchanged. They were solved with V_esc on N's hand core. Carrying them to the native shape unchanged is a declared choice: a re-solve would need a launch radius the native shape doesn't define. RET1 gives launch sensitivity -0.02 to -0.03 dex.
- AM1: its `curve`, unrefitted. E1, C1 hold provisional SN numbers from RET1, external, stated.
- Native map: frozen (M_t = M200/f_c, OP3's primary) and FC1's. Both reported. A pass on one only is tagged [MAP-DEPENDENT].
- Groups aren't contracted on the native path, as OP3. Clamping below the lowest tag is counted and stated. LITTLE THINGS on native: UR1's `_lt` recipe with the native M0.

## Pass lines, the record's, unchanged
SPARC rms <= 0.110 and Upsilon 0.50-0.80, both backgrounds; tilt <= 0.15; groups |Z| <= 2; LITTLE THINGS |median E| <= 0.10. DiskMass REACHED: median r in [0.90, 1.10] at 1.5 h_R, at least 27 of 30 fitted (UR3). Milky Way: FEASIBLE IN PRIORS through UR3's `classify`. Keys on GS4 +0.005 and X-COP as on record: the keys don't read the galaxy map, hand core 12 of 15 off and 14 of 15 Blumenthal; native fair share 12 of 15 (ZN4), EM1 line 14 of 15 (OP2 ng 80). Native + response on clusters has never been graded: it's run here only if a measured-response cell clears every galaxy gate, in which case a follow-up criteria addendum is committed first.

**The 0.50-0.80 line is not moved here. Whatever section S finds, no verdict uses a changed line.**

## Labels
- **START RESOLVES [cells]:** a cell with response measured, no FITTED number, clearing line, tilt, groups, LITTLE THINGS, DiskMass and Milky Way in priors. It does not by itself clear clusters; the cluster row is stated beside it.
- **PARTLY:** a measured-response cell clears Upsilon's line on both backgrounds but misses another gate; or an off cell clears all galaxy gates, in which case the start works and the response still has to be switched off with no reason given.
- **NOT THE START:** neither. Tag [MAP-DEPENDENT] as above.

## Line refit, FITTED, reported, not a pass
EM1 was fitted with no response, so with a response a refit is a real alternative. UR2 did it on the hand core: not redone. On the native shape, f_Q 0.872, both maps: EM1 + delta, one offset, solved by bisection for Upsilon 0.50 on both backgrounds. This is an inversion, not a scan. delta tested against BL1's blue range (-0.10, +0.14) at 2 sigma. Tilt, groups, LITTLE THINGS read at delta. Labelled FITTED whatever it finds. PINCHED if outside blue's range.

## S: Upsilon, reported, no verdict on any cell
- **S1 origin of the line.** Trace 0.50-0.80 in the record: first statement, what it was attached to, what its lower edge is, whether it's a measurement.
- **S2 SPARC-independent stellar masses on disk, no new data.** Durbala+20 in `data_assembly/alfalfa_sdss_local_control/alfalfa_sdss.csv`, disjoint from SPARC's rotation curves. L_W1 is recovered from logms_mcgaugh (constant M/L_W1 0.45). Upsilon_W1 = 0.45 x 10^(logM_X - logms_mcgaugh), X = GSWLC SED, Taylor g-i. W1 stands in for 3.6 micron: a small band difference, not corrected. V = w50 / (2 sin i), i from ba_r with q0 0.2, ba_r <= 0.71 (i >= 45), hi_code 1. Bins: 100-150, 150-250, 250-400. Median and 16-84 %. **Reading:** 0.30-0.40 is BROKEN by stellar masses if every estimator's median at 150-250 is >= 0.45; NOT BROKEN if at least one median is <= 0.40; otherwise BETWEEN. Colour and SED masses are models with an IMF, so this reads as limits on what population modelling says, not a measurement of stars.
- **S3 same galaxies.** SPARC UGC number = AGC number; Upsilon_3.6 from the catalogue's M_star at SPARC's distance over SPARC's L[3.6], paired with the fitted Upsilon on EM1 hand core off and Blumenthal, at V_flat 150-250. Small n, reported.
- **S4 inclination.** TP1 didn't test it. Partial Spearman of Upsilon on inclination at fixed lg V_flat, 100-400 km/s, EM1 hand core off and Blumenthal, TP1's line p < 0.0071. Size: 2 e_i cot i against the shift in V^2 the trough needs.
- **S5 other weighings on disk.** DiskMass Upsilon_K and its conversion (h120), read only.

## Checks, before any verdict
- K1 hand path: EM1 off and Blumenthal vs NR2_MEDIAN and NR3 MEDIAN: |d| <= 1e-6 in Upsilon, rms.
- K2 native path: EM1 tot f_Q 0 and 0.872 vs `op3_results.json`: |d| <= 1e-6 in Upsilon, rms.
- K3 table reproduces RET1 on the hand core: E1 off and C1 off through my interpolated tables vs RET1's rows: |dU| <= 0.01, |d rms| <= 0.002, declared because of interpolation.
- K4 weighing path reproduces UR3 with UR3's own S table: off r 1.365, Blumenthal 1.071, NFW-start off 1.090: |d| <= 0.002.
- K5 AM1 native off vs ZN2 A1 `alt.am1` rms within 0.03: its range, 0.233-0.253 at another map path.
- K6 eta(1e12) 21.53 in the hand path's log; S table's eta inputs are NR2's.
- MUTATE, separate outputs: M_b x 2 in the native response must move Upsilon by >= 0.02 (OP3's was 0.11); halo mass x 2 in the weighing must move DiskMass r by >= 0.02. Failed check: no verdict.

## Expectation on record
NOT THE START, about 70 %. Every no-fit rule on record (AM1, E1, C1) is heavier than EM1, and a heavier or cuspier start with the response lowers Upsilon further: UR2's arithmetic, OP3's 0.44. FAIR200 is lighter and should fail tilt and groups as on the hand core. PARTLY about 25 %, most likely through FAIR200 or a heavy-line tilt fix. On S: about 60 % that the line turns out not to be a measurement, and that at least one independent mass estimator sits at or below 0.40 at 150-250 km/s. That wouldn't rescue anything by itself.

## Compute
One thread, nice 15, per-cell JSON cached so the run resumes after a stop. Outputs in this lane; cache_* and *.log gitignored. No push.
