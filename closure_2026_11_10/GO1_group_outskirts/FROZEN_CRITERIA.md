# GO1 Part A: a stacked baryon census of eRASS1 groups out to turnaround. FROZEN CRITERIA

Committed alone, before any GO1 Part A script exists and before any GO1 shear, y or census number is computed. The only number
looked at before this file is a catalogue count (how many eRASS1 entries fall in the selection below, by redshift; no shear, no y).
TEST lane: it adopts nothing, relabels nothing (RB1's labels stand) and registers nothing. kappa = 1/2 FITTED; not theory closed.
Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (a0 = 1.1312e-10 m/s^2), graded separately and never pooled. Cold dark energy is
a gravitating field component with w about 0, never a particle. Nothing here says the data favour the framework. Data untrusted;
Python run with `-I`. Nothing is downloaded. Part 0 (the eRASS1 X-ray tile plan) is in DATA_PLAN.md and is not graded here.

## 0. What is tested (PAPER72 open item 5; RB1 limit 2)

- Form B as RB1 froze it: a group holds R times the baryons that fell into it as cold dark energy; gravity is Newtonian with the
  total mass. **Retained fraction** f_ret(<r) = R M_b(<r) / [M_tot(<r) - M_b(<r)], R = 5.41 (bracket 5.562).
- RB1 read f_ret = 0.597 at R500 in Lovisari's 20 groups (hydrostatic masses). B reads the missing 40 % as baryons that lie outside
  R500. **B needs f_ret(<r_ta) = 1 at the turnaround radius.** Inside r_ta, f_ret < 1 is allowed (gas expelled further out than
  the collisionless cold), so only the turnaround row is graded.
- Here M_tot comes from stacked weak lensing (no hydrostatic assumption) and M_b from X-ray gas inside R500, thermal-SZ (ACT y)
  gas outside R500, and stars.
- **Where a0 enters:** nowhere in f_ret (B's cold is real mass, the masses are measured). Both footings are run and the script
  checks their f_ret numbers are identical. a0 enters one reported row only: the law's own enclosed mass from the census baryons
  (M_b nu_mono(g_N / a0)) beside the lensing mass at x = 1, 3 and r_ta.

## 1. Data (all on disk)

- **Groups:** eRASS1 main cluster catalogue (Bulbul+2024; `../_external_data/cfg687_inputs/erass1_main.tsv`, CFG687's parser: col 1-3
  RA, Dec, z; col 5 Mgas500 in 1e11 Msun; col 8 R500 in kpc; col 10 M500 in 1e13 Msun). R500 and M500 come from eROSITA's
  scaling relations calibrated with weak lensing in LCDM; R500 is used as the radial unit and M500 only for T500 and the stars
  (disclosed imports). Mgas500 is the X-ray gas mass.
- **Shear:** KiDS-1000 SOM-gold (`../_external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits`), cached
  columns in the session scratch (CFG686's extract, copied). CFG686's estimator copied verbatim: e2-flipped tangential sign,
  inverse-Sigma_crit^2 weights, m = -0.01, Z_B > z_l + 0.2 and Z_B <= 1.2, BAO-raw distances (h r_d = 101.54 Mpc, h = 0.70).
  **KiDS-Legacy:** the release on disk (`../_external_data/kl1_kids_legacy_2026_11_10/`) holds cosmic-shear 2-point statistics,
  chains and n(z) only, no shear catalogue, so it cannot be stacked; not used (stated, not a choice).
- **y:** ACT DR6.02 NILC Compton-y strip (`../_external_data/act_dr6_nilc/strip_ComptonY.f32be`, Dec -36 to +4, 0.5 arcmin CAR,
  beam 1.6 arcmin FWHM), read by memmap with FR3's geometry (its K4a WCS check copied). Bracket: the CIB-deprojected strip.

## 2. Selection (frozen)

- In CFG687's KiDS boxes (N: RA 125-240, Dec -6 to 5; S: RA >= 325 or <= 60, Dec -37 to -25) AND inside the y strip
  (-35 < Dec < 3.5).
- **Lovisari's gas-mass range:** 1.35e12 <= Mgas500 <= 1.15e13 Msun (the 20 groups' min and max, h70). M500 > 0, R500 > 0.
- **Primary z 0.05-0.30.** Bracket z 0.05-0.20.
- Kept if: >= 200 sources with Z_B > z_l + 0.2 within x = 1-5, sources in every radial bin, and every y annulus has >= 90 % valid
  (finite, non-zero) pixels. Groups failing are dropped before stacking (the count is reported).

## 3. Radii, stacking, weights

- Radial unit x = R / R500 (R500 from the catalogue, projected with the BAO-raw D_A). **12 bins, edges logspace(0.25, 16): 0.25,
  0.354, 0.5, 0.707, 1, 1.41, 2, 2.83, 4, 5.66, 8, 11.3, 16.** x = 1 is an edge.
- Per group i: ΔΣ_i(x) by the estimator above (inverse-variance within the group), times R500_i^2 (Mpc^2) -> a mass per unit x^2.
- **Group weight** w_i = 1 / var_i, var_i = the shape-noise variance of group i's ΔΣ_i R500_i^2 in x = 1-5 (one weight per group,
  the same in every bin and for every quantity: shear, y, gas, stars, background). So every stacked number is the same weighted
  mean over the same groups.
- **Randoms:** 4 per group, uniform in the same KiDS box and the y strip, carrying the group's (z, R500); kept if their x = 1-5
  source count is >= 0.5 of the group's and their y annuli pass the 90 % rule. Stacked with the parent's weight and subtracted
  from the group stack (shear and y alike). If fewer than 2 randoms survive the group is dropped.
- **Errors:** jackknife over 30 equal-count RA-ordered sky patches of groups (randoms go with their parent group), applied to the
  whole chain (shear, y, deprojection, census, r_ta, f_ret).

## 4. The lensing mass

- **Deprojection (no halo model):** the stacked excess density rho_exc(x) = rho - rho_mean is piecewise constant on 12 shells:
  shell 0 = [0, 0.354] (it holds the core), shells j = 1..11 on the bin edges above, and a **tail** beyond x = 16 continuing the
  last shell as x^-2 out to x = 64. ΔΣ of each shell is computed exactly (R-weighted average over each bin's area) and the square
  12 x 12 system is solved directly (no regularisation). M_exc(<x) = sum over shells, in Msun (stack-weighted mean).
- Tail brackets: x^-1.5, x^-3, none.
- **Total mass:** M_tot(<x) = M_exc(<x) + rho_m(z) V(x), with rho_m = (1 + R) rho_b, rho_b = omega_b x 2.775e11 Msun/Mpc^3 x (1+z)^3,
  omega_b = 0.0224 (stated import), V(x) = 4 pi/3 (x R500_i)^3; both stacked with w_i. Under B the cosmic mean has f_ret = 1 by
  construction, so the background share pulls f_ret toward 1 only by its own weight.
- **Turnaround:** r_ta is the outermost x where the mean enclosed density M_tot(<x) / V(x) falls to **delta_ta = 5.55** x rho_m
  (a shell turning around now in matter domination); log-log interpolation between edges. Bracket delta_ta = 11 (with dark
  energy). NOT REACHED if the stack is still above delta_ta at x = 16.

## 5. The baryon census

- **Gas inside R500:** the stacked catalogue Mgas500 (X-ray). Bracket x 0.8 (Eddington bias of a flux-limited sample at low mass).
- **Hot gas outside R500 (ACT y):** per group the mean y in each x annulus (plus an inner disc 0-0.25), random-subtracted, scaled by
  c_i = R500_i^2 / T500_i, stacked with w_i, then deprojected by FR3's onion volume matrix on the same edges (the last shell
  truncated at x = 16; bracket with an x^-3 pressure tail). Gas mass per shell = mu_e m_p P_e V / (k T(x)), mu_e = 1.14.
  - T500_i = 8.71 keV (M500_i / 1e15 Msun)^(2/3) E(z)^(2/3) (self-similar, h70; disclosed import through M500).
  - **Primary T(x) = T500 x^-0.6 for x >= 1** (FR3's tau 0.77 at 1.52 R500, from X-COP's self-similar profile).
  - **Lower-bound reading: isothermal T(x) = T500** beyond R500. Observed group and cluster temperatures fall outward, and
    neighbours in the stack are on average less massive (cooler) than the central, so for the measured pressure this is the
    least gas mass: **f_ret_lo** is a lower bound on the hot-gas census.
  - **Beam:** a noise-free Arnaud gNFW y template is injected per group with its own beam (1.6 arcmin in x units) and put through
    the same annuli, stack and onion; per-shell correction = true / recovered, applied in the primary. Bracket: no correction.
- **Stars:** inside R500 the KVM18 relation M*,500 = 1.7e12 (M500/1e14)^0.6 (RB1's import). Beyond R500 the stars trace the
  lensing excess with each group's ratio s_i = M*,500 / M500: M*(1 < x' < x) = s [M_exc(<x) - M_exc(<1)]. Brackets: no stars beyond
  R500; x 1.5.
- **Background baryons:** rho_b V(x) (stacked), added to M_b. **M_b(<x)** = gas500 + y gas(1..x) + stars + rho_b [V(x) - V(1)];
  the y and lensing stacks are excess over the mean, the mean is added once for each.
- Reported beside: the y-weighted temperature inside 0.5-1 R500, T_mw = (Y_sph from the onion) / (Mgas(0.5-1) from the
  eRASS1 beta-model shape of CFG687, beta 2/3, r_c 0.15 R500) in units of T500, as a check on the T500 scale; and **T_close**, the
  mean T outside R500 at which the same measured pressure would give f_ret(<r_ta) = 1.

## 6. Labels (per footing; identical by construction, checked)

Graded at r_ta (delta_ta = 5.55), with sigma = the jackknife sigma of the quantity at each realisation's own r_ta:

- **NOT EVALUABLE** if r_ta is NOT REACHED, or reached in fewer than 27 of 30 jackknife realisations, or sigma(f_ret(<r_ta)) > 0.20
  (cannot tell RB1's 40 % shortfall from 1 at 2 sigma), or a null in section 7 fails (then **NO VERDICT [NULL FAILS]**).
- **FAILS FROM ABOVE** (counts against B, decisive): f_ret_lo(<r_ta) - 2 sigma_lo > 1. The lower-bound census already exceeds B's
  ceiling at the edge.
- **ABOVE ON PRIMARY T** (counts against B, not decisive): f_ret(<r_ta) - 2 sigma > 1 but not FAILS FROM ABOVE.
- **CLOSES ON HOT GAS** (consistent with B): |f_ret(<r_ta) - 1| <= 2 sigma and not FAILS FROM ABOVE.
- **SHORT AT TURNAROUND [LOWER-BOUND CENSUS]** (counts against B, NOT a falsification): f_ret(<r_ta) + 2 sigma < 1. The census sees
  hot gas only through its pressure; gas cooler than T(x) carries more mass per unit y, and gas below ~0.1 keV can hold the
  missing baryons without being seen in y or in eRASS1's band. T_close says how cool it would have to be.
- **Stated plainly:** with y alone this lane cannot falsify B from below (no upper bound on the baryons outside R500 exists on
  disk). Falsification from below needs the gas density and temperature separately, i.e. X-ray surface brightness out to r_ta
  (Part 0's tiles) with y.
- **Tags:** [BRACKET-DEPENDENT: list] if the label changes under any section 4/5 bracket, R 5.562, delta_ta 11, the CIB-deprojected
  map, or z 0.05-0.20.
- **Reported, not graded:** f_ret and f_ret_lo at x = 1, 2, 3, 5 (x = 1 beside RB1's hydrostatic 0.597, different groups and mass
  method); the excess-only f_ret (background removed); M_exc, M_b and their parts at each edge; the law row of section 0.

## 7. Known answers (must pass) and MUTATE twins (must bite)

- **KA1 estimator:** CFG686's esd (exec'd from its file) and my copy give identical ΔΣ (to 1e-10 relative) in CFG686's physical
  bins for 5 selected groups; CFG686's SIS self-test passes (< 1 %).
- **KA2 deprojection:** analytic ΔΣ of an NFW (c = 4, M500 = 5e13, R500 0.55 Mpc) plus a power-law excess rho ~ r^-2 beyond 2 R500,
  binned as the data, recovers M_exc(<x) at x = 1, 3, 8 within 3 % (noise-free; the tail matching the injection).
- **KA3 y:** the injected noise-free gNFW template stacked and onion-deprojected recovers its pressure-shell integrals at x = 1-4
  within 10 % after the beam correction; FR3's map geometry check (< 0.01 pix) passes.
- **KA4 identity:** with M_exc = 0 and no excess baryons, f_ret = 1 to 1e-12 at every x.
- **KA5 footings:** every f_ret number identical on both footings.
- **Nulls (section 6):** N1 cross shear: the deprojected M_exc(<x) at x = 1, 3, 8 with e_x in place of e_t is consistent with zero
  (each |z| < 3); N2 random-minus-random (two halves of the randoms as lenses) for M_exc and for the y gas at x = 3, 8: each |z| < 3.
- **MUTATE:** M1 R x 2 must move f_ret(<r_ta) by more than 2 sigma (power); M2 the y stack at positions shifted 1-3 deg must give
  y gas consistent with zero (|z| < 3) while the real stack does not (bites); M3 lensing with e_t sign flipped must give no r_ta
  or negative M_exc (bites).

## 8. Compute

Preemptible: per-group results checkpointed to the session scratch every 20 groups; SIGTERM saves and exits; reruns resume.
One thread. Outputs `go1.out`, `go1.json`, `go1_MUTATE.out`; RESULT.md with the label first and commit ids local / origin.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
