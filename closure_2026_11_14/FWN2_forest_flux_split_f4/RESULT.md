# FWN2 RESULT (2026-11-14): the crossing-speed split at f = 4, at flux level, in both builds

**Read across, as frozen (FROZEN_CRITERIA.md, 26cb002843, section 4). There is no amendment.**

| footing | build A, case S4 (f = 4) | build B, case J4 (f = 4) | read across |
|---|---|---|---|
| canonical | NO VERDICT (unresolved at 12 seeds: D 4.34, SE 1.1) | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5; gam_1.6) | **f = 4 NOT RESOLVED** |
| alt | NO VERDICT (unresolved at 12 seeds: D 5.37, SE 1.33) | NO VERDICT, FRAGILE (lam_x0.5; gam_1.6; tau_x0.9) | **f = 4 NOT RESOLVED** |

What the words mean:
- Build A cannot tell at f = 4 on either footing: its number sits above the gate and its error spans the gate.
- Build B, whose error is seven to eight times smaller, reads under the gate on canonical (a hit, FRAGILE) and misses the
  HOLDS line on alt by 0.035.
- Half a step either side, in build B only: f = 3.5 HOLDS (FRAGILE) and f = 4.5 FAILS (FRAGILE), on both footings.
- Every known answer passes in both builds on both footings, and every gating twin bites.

This is a TEST lane, NOT blind, and adopts nothing. FRZ6, FRZ6R, FWN1, FWN1R and every earlier lane keep their labels;
nothing is registered. The footings are graded separately and never pooled. Cold dark energy is a gravitating field
component; no particle is added. kappa = 1/2 and 5.41 are FITTED. The settled-radius family and the crossing-speed boundary
are both post hoc; f is a free constant; rule 6 is a candidate, NOT ADOPTED. A HOLDS label is a hit that awaits an
independent blind re-grade, not a pass of the theory. A hold means not excluded. Nothing here can say the data favour the
framework.

## The numbers

D is the 12-bin flux Delta chi^2 on DESI DR1 P1D (755 points, full covariance); the gate is Delta chi^2 <= 4.
Build A: 12 seeds at z 2.2, seed 0 at five other bins, six bins interpolated; SE = 2 sqrt(D N12) + N12.
Build B: 4 seeds in all 12 bins, ratio of seed sums, jackknife SE over the seed index.
Every number below is copied by a script from the grade files in this folder.

| build | case (f) | footing | D | SE | D + 2 SE | D - 2 SE | label as frozen |
|---|---|---|---|---|---|---|---|
| A | S4 (4) | canonical | 4.339 | 1.101 | 6.542 | 2.137 | NO VERDICT (unresolved at 12 seeds: D 4.34, SE 1.1) |
| A | S4 (4) | alt | 5.366 | 1.327 | 8.020 | 2.712 | NO VERDICT (unresolved at 12 seeds: D 5.37, SE 1.33) |
| B | J3.5 (3.5) | canonical | 1.498 | 0.087 | 1.672 | 1.324 | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5; gam_1.6) |
| B | J3.5 (3.5) | alt | 1.781 | 0.099 | 1.979 | 1.584 | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5; gam_1.6) |
| B | J4 (4) | canonical | 3.178 | 0.155 | 3.488 | 2.868 | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5; gam_1.6) |
| B | J4 (4) | alt | 3.712 | 0.161 | 4.035 | 3.390 | NO VERDICT, FRAGILE (lam_x0.5; gam_1.6; tau_x0.9) |
| B | J4.5 (4.5) | canonical | 5.617 | 0.227 | 6.072 | 5.162 | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lam_x2; gam_1.2) |
| B | J4.5 (4.5) | alt | 6.623 | 0.291 | 7.205 | 6.041 | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lam_x2; gam_1.2) |

How to read the table:
- **Build A at f = 4.** D is 4.34 / 5.37 (canonical / alt), above the gate, with twice its error reaching down to
  2.14 / 2.71. The label is NO VERDICT on both footings. Other build-A numbers: matter-level 9.62 / 29.24 against the halo
  model's 10.96 / 33.22; record convention D_rec 14.29 / 43.98; N12 0.062 / 0.073; the twelve single-seed values at z 2.2
  run from 1.08 to 3.35 (canonical) and 1.05 to 3.25 (alt).
- **Build B at f = 4.** D is 3.18 / 3.71. On canonical, D plus twice its error is 3.49, under the gate: HOLDS. On alt it
  is 4.035, over the gate by 0.035: NO VERDICT. The label stands as frozen; no rule was changed.
