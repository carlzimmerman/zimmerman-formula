# CFG386 FROZEN CRITERIA: pre-flight. How many ON-DISK z ~ 1.5-2.7 discs individually span the regimes CFG385 needs?

Committed alone, before any script. A PRE-FLIGHT: candidate counting from fitted models and published radii; no law is scored. kappa = 1/2 FITTED. Owner (2026-10-06, chat "Nobel Prize and neutrinos"): "go for it". The orchestrator agreed (read-only use of the CFG270 / SINS / KURVS inputs) and flagged beam smearing and pressure support.

**CFG385 requirement.** Each disc must have its OWN points from y >~ 3 (Newtonian) to y <~ 0.3 (deep). In calibration-free terms, using the measured g_obs = V^2/r: inner g_obs >= 3.5 a0 (P2: y = 3 gives 3.46 a0) and outer g_obs <= 0.55 a0 (y = 0.3 gives 0.55 a0).

## Samples and rules (declared)
- **KMOS3D (192 cube fits, data_assembly/kmos3d_cubes/k3d_fits_main_final_flags.csv + kmos3d_catalog.csv; z 2.0-2.7).**
  Model V(r) = V_a (2/pi) arctan(r/r_t) (the fits' own model). Radii in arcsec, converted to kpc with Planck18 D_A(z).
  - Inner resolved radius r_in = PSF_FWHM (CONSERVATIVE, beam-resolved) and PSF_FWHM/2 (LENIENT, reported).
  - Outer radius r_out = rmax (the outermost data radius in the fit).
  - g_obs = V^2/r (P0). Reported also with pressure P1: V_c^2 = V^2 + 2 sigma0^2 r/r_d.
  - A disc QUALIFIES if r_in < r_out, g_obs(r_in) >= 3.5 a0, g_obs(r_out) <= 0.55 a0, eVa/Va <= 0.10, and it is not a failed
    fit (Va < 790 km/s).
  - The thresholds use a0 = canonical 9.36e-11. The DE-law a0(z) about 0.8x is reported.
- **KURVS (z ~ 1.5; data_assembly/arxiv_tables/kurvs2023_velocities_at_radii.csv + kinematics):** V at 3 R_d, 6 R_d and the last
  point. It qualifies if its innermost listed point has g_obs >= 3.5 a0 and its outermost <= 0.55 a0, with errors <= 10%.
- **SINS/zC-SINF AO (CFG280):** published V_c at a single radius, so it cannot span by construction. Reported as 0 qualifying.

## Decision (declared)
- **ON-DISK DECISIVE CANDIDATE:** >= 10 qualifying discs (conservative r_in, P0) at z >= 2.
- **PARTIAL:** 1-9. List them; external data are needed to reach 10.
- **NONE ON DISK:** 0. The external fetch list is the next step (owner's go).
Pressure: report sigma0/V(r_out) for every qualifier. Discs with sigma0/V > 0.5 at r_out are flagged as pressure-limited
(CFG140/160 wall).

## Controls
- C1: the D_A conversion reproduces about 8.3-8.5 kpc/arcsec at z = 2.2 (Planck18).
- C2: the arctan model returns V(r -> infinity) -> V_a and V(r_t) = V_a/2.
- MUTATE: a0 x 10. The qualifying count must change (rc 1).

Local compute only. No downloads. No cube is re-fitted.
