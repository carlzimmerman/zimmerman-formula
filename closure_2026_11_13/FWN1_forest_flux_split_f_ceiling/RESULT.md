# FWN1 RESULT: the crossing-speed split at flux level for f = 5, 10 and no settled radius (12 seeds at z 2.2)

**Labels, graded under the frozen criteria (FROZEN_CRITERIA.md, fab8a8ee0e).** There is no amendment.

| case | canonical | alt |
|---|---|---|
| **Sinf: split with no settled radius (f = inf)** | **FOREST ROW FAILS AT FLUX LEVEL** | **FOREST ROW FAILS AT FLUX LEVEL** |
| **S10: split at f = 10** | **FOREST ROW FAILS AT FLUX LEVEL** | **FOREST ROW FAILS AT FLUX LEVEL** |
| S5: split at f = 5 | NO VERDICT (unresolved at 12 seeds: D 8.09, SE 2.41) | NO VERDICT (unresolved at 12 seeds: D 9.45, SE 2.79) |

What the labels mean:
- Every known answer passes on both footings, and both twins bite in every case.
- No frozen bracket brings S10 or Sinf under 4, so neither FAILS label is FRAGILE. The measured-range reading gives the same words.
- No case HOLDS, so no hit is waiting on a blind re-grade here.

This is a TEST lane and adopts nothing. FRZ4, FRZ5, FRZ6, JNT2 and every earlier lane keep their labels, and nothing is registered. The footings are graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is added. kappa = 1/2 and 5.41 are FITTED. The settled-radius family and the crossing-speed boundary are both post hoc. Nothing here can say the data favour the framework. This lane did not open the folder of the blind re-grade FRZ6R.

## The numbers

D is the 12-bin flux Delta chi^2:
- z 2.2 uses the mean of 12 seeds.
- z 2.6, 3.0, 3.4, 3.8 and 4.4 use seed 0.
- The six other bins are interpolated in z.

SE = 2 sqrt(D N12) + N12. The gate is Delta chi^2 <= 4.

