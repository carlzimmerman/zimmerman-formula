# QX10 iter_1 frozen criteria: primary CMB TT/TE/EE

Frozen before any iter_1 number. Kappa = 1/2 FITTED; not theory closed.

## Data (raw, on disk)

Planck PR3 (2018) CMB-only full spectra: COM_PowerSpect_CMB-TT-full_R3.01.txt (ell 2-2508),
COM_PowerSpect_CMB-TE-full_R3.01.txt and COM_PowerSpect_CMB-EE-full_R3.01.txt (ell 2-1996), under _external_data.
PR4 and ACT primary spectra are not on disk; downloading them needs the owner (NEEDS_OWNER.md). Error per ell: the mean
of the file's lower and upper errors. Diagonal, no covariance, no calibration or foreground nuisance (the CMB-only
spectra are already foreground-marginalised). This is a chi^2 against raw bandpowers, not the Planck likelihood.

## Model

CLASS (classy, as QX3) with lensed spectra (linear P, no halofit). The sector enters as pressureless matter
(omega_cdm = omega_d). That proxy is valid only if:
- J0: for every chosen cell, the comoving Jeans wavenumber a 2 pi / lambda_J(a) >= 50 Mpc^-1 at every z >= 10
  (100 x the largest primary-CMB k of about 0.5 Mpc^-1), evaluated on QX7's corner background;
- J1: the sector's late Jeans suppression of the lensing potential, S(L) from QX7's own G2' solver at that cell, changes
  the lensed TT by at most |1 - S(L)| x |C_TT,lensed - C_TT,unlensed|, and the implied Delta chi^2_TT <= 1.
If J0 or J1 fails for a cell, the proxy is invalid and iter_1 is NO VERDICT for that cell (a modified Boltzmann code is
needed).

## Framework-native background (stated; no LCDM parameter values as inputs)

Flat. rho_DE constant (a0 flat in z, the CFG689 prediction). The footing fixes the density through a0 = kappa c
sqrt(G rho) with kappa = 1/2 (FITTED), i.e. rho = 4 a0^2/(G c^2):
- canonical: rho = rho_DE, so omega_DE = 4 a0^2/(G c^2 rho_c,100); h^2 = omega_DE + omega_b + omega_d + omega_r;
- alt: rho = rho_total today, so h^2 = 4 a0^2/(G c^2 rho_c,100) is fixed and omega_DE = h^2 - omega_m - omega_r.
Disclosed now: the footings' a0 values were themselves built from the dark-energy and total densities (a0 = c H/Z), so the
background, and hence the acoustic angle, is not independent evidence. N_ur 3.046 massless, T_cmb 2.7255 (FIRAS), Y_He
from CLASS's BBN.

Fitted on the data (free in the framework): omega_d (the sector's abundance), A_s, n_s, tau_reio in [0.01, 0.15],
and omega_b inside QX3's BBN bracket [0.0215, 0.0230]. Optimiser: Nelder-Mead from two starts, best kept.

## Lines (per footing)

- L1: chi^2_X <= N_X + 3 sqrt(2 N_X) for X = TT, TE, EE separately, and for the sum.
- L2 (shape): in every band of 100 multipoles (TT 2-2508, TE and EE 2-1996), chi^2_band / n <= 1 + 3 sqrt(2/n).
- L3 (peaks): TT peak-height ratios H2/H1 and H3/H1 (quartic fits around each peak, CT3's method, MC errors with the
  data errors, seed 20261106) agree with the model's to within 3 sigma.
- C-wd (consistency with the graded window): the fitted omega_d within 10 % of 0.1196 and the fitted h inside QX3's
  bracket [0.65, 0.75]. If not, the window's G2'/G5-G7 were graded on a background the CMB does not allow: iter_1 reads
  INCONSISTENT, which counts as FAIL for hardening.
- PASS = J0, J1, L1, L2, L3 and C-wd all hold. FAIL if L1, L2, L3 or C-wd fails.

## Known answer (calibration of the gate)

K1: CLASS at the Planck 2018 TT,TE,EE+lowE best fit (a code and data check only, never an input to the graded model) must
pass L1 and L2. If K1 fails, the gate is uncalibrated and iter_1 is NO VERDICT.

## MUTATE (separate outputs)

- M-A (p = 0): lambda_J = lambda_* constant and physical (>= 1.47 Mpc), so at z >= 100 the comoving Jeans scale is >= 148
  Mpc and the sector cannot cluster on acoustic scales. Represented in CLASS as a w = 0 fluid with c_s^2 = 1 (cs2_fld,
  no PPF), abundance and the other free parameters refit. Must FAIL L1 on both footings.
- M-B (baryons only): omega_d -> 1e-7, refit. Must FAIL L1 on both footings.
If either does not fail, the gate has no power and iter_1 is NO VERDICT.
