# F1A frozen criteria: an independent audit of fact F1 (the primary CMB needs a cold component of ~5.56 x baryons; baryons-only fails; the khronon clock cannot cluster)

Frozen and committed alone, before any F1A script or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts
nothing. Audit lane (cold dark energy; no particle). Footings graded separately, never pooled: canonical a0
9.3603e-11, alt 1.1312e-10. One thread, < 1 GB, no download. Lane id: no F1A in `ls` or `git log`.

## Known before this freeze (not blind)

- QX15's labels and numbers: L1 PASS (PA chi2 3741.08 / 3741.15, Delta -64.7 vs its chi2_cal 3805.80); MB
  (baryons-only) Delta +172,848 / +166,612 with n_s on the 1.3 bracket edge; best fits omega_b 0.02236, omega_d 0.1209,
  h 0.674 on both footings; ACT KA 790.96.
- QX3 iter1's no-go (C1 Lean bound k_J^2 = 4 pi G rho_phi <= (3/2) H^2 for c_s^2 = 1; C2 max (k_J/k)^2 = 0.0065).
- One timing number: CLASS at l_max 7000 with lensing takes about 0.6 s on this machine.
- Step 2 is already read (below), because it decides which code this lane may not touch.

## Step 2 (reading, done before freezing; restated in RESULT)

- QX15's graded L1 and MB paths are qx15.py + qx15_like.py with CAMB. They import nothing from QX3 or QX10.
- QX15's cell path (do_cells: C1-C4 Delta_cell and the P1 power control) execs QX10 iter_1's `jcheck`, which execs QX3
  iter3's solver and carries a copy of QX3 iter2's Limber weight, `w = ((chis-chi)/(chi chis))^2 (1+z)^2 / H`, then
  `/ chi^2` (no k^-4; GL2 confirmed this kernel is wrong). So the cell Delta_cell values and P1 sit on that kernel; F1
  (L1, MB) does not. GL1's statement is confirmed for the primary-CMB fits and corrected for the cells.

## Own code (f1a.py; imports nothing from QX3, QX10 or QX15)

- Theory: CLASS (classy 3.3.4; QX15 used CAMB), lensed TT/TE/EE in muK^2 D_ell, l_max_scalars 7000, linear lensing for
  every graded fit (consistent between cold and baryons-only); N_ur 3.046, no massive neutrinos, T_cmb 2.7255.
  Reported: the cold fit's chi2 with HMCode lensing.
- Likelihoods, written from the data files and the public format (the third-party Cobaya / ACT files on disk are read as
  documentation, not imported):
  - Pcut: Planck PR4 CamSpec NPIPE 12.6, spectra 143x143, 217x217, 143x217, TE, EE, cut at the P-ACT convention
    (TT L <= 1000, TE and EE L <= 600), power-law residual foregrounds amp_X (L/1500)^n_X (amp_100 = 0), calibrations
    A_planck^2 (TT), calTE A_planck^2, calEE A_planck^2. Covariance sub-block of like_NPIPE_12.6_unified_cov.bin.
  - A: ACT DR6 CMB-only (dr6_data_cmbonly.fits, SACC read by hand with astropy), L 600-6500, A_act, P_act.
  - PA = Pcut + A. Nuisances profiled at every theory point (amps in [0, 50], tilts in [0, 5], A_act in [0.5, 1.5],
    P_act in [0.9, 1.1]), with the Gaussian calibration priors A_planck N(1, 0.0025), calTE N(1, 0.01), calEE
    N(1, 0.01) added to chi2.
- Fits: Nelder-Mead from two starts, at most 300 evaluations each, tau in [0.01, 0.15], n_s in [0.80, 1.30].

## Backgrounds

- **B1, the record background (as GL2):** omega_b 0.0215, H0 65, n_s 0.95 fixed; free omega_d, ln(1e10 A_s), tau. a0 does
  not enter it, so both footings get the same numbers; each is graded and reported separately.
