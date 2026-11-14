# FRZ6 RESULT: the settled layout and the crossing-speed split graded at flux level (12 seeds at z 2.2)

**Labels as frozen** (FROZEN_CRITERIA.md 569333ff30). These are the lane's labels.

| case | canonical | alt |
|---|---|---|
| **S, split, f = 2** | **FOREST ROW HOLDS AT FLUX LEVEL** | **FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lambda_P x 0.5)** |
| **S, split, f = 3** | **FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lambda_P x 0.5)** | **FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lambda_P x 0.5)** |
| S, split, f = 1.25 | NO VERDICT (known answer e fails; twin T1 does not bite) | NO VERDICT (e fails; T1 does not bite) |
| U, unsplit, f = 1 | NO VERDICT (e fails; i fails; T1 does not bite) | NO VERDICT (e fails; i fails) |
| U, unsplit, f = 2 | NO VERDICT (i fails; T1 does not bite) | NO VERDICT (i fails; T1 does not bite) |
| U, unsplit, f = 3 | NO VERDICT (i fails) | NO VERDICT (i fails) |
| C, control, f = inf | NO VERDICT (i fails) | NO VERDICT (i fails) |

**Labels under AMENDMENT_A1** (352a7fe6ae). A1 is post hoc and changes only whether known answer (i) passes.

| case | canonical | alt |
|---|---|---|
| S f = 2, 3 and S f = 1.25 | as frozen (the S cases do not use (i)) | as frozen |
| U f = 1 | NO VERDICT (e fails; T1 does not bite) | NO VERDICT (e fails) |
| U f = 2 | NO VERDICT (T1 does not bite) | NO VERDICT (T1 does not bite) |
| U f = 3 | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lambda_P x 0.5; gamma 1.6) | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lambda_P x 0.5; gamma 1.6) |
| **C f = inf** | **FOREST ROW FAILS AT FLUX LEVEL** (reproduces FRZ4) | **FOREST ROW FAILS AT FLUX LEVEL** (reproduces FRZ4) |

**What the labels mean**
- **Every HOLDS is a hit, not a pass of the theory.** It awaits an independent blind re-grade.
  - The settled-radius family is post hoc.
  - The crossing-speed boundary is post hoc to SRJ2 and JNT1.
  - kappa = 1/2 and 5.41 are FITTED.
  - Nothing here says the data favour the framework.
- **The as-frozen U and C words are NO VERDICT because of known answer (i).** (i) required FRZ4's reused spectra to be reproduced to 1e-12 for the 3D matter power as well as for P1D.
  - P1D, the graded quantity, is reproduced to 6.7e-16.
  - The 3D matter power is reproduced only to 1.7e-7, its single-precision rounding.
- **The control reproduces FRZ4's FAILS only under A1.** As frozen, it is NO VERDICT for the reason above alone. Its flux D minus 2 SE is 163 / 201, far above 4.

TEST lane: adopts nothing, relabels nothing. FRZ4, FRZ5, JNT2, JNT2R and every earlier lane keep their labels, and nothing is registered. Footings are graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is added.

**Pre-registration.** The frozen criteria were committed alone before any script existed (569333ff30, pushed as origin 82fc8815d3). They were deposited before any result, as DOI 10.5281/zenodo.24208901, created 2026-11-13 22:41 UTC; the lead recorded the deposit.

## The numbers

D is the 12-bin flux Delta chi^2. The z 2.2 bin is the mean ratio over 12 seeds; z 2.6 / 3.0 / 3.4 / 3.8 / 4.4 use seed 0; the six other bins are interpolated linearly in z. SE = 2 sqrt(D N12) + N12.

