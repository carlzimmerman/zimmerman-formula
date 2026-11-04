# WG2_bare_law_web_lensing: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** Several results are already known:
- WG1 (93e5f4e99c): the potential CMB lensing measures sits at 0.003-0.22 a0, inside the law's range. Board row D9 reads NOT EVALUABLE for the law alone, missing (a) a rule for the law on the linear web and (b) a baryon field without a cold term.
- WG1 D1/D2: if the law is off, the needed baryon contrast at k 0.02 Mpc⁻¹ is 0.13-1.0. If the law is on (simple form, rms mapping), it is 0.001-0.045.
- CFG363 and AUDIT_SIGMA8 over-lens with the cold mass included.

κ = ½ FITTED. The cold sector stays retired. No particle and no cold component is added. Not theory closed. Nothing here says the data favour the framework. No downloads.

Owner 2026-11-04, on WG1's NOT EVALUABLE: "you sure we cnt figure it out?" and "swing harder". This lane supplies both missing inputs, using the most natural choice on record for each, and grades the law alone against CMB lensing.

## Question
Run the law alone with a baryons-only initial field from the end of the baryon-photon era, under each natural web rule. Does it give the CMB-lensing amplitude Planck PR4 measures (L 8-400)?

## Inputs
### (b) The baryon field without a cold term
- **Source.** CLASS v3.3.4 (standard physics, as used in RF5). Settings:
  - ω_b 0.02237, h 0.6736, ω_cdm 1e-7 (numerically zero), n_s 0.9649, pivot 0.05 Mpc⁻¹;
  - massless neutrinos as CLASS defaults;
  - transfer functions d_b(k) normalised to unit curvature R.
- **Fields at z_on.** δ_b(k) = d_b(k) R_k, with P_R = 2π² A_s (k/k_p)^(n_s−1)/k³.
- **Velocities.** Zel'dovich, from dδ_b/d ln a by finite difference of CLASS d_b at z_on (1 ± 2 %). There is no division by d_b.
- **Primordial amplitude.** A_s ∈ {1e-9, 4e-9}, bracket ends; 2.1e-9 is used only for the K5-K7 checks.
  - The record has no CMB fit without a cold term, so A_s is not fitted here. The bracket spans a factor 4 in power around the value the record has used.
- **Backgrounds.**
  - **B2 (primary):** the expansion carries an unexplained smooth matter term, as in PAPER67, which takes ρ_DE from an expansion history whose matter term is several times the baryons. In CLASS this is a smooth fluid: Ω_fld 0.2504, w −0.001, c_s² 1. Ω_m,expansion is about 0.30, and only baryons cluster.
  - **B1:** baryons alone in the expansion, Ω_m = Ω_b, with Λ closing it to flat.
  - Radiation is included in E(a) in both, with ω_r 4.18e-5.

### (a) The web rules
- **R0, law OFF:** Newtonian gravity sourced by baryons.
- **R1, law ON:** QUMOND on the peculiar field (Milgrom's QUMOND, PAPER67's law, simple form).
  - ∇·g = ∇·[ν(|g_N|/a0(z)) g_N], with ν(y) = ½ + √(¼ + 1/y), g_N the Newtonian peculiar acceleration of the baryons, and the curl part dropped. This is QUMOND's construction.
  - The periodic box includes the external field from all scales in it.
  - This is the standard rule in published MOND cosmological N-body work. It is the record's FP22 "reading (a)" with no cold mass.
- **a0(z) for R1:**
  - TIE: a0 flat at the footing value. The band is flat to z 2.33 at 0.91-0.94, and constant ρ_DE is used beyond, as in a0kit.a0_of_z with w = −1.
  - RIVAL: a0 = a0_foot E(z).
- **Footing:** canonical, 9.3542e-11 m/s² (a0kit). Alt appears in one run only, R1 TIE B2 A_s 2.1e-9.
- **Turn-on:** the law acts from z_on = 50, chosen so the 1600 h⁻¹ Mpc box is inside the horizon. Before z_on the field is CLASS's GR evolution with the law off.
  - z_on 200 is reported for R1 TIE B2 A_s 2.1e-9 (K7). It is a bracket, not a gate.

## Engine
- Adapted from CFG359's PM (`cfg359_pm.py`, read only), changed as follows:
  - f_b = 1: baryons are the only clustering matter.
  - The simple ν replaces ν_mono, with no switch.
  - Radiation is added to E(a).
  - ICs come from CLASS as above.
