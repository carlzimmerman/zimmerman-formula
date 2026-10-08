# CFG491 FROZEN CRITERIA: the on-disk three-way test (framework vs ΛCDM vs standard MOND)

Written and committed alone, before any script of this lane exists and before any statistic below is computed on data.
κ = ½ is FITTED (one input fixed elsewhere). Both footings (canonical 9.3603e-11, alt 1.1312e-10 m/s²) are run separately and never pooled. The cold mass is still required; no dark-matter particle is added.

## Why this test

Step 1 of this lane (the differentiator matrix, README) finds that candidate B behaves like ΛCDM wherever the matter content or the external-field effect (EFE) decides (wide binaries, cluster satellites, voids, growth, clusters), and like MOND wherever the arrangement inside a galaxy decides (RAR shape and tightness). The observables that separate it from both at once on a single data set are (a) the lensing edge (not testable cleanly on disk: CFG413/486 show it is two-halo-template-dependent) and (b) the CONJUNCTION "no EFE AND a tight RAR" on rotation curves. (b) is the best test with data on disk. It is run here as a three-way comparison in which all three models are pushed through the same estimator and the same nuisance model.

Known limitation, stated in advance: the ΛCDM column is dark-matter-only abundance matching (the CFG476 generator). Feedback/hydrodynamic ΛCDM has no parameter-free prediction for either statistic and is NOT tested. Any outcome that separates the framework from ΛCDM separates it from DMO-ΛCDM only.

## Data (all on disk; no downloads)

- SPARC rotmod files + `SPARC_Lelli2016c.mrt` via `CFG4_common.load_sparc()`.
- Chae et al. 2021 environmental field amplitudes: `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv` (as used by CFG8).

## Sample

SPARC galaxies with Q ≤ 2, Inc ≥ 30°, a row in chae21_env.csv, and ≥ 5 points with g_bar > 0 and V_obs > 0. Nominal mass model: Υ_disk 0.5, Υ_bul 0.7, gas as tabulated, SPARC distance and inclination.

Environmental field (CFG8 convention): log e_N = mean of log_eN_maxclu and log_eN_noclu; g_N,ext = 10^(log e_N) × 1.2e-10 m/s²; its error σ_lN = sqrt(mean of the two squared errors + (half the maxclu−noclu difference)²). For a law with kernel k and scale a, the MOND external field is e = F_k(g_N,ext / a), F_k(z) = ν_k(z) z.

EFE kernel (CFG8's 1-D AQUAL construction): ν_e(z; e) = [F(z + z_e) − e]/z with F(z_e) = e.

## Statistics (per footing a_F; x = g_bar / a_F)

- **S1, the EFE slope β.** For each galaxy, over its points with x < 1 (galaxy kept for S1 only if ≥ 3 such points), with equal weights:
  - R_i = mean of r = log10 g_obs − log10[ν_mono(x) g_bar] (residual about the framework's isolated law);
  - D_i = mean of log10 ν_e^{mono}(x; e_i) − log10 ν_mono(x), with e_i = F_mono(g_N,ext/a_F) (the EFE template, computed with the framework's kernel and footing, identical for every model);
  - X_i = mean of log10 x.
  - β = OLS coefficient of D_i in R_i ~ 1 + D_i + X_i (equal galaxy weights). X_i controls for any acceleration-dependent misfit of the isolated law, so β reads only the environment-correlated part.
- **S2, RAR tightness.** CFG476's statistic on all points of the sample: weighted rms (weights 1/(eV/V)²) of log g_obs − log g_bar − log ν_mono(g_bar/a) with a free (bounded −11.5 … −9.0 in log).

## Models (each a mock generator; the predictions are the mock distributions of β and S2)

- **F (framework, candidate B):** g = ν_mono(g_bar,true / a_F) g_bar,true. No EFE.
- **L (ΛCDM, dark matter only):** g = g_bar,true + g_NFW(R_true), the CFG476 recipe: halo mass from Moster+13 at the galaxy's nominal M* with 0.15 dex scatter in M* at fixed M_h, Dutton–Macciò c(M) with 0.11 dex scatter. No EFE.
- **M (standard MOND, primary):** ν_RAR kernel at a = 1.2e-10 with the 1-D AQUAL EFE, e_true = F_RAR(g_N,ext,true / 1.2e-10).
- **M_same (reported, not in the verdict):** ν_mono at a_F with the EFE (the EFE alone, kernel and scale shared with F).

Nuisance model, identical for every model (Li+2018-style priors): Υ_disk and Υ_bul true = nominal × 10^N(0, 0.10); gas × 10^N(0, 0.04); D_true = D (1 + N(0, eD/D)) clipped ≥ 0.3 D (eD missing → 10%); i_true = Inc + N(0, eInc) clipped to [10°, 89°]; log g_N,ext,true = catalogue + N(0, σ_lN); V noise N(0, eV). Mock observed quantities are what an observer with the nominal model infers: g_bar is the nominal one; g_obs,inferred = (V_true sin i_true / sin i_nom + noise)² / R_nom × (D_true / D_nom), with V_true² = g R_true and R_true = R_nom D_true / D_nom; g_bar,true(R_true) = the nominal g_bar with the Υ and gas factors applied (g_bar is distance-independent at fixed angle).

N_mock = 300 per model per footing (fixed seeds).

## Decision rules (per footing)

- For each model m and each statistic s, p_m,s = 2 min(frac(mock ≤ data), frac(mock ≥ data)), floored at 1/N_mock.
- Model m is CONSISTENT iff p_m,β ≥ 0.05 and p_m,S2 ≥ 0.05 (two tests per model, no multiplicity correction; disclosed).
- **FRAMEWORK SINGLED OUT** iff F is consistent and both L and M are inconsistent.
- **FRAMEWORK EXCLUDED** iff F is inconsistent (the failing statistic named).
- Otherwise **NOT SINGLED OUT**, with the list of consistent models.
- **Power (pre-declared, decides the label):** P_single = the fraction of F mocks which, used as pseudo-data against the other F/L/M mocks, would return FRAMEWORK SINGLED OUT. If P_single < 0.5 the verdict carries the label LOW POWER, whatever it is.
- The same verdict on both footings is required to call it footing-independent; otherwise both are reported side by side.

## Controls

- **K1:** S2 on CFG476's own sample (Q ≤ 2, no Chae cut) at fixed Υ reproduces CFG476's 0.0994 dex within 0.0005.
- **K2:** ν_e(z; e = 1e-12) / ν(z) − 1 < 1e-6 for z in [1e-3, 10] for ν_mono and ν_RAR.
- **K3:** F(F⁻¹(e)) = e to relative 1e-6 for e in [1e-4, 1] for both kernels.
- **K4:** the L generator with V noise only (no other nuisance) on CFG476's sample gives median rms within 0.02 of CFG476's 0.205 (100 mocks).
- **MUTATE (`CFG491_MUTATE=1`, separate outputs):** the data velocities are replaced by one M (standard MOND with EFE) realisation (seed 4910). Required: F is judged inconsistent through β. The MUTATE run exits 1 when it detects this (teeth present) and 0 when it does not, in which case the test is reported as lacking teeth.

## What would and would not follow

- SINGLED OUT on both footings, not LOW POWER: "on SPARC + Chae's environment, the no-EFE + tight-RAR conjunction is preferred over DMO-ΛCDM and standard MOND". Not over feedback ΛCDM.
- Any β inconsistency for F is a framework failure (an EFE-like signal the framework does not have), reported as such.
- Nothing here bears on κ, ρ_Λ, the cold-fluid amount or a₀(z).