| case | D can / alt | N12 can / alt | (e) | SE can / alt | D + 2 SE can / alt | matter D_mat / D_ta (halo model) can | alt | D_rec can / alt | FRZ5 refit (template) can / alt |
|---|---|---|---|---|---|---|---|---|---|
| S f = 1.25 | 0.088 / 0.156 | 0.052 / 0.068 | FAIL / FAIL | 0.19 / 0.27 | 0.46 / 0.70 | 0.00042 / 0.00055 | 0.0027 / 0.0036 | 0.0008 / 0.0050 | 0.058 / 0.133 |
| **S f = 2** | **0.196 / 0.257** | 0.021 / 0.027 | pass / pass | 0.15 / 0.19 | **0.50 / 0.65** | 0.035 / 0.040 | 0.103 / 0.118 | 0.049 / 0.146 | 0.125 / 0.161 |
| **S f = 3** | **1.144 / 1.434** | 0.037 / 0.042 | pass / pass | 0.45 / 0.53 | **2.04 / 2.50** | 1.35 / 1.56 | 4.35 / 5.02 | 1.99 / 6.43 | 0.43 / 0.61 |
| U f = 1 | 0.100 / 0.106 | 0.126 / 0.159 | FAIL / FAIL | 0.35 / 0.42 | 0.80 / 0.95 | 25.9 / 27.7 | 24.8 / 26.2 | 38.7 / 36.7 | 0.081 / 0.088 |
| U f = 2 | 0.447 / 0.347 | 0.037 / 0.035 | pass / pass | 0.30 / 0.25 | 1.04 / 0.86 | 252 / 268 | 155 / 165 | 452 / 275 | 0.226 / 0.198 |
| U f = 3 | 2.149 / 1.879 | 0.057 / 0.054 | pass / pass | 0.76 / 0.69 | 3.66 / 3.26 | 379 / 410 | 274 / 297 | 680 / 481 | 0.785 / 0.729 |
| **C f = inf** | **256.1 / 282.3** | 1.92 / 1.36 | pass / pass | 46.3 / 40.5 | D - 2 SE = 163 / 201 | 4920 / 4983 | 4342 / 4398 | 9916 / 9009 | **22.0 / 21.3** |

**Reading the table**
- **Earlier FRZ4 numbers (2 seeds):** 0.10 / 0.11, 0.50 / 0.41, 2.20 / 2.04 and 269 / 288. The 12-seed means move little.
- **Single-seed spread at z 2.2** (canonical, smallest to largest of the 12 seeds):
  - S f = 2: 0.023 to 0.249.
  - S f = 3: 0.28 to 1.21.
  - U f = 3: 0.34 to 1.50.
  - C: 43 to 87.
- **The split lowers the flux D against the unsplit layout at the same f.** At f = 2: 0.196 against 0.447 canonical, 0.257 against 0.347 alt. At f = 3: 1.14 against 2.15 canonical, 1.43 against 1.88 alt.
- **At the smallest changes the flux number is a floor, not a signal.**
  - For S f = 1.25 and S f = 2, the flux D (0.09 to 0.26) is far above what the matter-level change would carry: D_mat is 0.0004 to 0.10.
  - That is the residual realisation noise of the stratified estimator, which (e) measures: N12 0.02 to 0.07.
  - So the S f = 2 HOLDS says the change is below what 12 seeds can resolve at flux level, and well under the gate. It does not say a signal was measured.
