# FRZ4 RESULT: the forest row graded at flux level, rare haloes realised bin by bin

**Labels, as frozen (FROZEN_CRITERIA.md 199d710a9a; no amendment):**

| case | canonical | alt |
|---|---|---|
| **A, f = inf (full layout)** | **FOREST ROW FAILS AT FLUX LEVEL** | **FOREST ROW FAILS AT FLUX LEVEL** |
| B, f = 1 (settled) | NO VERDICT (known answer e fails) | NO VERDICT (e fails) |
| B, f = 2 | NO VERDICT (e fails) | NO VERDICT (e fails) |
| B, f = 3 | NO VERDICT (e fails) | NO VERDICT (e fails) |

- **The matter-level known answer (c1) passes in every case and on both footings.** This is the one that sank SRF1. The
  realised fields carry 0.92 to 0.99 of the halo model's own change, in the 12-bin total and in every computed redshift
  bin (per-bin ratios 0.89 to 1.01).
- **Case A is the first graded flux-level label for the forest row.** The full layout fails at flux level on both footings,
  by a factor of about 70: Delta chi^2 = 269 / 288 against the gate of 4. No bracket brings it under 4; the lowest is
  59 / 38 (lambda_P = 100 proper kpc).
- **Case B cannot be graded.** At f = 1, 2, 3 the flux-level change is so small that two seeds of the base box differ by as
  much as the effect itself. The frozen seed-scatter test (e) therefore fails. The ungraded numbers are all below the gate
  (0.10 / 0.11, 0.50 / 0.41, 2.20 / 2.04). Even so, f = 3 is MARGINAL by the frozen SE, and one or more brackets cross
  the gate in every settled case (lambda_P x 0.5 for f = 1, 2, 3; also gamma 1.6 for f = 3). Had (e) passed, all six
  settled readings would carry FRAGILE.

TEST lane: adopts nothing, relabels nothing (FRZ1, FRZ1R, FRZ3, FRZ3R, SRH1, SRH1R, SRF1, SRF1R keep their labels),
registers nothing. Footings graded separately, never pooled. Cold dark energy is a gravitating field component; no
particle is added. kappa = 1/2 is FITTED. The settled-radius family is post hoc. A FAILS label is not offset by anything
here, and nothing here says the data favour the framework.

## The table per case (12 bins: 6 computed, 6 estimated by linear interpolation in z; criteria section 4)

| case | flux Delta chi^2 can / alt | matter, same fields | flux / matter | halo model D_ta | c1 = matter / D_ta | record D_rec | record-convention reading (flux x D_rec / matter) |
|---|---|---|---|---|---|---|---|
| f = 1 | 0.103 / 0.108 | 25.9 / 24.8 | 0.0040 / 0.0043 | 27.7 / 26.2 | 0.933 / 0.945 | 38.74 / 36.66 | 0.15 / 0.16 |
| f = 2 | 0.503 / 0.413 | 251.3 / 155.1 | 0.0020 / 0.0027 | 268.3 / 164.9 | 0.937 / 0.940 | 452.1 / 275.1 | 0.90 / 0.73 |
| f = 3 | 2.20 / 2.04 | 378.4 / 273.4 | 0.0058 / 0.0075 | 409.7 / 296.8 | 0.924 / 0.921 | 679.7 / 480.5 | 3.95 / 3.59 |
| **f = inf** | **269.1 / 288.4** | 4920 / 4341 | 0.055 / 0.066 | 4983 / 4398 | 0.987 / 0.987 | 9916 / 9009 | 542 / 598 |

**Share above and below FRZ1's boundary speed.**
- Each forced 0.1 dex bin is assigned to a regime by the majority of its grid masses. The base box is counted below the
  boundary.
- Delta chi^2 is quadratic in the change, so the two parts do not add to the total.

| case | below the boundary: flux / matter (can; alt) | above the boundary: flux / matter (can; alt) |
|---|---|---|
| f = 1 | 0.140 / 0.010; 0.141 / 0.020 | 0.032 / 26.4; 0.016 / 25.7 |
| f = 2 | 0.34 / 0.48; 0.30 / 0.52 | 0.083 / 234; 0.036 / 143 |
| f = 3 | 1.76 / 15.0; 1.72 / 20.2 | 0.092 / 250; 0.040 / 152 |
| f = inf | 263 / 2868; 284 / 2782 | 0.20 / 293; 0.21 / 186 |