- **B2, the footing background (QX10's frozen rule, written independently):** w = 4 a0^2 / (G c^2 rho_c100). Canonical
  h^2 = w + omega_b + omega_d + omega_r. Alt h^2 = w, omega_DE = w - omega_m. Free omega_b in [0.0215, 0.0230], omega_d,
  ln(1e10 A_s), n_s, tau.
- **Baryons-only (MB):** the same, with omega_cdm = 1e-7 (and omega_d = 0 in the footing rule).

## Graded quantities (per footing)

- **G1 (baryons-only fails):** DeltaMB = chi2_MB(PA) - chi2_cold(PA) on B1 and on B2. It FAILS (the cold component is
  needed) if DeltaMB > 25 on both.
- **G2 (the cold fit is adequate):** Delta_cal = chi2_cold(PA, B2) - chi2_cal, where chi2_cal is my PA chi2 at the
  published Cobaya NPIPE test cosmology (nuisances profiled). Adequate if Delta_cal <= 9.
- **G3 (the amount):** R = omega_d / omega_b at the B2 best fit. It matches the record if |R / 5.562 - 1| <= 0.10.
  On B1, R is reported.
- **G4 (the clock cannot cluster): own linear perturbation code, CLASS-free.** Newtonian-gauge fluid equations
  (Ma & Bertschinger 1995) in conformal time, phi = psi, for radiation (w = c_s^2 = 1/3, a fluid), baryons (dust;
  the photon coupling is ignored, as a sign check only), the cold component (dust, c_s^2 = 0) and a field X with
  c_s^2 = 1, w_X constant. Adiabatic initial conditions at z = 1e6; integrate to z = 1100. Two X cases:
  - X1 (AC2q's clock): rho_X = rho_DE today (Omega_DE from B2 canonical), w_X = -0.95 (generous; w = -1 has no
    perturbation at all).
  - X2 (the needed amount, stiff): rho_X = the cold component's density, w_X = 0, c_s^2 = 1, replacing the cold dust.
  Statistic: Q_X = |delta rho_X| / |delta rho_dust,ref| at z = 1100, for k 0.02-0.3 /Mpc, where delta rho_dust,ref is the
  cold dust's in the run with dust. The no-go's sign is REPRODUCED if Q_X <= 0.05 for X1 and X2 at every k >= 0.05 /Mpc.
  The equation the no-go rests on is stated in RESULT (QX3 iter1 C1).

## Label for F1 (per footing; lane label needs both footings to agree)

- **CONFIRMED:** G1 FAILS on B1 and B2, G2 adequate, G3 matches, G4 REPRODUCED, and the step-2 reading holds.
- **REFUTED:** baryons-only does not fail (DeltaMB <= 25 on B2), or the cold fit is not adequate (Delta_cal > 25), or G4 has
  Q_X >= 0.5 for X1 (the clock clusters at the needed level).
- **WEAKENED:** anything else (for example G3 misses by more than 10 %, Delta_cal in (9, 25], or G4 between the lines).

## Known answers (must pass, else NO VERDICT)

- KA-A: my ACT chi2 at the ACT-lite test point (CAMB 1.6.6, lmax 9000, lens_potential_accuracy 8, min_l_logl_sampling
  6000, A_act = P_act = 1) is 790.96 within 1.0. CAMB is used here only, as the published test's theory.
- KA-P: my full CamSpec TTTEEE chi2 (published nuisances, no priors) at Cobaya's NPIPE test point with CAMB 1.6.6 at the
  same settings QX15 used for its frozen KA-P (lmax 9000, lpa 8, mead2020) equals QX15's 11321.74 within 1.0 (same theory,
  independent likelihood code). The full covariance is Cholesky-factored in float32 in place to stay under 1 GB; if that
  breaks the 1 GB rule or precision, KA-P is reported as not run and KA rests on KA-A.
- KA-G4: with X = dust (c_s^2 = 0, w = 0, the cold density), Q_X = 1 within 1e-3 (the code reproduces the cold dust).

## MUTATE (separate outputs)

- M1: the B2 baryons-only fit must fail (DeltaMB > 25). Its size is compared with QX15's +172,848 / +166,612: same order
  if the ratio is in [0.5, 2]. A ratio outside is disclosed as a discrepancy in the record's number, not in F1.
- M2: omega_b moved to 0.0300 at the B2 cold best fit, other parameters held: the first TT peak position must move, and
  chi2(PA) must rise by > 25. If M1 or M2 fails, the label is NO VERDICT.
