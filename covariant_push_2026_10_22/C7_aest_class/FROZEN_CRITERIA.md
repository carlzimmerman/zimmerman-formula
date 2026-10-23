# C7_aest_class — FROZEN CRITERIA (written before any script or number)

Question: what are AeST's own linear CMB (TT/TE/EE) and matter P(k) predictions, computed by a patched copy of
CLASS v3.3.4 that evolves AeST's extra sector (background Q̄(a) and four extra variables per k), validated first
against pristine CLASS in AeST's exact dust limit?

Owner approval (relayed by the coordinator): fetch class_public v3.3.4 from its official GitHub release into its own
`_external_data` folder; start the native AeST CMB patch lane; derive the adiabatic initial conditions first; validate
against vanilla CLASS in the dust limit. Compiling and running CLASS is approved; no other script from the tarball is run.

## What this lane tests, and what it does not

- It tests AeST's **dust sector** (the k-essence scalar plus the unit-timelike vector at linear order) and the ratio
  **g = G_cosmo/G_N** (C2 P2). It does **not** test the galactic law: the a₀ term is absent at linear order on FRW
  (C2 K1: Y⁽⁰⁾ = Y⁽¹⁾ = 0; SZ21 says the same).
- The extra sector's present density Ω_aest (the Ω_c-like number) is set by the conserved shift charge I₀, an
  **initial condition, FITTED** (C2 K2). Wherever Ω_aest or ω_aest enters a run or a fit, it is labelled FITTED.
- κ = ½ is FITTED and does not enter. Neither a₀ footing enters. Never "the framework fits the CMB".

## External inputs (cited, on disk outside the repo)

- **SZ21** = arXiv:2007.00082 (`newRMONDLett.tex`, sha256 in C2 PROVENANCE): action (eq. `NT_A_action`); FRW action
  and K(Q̄) = −½F(0, Q̄); 8πG̃ρ̄ = Q̄K′ − K, 8πG̃P̄ = K, K′ = I₀/a³; Newtonian-gauge linear system (eqs.
  `delta_field_relation`, `theta_field_relation`, `delta_phi_dot_cv0`, `theta_phi_dot`, `Pi_delta_E_alpha`, the E
  equation after Fig. 1); K functions Cosh, Exp, Higgs-like; Fig. 1 benchmark parameters, read from the text layer of
  `Cl_TT_EE_with_residuals.pdf` (Cosh: K_B = 0.5, Q₀ = 0.1 Mpc⁻¹, K₂ = 7.5×10³, Z₀ = 10⁻⁹ Mpc⁻¹; Exp: K_B = 0.1,
  Q₀ = 10⁻⁴ Mpc⁻¹, K₂ = 9.5×10³, Z₀ = 10⁻¹⁷ Mpc⁻¹; Higgs-like: K_B = 0.3, Q₀ = 1 Mpc⁻¹, K₂ = 8.5×10⁸), MOND models
  λ_s = ∞; caption ΛCDM parameters 100θ_s = 1.04171, ω_c = 0.1202, ω_b = 0.02235, τ = 0.049, Y_He = 0.242,
  10⁹A_s = 2.078, n_s = 0.963. "∂F/∂Y = (2−K_B)λ_s … zero in the MOND limit" (text after `Minkowski_action`).
- **C2** (`covariant_push_2026_10_22/C2_aest_cosmology/`): G_N = (1 + 1/λ_s)Ĝ, g = (1 − K_B/2)λ_s/(1+λ_s);
  BBN line g > 0.9611 ⇒ K_B < 0.078 and λ_s > 24.7 (external to this lane, not re-derived); numpy re-implementations of
  plik-lite TTTEEE + low-ℓ TT + low-ℓ EE in `c2b_native_cmb.py` (imported read-only, not edited).
- **CLASS v3.3.4** (`lesgourg/class_public`, tag v3.3.4), provenance in `PROVENANCE.md`.

## Premises (POSTULATED unless stated)

- **P-F.** F(Y, Q) = −2K(Q) + (2−K_B)λ_c·Y + o(Y) near Y = 0. All runs use **λ_c = 0** (SZ21: F_Y vanishes in the
  MOND limit; Y = 0 on FRW). λ_c is kept symbolic in the derivation and reported, not run. With λ_c = 0, λ_s enters
  only through g.
- **P-g.** g enters as G̃ in the Friedmann equation while T_cmb, N_ur and the baryon number density are physical:
  the patched code multiplies the photon (and hence ultra-relativistic) Ω by g, divides the n_H conversion by g, and
  feeds CLASS's BBN table with ω_b/g and ΔN_eff = (43/7)(g − 1) (g* = 10.75 at BBN). ω_b inputs are in G̃ units.
  The paper's own runs have no G_N; its benchmarks are therefore run at **g = 1** and, separately labelled, at
  g = 1 − K_B/2 (λ_s = ∞).