- **The full layout:** the flux-level failure comes from haloes below the boundary. The haloes above it carry a tenth of
  the matter change and almost none of the flux change.
- **The settled layout:** the matter change sits above the boundary, but the flux sees almost none of it (0.02 to 0.09).
  What the flux shows is mostly the base box (below the boundary, plus the two-halo term), which is also where the seed
  noise is.

**Per bin and per wavenumber** (canonical; alt alike, in `frz4_grade_alt.out`).
- **f = inf, flux Delta chi^2 per bin, z 2.2 to 4.4:** 65.1, 57.0 (est.), 29.7, 25.0 (est.), 20.6, 9.9 (est.), 6.8, 3.3
  (est.), 2.3, 1.4 (est.), 0.6 (est.), 0.45. The estimated bins at z 2.4 and 2.8 carry about 30 % of the total; the single-bin values of the six computed bins alone sum to 125 / 140, still far above the gate.
- **f = inf, R_F at k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km:**
  - z 2.2: 1.026 / 1.041 / 1.066 / 1.089 / 1.066.
  - z 3.0: 1.016 / 1.017 / 1.020 / 1.019 / 0.995.
  - z 4.4: 1.015 / 1.008 / 0.999 / 0.979 / 0.965.
  - So the flux power rises 2 to 9 % at large scales and low z. From z 3.4 up it falls 2 to 3.5 % at the small-scale end.
    This is FRZ3R's sign pattern.
- **Matter ratio against the halo model at k 3 / 5:** z 2.2: 0.9225 / 0.8197 against 0.9252 / 0.8220; z 3.0: 0.9159 /
  0.7889 against 0.9197 / 0.7947.
- **f = 1:** R_F lies within 0.002 of 1 at every computed bin and every listed k_v. The largest single bin is z 2.6
  (0.028).

## Known answers

| | canonical | alt |
|---|---|---|
| (a) f = 0 equals the reference, every box at the anchors (tolerance 1e-12) | PASS: 0 in 89 boxes; Delta chi^2 0 | PASS: 0 in 90 boxes |
| (b) Poisson-only path at f = inf against FRZ3R's reading T parts | PASS: max rel 0; flux 165.951 = 165.951, matter 2257.12 = 2257.12 (computed bins) | PASS: 0; 210.793 = 210.793; 2082.16 = 2082.16 |
| (c0) D_rec against SRH1 / FZS1 / FRZ1 (1 %) | PASS: 38.743 vs 38.741; 452.13 vs 452.12; 679.69 vs SRF1 679.69; 9916.4 vs 9916.2 | PASS: 36.659 vs 36.658; 275.13 vs 275.12; 480.52 vs 480.52; 9008.8 vs 9008.7 |
| **(c1) realised matter / halo model (0.67 to 1.5; per computed bin 0.5 to 2)** | **PASS all four: 0.933, 0.937, 0.924, 0.987; bins 0.89 to 1.00** | **PASS all four: 0.945, 0.940, 0.921, 0.987; bins 0.89 to 1.01** |
| (d) mean flux, every field (1e-4) | PASS: 5.1e-14 | PASS: 5.3e-14 |
| (e) seed scatter at z 2.2 (N12 <= 0.1 D or <= 0.05) | f = 1 FAIL (N12 0.17 vs D 0.10); f = 2 FAIL (0.28 vs 0.50); f = 3 FAIL (0.60 vs 2.20; SE 2.9, MARGINAL); **f = inf PASS (12.7 vs 269; SE 130)** | f = 1 FAIL (0.42 vs 0.11); f = 2 FAIL (0.16 vs 0.41); f = 3 FAIL (0.49 vs 2.04; SE 2.5, MARGINAL); **f = inf PASS (6.6 vs 288; SE 94)** |

**What the sampling fix did.**
- SRF1 drew one forced halo per 0.5 dex group and left the rare reference haloes at Poisson positions in its denominator.
  It over-realised by 1.78 / 1.86 at f = 1.
- Here every rare 0.1 dex bin carrying at least 0.5 % of the change, or of the reference one-halo power, gets its own box:
  27 to 31 bins per redshift and footing, log M 10.7 to 14.1. Numerator and denominator are both stratified.
- The realised change now matches the halo model to 1 to 8 %, bin by bin. The non-forced rare bins hold 0.0 to 0.6 % of
  the change.

