# GO2: the group census out to turnaround around ISOLATED DESI DR1 BGS groups. FROZEN CRITERIA

Committed alone, before any GO2 script that computes a stacked signal or a graded number. TEST lane: adopts nothing, relabels
nothing (GO1's and RB1's labels stand), registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (a0 = 1.1312e-10
m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field component with w about 0, never a particle.
Nothing here says the data favour the framework. Data untrusted; Python run with `-I`; nothing downloaded.

## 0. What was seen before this file (disclosed)

- GO1's FROZEN_CRITERIA, AMENDMENT_A1, DATA_PLAN, RESULT (NOT EVALUABLE: the stacked mean enclosed density stays near 17 rho_m
  out to 16 R500 around 102 eRASS1 groups; f_ret 0.53 +- 0.14 at R500) and its scripts, which GO2 copies.
- The scout's note (`reviews/hy4_codex_audit_2026_11_12/A6_desi_euclid_scope.md`, groups row, top-five item 2).
- The DESI catalogue's columns and one-line percentiles of RA, Dec, Z, M_HALO, N_SAT, L_GAL, LOGMSTAR, P_SAT, WEIGHT,
  Z_ASSIGNED_FLAG; the docs page (PROVISIONAL web read): Self Calibrated Group Finder (Tinker+2021/2022, Williams+2026);
  M_HALO "assigned halo mass of entire group" in Msun/h (the FITS header says solMass; the page wins); mass definition not stated.
- Counts only (`go2_scout.py`, `go2_scout.out`, committed after this file): 666,233 DESI galaxies in the KiDS-1000 N box x ACT
  strip, none in the KiDS S box. Centrals with log10 M_HALO 13.5-14.5, z 0.05-0.30 in the N box: 6,600; with KiDS coverage
  (proxy) 3,365; with a 90 %-complete DESI disc 3,209; isolated by the cut of section 2: **532**. Other cuts tried in the same
  scout: 10 Mpc / 3000 km/s / half-mass: 385; 10 Mpc / 2000 km/s / equal-mass: 1,132; 5 Mpc: 1,476; mass 13.3-14.3: 543.
  No shear, no y, no stacked number of any kind was formed.

## 1. Data

- **Groups:** DESI DR1 VAC bgs-groups v1.0 (`_external_data/desi_dr1_bgs_groups_v1.0/bgs-groups-dr1-v1.0.fits`; passed as an
  argument; galaxies with IGRP, IS_SAT; one central per group). Centre = the central's RA, Dec; z = the central's Z.
- **Shear:** KiDS-1000 SOM-gold, GO1's cached columns and GO1's (CFG686's) estimator verbatim.
- **y:** ACT DR6.02 NILC Compton-y strip, GO1's reader verbatim (bracket: the CIB-deprojected strip).

## 2. Group sample (frozen)

- Central (IS_SAT false) with spectroscopic redshift (Z_ASSIGNED_FLAG 0 or -1), in the KiDS N box x strip (RA 125-240,
  Dec -6 to 3.5), **0.05 <= z <= 0.30**, **13.5 <= log10 M_HALO < 14.5** (catalogue units, Msun/h).
- **Footprint:** at least 90 % of the 10 Mpc isolation disc (sampled on a 0.1-radius grid) falls in 0.25 deg cells that hold any
  DESI galaxy.
- **Isolation, exactly:** the group is dropped if any OTHER central in the whole catalogue (any z, any mass column value, any
  Z_ASSIGNED_FLAG) has **M_HALO >= 0.5 x the group's M_HALO**, a **projected separation < 10 Mpc** (physical, at the group's z,
  BAO-raw D_A of GO1 with h = 0.70), and **|z_j - z_i| c / (1 + z_i) <= 2000 km/s** (line of sight).
