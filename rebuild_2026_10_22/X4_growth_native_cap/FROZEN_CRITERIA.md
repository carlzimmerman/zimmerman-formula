# X4_growth_native_cap: frozen criteria (2026-10-23, written and committed alone, before any script or number)

Lane X4 of `rebuild_2026_10_22/X0_explanation_map/MAP.md` (§1.B items 1–2; §3 "Growth at the cap").
The assumption ledger is `ASSUMPTION_LEDGER.md`, committed with this file.

κ = ½ FITTED. a₀ is absent at linear order on FRW (Q6 D0), so neither footing (9.3603e-11 / 1.1312e-10 m/s²) enters
any number here; where an inherited verdict depends on a footing (S4's galaxy guard) both footings are quoted, never
pooled. No dark-matter particle. No new fitted constant is adopted as a cure: λ_D is the record's growth-set knob and is
graded, never adopted. Never "theory closed". Never "the data favour the framework".

## 0. Questions, scope and pre-stated expectations

**(i)** What is v3's linear-growth gap at the μ_K that S4's isolated-galaxy guard allows? S4 (README §3,
`s4_v3_muk_clusters.out` L103–107): the guard passes at μ_K = 0.03 Mpc⁻¹ (max |v3/law − 1| at R ≤ 1.1 Mpc 0.021 / 0.024,
canonical / alt; line 0.14) and fails at 0.1 Mpc⁻¹ (0.290 / 0.317) on both footings. The true edge lies between the two
grid points. F3/M1/Q6/Q7 graded growth at BS24 Eq. 39's cap, 10 Mpc⁻¹ = 14.8 h/Mpc, which S4 excludes.

**(ii)** Is Q7's large-λ_D DBI door (R_B = 0.95 at λ_D,95) closed by its own consistency (linear |δQ| against the DBI
square-root ceiling λ_D^{-1/2}) and by the record's Lyman-α forest gate?

**Pre-stated expectations** (hand estimates, no code run; written so the reader can see what was expected):
- (i) F3's ODE (J_x kernel, a_i = 1e-3) should give R ≈ 0.08–0.15 at 0.03–0.1 Mpc⁻¹, bracketed by F3's 0.075 at
  0.0232 h/Mpc and 0.391 at 14.8 h/Mpc. The Boltzmann R_B should be lower (Q6 found 0.073 vs 0.391 at the cap).
  The μ_K gap to 0.95 should be ~10³–10⁵.
- (ii) From Q6 D2, the rest-frame δQ equals the khronon's own Yukawa-screened potential,
  δQ_rest ≈ (3/2)Ω_K ℋ² δ_rest /(k² + a²M²). Its per-mode amplitude is expected ≲ 1e-7, below the line (D PASS). The
  forest ratio at the cap point and at P1's μ is expected ≪ 0.8 (FAIL). At P2's μ (0.0448 Mpc⁻¹) the hold scale aM is
  expected near 4 h/Mpc at z = 3 and 1.6 h/Mpc at z = 2, so the forest band may be nearly unsuppressed at z = 3: outcome
  not predictable by hand.

## 1. Unit conversion (stated once, used everywhere)

- S4's μ_K is a **physical** inverse length in Mpc⁻¹ (its static solve is in physical Mpc; "μ_K⁻¹ = 33 Mpc").
- The K(Q) mass μ_K in the action is a physical constant; on FRW the hold acts on comoving k > a·M(a) (M = μ for the
  quadratic K at late times).
- F3 quotes μ_K in h/Mpc at its background A: **μ[h/Mpc] = μ[Mpc⁻¹] / h_A**, h_A = 0.6757803091543079
  (`F3_growth_audit/f3_growth_audit_results.json` K2.A_c2b_refit.params.h). So 10 Mpc⁻¹ = 14.7977 h/Mpc (F3's
  `mu_100kpc`), **0.03 Mpc⁻¹ = 0.044393 h/Mpc**, **0.1 Mpc⁻¹ = 0.147977 h/Mpc**.
