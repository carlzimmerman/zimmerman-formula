# AGB4R — blind re-grade of AGB4: my reading of the frozen rules (committed alone, before any magnitude is fitted against any age)

2026-11-14. Second, independent implementation of lane AGB4 (the progenitor-age slope of Son et al.,
arXiv:2510.13121, tested on published SDSS-II host ages and Pantheon+ magnitudes).

## What I read
- `closure_2026_11_14/AGB4_measured_host_ages/FROZEN_CRITERIA.md` (the only file of AGB4 opened).
- `closure_2026_11_14/AGB2_host_mass_step_redshift/AMENDMENT_1.md` (the weighting rule the criteria cite).
- `closure_2026_11_13/AGB1_progenitor_age_bias/FROZEN_CRITERIA.md`, the W1 block only, because the AGB4 criteria
  name AGB1's W1 words without their thresholds. Nothing else of AGB1 to AGB7 (no README, script, output, result,
  lead check or post hoc file) was opened. No `git show` or `git log -p` of any AGB commit.
- A hand-over note of the AGB1 blind re-grade in the group's shared notes folder (outside the repository). It names
  only AGB1's words; nothing about AGB4.
- The method of the reliability row as spelled out in the brief that started this session.

## What had been seen when this file was written
Data headers and the design only: the match counts, sample sizes, redshift ranges, mass and age shares, and the
design-only errors of the amplitude (no magnitude enters them). No magnitude has been fitted against any age, and no
magnitude column has been printed.

Design numbers reproduced before any fit (criteria value in brackets):
- 321 Pantheon+ rows with IDSURVEY 1, all 321 found by SDSS id in the Sako table [321].
- `pp`: 288 matched rows have an FSPS age; 286 have a positive lower bound (the other two carry −99) [286];
  zHD 0.0665 to 0.3799 [0.07–0.38]; 32.2 % with Pantheon+ log M < 10 [32 %]; 86 above 6 Gyr, 14 above 8 [86, 14].
- `rose`: 66 of `pp` have an entry in Rose et al.'s `results-summary.csv` (103 hosts) [66].
- `big`: 1,092 objects, 387 typed SNIa [1,092; 387] — reproduced only when the positive lower age bound is also
  required of `big` and the redshift cut uses `z_best_with_BOSS_CMB` (see A3).
- Design-only σ_A (weighted least squares, weights fixed, no data values): `pp` reading R 0.194 (M0) and 0.210 (M1)
  [0.19, 0.21]; Rose global 0.243 and local 0.252 (M0) [0.24, 0.25]; reading P 0.168 / 0.189; 12 bins 0.195 / 0.211;
  `big` 0.174 / 0.199.

