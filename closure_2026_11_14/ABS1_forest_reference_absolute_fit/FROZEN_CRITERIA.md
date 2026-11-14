# ABS1 FROZEN CRITERIA (2026-11-14): does the forest gate's own reference model fit the DESI data in absolute terms?

Committed alone, before any script of this lane exists and before any number of this lane is computed. TEST lane, NOT
blind. It tests the forest gate's MODEL, not the framework. It adopts nothing, relabels nothing (FWN1R, FWN2 and every
earlier lane keep their labels) and registers nothing. Footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2)
are graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is added.

## 0. What I had seen before freezing (not blind)

- The lead's brief and the house rules.
- The memory index lines on FWN1, FWN1R, WLJ1 and FWN2 (the split fails the forest at flux level at f 10 and with no
  settled radius in both builds; f 5 same size; rule 6 needs f; the forest caps f between 3 and 5).
- Code, read in full: `closure_2026_11_14/FWN1R_blind_split_f_ceiling/fwn1r_lib.py`, `fwn1r_run.py`, `fwn1r_grade.py`;
  `closure_2026_11_14/FWN2_forest_flux_split_f4/fwn2b_grade.py`; `tau_field`, `tune_A`, `p1d`, `dv_cell`, `flux_p1d` of
  `closure_2026_11_12/FRZ3R_blind_flux_forest_regrade/frz3r_core.py`; `forest_setup` and `forest_eval` of
  `closure_2026_11_09/SS1_self_shielded_conversion/ss1_cosmo.py`.
- Results, read in full: `FWN2_forest_flux_split_f4/RESULT.md`; the canonical half and most of the alt half of
  `fwn2b_grade.out` (all D, SE, per-bin D, R_F at k_v 0.003 / 0.01 / 0.03, brackets, labels). So I know the stored D,
  SE and labels: J3.5 1.498 (0.087) / 1.781 (0.099) HOLDS / HOLDS; J4 3.178 (0.155) / 3.712 (0.161) HOLDS / NO VERDICT;
  J4.5 5.617 (0.227) / 6.623 (0.291) FAILS / FAILS; J5 8.834 (0.333) / 10.897 (0.564) FAILS; J10 194.5 / 288.0 FAILS;
  Jinf 215.0 / 314.7; C 323.0 / 395.8. I know J4 alt misses the HOLDS line by 0.035 (D + 2 SE = 4.035).
- `closure_2026_11_13/FRZ5_forest_nuisance_refit/FROZEN_CRITERIA.md` sections 1 to 7 and the function list of
  `frz5_refit.py`; the top of `closure_2026_11_14/GAS1_forest_gas_parameters_sourced/READING.md` (bracket placements).
- One inline query (not a lane script), made to write section 1: the data loader returns 755 points with md5
  33d7fc21bfd3d745ed71a0bbe80ca433; per redshift bin the data k range, and the box k_v grid read from the `kv` field of
  the stored parts (no power value of the box or of the data was printed). Table in section 1.
- I have NOT seen any absolute flux power of the box, nor any value of the DESI P1D itself, nor any number this lane
  will compute.

## 1. What the stored spectra are (read from the code)

- **Field.** The gas density is the realised matter field (halo-model painted halos plus a lognormal smooth component,
  `realise`) smoothed with exp(-k^2 lambda^2 / 2), lambda = 79 comoving kpc = 0.0532 Mpc/h (`gas`), floored at 1e-6.
  Optical depth by the fluctuating Gunn-Peterson approximation tau = A rho^beta, beta = 2 - 0.7 (gamma - 1), gamma 1.5,
  with thermal broadening by a Gaussian of Doppler b = 12.85 km/s sqrt(T/1e4 K), T = T0 rho^(gamma - 1), T0 = 1e4 K, in
  12 classes of log b (`tau_field`). A is tuned so the box-mean flux equals exp(-tau_eff(z)),
  tau_eff = 0.751 ((1 + z) / 4.5)^2.90 - 0.132 (`tune_A`, `flux_p1d`).
