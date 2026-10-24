# X22_cosmic_dust_window — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, alone, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / LITERATURE-INPUT / LANE CHOICE.
This lane makes no new data product. It reproduces record numbers and combines them with a linear ODE and closed-form
statics. Paths are relative to the repository root.

## 1. Theory settings

| input | class | source |
|---|---|---|
| v3s frozen; the cosmic cold component ("cold energy") is gravitating field mass, Ω_c/Ω_b = 5.364, needed as dust from z ≈ 1100 | FRAMEWORK-NATIVE requirement (record's cosmic ratio) | `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`; X19 row 19 |
| κ = ½; a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FRAMEWORK-NATIVE (κ FITTED) | doors BRIEF, X6 |
| a₀ absent at linear order on FRW (forest/σ₈ side footing-independent) | FRAMEWORK-NATIVE (record result) | Q6 D0, X4 README |
| a separate dust sources the law like baryons and falls at the full g | FRAMEWORK-NATIVE (record derivation) | X6 X-D5, X-D6 |

## 2. Record results used as inputs (read-only)

| input | used for | class of its own inputs | file |
|---|---|---|---|
| L346 forest gate (bins, sw5 bands, band [0.8, 1.2]) | S0-1, forest class | PM matter power vs ΛCDM (ΛCDM-PROCESSED reference); band LITERATURE-INPUT | `real_research/g03_audit_2026/L346_switch_forest_gate_results.json` |
| L319 WDM line: T² = [1+(αk)^{2ν}]^{−10/ν}, ν = 1.12, α = 0.049 m^{−1.11}(Ω_m/0.25)^{0.11}(h/0.7)^{1.22}; 5.3 keV strict, 0.9 loose | S0-2, the cut family | LITERATURE-INPUT (WDM fitting formula, ΛCDM-calibrated) as transcribed in L319 L169–171 | `real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py` |
| X4's F_p rule and F0a/F0b numbers | forest class, S0-1/2 | as above | `rebuild_2026_10_22/X4_growth_native_cap/` |
| X6's SPARC d2 machinery, D-F profile, f_d,max, NGC 3198 deviation, f_c | S0-3/4, Step 2 | SPARC rotmod RAW; Υ grid and weights record conventions; D-F profile (M ∝ r to r_ta, δ_ta 5.55) a record estimator, not a simulation | `rebuild_2026_10_22/X6_dust_coupling/`, `real_research/data/sparc_data/*_rotmod.dat` |
| X19 class table (ρ_b, x, ρ_env, e, kT, N_orb, H) and background bands | S0-5, Step 3C | as X19's ledger (h 0.672, Ω_b 0.049 ΛCDM-PROCESSED conventions; Chae env for e) | `rebuild_2026_10_22/X19_selector_rank_test/x19_classes.csv` |
| BBKS + Sugiyama transfer and the rms-peculiar-gravity construction | σ₈ weights, g_rms (reported) | LITERATURE-INPUT fitting formula as transcribed in the record ("first-pass accuracy") | `prep_2026/mi_linear_cosmology/mi_growth.py` |
| μ-pincer Part F and its 4 km/s control | context, reported comparison | record | `qwen_claude_field_theory/closure_2026/condensate_pincer_2026/CONDENSATE_MU_PINCER_VERDICT.md` |
| CFG944 Theorem G (local L(θ,u) tethers cannot be off in the linear universe) | action search, 3C | record | `campaign_fresh_gravity/LEDGER.md` (CFG944 row) |

## 3. Literature values not in the record (PROVISIONAL)

| value | use | note |
|---|---|---|
| forest absorbers at z ≈ 2–3 trace baryon overdensity δ_b ≈ 0.1–10 (loose bound 100) | set C for the δ_b key | from memory, not looked up; the verdict line uses the loose bound 100 as well, and is reported for both |

## 4. Lane choices (all window-favourable unless stated)

| choice | direction |
|---|---|
| captured fraction from a frozen cut = T²(k_L) (power), not T (amplitude) and not nonlinear refill | favours a window (less cold mass in galaxies) |
| Lagrangian mass M_L = (Ω_m/Ω_b) M_b; k_L = π/R_L (half-mode convention) | neutral; the same convention as M_hm |
| α_NF (forest not FAIL) as the verdict-bearing forest cut, not α_PASS | favours a window |
| hydrostatic profile normalised to the cosmic mean at r_ta (not the overdense r_ta region); flat well at V_obs(R_last); β cap 2.9 | favours a window (lower content) |
| growth ODE from a_i = 1e-3 with both fluids on the growing mode, no radiation, baryons pressureless | the record's ODE convention (F3/X4); linear only |
| time power p graded on a frozen grid, never adopted | no knob fitting |
| per-footing f_max (X6's 0.027 is both footings jointly) | per footing as the rule demands |

## 5. What is not done

No CLASS run, no N-body, no flux-power modelling (the forest gate is the record's linear proxy on 3D power, as X4/X18).
No new action is written. Clusters, hosted dwarfs and lensing are not graded (reported side effects only).
