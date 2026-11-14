# AGB3R — blind re-grade of AGB3: my reading of the frozen rules (written before any magnitude is fitted)

2026-11-14. Second, independent implementation of lane AGB3 (`closure_2026_11_14/AGB3_des_host_star_formation/`),
written from that lane's `FROZEN_CRITERIA.md` alone. Of AGB3's folder I have read only that file. I have not opened
its README, scripts or outputs, nor AGB1's or AGB2's README or collect outputs, nor the memory note on these lanes.

## What I read besides AGB3's criteria, and why
- AGB1's `agb1_run.py` and `agb1_template.py` (imported unchanged for Parts S, J, E and KS), and AGB1's
  `FROZEN_CRITERIA.md`, which holds the W1, W2 and W3 rules that AGB3's words cite by name.
- AGB2's `agb2_galaxy.py` (imported unchanged: t(z), mass-loss law, delay-time distributions, mass-only ages),
  `agb2_joint.py` (only the function `joint` is used), and AGB2's `FROZEN_CRITERIA.md` and `AMENDMENT_1.md`, which
  define the "run" and "mass" templates, the H1/H2 fits and "amendment 1" (diagonal weights, sandwich error) that
  AGB3 cites. These are rule files; they carry AGB2's check numbers but no AGB2 amplitude.
- Later, for KS only: AGB1's `agb1_A_full.json` and `agb1_A_des_only.json`; for D1 only: the amplitude and error of
  `fits.sample_drop_DES.H1` in AGB2's `agb2_H_diag.json`.
- Before writing this file I ran, on no magnitude: the two-component model against the criteria's printed age table,
  and a listing of the host columns (ranges and counts). The counts reproduce the criteria exactly: 1,820 rows;
  `des_only` 1,623 (532 low-mass); `full` low-mass 594; `pure` 1,498 (472 low-mass); `young` 609 (586 DES); blue
  (colour ≤ 0.8) 733; log s ≥ −10: 1,145. (CID, IDSURVEY) is unique; no host column carries a fill value; 103 hosts
  have log s < −13 and 22 have log s > −8 (clipped by the model).

## The two-component model (ambiguities and how I resolved them)
1. **T_c, the duration of the constant part, is not stated.** I read it as "since the burst": T_c = T_f = t(z) − t(z_f)
   unless the surviving constant part alone exceeds the mass, in which case T_c is shortened until it gives the mass
   and there is no burst. This reproduces the criteria's printed table (27 entries, z 0.05 / 0.5 / 1.0, log s −13 … −8)
   to 0.005 Gyr, i.e. to its rounding; so the reading is confirmed by the criteria's own numbers.
2. Supernova weights: the constant part contributes SFR × Φ(τ) with SFR = s × M (the observed rate, formed mass, not
   surviving mass); the burst contributes M_b × Φ(T_f), with M_b the formed burst mass, so M_b(1 − f_ml(T_f)) is what
   survives. The mean age is the Φ-weighted mean over both parts. Integrals are cumulative trapezoids on a 10⁻⁴ Gyr grid.
3. t(z): AGB2's flat Ω_m 0.30, H0 70 closed form. Mass loss f_ml and the Childress delay-time distribution: AGB2's
   functions, imported. Short-delay fork: AGB2's power law (slope −1.13 from 40 Myr).
4. Host ages are evaluated at the supernova's zHD (the redshift used for binning and for the distance).
5. KM (iii): AGB2's own model tracks with 9 ≤ log M ≤ 11.5 at z 0.05 and 0.5; s = (mass formed in the last 4 Myr step
   / step) / stellar mass; compared with the same track's mean age from AGB2's `ages_at`. Pass if every |difference|
   ≤ 1.5 Gyr. KM (ii): s chosen so that T_c = 6 Gyr exactly (pure constant star formation over 6 Gyr, at z 0.05), model
   against `scipy.integrate.quad` of τΦ/Φ over [0, 6]; pass within 0.001 Gyr. KM (i): log s = −13 at z 0.05 against
   T_f(0.05); pass within 2 %.

## Part D
- Weighted least squares with weights 1/MUERR_RENORM² (all readings), parameter errors from the unscaled formula
  (XᵀWX)⁻¹ (AGB2 amendment 1: "the weighted-least-squares formula"). The model is linear, so
  Δχ²(A = a) = (Â − a)²/σ_A².