- **Real space.** `flux_p1d` calls `tau_field` with `vlos=None`: no peculiar velocities, no redshift-space shift.
- **Statistic stored.** p(k_v) = mean over all 384^2 sightlines along axis 2 of |FFT(delta_F)|^2 dv / N, with
  delta_F = F / <F> - 1 (the flux contrast normalised by the box mean). Units km/s. k_v = 2 pi rfftfreq(N, dv) in s/km
  (angular, the same convention as DESI's K). dv = 100 E(z) / (1 + z) dx km/s per cell with the record's Omega_m, so
  the velocity mapping uses the box's own H(z); no extra conversion is applied to the data's s/km. 193 values per part,
  index 0 is k = 0. No pixel window, resolution or noise term (DESI's P1D is already corrected for those).
- **Box coverage.** Box 20 Mpc/h, N 384. Fundamental k_v[1] and Nyquist k_v[192] (s/km) against the data's k range:

| z | points | data k min / max | k_f (box) | k_Nyq (box) | points below k_f |
|---|---|---|---|---|---|
| 2.2 | 49 | 0.00125 / 0.02525 | 0.00304 | 0.583 | 4 |
| 2.4 | 52 | 0.00125 / 0.02675 | 0.00296 | 0.568 | 4 |
| 2.6 | 55 | 0.00125 / 0.02825 | 0.00289 | 0.555 | 4 |
| 2.8 | 58 | 0.00125 / 0.02975 | 0.00282 | 0.542 | 4 |
| 3.0 | 61 | 0.00125 / 0.03178 | 0.00276 | 0.529 | 4 |
| 3.2 | 63 | 0.00125 / 0.03328 | 0.00270 | 0.518 | 3 |
| 3.4 | 65 | 0.00125 / 0.03485 | 0.00264 | 0.507 | 3 |
| 3.6 | 67 | 0.00125 / 0.03649 | 0.00259 | 0.497 | 3 |
| 3.8 | 69 | 0.00125 / 0.03821 | 0.00253 | 0.487 | 3 |
| 4.0 | 70 | 0.00125 / 0.03910 | 0.00249 | 0.477 | 3 |
| 4.2 | 72 | 0.00125 / 0.04094 | 0.00244 | 0.469 | 3 |
| 4.4 | 74 | 0.00125 / 0.04287 | 0.00240 | 0.460 | 3 |

  41 points lie below the fundamental; none lies above the Nyquist mode (the data stop near 0.04 s/km). The k_v grid is
  the same on both footings.
- **How the graders treat them.** `at_points` interpolates the ratio R = (seed sum of case) / (seed sum of R) linearly
  in ln k from k_v[1] upward with `np.interp`, so below k_f the ratio is held at its k_v[1] value. Every one of the 755
  points enters the gate's d = (r - 1) x P_data.

## 2. Construction of the absolute model P1D at the data points

- Reference = case "R" (the reference layout), primary gas, build B.
- Parts: `closure_2026_11_14/FWN2_forest_flux_split_f4/parts_b/prim_z<z>_s<s>_<footing>.json`, seeds 0 to 3, all 12
  bins; P_ref,box(k_v) = mean of the four seeds' `flux.primary.R.p` (the same seeds and the same sum the grader uses).
- At a data point with k >= k_v[1]: ln P interpolated linearly in ln k between neighbouring box modes.
- **Points used in the absolute fit: the 714 points with k >= k_f** (the 41 below the fundamental are left out, since
  the box holds no mode there). The covariance used is the 714 x 714 block of the data covariance (rebuilt from the
  loader's Cholesky factor, as the graders do).
- For the gate re-evaluation (all 755 points must enter, as in the gate): below k_f the model is held at its k_v[1]
  value (the same flat hold the grader applies to r). Variant reported: P_data at those 41 points instead.
- Variants reported, never the word: (v1) all 755 points with the held model; (v2) the 714 points with the four-seed
  scatter of the mean added to the diagonal (model sample variance); (v3) only points with k >= 3 k_f.

## 3. Statistics

All with the data covariance C (full, cross-z kept unless a bin is named). Per bin = that bin's block alone; total =
the full block over all used points.

- chi2_abs,0 = (m - P)^T C^-1 (m - P), m the model, no nuisance. dof = N_used.
- chi2_abs,A: m_j -> A_j m_j, one free amplitude per bin (12 in all), solved jointly by generalised least squares
  (linear, closed form). dof = N_used - 12. Per-bin figures: the bin alone with its own A_j.
- chi2_abs,AT: m_j -> A_j (k / 0.01 s/km)^alpha_j m_j, per bin, the amplitude and tilt of FRZ5's template (FRZ5
  FROZEN_CRITERIA section 2, after P1D3), alpha_j in [-1, 1] as FRZ5 (primary); unbounded reported beside. FRZ5's third
  term (pressure smoothing on the linear-matter P1D integral) is not reused: it is defined on a quantity this box does
  not use; the frozen gas brackets take its place. Minimiser: scipy `least_squares` (trf) on the whitened residual,
  starts at (A from the amplitude fit, alpha 0) and at alpha = +/-0.5; lowest kept. dof = N_used - 24.
- **Brackets at the anchors** (z 2.2, 3.0, 4.4; seeds 0 and 1, `parts_b/br_z<z>_s<s>_<tag>_<footing>.json`, case R):
  chi2_abs,0 / ,A / ,AT on the anchors' covered points (anchor block of C) for each of the eight tags lam_x0.5, lam_x2,
  gam_1.2, gam_1.6, tau_x0.9, tau_x1.1, lam_91.4, lam_138.6, beside the primary at the same two seeds. Reported.
- Reported beside: m / P_data per bin at k = 0.003, 0.01, 0.02 s/km and at the bin's top k; fitted A_j and alpha_j.

## 4. The re-evaluated gate

- d' = (r - 1) x P_ref,model at all 755 points, r exactly as the grader builds it (ratio of four-seed sums, `at_points`);
  D' = d'^T C^-1 d' (`cho_solve` form, as `dchi2`). SE' by the grader's jackknife over seeds with P_ref,model held at
  the four-seed mean; D_noise' (KA-S) as the grader with P_ref,model.
- Cases: from `parts_b`: J3.5, J4, J4.5, J5, U4; from `FWN1R_blind_split_f_ceiling/parts`: J3, J5, J10, Jinf, C.
- **Graded set** (labels re-read with D', SE'): J3.5, J4, J4.5 (stored labels in `fwn2b_grade.json`) and J5, J10, Jinf
  (stored labels in `fwn1r_grade.json`). Label rule unchanged: HOLDS if (stored known answers and twins pass, KA-S' pass,
  KA-M stored pass) and D' + 2 SE' < 4; FAILS if D' - 2 SE' > 4; else NO VERDICT. Only the base word (before
  ", FRAGILE") is compared. J3, C, U4 reported.
- Reported beside: D' / D per case; per-bin D'; the ceiling on f (log-linear crossing of D' + 2 SE', D', D' - 2 SE' = 4
  over f 3, 3.5, 4, 4.5, 5, 10); the bracket estimates D' A'_b / A'_p; the variant with P_data at the 41 uncovered
  points; and the variant d'' = (r - 1) x A_j m (the amplitude-refit model).

## 5. Known answers (all must pass before any new number is read; a failure gives NOT EVALUABLE for what it feeds)

- KA1 the loader returns 755 points and md5 33d7fc21bfd3d745ed71a0bbe80ca433.
- KA2 my code, with P_data as the scale, reproduces the stored D of every case listed in section 4 from the parts to
  1e-6 relative (in particular J4 3.178 / 3.712 and J5 8.834 / 10.897 against `fwn2b_grade.json`, and J3, J5, J10, Jinf,
  C against `fwn1r_grade.json`), and the stored SE to 1e-6 relative.
- KA3 the data fed as the model gives chi2_abs,0 = 0 (<= 1e-20 absolute) and amplitudes 1, tilts 0 to 1e-8.
- KA4 mean flux: every stored field (primary and brackets, both part folders) has |meanF - target| <= 1e-4, and the
  target equals exp(-s tau_eff(z)) recomputed by me to 1e-12 relative.
- KA5 the reference R in `parts_b` equals R in FWN1R's `parts` in all 48 files per footing (max relative deviation
  <= 1e-12), so both part folders share one reference.

## 6. Twins and mutations (must bite; `*_MUTATE.*` outputs)

- TW1 model x 1.2: chi2_abs,0 must rise by exactly 0.44 m^T C^-1 m - 0.4 m^T C^-1 P (computed by a second path,
  `np.linalg.solve`, to 1e-8 relative); and on the data as model it must equal 0.04 P^T C^-1 P.
- TW2 the amplitude nuisance on 1.2 x model must return chi2_abs,A of the unscaled model to 1e-8 relative, with every
  A_j divided by 1.2 to 1e-8; on 1.2 x data it must return 0.
- TW3 model x (k / 0.01)^0.1 in every bin: chi2_abs,AT must return the unscaled value to 1e-6 relative.
- TW4 gate scale 1.2 x P_data: D' must equal 1.44 x D to 1e-10 relative for every case.
- A twin that does not bite gives NOT EVALUABLE for what it feeds.

## 7. Words and lines (per footing)

Fit word (N = 714 used points):
- **REFERENCE FITS IN ABSOLUTE TERMS** if chi2_abs,0 <= N + 3 sqrt(2 N) = 714 + 113.4 = 827.4.
- **FITS ONLY WITH NUISANCE** if not, but chi2_abs,AT (bounded tilt) <= (N - 24) + 3 sqrt(2 (N - 24)) = 690 + 111.4 =
  801.4.
- **DOES NOT FIT** otherwise.
- Reason: a model that reproduces the data within their stated errors gives chi2 near the number of points; 3 sigma of
  the chi-squared distribution is the usual line. The gate's premise is that the reference reproduces the data, so this
  is the line that premise must meet. The amplitude-only figure and the brackets are reported, not part of the word.

Gate word:
- **GATE UNCHANGED BY THE ABSOLUTE LEVEL** if all six graded base labels (J3.5, J4, J4.5, J5, J10, Jinf) are the same
  with D', SE' as stored.
- **GATE MOVES: a frozen label of FWN2 would change sides** if any of them differs (named, with D', SE').
- **NOT EVALUABLE** if a known answer fails, a gate twin (TW4) does not bite, or P_ref,model <= 0 at any point.
- Reason: the brief asks whether the unchecked step matters for the record's words; the labels are the record's words.
  Note frozen in advance: J4 alt sits 0.035 above its HOLDS line, so a scale lower by 0.4 % at the points that drive D
  flips it to HOLDS. The result file will therefore also say, for every moved label, how large a scale change moves it,
  and whether any label crosses from HOLDS to FAILS or back (the stronger reading, reported).

## 8. Hand estimate (before any number)

- The box is a 20 Mpc/h, N 384, real-space fluctuating Gunn-Peterson box on a halo-model / lognormal density, not a
  hydrodynamic simulation. Without peculiar velocities the large-scale flux power lacks the redshift-space boost (for the
  forest this boost is large: a factor of order 1.3 to 2 in P1D at low k), and the box lacks every transverse mode
  longer than 20 Mpc/h, which also feeds low-k P1D. At high k, real space lacks the velocity-gradient smoothing, so the
  small-scale power is likely too HIGH, unless the 79 kpc smoothing and the thermal broadening overdo it.
- Expectation: m / P_data low by 20 to 50 % near k_f, and off by 10 to 50 % (sign uncertain, more likely high) at the
  top k; the error grows towards z 2.2 where DESI's errors are smallest.
- chi2_abs,0 total: above 10^4 (70 %); 10^3 to 10^4 (20 %); below 10^3 (10 %). chi2_abs,A: falls by a factor 3 to 10,
  stays well above 800 (75 %). chi2_abs,AT: still above 801 (70 %).
- Fit word: DOES NOT FIT 80 %; FITS ONLY WITH NUISANCE 15 %; FITS IN ABSOLUTE TERMS 5 %.
- Gate: D' / D is about (m / P_data)^2 weighted to z 2.2 to 2.6 and k 0.01 to 0.025, where r - 1 is largest. Central
  guess D' / D = 1.2, range 0.6 to 2.3. GATE MOVES 80 % (J4 alt alone moves for any factor outside 0.996 to 1.086;
  J4 canonical moves to NO VERDICT for a factor above 1.07 in amplitude); GATE UNCHANGED 17 %; NOT EVALUABLE 3 %.
  A HOLDS-to-FAILS or FAILS-to-HOLDS crossing: 30 %.
- Twin TW1 on the data as model: P^T C^-1 P is the data's total signal-to-noise squared; with errors of 1 to 5 % per
  point, 10^5 to 10^6, so the shift is about 4 x 10^3 to 4 x 10^4.

## 9. What the lane cannot say

- It tests the gate's model, not the framework. A misfit of the reference is a property of a 20 Mpc/h real-space
  fluctuating Gunn-Peterson box with fixed, provisional gas parameters; it is not evidence for or against any layout,
  for or against the framework, or for or against Lambda-CDM.
- It computes no new forest field. Redshift-space distortions, larger boxes, other seeds, T0 brackets, and metal or DLA
  contamination of the data are not covered. A fit with nuisance is not a fit of a physical model.
- Moving a gate number here does not relabel any record lane; it says whether the record's labels depend on the
  unchecked step.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
