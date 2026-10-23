# F3_growth_audit FROZEN CRITERIA (2026-10-22): the growth / cosmic-shear failures and the growth no-go, re-audited against the covariant screened theory (THEORY_V3_DRAFT)

Written and committed alone, before any script or number of this lane. Rules: `rebuild_2026_10_22/BRIEF.md`,
`doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled.
No dark-matter particle (the cold sector is "cold energy" / BS K(Q) dust). Never "theory closed". Never "the data favour
the framework". No PM simulation; CFG960 (running) is not touched or duplicated. Every run: `OMP_NUM_THREADS=1 nice -n 15`,
< 1 GB RSS, minutes. No downloads.

## 0. What is audited

- (a) CFG555/CFG556: growth on the full gravitating mass 15–19 % too clumpy at 512³ (max|P−1| 0.150–0.193; σ8 +3–5 %).
- (b) CFG596: canonical settling rules EXCLUDED by raw KiDS-1000 ξ± (Δχ² +68.7, S0 χ² 144.3, F 213.0, N_kept 104).
- (c) Status board column 5: "Fails: one local theory that gives the law, a¹ growth and no external-field effect"
  (CFG941 theorem D-T, CFG944, CFG946 theorem T-O2, CFG947).

## 1. Assumption ledger (classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSITED RULE)

POSITED RULE = a rule of the PM engine that no action in the record produces (added class; CFG941 (g), CFG947, CFG955).

### 1a. The PM engine (CFG424 → 518 → 521 → 524 → 527 lineage; lean copy `CFG596_lean_pm_1024/cfg596_pm.py`)

| ingredient | what the engine does | class | file |
|---|---|---|---|
| initial spectrum | Eisenstein–Hu no-wiggle T(k), n_s = 0.965, normalised to σ8 = 0.811 at z = 0, back-scaled by ΛCDM D(a) to z_i = 49 (Zel'dovich) | ΛCDM-PROCESSED (Planck-2018 ΛCDM fit values; EH fitting form) | `cfg527_pm.py` L109-133, L248-262 |
| physical densities | h = 0.6736, ω_b = 0.02237, ω_c = 0.1200 (Ω_m 0.3153) | ΛCDM-PROCESSED (Planck-2018 ΛCDM) | `cfg527_pm.py` L102-104 |
| background | flat w = −1 GR, E(a) = √(Ω_m a⁻³ + Ω_Λ), massless ν, no radiation | ΛCDM-PROCESSED (values) / FRAMEWORK-NATIVE in form (C2: dust-limit background is GR) | `cfg527_pm.py` L110 |
| cold-sector EoM | the cold share rides on the same collisionless particles as baryons (one species, Newtonian −∇Φ); no own field, no pressure, no Jeans scale | POSITED (CFG941 (g): "universal −∇Φ for all cold particles"); differs from BS dust (c_s² = (Q̄−1)/Q̄, C5) | `cfg527_pm.py` forces() |
| "gravitating field" | Newtonian Φ of ALL particles **plus** an additive QUMOND-type phantom source s_ph = −∇·[(ν−1) g_N,b] built from the (filtered, f_ret-weighted) baryon Newtonian field, kernel ν_mono(y) = 1/(1−e^{−√y}) monotonised | STANDARD-MOND-MACHINERY (QUMOND phantom, additive on top of Newtonian dust; not AQUAL μ = x/(1+x)) | `cfg527_pm.py` L410-433 |
| settling rule | tidal switch f_sw (λ₂ vs Δ_ta, ε = 0.077), census edge (5.364/f_ret r_M), turnaround catchments, excess e = f_sw max(s_ph − s_c, 0), compensation drawn from the shell (zero-sum per catchment), cap q ≤ 1, f_ret(M) census table, RMIN | POSITED RULE (no action produces it: CFG941, CFG947, CFG955); f_ret mixed provenance (CFG886) | `cfg527_pm.py` L376-391, L434-466, L300-316 |
| Δ_ta(z) | turnaround table from a ΛCDM spherical shell ODE | ΛCDM-PROCESSED | `cfg527_pm.py` L140-160 |
| a₀ | canonical 9.3603e-11 / alt 1.1312e-10, flat in z (FLAT) | FRAMEWORK-NATIVE (κ = ½ FITTED) | `cfg527_pm.py` L105 |
| comparison model S0 | same engine, switch off: Newtonian collisionless dust on the same ICs | same-pipeline control (inherits the ΛCDM-PROCESSED ICs/background) | CFG596 README |

### 1b. The KiDS likelihood (`CFG592_cosmic_shear_likelihood/cfg592_native.py`, library part exec'd unchanged by CFG596)

| ingredient | class |
|---|---|
| KiDS-1000 ξ± data vector (`xipm_KIDS1000_*.fits`) | RAW (survey-reduced shear 2-pt; measurement) |
| covariance (analytic, survey's fiducial cosmology) | SURVEY-CALIBRATION (with a ΛCDM fiducial inside the covariance model) |
| n(z) (SOM) and the Δz prior (SOM covariance, mean shifts) | SURVEY-CALIBRATION |
| shear bias m (inside the KiDS covariance; DES m priors) | SURVEY-CALIBRATION |
| IA: NLA, C1ρ = 0.0134, A_IA free in [−6, 6], growth factor from the PM ΛCDM D(z) | SURVEY-CALIBRATION (model) + ΛCDM-PROCESSED (D(z)) |
| projection background χ(z): flat w = −1, Ω_m 0.3153 ("PM"); DESI CPL variant | ΛCDM-PROCESSED |
| P(k, z) between snapshots: log-linear in z over nodes 0/0.5/1, D² above z = 1; EH below k_lo; power law above k_hi | ΛCDM-PROCESSED (EH, D) at the edges |
| support cut (≥ 90 % of the |integrand| inside [k_lo, k_hi]), N_kept ≥ 10 | pipeline rule |
| statistic Δχ²(F − S0), classes EXCLUDED/TENSION/CONSISTENT/NOT DIAGNOSTIC, T-OWN tooth | pipeline rule (T-OWN post-hoc vs CFG592, disclosed) |

### 1c. The covariant theory (THEORY_V3_DRAFT; C2, C4, C5) and this lane's rebuild

| ingredient | class | file |
|---|---|---|
| action: BS Khronon + J_x (μ = x/(1+x), AQUAL static limit) + K(Q) dust + γ_L stiffness | FRAMEWORK-NATIVE (J_x POSTULATED, outside BS's admissible class; C4) | C4, THEORY_V3 §1 |
| K(Q) = μ_K²(Q−1)² (BS24 Eq. 7), c_s² = (Q̄−1)/Q̄ | FRAMEWORK-NATIVE (external transcription BS24, PROVISIONAL; C4) | C4, C5 |
| μ_K, the K(Q) mass | NOT IN THE v3 PARAMETER TABLE; BS24 Eq. 39 demands μ_K⁻¹ ≫ 100 kpc (galaxies) — external premise | C4 L45, L95 |
| dust abundance (Ω_c-like) | FITTED (initial condition I₀) | C2 K2, C4 |
| A_s, n_s, ω_b, ω_c, θ_s, τ | FRAMEWORK-NATIVE in the dust limit (the dust-limit linear sector is ΛCDM's, C7 V1); values from the record's own plik-lite refit (C2 c2b P5, g = 1); plik-lite foreground compression = SURVEY-CALIBRATION | `C2_aest_cosmology/c2b_native_cmb_results.json` |
| native background alternative | CFG886 GR fit (BAO + BBN, no CMB): Ω_m 0.2976, h 0.6856 | C2 K5/K7 |
| linear growth "GR on dust, γ = 0.555" | FRAMEWORK-NATIVE **for AeST** (J ∝ Y^{3/2}, J′(0) = 0); to be re-checked for v3's J_x (this lane, K1) | C2 K7 |
| BS dust linear kernels | (i) Jeans form from C5's c_s²; (ii) BSK2 kernel s = μ²a²/(k²+μ²a²) (record, `real_research/bs_khronon_2026/BSK2_frw_dust_sigma8.py`; baryons Newtonian at every k is BSK2's premise) | C5; BSK2 |
| linear P(k) | vanilla CLASS (classy 3.3.4, massless ν, N_ur 3.044) = the dust limit | tool |

## 2. Checks (script `f3_growth_audit.py`; one line per check; exit 0 iff all pass)

- **K0 reproduction (must pass before any verdict).** Re-score CFG596 canonical (P0 S0, P1 RES) on KiDS with the exec'd
  CFG592 library and the CFG596 node construction: S0 χ²_min, F χ²_min and Δχ² must match `cfg596_native_results.json`
  (144.26 / 212.99 / +68.73) to |Δ| ≤ 0.05.
- **K0b reproduction.** BSK2's σ8 ratio at BS24's μ (0.037) and its floor μ ≥ 1.1e3 h/Mpc reproduced by this lane's own
  integrator with BSK2's cosmology and a_i = 1e-4, to 10 % relative.
- **K0c reproduction.** C2 K7 f(0) = 0.5105 on the CFG886 background reproduced to 1e-3 by this lane's growth solver; and
  CLASS's f(z = 0) at the same densities within 1 %.
- **K1 (symbolic, sympy).** (i) For v3's J_x: J_x′(Y → 0) = −1, so the lapse-gradient coefficient 1 + J′ vanishes at Y = 0 (FRW)
  and the linear equations about FRW are NOT GR's on k ≫ aμ_K. PASS = the identity holds exactly. (ii) For K = μ²(Q−1)²:
  the Jeans wavenumber k_J² = 4πGρ_K/c_s² (8πGρ_K = QK′ − K, c_s² = K′/(QK″)) equals μ²Q̄² exactly, i.e. the dust's Jeans
  scale IS the static mass of the μ²ψ term. PASS = exact.
- **K2 (dust-limit linear prediction).** σ8 and S8 = σ8√(Ω_m/0.3) from CLASS at (A) the C2 c2b g = 1 refit and (B) the CFG886
  background with (A)'s A_s, n_s, ω_b. Reported, plus (C) the PM IC σ8 = 0.811 for reference. PASS = finite and CLASS
  self-consistent (σ8 from CLASS vs own integral of CLASS P(k) to 1e-3).
- **K3 (linear KiDS comparison).** Model: (A) and (B) linear P(k, z) (CLASS at z nodes, no nonlinear correction), projected on the
  model's own Ω_m background. Kept points: published cuts AND ≥ 90 % of the |integrand| at k ≤ k_lin. Primary k_lin = 0.2 h/Mpc;
  variant 0.3 h/Mpc (quasi-linear). Nuisances: the library's (Δz SOM prior, NLA IA marginalised). Reported: N_kept, χ²_min,
  p (χ²_data, N_kept dof), and the data-preferred amplitude A (P → A·P, a MEASUREMENT of the amplitude, not a model knob)
  with its Δχ² = 1 interval, and the implied S8,data = S8,pred·√A.
  - Class (frozen): NOT DIAGNOSTIC if N_kept < 10 or σ_A > 0.3; else TENSION if |A − 1| > 2σ_A; else CONSISTENT.
  - PASS = the computation completes (the class is a result, not a gate).
- **K4 (BS dust at finite μ_K).** σ8 ratio to the dust limit (both kernels; a_i = 1e-3 optimistic start with GR modes, and
  BSK2's a_i = 1e-4) on background (A), at μ_K⁻¹ = 100 kpc physical today (BS24 Eq. 39 edge), at BSK2's floor 1.1e3 h/Mpc and at
  BS24's 1/43 h/Mpc; plus μ_min for ratio ≥ 0.95 (a derived bound by root finding, not a fit). PASS = μ→∞ limit reproduces
  the dust limit to 1e-4.
- **K5 (the μ_K window).** Window = [μ_min(σ8 ratio ≥ 0.95, Jeans kernel, a_i = 1e-3), μ_max(BS24 Eq. 39: μ⁻¹ ≥ 100 kpc)].
  PASS = computed. Result EMPTY or not is a finding.
- **K6 (no-go premises, EFE price).** 1D AQUAL (μ = x/(1+x)) internal boost of a satellite with g_N,in = 0.01 a₀ isolated vs in a
  host field g_ext = 0.11 a₀ (MW at 100 kpc), both footings irrelevant (a₀ units). PASS = the ratio differs from 1 by > 10 %
  (an EFE exists, i.e. v3 violates the no-go's "no EFE" premise by construction).
- **MUTATE** (`F3_MUTATE=1`, outputs `*_MUTATE.*`): K1(i) uses AeST's J ∝ Y^{3/2} in place of J_x (must FAIL K1(i)), and K0 uses
  B ≡ 1 for F (Δχ² → 0, must FAIL K0).

## 3. Verdict rules per failure

For each of (a), (b), (c), exactly one of:
- **INHERITED BY THE COVARIANT THEORY** (with the number from K2–K5): the failure's cause is in v3's own action/linear sector.
- **BELONGS TO THE SETTLING RULES ONLY**: the failure statistic is carried by a POSITED RULE (1a) that v3 does not contain.
- **UNDECIDABLE WITHOUT A NATIVE SIM**: name the sim (field equation, species, parameters, box, statistic).

A failure can carry two labels for two distinct parts (e.g. the settling-rule part and v3's own nonlinear part); each part is
stated with its number. Nothing here re-scores CFG596's frozen verdict; the CFG596 verdict stands as frozen.
