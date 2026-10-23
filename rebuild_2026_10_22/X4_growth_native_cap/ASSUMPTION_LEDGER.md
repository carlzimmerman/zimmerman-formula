# X4_growth_native_cap: assumption ledger (before any number; committed with FROZEN_CRITERIA.md)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
Extra labels where needed: FITTED (a constant set from data), POSTULATED (a premise with no derivation), KNOB (a constant
set by the failure it cures; rule 4).

No STANDARD-MOND-MACHINERY enters any number computed here: a₀ is absent at linear order on FRW (Q6 D0). It enters only
through S4's inherited galaxy guard, which is AQUAL with μ = x/(1+x) (FRAMEWORK-NATIVE), on both footings.

## A. Inherited verdicts and numbers (read, not recomputed, except where §2 of the criteria reproduces them)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| A1 | S4's isolated-galaxy guard: passes μ_K ≤ 0.03 Mpc⁻¹, fails ≥ 0.1 (both footings); μ_K physical | FRAMEWORK-NATIVE static solve (quadratic K, AQUAL) on RAW + SURVEY-CALIBRATION lensing data (B21 Fig. 3 ESD, released covariance; F2 lens inventory) | `rebuild_2026_10_22/S4_v3_muK_clusters/README.md` §3; `s4_v3_muk_clusters.out` L100–107; `s4_v3_muk_clusters_results.json` keys `galaxy`, `mu_K_gal` | static, spherical, VSZ zero point; the guard's own caveats are S4's |
| A2 | BS24 Eq. 39 galaxy cap μ_K⁻¹ ≥ 100 kpc (10 Mpc⁻¹) | LITERATURE-INPUT (WebFetch transcription, PROVISIONAL) | F3 K4/K5; C4 | the value S4 excludes |
| A3 | F3's sub-horizon two-fluid ODE: baryons Newtonian at every k; khronon kernel s = a²μ²/(k²+a²μ²) (J_x, j₁ = −1) or 1 − k²/(a²μ²) (j₁ = 0); GR growth δ ∝ a before a_i | kernel FRAMEWORK-NATIVE (Q6 D5 exact); "baryons Newtonian at every k" and the a_i start POSTULATED (F3 states a_i = 1e-3 is an upper bound) | `rebuild_2026_10_22/F3_growth_audit/f3_growth_audit.py` L88–150 | copied verbatim |
| A4 | F3 background A: C2 c2b plik-lite ΛCDM-form refit (h_A 0.67578, Ω_m 0.3129), CLASS dust-limit linear P(k) via classy v3.3.4 | ΛCDM-PROCESSED parameters on a GR form that is FRAMEWORK-NATIVE only in the dust limit; Planck plik-lite SURVEY-CALIBRATION | `F3_growth_audit/f3_growth_audit_results.json` K2.A_c2b_refit | |
| A5 | F3 K5 thresholds μ_K,95 = 361 / 411 / 2542 h/Mpc | FRAMEWORK-NATIVE (ODE) on A4 | F3 results K5.windows | inherited for the gap factor (g2) |
| A6 | Q6's Khronon CLASS (LOB: dust background + literal c_s², j₁ = −1), validated under Q6 AMENDMENT A3 | FRAMEWORK-NATIVE perturbation equations (Q6 D2, from BS24's action) inside a standard GR Boltzmann code; LOB drops the literal a⁻⁶ background term (Q6 A2), i.e. POSTULATED background | `rebuild_2026_10_22/Q6_v3_class/{khronon.patch, PROVENANCE.md, README.md}`; binary `../_external_data/class_khronon_build_2026_10_23/class_khronon/class` | read-only use of the built binary |
| A7 | Q6 R_B = 0.073375 at the cap; μ_K,95 > 2542 h/Mpc (Boltzmann) | as A6 | `Q6_v3_class/q6_native_results.json` stepC | |
| A8 | C7 ΛCDM refit P0 (ω_b, ω_dm, 100θ_s, ln10¹⁰A_s, n_s, τ) used for every fixed-parameter run | ΛCDM-PROCESSED (ΛCDM fit to plik-lite + low-ℓ) | `covariant_push_2026_10_22/C7_aest_class/c7_native_results.json` fits.LCDM | the khronon abundance ω_K = ω_dm is a FITTED initial condition |
| A9 | Q7's DBI K = (2μ²/λ_D)[1 − √(1 − λ_D(Q−1)²)] in CLASS (`aest_K_type` 5), validated under Q7 AMENDMENT A1 | form LITERATURE-INPUT (BS24 §4 / BS25, PROVISIONAL WebFetch); equations FRAMEWORK-NATIVE (S7/S8 identical to Q6's) | `rebuild_2026_10_22/Q7_bs25_cosmology/{dbi.patch, PROVENANCE.md}`; binary `../_external_data/class_khronon_dbi_build_2026_10_23/class_dbi/class` | read-only use |
| A10 | λ_D,95 at cap / P1μ / P2μ (7.84e9 / 3.55e10 / 3.98e9) | KNOB (set by the σ₈ failure; never adopted) | `Q7_bs25_cosmology/q7_native_results.json` scans.*.lambda_D_95 | graded here, not adopted |
| A11 | Q7's CMB best fits CAP@l95_best and LCDM_best (parameters from the on-disk .ini files) | the DBI fit: FRAMEWORK-NATIVE linear sector fitted to SURVEY-CALIBRATION data (plik-lite); LCDM_best ΛCDM-PROCESSED | `../_external_data/class_khronon_dbi_build_2026_10_23/runs_native/{CAP@l95_best_,LCDM_best_}.ini` and `_pk.dat`; Q7 JSON fits | read-only |
| A12 | P1 / P2 μ values (μ⁻¹ = 223 kpc, 22.3 Mpc) | LITERATURE-INPUT (BS24 Fig. 1 caption, PROVISIONAL) | Q7 README §1 | used only as Q7's μ points |
| A13 | Q7's static-branch ceiling estimate (|Q−1| ≈ |φ|/c² ≳ v_c²/c²) | LITERATURE-INPUT (BS25 Eqs. 11/13, PROVISIONAL) + order-of-magnitude | Q7 README §5 | reported, not graded |
| A14 | L346's forest gate: P/P_ΛCDM ∈ [0.8, 1.2] at k = 1–4 h/Mpc (six PM bins), z = 3 and 2 | LITERATURE-INPUT summarised as "the record's standing criterion" (forest P(k) constraints are inferred with ΛCDM hydro simulations: ΛCDM-PROCESSED) | `real_research/g03_audit_2026/L346_switch_forest_gate.py` L16–38, L255, L285; `.out`; `_results.json` | the record applied it to nonlinear PM power; here to linear power (proxy, stated) |
| A15 | L319's strict forest line T²(k = 5 h/Mpc) ≥ T²_5.3keV = 0.995 at z = 3 and 2 (Iršič+2017 thermal-relic bound; Viel+2005 transfer fit α = 0.049 m^-1.11 (Ω/0.25)^0.11 (h/0.7)^1.22, ν = 1.12); loose ≥ 0.9 | LITERATURE-INPUT, ΛCDM-PROCESSED (WDM bounds come from ΛCDM-based hydro calibrations); L319's cosmology h 0.6736 ΛCDM-PROCESSED | `real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py` L21–24, L169–171, L185; `.out` L43 | the record's linear forest gate |
| A16 | CLASS v3.3.4 core (photons, baryons, neutrinos as massless ur N_ur 3.044, recombination, reionisation) | standard GR physics; SURVEY-CALIBRATION inputs (T_cmb, Y_He from BBN tables) | C7 PROVENANCE | unchanged by the patches outside the khronon sector |