- **The two builds at f = 4.** Build A is the higher by 1.16 / 1.65, which is 1.04 / 1.24 times the two errors combined
  (ratio of the numbers 1.37 / 1.45). They do not contradict each other; build A's error is too large to add anything.
- **Half steps, build B.** f = 3.5 reads 1.50 / 1.78 and holds with room. f = 4.5 reads 5.62 / 6.62 and fails with room.
  So in this build the gate is crossed between f = 4 and 4.5 on canonical, and between 3.5 and 4.5 on alt.

Words by f, build A / build B, with this lane's points added (`fwn2_collect.out`):

| f | canonical | alt |
|---|---|---|
| 2 | HOLDS (FRZ6) / NO VERDICT (FRZ6R) | HOLDS (FRZ6) / NO VERDICT (FRZ6R) |
| 3 | HOLDS (FRZ6) / NO VERDICT (FRZ6R) | HOLDS (FRZ6) / NO VERDICT (FRZ6R) |
| 3.5 | not run / HOLDS | not run / HOLDS |
| 4 | NO VERDICT / HOLDS | NO VERDICT / NO VERDICT |
| 4.5 | not run / FAILS | not run / FAILS |
| 5 | NO VERDICT (FWN1) / FAILS (FWN1R) | NO VERDICT (FWN1) / FAILS (FWN1R) |
| 10 | FAILS (FWN1) / FAILS (FWN1R) | FAILS (FWN1) / FAILS (FWN1R) |
| no settled radius | FAILS (FWN1) / FAILS (FWN1R) | FAILS (FWN1) / FAILS (FWN1R) |

- **Largest f that HOLDS as a label in both builds: none.** At f = 2 and 3 build A holds and the blind FRZ6R reads
  NO VERDICT (its own boundary-removed twin did not bite there); at f = 3.5 build A was not run; at f = 4 build A cannot
  tell.
- **Smallest f that FAILS as a label in both builds: 10** (unchanged from FWN1 and FWN1R).
- Every HOLDS and every FAILS label from f = 3 to 5 is FRAGILE.

## The ceiling on f (reported, never a label)

Log-linear interpolation between adjacent run points, of the f where each quantity equals the gate:

| | build A canonical | build A alt | build B canonical | build B alt |
|---|---|---|---|---|
| D + 2 SE = 4 | 3.54 | 3.37 | 4.12 | 3.99 |
| D = 4 | 3.93 | 3.75 | 4.19 | 4.06 |
| D - 2 SE = 4 | 5.20 | 5.03 | 4.28 | 4.14 |

- Before this lane the same interpolation, across the gap from f = 3 to 5, gave 3.6 / 3.4 (FWN1) and 4.24 / 4.07 (FWN1R)
  for D + 2 SE = 4. With f = 4 run, build A reads 3.54 / 3.37 and build B 4.12 / 3.99.
- Build B's band is now 0.16 / 0.14 wide in f (4.12 to 4.28 canonical, 3.99 to 4.14 alt). Build A's band is 3.5 to 5.2
  and 3.4 to 5.0.
- Build B's run points, D (SE): canonical f 2: 0.024 (0.003); 3: 0.572 (0.044); 3.5: 1.498 (0.087); 4: 3.178 (0.155);
  4.5: 5.617 (0.227); 5: 8.834 (0.333); 10: 194.5 (5.2). Alt f 2: 0.029 (0.003); 3: 0.691 (0.047); 3.5: 1.781 (0.099);
  4: 3.712 (0.161); 4.5: 6.623 (0.291); 5: 10.897 (0.564); 10: 288.0 (6.8).

## Known answers and controls

- **Build A, both footings:** (a), (b), (c0), (c1), (d), (e), (f), (i), (j1), (j2), (j3) all PASS.
  - (i) identity with FWN1: this lane's base-box reference field equals FWN1's in all 12 seeds (0.0), in every box of
    every other-redshift part (at most 4.4e-16 in P1D, 7.9e-8 in P3D) and in the bracket parts (4.4e-16).
  - (j1) control S5 at seeds 0 and 1 equals FWN1's over 128 boxes: P1D 0.0, P3D 6.0e-8 / 1.9e-7.
  - (j2) control C from FRZ6's parts: 256.07 (46.30) / 282.35 (40.54), D - 2 SE 163.46 / 201.27, still fails.
  - (j3) this lane's grader on FWN1's parts gives FWN1's stored S5.00: 8.0854 (2.4138) / 9.4479 (2.7901), relative
    difference 0.
  - (c0) D_rec of S4.00 through this lane's tables 14.295 / 43.984 against JNT2's chain 14.294 / 43.980.