## The model, as I read it
y_i = Σ_b o_b [z_i in bin b] + g (L_i − ½) + A D_i + a x1_i + b c_i, D_i = −0.030 mag/Gyr × age_i.
- One offset per redshift bin and no global intercept. g only in M1. a, b only in reading R and in `big`.
- **Weights**: diagonal, w_i = 1/C_ii of `PantheonPlusSH0ES_STAT+SYS.cov` (`pp`, `rose`); 1/(muerr² + 0.1²) for
  `big`, muerr of the table's first (spectroscopic-redshift) SALT2 block. Parameter errors from the plain
  weighted-least-squares formula (XᵀWX)⁻¹, **not** rescaled by χ²/dof (AGB2 amendment 1: "the
  weighted-least-squares formula"). χ²/dof is printed beside each fit.
- **Δχ²(A=k)** = χ² refitted with A fixed at k (all other parameters free) minus χ²_min. For a linear fit with fixed
  weights it equals ((Â − k)/σ_A)²; both are computed and must agree.
- **μ_fid**: flat ΛCDM, Ω_m = 0.334, D_L = (1 + z_hel) D_C(z_HD) (the Pantheon+ convention); H0 = 70 (absorbed by the
  bin offsets). `pp`/`rose`: zHD and zHEL of Pantheon+. `big`: `z_best_with_BOSS_CMB` and `..._HELIO`.
- **Readings**: R: y = mB − μ_fid, a and b free, x1 and c from Pantheon+. P: y = m_b_corr − μ_fid, no a, b.
  `big`: y = −2.5 log₁₀ x0 − μ_fid, a, b free, x1 and c from the table's first SALT2 block.
- **L_i** = 1 if log M < 10: Pantheon+ HOST_LOGMASS for `pp` and `rose`, `logMass_Ravi` for `big`.
- **Ages**: FSPS `age_Ravi` (Gyr) for the words; `age_Mat` (PEGASE) for its reported row; Rose `Global age` and
  `Local age` from `results-summary.csv` for the Rose rows.

## Ambiguities and how I resolved them (fixed now, before any fit)
- **A1, equal-count bins.** Sort by the sample's redshift (zHD for `pp`/`rose`, CMB-frame table redshift for `big`),
  ties broken by SDSS id; bin = floor(rank × n_bins / N). Sizes differ by at most one. Bins are recomputed for every
  sample and every fork (so the "without wide intervals" fork has its own 8 bins).
- **A2, the match.** Pantheon+ CID (IDSURVEY 1) read as an integer and matched to `cid` of the Sako table. K1's
  "table redshift" is `z_best_with_BOSS_CMB` (zHD is CMB-frame); the heliocentric difference is printed too.
  The K1 correlation is Pearson's r over the 286 rows of `pp`.
- **A3, `big`.** The criteria list "with an FSPS age" for `big` without the positive lower bound stated for `pp`.
  Without it the count is 1,095 (389 spectroscopic); with it, 1,092 (387), the frozen count. I require it (the −99
  lower bound flags a failed host fit). "Typed SNIa or zSNIa" = `type_dr` exactly `SNIa` or `zSNIa` ("SNIa?" and
  `pSNIa` excluded). "Spectroscopic" = `type_dr` == `SNIa`. Redshift cut 0.03 < z_CMB < 0.45 (strict).
- **A4, the "wide interval" fork.** `age_lo_Ravi` and `age_hi_Ravi` are bounds, not errors (lo ≤ age ≤ hi in all 286
  rows). "Stated age interval wider than ± 2.5 Gyr" is read as **(age_hi − age_lo)/2 > 2.5 Gyr**, i.e. the full
  interval wider than 5 Gyr: 8 hosts removed, 278 left. The other possible reading, either side longer than 2.5 Gyr
  (38 removed), is run and reported as a reading only; it does not enter the second word.
- **A5, the forks.** One change at a time from the primary (`pp`, reading R, FSPS, 8 bins): (i) reading P; (ii) 12
  bins; (iii) `big` as the criteria define it (its own y, weights, 16 bins, FSPS mass for L, a and b free); (iv) `pp`
  without the 8 wide-interval hosts. Each fork's first word is judged by the same rule as the word it tests (U words
  for M0, W1 words for M1). ROBUST if all four forks give the primary's first word; else FRAGILE, naming each fork
  that differs. The forks do not need their own K4.
- **A6, the words.** M0 (g = 0), AGB3's U words exactly as the AGB4 criteria spell them, on Â and Δχ²(A=1). M1
  (g free), AGB1's W1 words: EXCLUDED AT 3 SIGMA if Δχ²(1) ≥ 9 and Δχ²(0) < 4; DISFAVOURED if 4 ≤ Δχ²(1) < 9 and
  Δχ²(0) < 4; REQUIRED AT 3 SIGMA if Δχ²(0) ≥ 9 and Δχ²(1) < 4; FAVOURED if 4 ≤ Δχ²(0) < 9 and Δχ²(1) < 4;
  UNDECIDED if both < 4; NEITHER if both ≥ 4 (each prefixed "AGE BIAS").
- **A7, K2.** Stretch = Pantheon+ x1 (the stretch of the `pp` fit); low stretch = x1 < −1; old = age ≥ 6 Gyr; shares
  unweighted. The same with the Sako table's x1 is printed.
