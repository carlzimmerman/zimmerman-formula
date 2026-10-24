# X18_beta_growth_forest: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½), ILLUSTRATIVE, ADOPTED (a posed choice, not derived) and METHOD.

| id | ingredient | class | where | used here as |
|---|---|---|---|---|
| A1 | v3s + C1 (the K² term, B = β/(2+3β)); window β_min(foot) / β_max(μ_K) | FRAMEWORK-NATIVE record (X14 SYMPY/NUM; upper edge from C5's IR-band estimate) | X14 JSON; X15/X17 S0-2 | graded β grid (§4); never fitted |
| A2 | khronon linear dispersion with C1 at general M_θ, M_θ ∈ [1 + x, (1 + x)²] | FRAMEWORK-NATIVE (SYMPY record: X3 B1-S, X14 `disp`, X17 S0-3) | X17 script L345–381 (copied) | Q-KER, Q-DISP, the saturated kernel s_M |
| A3 | the record's dust kernel s(k; f₀) = (μ² − f₀k²)/((1 − f₀)k² + μ²) | FRAMEWORK-NATIVE (M1 SYMPY; Lean `kernel_*`) | V3_FULL_PICTURE §4.2 | identification s_M = s(k; 1 − 1/M) (stated, checked by Q-KER) |
| A4 | X14's hold-flux cap identity 𝒰(y) = a₀y/(a₀ − \|y\|) (inverse of the simple-μ Gauss law) | FRAMEWORK-NATIVE (X14, coordinator hand-checked) | V3_FULL_PICTURE §6 X14 bullet | x = y/(1 − y); CAP flag at y ≥ 1 |
| A5 | the perturbation's acceleration per ln k, y_k = Kρ̄_τΔ_τk_p/(k_p² + μ²)/a₀ | METHOD (the linear Gauss law at M = 1 incl. the μ_K term, then A4; WKB per-ln-k amplitude) | §1 | Step 1 |
| A6 | brackets S (own amplitude) and E (cumulative rms over k' ≤ k) | ADOPTED (two WKB readings of "the background a mode sees"; both graded, verdict needs agreement) | §1, §6 | Step 2 brackets |
| A7 | orientation brackets ⊥ (M = 1 + x), ∥ (M = (1 + x)²) | FRAMEWORK-NATIVE limits (record M_T, M_L); averaging not computed | §1 | Step 2 brackets |
| A8 | F3/X4 two-fluid sub-horizon ODE, growing-dust start at a_i, radiation in E(a); X17's C1 version (`growth_C1`) | FRAMEWORK-NATIVE record (ODE is an upper-bound convention, X4) | X17 script L442–491, L896–934 (copied verbatim) | S0-2, S0-3, all cells |
| A9 | background A (C2b refit: ω_b, ω_cdm, h, ln10¹⁰A_s, n_s, τ) and its CLASS z = 0 linear P(k) | LCDM-PROCESSED (as X4/X17) | F3 JSON `K2.A_c2b_refit` | Δ_A(k) normalisation of y_k; σ₈ convention |
| A10 | a₀(z) = κc√(Gρ_DE(z)), constant for constant Λ | FRAMEWORK-NATIVE standing statement; κ = ½ FITTED | record standing rule | a₀ constant per footing |
| A11 | footings a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | X17 `FOOT` | never pooled |
| A12 | μ_K = 0.1 and 0.03 Mpc⁻¹ (physical) | FRAMEWORK-NATIVE record (S4 edges) | X17 `MUK` | grids |
| A13 | L346 forest band [0.8, 1.2] at its six bins, z = 3 and 2 | LITERATURE-INPUT, ΛCDM-PROCESSED (X4 A14) | `real_research/g03_audit_2026/L346_switch_forest_gate.py` L16–38, L255, L285; its JSON | F_L346 (on quasi-linear 3D power, proxy) |
| A14 | L319 line T²(k5) ≥ T²_5.3keV = 0.99519 (Iršič+2017 bound, Viel+2005 fit); loose 0.9 | LITERATURE-INPUT, ΛCDM-PROCESSED (X4 A15) | `real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py` L169–171, L184–185 | F_L319 |
| A15 | [0.5, 2.0] decisive-failure margin | X4's pre-declared convention (X4 B7), reused unchanged | X4 FROZEN_CRITERIA §F | F = FAIL rule |
| A16 | [0.95, 1.05] σ₈ band | ADOPTED (this lane; reported only) | §6 | report line |
| A17 | P1D projection to k = 50 h/Mpc on the lane grid | METHOD (reported only) | §5 | report line |