- Bins: 20 (or 40) equal-count bins in zHD of the sample in use, by rank: bin = ⌊N_bins × rank/n⌋ (stable sort).
- μ_fid = 5 log₁₀[(1 + zHEL) D_M(zHD)] for flat Ω_m 0.330 (AGB2's form; any smooth error goes into the bin offsets).
- L_i = 1 if HOST_LOGMASS < 10. Readings R, P, B exactly as written (R: x1 and c as free regressors).
- Templates: sfr D = −0.030 × two-component age; mass D = −0.030 × AGB2 mean age(log M, zHD); run
  D = 0.030 × Δτ(zHD) × (L − ½), Δτ(z) = mean over the sample's high-mass hosts of the AGB2 mean age at z minus the mean
  over its low-mass hosts, on a 0.01 grid in z, linear between grid points.
- **Half template**: amplitude 2Â with error 2σ, for every word that uses it (D2's fork, U's fork, J's prior 2Â ± 2σ);
  U's rule "Â < 1" is then applied to 2Â.
- D2 forks, one at a time from the primary (`des_only`, R, 20 bins, z_f 3): reading P; `full`; 40 bins; `pure`;
  z_f 2; z_f 5; half template. U forks: the same with reading B in the place of P, plus mass-only ages.
- U: g fixed at 0, reading R. The four U words partition the plane as written (Â = 1 exactly with Δχ² ≥ 4 cannot occur).
- K2: reading B, `full`, 20 bins, y = Σ o_b + g (L − ½); pass if |g − 0.033| ≤ 0.016 (sign: low-mass hosts fainter is g > 0).
- K3: on `des_only` (20 bins), y = o_b (fixed values 0.10 + 0.01 b) + 0.05 (L − ½) where the step is free
  (D1, D2; not U) + (−0.15 x1 + 3.1 c in reading R) + A_true × D; A_true 1 and 0; D1, D2, U × R, P: twelve twins.
  Pass each: |Â − A_true| ≤ 10⁻⁶ and χ²_min ≤ 10⁻⁸. Exit 3 if all pass, 4 otherwise.
- K4: `des_only`, reading R, D1, D2, U. 400 draws from numpy `default_rng(20261115)`; in each draw one permutation of
  the host rows (log M, log s, colour moved together) inside each of the 20 bins, the same permutation used for all
  three configurations; templates recomputed at each supernova's own zHD (Δτ(z) of D1 is unchanged by a permutation).
  Pass each configuration: |mean Â| ≤ 0.2 σ_A; shuffle scatter / σ_A in [0.8, 1.25]; HC0 sandwich error from the real
  fit's residuals / σ_A in [0.8, 1.25] (one row per supernova, so clustering by CID is the HC0 form).
- Reported rows: D1 (`des_only` and `full`) and its inverse-variance combination with AGB2's `sample_drop_DES` H1;
  H2 on this sample (mass template, step free, R, `des_only`); band steps on `full` (one fit per split and reading, five
  band-steps g_band × [z in band] × (S − ½) with the 20 bin offsets and, in R, x1 and c; S = 1 on the side the model
  calls young: log M < 10, log s ≥ −10, colour ≤ 1.0), beside 0.030 × (mean two-component age of the old side − of the
  young side) in that band; D2 with the short-delay distribution; D2 on `full` in reading P.

## Part S
- T_H(z) = 0.030 × [ā_1 − ā(z)], ā(z) linear in the 20 bin means (z̄_b, ā_b) of the sample's host ages, flat outside;
  evaluated at the distance file's zHD. Host properties are joined to the distance file by (CID, IDSURVEY).
- AGB1's `SN`, `BAO("all")`, `Fitter("A")` unchanged; the template enters through `SN.add_template`. Fits and forks
  exactly as AGB1's `run_block` builds them: base fit, q0 = 0 fit started also from the base, never-accelerated fit
  started also from the q0 = 0 and base fits, base re-fitted if a constrained fit beats it.
- S2 / S3 on `full` at A_H = 1 by W2 / W3. S2's forks: `des_only` with its own T_H; T_H from mass-only ages; z_f 2;
  z_f 5 (each on `full` at A_H = 1 unless named). S3 printed for the same forks.
- Reported: A_H free with Δχ² at 0 and 1 (from the profile, as AGB1's `run_block`); host by host: the vector
  0.030 × (ā_1 − age_i) per supernova in the place of the smooth curve, A_H = 1 forks and A_H free.
- KS: Δχ²_today and Δχ²_never of my A_H = 0 fits (`full`, `des_only`) and of AGB1's T_S at coefficient 1 must equal
  AGB1's committed forks A0 and A1 to 0.01.

## Part J
- f, t on −1.0 … 2.0 step 0.1 and n on step 0.25, per configuration, warm-started as AGB2's `agb2_joint.py` main does
  (AGB1's fixed starts plus the neighbouring point; t from the f point and the previous t; n from the nearest t, f and
  the previous n; f lowered if a q0 = 0 fit beats it). Arithmetic by `agb2_joint.joint`, unchanged.
- J2 (W2 with q0 of the free fit at the joint best A_H, Δχ²_today from `joint`) and J3 (W3 on Δχ²_never), judged on
  `full` with D2's primary (Â, σ) as the prior. J2's forks: `des_only` distances with its own T_H; prior from D2 in
  reading P; prior 2Â ± 2σ; T_H from mass-only ages (prior unchanged); prior from U's primary (Â, σ).

## Part E
- AGB1's Part A model (DESI BAO + the selected supernovae; covariance sub-block by inverting, taking the block and
  inverting, as AGB1's `SN` does), published moduli, no age term: free, q0 = 0, q ≥ 0. I read "on these supernovae
  alone" as "with only these supernovae"; the BAO stay in (it is Part A's model). As an unlabelled extra I also print
  the same subsample with no BAO.
- E2 / E3 on `young` (log s ≥ −9.5, 609); E2's forks: blue (colour ≤ 0.8, 733) and log s ≥ −10 (1,145). Reported:
  the complement (log s < −9.5, 1,211) and the young DES supernovae alone (586).

## Gates
Part D NOT EVALUABLE if KM, K1, K2, K3 or K4 fails (K4 per configuration). Parts S and E NOT EVALUABLE if KM, K1 or KS
fails. Part J needs D2 and Part S. Numbers are reported either way.

kappa = 1/2 FITTED; not theory closed.
