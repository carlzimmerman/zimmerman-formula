# CFG436 FROZEN CRITERIA: T16's z-slope discriminator on CHEX-MATE (is the coupling gradient in radius or in time?)

Frozen before any CFG436 script exists. kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10, from CFG4_common) are reported separately, never pooled. No dark-matter particle; the cold fluid's mass is still required.

## Door (door 10)
DeepSeek T16 (deepseek_push/openai_math_cross_analysis_2026-10/t16_coupling_gradient/, incl. the 10-07 correction) registered a discriminator. Under SATURATION, cluster deficits are static: d(deficit)/dz ~ 0. Under SLOW-RATE settling, deficits still grow toward low z. The deficit is definition A (CFG382 target audit; T15/T16 cluster values 0.41 at b = 0, 0.91 at b = 0.3):
  x = (M_tot - M_b - M_ph)/(5.364 M_b) at R500, with M_ph = (nu_mono(g_N/a0) - 1) M_b and g_N = G M_b/R500^2.
T16 registered the test for X-COP's z-range (0.04-0.1). CHEX-MATE (z 0.05-0.6) gives the lever arm.

## Registered predictions (as T16 states them; no new freedom)
- SATURATION: x(z)/x(z_ref) = 1.
- SLOW-RATE: x(z)/x(z_ref) = F(z)/F(z_ref), with F = 1 - exp(-lambda r(z) tau(z)).
  - r(z) = sqrt(4 pi G rho500(z)), with rho500(z) = 1.55e-24 kg/m^3 x E(z)^2 (T16's R500 density, scaled with rho_crit(z); PRIMARY). The fixed-density variant is reported.
  - tau(z) = t(z) - t(z=2) (T16's tau = 10.3 Gyr from z = 2 at z = 0).
  - lambda in {0.0073, 0.0172} (T16's corrected cluster window), 0.016 (the universal deficit-closing value) and 0.028 (the MW floor). All are reported; the PRIMARY prediction is the window midpoint 0.0123, with the window ends as a bracket.
- Cosmology: flat LCDM, Omega_m 0.3, h 0.7 (only for t(z), E(z), R500).
- The reading that def-A subtracts the full target M_ph (so a physical settling history could map onto x differently) is disclosed as a caveat. The test follows T16's registered sentence.

## Data gate G0 (PRIMARY test)
The primary test needs a PUBLIC per-cluster CHEX-MATE table with z, a total mass M500 (hydrostatic, lensing or dynamical) and M_gas,500 for >= 30 clusters spanning at least 0.05-0.5 in z. The script scans every table environment in the fetched CHEX-MATE sources (../../../_external_data/cfg436_work/src_*) for a gas-mass column. It also records the statement in arXiv 2609.09144 (Sept 2026) on whether individual CHEX-MATE gas fractions exist. If no such table is found, the PRIMARY verdict is **NOT POSSIBLE**, with the missing items listed.

## Indicative row (SECONDARY; never decisive for T16)
arXiv 2609.09144 gives BFC-model gas fractions for four CHEX-MATE stacks. Two of them are at nearly equal SZ mass but different z: bin 3 (M_SZ >= 6.2e14, z < 0.33, median z 0.234, median M_SZ 7.83e14) and bin 4 (z >= 0.33, median z 0.430, median M_SZ 8.36e14). The values exist only in the vector figure figures/fgas_measured.pdf. The script extracts them exactly from the PDF drawing commands (marker centres and error-bar ends), calibrated on the figure's own axis ticks (no by-eye digitising).
- Which of the two high-mass markers is bin 3 and which is bin 4 is NOT labelled. Assignment A follows the drawing order (3rd marker = bin 3); assignment B swaps them. Both are reported. If the verdict differs between A and B, the indicative row is NOT POSSIBLE.
- Masses: the plotted M500c (BFC posterior, built on M_SZ/(1 + b_SZ) with b_SZ = -0.38, assumed z-independent by the source). M_b = M_gas + M_star, with f_star = 0.012 (bracket 0.008-0.016, the same for both bins). R500 from M500c and rho_crit(z).
- R_obs = x(bin 4)/x(bin 3). sigma_R from a 20000-draw Monte Carlo (seed 436): each f_gas is Gaussian with sigma equal to half its 16-84 bar, independent.
- **Power gate (required):** |1 - R_slow| >= 2 sigma_R (R_slow at the PRIMARY lambda), else the row is **NON-DIAGNOSTIC**.
- If the power gate passes:
  - FAVOURS SATURATION if |R_obs - 1| <= 2 sigma_R and |R_obs - R_slow| > 3 sigma_R.
  - FAVOURS SLOW-RATE in the mirror case.
  - NEITHER if both deviate by > 3 sigma_R.
  - otherwise INCONCLUSIVE.

## Forecast (reported)
- Predicted d ln x/dz over z 0.05-0.6 (slow-rate, each lambda).
- The per-cluster precision needed for a 3 sigma slope with 118 clusters, for per-cluster scatter sigma_ln x = 0.3 and 0.5 and the CHEX-MATE z spread (std from the HIGHMz + overview redshifts on disk).
- The largest drift in hydrostatic bias over z 0.05-0.6 that keeps the induced spurious slope below half the predicted slope.

## Controls (main run exits 1 if C1-C3 fail; failures are kept and reported)
- C1: the figure calibration reproduces every y-axis tick (0.000-0.200) and x-axis decade tick to 0.5 pt, and the four CHEX-MATE markers are found (exactly 4 dark-blue error-bar pairs left of the panel divide).
- C2: the extracted bin-1/bin-2 masses are ordered as the table's M_SZ medians (bin 1 < bin 2 < bins 3,4). This sanity-checks the mapping of markers to bins 1-2.
- C3: T16 reproduction: F at z = 0 with lambda = 0.0172 equals 1 - exp(-0.0172 x 11.74) to 1e-3 (T16's rate x tau = 11.74), and nu_mono(y) >= 1.

## MUTATE (`--mutate`, writes cfg436_MUTATE.out and cfg436_results_MUTATE.json)
A deliberately planted indicative row: bin 4's f_gas is set so that x(bin 4) = R_slow x x(bin 3) exactly (primary lambda, canonical footing), and both f_gas errors are shrunk x10. The row MUST then return FAVOURS SLOW-RATE (power gate passing) under assignment A. G0 is not mutated (it is a data inventory). MUTATE exits 1 (= detected) if the flip happens, else 0, and the main verdict is flagged.