- **The FRZ5 refit is a template reading** (P1D3's per-bin amplitude, tilt and smoothing; `frz5_refit.py` run read-only up to its "reading G" marker).
  - Every fit is honest: no parameter is at a bound and no shift exceeds its limit.
  - The control's refit is 22.0 / 21.3 (FRZ5 gave 23.0 / 23.9). That is still above 4, so the full layout fails after refit too.

### Brackets: 12-bin estimate = D x (bracket / primary) on the bracket subset, seed 0, z 2.2 + 3.0 (clustered at z 2.2)

| bracket | S f = 1.25 can / alt | S f = 2 | S f = 3 | U f = 1 | U f = 2 | U f = 3 | C f = inf |
|---|---|---|---|---|---|---|---|
| lambda_P x 0.5 | **5.39 / 23.2** | 1.45 / **13.8** | **10.9 / 8.9** | **17.8 / 12.4** | **11.7 / 6.2** | **24.1 / 12.4** | 582 / 726 |
| lambda_P x 2 | 0.003 / 0.002 | 0.029 / 0.024 | 0.056 / 0.057 | 0.030 / 0.023 | 0.31 / 0.19 | 0.54 / 0.34 | 88 / 74 |
| lambda_P = 100 proper kpc | 1.5e-5 / 3.2e-5 | 0.0004 / 0.0009 | 0.009 / 0.021 | 0.013 / 0.012 | 0.11 / 0.065 | 0.14 / 0.10 | 57 / 38 |
| gamma 1.2 | 0.006 / 0.013 | 0.018 / 0.010 | 0.029 / 0.016 | 0.068 / 0.065 | 0.62 / 0.38 | 1.00 / 0.51 | 187 / 157 |
| gamma 1.6 | 0.17 / 0.25 | 0.27 / 0.54 | 2.41 / 3.42 | 0.23 / 0.20 | 0.83 / 0.68 | **5.38 / 5.08** | 337 / 383 |
| tau_eff x 0.9 | 0.091 / 0.15 | 0.22 / 0.30 | 1.31 / 1.68 | 0.11 / 0.11 | 0.46 / 0.36 | 2.56 / 2.29 | 280 / 315 |
| tau_eff x 1.1 | 0.084 / 0.16 | 0.18 / 0.22 | 1.01 / 1.24 | 0.092 / 0.10 | 0.44 / 0.34 | 1.86 / 1.58 | 235 / 254 |
| clustered placement | 0.094 / 0.48 | 0.15 / 0.19 | 0.21 / 0.23 | 0.019 / 0.078 | 0.70 / 0.28 | 0.31 / 0.44 | 48 / 78 |
| **measured range, 91.4 ckpc** | 0.045 / 0.071 | 0.14 / 0.19 | 0.77 / 0.67 | 0.093 / 0.074 | 0.54 / 0.31 | 2.18 / 1.23 | 196 / 207 |
| measured central, 113.8 ckpc (U, C only) | - | - | - | 0.081 / 0.041 | 0.41 / 0.22 | 1.46 / 0.80 | 132 / 134 |
| **measured range, 138.6 ckpc** | 0.015 / 0.014 | 0.026 / 0.045 | 0.14 / 0.19 | 0.032 / 0.038 | 0.33 / 0.21 | 0.94 / 0.36 | 100 / 94 |

**Brackets for U and C.**
- They use FRZ4's bracket parts and subset unchanged, rescaled to this lane's D. The measured-range values come from this lane's `mrU` parts on FRZ4's subset.
- **No bracket brings the control under 4.** Its lowest values are 48 (canonical, clustered) and 38 (alt, 100 proper kpc).

**Measured-range reading** (reported, never the label).
- Method: the lambda_P brackets are replaced by Rorai et al. 2017, Table S2, z = 3.0, range 91.4 to 138.6 comoving kpc. This is PROVISIONAL: read from the paper's web text, nothing downloaded, and their lambda_P may not equal this build's Gaussian filter scale one for one. gamma, tau_eff and clustered placement are kept.
- **Split:** under this reading, every split label that holds loses FRAGILE. S f = 2 and S f = 3 read **HOLDS / HOLDS** on both footings.
- **Unsplit and control, under A1:** U f = 3 reads HOLDS, FRAGILE (gamma 1.6) on both footings, and C still FAILS.
- **The primary value is below the measured range.** The primary lambda_P (79 comoving kpc, inherited) sits below the measured range at z 3. Every lambda_P inside the range lowers D.

**Bracket subset caveat.** The S subset holds 5 / 6 bins at z 2.2 (log M 11.3 to 11.7 canonical, 11.5 to 12.0 alt) and 2 / 4 at z 3.0. On that subset the primary Delta chi^2 is tiny for S f = 1.25 and S f = 2, so the bracket / primary ratio is very noisy there. This is FRZ4's caveat, unchanged. It is why lambda_P x 0.5 reads 23 for S f = 1.25 (alt) against D 0.16.

## Known answers (both footings)

| | canonical | alt |
|---|---|---|
| (a) f = 0 equals the reference (1e-12) | PASS: 5.6e-16 over 178 boxes; Delta chi^2 0 | PASS: 4.4e-16 over 180 boxes |
| (b) FRZ4's Poisson-only answer on FRZ4's parts | PASS: max rel 0; 165.951 = 165.951 | PASS: max rel 0; 210.793 = 210.793 |
| (c0) D_rec against the record | PASS, all 7 cases. U / C against SRH1 / SRF1 / FRZ1 within 3e-5; **S against JNT2's G1: 0.00081 / 0.04925 / 1.9900 vs 0.00081 / 0.04924 / 1.9898** | PASS, all 7; **S: 0.00505 / 0.14565 / 6.4327 vs 0.00505 / 0.14563 / 6.4321** |
| (c1) realised matter against the halo model | PASS, all 7. Ratio 0.925 to 0.987 (U, C, S f = 3); D_mat <= 1 rule for S f = 1.25, 2 (0.0004, 0.035); every checked bin 0.89 to 1.00 | PASS, all 7. Ratio 0.866 to 0.987; S f = 1.25, 2 at 0.0027, 0.10; checked bins 0.82 to 1.00 |
| (d) mean flux (1e-4) | PASS: 5.1e-14 | PASS: 5.3e-14 |
| (e) seed scatter, n = 12 | U f = 1 FAIL (N12 0.126 vs D 0.100); **S f = 1.25 FAIL** (0.052 vs 0.088); the other five PASS | U f = 1 FAIL (0.159 vs 0.106); **S f = 1.25 FAIL** (0.068 vs 0.156); the other five PASS |
| (f) split identity (S only) | PASS: B equals R to 6.7e-16 in 1254 spectra of bins wholly above v*; grid haloes above v* = JNT2's at every computed bin (170, 181, 192, 202, 211, 223) | PASS: 1119 spectra; 160, 172, 182, 192, 201, 213 |
| (i) identity with FRZ4 (U and C only) | **as frozen FAIL**: P1D 5.6e-16, P3D 1.7e-7 over 500 spectra (whole part z 2.2 seed 1: 320 spectra); **A1 PASS** | **as frozen FAIL**: P1D 6.7e-16, P3D 1.7e-7 over 518; **A1 PASS** |

- **(e) at n = 2 equals FRZ4's statistic exactly.** On seeds 0 and 1 the generalised form gives FRZ4's half-difference value to 1e-15 for every case. For example, U f = 1 canonical: 0.0062549 = 0.0062549.
- **The z 2.2 bin's share of D is as frozen.** It is a 12-seed mean; the other computed bins are single seeds. (e) scales the z 2.2 noise to 12 bins as FRZ4 did, so the noise of the single-seed bins is not measured directly.

## Twins (12 seeds at z 2.2; `frz6_grade_<footing>_MUTATE.out`)

| twin | U f = 1 | U f = 2 | U f = 3 | C f = inf | S f = 1.25 | S f = 2 | S f = 3 |
|---|---|---|---|---|---|---|---|
| T1, base change doubled, factor (needs >= 1.5), can / alt | **1.49** / 2.12 | **1.23 / 1.32** | 1.82 / 1.83 | 3.17 / 3.37 | **0.95 / 0.97** | 1.72 / 1.68 | 2.13 / 2.00 |
| T2, base saturation removed, factor (needs >= 1.25 or <= 0.8) | 34 / 42 | 871 / 1229 | 1098 / 1140 | 21 / 6.9 | 713 / 2213 | 1635 / 1626 | 1048 / 1075 |

**Why T1 fails to bite in some cases.**
- T1 assumed the base box carries the settled change, but for U f = 1, 2 and S f = 1.25 it does not. There, the base box's change and the forced boxes' change partly cancel, so doubling the base alone moves the z 2.2 value by less than 1.5x. For S f = 1.25 it barely moves at all, because the z 2.2 flux value there is realisation noise.
- This is a design weakness of the twin, written before the numbers. It was not amended. Under the frozen rule it makes those cases NO VERDICT.

**The graded HOLDS cases pass every check.** Both twins bite for S f = 2, S f = 3 and U f = 3 on both footings. This was re-checked at 12 seeds before HOLDS was written.

**Reported, not graded:**
- FRZ4's M2 (all boxes, seed 0): 4.2 / 2.7 / 3.7 / 66 canonical; 5.7 / 2.9 / 3.0 / 99 alt.
- FRZ4's M1 (subset): 9e4 / 7e4 / 8e3 / 60 canonical; 2e5 / 7e4 / 6e3 / 46 alt.
- M1 on the S subset: 300 to 1640.

## What was left out

- **Gas physics.** Everything FRZ4 left out stays out:
  - hydrodynamics, shocks and hot halo gas, self-shielding;
  - UV and temperature fluctuations, metals, continuum and noise;
  - peculiar velocities (real space only).
  - The 20 Mpc/h box: one forced halo per box, no two-halo term between forced haloes, uniform placement in the primary.
- **Inherited PROVISIONAL inputs:** FRZ1's halo model, SRH1's layout, the FGPA constants, tau_eff(z), and lambda_P = 79 comoving kpc.
- **Seeds.** Only z 2.2 has 12 seeds; the five other computed bins have one seed each. Six bins are interpolated.
- **Membership.** The split uses the model virial speed only (FRZ1's v_vir of M200c). Forest haloes have no measured speed.
- **Not bracketed:** the rare threshold, the 0.005 forcing cut, box size and resolution.
- **Brackets complete.** Every bracket part was computed, so no label carries "[brackets incomplete]".

## Disclosures

- **Order of commits.**
  1. Criteria alone (569333ff30).
  2. AMENDMENT_A1 alone (352a7fe6ae). Its header says "about 19:10 EST"; it was actually written and committed at about 18:48 EST. Git holds the true time.
  3. Scripts, 44 parts and graded outputs (d4e502f2d9).
  4. This file.
  Nothing pushed.
- **Runner stop at 18:45 EST (code bug, fixed).**
  - In `frz6_run.py`, `spec_list` built the bracket specs from FRZ4's `BR_SPECS` without FRZ4's substitution of `lam_rec(z)` for the 100-proper-kpc spec, whose length is `None`. The first bracket part then stopped in `gas` with a `TypeError`.
  - The fix: `spec_list(names, z)` now maps a `None` length to `lam_rec(z)`, exactly as FRZ4's `specs_for` does. Both calls pass z.
  - No criterion, spec or number changed. The remaining stages ran from `run_rest.sh` in the frozen order, after the first bracket box was inspected.
  - All primary parts were finished before the stop.
- **Grader bug, fixed before the final grading.** Known answer (i) is "one whole part (z 2.2 seed 1 canonical)". The grader first looked for that part in the footing being graded, which made alt fail for lack of a part. It now uses the canonical whole part for both footings, as the criteria say.
- **Test runs.**
  - One disclosed test grading of each footing on the primary parts (brackets not yet complete), plus one test refit (alt). They found the alt whole-part lookup bug above and the P3D precision fact behind A1.
  - Their outputs were deleted. No final number comes from them. Only A1 (committed alone) and the bug fix followed.
  - The tests did print U and C bracket estimates, rescaled from FRZ4's existing bracket parts, before A1 was committed. No S bracket number existed then.
- **Wrong line range in the criteria.** The criteria cite `jnt2_common.py` lines 11 to 23 for the split's constants. The correct lines are **7 to 18** (`vstar_kms`, mode "main"), with `jnt2_hm.py` lines 29 to 45 (`above()`, `lay_J`).
- **Lost console log.** The primary runner's console output was lost after the first flux jobs. The likely cause is that `frz3r_core.py` (line 22) uses `contextlib.redirect_stdout`, which is not thread safe, inside the threaded flux jobs. Numbers are unaffected. Progress was tracked by part files. The resumed bracket run logged normally.
- **Memory.**
  - In the primary stages, a process passed 16 GB peak inside almost every forced box (sampled directly: about 11 to 17.6 GB in one box). It exited with code 76 and was restarted from the box files, as the frozen rule requires. The exact count was in the lost log.
  - The resumed bracket stages restarted once.
  - Swap stayed at 3.8 to 4.4 GB; free disk stayed at 18 to 20 GB.
- **Wall time.** About 7.5 h of compute: primaries 12:34 to about 18:45 EST, brackets 18:45 to 19:58. About 8 h in total for the lane, inside the 10 h budget.
- **Housekeeping.** Temporary tables and arrays (223 MB) were deleted; `frz6_tables.py` regenerates them. Nothing was downloaded and nothing was written outside this folder.
- **Reuse.** FRZ4's parts were read read-only. Their U and C forced-box fields were merged only into parts whose R fields reproduce FRZ4's (P1D to 6.7e-16).

## Files

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`.
- `frz6_tables.py`: FRZ4's tables plus the split keys.
- `frz6_run.py`: FRZ4's runner with the added fields and stages.
- `frz6_grade.py`: FRZ4's grader with (e) generalised, (f), (i), the twins and the A1 reading.
- `frz6_refit.py`: FRZ5's refit, run read-only.
- `run_all.sh`, `run_rest.sh`.
- `parts/*.json`: 44 parts, 49 MB.
- Outputs: `frz6_grade_<footing>.json/.out`, `_MUTATE.json/.out` and `frz6_refit_<footing>.json/.out`.

## What this does to the forest row

At flux level, with 12 seeds where the noise lives, the crossing-speed split passes the forest gate at f = 2 and f = 3 on both footings, as frozen. D + 2 SE is 0.50 / 0.65 at f = 2 and 2.0 / 2.5 at f = 3, against 4.

That is a hit for the candidate sixth rule, not a pass:
- **Fragile under the frozen brackets.** Halving the pressure-smoothing scale pushes f = 3 (both footings) and f = 2 (alt) over the gate. Under the published measured smoothing range, nothing crosses.
- **At f = 2 the flux change is below what the build resolves.** The number is a noise floor; no signal was measured.
- **Unconfirmed.** It awaits an independent blind re-grade.

The unsplit settled layout and the full-layout control get graded words only under the post hoc amendment A1. Under A1:
- **The full layout fails at flux level on both footings again:** 256 / 282, and 22 / 21 after FRZ5's refit.
- **The unsplit layout at f = 3 holds, but FRAGILE:** lambda_P x 0.5 and gamma 1.6 both cross the gate.

The f = 1 and f = 1.25 cases stay ungraded: even 12 seeds do not resolve a change that small. The f = 2 unsplit case also stays ungraded, because its doubled-change twin did not bite.

So the forest row is no longer the plain failure of the full layout. The settled and split layouts are graded as holding at flux level where the build can resolve them, with every frozen caveat attached. The full layout still fails.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
