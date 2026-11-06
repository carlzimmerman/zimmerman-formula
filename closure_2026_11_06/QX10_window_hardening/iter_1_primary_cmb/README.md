# QX10 iter_1: primary CMB TT/TE/EE. NO VERDICT for all four cells (late-lensing bound J1); the early sector fits

Kappa = 1/2 FITTED; not theory closed. Criteria c1f0cadb7a. Script qx10_i1.py (fit / k1 / jcheck / grade).
Outputs qx10_i1.json/.out, qx10_i1_MUTATE.json/.out; fits fit_<footing>_<mode>.json/.npz; k1.json; jcheck.json.

## Result

- **K1 (calibration):** the Planck 2018 best fit (a code and data check, never an input) passes L1 and L2 on these raw
  diagonal spectra: TT 2593/2507, TE 2084/1995, EE 2066/1995, 0 of 66 bands fail. The gate is calibrated.
- **The sector as CDM at recombination (J0): PASS on every cell.** The comoving Jeans wavenumber at z >= 10 is at least
  7e8 Mpc^-1 (line 50). The switch keeps the sector cold through the whole primary-CMB epoch.
- **Fits on the footing background:**
  - canonical (omega_DE fixed by a0): omega_b 0.02225, omega_d 0.1209, ln(1e10 A_s) 3.049, n_s 0.9649, tau 0.056, h 0.6740.
  - alt (h^2 fixed by a0): the same to 1e-4, h 0.6740.
  - chi^2: TT 2578 / 2507, TE 2074 / 1995, EE 2066 / 1995, sum 6718 / 6497 (line 6839): L1 PASS. L2 0 of 66 bands fail.
  - L3 peaks: model H2/H1 0.4538, H3/H1 0.4451 vs data 0.4505 +- 0.0068, 0.4412 +- 0.0063: PASS.
  - C-wd: omega_d 0.1209 is +1.1 % from the window's 0.1196, h inside [0.65, 0.75]: consistent.
- **J1 (late lensing of TT): FAIL on every cell**, so the CDM proxy is not shown valid at the lensing level and iter_1 is
  **NO VERDICT** as frozen. Max |1 - S(L)| over L 2-2500 is 0.061 (C2), 0.111 (C4), 0.124 (C1) and 0.525 (C3). The
  conservative bound Delta chi^2_TT = sum[(max|1-S| x |C_lensed - C_unlensed|)/sigma]^2 is 1.05, 3.47, 4.30 and 77.2,
  against the line 1. The bound applies the largest suppression at every multipole, so it overstates the effect. Settling it
  needs the sector's Jeans term inside a Boltzmann code's lensing step.
- MUTATE: M-A (p = 0, a smooth w ~ 0 fluid with c_s^2 = 1) chi^2 sum 30,923 / 31,046 and M-B (baryons only) 117,280 /
  114,383. Both FAIL L1 on both footings. BITES.

## Disclosed

- **Not independent evidence.** The two footings give the same background, h = 0.674, because their a0 values were built
  from the dark-energy and total densities (a0 = c H/Z). So the acoustic-angle agreement is not independent evidence. With the
  sector cold at z >= 10 (J0), the primary spectrum is the standard cold-component spectrum. The test shows that the window's
  sector does not spoil it; it does not show that the framework predicts it.
- **Data limits.** These are raw Planck PR3 CMB-only spectra with diagonal errors, not the Planck likelihood. PR4 and ACT
  primary spectra are not on disk (NEEDS_OWNER.md).
- **MUTATE representation.** M-A uses w0_fld = -1e-3, not 0: CLASS refuses a w >= 0 fluid at early times when setting
  adiabatic initial conditions. The background change is 2 % over a factor 1100 in a.
