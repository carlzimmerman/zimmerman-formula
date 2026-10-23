# Z1 requirements matrix: the verified constraints any successor must meet

Every number comes from a lane the coordinator reran or reproduced. Pointers are `file:line` at HEAD 99a3a3c069 (which contains the v3s adoption 591ec436be and e1e999455a).
Paths are repo-relative; `R/` = `rebuild_2026_10_22/`, `CP/` = `covariant_push_2026_10_22/`, `DP/` = `doors_push_2026_10_22/`,
`TD` = `CP/THEORY_V3_DRAFT.md`, `LEDGER` = `campaign_fresh_gravity/LEDGER.md`.
κ = ½ FITTED. Numbers are canonical / alt, never pooled. "Law" means AQUAL with μ = x/(1+x).

## A. The rows (24)

| # | constraint | the number a successor must meet | evidence |
|---|---|---|---|
| R1 | GW speed = c; binary pulsars | v3: Δv/c ≤ 6e-32 against the 1e-15 bound; only tensor modes propagate at leading order; ≤ 3e-14 of the double-pulsar error | `CP/C8_instantaneous/README.md:14`, `CP/C5_health/README.md:9`, `TD:82` |
| R2 | Healthy, well-posed DOF everywhere | γ_L stiffness is Hadamard ill-posed where ρ_τ < 0 (every two-body saddle; growth ∝ L★k) — v3 as written | `R/H4_v3_saddle_stability/README.md:3` |
| R2b | (same) | v4 is ill-posed wherever the aether twists (every non-symmetric bound system) | `R/I1_gammaL_causality/README.md:3` |
| R2c | (same) | v3's constraint algebra closes: 3 DOF, no tertiary; H4 is the scalar's dynamics, not a rank change | `reviews/v3_constraint_algebra_2026_10_23/README.md:8` |
| R2d | (same) | the switched stiffness −(γ_L/2)[max(D·P,0)]² is WELL-POSED + STATICS UNCHANGED (1D nonlinear, slab, interface; 2D/3D open); adopted by the owner as v3s (591ec436be); qualifier 4 (soft-side strong coupling) resolved benign (d27e01f42e) | `R/X3_switched_stiffness/README.md:3`, `:19`, `reviews/v3s_soft_side_strong_coupling_2026_10_23/` |
| R3 | n = 1 law, SPARC RAR | one Υ per galaxy, EFE solved: rms 0.054 / 0.054 dex; median Υ 0.52 / 0.44; χ² line fails (63–64 % acceptable) — CONDITIONAL | `R/P4_v3_galaxy_tiles/README.md:16` |
| R4 | MeerKAT local a₀ | +0.033 dex from SPARC with the same recipe — PASS | `R/P4_v3_galaxy_tiles/README.md:17` |
| R5 | Groups (BFJR) | isolated law +0.010 / −0.010 dex — PASS; above the law at g_e = 0.03 a₀ | `R/P4_v3_galaxy_tiles/README.md:18` |
| R6 | Isolated Local Group dwarfs | +0.06 ± 0.08 / +0.02 ± 0.08 dex over v3 — consistent | `R/X1_hosted_recount/README.md:80` |
| R7 | Solar-System screening (Cassini Q₂) | screened: passes by 2.8e7–5e9 (24 cells); unscreened law fails 2.44–4.59× / 2.85–5.19×; no unscreened law passes Q₂ and SPARC | `CP/C6_literal_cassini/README.md:7`, `DP/D7d_screened_q2/README.md:3`, `DP/E2_field_equation/README.md:8`, `DP/D7c_q2_rar_gate/README.md:7` |
| R8 | Outer globulars Newtonian | L★ = 0 excluded in all 18 cells (Δχ² 4.9–22.8); floor L★_95 21.7 / 22.9 pc with the EFE; 28.4 / 29.3 pc with no EFE | `TD:86`, `DP/D10_native_Lstar/README.md:3`, `R/T1_efe_strength/README.md:60` |
| R9 | Wide binaries (pending DR4) | screened γ_v − 1 ≈ 8e-6 vs law-first 1.167 / 1.199 at 20 kAU; DR4 2026-12-02; power gap for a MOND-size boost at the plan's N | `TD:85`, `DP/E2_field_equation/README.md:11`, `LEDGER:701` |
| R10 | MW vertical force | AQUAL disc: K_z(1.1 kpc) 92.3 / 96.9 vs 66.4 ± 2.2; χ² 178 / 251 vs 67.5 — FAIL; a light-disc corner passes only with R_d ≥ 2.8σ below priors and still misses K_z(R₀) by ≥ 4.7σ | `R/P4_v3_galaxy_tiles/README.md:19`, `R/X5_mw_joint_baryons/README.md:7` |
| R11 | MW outer slope | law −0.126 / −0.114 vs data −0.325, Z −4.37 / −4.62; robust to the S2 error budget (Z −3.88 / −4.09) | `TD:108`, `R/X5_mw_joint_baryons/README.md:8` |
| R12 | TDGs and DF2/DF4 Newtonian | dust-free ⇒ Newtonian: TDGs +0.055 ± 0.114 dex (U1 native pass); static AQUAL in the host field sits −0.59 / −0.62 dex and −1.66 / −1.74 ln below the law (FAIL) | `R/U1_v3_dust_content/README.md:15`, `R/P4_v3_galaxy_tiles/README.md:20` |
| R13 | Hosted dwarfs (satellites) | above the isolated law by +0.28 / +0.24 (MW classical), +0.63 / +0.59 (MW ultra-faints), +0.25 / +0.21 (bright M31), +0.64 / +0.59 (M31 others) dex; above v3 + EFE by +1.33 / +1.30 (S1 sample); above Newton at ≥ 5σ in six sets | `R/X1_hosted_recount/README.md:74`–`:79`, `R/S1_v3_hosted_small/README.md:7`, `R/X1_hosted_recount/README.md:8` |
| R14 | Coma UDGs | +0.33 dex above the isolated law; +1.12 / +1.08 dex above the law in Coma's field (FAIL, robust); Newton excluded at 5.45σ | `R/S1_v3_hosted_small/README.md:8`, `LEDGER:704` |
| R15 | Cluster cores (eRASS1 × raw KiDS) | A_MID (0.3–1 Mpc) 1.68–1.85 / 1.54–1.70, Z ≈ +5–6 jackknife, 2.2–2.7 with systematics; by gas tercile MID 1.12 / 1.88 / 1.89 and OUTER 0.50 / 0.78 / 1.40 (canonical); debris *replacing* the law passes, added to it overshoots | `R/F1_cluster_cores/README.md:3`–`:10`, `R/X2_cluster_outskirts/README.md:25`, `:71`–`:75`, `:21` |
| R16 | Linear growth within 5 % of dust | v3 at the galaxy-allowed μ_K: R_B 0.0032 / 0.0052 (×300 / ×182 short); dust limit S₈ 0.845 → 0.814 (native H₀) CONSISTENT with raw KiDS at k ≤ 0.3 h/Mpc | `R/X4_growth_native_cap/README.md:15`, `R/F3_growth_audit/README.md:8`, `:60` |
| R17 | BBN / radiation era | literal BS K(Q) has a stiff a⁻⁶ partner: no radiation era unless μ_K ≥ 1.84e8 h/Mpc; BS25's DBI K fixes BBN but not growth (R_B 0.26–0.32) | `R/Q6_v3_class/README.md:5`, `R/Q7_bs25_cosmology/README.md:3`, `:21`–`:26` |
| R18 | CMB TT/TE/EE (plik-lite + low-ℓ) | ΛCDM refit χ² 1003.47; v3 Δχ² +13891 … +18.7 over μ_K 14.8–2542 h/Mpc; DBI +350 / +748; a₀ absent at linear order, so only an a⁻³ dust has fitted the third peak | `R/Q6_v3_class/README.md:20`–`:29`, `R/Q7_bs25_cosmology/README.md:27`–`:31`, `R/X0_explanation_map/MAP.md:22` |
| R19 | No isocurvature from the cold-sector origin | light-spectator (two-field MeV) origin fails the Planck CDI bound by 2e8–6e8 in power at every computed point | `R/X1_seedfree_abundance/README.md:3`, `:91` |
| R20 | a₀ tied to Λ | a₀ = κc√(Gρ_Λ) = c²√(Λ/32π) at κ = ½ (Lean); κ FITTED: κ_Λ 0.417 ± 0.095 (CFG493), 0.499 ± 0.116 (S3 AQUAL discs) | `CP/V3_FULL_PICTURE.md:33`, `TD:69`, `TD:108` |
| R21 | Strong field | static BHs, NS, ringdown shifts ≤ 2.9e-11; strong coupling PASS as an estimate (lab margin 1.7× in k) | `R/P3_v3_strong_field/README.md:3`, `:10` |
| R22 | Galaxy lensing, inner and red | blue 0.878 ± 0.074 / 0.802 ± 0.067 (data/v3); red inventory 1.313 / 1.200 short | `R/S2_v3_lowg_lensing/README.md:20`–`:22` |
| R23 | Isolated-galaxy lensing, outer | F2 frozen REAL FAILURE, not robust → UNDECIDABLE (the record's Δχ² +100 is a catchment-edge artefact); P2: data 2.8–3.0σ BELOW zero-field v3 beyond 1.1 Mpc, consistent with the catalogue field; N too small | `R/F2_outer_lensing/README.md:3`–`:12`, `R/P2_spec_isolated_lensing/README.md:3`, `:13`–`:14` |
| R24 | Cosmic shear (nonlinear) | settling rules excluded by raw KiDS (CFG596 Δχ² +68.7; CFG960 SC1x +47.28); the native shear pass is carried by gas expulsion (CFG963) | `R/F3_growth_audit/README.md:8`, `LEDGER:744`, `LEDGER:753` |

Rows R1–R20 cover the coordinator's list. R21–R24 are added because a successor must not lose them.
Not a row: the ALMA U4/GS4 readings (expected unscorable, `TD:124`).

## B. Tensions: rows that no single known mechanism meets together

| tension | rows | the obstruction | where it is shown |
|---|---|---|---|
| **U1: held phantom vs self-binding cold mass** | R3–R6, R12 vs R13–R16 | in the khronon family the cold medium's force relative to free fall is the law's own field (α ≡ 1), so held dust is the phantom, is weightless in a host (T3) and has no linear self-gravity; any always-on tether whose phantom is its own mass cancels its self-gravity (Theorem D-T); any local holding force does (D-T′) | `R/X6_dust_coupling/README.md:12`–`:20`, `R/U1_v3_dust_content/README.md:10`, `LEDGER:699`, `LEDGER:707` |
| U1′: separate dust double counts | R3, R6 vs R16 | a second dust that weighs in hosts and grows sources the law like baryons: SPARC Υ falls to 0.42 / 0.37, NGC 3198 off by 0.145 dex ("CDM under another name") | `R/X6_dust_coupling/README.md:7`, `CP/V3_FULL_PICTURE.md:148` |
| Local selectors | R16, R18 vs R3 | the linear-era cold field exceeds a₀ at z ≥ 84–101 (15.6 a₀ at z = 1100), and late linear fields are deep (x ≪ 1); a local L(θ,u) gate that is off in the linear universe forces a vacuum offset 15–25× what slip allows (Theorem G); any label-free tether hovers (Theorem S) | `LEDGER:705`, `LEDGER:709` |
| μ_K pincer | R13, R15 vs R16 | growth needs μ_K ≥ 411 h/Mpc; galaxies allow ≤ 0.03–0.1 Mpc⁻¹; gap 2.4e3–5.7e4; the static branch hits galaxies before clusters (onset ∝ M^{1/6}) | `R/X4_growth_native_cap/README.md:15`, `R/S4_v3_muK_clusters/README.md:9` |
| Screening vs health | R7, R8 vs R2 | screening needs γ_L; γ_L is ill-posed at saddles (H4) and where the aether twists (I1); density screening needs 3 constants and breaks SPARC (V1). Cured for v3 only: the switched stiffness (X3) | `R/H4_v3_saddle_stability/README.md:3`, `R/I1_gammaL_causality/README.md:3`, `TD:114`, `R/X3_switched_stiffness/README.md:3` |
| BBN vs growth | R17 vs R16, R18 | the quadratic K has no radiation era; the DBI K fixes BBN but not growth; a huge λ_D restores σ₈ but fails the Lyman-α forest | `R/Q6_v3_class/README.md:5`, `R/Q7_bs25_cosmology/README.md:3`, `R/X4_growth_native_cap/README.md:16` |
| EFE sign | R13, R14 vs R23, R9 | hosted dwarfs want no EFE (the exact AQUAL EFE costs +0.58 dex); P2 lensing wants ε ≥ 0.67; one EFE strength does not fit (p 0.023 / 0.014) | `R/T1_efe_strength/README.md:8`–`:12`, `R/S1_v3_hosted_small/README.md:7` |
| Supply edge vs supply-free law | R23 vs R13, R16 | a medium whose phantom is its own mass needs a supply, and the supply edge produced the record's outer-lensing Δχ² +100; a supply-free (polarization) phantom has no edge but then the cosmic dust is separate and double counts | `R/F2_outer_lensing/README.md:10`–`:12`, `R/X6_dust_coupling/README.md:18` |
| MOND-class generics | R10, R11, R15, R18 | MW joint radial + vertical fits fail across the μ-law family; cluster cores have no clean rule-compatible pass; the third peak forms at x ≈ 11–14 where a₀ is inert | `R/X0_explanation_map/MAP.md:18`–`:26` |

The U1 tension is the hub. Every other tension either feeds it (μ_K pincer, BBN vs growth, local selectors) or is
generic to the MOND class.
