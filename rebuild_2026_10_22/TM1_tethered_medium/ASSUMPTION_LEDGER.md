# TM1_tethered_medium: assumption ledger (committed with the frozen criteria, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSTULATE (a PAPER49
rule with no action) / FITTED. κ = ½ FITTED; footings never pooled.

## A. Source hashes (sha256, first 16 hex)

| file | sha256 |
|---|---|
| `qwen_claude_field_theory/papers_2026/PAPER49_why_cold_energy_settles_2026.tex` (v1.2, 77b39b9fcd) | 3db1d47520b500a7 |
| `qwen_claude_field_theory/papers_2026/PAPER49_why_cold_energy_settles_2026.zenodo.json` | a9e9c5ffcb5b7782 |
| `argon_push/AG6C_relativistic_completion/ag6c_s0_saddle.py` | 8918d5d28a66e54e |
| `rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores.py` | 4837ade939d4dc83 |
| `rebuild_2026_10_22/X2_cluster_outskirts/x2_cluster_outskirts.py` | 52ed15f74e716ad4 |
| `rebuild_2026_10_22/X2_cluster_outskirts/x2_replay_percluster.npz` | 8d473764e791df67 |
| `doors_push_2026_10_22/D6_u_mechanism/d6_u_mechanism.py` | ef9a10aa0f4dd11a |
| `doors_push_2026_10_22/D6_u_mechanism/d6_selfsim_tables.npz` | d8cbb305d8ac326d |
| `rebuild_2026_10_22/F3_growth_audit/f3_growth_audit.py` | 02db36204f619f9c |
| `rebuild_2026_10_22/Z2_satellite_systematics/z2_per_system.csv` | f0e356892e75c3cf |
| `rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py` | 955298d5486a86b4 |
| `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py` | 3aa96a78cd5e02e1 |

## B. The flavor's ingredients