- **P-Λ.** The constant −2Λ in K is moved to CLASS's Ω_Λ; the extra sector's K has K(Q₀) = 0 at its minimum. This is
  exact (a constant in K has δT^μ_ν = 0).
- **P-ν.** Massless neutrinos, N_ur = 3.044 (CLASS default); no ncdm. Same in vanilla and patched runs.
- **P-CDM.** CLASS's synchronous gauge needs a CDM species to fix the residual gauge. Patched runs keep
  ω_cdm = 10⁻⁸ (inert, 8×10⁻⁸ of the cold total); vanilla comparisons put the same total into CDM.

## Method (fixed now)

**Step D: derivation (sympy, script `c7_derive.py`).** From SZ21's covariant action, with all scalar perturbations
depending on (τ, x) only: general metric (four functions h₀₀, h₀ₓ, hₓₓ, h_yy = h_zz), scalar φ̄ + ϕ, vector
A_x = ∂ₓα with A₀ fixed by the unit constraint (multiplier eliminated). Expand √−g·L to second order in ε; Euler–Lagrange
equations for ϕ and α; the extra sector's T^{μν} from the metric variations; then δ, θ, δp, σ in CLASS conventions.
- **D1** background: T̄^{μν} reproduces 8πG̃ρ̄ = Q̄K′ − K and 8πG̃P̄ = K; the φ̄ equation gives (a³K′)˙ = 0.
- **D2** Newtonian gauge: the derived δ, θ, Π = δp/ρ̄, σ and their equations equal SZ21's (δ, θ, Π definitions and
  fluid equations, σ = 0, and the E equation follows from the ϕ, α equations). A mismatch is a FAIL of D2 and is reported
  term by term; the implementation then uses the derived equations, and only if D3 and D4 pass.
- **D3** gauge covariance: under the derived infinitesimal gauge map, the synchronous-gauge system maps exactly onto the
  Newtonian-gauge system (sympy residual identically 0).
- **D4** conservation: ∇_μT^{μν}_aest = 0 at linear order on the shell of the ϕ, α equations (identically 0).