- **A8, K3.** Twin y = o_b + 0.05 (L − ½) [M1 only] − 0.15 x1 + 3.1 c + A_true D with o_b = −19.30 + 0.02 b. Eight
  twins: {`pp` reading R, `big`} × {M0, M1} × A_true ∈ {0, 1}, each fitted with the real weights. Pass each:
  |Â − A_true| ≤ 10⁻⁶ and χ²_min ≤ 10⁻⁸. The script exits 3 if all eight pass and 4 otherwise.
- **A9, K4.** For `pp` reading R, M0 and M1 separately. σ_A = the real fit's formula error. Shuffle: within each of
  the 8 bins the (FSPS age, L) pairs are permuted together among the supernovae (y, x1, c, weights stay); a fresh
  `numpy.random.default_rng(20261117)` per configuration, 400 draws, one permutation per bin per draw in bin order.
  Scatter = standard deviation (ddof = 1) of the 400 Â. Sandwich = HC0, (XᵀWX)⁻¹ [Σ w_i² r_i² x_i x_iᵀ] (XᵀWX)⁻¹,
  r from the real fit; one row per supernova, so clustering by supernova is the same as HC0. HC1 (× N/(N−p)) is
  printed beside it. Pass: |mean Â| ≤ 0.2 σ_A; scatter/σ_A and sandwich/σ_A both in [0.8, 1.25].
- **A10, KR.** `campbell_local.tsv`: `mu`, `err_mu`, `redshift`. Hubble line: flat ΛCDM Ω_m = 0.3,
  D_L = (1 + z) D_C(z) with the one redshift given; residual = mu − μ_line (the constant offset cancels in the
  difference). Ages: `Local age` of `results-summary.csv`, joined by SN id. Younger: local age < 8 Gyr; older:
  ≥ 8 Gyr (an age of exactly 8.0 counts as older). Step = mean residual (younger) − mean residual (older), means
  **weighted by 1/err_mu²** (primary); the unweighted step and the step from the file's own `hr` column are printed.
  Pass: |step − 0.114| ≤ 0.04. A failed KR makes only the Rose rows NOT EVALUABLE.
- **A11, the gates.** M0 and M1 are NOT EVALUABLE if K1, K2 or K3 fails. A K4 failure removes the word of that
  configuration (M0 or M1) only. Numbers are printed in every case.
- **A12, reported rows (no words).** All on `pp` reading R unless stated, M0 and M1 each:
  Rose global and local ages on `rose` (4 bins; reading P also printed); PEGASE ages; `big` restricted to its 387
  spectroscopic objects (16 bins, as `big`); the template split at 6 Gyr, read two ways — (a, primary) a continuous
  hinge, D_lo = −0.030 min(age, 6), D_hi = −0.030 max(age − 6, 0), giving the slope amplitude below and above 6 Gyr;
  (b) two pieces, D [age < 6] and D [age ≥ 6]; the low-stretch share (x1 < −1) in age bins < 2, 2–4, 4–6, 6–8,
  8–14 Gyr; the reliability row (A13); every fork's numbers; the either-side reading of A4.
- **A13, reliability.** Inside the 8 bins of the primary fit, with the fit's weights: each variable demeaned by its
  bin's weighted mean; weighted (co)variances over all rows with denominator Σw. W = FSPS age, Z1 = Pantheon+ x1,
  Z2 = Pantheon+ HOST_LOGMASS (the mass of the fit). Shared = cov(W,Z1) cov(W,Z2)/cov(Z1,Z2); reliability =
  shared/var(W); noise = var(W) − shared. In a fit: var_left = Σ w r_W²/Σ w, r_W the weighted residual of W after
  the fit's other columns; reliability_fit = 1 − noise/var_left; corrected amplitude Â/reliability_fit with error
  σ_A/reliability_fit (the reliability treated as fixed). The same with FSPS mass as Z2 is printed (that mass comes
  from the same photometric fit as the age, so its errors may be shared with the age's).

## Files
`agb4r_data.py` (loaders, match, μ_fid, bins), `agb4r_run.py` (checks and fits, one JSON and one log per mode),
`RESULT_BLIND.md`. This file is committed alone first.

kappa = 1/2 FITTED; not theory closed.
