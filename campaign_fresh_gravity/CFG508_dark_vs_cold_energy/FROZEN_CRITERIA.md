# CFG508 FROZEN CRITERIA: dark energy vs cold energy. What is the difference, and are they two faces of one thing?

Committed alone, before any script was written or any number in this lane computed.

## Terms (owner, 2026-10-08)
- **COLD ENERGY**: the framework's cold, clumping component. Pressureless (w ~ 0), clusters, settles into the law's phantom.
  Cosmic amount R = Omega_c/Omega_b = 5.364 is an INPUT. Its mass is still required. No particle is claimed.
- **DARK ENERGY**: the vacuum component (w ~ -1, smooth). The law a0 = kappa c sqrt(G rho_DE) ties it to galaxy dynamics,
  kappa = 1/2 FITTED. Both footings (a0 = 9.36e-11 and 1.13e-10 m/s^2) are reported separately, never pooled.
- Parallel lane CFG507 studies the ORIGIN of the cold energy (interacting vacuum, the law's field energy). This lane does not
  model the origin; it tests DIFFERENCE and UNITY only. Any overlap is cited, not re-run.

Inputs: Planck 2018 (h 0.6736, omega_b 0.02237, omega_c 0.1200), flat; radiation neglected after z = 200 (same in every
model, so it cancels in ratios). On-disk data only, nothing downloaded:
- DESI DR2 w0wa chains (../_external_data/desi_dr2_chains: cmb, pantheonplus, union3, desy5), columns w, wa, omegam.
- DESI DR1 ShapeFit f sigma8 / (f sigma8)_fid, six bins (DESI 2024 V Table 9), as transcribed in the committed
  fable_independent_2026/L181_desi_dr1_fsigma8_check.py (ShapeFit+BAO sub-panel primary, ShapeFit-only reported).
- The record's own growth cut (CFG361 frozen: |sigma8 ratio - 1| <= 5% AND max_{k<=1 h/Mpc} |P ratio - 1| <= 10%).
- CAMB (linear P(k, z) for the LCDM reference) and stock CLASS (validation only).

## Part 1: property table (record + standard cosmology; no verdict weight)
Rows: w(z); c_s^2; clustering (falls into potentials?); coupling to the law; role in growth; CMB (ISW, acoustic peaks);
BAO; lensing; amount and its status; the record's lanes for each entry (PAPER42, CFG368 (criteria only; results
uncommitted), CFG417, CFG419/421/426, CFG424-460, CFG428, CFG447, CFG452, CFG474, CFG496, DE1-DE13, a0(z) lanes).