**Step IC: adiabatic initial conditions (sympy, same script, committed before any spectrum).** Radiation era,
synchronous gauge, CLASS's metric solution h = C(kτ)², η = 2C − (5+4f_ν)C(kτ)²/(6(15+4f_ν)), leading order in kτ
and in ωτ (CLASS's ω = a·ρ_m/√ρ_r), the extra sector a test field (ρ_aest/ρ_r = O(ωτ)), background coefficients w,
c_ad² and Q̄ frozen at τ_ini (valid when they vary slowly; true for Cosh and Exp, stated per run).
- **IC1** the series solution satisfies the extra-sector equations: residual starts at least one order in kτ above the
  leading term of each equation (sympy).
- **IC2** in the exact dust limit (w = c_ad² = 0) the IC equals CLASS's CDM IC: δ = ¾δ_γ, θ = 0.
- **IC3** the Newtonian-gauge IC obtained by the D3 map satisfies the Newtonian-gauge extra-sector equations at the same
  order.
- If SZ21's conventions leave an ambiguity (e.g. which homogeneous modes count as "adiabatic"), the README says so.

**Step P: patch.** `background.c` (Q̄(a) from K′(Q̄) = I₀/a³, ρ, p, w, c_ad²; I₀ solved so that Ω_aest is the input),
`perturbations.c` (four ODEs per k: δ, θ, E, α; their stress-energy into CLASS's Einstein equations; IC; gauge),
`input.c` (parameters `Omega_aest`/`omega_aest`, `aest_K_type` ∈ {dust, cosh, exp, quadratic}, `aest_K_B`,
`aest_Q0`, `aest_K2`, `aest_Z0`, `aest_g`), plus the g-conversions of P-g. The extra sector's equations sit in one
function so a Khronon-dust variant can be swapped in. Saved as `aest.patch` (diff against the pristine tree).
"Exact dust limit" = `aest_K_type = dust`: the same code path with w = c_ad² = 0 and Q̄ = Q₀ (the K₂ → ∞ limit at fixed
Q₀, I₀); E and α still evolve.

## Validation checks (script `c7_validate.py`; one line per check; `--mutate` breaks at least one)

Spectra compared: lensed TT, TE, EE and C_ℓ^φφ for 2 ≤ ℓ ≤ 2500, and linear P(k, z = 0) for 10⁻⁴ ≤ k ≤ 1 Mpc⁻¹.
Relative difference = |ΔX/X|; for TE, |ΔTE|/√(TT·EE).

- **V1 dust limit (PASS line ≤ 1×10⁻⁴, every spectrum).** Patched CLASS with `aest_K_type = dust`, ω_aest = ω_c − 10⁻⁸,
  ω_cdm = 10⁻⁸, g = 1, vs the pristine build with ω_cdm = ω_c, same .ini otherwise, at Planck-2018-like parameters,
  run with `tol_perturbations_integration = 1e-7` in both. In **both** gauges (synchronous; Newtonian). Background:
  100θ_s and r_drag agree to ≤ 1×10⁻⁶. Justification of 1×10⁻⁴: both codes integrate identical dust equations; the only
  difference is the adaptive step control seeing four extra variables. The same comparison at default tolerance is
  reported, not scored.
- **V2 convergence (PASS line: max relative change ≤ max(2×10⁻³, 2 × vanilla's change)).** Cosh benchmark (g = 1),
  default precision vs high precision (`tol_perturbations_integration = 1e-7`, `perturbations_sampling_stepsize = 0.05`,
  `k_per_decade_for_pk = 20`, `l_logstep = 1.026`, `l_linstep = 25`); vanilla ΛCDM under the same switch gives the
  reference change. CLASS's default is designed to be permille-accurate, hence 2×10⁻³.
- **V3 gauge consistency (PASS line: max relative TT/TE/EE/φφ difference synchronous vs Newtonian ≤ max(1×10⁻³,
  3 × vanilla's own gauge difference)).** Cosh and Exp benchmarks (g = 1). This is the test of the non-dust terms.
- **V4 MUTATE.** `C7_MUTATE=1` builds the patch with one sign flipped in the extra ODEs (the metric-source term of
  the extra-sector density equation). It must break V1 or V3; `*_MUTATE.out`, `*_results_MUTATE.json`.
- **V5 IC attractor (PASS line ≤ 1×10⁻⁴ beyond vanilla's own change).** Moving CLASS's start time earlier
  (`start_small_k_at_tau_c_over_tau_h` and `start_large_k_at_tau_h_over_tau_k` × 0.5) changes the Cosh benchmark's
  spectra by no more than vanilla's change + 1×10⁻⁴.
- **V6 limit continuity (DIAGNOSTIC, not gating).** Cosh with Z₀ × {1, 0.1, 0.01}: the max deviation from the dust
  limit is reported; SZ21 expects it to shrink as w, c_ad² → 0. Non-monotone behaviour is reported as a finding about
  the theory, not counted as a code failure.

**"Native prediction ready"** iff V1, V2, V3, V5 pass and the MUTATE run breaks V1 or V3.

## Step N: native spectra (only after "native prediction ready"; script `c7_native.py`)

- Runs (λ_c = 0 throughout; Ω_aest FITTED): **B-Cosh**, **B-Exp** at SZ21's parameters, g = 1; **B-Cosh-g**, **B-Exp-g**
  with g = 1 − K_B/2 (0.75, 0.95); **N1** Cosh K-shape (Q₀, K₂, Z₀ as SZ21) with K_B = 0.05, λ_s = ∞ (g = 0.975);
  **N2** same with K_B = 0.07, λ_s = 400 (g = 0.96259). N1 and N2 satisfy the BBN line. Higgs-like is not run (SZ21:
  not a MOND model).
- Outputs: lensed TT/TE/EE, φφ, P(k); residuals vs pristine ΛCDM at the same parameters.
- χ² against plik-lite TTTEEE + low-ℓ TT + low-ℓ EE with C2's numpy likelihoods: (a) at the caption parameters;
  (b) minimised over (ω_b, ω_aest [FITTED], 100θ_s, ln10¹⁰A_s, n_s, τ) with a fixed deterministic Nelder–Mead,
  start at C2's ΛCDM refit, budget ≤ 150 CLASS runs per model, A_planck as C2. Vanilla ΛCDM minimised the same way is
  reported beside it. **Numbers only, no verdict** (no pass/fail line is frozen for χ²).

## Compute

`OMP_NUM_THREADS=1 nice -n 15`, make ≤ -j2, < 1.5 GB RSS (< 1 GB and long runs paused while `cfg960_sctm_pm.py` runs).

## Files and rules

Commit only this lane's paths; never push. CLASS source is not committed: only `aest.patch`, scripts, outputs,
`PROVENANCE.md`, README. Milestones: (1) this file alone; (2) derivation + IC; (3) patch; (4) validation; (5) native.
Any change to this file is an append-only AMENDMENT marked pre- or post-result.

## AMENDMENT A1 (pre-result, before any patch build or spectrum; 2026-10-23)

The four evolved extra-sector variables are (δ, θ, E, χ) with χ = ϕ + Q̄α, instead of (δ, θ, E, α). The map is
invertible (α = (χ − aQ̄θ/k²)/Q̄). χ and E are gauge-invariant, so their equations carry no metric term and are identical
in both gauges. Evolving α in Newtonian gauge would make χ a difference of two large numbers. The equivalence is a
derivation check (D6 in `c7_derive.py`, sympy, both gauges). Nothing else changes: same checks, same thresholds,
same MUTATE (the metric-source term of the density equation).