**Why (e) fails for the settled cases, and what would be needed (no tuning after the fact).**
- The two seeds' z 2.2 single-bin values are 0.0088 / 0.0112 (f = 1), 0.124 / 0.192 (f = 2) and 0.92 / 0.50 (f = 3) on
  canonical.
- The noise is in the base box's response, which differs by seed in its smooth field and Poisson haloes. The forced
  haloes are not the source.
- To pass the frozen test, the half-difference Delta chi^2 has to fall by about 3x (f = 2, f = 3) to 9x (alt f = 1).
  Since that Delta chi^2 falls as 1 / n_seeds, this needs about **6 to 18 seeds at z 2.2** (base box and all forced
  boxes; about 15 min per seed and footing). It would also be prudent to run more than one seed at the other low-z bins.
- A re-run with more seeds would be a dated amendment, committed alone, and it would report this as-frozen reading
  first.

## Mutations (both bite in every case; `frz4_grade_<footing>_MUTATE.out`)

- **M1, saturation removed** (z 2.2, bracket subset): Delta chi^2 rises by factors of 9e4 / 7e4 / 8e3 / 60 (f = 1, 2,
  3, inf; canonical); alt is 2e5 / 7e4 / 6e3 / 46. Saturation still does almost all the softening.
- **M2, layout change doubled** (z 2.2, all boxes): factors 4.2 / 2.7 / 3.7 / 66 (canonical) and 5.7 / 2.9 / 3.0 / 99
  (alt). At f = inf the doubled change drives halo cores to the density floor, hence the large factor.

## Brackets (12-bin estimate = primary x bracket / primary on the bracket subset, z 2.2 + 3.0; clustered at z 2.2)

| bracket | f = 1 can / alt | f = 2 | f = 3 | f = inf |
|---|---|---|---|---|
| lambda_P x 0.5 | **18.3 / 12.6** | **13.2 / 7.3** | **24.7 / 13.4** | 612 / 742 |
| lambda_P x 2 | 0.03 / 0.02 | 0.35 / 0.23 | 0.56 / 0.37 | 92 / 76 |
| lambda_P = 100 proper kpc | 0.01 / 0.01 | 0.12 / 0.08 | 0.15 / 0.11 | **59 / 38 (lowest)** |
| gamma 1.2 | 0.07 / 0.07 | 0.69 / 0.45 | 1.03 / 0.56 | 197 / 161 |
| gamma 1.6 | 0.24 / 0.21 | 0.93 / 0.81 | **5.5 / 5.5** | 354 / 391 |
| tau_eff x 0.9 | 0.11 / 0.11 | 0.52 / 0.43 | 2.6 / 2.5 | 295 / 322 |
| tau_eff x 1.1 | 0.09 / 0.10 | 0.50 / 0.40 | 1.9 / 1.7 | 247 / 260 |
| clustered placement | 0.02 / 0.08 | 0.79 / 0.33 | 0.32 / 0.47 | 51 / 79 |

- **Case A: no bracket crosses the gate**, so the label has no FRAGILE. The pressure-smoothing scale moves the number by
  a factor of about 10 (59 to 612), as in FRZ3R, and stays far above 4 at every value tried.
- **Case B (ungraded):** lambda_P x 0.5 crosses the gate at every settled f on both footings; gamma 1.6 also crosses at
  f = 3.
  - Caveat: the bracket subset covers only 0.35 to 0.46 of the forced change at f = 1 to 3 (0.6 to 0.8 at f = inf). The
    frozen rule stops at 10 bins.
  - The subset's primary Delta chi^2 is itself small and noisy at f <= 3, so these ratios are uncertain. That is why
    f = 1 reads above f = 2.

## Other reported readings

- **Poisson-only reading** at f = inf: FRZ3R's reading T path on these seeds, every halo at its Poisson position, 12
  bins with the same estimated bins.
  - Flux: 357 / 442. Matter: 5316 / 4887. FRZ3R's own value was 363 / 425.
  - The stratified build gives 269 / 288 at the same matter level within 8 %. The rare haloes, realised fully, soften the
    flux somewhat.
- **Record-convention reading** of case A: flux x D_rec / D_mat = 542 / 598. This is the scale of FRZ1's 9916 / 9009
  carried through this build's flux-to-matter ratio.