- **Box and steps:** L = 1600 h⁻¹ Mpc, 128³ particles and mesh, CIC, periodic, fixed seed. 200 log-spaced steps from a_on to 1.
- **Snapshots:** z 30, 20, 15, 10, 7, 5, 4, 3, 2.5, 2, 1.6, 1.3, 1, 0.8, 0.6, 0.45, 0.3, 0.2, 0.1, 0. At each snapshot the engine records P_Ψ(k) of the total potential (Newton + phantom), CIC-deconvolved, with Ψ = Φ/c².
- **Projection:** WG1's Limber engine, with χ(z) from the same E(a).
  - P_Ψ is interpolated in log k and in z between snapshots.
  - For z > z_on, the z_on snapshot is held.
  - For k below the box's lowest bin, Δ²_Ψ is held flat.
  - Above 0.5 k_Nyquist, a power law is fitted over the last factor 2 in k. A zero-beyond variant is reported.
  - Per bin, the fraction of the C_L integral from in-box k is reported.

## Run matrix (canonical unless stated)
- **R0:** {B1, B2} × A_s {1e-9, 4e-9}. 4 runs.
- **R1:** {TIE, RIVAL} × {B1, B2} × A_s {1e-9, 4e-9}. 8 runs.
- **Checks** (R1 TIE B2 A_s 2.1e-9 unless stated): 128³ at 200 steps (reference); 192³ (K5); 400 steps (K6); z_on 200 (K7); alt footing. 5 runs.

## Grading
- **Ratio:** r = model / data amplitude, r = 1/A_fit, where A_fit is the best-fit multiplier of the model to PR4. Computed on the PACKAGE rule (W + M − F, CMB-marginalised covariance), with the PLAIN rule (W) also reported.
- **Per web rule** (R0; R1-TIE; R1-RIVAL), over its four bracket members (B1/B2 × two A_s):
  - **FAILS LOW:** every member r < 0.5.
  - **FAILS HIGH:** every member r > 2.
  - **WITHIN ×2:** every member 0.5 ≤ r ≤ 2. It is also reported whether every member has |r − 1| ≤ 0.056 (2σ of the PR4 amplitude) and the unscaled model has χ² p ≥ 0.001. Only that reads AMPLITUDE PASS.
  - **STRADDLES:** anything else.
- **D9 for the law alone:**
  - If R0 and both R1 rules each read FAILS (either side): **D9 FAILS for the law alone under every web rule tried**, with the sides stated.
  - If an R1 rule reads WITHIN ×2: **D9 IN RANGE under R1-[rule]**. This is not a CMB pass: the primary CMB still has no fit without dust.
  - Otherwise: **D9 UNDECIDED**, brackets straddle.
- **Validity checks:**
  - **K5:** the 192³ run must give the same per-run label, read on the single-run thresholds above, and r within a factor 1.5 of the 128³ run. Otherwise every R1 label carries NOT CONVERGED.
  - **K6:** the 400-step run must give r within 10 % of the 200-step run. Otherwise every label carries NOT CONVERGED.

## Checks (all must PASS before any label is read)
- **K1 growth.** Newtonian, all matter clustering, Ω_m 1, no radiation, 64³, small amplitude. P(k) at a 0.5 over P at a_i must equal (a/a_i)² within 3 %, averaged over k < 0.05 h Mpc⁻¹.
- **K2 QUMOND solver.** A 1D sinusoidal δ along x, where the curl term is exactly zero. The solver's total g must equal ν(|g_N|/a0) g_N pointwise to 1e-4, relative to the field maximum.
- **K3 Limber.** WG1's K1 analytic case, to 1e-3.
- **K4 ICs.** The measured initial P_δ must match the CLASS input within 10 %, averaged over 0.01-0.1 h Mpc⁻¹.
- **MUTATE.** The Poisson factor 1.5 is halved in the engine. K1 must FAIL. Outputs carry `_MUTATE`.

## What this lane can't say
- It is not a primary-CMB test. The baryons-only acoustic peaks are not graded.
- 1600 h⁻¹ Mpc at 128³ resolves about 12.5 h⁻¹ Mpc. The law's response below that scale is smoothed. K5 is the only resolution check.
- The rules are the two natural ones. A tuned rule between them is not excluded.
- A_s is bracketed, not fitted.
- Nothing here reinstates the cold sector.

## Output
- `wg2_pm.py`: the engine.
- `wg2_run.py`: one run writes `runs/<tag>.json`.
- `wg2_grade.py`: checks, projection and labels, written to `wg2_results.json` and `wg2.out`. MUTATE writes `_MUTATE`.
- `README.md`.
- Runs are single-threaded, under 1 GB each, at most 5 in parallel, and checkpoint-free (minutes each).