## Part 2: hypotheses (declared now)
- **H2 (two independent components):** smooth vacuum (w = -1, or DESI's w(z)) + pressureless clustering cold energy, no
  exchange, independent amounts. Dark constants: 2 (rho_DE, Omega_c).
- **U-A (adiabatic unified fluid, generalized Chaplygin family):** one fluid, P = -A/rho^alpha,
  rho^(1+alpha) = A + B a^(-3(1+alpha)); w = -A_s/(A_s + (1-A_s) a^(-3(1+alpha))), adiabatic c_s^2 = -alpha w.
  alpha = 0 is exactly H2 (Lambda + dust). Normalisation: the early-time dust amount equals Planck omega_c (what the CMB
  sees), flat today. Constants: 3 (A, B, alpha). Both signs of alpha scanned.
- **U-X (the same fluid read as an exchanging pair):** U-A decomposed into vacuum + dust exchanging energy
  (Q = 3 alpha H rho_c rho_v / (rho_c + rho_v), Wang et al. 2013 decomposed GCG). Identical background and, for the
  scoring here, identical perturbations to U-A; it is used only to turn an alpha bound into an a0(z) consequence via
  a0(z)/a0(0) = sqrt(rho_v(z)/rho_v(0)).
- **U-0 (formal unity, c_s^2 == 0 by construction):** a single scalar with a dust-like part of zero sound speed plus a
  constant potential (Lim-Sawicki-Vikman "dust of dark energy" / mimetic class). Background and linear perturbations
  identical to H2 by construction. Constants: 2 (potential constant + initial dust amount). Not scored numerically;
  identity with H2 is shown analytically and the count is stated.
- **U-R (fixed ratio):** one substance whose two parts keep a fixed ratio rho_c/rho_DE across time.
- **U-F (the record's field):** PAPER42 (dark energy = zero-field energy of the MOND field, w = -1, Lambda/a0^2 =
  (pi/4) y_t) plus a condensed cold part from the SAME field. Tested by reading the record: does any committed lane fix
  Omega_c (or rho_c/rho_DE) from the field's constants? (CFG428 one Bose field, CFG288/CFG360 amount free, CFG496 no clue.)

## Part 3: tests and thresholds (declared now)

**T1 (power spectrum / growth, U-A): the Sandvik-type test.** Own sub-horizon linear solver (Newtonian gauge, fluid
equations with w(a), c_s^2, w' term; baryons as dust) from a = 1/201 to 1, growing-mode ICs identical for every model;
ratios R(k, z) = delta_model / delta_LCDM taken in the same solver. Matter clustering is read as the observer reads it:
delta_obs = (rho_b delta_b + rho_u delta_u) / (rho_b + rho_c,early a^-3) (so alpha = 0 gives LCDM exactly).
Velocity amplitude: f sigma8 is the rms of the linear velocity divergence in 8 Mpc/h spheres, computed with the CAMB
LCDM P_lin(k, z) times the model's (theta_model/delta_LCDM)^2.
- Two tracers, both reported: BARYON (galaxy velocities = baryon velocities) and TOTAL (momentum-weighted). An
  exclusion is declared only if it holds for BOTH tracers (the less-constraining tracer decides; no manufactured fail).
- **T1a (data):** chi^2 of the model's f sigma8 ratio against the six DESI DR1 ShapeFit+BAO bins (symmetrised errors).
  EXCLUDED if Delta chi^2 (model - LCDM) >= 9 on both tracers.
- **T1b (record growth cut):** CFG361's cut applied to the linear P ratio at z = 0 (sigma8 ratio within 5%,
  max_{k<=1} |P ratio - 1| <= 10%). FAILS-CUT if outside on both tracers. Reported alongside T1a; the alpha bound is
  quoted from each.
- Scan: alpha in +-{1e-8 ... 1e-1} (log grid, 29 points per sign) plus alpha = 0. Output: the allowed interval
  [alpha_min, alpha_max] per test.
- **MUTATE (CFG508_MUTATE=1):** a unified model with constant rest-frame c_s^2 = 0.01 (LCDM background) MUST be EXCLUDED
  by T1a (and fail T1b). If it is not, the test cannot fail and the lane verdict is VOID. Separate outputs.

**T2 (background / DESI DR2, U-A = U-X):** project each alpha's expansion history onto what an observer assuming
non-interacting dust (omega_c,early) infers: rho_DE,eff = rho_total - rho_m,obs; fit CPL (w0, wa) over 0 <= z <= 2.5
(fit residual reported). Score with a 2-D Gaussian (w0, wa) per DESI DR2 chain (mean and covariance from the weighted
samples after 30% burn-in; Omega_m shift ignored, as in CFG360/368; stated limitation). Delta chi^2 (alpha) vs alpha = 0.
- **DESI-PREFERS-U-A:** best alpha improves on alpha = 0 by Delta chi^2 <= -4 on all three SN chains.
- **CLASH:** if DESI-PREFERS-U-A and the preferred alpha lies outside T1a's allowed interval, then "the unified-fluid
  reading of DESI's w(z) is EXCLUDED by growth". Reported either way: the a0(z)/a0(0) consequence at z = 1, 2, 2.5 for
  (i) DESI's best alpha and (ii) T1a's bound.

**T3 (fixed ratio, U-R):** from the four DESI DR2 chains, r(z)/r(0) = (1+z)^3 rho_DE(0)/rho_DE(z) (cold energy
non-interacting; CPL rho_DE) at TWO epochs, z = 1 and z = 2 (CFG496 lesson: never a single second epoch), plus z = 0.5
reported. U-R PASSES if 1 lies inside the 95% interval at BOTH epochs on any chain; else U-R EXCLUDED.
- **Scrambled cosmology (CFG496 method):** 200 draws of R' = Omega_c/Omega_b uniform in [3, 8] (Omega_b fixed, flat).
  The ratio drift must be independent of R' (max change < 1e-12) and the number of draws where U-R passes is reported
  (expected 0). Any pass in a scrambled draw is a false positive and is disclosed.

**T4 (record read, U-F and U-0):** constant counts and whether any committed lane ties the amounts. Read-only.

**Controls.**
- K1: alpha = 0 reproduces the standard LCDM growth ODE D(a) and f(a) to 1e-4 at z = 0, 0.5, 1.5.
- K2: the solver against stock CLASS for a constant-c_s^2 fluid (w0_fld = -1e-5, cs2_fld = 1e-6, omega_cdm = 0.001,
  Lambda fills): |ratio_mine - ratio_CLASS| <= 0.02 for the fluid delta at z = 0, k in {0.1, 0.3, 1} h/Mpc where the
  ratio is > 0.1.
- K3: alpha = 0 in T2 returns (w0, wa) = (-1, 0) to 1e-6.
- K4: the T1a chi^2 of LCDM reproduces L181's committed value (4.56 for ShapeFit+BAO) to 0.01.
- K5: the scrambled-cosmology independence check of T3.
Main run exits 0 only if K1-K5 pass.

## Part 4: distinguishing observables (reported, no verdict weight)
For each observable: H2 prediction, unified prediction (at T1a's bound where U-A applies), current precision, and what
would decide: (a) fixed ratio / ratio drift across epochs; (b) exchange signature in w(z) correlated with growth;
(c) a0(z) vs sqrt(rho_DE) from a non-interacting fit; (d) ISW / ISW-galaxy cross-correlation (potential decay rate
dlnPhi/dlna at k = 0.01, 0.1 from the solver); (e) the settled cold-energy fraction vs local dark energy (environmental
a0 constancy); (f) small-scale P(k) / Ly-alpha sound-speed limits.

## Part 5: lane verdict rule (declared now)
- **UNIFIED VIABLE (constant count N):** a unified class with a nonzero unity parameter is PREFERRED over H2
  (Delta chi^2 <= -4 jointly) and survives T1a/T1b and T3; OR a committed lane fixes the cold amount (or rho_c/rho_DE)
  from the dark-energy field's constants, so unity lowers the count below 2, and it survives the tests. N stated.
- **TWO INDEPENDENT COMPONENTS FAVOURED:** no unified class with a nonzero unity parameter is preferred; U-A's alpha is
  bounded by T1a to |alpha| < 1e-3 (or tighter); U-R is excluded; no committed lane ties the amounts; AND every surviving
  unified class (including U-0) needs MORE dark constants than H2.
- **NOT DECIDABLE:** as the previous case, except that a surviving unified class (e.g. U-0) has the SAME dark-constant
  count as H2 and is observationally identical to it. The data that would decide are then stated.
- MUTATE failing to exclude c_s^2 = 0.01 makes the lane VOID.

Standing: kappa = 1/2 is FITTED; the cold energy's mass is still required; no dark-matter particle is claimed; this is
not "theory closed". A fail is verified as hard as a win.