- Q6/Q7's CLASS takes μ² directly in Mpc⁻² (`aest_K2`); their cap is 14.8 × 0.67552 = 9.9977 Mpc⁻¹ (HREF = 0.67552).
  This lane passes `aest_K2 = μ²` with μ = 0.03 and 0.1 Mpc⁻¹; no h enters.
- k in CLASS outputs is in h/Mpc; it is converted to Mpc⁻¹ with each run's own h (parsed from CLASS's stdout).

## 2. Step 0: reproductions (each must pass before its step's numbers are read)

| id | what | pass line |
|---|---|---|
| G0a | F3's ODE (`growth_ratio`, `sig8_ratio`, `class_run`, copied verbatim into this lane's script) on background A reproduces F3 K4 at μ = 10/h_A h/Mpc: bsk2 a_i 1e-3 = 0.390800, bsk2 a_i 1e-4 = 0.202602, jeans a_i 1e-3 = 0.120552 | each \|r/r_F3 − 1\| ≤ 1e-4 |
| G0b | Q6's validated binary (`class_khronon`, sha256 3ccb50b2…) at C7's ΛCDM refit (P0): DUST σ₈ 0.827959, LOB 14.8 σ₈ 0.0607512, R_B 0.073375 | each ≤ 1e-4 relative |
| G0c | conversion: 10/h_A equals F3's stored `mu_hMpc` 14.79770846314582 | ≤ 1e-9 relative |
| D0a | Q7's validated DBI binary (`class_dbi`, sha256 d30e764e…) re-run with Q7's committed CAP@l95_best and the vanilla binary with LCDM_best parameters (read from Q7's on-disk .ini files), outputs extended only by z_pk / mTk / vTk / background: z = 0 P(k) reproduces Q7's committed `_pk.dat` files; Q7's best-fit ratios P/P_ΛCDM at k = 0.1 / 1 / 3 h/Mpc (0.97677 / 0.32937 / 0.09799) and σ₈ 0.787585 | max \|Δln P\| ≤ 1e-4 over k ≤ 10 h/Mpc; each ratio within 1e-3 absolute; σ₈ within 1e-5 |
| D0b | Q7's λ_D,95 at fixed parameters (P0): R_B = σ₈(DBI)/σ₈(DUST) at λ_D,95 for cap (7.839652757518063e9, μ 9.997696 Mpc⁻¹), P1μ (3.551214176016054e10, μ 4.484305 Mpc⁻¹), P2μ (3.9782812179748836e9, μ 0.04484305 Mpc⁻¹) | each \|R_B − 0.95\| ≤ 0.002 |
| D0c | δQ extraction validated on DUST (type 0, P0): δ_K extracted from d_tot by subtraction equals d_cdm (the 1e-8 CDM tracer), and θ_K ≈ 0 (synchronous gauge), at every z of §4 and every k ≤ 10 h/Mpc | max \|δ_K/d_cdm − 1\| ≤ 1e-5 and max \|3ℋθ_K/k²\|/\|d_cdm\| ≤ 1e-5 |
| D0d | normalisation: CLASS's P(k, z) equals (2π²/k³) A_s (k/k_p)^{n_s−1} d_m(k, z)² (k_p = 0.05 Mpc⁻¹; h³ unit change) | ≤ 1e-3 relative at every z, k ≤ 10 h/Mpc |
| D0e | background: the analytic DBI ρ_K(a) (BS24 Eq. 88/89, Q7's cancellation-free form, I₀ solved from Ω_aest as CLASS does) equals CLASS's (ρ_tot − ρ_g − ρ_b − ρ_cdm − ρ_ur − ρ_Λ) from its background file; own I₀ equals the I₀ CLASS prints | ≤ 1e-6 relative at every z of §4; I₀ ≤ 1e-8 relative |
| F0a | L346's gate reproduced from its committed JSON (`real_research/g03_audit_2026/L346_switch_forest_gate_results.json`): with this lane's gate function, sw5_canon z = 3 band 1.06–1.22, sw5_alt z = 3 1.07–1.25, verdict FAIL; never_on/LCDM ratio exactly 1 (PASS) | band ends within 0.005 of L346's printed values; verdicts equal |
| F0b | L319's strict line reproduced: T²_5.3keV(k = 5 h/Mpc) with L319's formula and cosmology (`real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py` L169–171, h 0.6736, ω_b 0.02237, ω_c 0.1200) = 0.995 (L319 .out L43) | within 5e-4 |
| F0c | the gate on ΛCDM through this lane's CLASS pipeline: DUST (DBI binary, type 0) vs vanilla ΛCDM at P0, and DBI(λ_D = 1e30, cap) vs DUST, at z = 3 and z = 2 | every L346 bin within 1e-3 of 1; T²(k = 5) within 1e-3 of 1 ⇒ gate PASS |

If a reproduction fails, its step's numbers are still printed but carry no verdict weight; the verdict for that step is
UNDECIDED (reproduction failed), unless an amendment written before reading the step's numbers fixes a non-physics cause.

## 3. Step 1, question (i): growth at the native cap

**Runs.** μ_K ∈ {0.03, 0.1} Mpc⁻¹ only (no other μ_K; stop rule §7).
- **ODE** (F3's, copied): background A, CLASS dust-limit P(k), columns bsk2 (J_x) a_i = 1e-3 (**primary ODE column**, the
  0.391 column) and a_i = 1e-4 (reported); the jeans column only where F3's own skip rule allows it
  (3/(a_i μ_h) ≤ 3000), otherwise reported as skipped.
- **Boltzmann** (Q6's validated LOB, `aest_K_type` 4, j₁ = −1, `aest_K2` = μ²) at P0 with Q6's precision settings, against
  DUST at P0: R_B = σ₈(LOB)/σ₈(DUST). Each CLASS process must stay < 1 GB and < 30 min; if CLASS refuses or exceeds the
  limits, the Boltzmann number is reported missing and the ODE alone is used (said plainly).
- Reported only: ΔN_eff,equiv(1 MeV) of the literal quadratic background at the two μ (Q7's `rho8`/`dneff` algebra with
  λ_D = 0), to state that LOB (dust background) is not the literal theory there either.

**Checks.**
- G1 (monotone sanity): for each estimator and column, R(0.03) ≤ R(0.1) ≤ R(cap) (cap values: F3 K4 / Q6 R_B 0.073375).
- G2: both Boltzmann runs complete within the limits (FAIL is allowed and is then reported; verdict falls to the ODE).

**Gap factors (both reported, with JSON keys).**
- (g1) σ₈ shortfall = 0.95 / R at 0.03 and 0.1 Mpc⁻¹, for R_B and for the ODE columns.
- (g2) μ_K gap = μ_K,95 / μ_K,guard with μ_K,guard ∈ {0.03, 0.1} Mpc⁻¹ and μ_K,95 inherited:
  F3 K5 361 / 411 / 2542 h/Mpc (× h_A → Mpc⁻¹) and Q6's Boltzmann "> 2542 h/Mpc" (× 0.67552; a lower bound, so its gap
  is a lower bound). Not recomputed (no μ_K scan).

**Verdict classes for (i)** (primary estimator R_B; ODE if R_B is missing):
- **GROWTH FAILS AT THE NATIVE CAP**: R(0.1) < 0.95 on the primary estimator **and** on the primary ODE column (the ODE
  start-time choice a_i = 1e-3 overstates growth, F3). With G1 monotonicity this bounds R at the true guard edge.
- **GROWTH PASSES AT THE NATIVE CAP**: R(0.03) ≥ 0.95 on the primary estimator.
- **UNDECIDED**: anything else (straddle, or the estimators on opposite sides of 0.95, or G1 fails).

## 4. Step 2, question (ii): the DBI door

**Points (all pre-declared; no λ_D or μ scan).** Q7's three committed λ_D,95 values (§2 D0b):
- **cap** (μ 9.997696 Mpc⁻¹, λ_D 7.839652757518063e9): **primary** = Q7's CMB best fit CAP@l95_best (Δχ² +1.58),
  compared with Q7's ΛCDM best fit LCDM_best; reported = fixed parameters P0 vs DUST at P0.
- **P1μ** (4.484305 Mpc⁻¹, 3.551214176016054e10) and **P2μ** (0.04484305 Mpc⁻¹, 3.9782812179748836e9): fixed
  parameters P0 vs DUST at P0 (Q7 fitted neither; no fit is run here).

**Outputs per run.** z_pk = {0, 0.5, 1, 2, 3, 5, 10, 20, 37, 60, 100, 200, 500}; mPk, mTk, vTk (synchronous gauge,
CLASS format, normalised to initial curvature 1), background file; Q7's precision settings and P_k_max_h/Mpc = 10. If
CLASS refuses a z, the run is repeated once with the z values above the refused one removed, and the reduced grid is
logged (technical fallback, pre-declared).

**D, the consistency check (the task's line).**
- Extraction (synchronous gauge): δρ_K = d_tot·ρ_tot,noΛ − Σ_{g,b,cdm,ur} ρ_i d_i; (ρ+p)_K θ_K = t_tot·Σ(ρ+p) −
  Σ_{g,b,ur}(ρ_i+p_i)θ_i (θ_cdm = 0). CLASS's d_tot excludes ρ_Λ (its source code, `perturbations.c` delta_tot).
- Rest-frame (gauge-invariant, Q6 D2: δQ_rest = −Q̄Ξ): δ_rest = δ_K + 3ℋ(1+w)θ_K/k²;
  **δQ_rest = 8πGρ̄_K c_s²(k,a) δ_rest / K′** with c_s² = Q̄K′/(Q̄²K″ + 2k²/a²), K″ = 2μ²r³, Q̄ = 1 + Z/r, Z = K′/(2μ²),
  r = √(1 + λ_D Z²), K′ = I₀/a³ (Q7 dbi.patch; BS24 Eq. 71). Reported alongside: synchronous-gauge δQ = 8πGδp/K′ (Q6 D2,
  all gauges) with CLASS's own δp/ρ formula.
- Physical amplitude: Δ_δQ(k,z) = √(A_s (k/k_p)^{n_s−1}) · |T_δQ(k,z)| per ln k; σ_δQ(z) = [∫ Δ²_δQ d ln k]^{1/2} over the
  CLASS k grid with k ≤ 10 h/Mpc (trapezoid in ln k).
- **Line L = λ_D^{-1/2}/3** (so that a 3σ linear excursion stays inside the ceiling): cap 3.765e-6, P1μ 1.769e-6,
  P2μ 5.285e-6.
- **D_p = FAIL** if max_z σ_δQ,rest > L **and** max_{k,z} Δ_δQ,rest > L; **PASS** if both ≤ L; **UNDECIDED** otherwise.
- Reported only (no verdict weight): the headroom ratio max_z 3σ_δQ,rest(z)/[λ_D^{-1/2} − (Q̄(z) − 1)]. Near the ceiling
  K′ diverges, so the rest-frame Q cannot be pushed through it by density alone; a ratio above 1 means linear theory is
  invalid there, not that the root is complex. The static-branch cluster estimate (Q7: λ_D^{-1/2} = 1.02 / 0.48 / 1.42 ×
  v²/c² of a 1000 km/s cluster) is inherited and reported, not re-graded.

**F, the forest gate (linear P(k); the record's gates).**
- **F_L346** (the gate the task names; L346 F2): P_model/P_ref at L346's six bins k = 1.10, 1.39, 1.76, 2.23, 2.81,
  3.56 h/Mpc, at z = 3 **and** z = 2, must lie in **[0.8, 1.2]**. L346 applied it to nonlinear PM matter power; here it is
  applied to linear CLASS P(k) (no PM simulation is allowed in this rebuild).
- **F_L319** (the record's linear, WDM-calibrated gate; L319/L168): T²(k = 5 h/Mpc) = P_model/P_ref at z = 3 **and** z = 2
  ≥ T²_5.3keV (strict, F0b) ; loose reading ≥ 0.9.
- Reference: cap primary vs LCDM_best (both CMB best fits); every fixed-parameter point vs DUST at P0 (= ΛCDM, F0c).
- **F_p = FAIL** if F_L319 loose fails at z = 3 or z = 2, **or** the worst L346 bin at z = 3 or z = 2 lies outside
  [0.5, 2.0] (a factor ≥ 1.6 beyond the band edge: a pre-declared margin so that a linear-only failure is not one that
  nonlinear refill could plausibly erase). **F_p = PASS** if F_L346 passes and F_L319 strict passes. **UNDECIDED**
  otherwise. z = 3 alone is also reported (the task's "z ~ 3").

**G, the galaxy guard (inherited from S4, not recomputed).** G_p = FAIL if μ ≥ 0.1 Mpc⁻¹, PASS if μ ≤ 0.03,
NOT ON S4'S GRID otherwise (P2μ). Reported with the DBI-vs-quadratic size λ_D (v²/c²)² at v = 220 km/s, which says whether
S4's quadratic-K static solve applies to the DBI K in galaxies.

**Verdict classes for (ii).**
- **DOOR CLOSED** (naming the check(s): BY D / BY F / BY D AND F, per point): every point has D_p = FAIL or F_p = FAIL.
- **OPEN BUT A KNOB (cannot be adopted)**: at least one point has D_p = PASS and F_p = PASS. λ_D is set by the failure
  (rule 4), so the door is reported, never adopted; that point's G status is stated.
- **UNDECIDED**: anything else (or a §2 reproduction for step 2 fails).
- Also printed: the reading restricted to points not already excluded by G.

## 5. MUTATE controls (each must FAIL at least one check; outputs `*_MUTATE.out` / `*_results_MUTATE.json`)

- Step 1 script, `X4_MUTATE=1`: the copied ODE kernel is replaced by s ≡ 1 (no hold) and Q6's MUTATE binary
  (`class_khronon_mutate`) is used. **G0a and G0b must FAIL.**
- Step 2 script, `X4_MUTATE=1`: Q7's MUTATE binary (`class_dbi_mutate`, K″ = 2μ²/r³) for every DBI run, and the extraction
  drops the photon and ur subtraction and the θ term. **D0a and D0c must FAIL.**
- Run directories for the MUTATE runs are separate (`runs_MUTATE`); outputs are named by mode.

## 6. Compute and process rules

- Every process: `OMP_NUM_THREADS=1 nice -n 15`, one CLASS process at a time, < 1 GB RSS, each run ≤ 30 min. The
  heavy-queue status is checked before each script; if free+inactive memory is low, wait. compute_queue/ and other lanes
  are never touched. No PM simulation. No download.
- CLASS run files go outside the repo: `../_external_data/x4_growth_native_cap_2026_10_23/runs[_MUTATE]/` (not committed).
  Committed: scripts, `.out`, `_results.json` (main and MUTATE), README.
- Commits: pathspec of this lane only. Order: this file + `ASSUMPTION_LEDGER.md` alone; then scripts + outputs; then
  README. Every amendment is appended below, labelled PRE-RESULT or POST-RESULT, and committed before the numbers it governs
  where it is pre-result.

## 7. Stop rule

μ_K ∈ {0.03, 0.1} Mpc⁻¹ for step 1; the three λ_D,95 points (plus λ_D = 1e30 as the control) for step 2. No scans of
λ_D or μ_K beyond these, whatever the outcome. No fit is run. A failing number is reported as it falls.

## 8. What the lane will not show (pre-declared)

- No nonlinear growth (L1's question) and no nonlinear forest flux power; F is a linear-P(k) proxy of the record's gates.
- No new S4 static solve (P2μ's guard status stays "not on S4's grid").
- No CMB fit at P1μ or P2μ; their forest numbers are at fixed ΛCDM-refit parameters.
- δQ is linear; the cluster static branch is inherited from Q7, not solved.
- BS24/BS25 equations remain the record's PROVISIONAL WebFetch transcriptions (Q6/Q7).