## B. This lane's own ingredients

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | unit conversion μ[h/Mpc] = μ[Mpc⁻¹]/h_A; μ physical in S4 and in the action | FRAMEWORK-NATIVE bookkeeping | criteria §1 | |
| B2 | the two step-1 values μ_K = 0.03 and 0.1 Mpc⁻¹ | S4's grid points that bracket the guard edge (A1) | criteria §3 | no other μ_K |
| B3 | δQ relations: 8πGδp = K′δQ (all gauges); δQ_rest = −Q̄Ξ (π = 0); 8πGδρ_rest = −(Q̄²K″ − 2j₁k²/a²)Ξ; δp_rest = c_s²δρ_rest ⇒ δQ_rest = 8πGρ̄ c_s² δ_rest/K′ (j₁ = −1) | FRAMEWORK-NATIVE (Q6 D2, sympy-exact from BS24's action) | `Q6_v3_class/q6_derive.py` L203–227; `.out` D2 lines | linear only |
| B4 | extraction of δ_K, θ_K from CLASS's d_tot/t_tot by subtraction (synchronous gauge) | numerical method | criteria §4 | validated on DUST (D0c) |
| B5 | physical normalisation by A_s (k/k_p)^{n_s−1}, k_p = 0.05 Mpc⁻¹, transfer functions for unit initial curvature | standard (CLASS convention) | CLASS tk header | checked by D0d |
| B6 | line L = λ_D^{-1/2}/3 (a 3σ linear excursion stays inside the ceiling) | task-declared consistency line | criteria §4 | |
| B7 | F margin [0.5, 2.0] for a decisive linear-only failure of the L346 band | pre-declared convention of this lane (not from the record) | criteria §4 | labelled as such |
| B8 | z grid {0, 0.5, 1, 2, 3, 5, 10, 20, 37, 60, 100, 200, 500}; k ≤ 10 h/Mpc | numerical choice | criteria §4 | a maximum between grid points can be missed (stated) |