- **Kept** (GO1's rules verbatim): >= 200 sources with Z_B > z_l + 0.2 in x = 1-5, sources in every bin, every y annulus
  >= 90 % valid, >= 2 of 4 randoms survive (randoms uniform in the N box x strip, carrying the group's z and R500).
- **Expected:** about 530 isolated groups, about 350-450 kept. **If fewer than 150 are kept: NOT EVALUABLE [too few groups].**
- **Radial unit (disclosed import):** M_HALO is read as M200m in Msun/h, h = 0.6736 (DESI fiducial); M500c from an NFW of fixed
  c200m = 6 at the group's z (rho_c, rho_m of flat Om 0.315); R500 = (3 M500 / (4 pi 500 rho_c(z)))^(1/3). M500 is used only as
  the radial unit, for T500 (GO1's self-similar formula) and for the KVM18 stars, never as a mass in f_ret.
  Bracket: M500 x 0.7 and x 1.4 (mass definition and h factor).

## 3. Measurements (as GO1 + A1 unless stated)

- Same 12 bins in x = R/R500 (edges logspace 0.25-16), same per-group shear sums, same group weight w_i = 1/var15 / R500^4,
  4 randoms per group subtracted, 30 RA-ordered jackknife patches through the whole chain.
- **Lensing mass:** A1's deprojection verbatim (point-mass core + 12 shells, x^-2 tail to 64, weighted least squares with
  Tikhonov lambda_n 2.5e-5, sigma_i from the full stack's jackknife). M_tot(<x) = M_exc + rho_m V, rho_m = (1 + R) rho_b,
  omega_b 0.0224. **Mean enclosed density delta(x) = M_tot / (rho_m V)**, profile reported at every edge out to x = 16.
- **Gas:** **changed from GO1, because DESI groups carry no X-ray gas mass.** Gas inside R500 = the beam-corrected onion
  shells of the stacked y inside x = 1 (inner sphere 0-0.25 plus shells to 1) at T = T500 (GO1 measured T_mw = 1.00 T500 there).
  Bracket: gas500 = 0.0536 x M500 (GO1's lensing-weighted eRASS1 Mgas500 / M500). Gas outside R500 exactly as GO1: onion,
  gNFW beam correction, primary T = T500 x^-0.6, isothermal T500 for the lower-bound census f_ret_lo; mu_e 1.14.
  Conversion: M_gas(shell) = mu_e m_p P_e V / (k T), P_e from y via sigma_T / (m_e c^2) (GO1's YCONST).
- **Stars:** GO1 verbatim (KVM18 inside R500; beyond R500 tracing the lensing excess with s = M*/M500; brackets 0 and x 1.5).
  Reported beside: the stacked sum of DESI member LOGMSTAR inside the group (a visible-member floor, not graded).
- **Background baryons:** rho_b [V(x) - V(1)] as GO1.

## 4. Statistic

- **r_ta:** outermost x where delta falls through **5.55** (log-log interpolation; bracket 11). NOT REACHED if delta(16) >= 5.55.
- At r_ta: M_tot(<r_ta) (lensing), M_b(<R500), M_b(<r_ta), and **f_ret(<r_ta) = R M_b / (M_tot - M_b)**, R = 5.41 (bracket
  5.562). Form B requires f_ret(<r_ta) = 1. f_ret contains no a0: computed once, written per footing, checked identical.
  a0 enters only the reported law row (GO1's: M_b nu_mono(g_N/a0) over M_tot at x = 1, 3, r_ta), per footing.
- Shortfall = 1 - f_ret(<r_ta), significance = shortfall / sigma (jackknife at each realisation's own r_ta).
- **T_close** (GO1's): the mean temperature outside R500 at which the measured pressure would close f_ret(<r_ta) = 1.

## 5. Labels (per footing; identical by construction, checked)

1. **NO VERDICT [KNOWN ANSWER FAILS: list]** if any of section 6 fails.
2. **NOT EVALUABLE** if fewer than 150 groups are kept; or r_ta NOT REACHED; or reached in fewer than 27 of 30 jackknife
   realisations; or sigma(f_ret(<r_ta)) > 0.20.
3. **CENSUS FALLS SHORT** if f_ret(<r_ta) + 2 sigma < 1 on the primary census (the gas-richer temperature reading of the two).
   The row is falsified for gas at the temperatures assumed; T_close is given beside it (y sees pressure: gas cooler than
   T_close could hold the rest unseen, stated with the label, not hidden).
4. **CENSUS REACHES THE FULL SHARE** otherwise (f_ret + 2 sigma >= 1). One-sided: the row stands, it is not a pass. Tag
   **[OVERSHOOT]** if the lower-bound census f_ret_lo - 2 sigma_lo > 1 (more baryons than B allows: counts against B, reported).
- **[BRACKET-DEPENDENT: list]** if the label moves under any bracket of sections 2-4 (lens tail x^-1.5 / x^-3 / none, y tail,
  no beam correction, CIB-deprojected y, gas500 = 0.0536 M500, stars 0 / x 1.5, R 5.562, delta_ta 11, lambda_n 2.5e-7 / 2.5e-3,
  M500 x 0.7 / x 1.4, z 0.05-0.20).

## 6. Known answers (any failure stops grading)

- **KA1 GO1 reproduction:** (a) GO2's measurement code on GO1's eRASS1 selection reproduces GO1's checkpointed per-group
  shear sums (numt, den) for its first 10 groups to 1e-10 relative; (b) GO2's stacker fed GO1's checkpoint with GO1's settings
  (catalogue Mgas500) reproduces go1.json's primary delta and M_exc at x = 1, 4, 8, 11.3, 16 to 1e-6 relative.
- **KA2 random-position stack:** randoms used as lenses (one half minus the other) give M_exc at x = 3, 8, 16 and y gas at
  x = 1, 3, 8 each within |z| < 3; cross shear M_exc at x = 1, 3, 8 within |z| < 3.
- **KA3 methods (GO1's, same tolerances):** A1 deprojection of NFW + r^-2 within 5 % at x = 1, 2.83, 8, mocks bias <= 0.3 sd;
  beta-model y template recovered within 10 % in shells 1-4; map geometry < 0.01 pix; f_ret identity with no excess; footings
  identical.

## 7. Mutations (separate `go2_MUTATE.out`; must bite)

- **M1 isolation off:** 600 groups drawn (seed 20261112) from those in the same box, z, mass range and footprint that FAIL the
  isolation cut, measured and stacked the same way. Bites if delta(x = 11.3) of the control exceeds the isolated stack's by
  more than 2 combined sigma. (If it does not bite, the isolation cut does not do what the lane assumes; reported.)
- **M2 e_t sign flipped:** must give no r_ta or M_exc(<16) < 0.
- **M3 y at positions shifted 1-3 deg:** gas inside R500 consistent with zero (|z| < 3) while the real one is >= 3 sigma.
- **M4 R x 2:** must move f_ret(<r_ta) by more than 2 sigma (only if r_ta is reached; otherwise printed as cannot run).

## 8. Hand estimate (before any number)

For log M_HALO 13.5-14.5 (median about 10^13.8 Msun/h, M200m about 9e13 Msun, M500 about 5.5e13, R500 about 0.55 Mpc at
z 0.2), the mass inside turnaround at 5.55 rho_m (about 3.3e11 Msun/Mpc^3 at z 0.15) is about 2 M200m, so r_ta is about 5 Mpc,
**about 9-10 R500**, inside the grid IF isolation removes the neighbours that held GO1 near 17. Lensing: about 4x GO1's groups
at about half GO1's mass, so delta near 8 R500 is uncertain by about 1.5 (enough to locate r_ta). y: the y-gas noise per group at
fixed x is roughly mass-independent (R500^2 / T500) while the signal scales with mass; GO1 had +-5e13 Msun at 8 R500 with 102
groups, so about +-2.5e13 here against a needed baryon mass of about M_tot / 6.4, about 3e13: **sigma(f_ret(<r_ta)) about
0.6-0.9. Expected label: NOT EVALUABLE [sigma f_ret > 0.20]**, with r_ta probably located near 8-11 R500.

## 9. Compute

At most 4 threads, nice 19, checkpoint every 20 groups to the session scratch, SIGTERM saves and exits. Expected run: minutes.
Outputs `go2.out`, `go2.json`, `go2_MUTATE.out`, `RESULT.md` (label first, at most 100 lines).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