- **Against the earlier ungraded builds:**
  - Case A: FRZ3 4.71 / 2.58 (at 80 proper kpc smoothing); FRZ3R 363 / 425; SRF1 170 / 263 (incomplete inf row).
  - Case B, f = 1: SRF1 0.068 / 0.072; SRF1R 0.008 / 0.005.
  - This build: 269 / 288 and 0.10 / 0.11.

## What is left out

- **Gas physics:** hydrodynamics, shock heating and hot halo gas, self-shielding and damped systems, UV and temperature
  fluctuations, metals, continuum and noise. The FGPA's saturated cores carry the softening (M1).
- **Peculiar velocities:** real space only.
- **Box:** 20 Mpc/h, so no modes below the fundamental.
  - Rare haloes are realised one at a time in an otherwise unchanged box.
  - A forced 1e14 Msun/h halo is a large fraction of the box mass.
  - There is no two-halo term between forced haloes.
  - Uniform placement in the primary; clustering only as a bracket.
- **Inputs inherited as PROVISIONAL:** FRZ1's halo model (Tinker and Duffy scalings) and SRH1's layout; the FGPA
  constants; tau_eff(z); lambda_P = 79 comoving kpc (Kulkarni et al. 2015). The pressure-smoothing scale moves case A by a
  factor of 10 without crossing the gate.
- **Estimated bins:** six of DESI DR1's twelve bins (2.4, 2.8, 3.2, 3.6, 4.0, 4.2) are linear interpolations in z.
- **Seeds:** one seed except at z 2.2.
- **Not bracketed:** the rare threshold 30, the 0.005 forcing cut, one halo per forced box, box size, resolution.
- **Lensing and rotation-curve rows:** not touched.

## Disclosures

- **Order of commits.** The criteria were committed alone before any script existed (199d710a9a). Code, parts and
  grading outputs come next, then this file. Not pushed.
- **Test grading.** One test grading of the canonical footing was run on the first finished part (z 2.2, seed 0) to
  catch bugs. It found empty 3D bins at low k: NaN, now masked to bins that hold modes, as SRF1 does with isfinite. Its
  outputs were deleted. No number of the final grade comes from it, and no criterion changed after it.
- **Memory.** A process exits when its peak passes 12 GB and is restarted (5 restarts). One bracket box (z 3.0,
  canonical, log M 12.4) reached **25.1 GB peak**, above the 20 GB ceiling, before that check ran at the end of the
  box. It was not killed. The box completed, and its numbers do not depend on memory. Peaks elsewhere were 12 to 15 GB.
- **Bracket subset.** Read as "until the subset's cumulative share of the forced set's total change reaches 0.8 at every
  f, at most 10 bins". The cap of 10 was reached in every part, before 0.8 was.
- **Machine time:** about 3.5 h wall (07:14 to 10:49 EST), one job, nice 19, 2 flux threads.
  - Tables: 12 x 27 s.
  - Primary: 6 z x 2 footings plus seed 1 at z 2.2.
  - Brackets at z 2.2 and 3.0; clustered at z 2.2.
  - Halo-model tables and base-box arrays (about 185 MB) were deleted; `frz4_tables.py` regenerates them.
  - Nothing downloaded; nothing written outside this folder. Console logs are git-ignored.
- **Folders never opened:** JNT2, JNT2R and JNT1R.

## Files

- `FROZEN_CRITERIA.md`.
- Scripts:
  - `frz4_tables.py`: SRF1's `srf1_tables.py`, copied and cut to f = 0, 1, 2, 3, inf.
  - `frz4_run.py`: SRF1's painting and flux job; imports FRZ3R's `frz3r_core.py` read-only.
  - `run_all.sh`.
  - `frz4_grade.py`: executes FRZ3R's grading set-up read-only.
- Outputs:
  - `parts/*.json`: 20 parts, 23 MB.
  - `frz4_grade_<footing>.json/.out` and `_MUTATE.json/.out`.

**Commit ids and the lead's re-run (added 2026-11-13, after landing; no number or label changes).** Local: criteria
199d710a9a, code, parts and grading outputs b89ced280f, RESULT b23f8b4aec (origin tip fe9a3ec771). Pushed. The lead
session re-ran `frz4_grade.py` for both footings from a copy at the same folder depth, on the committed part files: all
eight outputs are equal byte for byte. No field part was regenerated. A reproduction of the grading, not an independent
re-grade; the full-layout label agrees with the reported reading of the earlier blind build FRZ3R (363 / 425 there
against 357 / 442 here on the same placement).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