| ingredient | class | source |
|---|---|---|
| a₀ = κ c √(Gρ_DE), κ = ½ | FITTED (κ) / FRAMEWORK-NATIVE (form) | PAPER49 L23 |
| Ω_c/Ω_b = 5.364 | measured (FITTED to cosmology) | PAPER49 L24 |
| the action L (Φ, P, W_rem, γ) | FRAMEWORK-NATIVE | PAPER49 L30–L32 |
| ρ_c = ρ̄ + ∇·P, ∂ₜP = −j | FRAMEWORK-NATIVE (definition) | L27 |
| L★ ∈ [24 pc, ~1 kpc] | bounded (FITTED floor from globulars; ceiling from c_T, CFG961) | L32; THEORY_CANONICAL 10-21 draft L385–L387 |
| T: tether only to condensed baryons, only at low relative speed | **POSTULATE** (L57: "the action as written responds to all baryons") | L34, L48–L52, L57 |
| C: catchment supply (baryons inside turnaround) | **POSTULATE** | L50 |
| S: rest state reached (adiabatic following) | **POSTULATE**, partly derived: CFG939 (spherical, single medium, phase mixing; 44 % of infall mass ejected) | L44; LEDGER CFG939 |
| U: untethered, collisionless cold energy in hot-gas systems and mergers | **POSTULATE** | L51–L52 |
| kinetic term of the medium, ρ̄\|ξ̇\|²/2 with P = −ρ̄ξ | FORCED by "real rest mass" + ∂ₜP = −j (also CFG938's forced dust term); not in PAPER49's Lagrangian | L26–L27; LEDGER CFG938 |
| covariant parent (CFG938) | FRAMEWORK-NATIVE but CHOSEN pieces (χ, λ multiplier, stiffness form); ill-posed on FRW (CFG961) | LEDGER:697; THEORY_CANONICAL_2026-10-21_DRAFT.md L375–L389 |

## C. Inherited pipeline ingredients, by row

| row | ingredient | class | source |
|---|---|---|---|
| 1 | F3 backgrounds A/B (CLASS, ω_b, ω_cdm, h, A_s) | ΛCDM-PROCESSED | F3 README §1; results K2 |
| 1 | sub-horizon Newtonian two-fluid growth (F3 `growth_ratio`) | FRAMEWORK-NATIVE in the dust limit | F3 L101–L120 |
| 2 | Z2 per-system Δ, clean flags C1–C4, x_e, M_V, orbits in S1's MW field | RAW (kinematics, photometry) + SPS-free; MW model Hernquist 6e10 with the law (FRAMEWORK-NATIVE) | Z2 README; ASSUMPTION_LEDGER there |
| 2 | stiffened AQUAL with host field (D10 solver) | FRAMEWORK-NATIVE (S4 identifies it with PAPER49's rest state) | D10 README |
| 3 | KiDS-1000 shear stack on eRASS1 clusters | RAW shear; SURVEY-CALIBRATION (m-bias, n(z), boost) | F1/X2/X7 |
| 3 | eRASS1 Mgas500, R500 | SURVEY-CALIBRATION (X-ray scaling) | F1 ledger |
| 3 | β = 2/3 gas to 3 Mpc; stars 0.20 × gas | record convention (78 % of the budget beyond R500 is extrapolation, CFG949) | F1 G0; CFG949 row |
| 3 | distances DM(z, h), h 0.672/0.686 | FRAMEWORK-NATIVE h | F1 C2 |
| 3 | self-similar collisionless infall, EdS, radial orbits, ε bracket | derived dynamics under an INITIAL-CONDITION POSTULATE (scale-free accretion); EdS (not native Λ) | D6 Q2; Bertschinger 1985; Fillmore & Goldreich 1984 |
| 3 | turnaround overdensity (3π/4)² of the EdS mean | EdS (approximation, stated) | — |
| 3 | ω_b = 0.0224 | BBN (external measurement) | AG6C S0 header |
| 3 | spherical AQUAL ν (U1, U2) | FRAMEWORK-NATIVE | F1 K5 |
| 4, 6 | SPARC rotmod + Lelli 2016c table (L36, M_HI, D, Inc) | RAW (+ SPS via Υ, fitted per galaxy) | P4 T1 |
| 4 | M_b = Υ L36 + 1.33 M_HI (bulge at disc Υ) | convention (bulge treatment stated) | — |
| 5 | AG6C two-body solve (deep MOND, γ = 0; full-μ check) | FRAMEWORK-NATIVE | AG6C §5 |
| 5 | ρ̄_c = 5.364 Ω_b ρ_crit | FRAMEWORK-NATIVE + BBN | AG6C S0 header |
| 5 | AG7 power estimate (Epps & Hudson 2017 published numbers) | RAW published + survey | AG7 README |

## D. Record statements this lane must re-check against PAPER49's action

| record statement | what this lane does |
|---|---|
| CFG938: covariant parent CONDITIONAL; tethered medium has no linear self-gravity, δ ∝ a^0.61 | S3, S6 on PAPER49's own Lagrangian + forced kinetic term |
| CFG941 Theorem D-T (c₂ = 1 ⇒ no self-gravity, no gravity between tethered components); growth a^0.694 in the χ parent | S1 (W_rem has no quadratic term), S3 |
| WT-02 / CFG961: CFG938's parent Hadamard ill-posed on FRW; c_T ≠ c structurally | quoted, not re-derived (row 1 (c)) |
| CFG944 side flag: the always-on tether's argument reaches u = a₀ at z ≥ 84 | quoted in row 1 as a limit of linear theory |
| CFG945 Theorem S / CFG941 hover lemma (Δa/g_host 1.02–1.11) | row 2 |
| CFG946 D-T′, L-G (no-EFE field ⇒ no deep law) | row 2 context |
| D6: u not universal; its self-similar K3 FAIL (interior slope 0.625 vs 0.75) | SSa, SSb |
| Y1 (Codex's P-medium): growth but no law | overall reading |
| Z1 FAMILY_SCORES: BLT dipolar growth carries a ghost (K1, K3) | S5: same or different for PAPER49 |
| CFG949: untethered clusters with NFW debris explain at the primary corner, fragile | row 3 uses a derived profile, no NFW |
| CFG815: PAPER49's own hot-gas test FAILS (MID tercile 1.64, Z +4.6) | quoted in row 3 |
| CFG801: own-supply edge excluded (Δχ² +197) | quoted in row 4 |
| CFG963: the native shear pass is carried by gas expulsion | quoted in row 1 context |