- **Build B, both footings:** KA-5, KA-C and KA-INF (read from FWN1R's grade file), KA-N, KA-F, KA-M and KA-S all PASS.
  - KA-5: the recomputed R and J5 equal FWN1R's stored parts in all 48 files per footing (largest deviation 0.0); J5
    reads 8.8339 (0.3328) / 10.8967 (0.5639), equal to FWN1R's stored values, and still fails.
- No known answer and no gating twin fails anywhere, so no label here is a NO VERDICT by cause other than the size of
  the error.

## Twins

- **Build A:** T1 (the layout change doubled in every box) 5.373 against 1.695, a factor 3.17 (canonical) and 5.438
  against 1.713, a factor 3.17 (alt): bites. T2 (saturation removed in the base box) 600.7 against 0.819 and 605.7
  against 0.584: bites.
- **Build B:** TW-A (boundary removed with no settled radius; FWN1R's stored value, not recomputed) 323.0 against 215.0,
  ratio 1.50, and 395.8 against 314.7, ratio 1.26: bites. TW-B4 (the difference doubled at f = 4) 5.001 against 1.353,
  a factor 3.70, and 5.640 against 1.534, a factor 3.68: bites (linear response predicts 4).
- **Reported, not a gate (frozen as such): the boundary removed at f = 4.** With the settled layout at f = 4 in every
  halo, D is 4.417 (0.391) against the split's 3.178 (0.155) on canonical, ratio 1.39: FWN1R's rule would bite. On alt it
  is 4.250 (0.359) against 3.712 (0.161), ratio 1.14: the rule would not bite. On alt, at f = 4, the crossing-speed
  boundary changes the forest number by less than this build can resolve; the settled radius does the work there.

## Brackets and the measured range

12-bin estimates under each frozen bracket (gate 4):

| case | footing | lambda_P x 0.5 | lambda_P x 2 | gamma 1.2 | gamma 1.6 | tau_eff x 0.9 | tau_eff x 1.1 |
|---|---|---|---|---|---|---|---|
| A S4 | canonical | 15.5 | 0.194 | 0.187 | 10.4 | 5.04 | 3.78 |
| A S4 | alt | 25.9 | 0.262 | 0.31 | 14.8 | 6.47 | 4.53 |
| B J3.5 | canonical | 9.63 | 0.0861 | 0.0381 | 4.8 | 1.78 | 1.27 |
| B J3.5 | alt | 10.1 | 0.122 | 0.0492 | 5.79 | 2.14 | 1.5 |
| B J4 | canonical | 17.4 | 0.21 | 0.196 | 10.5 | 3.79 | 2.7 |
| B J4 | alt | 18.2 | 0.306 | 0.303 | 12.6 | 4.44 | 3.14 |
| B J4.5 | canonical | 28.2 | 0.441 | 0.821 | 19.4 | 6.67 | 4.79 |
| B J4.5 | alt | 29.7 | 0.685 | 1.29 | 23 | 7.86 | 5.62 |

Build A's other brackets for S4: lambda_P 100 proper kpc 0.0796 / 0.259; clustered placement 0.382 / 0.63.

- Every hold crosses the gate when the gas smoothing scale is halved and when gamma is 1.6. FWN1R stated that half the
  smoothing scale is below one grid cell of this box and is not resolved.
- Both fails at f = 4.5 come back under the gate when the smoothing scale is doubled and when gamma is 1.2.
- At f = 4 the forest number moves by a factor of 60 to 100 across the frozen smoothing bracket and 40 to 55 across
  the gamma bracket, in both builds. The answer at f = 4 is set more by the gas parameters than by f.
- **Measured-range reading (reported beside the label, never the label).** With the smoothing scale at the two ends of
  the measured range (91.4 and 138.6 comoving kpc; Rorai et al. 2017, PROVISIONAL), both above the primary 79:
  - Build B J4: 2.545 / 0.406 (canonical) and 2.808 / 0.518 (alt): HOLDS at both ends on both footings.
  - Build B J4.5: 4.234 (NO VERDICT) / 0.821 (HOLDS) on canonical; 4.707 (FAILS) / 1.073 (HOLDS) on alt.
  - Build B J3.5: 1.311 / 0.161 and 1.484 / 0.214: HOLDS.
  - Build A S4: 3.31 / 0.523 (canonical) and 3.50 / 0.708 (alt); its measured-range reading stays NO VERDICT.

## Hand estimate against the result

The estimate was written in the frozen criteria (section 6) before any number of this lane.

| item | estimate, canonical / alt | result, canonical / alt | landed? |
|---|---|---|---|
| build A S4, D | 3.4 / 4.1 | 4.34 / 5.37 | higher, inside one SE |
| build A S4, SE | 1.2 / 1.4 | 1.10 / 1.33 | yes |
| build A S4, label | NO VERDICT 80 % | NO VERDICT / NO VERDICT | yes |
| build A twins | bite 95 % | bite | yes |
| build B J4, D | 2.7 / 3.3 | 3.18 / 3.71 | higher by 0.5 / 0.4 |
| build B J4, SE | 0.14 / 0.19 | 0.155 / 0.161 | yes |
| build B J4, label | HOLDS 60 % / 45 %, else NO VERDICT; FRAGILE more likely than not | HOLDS, FRAGILE / NO VERDICT, FRAGILE | yes |
| build B J3.5 | 1.3 / 1.6, HOLDS 85 % | 1.50 / 1.78, HOLDS | yes |
| build B J4.5 | 5.0 / 6.2, FAILS 60 % / 75 % | 5.62 / 6.62, FAILS | yes |
| TW-B4 factor | 3.3 to 4, bites | 3.70 / 3.68, bites | yes |
| U4 against J4, ratio | 1.2 to 2; bites 50 % | 1.39, would bite / 1.14, would not | canonical yes; alt below the range |
| read across | NOT RESOLVED 75 % | NOT RESOLVED / NOT RESOLVED | yes |
| build B ceiling | between 4 and 4.5 | 4.12 / 3.99 | canonical yes; alt just below 4 |

The interpolation between f = 3 and 5 ran low at f = 4 in both builds. Nothing landed outside the stated odds.

## What this changes and what it does not

- **f = 4 is now run in both builds; it is not resolved as a read across.** The scorecard's line "f 4 was run in neither
  build" is out of date.
- **The upper edge of f in the forest at flux level.** In the blind-written build (B): holds at 3.5 on both footings and
  at 4 on canonical, fails at 4.5 on both; every one of those labels is FRAGILE. In FRZ6's build (A): holds at 2 and 3
  (FRZ6), cannot tell at 4 and 5, fails at 10. As labels in both builds: nothing holds in both, and 10 is the smallest
  f that fails in both.
- **The holds are hits, not passes.** This lane is not blind: the lead knew both neighbours and wrote the estimate
  above. J3.5 on both footings and J4 on canonical await an independent blind re-grade. Build B's library was written
  blind for FWN1R, but the f = 3.5 and 4 cases were added and graded here by the lead.
- **Rule 6 stays a candidate, NOT ADOPTED.** Its settled radius is still needed (FWN1, FWN1R), f is still a free
  constant fitted to nothing, and the lower edge 1.25 still comes from a lensing gate that cannot see f.
- **Not covered.** Both builds share the same gas model and parameters (FGPA, T0, gamma, tau_eff, lambda_P; all
  PROVISIONAL), the same 20 Mpc/h box at N 384, real space, and the same post hoc layout family. A wrong assumption
  there is shared. FRZ5's refit reading was not run. The lensing-amplitude tension is not touched.
- **Build A cannot settle f = 4 at this size.** With D 4.34 and the gate at 4 on canonical, twice the error would have
  to fall below 0.34; at 12 seeds it is 2.2. By hand, that is about 40 times the seeds.

## Procedure notes

- The criteria were committed alone at 09:34:27 EST (26cb002843). Their header says "written about 09:40 EST"; that was
  an estimate made while writing, and the commit time is the record. The first build-B part file is stamped 09:38:30 and
  the first build-A part file 09:54:03.
- Both builds' scripts are copies of FWN1's and FWN1R's with the case list changed; FWN1R's library is imported
  read-only from its folder. No file or part of an earlier lane was edited.
- Before any graded number of this lane existed, both graders and the collector were run on relabelled parts of FWN1
  and FWN1R. Build B's grader reproduced FWN1R's stored values exactly. Build A's grader returned FWN1's S5.00 values
  exactly under the name S4.00, and its known answer (c1) failed there, as it should on relabelled data.
- The first part of each build was checked against FWN1's and FWN1R's stored parts (0.00e+00) before the stages were
  left to run.
- Compute: build A, 40 parts, 09:54 to 12:17, 17 restarts by its memory guard, no wait and no stop. Build B, 192 part
  files, 09:38 to 12:35, one wait (free + inactive memory 21.0 GB against the 24 GB line), no stop. A second build-B
  runner was started at 12:18, after build A's done marker (12:17). Never more than two heavy processes.
- Lead re-run: the two graders, both footings, and the collector were run again from a copy of the scripts and parts in
  a new folder at the same depth, with build A's tables regenerated there. All 13 output files are byte-identical to
  the ones committed here.
- The regenerable tables (`tmp/`) were deleted; the parts are committed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