| case | D can / alt | SE can / alt | D + 2 SE can / alt | D - 2 SE can / alt | N12 can / alt | matter D_mat / halo-model D_ta, can | alt | D_rec can / alt | FRZ5 refit (template) can / alt |
|---|---|---|---|---|---|---|---|---|---|
| S5 | 8.09 / 9.45 | 2.41 / 2.79 | 12.9 / 15.0 | **3.26 / 3.87** | 0.157 / 0.180 | 33.7 / 37.7 | 94.7 / 105.4 | 50.5 / 144.7 | 1.28 / 2.05 |
| S10 | **184.3 / 233.5** | 31.3 / 34.5 | 246.8 / 302.4 | **121.7 / 164.5** | 1.23 / 1.19 | 91.0 / 96.1 | 191.3 / 202.8 | 151.7 / 338.1 | **13.3 / 13.3** |
| Sinf | **200.5 / 251.1** | 34.0 / 37.1 | 268.5 / 325.2 | **132.4 / 176.9** | 1.33 / 1.28 | 79.5 / 82.1 | 161.6 / 167.6 | 125.2 / 269.6 | **13.7 / 13.1** |
| control C (unsplit, f = inf; FRZ6's parts) | 256.1 / 282.3 | 46.3 / 40.5 | | 163.5 / 201.3 (still fails) | | | | | (FRZ6: 22.0 / 21.3) |
| for reference, FRZ6 S f = 2 / f = 3 (stored) | 0.196, 1.144 / 0.257, 1.434 | | 0.50, 2.04 / 0.65, 2.50 | | | | | | |

How to read the table:
- **Removing the settled radius leaves most of the full layout's failure in place.**
  - Sinf is 200 / 251, against 256 / 282 for the unsplit full layout.
  - Sending every halo faster than v*(z) back to the reference layout removes only 22 % / 11 % of D.
  - The haloes slower than v*(z) carry the full layout out to r_ta, and that alone fails by about 50 to 63 times the gate.
- **S10 equals Sinf at z 2.2 and 2.6.**
  - The z 2.2 single-bin values and the 12 single-seed values are identical.
  - At those redshifts, 10 R_fold already exceeds r_ta for every halo slower than v*(z), so the cap R_set = r_ta takes over.
  - S10 and Sinf differ only from z 3.0 upward.
- **Single-seed z 2.2 values:**
  - S5: canonical 1.59 to 5.67, alt 1.66 to 5.46.
  - S10 and Sinf: canonical 25.8 to 54.2, alt 43.1 to 81.4.
- **Per-bin Delta chi^2 sits mostly at z 2.2 to 3.0.**
  - S10 canonical: 38.7 / 42.7 / 30.3 / 18.8 / 12.3 at z 2.2 / 2.4 / 2.6 / 2.8 / 3.0.
  - S5 canonical: 2.76 / 1.86 / 1.11 at z 2.2 / 2.4 / 2.6.
- **Flux ratio R_F at z 2.2** (k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km):
  - Sinf canonical: 1.024 / 1.034 / 1.057 / 1.087 / 1.075.
  - Sinf alt: 1.035 / 1.046 / 1.068 / 1.088 / 1.061.
  - S5 canonical: 0.992 / 0.994 / 1.002 / 1.028 / 1.039.
- **The FRZ5 refit is a template reading, not a physical gas model.** It applies P1D3's per-bin amplitude, tilt and smoothing.
  - Every fit is honest: no parameter sits at a bound.
  - It lowers S10 and Sinf to 13.1 to 13.7, still above 4.
  - It lowers S5 to 1.3 / 2.0.
- **Hand estimate against the outcome.**
  - I guessed D about 20 to 120 for Sinf and 10 to 90 for S10. Both came out higher (184 to 251).
  - The FAILS words matched the most likely guesses (75 % and 65 %).
  - S5 NO VERDICT was given 35 %.
  - A ceiling between 3 and 5 was given 60 %.

## The ceiling (reported, never a label)

Method:
- Q(f) = D + 2 SE at f = 2 and 3 (FRZ6's stored S rows), 5 and 10 (this lane), and inf.
- f* is where Q reaches 4, found by interpolating ln Q linearly in ln f between the two grid points that bracket 4. The form was fixed in the criteria before any number.

| footing | Q(2) | Q(3) | Q(5) | Q(10) | Q(inf) | **f* (D + 2 SE = 4)** | f where D = 4 | f where D - 2 SE = 4 |
|---|---|---|---|---|---|---|---|---|
| canonical | 0.50 | 2.04 | 12.9 | 247 | 269 | **3.6** (between 3 and 5) | 4.2 | 5.2 |
| alt | 0.65 | 2.50 | 15.0 | 302 | 325 | **3.4** (between 3 and 5) | 4.0 | 5.0 |

How uncertain this is:
- f* rests on only two grid points, f = 3 and f = 5.
- The f = 3 point is FRZ6's. This lane reproduced FRZ6's f = 3 spectra exactly on z 2.2 seeds 0 and 1 (known answer j1), but did not regrade it.
- The log-linear form is an assumption. Q rises about 6x between f = 3 and 5, so a different form could move f* by roughly 0.3 either way.
- The three columns give a fair band: about **3.4 to 5.2** for the f at which this build's forest fails at flux level.
- Every inherited PROVISIONAL gas input moves it further. For example, halving the pressure smoothing scale already made f = 3 FRAGILE in FRZ6. On the measured smoothing range, S5's estimate would be 0.93 to 4.6 (canonical) and 1.7 to 6.4 (alt), which straddles the gate.
- Read it as: the upper edge for f lies between 3 and 5, not as a measured value.

## Brackets

The 12-bin estimate is D x (bracket / primary), computed on the bracket subset at seed 0, z 2.2 and 3.0 (z 2.2 alone for clustered placement).
- Subset bins: log M 11.3 to 11.7 canonical and 11.5 to 12.0 alt at z 2.2; log M 11.0 to 11.2 canonical and 11.1 to 11.4 alt at z 3.0.

| bracket | S5 can / alt | S10 can / alt | Sinf can / alt |
|---|---|---|---|
| lambda_P x 0.5 | 27.2 / 37.7 | 604 / 593 | 692 / 670 |
| lambda_P x 2 | 0.62 / 1.02 | 37.2 / 61.1 | 39.3 / 64.3 |
| lambda_P = 100 proper kpc | 0.41 / 1.44 | **10.9** / 28.1 | **11.3** / 29.4 |
| gamma 1.2 | 2.36 / 3.40 | 97.7 / 114 | 105 / 121 |
| gamma 1.6 | 25.3 / 34.2 | 296 / 343 | 320 / 369 |
| tau_eff x 0.9 | 9.61 / 11.6 | 209 / 268 | 227 / 289 |
| tau_eff x 1.1 | 6.89 / 7.80 | 163 / 204 | 177 / 219 |
| clustered placement | 0.53 / 1.52 | 68.8 / 73.2 | 74.9 / 78.7 |
| measured range, 91.4 comoving kpc | 4.56 / 6.39 | 135 / 179 | 145 / 192 |
| measured range, 138.6 comoving kpc | 0.93 / 1.73 | 45.4 / 75.5 | 48.1 / 79.6 |

- **No bracket brings S10 or Sinf under 4.** The lowest values are 10.9 / 28.1 for S10 and 11.3 / 29.4 for Sinf, both at lambda_P = 100 proper kpc. So the FAILS labels are not FRAGILE.
- S5 is unresolved, so no FRAGILE word applies to it. Its brackets range from 0.4 to 38 and fall on both sides of 4.
- The measured-range reading (Rorai et al. 2017, Table S2, z = 3.0; PROVISIONAL, as in FRZ6) replaces the three lambda_P brackets. It gives the same words: FAILS / FAILS for S10 and Sinf, and NO VERDICT for S5.
- Every bracket part was computed, so no label carries "[brackets incomplete]".

## Known answers (both footings pass all of them)

| | canonical | alt |
|---|---|---|
| (a) f = 0 equals the reference | PASS: 0 over 89 boxes at z 2.2, 3.0, 4.4; Delta chi^2 0 | PASS: 0 over 90 boxes |
| (b) FRZ4's Poisson-only answer | PASS: 165.951 = 165.951 | PASS: 210.793 = 210.793 |
| (c0) D_rec against the independent JNT2 chain | PASS: 50.542 / 151.710 / 125.228 vs 50.538 / 151.704 / 125.223; chain f = 3 equals JNT2's stored 1.98976 exactly | PASS: 144.686 / 338.132 / 269.556 vs 144.679 / 338.123 / 269.549; chain f = 3 equals 6.43208 exactly |
| (c1) realised matter against the halo model | PASS: ratio 0.893 / 0.947 / 0.969; checked bins 0.82 to 0.97 | PASS: 0.899 / 0.943 / 0.964; checked bins 0.84 to 0.98 |
| (d) mean flux within 1e-4 | PASS: 5.0e-14 | PASS: 5.2e-14 |
| (e) seed scatter at n = 12 | PASS, all three cases (N12 0.157 vs 0.1 D = 0.81; 1.23 vs 18.4; 1.33 vs 20.0) | PASS, all three |
| (f) split identity and membership | PASS: B = R exactly in 1254 wholly-above spectra; membership 170 / 181 / 192 / 202 / 211 / 223 = JNT2's | PASS: 1119 spectra; 160 / 172 / 182 / 192 / 201 / 213 |
| (g) f = inf identity | PASS. (g1) In all 12 z bins, Sinf = finf exactly in every below-v* grid halo (151 at z 2.2) and = reference exactly in every above-v* halo. (g2) In 12 seeds' wholly-below forced boxes, B\|Sinf = FRZ6 / FRZ4 B\|finf, P1D and P3D difference 0 | PASS. (g1) 161 below / 160 above at z 2.2. (g2) as canonical |
| (i) R identical to FRZ6 (P1D 1e-12, P3D 1e-6, A1's tolerances) | PASS: P1D 6.7e-16, P3D 1.6e-7 over 1066 spectra; brackets 0 over 90 | PASS: P1D 6.7e-16, P3D 1.8e-7 over 1068; brackets 4.4e-16 over 120 |
| (i) pass-2 base-box R against pass 1 | PASS: 0 | PASS: P1D 0, P3D 9.7e-8 |
| (j1) control S3: this lane's f = 3 split = FRZ6's (z 2.2, seeds 0 and 1) | PASS: P1D 5.6e-16, P3D 1.5e-7 over 128 spectra | PASS: P1D 4.4e-16, P3D 2.2e-7 |
| (j2) control C graded from FRZ6's parts | PASS: D 256.0729 and SE 46.3044 equal FRZ6's exactly; D - 2 SE 163.5 > 4 | PASS: 282.3478, 40.5366 exactly; 201.3 |

- The 3D power differences are single-precision rounding, as FRZ6's amendment A1 found. They include 9.7e-8 between two runs of the same alt base box.
- The P3D tolerance was fixed a priori from A1, and the graded P1D agrees to machine precision everywhere.
- Shares of each case's change: non-forced rare bins carry 0 at every computed z. Forced bins carry 0.91 / 1.09 / 1.09 (canonical, S5 / S10 / Sinf) at z 2.2; the rest is in common bins.

## Twins (12 seeds at z 2.2; `fwn1_grade_<footing>_MUTATE.out`)

| twin | S5 can / alt | S10 can / alt | Sinf can / alt |
|---|---|---|---|
| T1, change doubled in every box (needs factor >= 1.5) | 3.04 / 3.19 | 78 / 109 | 78 / 109 |
| T2, saturation removed in the base box (needs >= 1.25 or <= 0.8) | 952 / 1298 | 17.9 / 6.35 | 17.9 / 6.35 |

- T1 was redesigned as the criteria required: the change is doubled in every box, so base-box and forced-box parts cannot cancel. It bites everywhere.
- At small change it scales by about 3x. For S10 and Sinf it scales by 78 to 109x, because the saturated, nonlinear flux response grows far faster than 4x. That still counts as biting, as the frozen rule says.
- Before the labels were written, the twins were re-checked at 12 seeds and control C was confirmed still failing (j2). No HOLDS was written.

## What was left out

- **Gas physics.** Everything FRZ4 and FRZ6 left out stays out:
  - hydrodynamics, shocks, hot halo gas and self-shielding;
  - UV and temperature fluctuations, metals, continuum and noise;
  - peculiar velocities (real space only);
  - the 20 Mpc/h box with one forced halo per box.
- **Inherited PROVISIONAL inputs:** FRZ1's halo model, SRH1's layout and cap, the FGPA constants, tau_eff(z), and lambda_P = 79 comoving kpc.
- **Seeds.** Only z 2.2 has 12 seeds; the other computed bins have seed 0 only, and six bins are interpolated.
- **Membership.** It uses the model virial speed only (FRZ1's v_vir of M200c).
- **The ceiling grid.** f = 4 was not computed, so f* comes from interpolation. The frozen criteria named f = 5, 10 and inf only.
- **Not bracketed:** the rare threshold, the forcing cut, box size and resolution.

## Disclosures

**Order of commits**
1. Criteria alone (fab8a8ee0e).
2. Scripts, 64 part files (47 MB, each under 2 MB), graded outputs, refit and logs (78c950240a).
3. This file.

There was no amendment. Nothing was pushed.

**Runner stop and pause (operational; no criterion changed)**
- The runner started at 20:53 EST.
- At 21:17 the machine went into heavy swap, about 21 GB, and free disk fell to about 4 GB.
  - The lead had loaded the machine with several heavy lanes at once.
  - This lane's part process was seen near 20 GB. The old 16 GB rule only checked peak memory at the end of each box.
- At 21:19 the runner's pre-part guard stopped it (swap 9.1 GB > 8 GB). Five complete parts were on disk.
- A relauncher was started at 21:20. It never relaunched, and it was stopped on the lead's instruction to keep the runner down.
- On the lead's operational instruction, three changes were made while paused:
  1. **A physical-footprint guard after every flux job.** Above 14 GB the process exits and restarts; a box that forces two exits then runs with one thread. Numbers cannot change, because flux jobs are deterministic and box files are written only when complete.
  2. **A new pre-part check.** Stop if free disk is below 8 GB or swap use is above 14 GB. Otherwise wait until free disk is at least 10 GB and free plus inactive memory is at least 24 GB. The old "swap at most 8 GB" test could not pass while idle applications held about 9 GB of stale swap.
  3. **A check of the five finished parts.** All were complete: 31 of 31 boxes, full field lists, every spectrum finite.
- The runner restarted at 22:30 on the lead's go and finished at 03:35 (64 parts). After the restart the footprint guard never fired and the pre-part check never waited.
- Details are in `logs/ops_notes.txt`. `resume_when_swap_ok.sh` is obsolete and was never used to relaunch.

**One disclosed test grading (canonical)**
- It ran at about 21:05 EST on the single part then on disk (z 2.2 seed 0, Sinf), to check the grader's code paths.
- It printed one-seed numbers for Sinf at z 2.2 only.
- Its JSON and .out outputs were deleted; its console log is kept as `logs/test_grade_canonical.log`.
- No code, criterion or number changed after it.

**Stage tests**
- Before the runner started, the first part of each later stage was run to its base box and first forced box, then stopped (`test_stages.sh`, `test_br.sh`).
- The runner later resumed those parts from their box files.
- The first bracket box was run explicitly. FRZ6's `None` smoothing-length bug for the 100-proper-kpc spec was already fixed in the copied code.

**Console log**
- `logs/run_all.log` lost the in-part progress lines, as in FRZ6 (`redirect_stdout` in `frz3r_core` is not thread-safe). Guard lines and stops were logged. Progress was tracked by part files.

**Compute**
- At most 3 flux threads, `nice -n 19`, one part process at a time.
- Free disk stayed between 15 and 16 GB. Swap stayed between 6.6 and 7.1 GB after the restart.

**Wall time**
- Compute: 20:38 to 21:19 and 22:30 to 03:35 EST, about 5.8 h.
- About 7.5 h for the lane overall, including the 71-minute pause.

**Housekeeping**
- Tables and base-box arrays (`tmp/`) were deleted; `fwn1_tables.py` regenerates them.
- Nothing was downloaded and nothing was written outside this folder.
- FRZ6's, FRZ4's, FRZ3R's and JNT2's files were read only.

**Hand estimate miss**
- The S10 and Sinf D values came out above the ranges written before any number. The words did not.

## Files

- `FROZEN_CRITERIA.md`
- `fwn1_tables.py`: FRZ6's tables with the S3.00, S5.00, S10.00 and Sinf split keys and known answer (g1).
- `fwn1_run.py`: FRZ6's runner with this lane's field plan and the footprint guard.
- `fwn1_c0.py`: the independent JNT2 chain.
- `fwn1_grade.py`: grading, controls, twins and the ceiling.
- `fwn1_refit.py`: FRZ5's refit, run read-only.
- `run_all.sh`, `test_stages.sh`, `test_br.sh`, `resume_when_swap_ok.sh` (obsolete).
- `parts/*.json`: 64 part files.
- Outputs: `fwn1_grade_<footing>.json/.out`, `_MUTATE.json/.out`, `fwn1_refit_<footing>.json/.out` and `fwn1_c0_<footing>.json/.out`.
- `logs/`.

## What this does to rule 6's settled radius

At flux level the crossing-speed split cannot do without a settled radius. With no settled radius, every halo slower than v*(z) carries the law's full layout out to its turnaround radius. The forest row then fails on both footings: D = 200 / 251 against a gate of 4, still 13 after FRZ5's template refit, and no frozen bracket rescues it. The split alone removes only a small part of the full layout's failure (256 / 282). The forest therefore fixes an upper edge for f.
- In this build the split passes at f = 2 and 3 (FRZ6, hits awaiting a blind re-grade), is unresolved at f = 5, and fails at f = 10 and beyond.
- The edge lies between 3 and 5: D + 2 SE reaches 4 near f 3.4 to 3.6, and the full band from D + 2 SE to D - 2 SE runs from 3.4 to 5.2.
- That edge is set by inherited, PROVISIONAL gas inputs, and the pressure smoothing scale alone could move it.

So f stays a free constant, not fixed by theory. This lane gives it an upper edge from the forest at flux level, roughly 3 to 5. Any lower edge comes from other rows and earlier lanes, which this lane did not re-check. Rule 6 needs its settled radius for the forest, and the forest allows that radius only up to about four times the fold radius.

## Commit ids and the lead's re-run (2026-11-14)

- Criteria fab8a8ee0e (origin 5d67fec5b3); scripts, parts and graded outputs 78c950240a (origin ab0e84c528); result 7676843bbf
  (origin 43ba522198).
- The lead re-ran, from a copy of the scripts and the committed parts at the same folder depth: `fwn1_c0.py` (the
  independent chain), `fwn1_grade.py` and `fwn1_refit.py`, on both footings. The two chain JSON files, the eight grade and
  twin outputs and the four refit outputs equal byte for byte; the two chain logs differ only in elapsed-seconds stamps.
  The boxes themselves were not re-run. (A first re-run that left the chain files out of the copy is discarded.)
- A reproduction of the grading, not an independent re-grade. An independent check of the same three cases in the blind
  build of FRZ6R was started on 2026-11-14 (lane FWN1R). No number or label changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
