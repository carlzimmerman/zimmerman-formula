# κ attempts ledger (CFG894, 2026-10-20)

This file lists every κ derivation or selection attempt found in the record. The law is a₀ = κ c √(G ρ_DE), and **κ = ½ is
FITTED**. Equivalent forms: Λ = 32π a₀²/c⁴, G ρ_Λ = 4 a₀²/c², Z = cH_Λ/a₀ = √(32π/3) = 5.7888 (Z is never ~21). Deriving Z,
the "32π", the "4" or the "¼" is the same problem as deriving κ.

**How this file is made.** The tables below are rendered by `kappa_campaign_lee.py` from `kappa_attempts_register.csv`. That
CSV is the source: one row per attempt, append-only, ids K001… The same script prints the counts and the look-elsewhere
numbers into `kappa_campaign_lee.out`. If you edit the CSV, rerun the script; never hand-edit the tables.

**Where the rows come from.** Five read-only sweeps on 2026-10-20 covered sonnet55_push/puzzle_32pi (p01–p63, agents A–Z,
EXT01–04), sol61_push (top level, puzzle_32pi, puzzle_32pi_*_2026_10_14/15 and later lanes), real_research and its reviews,
reviews/, kappa_closure, nbody_2026, fable_independent_2026 (kappa_slot_2026, lean_2026, L-lanes), opus_48/49,
qwen_claude_field_theory, campaign_fresh_gravity, campaign_fresh_gravity_astra, argon_push, deepseek_push, qwen*,
the other model pushes, hunt_2026, project_atomos, predictions_2026, RETRACTIONS.md and STANDING.md. Rows that repeat the same
mechanism in another file were merged into one; pure re-runs are marked `audit`. Every commit hash was checked to exist.
Rows marked `untracked` are files on disk that are not committed (31 sol61 Oct-14/15 directories, the p62/p63 scripts, the
10-20 KAPPA_LOGIC Lean file, and the gated brute-force verdict, which `.gitignore` hides through its `*brute*` pattern).

## Totals (787 rows)

- **537 derivation or selection attempts.** That excludes observational, audit, Lean and κ-blind rows.
- **None derives κ = ½.**
- **129 produced a number.** 60 produced one determinate value; 69 are menus of several values from
  admissible variants. Every other attempt ended in one of four ways:
  - a condition equal to the target,
  - a free ratio, or a trade for a new constant,
  - a bound,
  - a closure.
- 44 rows are measurements (κ determinations, not derivations), and 7 are registered but unrun.

**17 of the 60 determinate values land inside today's 2σ data window [0.227, 0.607].** That window is CFG493's
κ_Λ = 0.417 ± 0.095.
- Every landing is an O(1) number that the window cannot separate from ½.
- They are mostly the same few values, recurring: 0.461 (Z = 2π), 0.482 (Z = 6, Verlinde), 0.55–0.557 (particle horizon,
  Nariai).
- The rate (about 33%) is what a random draw from the record-natural number set gives (27–28%; see
  `kappa_campaign_lee.out`). So the landings are no evidence that any route knows κ.

**68 attempts output exactly ½, and every one was voided or left conditional.** That is about one attempt in seven.
The ½ got in by one of these routes:
- inserted or written in (CFG43, CFG187, G031);
- posited (the free-fall surface gravity c²/2R*, i.e. J = Gρr²/c² = 1);
- tuned (p20c, AS651.C01, lens q = 4, cosmic-string Gμ = 3/16);
- by naming, where a different quantity was called κ (the SIS ratio σ²/v² in GF2, Q001, Q007, Q010 and deepseek_moa; I14's
  lattice coupling);
- by a channel or polarisation count (PD07, H017, kimik3, gemini38: a retracted class);
- by circularity (GF1's n = 2 and the Ω_Λ selectors);
- by a gauge or algebra error (graviton normalisation A; EXT02).

**Historically, then, P(flawed | the output is ½) = 1.** The campaign rules (`KAPPA_CAMPAIGN_RULES.md`) are built around that
fact.

## What each family showed (one paragraph each; the tables give the rows)

- **HT, horizon/thermal.** Every identification uses a₀ and H only.
  - The π-parity obstruction applies (L4, LN5, CFG263). The outputs are rational × π^k with k odd, so never ½. The values
    cluster on Z ∈ {1, 2, 2π, 6, ½}.
  - The 2π landing (κ = 0.461) is data-consistent and recurs, but it is one input (T_GH = ħH/2π) wearing several hats.
  - The KMS "derivation" of 0.4607 (RT-17) was later withdrawn by RT-19 (a 4π error, giving 2cH_Λ). PAPER6 and some notes still
    present 0.4607 as coefficient-free. **Record conflict, listed below.**
- **HE, holographic/entropic.** The Bekenstein–Hawking ¼ carries ħ⁻¹, while a₀ is ħ-free (RT-18, CFG264).
  - CKN and the seesaw are identities (FL12, RR-24/25).
  - Verlinde's 6 (0.482) lands in the window, but its local term fails SPARC (p34) and its shape test fails 0/16 (CFG117).
- **VM, vacuum matching.**
  - The a₀ sector's vacuum constant is a zero mode in every local action (k01, AS067, AS069, ARGON01, sol61 non-selection
    Lean).
  - Natural kernel vacua give κ ≈ 1, which is excluded.
  - Tail and cutoff versions trade κ for a turn-off y_t ≈ 129. Detached TNOs likely exclude that turn-off (p56), and Cassini
    rejects the whole QUMOND/BIMOND class (p58).
- **FN, normalisation of W and the action.**
  - The four-form gives a free ratio Z/β² (k04, AS651–658).
  - Spectral functionals obey the reparametrisation theorem: a probe, never a derivation (RT-12).
  - The gated brute force (six action classes) found no survivor.
  - a₀-as-field (p63) is registered but unrun.
- **PS, π-counting and geometry.**
  - 32π is 8π × 4 and carries no geometric meaning (k05). About 60 horizon/vacuum principles give q·π^±1 (L4).
  - Nariai (0.557) evaluates outside its own static patch.
  - The free-fall surface gravity gives ½ only by positing J = 1. No physical object has radius c/√(Gρ) (RV-25).
- **GB, graviton bath.**
  - The ε_tot = 1/(32π) slot is not live: it double-counts S_dS (KS01).
  - Mode counting spans 161× (RV-40).
  - The polarisation-count class is retracted (H061).
- **TA, topological.** η = 0 on the round dS S³ (theorem-grade). Forced halves sit in the wrong slot; anomalies give integers
  or need inserted constants.
- **QG.** Asymptotic-safety exponents are type-mismatched; DSSYK was computed to fail; the RG, dilaton and large-N ratios give
  the wrong numbers.
- **KS, kinetic and cold-energy dynamics.**
  - SIS σ²/v² = ½ is a different quantity (AUDIT_GF2).
  - CFG893 (131bedf33): the c-free cold-energy system is invariant under S_λ (x→λx, M→λ³M, a₀→λa₀). Any c-free balance
    therefore makes a₀ depend on galaxy mass or holds for every a₀, and κ needs c. **This is now a campaign rule.**
- **CC, cosmological ties.**
  - Unimodular (XR20), the clocks and the horizons tie a₀ to Λ without fixing κ.
  - The particle horizon (0.55) is an epoch coincidence that fails the flat a₀(z) record.
  - Ω_Λ-from-a₀ "selectors" are circular (CFG835).
- **NU, numerology.** Base rates:
  - ½ appears in 0.94% of an 852-form principle grammar (p60);
  - 10.8% of ≤3-operation numbers fall in a 2σ band (KS04);
  - 596 closed forms lie within 1% of Z (RT-22).
- **OB, measurements, not derivations.** The primary is CFG493. Never quote 0.551 ± 0.043, 0.465 ± 0.076 (use 0.450 ± 0.073),
  SPARC 1.0766e-10 or the p48 pool.
- **AU/LN, audits and Lean.** κ is independent of every committed premise set (L3, sol61-104).
- **EX, pasted derivations.** All circular or erroneous.

## Record conflicts and hygiene items found by this sweep (not fixed here; read-only lane)

1. **Q010 versus AUDIT_GF2.**
   - qwen38_push/Q010_kappa_referee calls GF2 "UPHELD-QUALIFIED: DERIVED (dynamical face)" and never engages AUDIT_GF2
     (a755b66ca).
   - Only Q010's criteria are committed (0eb0b4d07); its README, results and Lean are untracked.
   - qwen38 PREDICTIONS and STATUS repeat "derived".
   - **AUDIT_GF2 stands: GF2's ½ is the SIS ratio, and changing the law's κ leaves it at ½.** Q010 must not be cited.
2. **RT-17 versus RT-19.** The KMS 0.4607 "first predicted κ" was withdrawn by RT-19 (4π error → a₀ = 2cH_Λ). PAPER6
   (F04 in the sweep) and AS066 still present 0.4607 as a coefficient-free horizon value. Which one stands should be settled
   before anyone cites "the dS tie gives 0.461".
3. **Never separately audited:**
   - G031's "ρ_L = 4a₀²/(Gc²) DERIVED (action level)": same tie-written-in class as CFG43;
   - glm53's README "κ = ½ DERIVED";
   - the gemini38 photocount chain: retracted class.
4. **Stale index.** fable_independent_2026/kappa_slot_2026/KS00_INDEX.md lists KS01 only (KS02–KS08 exist).
5. **Unreproducible from the repo.** opus_48 review memos cite /tmp scripts that are not in the repo (ROUTE2, ROUTE4, ROUTE5,
   AEST-joint, FRONTIER1, CLASS3, CLASS6, MECH4, ETA).
6. **Untracked:** KAPPA_GATED_ACTION_BRUTEFORCE_VERDICT_2026-06.md (hidden by the `*brute*` .gitignore pattern) and the 31
   sol61 Oct-14/15 directories.

## Registered, unrun (run these before launching anything that overlaps them)

- p62 (GF1 pin audit).
- p63-C1, C1b, C2 and C3 (a₀ as a field: cosmic bound charge, patch bootstrap, flux lattice, Kaloper–Sorbo ħ audit). Criteria
  2a36f4ae5, errata 5e5a10e33 and a1e430de1.
- KAPPA_LOGIC_2026_10_20.lean (the 32π chat; compile in lean_2026).
- Nine deepseek AS proposals that were never executed.

## Active parallel efforts (do not duplicate)

- **The "32pi squared puzzle" chat.** It is auditing the empirical provenance of the measured κ values and doing the logic/Lean
  argument (KAPPA_LOGIC).
- **CFG893.** κ from the new cold-energy structures. DONE 2026-10-20: NOT SELECTED (131bedf33).
- **CFG895.** The α (fine-structure) ledger: a separate constant and a separate lane.

## Counts by family

| family | rows | determinate | menu | no number | pending | observational |
|---|---|---|---|---|---|---|
| HT Horizon / thermodynamic (Unruh, Gibbons-Hawking, KMS, surface gravity) | 56 | 13 | 14 | 29 | 0 | 0 |
| HE Holographic / entropic (BH entropy, CKN seesaw, Verlinde, entanglement, Jacobson) | 42 | 9 | 14 | 19 | 0 | 0 |
| VM Vacuum-energy matching (the a0 sector's vacuum = rho_DE; kernel tails, BIMOND/QUMOND) | 64 | 4 | 10 | 50 | 0 | 0 |
| FN Field-theory normalisation of W(u) / action coefficients (four-form, spectral, heat kernel, a0-as-field) | 148 | 9 | 7 | 127 | 5 | 0 |
| PS 16pi / 32pi / pi-counting and geometric structures (Gauss-Bonnet, SdS/Nariai, membranes, Tolman/Komar) | 58 | 9 | 12 | 36 | 0 | 0 |
| GB Graviton bath / mode counting | 15 | 2 | 3 | 10 | 0 | 0 |
| TA Topological / index / anomaly | 24 | 1 | 0 | 23 | 0 | 0 |
| QG Quantum-gravity programmes (asymptotic safety, DSSYK, RG improvement) | 29 | 6 | 1 | 22 | 0 | 0 |
| KS Kinetic / settling / collective / cold-energy dynamics | 35 | 2 | 2 | 31 | 0 | 0 |
| CC Cosmological consistency (horizons, epochs, H0, unimodular, sequestering) | 51 | 2 | 4 | 40 | 0 | 0 |
| NU Numerology and grammar searches (flagged) | 30 | 1 | 2 | 9 | 0 | 0 |
| OB Observational determinations of kappa (NOT derivations) | 54 | 0 | 0 | 0 | 0 | 44 |
| AU Audits, controls, meta-analyses | 140 | 0 | 0 | 0 | 1 | 0 |
| LN Logic / Lean formalisations | 16 | 0 | 0 | 0 | 1 | 0 |
| EX External pasted derivations | 9 | 2 | 0 | 7 | 0 | 0 |

Class key: `odd` determinate, a-and-H-only (kappa^2 in Q*pi^odd; cannot give 1/2 exactly); `any` determinate, density route (kappa^2 in Q*pi^k; can give 1/2); `cont` determinate, transcendental root (log-uniform reference); `menu` several values from admissible variants (non-determinate: never a hit); `free` condition only / free ratio / trade / bound / not selected (no number); `pend` registered, not yet run; `obs` observational determination of kappa (not a derivation; not a trial); `audit` audit / meta / control (not a trial); `lean` logic or Lean formalisation (not a trial); `nk` kappa-blind lane listed for completeness (not counted).

## HT: Horizon / thermodynamic (Unruh, Gibbons-Hawking, KMS, surface gravity)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K003 | p03a | `sonnet55_push/puzzle_32pi/p03_egb_and_data.py` | 4D Einstein-Gauss-Bonnet BH maximal Hawking temperature | - | free | RETRACTED lead (misremembered temperature) | 9172fe05b |
| K013 | p12 | `sonnet55_push/puzzle_32pi/p12_horizon_equation_no_local_bridge.py` | static horizon equation with local density | - | free | CLOSURE (sharp no-go): kappa=1/(2r_h) only if rho(r_h)=0 | e6d9add5c |
| K023 | p20a | `sonnet55_push/puzzle_32pi/p20_acoustic_horizon/p20a_machinery_A1.py` | cosmological sound horizon of the a0 sector | 2.894 | odd | MISS: needs c_s=2.894c (superluminal) | df88379e3 |
| K024 | p20b | `sonnet55_push/puzzle_32pi/p20_acoustic_horizon/p20b_khronon_universal_horizon.py` | khronon universal horizon in SdS | - | free | CLOSURE: Lambda cancels | 2819f9e78 |
| K025 | p20c | `sonnet55_push/puzzle_32pi/p20_acoustic_horizon/p20c_A2_and_finite_speed_khronon.py` | sonic horizon around a mass; finite-speed khronon | - | free | VOID: 1/2 only at tuned n=2+sqrt2 (insertion) | ca1b28752 |
| K074 | R-S4 | `sonnet55_push/puzzle_32pi/README.md` | Milgrom cH/2pi thermal reading (A*Lambda=12pi^3) | 0.461 | odd | DATA-LEVEL landing; 'classical, no thermal 2pi' inference WITHDRAWN (audit M5) | 4896943eb |
| K093 | N | `sonnet55_push/puzzle_32pi/agents/N_jacobson_thermo_dS/` | Jacobson chain with exact dS Unruh temperature | {2.894, 5.79} | menu | MISS: Killing factor cancels | 243a089c9 |
| K101 | W03 | `sonnet55_push/puzzle_32pi/agents/W_fresh_ideas/` | SdS extended thermodynamics | {1.29, 1.02, 2.19} | menu | MISS: rational x pi | 1138d817f |
| K105 | X3 | `sonnet55_push/puzzle_32pi/agents/X3_extended_thermo_mach/` | extended BH thermodynamics + Sciama/Mach | - | free | CLOSURE: rational x pi; 1/4 only at a tuned cutoff 2R* | 1138d817f |
| K114 | B3 | `sonnet55_push/puzzle_32pi/agents/B3_modified_horizon_equation/` | f(R)/Horndeski/Rastall/Lovelock/4D EGB horizons | - | free | VOID: reached only in 4D EGB with G_eff<0 and a hand-tied coupling | e6d9add5c |
| K139 | LN9 | `fable_independent_2026/lean_2026/ALPHA_CFG47_U2_unruh_cap_condensate.lean` | T_Unruh = T_dS divided by n modes | - | free | CLOSURE: 1/2 needs n=Z=5.79; no integer works | ecf3d3ffa |
| K146 | FL3 | `fable_independent_2026/L40_coefficient_rigidity.py` | S8 horizon thermodynamics with zero free choices | 2.894 | odd | MISS: refuted at 56 sigma; the 0.4607 version needs an inserted 1/(2pi) | 3cb26cf41 |
| K163 | OR2 | `opus_48_extended_research/reviews/ROUTE2_DSUNRUH_CROSSOVER_Z_VERDICT_2026-06-15.md` | Unruh / dS temperature crossovers | {2.894, 0.461} | menu | MENU: temperature equality gives Z=1 or 2pi | 889f30c2b |
| K171 | OR10 | `opus_48_extended_research/reviews/NONLOCAL_MI_INTEGRAL_VERDICT_2026-06-15.md` | nonlocal dS-Unruh worldline integral with FDT | 5.79 | odd | MISS: 2cH_Lambda | aa17cee7f |
| K172 | OR11 | `opus_48_extended_research/reviews/PUREDS_LEGVII_FORCING_VERDICT_2026-06-15.md` | pure-dS particles + SM-bridge splice | - | free | CLOSURE: integer powers of pi | 4c62ee0e1 |
| K173 | OR12 | `opus_48_extended_research/reviews/TOE_STAGE2_CALC_VERDICT_2026-06-15.md` | dS-Unruh temperature-to-inertia couplings | {2.894, 1.447} | menu | DEAD; Cassini-excluded by 4.73 orders | 52b809d9e |
| K185 | OR24 | `opus_48_extended_research/reviews/toe_law/agentYY_modular_a0.md` | crossed-product free energy / relative entropy | - | free | CLOSURE: monotone, no feature at a~H | f1535b7d8 |
| K186 | OR25 | `opus_48_extended_research/reviews/toe_law/agentWW_routeModular.md` | Deser-Levin temperature as modular (KMS) temperature | - | free | IDENTITY, not a derivation of a0 | f1535b7d8 |
| K191 | OP3 | `opus_48_extended_research/papers/TWO_BARRIERS_TO_THE_MOND_COEFFICIENT_2026-08-03.md` | dS-Unruh balance on orbits | 5.79 | odd | MISS: 2cH_Lambda | 6e81e32f8 |
| K193 | OP5 | `opus_48_extended_research/papers/DRAFT_r_ONE_PARAMETER_NOGO.md` | dS-Unruh inertia class q=2/r for any f(T) | - | free | CLOSURE: one free ratio r | 8f2e9a036 |
| K203 | QC2 | `qwen_claude_field_theory/closure_2026/a0_promotion_2026/A0_PROMOTION_VERDICT.md` | postulates P1-P8 (offset / dS surface gravity / GH / Jeans) | {3.545, 2.894, 0.461, 0.5, 0.564} | menu | MENU: three allowed values not separable; P5 uses a length not in the action | 3fa2b8af9 |
| K221 | sol61-12 | `sol61_push/SHARED_SCALE_RESULTS.md` | Euclidean S4 horizon regularity / on-shell action | - | free | CLOSURE: no stationary point | 8fbd56a2c |
| K230 | sol61-21 | `sol61_push/CLOSED_SURFACE_RESULTS.md` | Dirac-mode curvature gap on a dS-radius sphere | - | free | FREE: a crossover not a coefficient | d912edb16 |
| K243 | sol61-34 | `sol61_push/EXPANSION_BRIDGE_GAP_CONES_RESULTS.md` | scalar-cone horizon identification | - | free | CLOSURE: incompatible with MOND window | 5f1809b2d |
| K246 | sol61-37 | `sol61_push/FINAL_5_PERCENT_SPRINT.md` | dS detector temperature as surface temperature | - | free | CLOSURE | d1e19d49e |
| K266 | sol61-57 | `sol61_push/puzzle_32pi/clock_horizon_regular_2026_10_06` | Killing-horizon crossing as an eigenvalue for A/H | - | free | CLOSURE: A/H free | cfa06dbfa |
| K324 | RR-01 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | F1(a) dS-Unruh Taylor-1/2 of sqrt(a^2+(cH)^2)-cH | 5.79 | odd | MISS: a genuine forced 1/2 but on the temperature root (a0=2cH_L); off by exactly Z | b35a41b7f |
| K325 | RR-02 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | F1(b) equipartition 1/2 kT_dS | - | free | CLOSURE: hbar-laden | b35a41b7f |
| K338 | RR-17 | `real_research/TOPOLOGICAL_KAPPA_ETA_VERDICT_2026-06.md` | self-adjoint horizon boundary condition | - | free | CLOSURE: a BC fixes the spectrum not the normalisation | 60c4885cb |
| K347 | RR-28 | `real_research/THE_FACTOR_OF_FOUR.md` | thermal Marongwe-Kauffman a0=cH_L/2pi | 0.461 | odd | DATA-LEVEL landing (Z=2pi); readings fan out across 1/2 | eb0c3301e |
| K361 | RR-43 | `real_research/bridge2_coefficient_thermodynamics.py` | Unruh=dS / Milgrom 2pi / Verlinde 6 / Schwarzschild readings | {2.894, 0.461, 0.482} | menu | MENU: does not pin | 0132f41b3 |
| K366 | RR-48 | `real_research/coefficient_posit_attack.py` | dS equipartition / Unruh / Padmanabhan carried to X | {2.894, 0.461} | menu | IRREDUCIBLE POSIT | 2744ee130 |
| K371 | RV-03 | `real_research/reviews/unruh_gh_coincidence_Z_2026.py` | T_Unruh(a0)=T_GH + area weighting | {2.894, 1.447, 0.461, 0.482} | menu | MENU: Z stays posited | bfc5b92ba |
| K376 | RV-08 | `real_research/reviews/derive_Z_equipartition_attempt.py` | equipartition on free-fall and horizon screens | {4.19, 0.482} | menu | MENU | e42b46e1e |
| K384 | RV-16 | `real_research/reviews/close_coefficient_Z.py` | normalisations bridging Deser-Levin to cH/Z | - | free | STALLED (number field) | 8db8b0136 |
| K387 | RV-19 | `real_research/reviews/desitter_factor_audit.py` | the dS horizon's natural O(1)s | 0.461 | odd | DATA-LEVEL landing (2pi) | 999f94dfe |
| K391 | RV-23 | `real_research/reviews/factor_of_two_desitter.py` | first-principles routes for k | {2.894, 1.447, 0.461, 0.482} | menu | MENU | ed8426e41 |
| K398 | RV-30 | `real_research/reviews/kappa_unit_response_2026_09_20/THERMAL_ROUTE.md` | thermal calibration of the channel response | - | free | INCOMPLETE | c3ccd563d |
| K427 | RV-59 | `real_research/reviews/mi_crossover_master_formula_2026.py` | I=f(T)-f(T_GH) class | - | free | FREE RATIO r | 260d3e155 |
| K438 | RV-71 | `real_research/reviews/mi_wightman_first_moment_2026.py` | dS Wightman integral for M1 | - | free | CLOSURE: zeta pole | 293bd4f6e |
| K445 | RT-03 | `reviews/mi_spectral_kms_bootstrap_2026.py` | thermal half-saturation R(Z)=1/2 | 0.69 | cont | MISS | 335595760 |
| K450 | RT-08 | `reviews/mi_thermal_class_nogo_2026.py` | 8 thermal-saturation targets | - | free | NO-GO for the class | 326e681ea |
| K455 | RT-13 | `reviews/mi_horizon_entropy_route_2026.py` | C1 Unruh/GH temperature matching | 2.894 | odd | MISS | fdc822157 |
| K459 | RT-17 | `reviews/mi_kernel_measure_from_desitter_2026.py` | KMS frequency identification w<->x | 0.4607 | odd | DATA-LEVEL landing; later WITHDRAWN (4pi error, RT-19): CONFLICT to resolve | a96497f0e |
| K461 | RT-19 | `reviews/mi_dsunruh_kernel_package_2026.py` | standard dS-Unruh acceleration construction | 5.79 | odd | MISS (a0=2cH_L) | e54059e9c |
| K462 | RT-20 | `reviews/mi_dsunruh_freedom_audit_2026.py` | response-power uniqueness | - | free | CONDITION | d5f3501be |
| K474 | NB-06 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T001 published dS-thermo routes | - | free | 0/4 in window | b062ad4a2 |
| K476 | NB-08 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T004 linear-response functions | {2.894, 1.085, 2.309} | menu | NULL: sigma is a dial | b062ad4a2 |
| K477 | NB-09 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T006 first-law smearings | {0.667, 0.600, 0.306, 0.589, 0.608} | menu | MENU: choice-dependent (4 of 5 in today's window) | b062ad4a2 |
| K478 | NB-10 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T005 q-deformed Deser-Levin | - | free | REFUTED | b062ad4a2 |
| K488 | CFG47 | `campaign_fresh_gravity/CFG47_unruh_matching` | T_Unruh=T_dS with n modes | {1.447, 2.894} | menu | RETIRED: 12.9 sigma from data; needs n=Z | 4dfa7d995 |
| K507 | CFG775 | `campaign_fresh_gravity/CFG775_bh_horizon_dark_energy` | BH horizon / tether relations | - | free | one coincidence; q not fixed | e20f1767d |
| K528 | AS066 | `deepseek_push/astra_spawn_ideas/results/AS066` | horizon coefficient sqrt(8pi/3)/(2pi) | 0.4607 | odd | DATA-LEVEL landing; conditional theorem, no selection | 511efeb1d |
| K553 | T008 | `qwen_38_experiment/KAPPA_LEDGER.md` | two-temperature interpolation | - | free | UNGRADED (script red) | b062ad4a2 |
| K582 | K004 | `grok_push/K004_VERDICT.md` | horizon ball (4pi/3)(3/8pi)=1/2 moved onto s | - | free | VOID: EMPTY, c and H cancel | db1cdf41a |
| K740 | W4-19/L3 | `why_4_puzzle/W4_19_literature_addendum` | van Putten 2017 (1707.01619): a0 = sqrt(1-q) H/2pi with Lambda = omega0^2 | {0.798, 0.688} | menu | MISS: (a) sqrt(2/pi), (b) LCDM q0 0.688; both pi-odd, out of window | 726716bac |

## HE: Holographic / entropic (BH entropy, CKN seesaw, Verlinde, entanglement, Jacobson)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K038 | p33 | `sonnet55_push/puzzle_32pi/p33_energy_additive_verlinde.py` | Verlinde elastic response with field-energy additivity (Z=6) | 0.482 | odd | DATA-LEVEL landing but mechanism EXCLUDED: its local term fails SPARC (p34 Dchi2 +1389/+2216) | fbb81f192 |
| K057 | p51 | `sonnet55_push/puzzle_32pi/p51_holographic_equipartition.py` | Padmanabhan holographic equipartition on the a0 horizon | {1.45, 2.05, 4.09} | menu | MISS: hbar cancels but every value carries one pi | d23562980 |
| K095 | R | `sonnet55_push/puzzle_32pi/agents/R_entanglement_equilibrium/` | entanglement equilibrium at finite ball radius | - | free | CLOSURE: Einstein equation exact at every radius; 5.7% near-hit moves x2.3-2.8 with definition | 243a089c9 |
| K131 | KS05 | `fable_independent_2026/kappa_slot_2026/KS05_category3_enhancement.py` | price four S_dS enhancements (Verlinde / dS IR / tensors / CKN) | {0.48, 0.5} | menu | VOID as a hit: Verlinde postulated; CKN equals the target by the seesaw identity; others excluded | 958f352c3 |
| K134 | KS08 | `fable_independent_2026/kappa_slot_2026/KS08_emergent_gravity_forcing.py` | holographic equipartition from scratch with two bit counts | {2.89, 0.72, 0.48, 0.46} | menu | MENU: forces the form and an O(1/2) coefficient, not 1/2; assumes holography | a366aec2b |
| K165 | OR4 | `opus_48_extended_research/reviews/ROUTE4_HOLOGRAPHIC_ENTROPY_Z_2026-06-15.md` | DOF counting (Verlinde/Padmanabhan/CKN/Jacobson) | {0.482} | menu | UNFORCED: free counting O(1) | 889f30c2b |
| K170 | OR9 | `opus_48_extended_research/reviews/GRAVITATIONAL_ROUTE_FORCES_KERNEL_NOT_KAPPA_2026-06-15.md` | Jacobson / Euclidean S4 / Komar-Tolman | - | free | CLOSURE: kernel sqrt(8pi/3) forced; kappa free | 826912366 |
| K179 | OR18 | `opus_48_extended_research/reviews/CKN_DOF_KAPPA_BRIDGE_2026-06-17.md` | CKN bound with SM g* | {0.18, 0.41} | menu | MISS: g*-dependent; exact only at g*=1 | 1b19a3edb |
| K240 | sol61-31 | `sol61_push/HORIZON_SHARING_RESULTS.md` | Brodie two-horizon entropy sharing a0=cH/6 | 0.482 | odd | DATA-LEVEL landing but entropy one-form not integrable; no covariant completion | 25b775fb0 |
| K299 | sol61-90 | `sol61_push/puzzle_32pi_micro_2026_10_14` | exponential-ensemble large-deviation log potential | {3.5} | menu | MISS: classical invariant 4 gives ~3.5; 64pi only at tuned state | untracked |
| K320 | sol61-111 | `sol61_push/horizon_mechanism_attempt_2026_10_14/REPORT.md` | lukewarm RN-dS entropy maximum | - | free | CLOSURE: alpha is an input | fb6d2bd49 |
| K321 | sol61-112 | `sol61_push/cold_horizon_connection_2026_10_14/REPORT.md` | SdS entropy identity; geometric-mean radius | - | free | identity only | fb6d2bd49 |
| K343 | RR-24 | `real_research/CKN_LAMBDA_VALUE_VERDICT_2026-06-06.md` | CKN bound saturated (4/Z^2 = 3/8pi) | - | free | CONDITION: identity iff Z^2=32pi/3; the O(1) is chosen | 9415534ae |
| K344 | RR-25 | `real_research/THE_COSMIC_SEESAW.md` | seesaw E_L = sqrt((2/Z) E_P E_H) | - | free | IDENTITY | 64f15e30d |
| K349 | RR-31 | `real_research/COEFFICIENT_DEFINITIVE_VERDICT.md` | 'second BH 1/4' candidates | {1.447, 2.05, 0.25, 0.241, 0.707} | menu | MISS: BH 1/4 already spent inside 8pi | f1535b7d8 |
| K351 | RR-33 | `real_research/COEFFICIENT_DEFINITIVE_VERDICT.md` | hbar^0 fingerprint / AeST saddle blindness | - | free | CLOSURE: a0 absent from on-shell action | f1535b7d8 |
| K354 | RR-36 | `real_research/FORCING_ROUTES_REWORKED.md` | Jacobson entanglement equilibrium + dS volume law | 0.482 | odd | DATA-LEVEL landing (Z~6), not forced; needs relaxed constraint | a8ae416c6 |
| K363 | RR-45 | `real_research/coefficient_from_horizon_entropy.py` | area-law equipartition; Verlinde volume law | {0.482} | menu | MENU: no uncontested route | 8685d967a |
| K373 | RV-05 | `real_research/reviews/boundary_dof_kappa_2026.py` | boundary CKN saturation from d=3 geometry | - | free | WALL: blind to kappa | 5a17ea5f2 |
| K378 | RV-10 | `real_research/reviews/entropy_coefficient_rigorous_endgame.py` | naive equipartition (excess T / Deser-Levin T) | {0.482} | menu | MENU | eb0c3301e |
| K380 | RV-12 | `real_research/reviews/holographic_entropy_chase.py` | Verlinde/Padmanabhan coefficient | {2.894, 0.461, 0.482} | menu | MENU: scheme-dependent | 6e84e00b6 |
| K386 | RV-18 | `real_research/reviews/desitter_entropy_coefficient.py` | Verlinde dS entropy + number field | - | free | CLOSURE: entropy cannot produce a square root | f1535b7d8 |
| K388 | RV-20 | `real_research/reviews/entropy_coefficient_attempt.py` | 5 horizon/entropy routes | {2.894, 1.447, 0.461, 0.706, 0.483} | menu | MENU: bracket 0.1727 | 999f94dfe |
| K390 | RV-22 | `real_research/reviews/factor_of_four_second_quarter_test.py` | second BH 1/4 vs (1/2)^2 | - | free | ROUTE-DEPENDENT | 782d61a97 |
| K410 | RV-42 | `real_research/reviews/mi_wald_entropy_normalisation_2026.py` | Wald-entropy normalisation vs 1/4 | - | free | KILL: test vacuous | ff9813cf3 |
| K411 | RV-43 | `real_research/reviews/mi_aest_entropy_discriminator_2026.py` | AeST Wald entropy | - | free | WITHDRAWN: f'=1 | ff9813cf3 |
| K412 | RV-44 | `real_research/reviews/mi_geometric_lock_entropy_2026.py` | BH 1/4 via holographic equipartition | {5.79, 0.72} | menu | MISS | 9d910f058 |
| K419 | RV-51 | `real_research/reviews/project_strained_horizon_cubic_O3.py` | O(eps^3) strained-horizon free energy vs dQ=TdS | - | free | NULL | eb0c3301e |
| K420 | RV-52 | `real_research/reviews/strained_horizon_clausius_match.py` | local Clausius relation | - | free | NULL: a0 ~ M^-1/3 | eb0c3301e |
| K421 | RV-53 | `real_research/reviews/strained_horizon_wald_theta.py` | Iyer-Wald Theta-form Delta S | - | free | NULL | eb0c3301e |
| K423 | RV-55 | `real_research/reviews/wald_entropy_aest_coefficient.py` | Wald-Noether entropy of AeST | - | free | FREE: a0 absent | 782d61a97 |
| K424 | RV-56 | `real_research/reviews/yphi32_from_entropy.py` | Verlinde route to the Y^(3/2) term | {0.461, 0.482} | menu | MENU: contested | ffad23087 |
| K425 | RV-57 | `real_research/reviews/toe_law/agentP_verlinde_coefficient.py` | Verlinde a_M=a0/6 dimension-forced | 0.482 | odd | DATA-LEVEL landing; chain contested | cc9f50b40 |
| K456 | RT-14 | `reviews/mi_horizon_entropy_route_2026.py` | C2 equipartition on the cell count | 1.447 | odd | MISS | fdc822157 |
| K457 | RT-15 | `reviews/mi_horizon_entropy_route_2026.py` | C3 equipartition on the entropy count S=N/4 | 5.79 | odd | MISS: BH 1/4 lands on Milgrom 1999 (a0=2cH) | fdc822157 |
| K460 | RT-18 | `reviews/mi_quadratic_z_escape_2026.py` | quadratic-in-Z with the BH 1/4 | - | free | CLOSED: the 1/4 carries hbar | d83f7ad40 |
| K471 | NB-03 | `nbody_2026/stage47_ds_entropy_mechanism_2026.py` | G S_dS = pi/H^2 mechanism | - | free | no kappa | 8e4d59205 |
| K489 | CFG117 | `campaign_fresh_gravity/CFG117_verlinde` | Verlinde a_V=cH/6 mapped onto the law | 0.482 | odd | DATA-LEVEL landing but shape test G1 fails 0/16 | bb504274c |
| K498 | CFG264-OD | `campaign_fresh_gravity/CFG264_rational_four` | owner's route: entropy quarter over the bulk 8pi | - | free | SCOPED NO-GO (hbar) | 236771412 |
| K559 | route3 | `qwen_claude_field_theory/closure_2026/route3_entropic_gravity_2026.py` | Verlinde entropic on H_Lambda | 0.482 | odd | DATA-LEVEL landing; not a derivation | e18afc17f |
| K561 | route4 | `qwen_claude_field_theory/closure_2026/route4_kappa_derivability_2026.py` | Verlinde 1/6 in framework variables | {0.482, 0.583} | menu | MENU: within 3.3% on alt only | 16015fc0d |
| K738 | W4-19/L1 | `why_4_puzzle/W4_19_literature_addendum` | Zhao 2008 (0802.1775): DE/DM switch where rho c^2 ~ a0^2/8piG (Newtonian field energy at a0), read as equality | 5.013 | any | MISS: kappa^2 = 8pi; misses 4a0^2/G by exactly 32pi | 726716bac |

## VM: Vacuum-energy matching (the a0 sector's vacuum = rho_DE; kernel tails, BIMOND/QUMOND)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K010 | p09 | `sonnet55_push/puzzle_32pi/p09_vacuum_self_consistency.py` | dark energy = vacuum value of the a0-sector potential | - | free | SLOT U_v=32pi <=> W_v=4; no-go withdrawn (H3); reduction stands | e1cc3587e |
| K014 | p13 | `sonnet55_push/puzzle_32pi/p13_energy_density_three_tests.py` | rho_L = W a0^2/G as the a0 sector's vacuum energy | - | free | SLOT W=4; screen T1 FAILS (AQUAL F(0) free) | e23bc853c |
| K026 | p21 | `sonnet55_push/puzzle_32pi/p21_bimond_vacuum.py` | BIMOND vacuum term -(1/2)(1+f'(1)) a0^2 M(0) | 1.39 | any | MISS: right form and sign; RAR kernel ~1.39; framework kernel diverges; coefficient inserted | 059462d13 |
| K027 | p22 | `sonnet55_push/puzzle_32pi/p22_bimond_tail_alpha.py` | minimal BIMOND with sharpened nu tail | - | free | TRADE: 1/2 needs alpha*=2.0025 (near-divergent tuning) | 895358d6e |
| K028 | p23 | `sonnet55_push/puzzle_32pi/p23_bimond_aux_metric_horizon.py` | horizons of the BIMOND auxiliary metric | - | free | CLOSURE: nothing selects I_nu=32pi | be1ea98ea |
| K029 | p24 | `sonnet55_push/puzzle_32pi/p24_what_pins_fprime.py` | what pins f'(1) | - | free | TRADE: pinning moves the coefficient into the tail | 31c63e6c0 |
| K030 | p25 | `sonnet55_push/puzzle_32pi/p25_symmetric_bimond_map.py` | exchange-symmetric BIMOND map; class-independent vacuum integral | 1.39 | any | MISS: kernel-only restatement of p21 | 97a6aeaa9 |
| K031 | p26 | `sonnet55_push/puzzle_32pi/p26_what_pins_the_tail.py` | what pins the tail (data / Milgrom-99 / Planck cutoff) | {0.59} | menu | MENU: nothing pins the tail; 32pi needs a cutoff 3e25 x Planck | 2dc5cf776 |
| K032 | p27 | `sonnet55_push/puzzle_32pi/p27_planck_cutoff_framework_kernel.py` | framework kernel + Planck cutoff | 1e-30 | any | MISS: vacuum tracks the cutoff linearly | 5812dd755 |
| K033 | p28 | `sonnet55_push/puzzle_32pi/p28_planck_cutoff_tail_family.py` | Planck cutoff with steeper-tail families | {0.84, 0.59} | menu | MENU: 32pi needs a fitted exponent | d74d80fcd |
| K034 | p29 | `sonnet55_push/puzzle_32pi/p29_exponent2_cutoffs.py` | exponent-2 tail with electron..Planck cutoffs | {0.59, 1.05} | menu | MENU: no physical cutoff reaches 32pi; needs A=0.706 | be5743071 |
| K035 | p30 | `sonnet55_push/puzzle_32pi/p30_amplitude_inv_sqrt2_planck.py` | tail amplitude 1/sqrt2 + Planck cutoff | {0.5} | menu | VOID (post-hoc near-hit on the self-defined footing; amplitude read off a fit; 1.1-3.0 sigma high vs measured a0) | 89a690a48 |
| K036 | p31 | `sonnet55_push/puzzle_32pi/p31_amplitude_inv_sqrt2_gut.py` | amplitude 1/sqrt2 + GUT cutoff | {0.51} | menu | POST-HOC | 5cbe7ef47 |
| K037 | p32 | `sonnet55_push/puzzle_32pi/p32_amplitude_inv_sqrt2_all_cutoffs.py` | amplitude 1/sqrt2 over five cutoffs | {0.50, 0.63} | menu | MENU: 3/5 cutoffs fit; data cannot pick a cutoff | e17cebdeb |
| K040 | p35 | `sonnet55_push/puzzle_32pi/p35_kernel_tail_fix.py` | kernel turn-off y_t; finite vacuum integral | - | free | TRADE: coefficient for y_t (1/2 at y_t=128.9) | 05168566a |
| K044 | p39 | `sonnet55_push/puzzle_32pi/p39_uv_completion_catalog.py` | classical UV completion Lambda c^4/a0^2 = I/2 | {1.39, 11} | menu | MISS: finite principled kernels short by x5.6-7.7 | 7de761fc2 |
| K045 | p40S | `sonnet55_push/puzzle_32pi/p40_selfconsistency_and_nice_numbers.py` | capacity principle (MOND energy saturates at vacuum energy) | 2.8 | any | MISS: no root except ~2.8 | 26510e942 |
| K051 | p45 | `sonnet55_push/puzzle_32pi/p45_vacuum_closed_form.py` | closed form (pi/4)y_t - (1/8)ln(4y_t) + 1/16 | - | free | TRADE: exact relocation into y_t | faa9cc18d |
| K055 | p49 | `sonnet55_push/puzzle_32pi/p49_orbital_sum_rule_check.py` | Sol's orbital sum rule | - | free | IDENTITY (the p21/p25 integral) | 614eab208 |
| K059 | p53 | `sonnet55_push/puzzle_32pi/p53_bimond_general_alpha.py` | BIMOND with general auxiliary coupling alpha | - | free | TRADE: alpha degenerate with y_t | 424268bec |
| K060 | p54 | `sonnet55_push/puzzle_32pi/p54_what_fixes_alpha_yt.py` | exchange symmetry forces alpha=1 | - | free | TRADE: y_t not fixed; one pure number remains | 52c96a80f |
| K061 | p55 | `sonnet55_push/puzzle_32pi/p55_turnoff_principles.py` | turn-off principles P1-P3 | {2.4, 4.3, 21} | menu | MISS | 220bff33c |
| K090 | K | `sonnet55_push/puzzle_32pi/agents/K_density_linear_family/` | AQUAL offset as vacuum energy c=int(1-mu)dy | {0.482} | menu | MENU/TRADE: OR family 0.482; coefficient moves into an untested tail | 20bdc3eb0 |
| K096 | S | `sonnet55_push/puzzle_32pi/agents/S_quasilocal_field_energy/` | Brown-York / field-energy budgets (341 principles) | - | free | CLOSURE: 0/341 hits | 243a089c9 |
| K102 | W11 | `sonnet55_push/puzzle_32pi/agents/W_fresh_ideas/` | deep-MOND k-essence attractor | - | free | CLOSURE: kappa^2=8pi/q never 1/4 (Poisson-prefactor theorem) | 1138d817f |
| K205 | KC1 | `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` | zero-mode theorem; kernel vacuum 4pi^4/15 as rho_DE | {0.98, 1.05, 0.70, 0.80} | menu | MISS: zero mode decouples a0 from Lambda; natural vacuum gives kappa ~1 (>=6.8 sigma) | d5cba7d34 |
| K206 | KC2 | `kappa_closure/k02_global_constraint_average.py` | sequestering global constraint <L_phi>/rho_Lambda | - | free | CLOSURE: five orders short (halo filling factor) | 28c61fe68 |
| K211 | sol61-02 | `sol61_push/PUZZLE_32PI_RESULTS.md` | Route 1: P2 AQUAL primitive; vacuum = additive constant | - | free | SLOT: constant invisible to the force | 739a063b4 |
| K213 | sol61-04 | `sol61_push/PUZZLE_32PI_RESULTS.md` | Route 3: magnetic gauge condensate L=-V(X) | - | free | CLOSURE: w=-1 forces V'=0; shift free | 739a063b4 |
| K218 | sol61-09 | `sol61_push/TONIGHT_32PI_RESULTS.md` | inverse fluctuation density reproducing P2 | - | free | CIRCULAR: built from the target; vacuum height chosen | 8c3efb551 |
| K219 | sol61-10 | `sol61_push/TONIGHT_32PI_RESULTS.md` | lock a0^2=kappa^2 G[-K(Q)] to a DBI pressure minimum | - | free | FREE RATIO: kappa 0.4/0.5/0.6 all admissible | 8c3efb551 |
| K225 | sol61-16 | `sol61_push/CORE_REVIEW_2026-09-30.md` | CFG43 fluid pressure cap sets a0^2 | - | free | SLOT eps=1/(32pi); all caps causal | ea962ad3a |
| K228 | sol61-19 | `sol61_push/SPECTRAL_BALANCE_RESULTS.md` | boson/fermion zero-point spectrum gives vacuum + cubic | - | free | FREE: needs a chosen h | 534020cc1 |
| K229 | sol61-20 | `sol61_push/SLOW_WALL_RESULTS.md` | wall-network energy as a Lambda proxy | - | free | CLOSURE: ratio scales as a^-3 | 3adc1a305 |
| K231 | sol61-22 | `sol61_push/RELAXING_DENSITY_RESULTS.md` | relaxing area density envelope energy | - | free | CONDITION D(1+D)^2=48pi; constant free | 5e0250fdc |
| K234 | sol61-25 | `sol61_push/VACUUM_OFFSET_SELECTION_RESULTS.md` | additive V0 in the variable-clock action | - | free | FREE RATIO | 61cc7086f |
| K244 | sol61-35 | `sol61_push/EXPANSION_BRIDGE_GAP_SPECTRUM_RESULTS.md` | multi-gap positive spectrum | - | free | FREE weights | 93a4cbaaa |
| K247 | sol61-38 | `sol61_push/puzzle_32pi/README.md` | k=2 tail-cutoff vacuum integral C(T) | - | free | FIT: T=128.9 gives 32pi; every C has a T | cfa06dbfa |
| K250 | sol61-41 | `sol61_push/puzzle_32pi/breakthrough_2026_10_05/REPORT.md` | orbital epicycle sum rule | - | free | BOUND: necessary condition only | 3b06b67c4 |
| K251 | sol61-42 | `sol61_push/puzzle_32pi/claude_variational_selector_2026_10_06` | stationarise QUMOND source energy wrt cutoff | - | free | CLOSURE: no finite T | 1288c215c |
| K252 | sol61-43 | `sol61_push/puzzle_32pi/local_cutoff_modulus_2026_10_06` | cutoff as a local field | - | free | FREE: set by the chosen V | 83b519c12 |
| K253 | sol61-44 | `sol61_push/puzzle_32pi/dynamical_cutoff_vacuum_2026_10_06` | canonical modulus u=lnT | - | free | CLOSURE: field rolls | 26fe6d3e0 |
| K254 | sol61-45 | `sol61_push/puzzle_32pi/cutoff_log_slope_2026_10_06` | power-law potential A(T) T^-beta | - | free | CLOSURE: no minimum | 8d829a2cf |
| K274 | sol61-65 | `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/CLAUDE_DELTA_AND_CUTOFF_LEMMA.md` | self-reflection equation for the cutoff exponent | - | free | FIT: free k fits any C | 07fa64b44 |
| K275 | sol61-66 | `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/algebraic_source` | 'G per solid angle' local source | - | free | CLOSURE: constant vacuum datum remains | 81af81ba8 |
| K279 | sol61-70 | `sol61_push/puzzle_32pi/selection_2026_10_06/vacuum_constraint` | four-form vacuum sequestering | - | free | CONDITION: boundary flux ratio free | 310f0d1a4 |
| K289 | sol61-80 | `sol61_push/cold_production_2026_10_11/VACUUM_SELECTOR_AUDIT.md` | direct Lambda force / Ricci-scalar portal | - | free | CLOSURE: needs xi~1e35 | e2440ea30 |
| K294 | sol61-85 | `sol61_push/puzzle_32pi_week_2026_10_14` | CFG695 saturating potential with constant C | - | free | SLOT: C absent from every derivative | untracked |
| K296 | sol61-87 | `sol61_push/puzzle_32pi_coupled_2026_10_14` | hidden-field relaxation repairs response shape | - | free | FREE | untracked |
| K314 | sol61-105 | `sol61_push/puzzle_32pi_curvature_tracking_2026_10_15` | tracker cancelling the offset in the ratio | - | free | FREE ratio | untracked |
| K328 | RR-05 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | F2 Bousso-Polchinski flux kinetic 1/2 | - | free | CLOSURE: double-count | b35a41b7f |
| K335 | RR-13 | `real_research/KAPPA_FIVE_HAIL_MARY_VERDICT_2026-06.md` | zeta/Casimir horizon zero-point energy | - | free | CLOSURE: double-count | b35a41b7f |
| K439 | RV-72 | `real_research/reviews/mi_condensate_vacuum_energy_a0_2026.py` | ghost-condensate vacuum energy fixes a0 | - | free | equivalent rewrite; cluster prediction fails | 71129b596 |
| K490 | CFG174 | `campaign_fresh_gravity/CFG174_door11_vacuum_column` | flowing Lambda-vacuum column budget | - | free | restatement | a598b90f2 |
| K508 | CFG807 | `campaign_fresh_gravity/CFG807_stiff_vacuum_route` | stiffened action revives PAPER42 vacuum route | - | free | BLOCKED: hand-set y_t | f1ba33360 |
| K518 | ARGON10-D1 | `argon_push/ARGON10_four_gaps_2026-10-16` | dark-energy normalisation gap | - | free | NOT FIXED: needs Hubble or boundary input | 3839aa9b0 |
| K567 | H016 | `hy4_push/lean/H016_the_seesaw.lean` | seesaw a0 = Lambda^2/(n M_Pl) | - | free | restatement; n empirical | 7733ce681 |
| K595 | CFG897 | `campaign_fresh_gravity/CFG897_kappa_D1_stiffness_frw_vacuum` | stiffness term's own FRW vacuum (covariant completions of -(gamma/2)/grad P/^2; timelike P; 4piG/P/<=a0) = rho_DE | - | free | CLOSURE: fixed-norm eps <= 0 (sign); w = w_total (G renorm 1e-19..1e-15); size-only kappa >= 1e7 (3e6 with O(1) non-minimal; TRADE kappa ~ c/(L* sqrt(G rho))), L* needed >= 4.9 Gpc: EXCLUDED; Maxwell/tether/law vacuum vanish; free (div P)^2 CONDITION | 303517f23 |
| K598 | CFG900 | `campaign_fresh_gravity/CFG900_kappa_D4_lorentz_nodal_medium` | nodal fermion medium made Lorentz-invariant (v = c), its own filled-band vacuum = rho_DE (strict LI Dirac sea; ring with cone dim reg / tube / Pauli-Villars; timelike P0 loci) | - | free | CLOSURE: strict LI has only point nodes -> m^D vs /P/^(D-1) (NO LAW); universal beta/P/^3/3 vanishes at P_cos = 0 (IDENTITY); tube E0 < 0, w = +1/2 (sign lock); PV constant sign free; every link kappa^2 = 12pi/(sigma lambda^3) (one-parameter map; v and hbar cancel); excluded posits slot 6.14 / horizon 0.643 miss | 8b1267c5d |
| K621 | W4-03/AS725 | `why_4_puzzle/W4_03_unrun_as_proposals` | mu(g) = K'(g)/(2g) integrability with a vacuum functional of K | - | free | CLOSURE: K0 free (k01 zero mode); Newtonian offsets diverge (Q: -a0 g; MU2: -8 a0^2 ln g), no finite K0-free vacuum | 3c96c6ce3 |
| K633 | W4-04/R2T | `why_4_puzzle/W4_04_microscopic_normalization` | gapless bosonic thermal zero mode and common amplitude ratios | - | free | NO MOND PREDICTION: formal ratios 16/15 and 16/5 cancel species/hbar/common slope; cubic negative, low-field quadratic dominant, high-field response suppressed, state w=1/3; relative species slopes alter ratio unless symmetry forbids | a811e18fb |
| K655 | W4-08/R1b | `why_4_puzzle/W4_08_positive_mond_amplitudes` | equal-weight split boson-fermion bands with critical quadratic cancellation and positive same-band energy | - | free | TRADE: R(d)=(8/27)f/b^3 with physical d=Delta/L free; common factors cancel; reciprocal minimum wrong target; sheet stress not vacuum; no gap selection | 4131def0e |
| K658 | W4-08/R3FI | `why_4_puzzle/W4_08_positive_mond_amplitudes` | generate positive vacuum energy from same auxiliary using linear J deformation | - | free | CLOSURE for this branch: vacuum moves to y0>0 and IR becomes quadratic; nominal target ratio uses obsolete cubic and removes intermediate cubic window; no operational MOND amplitude | 4131def0e |
| K674 | W4-08/R1scale | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal` | common dynamical scale and physical gap with running effective potential | - | free | CLOSURE for single-log positive vacuum minimum: negative radial curvature; strict quadratic stability needs running curvature above the Schur bound; added stabilizer changes total amplitude and leaves normalization unselected | f77a0cd8d |

## FN: Field-theory normalisation of W(u) / action coefficients (four-form, spectral, heat kernel, a0-as-field)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K006 | p05 | `sonnet55_push/puzzle_32pi/p05_channel_reading.py` | 1/2 as the slope mu'(0)=N; five origins of the 2 | {0.5, 0.33, 1.0} | menu | MENU: 1/2 at d=3 is the normalisation lock (identity); 0.33-1.00 at d=4 | e8665ae36 |
| K009 | p08 | `sonnet55_push/puzzle_32pi/p08_gauss_law_form.py` | four-form / Gauss-law flux form | - | free | IDENTITY once a0:=H/Z; flux quantisation fixes Lambda only | 21dcd9724 |
| K067 | p61 | `sonnet55_push/puzzle_32pi/p61_quadrature_hyperbola.py` | quadrature law as a unit hyperbola / mass shell | - | free | RELOCATION: H_M^2 = G rho/16 | 4896943eb |
| K069 | p63-C1 | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling/` | saturated dual polarization: rho_L = cold energy's cosmic bound charge | - | pend | PENDING (hand estimate 1.447 dS / ~1.20 today; a0 ~ 1/H; expected to fail finite-W gate) | a1e430de1 |
| K070 | p63-C1b | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling/` | patch bootstrap | - | pend | PENDING (hand estimate 2.89) | a1e430de1 |
| K071 | p63-C2 | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling/` | flux lattice kappa = kappa1/N | - | pend | PENDING; MENU class (declared null ~0.71) | a1e430de1 |
| K072 | p63-C3 | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling/` | Kaloper-Sorbo monodromy quantisation (hbar audit) | - | pend | PENDING | a1e430de1 |
| K083 | D | `sonnet55_push/puzzle_32pi/agents/D_filtered_vacuum_energy/` | heat-kernel filtered vacuum / spectral sums | - | free | CLOSURE: filter-blind; 20/20 decoys also hit | 20bdc3eb0 |
| K128 | KS02 | `fable_independent_2026/kappa_slot_2026/KS02_normalisation_table.py` | graviton normalisation grid with S_dS granted | {1.447, 0.5, 0.53} | menu | MENU (CONVENTION): standard TT norm 1.447; 1/2 only by dropping the Friedmann 8pi/3; energy-density route 0.53 | 958f352c3 |
| K137 | LN7 | `fable_independent_2026/lean_2026/REV_kappa_memory_moment_dimension.lean` | kappa tied to memory first moment / D-dim Friedmann | - | free | VOID: 1/2 iff D=4, but the xi input is the D=4 value that already equals 1/2 | 23dc871c4 |
| K143 | LN13 | `fable_independent_2026/lean_2026/I14_phantom_vacuum_wall.lean` | stability threshold of a lattice Dirichlet form b=1/4-kappa2+... | - | free | VOID (naming): its 'kappa^2=1/4' is a lattice coupling, never linked to the law's kappa; killed by doorD and doorH | 93bc3420a |
| K144 | FL1 | `fable_independent_2026/L3_flux_quantisation.py` | four-form flux quantisation + membrane tension for Z/beta^2 | - | free | CLOSURE: quantisation fixes the sum; kappa needs the split | 0e20cf937 |
| K147 | FL4 | `fable_independent_2026/L40_coefficient_rigidity.py` | S9 dimensional transmutation with two condensates | - | free | TRADE: scheme-dependent O(1); 6 free choices | 3cb26cf41 |
| K149 | FL6 | `fable_independent_2026/L40_coefficient_rigidity.py` | T7 membrane charge or tension depending on a0 | - | free | CLOSURE by theorem T7 | 3cb26cf41 |
| K150 | FL7 | `fable_independent_2026/L226_kappa_and_the_free_function.py` | constant shift of a free interpolating function | - | free | REDUCTION: 1/2 needs branch coefficient b=6.684 | b17af502c |
| K151 | FL8 | `fable_independent_2026/L227_nu_rar_as_a_fixed_shape.py` | nu_RAR as the fundamental fixed shape | - | free | CLOSURE: monotone scale-free kernels cannot carry the amplitude | 1a6cdad2e |
| K153 | FL10 | `fable_independent_2026/L229_the_principle.py` | 'no independent a0': cosmological state at the 3/2 branch point | - | free | TRADE: one ratio xi/K left | f95ed77a1 |
| K154 | FL11 | `fable_independent_2026/L230_one_number.py` | single-field AQUAL in dark-energy units kappa=1/(deep slope) | 1.0 | any | MISS: parameter-free shapes give 1; excluded 7.0/10.4 sigma | 504bd5ad4 |
| K157 | OA1 | `opus_48_extended_research/kappa_audit_2026/K_AUDIT_kappa_derivation_three_premises.py` | kappa=1/(2cp) from two metric channels | {0.5, 1} | menu | VOID as a hit: two-valued; 1/2 picked empirically | 9ff48821e |
| K167 | OR6 | `opus_48_extended_research/reviews/ROUTE_AEST_JOINT_COEFFICIENT_2026-06-15.md` | joint AeST requirements | - | free | CLOSURE: a0 and Lambda in disjoint sectors | 889f30c2b |
| K177 | OR16 | `opus_48_extended_research/reviews/KAPPA_FORCING_DOOR_CLOSED_2026-06-17.md` | ghost-freedom / unitarity / holography on the Route-E action | - | free | CLOSURE: kappa is an overall normalisation | 66cac8ead |
| K178 | OR17 | `opus_48_extended_research/reviews/GHOST_FREEDOM_DOES_NOT_FIX_KAPPA_2026-06-17.md` | in-in (Galley) Route-E action + aether stability | - | free | CLOSURE: only an open inequality | 60c4885cb |
| K181 | OR20 | `opus_48_extended_research/reviews/KAPPA_CLASS6_SPECTRAL_ACTION_VERDICT_2026-06-26.md` | spectral action heat kernel; causal-set action | - | free | CLOSURE: f-moments are free cutoff data | 442a51c56 |
| K187 | OR26 | `opus_48_extended_research/reviews/door_runs/door_S_seraille_coefficient.py` | Blanchet-Seraille a0~c^2/alpha, Lambda~1/alpha^2 | - | free | TRADE: ratio of two undetermined O(1)s | 510357684 |
| K194 | OP6 | `opus_48_extended_research/papers/DESITTER_VACUUM_CANNOT_FIX_A0.md` | memory kernel = dS vacuum autocorrelation | - | free | CLOSURE: the scale-setting moment diverges (zeta(1) pole) | fe3065fc4 |
| K200 | OD2 | `opus_49_doorH/DERIVATION.md` | exact second-variation operator vs I14 | - | free | CLOSURE: boundary kappa^2=0 | 33b380c45 |
| K202 | QC1 | `qwen_claude_field_theory/closure_2026/a0_promotion_2026/A0_PROMOTION_VERDICT.md` | promotion a0^2 = alpha G (-K(Q)) in the condensate action | - | free | CLOSURE: alpha=kappa^2 a free modulus | 3fa2b8af9 |
| K208 | KC4 | `kappa_closure/k04_four_form_promotion_consistency.py` | four-form promotion a0 = beta sqrt(G) /q/ | - | free | TRADE: kappa^2 = 2 beta^2/(Z + 2 b beta^2) free ratio; F6 could never fail | 2fb80ca12 |
| K212 | sol61-03 | `sol61_push/PUZZLE_32PI_RESULTS.md` | Route 2: Blanchet-Seraille dipole + Lambda=q/alpha^2 | - | free | BOUND/FIT: 32pi needs K>=138.9; choosing amplitudes is a fit | 739a063b4 |
| K224 | sol61-15 | `sol61_push/CRITICAL_RESPONSE_RESULTS.md` | critical polarization from 2D fermion sheets | - | free | CONDITION: vacuum counterterm free | ec25883ef |
| K227 | sol61-18 | `sol61_push/BULK_FINITE_MASS_RESULTS.md` | eight-band loop kernel and finite-mass far field | - | free | CLOSURE: vacuum constant independent of the loop ratio | 7c99d3f30 |
| K249 | sol61-40 | `sol61_push/puzzle_32pi/breakthrough_2026_10_05/REPORT.md` | exchange-symmetric BIMOND NR actions | - | free | FREE: M(0) and tail free | 3b06b67c4 |
| K255 | sol61-46 | `sol61_push/puzzle_32pi/nonminimal_cutoff_selector_2026_10_06` | curvature multiplier stabilising the cutoff | - | free | BOUND kappa>1.78 | 3908b938f |
| K256 | sol61-47 | `sol61_push/puzzle_32pi/conformal_cutoff_selector_2026_10_06` | conformal coupling of the cutoff | - | free | BOUND kappa>5.6 | 3908b938f |
| K258 | sol61-49 | `sol61_push/puzzle_32pi/exceptional_scalar_selector_2026_10_06` | complete exceptionality of P(X) simple waves | - | free | CLOSURE: excludes exact deep MOND | 4c0affe15 |
| K259 | sol61-50 | `sol61_push/puzzle_32pi/stable_auxiliary_selector_2026_10_06` | stable adiabatic auxiliary amplitudes | - | free | CLOSURE: wrong response slope | 4c0affe15 |
| K260 | sol61-51 | `sol61_push/puzzle_32pi/claude_cutoff_clock_2026_10_06` | turn-off kernel as normalised-clock response | - | free | CLOSURE | 5a7ba806a |
| K265 | sol61-56 | `sol61_push/puzzle_32pi/projected_cutoff_constraint_type_2026_10_06` | finite vacuum moment vs elliptic lapse | - | free | CLOSURE | c1449c087 |
| K270 | sol61-61 | `sol61_push/puzzle_32pi/finite_acceleration_symbol_2026_10_06` | constrained ADM principal symbol | - | free | CLOSURE: negative-kinetic direction | b36fda56e |
| K281 | sol61-72 | `sol61_push/puzzle_32pi/selection_2026_10_06/analytic_uv` | positive Stieltjes spectral kernels | - | free | CLOSURE | 310f0d1a4 |
| K282 | sol61-73 | `sol61_push/puzzle_32pi/selection_2026_10_06/positive_laplace` | complete monotonicity minimum tail | - | free | BOUND: P2 must end before Y=202 if C=32pi | 310f0d1a4 |
| K290 | sol61-81 | `sol61_push/cold_production_2026_10_11/POLARIZATION_SELECTOR.md` | Blanchet-Le Tiec dipolar-fluid potential | - | free | FREE: W0 drops out of the response | e2440ea30 |
| K301 | sol61-92 | `sol61_push/puzzle_32pi_local_health_2026_10_14` | restoring potential + tensor checks | - | free | CLOSURE | untracked |
| K302 | sol61-93 | `sol61_push/puzzle_32pi_shaped_2026_10_14` | shaped positive potential | - | free | FREE C | untracked |
| K305 | sol61-96 | `sol61_push/puzzle_32pi_local_selector_2026_10_14` | local response of the joint selector | - | free | BOUND only | untracked |
| K308 | sol61-99 | `sol61_push/puzzle_32pi_response_cone_2026_10_14` | conformally coupled P(X) response | - | free | FREE C | untracked |
| K309 | sol61-100 | `sol61_push/puzzle_32pi_spatial_regulator_2026_10_14` | preferred-frame higher spatial derivatives | - | free | FREE | untracked |
| K310 | sol61-101 | `sol61_push/puzzle_32pi_source_audit_2026_10_14` | finite-source existence + one-loop matching | - | free | FREE | untracked |
| K317 | sol61-108 | `sol61_push/puzzle_32pi_relaxing_auxiliary_2026_10_15` | algebraic auxiliary interpolation | - | free | FREE C | untracked |
| K322 | sol61-113 | `sol61_push/breakthrough_search_2026_10_19/normalization/DERIVATION.txt` | Blanchet-Marsat khronon endpoint identity | - | free | FREE: family realises 1/2 and 1 alike | 0725bdf3f |
| K339 | RR-18 | `real_research/KAPPA_GATED_ACTION_BRUTEFORCE_VERDICT_2026-06.md` | gated brute force class 1: k-essence / P(X) | - | free | CLOSURE: free multiplier | untracked (gitignored *brute*) |
| K340 | RR-19 | `real_research/KAPPA_GATED_ACTION_BRUTEFORCE_VERDICT_2026-06.md` | class 2: nonlocal/fractional inertia kernels | - | free | CLOSURE: temperature root; anti-MOND sign | untracked (gitignored *brute*) |
| K353 | RR-35 | `real_research/FORCING_ROUTES_REWORKED.md` | AeST non-separable F(Y,Q) cross-coupling | - | free | INSERTED: safe branch needs a bare 1/Lambda | a8ae416c6 |
| K356 | RR-38 | `real_research/FORCING_ROUTES_REWORKED.md` | heat-kernel a0/a2 ratio on dS4 | - | free | CLOSURE: degenerate / regulator-dependent | a8ae416c6 |
| K397 | RV-29 | `real_research/reviews/kappa_unit_response_2026_09_20/` | two-channel auxiliary action with unit response | - | free | CONDITIONAL 1/2 on equal weight (named input) | c3ccd563d |
| K399 | RV-31 | `real_research/reviews/kappa_unit_response_2026_09_20/ACTION_ROUTE.md` | four-form / fixed-shape normalisation | - | free | free parameter remains | c3ccd563d |
| K409 | RV-41 | `real_research/reviews/mi_psi_search_r2Z_2026.py` | variational bound on crossover ratio r | - | free | CLOSURE | f5284541c |
| K428 | RV-60 | `real_research/reviews/mi_r_admissibility_bound_2026.py` | 7-shape menu ceiling on r | - | free | WITHDRAWN IN PART | f5284541c |
| K431 | RV-64 | `real_research/reviews/mi_response_kernel_arithmetic_2026.py` | arithmetic of the dS thermal response kernel | - | free | CLOSURE: sqrt6 obstruction | 6e5174bc0 |
| K442 | RV-75 | `real_research/reviews/mi_a0_from_one_line_2026.py` | one-line action: M1 defines a0 | - | free | CLOSURE | 2b16ee840 |
| K443 | RT-01 | `reviews/mi_bootstrap_circularity_2026.py` | local kernel conditions (sum rule / Herglotz) | - | free | CIRCULAR | cee88b905 |
| K444 | RT-02 | `reviews/mi_spectral_weight_swing_2026.py` | global weight W_above vs 12 natural values | {0.461} | menu | MENU: natural values pick 2pi | 2778aa35f |
| K447 | RT-05 | `reviews/mi_forced_weight_attempt_2026.py` | P1 fluctuation-dissipation weight R=2/pi | 1.1379 | cont | MISS +128% | 16ee75b82 |
| K448 | RT-06 | `reviews/mi_forced_weight_attempt_2026.py` | P2 crossover matching | 1.0122 | cont | MISS +102% | 16ee75b82 |
| K449 | RT-07 | `reviews/mi_dissipative_identification_2026.py` | corrected P1 dissipative weight D=1/pi | 0.3248 | cont | in today's window but called a miss vs 1/2; 0.506 knob rejected | 1676a884a |
| K451 | RT-09 | `reviews/mi_three_classes_2026.py` | weightings / target-free functionals / cancellation | - | free | spectral programme exhausted | 8920d1d8c |
| K454 | RT-12 | `reviews/mi_kappa_linear_class_2026.py` | kappa-linear spectral class; W_n ~ kappa^n | {0.461, 0.354} | menu | REPARAMETRISATION THEOREM: probe yes, derivation no; in-box naturals give 2pi | d419eee26 |
| K466 | RT-24 | `reviews/mi_eq34_inversion_banked_2026.py` | Milgrom 1994 eq.34 nonlocal class | - | free | kappa-blind | a48c88db0 |
| K467 | RT-25 | `reviews/mi_action_programme_close_2026.py` | acceleration-space action / einbein | - | free | CLOSURE | 251280714 |
| K470 | NB-02 | `nbody_2026/stage46_factor_two_from_aether_candidate_2026.py` | aether K_B renormalisation | - | free | RETRACTED: K_B=3/2 tautology; direction inverted (stage48) | 8da68daa6 |
| K486 | CFG43 | `campaign_fresh_gravity/CFG43_fluid_tie` | Henneaux-Teitelboim Lambda + cold fluid stress cap | - | free | VOID: tie exists only because kappa=1/2 is written in | 143f7a475 |
| K492 | CFG187 | `campaign_fresh_gravity/CFG187_aest_lambda_tie_candidate` | AeST with a0(Lambda) tied through the HT field | - | free | VOID: 1/2 written in | 7be5e8637 |
| K493 | CFG232 | `campaign_fresh_gravity/CFG232_door13_bimond` | BIMOND kappa^2 = -16 pi beta/(sigma_s M0) | - | free | FREE RATIO | 982fe61dd |
| K516 | astra-s04 | `campaign_fresh_gravity_astra/stage_04/scale_dynamics/README.md` | a0 as a scale field chi | - | free | CLOSURE: constant-vacuum identification forces chi=0 | e6d9add5c |
| K517 | ARGON01 | `argon_push/ARGON01_modulus_kappa_2026-10-15` | kernel lambda promoted to a dynamical modulus | - | free | NO-GO: rho_vac a free integration constant | 03dd0463c |
| K525 | AS059 | `deepseek_push/astra_spawn_ideas/results/AS059` | deep coefficient in a two-slot action | - | free | scoped | 511efeb1d |
| K526 | AS061 | `deepseek_push/astra_spawn_ideas/results/AS061` | does vacuum energy fix the susceptibility | - | free | C0 invariant | 511efeb1d |
| K527 | AS064 | `deepseek_push/astra_spawn_ideas/results/AS064` | two-channel OR response unequal split | - | free | slope = count only inside the class | 511efeb1d |
| K529 | AS067 | `deepseek_push/astra_spawn_ideas/results/AS067` | additive vacuum zero mode | - | free | zero mode confirmed | f14dd4b27 |
| K530 | AS068 | `deepseek_push/astra_spawn_ideas/results/AS068` | boundary condition removing the zero mode | - | free | COUNTEREXAMPLE | 511efeb1d |
| K531 | AS069 | `deepseek_push/astra_spawn_ideas/results/AS069` | kernel lambda vs vacuum energy | - | free | constant free | f14dd4b27 |
| K532 | AS070 | `deepseek_push/astra_spawn_ideas/results/AS070` | multiplier constraint F = 4a0^2 - G c^2 rho_L | - | free | imposed not derived | 511efeb1d |
| K534 | AS073 | `deepseek_push/astra_spawn_ideas/results/AS073` | variational selection of the coefficient | - | free | COUNTEREXAMPLE | 511efeb1d |
| K535 | AS074 | `deepseek_push/astra_spawn_ideas/results/AS074` | robustness under kernel deformations | - | free | kappa not rigid | 511efeb1d |
| K537 | AS138.C01 | `deepseek_push/astra_spawn_ideas/results/AS138` | total Ward conservation in the common action | - | free | COUNTEREXAMPLE: conservation reads 0=0; kappa a datum | 6c3bd3b7a |
| K538 | AS651 | `deepseek_push/astra_spawn_ideas/results/AS651` | four-form metric variation / Legendre vacuum energy | - | free | FREE RATIO Z/beta^2 | 125014663 |
| K539 | AS652 | `deepseek_push/astra_spawn_ideas/results/AS652` | four-form flux equation | - | free | a0 environmental | 125014663 |
| K540 | AS653 | `deepseek_push/astra_spawn_ideas/results/AS653` | general flux power | - | free | homogeneity only | 125014663 |
| K541 | AS658 | `deepseek_push/astra_spawn_ideas/results/AS658` | three-form gauge DOF count | - | free | free ratio | 125014663 |
| K543 | AS651.C01 | `deepseek_push/astra_spawn_ideas/results/AS651.C01` | MONO-kernel transfer of b | - | free | VOID: 1/2 only at a tuned ratio | e6d9add5c |
| K545 | AS252 | `deepseek_push/astra_spawn_ideas/results/AS252` | cosmological Einstein coefficient matched to G | - | free | free | e6d9add5c |
| K547 | AS-unrun | `deepseek_push/astra_spawn_ideas/` | 9 unrun proposals (AS025 AS119 AS562 AS654 AS655 AS672 AS698 AS725 AS1923) | - | pend | NOT EXECUTED (proposals only) | 511efeb1d |
| K562 | I411 | `qwen_claude_field_theory/ALREADY_TRIED.md` | brane tension at beta=1 fixes kappa | - | free | VOID: solves for the target | 33156aa08 |
| K569 | H018 | `hy4_push/H018_counting_from_the_action.py` | deep response is a unique monopole | - | free | one channel | 8a641ea74 |
| K570 | H046 | `hy4_push/H046_results.json` | do health conditions force n=2 | - | free | NOT forced | cac96f7c0 |
| K578 | G002 | `glm53_push/G002_onefunction_construction.py` | kappa=1/n with n from the SPARC slope | - | free | VOID: measured integer called derived; Lean sorry | 358768f02 |
| K580 | G031 | `glm53_push/G031_gr_fluid_action.out` | rho_L = 4a0^2/(G c^2) 'derived at action level' | - | free | VOID: tie written in (CFG43 class) | 6fc60a401 |
| K587 | R07 | `RETRACTIONS.md` | covariant MI action v1-v11 | - | free | fails for orbits | 508a12052 |
| K591 | R15 | `RETRACTIONS.md` | 'a0^2 = kappa^2 c^2 G rho derived from AeST' | - | free | RETRACTED: a target relation | 508a12052 |
| K602 | CFG911 | `campaign_fresh_gravity/CFG911_kappa_constructive_coupling` | constructive pi-free portals of a dynamical rho_DE (premise A as bimetric horizon / multiplier xi G F[T_DE]; G-free tie; canonical field strength; trace share; dynamical quintessence; areal; hemispherical flux) | {0.5, 1, 2, 1.414, 0.816, 0.707, 1.772} | menu | 1/2 ONLY IN MENUS OR POSITS: multiplier portals TRADE (kappa^2 = xi); bimetric posit X7; trace share needs d = 4 (X4); hemisphere 1/4 needs w = +1/3 (excluded); kappa-free targets: a0(z) spread by stress reading 0.13-0.25 dex at z = 2; running -(3/2)(1+w); kinetic portal excluded if DESI crossing confirmed; dynamical portal locally silent | 36a18db2e |
| K604 | W4-01/F2 | `why_4_puzzle/W4_01_untouched_gravity_families` | Kaluza-Klein on a circle (G4=G5/(2pi R)): a0 from G5 rho_DE, force-law G5N rho_DE, or c^2/R; R free, R=c/H_Lambda, or Casimir-stabilised | - | free | TRADE: R unstabilised; R=c/H_Lambda gives menu {2.171, 0.921, 2.894} all pi-odd misses; Casimir radius hbar-bearing; force-law G5 gives a pi-free a0=(8/3) R G rho but R free (R=c/sqrt(G rho) is the forbidden J=1 posit) | cafc0bf78 |
| K607 | W4-01/F5 | `why_4_puzzle/W4_01_untouched_gravity_families` | Einstein-Cartan spin-torsion energy (pi/2) G hbar^2 n^2 as the a0 scale; with independent rho_DE, or as the dark energy itself | - | free | HBAR: kappa^2 ~ hbar^2 n^2/rho (excluded); spin energy as the DE gives kappa = 1 by construction (identity, wrong sign, not scored) | cafc0bf78 |
| K610 | W4-02/portal/R1 | `why_4_puzzle/W4_02_independent_portal_audit` | fixed-metric symmetry, canonical normalization, Born-Infeld duality and granted weak-field no-force | - | free | TRADE/CLOSURE: physical xi=(alpha_c^2/G)(T/C); vacuum identity operator and source normalization remain independent; even C=T plus no-force yields a non-MOND threshold xi=Omega_(d-2), not law selection | 04d9b80a9 |
| K611 | W4-02/portal/R2 | `why_4_puzzle/W4_02_independent_portal_audit` | causal response selection with fixed vacuum: exact simple-mu and quadratic preferred-frame scalar families | - | free | NO SELECTION: every xi>0 has the same fixed vacuum parameter and high-field G, positive scalar time kinetic energy and subluminal local cones at finite nonzero gradient; effective toys, not full covariant completions; independent proof audit; 34/34 checks and three mutations bite | 04d9b80a9 |
| K617 | W4-03/AS654 | `why_4_puzzle/W4_03_unrun_as_proposals` | four-form P(q) = Z q^2/2 + C0 with a0 = beta sqrt(G) q | - | free | CONDITION: kappa^2 = 2beta^2/(Z - 2C0/q^2); the LOCK needs C0 = 0 and nothing names it; a0^2 = (2beta^2 G/Z)(eps + C0) (offset tracking if w != -1) | 3c96c6ce3 |
| K618 | W4-03/AS655 | `why_4_puzzle/W4_03_unrun_as_proposals` | four-form P(q) = Z q^2/2 + lambda q^4/Q0^2 | - | free | TRADE: kappa^2 = 2beta^2/(Z + 6 lambda q^2/Q0^2) runs; tracking slope (Z+6x)/(2(Z+12x)) < 1/2 | 3c96c6ce3 |
| K619 | W4-03/AS672 | `why_4_puzzle/W4_03_unrun_as_proposals` | rigidity as the functional equation a0(q)^2 = kappa^2 G [q P_q - P] | - | free | CLOSURE: solvable for every kappa (0.3, 0.5, 0.7 and general a0(q)); free zero-energy mode C q; linear a0 reproduces k04 | 3c96c6ce3 |
| K622 | W4-03/AS1923 | `why_4_puzzle/W4_03_unrun_as_proposals` | compact three-form quantisation q = 2 pi n f/Vol in k04 | - | free | TRADE: kappa^2 = 2beta^2/(Z + 2b beta^2) independent of n, f, Vol (= FL1/K144); unit flux spacing gives nothing | 3c96c6ce3 |
| K624 | W4-05/V1 | `why_4_puzzle/W4_05_self_determined_vacua` | EiBI gravity: no separate cosmological term (lambda = 0, kappa_E < 0) fixes Lambda_eff = 1/l^2; a = c^2/l; lambda free variant | 5.013 | odd | MISS: kappa^2 = 8pi (pi x algebraic), kappa 5.013; lambda free -> TRADE | c506c58b3 |
| K630 | W4-05/V7 | `why_4_puzzle/W4_05_self_determined_vacua` | TeVeS a0 = sqrt(3k) c^2/(4 pi l) with Lambda free | - | free | TRADE: k, l, Lambda independent (original TeVeS tensor speed excluded by GW170817, recalled) | c506c58b3 |
| K631 | W4-04/R1 | `why_4_puzzle/W4_04_microscopic_normalization` | local supersymmetry: nilpotent de Sitter SUGRA and canonical BI/new-FI vacuum-response identity | - | free | NO OPERATIONAL SELECTION: V=2T-3Mp^2 m32^2; restricted m32=0 fixes electric c4 V=1/4, not xi; actual field Coulombic in IR; fixed-V fixed-canonical-source SUSY deformation changes T | a811e18fb |
| K634 | W4-04/R3 | `why_4_puzzle/W4_04_microscopic_normalization` | D3 DBI+CS+bulk normalization, stretched endpoint electric threshold and leading KKLT stabilized vacuum | - | free | TRADE/WRONG FORCE: endpoint critical electric force equals string tension, acceleration depends on mass/separation; IR Coulombic; net vacuum differs from brane tension; explicit single-real-modulus Minkowski crossing leaves vacuum ratio variable; no flux-landscape no-go | a811e18fb |
| K637 | W4-07/B1 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | partially massless spin-2 in dS: Higuchi bound saturated, m^2 = (d-2)H^2 fixed by gauge symmetry; a0 = m c^2 | 4.093 | odd | MISS: kappa^2 = 16pi/(d-1) = 16pi/3 at d=4 (pi x algebraic); rigid through H | 2e238ed36 |
| K638 | W4-07/B2 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | conformally coupled scalar in dS: m^2 = R/6 = 2H^2 fixed by conformal symmetry; a0 = m c^2 | 4.093 | odd | MISS: kappa^2 = 4pi d/(d-1) = 16pi/3 at d=4 (pi x algebraic); differs from B1 at d=5 | 2e238ed36 |
| K643 | W4-07/B7 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | seesaw realised as Berezhiani-Khoury superfluid a0 = alpha^3 Lambda^2/M_P with Lambda^4 = eps_DE | - | free | TRADE: hbar cancels; kappa^2 = alpha^6 (non-reduced M_Pl) or 8pi alpha^6 (reduced); alpha free | 2e238ed36 |
| K644 | W4-07/B8 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | flat-space amplitude positivity bounds | - | free | CLOSURE: no flat-space vertex depends on a vacuum constant; eps enters only via curvature (H-type) | 2e238ed36 |
| K654 | W4-08/R1 | `why_4_puzzle/W4_08_positive_mond_amplitudes` | full regulated critical Dirac band with positive cubic IR and quadratic UV static response | - | free | TRADE: full homogeneous static Hessians positive but raw band energy negative; positive baseline sigma remains free; criticality unprotected; no healthy microscopic normalization | 4131def0e |
| K656 | W4-08/R2 | `why_4_puzzle/W4_08_positive_mond_amplitudes` | documented two-field MOND superfluid amplitude parent with both radial modes retained | - | free | TRADE: open local quadratic positive Hamiltonian region but a0=lambda^3/(8pi G Lambda) with lambda and V0 free; charged state not vacuum; supermetric low-energy characteristic; no full healthy UV claim | 4131def0e |
| K657 | W4-08/R3 | `why_4_puzzle/W4_08_positive_mond_amplitudes` | exact second-class auxiliary MOND response with positive reduced energy and canonical physical bracket | - | free | TRADE: exact attractive g=gN+sqrt(a0gN) but R=8epsilon0/(9gamma b^3) free; positive kinetic regulator tachyon; quantum vacuum constraint rank changes | 4131def0e |
| K663 | W4-11/Q3 | `why_4_puzzle/W4_11_last_gravity_classes` | bumblebee vector with V(B^2 -+ b^2) | - | free | TRADE: vacuum constant independent of b | 1cbcd12ee |
| K665 | p63-C1 | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling` | RESULT of pending K069: saturated dual polarization (dark energy = cold energy's cosmic bound charge) | 1.198 | free | INCONSISTENT: cosmic state at saturation, W -> +inf (premise gate fails); kappa_L 1.198, a0 ~ 1/H(z) (OTHER). Supersedes the PENDING status of K069 | 5df0e1cd8 |
| K666 | p63-C1b | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling` | RESULT of pending K070: patch bootstrap (bound charge inside R = c/H_L equals the vacuum mass) | 2.894 | odd | FORCED-OUT / MISS: Z = 1, kappa_L 2.894 (tracking, finite W). Supersedes the PENDING status of K070 | 5df0e1cd8 |
| K667 | p63-C2 | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling` | RESULT of pending K071: flux lattice kappa = kappa_1/N | {0.5, 0.333, 0.25} | menu | MENU (spurious 1/2): kappa_1 = 1 lands at N = 2, 3, 4; null 0.71; the lattice does not single out N = 2. Supersedes the PENDING status of K071 | 5df0e1cd8 |
| K668 | p63-C3 | `sonnet55_push/puzzle_32pi/p63_a0_field_coupling` | RESULT of pending K072: Kaloper-Sorbo monodromy quantisation | - | free | FREE: quantisation fixes (f, mu, e) only; beta^2/Z free; no hbar. Supersedes the PENDING status of K072 | 5df0e1cd8 |
| K675 | W4-08/R4vector | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal` | temporal-vector second-class completion with radial MOND source and principal cones | - | free | TRADE: nonnegative constrained classical energy and positive-source MOND branch; epsilon0/(gamma b^3) free; zero-field longitudinal degeneration and microscopic clock/current completion unresolved | f77a0cd8d |
| K676 | W4-08/R5scalar | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal` | regular charged sextic scalar pressure parent with amplitudes retained | - | free | TRADE: regular classical cubic pressure and mV^2=gamma Y/2 derived; this half is not law kappa; exact Gauss current forbids sole nonzero homogeneous condensate without compensating charge | f77a0cd8d |
| K679 | W4-08/R6neutral | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/NEUTRAL_CURRENT_TEST.md` | two opposite-charge regular sextic condensates with a neutral clock and exact Gauss current | - | free | CLOSURE under explicit affine-gradient fixed-charge hypotheses: regular neutral clock has quadratic IR and medium stress; dilute exact pair switches off; concavity excludes positive cubic after critical linear subtraction; derivative-current completions remain open | 3a26d1eb9 |
| K680 | W4-08/R7current | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/current_interactions` | regular polynomial charge-current coupling alpha j0 times scalar gradient squared | - | free | CLOSURE for this classical sector: exact canonical charge shifts; zero-charge amplitude stays empty; fixed-charge critical subtraction gives h^4 not positive h^3; Hamiltonian regular in Cartesian fields | 73cb47a32 |
| K682 | W4-08/R9Jacobian | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/current_interactions` | independent Jacobian topological current coupled to Maxwell and sextic charged matter | - | free | TRADE/CLOSURE in trivial compact sector: local neutrality gives positive two-gradient cubic but full Gauss permits empty-scalar electric-flux trial with excess O(delta^4); no single-scalar 3-space MOND or vacuum selector | 73cb47a32 |
| K683 | W4-08/R10CS | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/current_interactions` | Chern-Simons charge-flux constraint and selfdual sextic coupling | - | free | TRADE: positive magnetic lower envelope is not full constitutive coefficient because covariant gradients remain; planar source/duality bridge missing; selfdual vacuum energy zero and positive additive constant free | 73cb47a32 |
| K684 | W4-08/R11axion | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/current_interactions` | regular 3+1 axion magnetic current coupled to positive cubic temporal pressure | - | free | CLOSURE under finite-norm zero-external-flux and vanishing electric boundary assumptions: transverse projection gives nonnegative integrated Gauss identity forcing Y=0; fixed flux is a different untested state | 73cb47a32 |
| K686 | W4-08/R12Fzero | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | noncanonical supersymmetric chiral auxiliary branch with zero superpotential | - | free | CLOSURE for specified constant-coefficient model: constant nonzero branch has negative rigid energy and negative fermion coefficient; real scalar has no derivative response | 814cbf3fe |
| K687 | W4-08/R13Ffold | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | linear-superpotential chiral fold with positive rigid vacuum and positive static cubic correction | - | free | CLOSURE for this model: double root imposed; critical timelike continuation disappears and alternative roots have a decoupled chi ghost; IR remains quadratic and displayed large-gradient action quartic; nominal Taylor ratio is not physical MOND R | 814cbf3fe |
| K689 | W4-08/R14D | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | ordinary minimal nonlinear-electrodynamics auxiliary and specified neutral-gradient portal | - | free | SCOPED CLOSURE: regular convex branch cannot give cubic cusp; finite critical portal cusp violates stated convexity class and parity-even oriented case has a supermetric photon mode; generalized D operators remain outside test | 814cbf3fe |
| K690 | W4-08/R14BI | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | exact Born-Infeld ordinary-FI elimination and vacuum versus canonical nonlinearity relation | - | free | TRADE: displayed rigid vacuum over canonical tension equals 1-1/B with free FI ratio; no MOND cubic and diagnostic gradient portal gives h^4; gravitating vacuum interpretation not derived | 814cbf3fe |
| K693 | W4-08/R15clock | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | rational clock-projected chiral auxiliary branch with positive rigid vacuum and actual MOND plus Newtonian limits | - | free | PARTIAL/TRADE: conditional rigid R4096/1125 and scalar xi125pi/128 use real IR and UV coefficients; selected static branch convex; allowed operator changes ratio; gravitating clock and quantum bridges absent | 65be2b68f |
| K696 | W4-08/R16form | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | analytic nonlinear top form with bounded scalar gradient portal and fixed canonical flux | - | free | PARTIAL/TRADE: selected zero-flux branch gives exact MOND plus Newtonian crossover and bounded scalar cones with fixed clock; same-form vacuum zero; extra inner branch and zero-field degeneration remain | 65be2b68f |
| K697 | W4-08/R16flux | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | same-form positive vacuum from finite flux in the exact MOND crossover prototype | - | free | CLOSURE for tested normalization: finite flux gives nonzero IR stiffness and force boost at most1+b/Y0; using obsolete zero-flux C3 to match target forces Y0>b and removes cubic window; no operational target ratio | 65be2b68f |
| K704 | W4-08/R17force | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/gravity_constraints` | universal conformal physical metric and actual tensor-plus-scalar MOND amplitude | - | free | TRADE: Guv=Gt+Gs and aIR=f a_s give xiV0=f^3(125pi/128); scalar charge remains free; Friedmann-inferred density introduces Guv/Gcos; rigid scalar-only ratio is not physical prediction | 590d17d77 |
| K708 | W4-08/5Ddielectric | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_normalization` | radial relaxation of critical dielectric with added N1 cubic potential and FI uplift | - | free | PARTIAL/CLOSURE: positive electric cubic and fixed-D minimum are real; critical photon kinetic and vacuum energy vanish; added potential coefficient unprotected; FI restores quadratic IR; like-charge force repulsive; reversed-regime L and H ratios not operational MOND amplitudes | eeb8b9492 |
| K710 | W4-08/disformal | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_normalization` | universal changed physical matter metric and source-lensing amplitude dictionary | - | free | TRADE: TeVeS-shaped gamma1 family has free canonical scalar charge at fixed response; actual-V xi keeps f-cube while inferred footing gains B0^2 for general reference; saturated-neighborhood cone rule is added assumption; inherited matter-free clock instability unchanged; no healthy selector | eeb8b9492 |
| K715 | W4-08/geometric-metric | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/geometric_source` | higher-gradient superfluid gravitational order parameter with universal attractive metric source and exact broken-branch interpolation | - | free | PARTIAL/TRADE: C2=Mpl^2 and C3=2Mpl^2/(3a0) give actual metric MOND in a local algebraic EFT window; a0 input; finite-Z gradients nonuniform; finite-density fluid not vacuum; no microscopic selector | be8fc76cb |
| K731 | W4-18/B3 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Hardy/BF inverse-square 1/4 and the dS4 complementary-series / critical-damping edge m = 3H/2 as a0/c | 4.342 | odd | MISS: no Hardy slot (deep-MOND perturbation exponents +-sqrt(l(l+1)/2), no tunable coupling); edge kappa = sqrt(6pi) pi-odd | 918a2439d |
| K742 | W4-19/L5 | `why_4_puzzle/W4_19_literature_addendum` | Navarro & Van Acoleyen 2006 (gr-qc/0512109): a0 = c mu from f(R,P,Q) curvature invariants | - | free | FREE: mu set by the chosen f (read from a summary only) | 726716bac |
| K750 | W4-22/M | `why_4_puzzle/W4_22_gauss_times_loop_model` | Gauss-normalized Newtonian stiffness c^4/(8piG) x 3D one-loop MOND cubic (zero mode, N dof, mass lambda/grad Phi/) x tree vacuum | - | free | TRADE: R = (32pi N^2/9) Y, kappa = 1/(N sqrt Y) pi-free, N = 2 prefactor exactly 128pi/9 = (8pi)^3/(6pi)^2; the 4 relocates to N^2 Y = 4 (Y = 1, N = 2 is H061); Newton-leading at low field, and the MOND-shape cancellation re-glues the pi (xi = pi^3 N T^4/27 eps); signs barred by concavity | f216b048f |
| K752 | W4-23/M | `why_4_puzzle/W4_23_gauss_law_flux_rescue` | minimal fixed-flux (Gauss-law) medium: inf_x[a x^-n + b t x^(n-2)], t = gN^2, separate vacuum | - | free | TRADE: dimension-fixed deep-MOND exponents (n = 3: g = gN + sqrt(a0 gN)); stable only for the electrostatic sign; for gravity's attractive sign the branch is a maximum (W4-08 tachyon); R = eps/(54 a b^3 K^3), xi = 192 pi a b^3 K^3/eps | 439c6ba1d |
| K755 | A0SEL-20261024/SCALE | `reviews/a0_selection_2026_10_24` | classical two-scalar scale-invariant vacuum | - | free | TRADE: uniform positive quartic rescaling preserves stationary angle but scales Einstein-frame vacuum; radial modulus and response map remain unfixed | freeze:87e0c60793 |
| K759 | MICROMED-20261024/LAMBDA | `reviews/microscopic_medium_2026_10_24` | protected Lambda-solid scaling symmetry and nonlinear shape response | - | free | TRADE: symmetry-compatible eta*(Tr B^2/(Tr B)^2-1/n) preserves background and changes shear; its square preserves quadratic data but changes nonlinear response; strain is not identified with MOND acceleration | freeze:36c2d800d1;continuation:0e132d0606 |

## PS: 16pi / 32pi / pi-counting and geometric structures (Gauss-Bonnet, SdS/Nariai, membranes, Tolman/Komar)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K001 | p01 | `sonnet55_push/puzzle_32pi/p01_exact_reductions.py` | Gauss-Bonnet integrals; A*Lambda=32pi^2 <=> K_Sigma=rho_Lambda | - | free | CLOSURE: int E4=64pi^2 at every size; 32pi^2=(8pi)(4pi) is bookkeeping | 4e233d832 |
| K007 | p06 | `sonnet55_push/puzzle_32pi/p06_embedding_no_go.py` | literal a0-horizon in its own dS (SdS/Nariai/Israel walls) | - | free | BOUND kappa>=1.447 for embedding; partly WITHDRAWN (audit H1/H2) | b77650457 |
| K008 | p07 | `sonnet55_push/puzzle_32pi/p07_membrane_probe_target.py` | Brown-Teitelboim membrane probe acceleration | - | free | FREE RATIO e/sigma=3/(2sqrt2); 'closed' withdrawn (H1) | 3416d61fb |
| K020 | p17 | `sonnet55_push/puzzle_32pi/p17_natural_conditions.py` | 13 standard BH/vacuum conditions solved for G rho r^2 | {0.92, 1.45, 2.05, 2.51, 3.54, 5.01} | menu | MISS: each row carries one net pi; none in window | b92128c23 |
| K021 | p18 | `sonnet55_push/puzzle_32pi/p18_heaviside_units.py` | p17 redone in Heaviside-Lorentz units | - | audit | AUDIT: units relabel; 8pi/3 gap unit-invariant | 3241bbeda |
| K022 | p19 | `sonnet55_push/puzzle_32pi/p19_horizon_flux.py` | horizon flux balance int Lambda dA <= int K dA | 2.5 | any | MISS: GR's 8piG gives ~2.5; 1/2 needs coupling G with no reason | 498b37a11 |
| K058 | p52 | `sonnet55_push/puzzle_32pi/p52_gauss_flux_candidates.py` | 12 Gauss field/source pairs over the a0 horizon | {0.5, 0.71} | menu | VOID: the one pair giving 1/2 is unphysical (light orbit at r*; cube source) | b85d70465 |
| K073 | R-KT | `sonnet55_push/puzzle_32pi/README.md` | Gauss-Bonnet Kounterterm; Wald entropy | 1.45 | any | MISS (hand check) | 4896943eb |
| K079 | L5 | `fable_independent_2026/lean_2026/PUZZLE_32pi_premise_A_2026_10_05.lean` | premise A: MOND sector couples via G not 8piG | - | free | CONDITIONAL 1/2: the premise is the answer; Cassini rejects its class (p58) | 3fd60f9fb |
| K086 | G | `sonnet55_push/puzzle_32pi/agents/G_symmetry_conformal/` | dS/conformal symmetry; dilatation; AQUAL offset | {2.89, 0.99} | menu | MISS: algebraic-vs-pi dichotomy | 20bdc3eb0 |
| K089 | J | `sonnet55_push/puzzle_32pi/agents/J_membrane_extremality/` | membrane BPS / no-force / quantisation for e/sigma | {1.45, 2.89} | menu | MISS: e/sigma free; n=16 near-hit matched by 58% of decoys | 20bdc3eb0 |
| K091 | L | `sonnet55_push/puzzle_32pi/agents/L_sds_two_horizon/` | SdS two-horizon point selection | - | free | CLOSURE: monotone family realises every value | 20bdc3eb0 |
| K092 | M | `sonnet55_push/puzzle_32pi/agents/M_two_parameter_algebra/` | kinematical algebra with a0 and Lambda as deformations | - | free | CLOSURE: nothing forced | 243a089c9 |
| K097 | T | `sonnet55_push/puzzle_32pi/agents/T_weyl_conformal_gravity/` | Weyl gravity / Mannheim-Kazanas invariants | 0.07 | any | MISS: a0 is a gauge parameter; the theory's gamma0 gives ~0.07 | 243a089c9 |
| K103 | X1 | `sonnet55_push/puzzle_32pi/agents/X1_one_generator/` | one generator of the 4's (Noether/Euler) | - | free | CLOSURE: TT-Euler match is a D=4 accident | 1138d817f |
| K106 | Y | `sonnet55_push/puzzle_32pi/agents/Y_maximal_force/` | maximal force / string tension / dS C-metric | {7.1, 0.482} | menu | MENU: 6F_max is Friedmann written as a force; 0.482 = Verlinde Z=6 restated | 1138d817f |
| K110 | N1 | `sonnet55_push/puzzle_32pi/agents/N1_algebraic_lambda_Z/` | Nariai-type algebraic vacuum acceleration Z=3sqrt3 | 0.557 | odd | VOID as a hit: radius outside the static patch; in-patch radii give Z=sqrt3 (excluded >7 sigma); menu post-hoc (28% false match) | e6d9add5c |
| K113 | B1 | `sonnet55_push/puzzle_32pi/agents/B1_global_boundary_tie/` | global ties among SdS / Einstein-Straus radii | - | free | CLOSURE: coincidences algebraic, never 8pi | e6d9add5c |
| K132 | KS06 | `fable_independent_2026/kappa_slot_2026/KS06_number_field.py` | pi-decomposition of 1/(32pi); rate vs density mechanism | - | free | CONDITION: a rational kappa is allowed; value rides on the graviton convention | 958f352c3 |
| K168 | OR7 | `opus_48_extended_research/reviews/FRONTIER1_D3_STRUCTURE_Z_2026-06-15.md` | dimension dependence Z_d | - | free | VOID: 5.789 at d=3 only with kappa=1/2 held fixed (back-fitted) | 735f3518e |
| K195 | OP7 | `opus_48_extended_research/papers/DESITTER_GAUGE_MOND_SCALE.md` | gauged SO(4,1) gravity | - | free | CLOSURE: one free number | 282457e11 |
| K209 | KC5 | `kappa_closure/k05_is_32pi_special.py` | is 32pi special (natural vacuum constructions) | {2.894, 1.447, 0.461, 4.19, 8.38} | menu | MISS: the only content is 1/kappa^2=4; 104 simple constants within 1 sigma | 3de3f608b |
| K236 | sol61-27 | `sol61_push/SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md` | density-length identity r_U^2 Lambda=16pi/S* | - | free | CONDITION | 69f7a0d06 |
| K278 | sol61-69 | `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/NORMALIZATION_SCREEN.md` | d-dim Newton calibration with J=G rho r*^2/c^2=1 | - | free | VOID: exactly 32pi in d=4 only if J=1 (chosen) | 81af81ba8 |
| K284 | sol61-75 | `sol61_push/geometric_selection_2026_10_10/REPORT.md` | regularity + cosmological length + Phi(L)=0 | - | free | FREE: continuous counterfamily | f6d4abc64 |
| K295 | sol61-86 | `sol61_push/puzzle_32pi_coefficient_verdict_2026_10_14` | counterfamily / spin-2 projector 1/2 / int E4 / CKL averaging | {0.58, 0.5} | menu | VOID as a hit: spin-2 1/2 misapplied to vacuum; CKL 24pi rests on assumed averaging | untracked |
| K300 | sol61-91 | `sol61_push/puzzle_32pi_dynamic_2026_10_14` | scalar-Euler f(a)E4 curvature bridge | - | free | FREE beta | untracked |
| K304 | sol61-95 | `sol61_push/puzzle_32pi_joint_selector_2026_10_14` | scalar-Gauss-Bonnet log coupling | - | free | FREE gamma | untracked |
| K327 | RR-04 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | F1(d) dS surface gravity c^2/2R_dS | 2.894 | odd | MISS: GH 1/2 already spent building cH | b35a41b7f |
| K345 | RR-26 | `real_research/THE_FACTOR_OF_FOUR.md` | free-fall c/2 / surface-gravity / BH-1/4 readings | - | free | VOID as derivation: 1/2 posited | eb0c3301e |
| K346 | RR-27 | `real_research/THE_FACTOR_OF_FOUR.md` | Jeans-scale reading 1/sqrt(pi) | {0.564} | menu | MENU: a reading, not selected | eb0c3301e |
| K348 | RR-29 | `real_research/FORCING_THE_COEFFICIENT.md` | factor-by-factor Z^2 = 4 x 8pi/3; density / Unruh / Verlinde routes | {0.5, 0.461, 0.482} | menu | MENU: route-forced not uniquely forced (8% spread) | 3d8c0388f |
| K352 | RR-34 | `real_research/ANHARMONIC_AND_32PI.md` | 32pi as anharmonic gearing 8pi x 4 | - | free | VOID: 1/2 is the free-fall convention | 95d162aac |
| K355 | RR-37 | `real_research/FORCING_ROUTES_REWORKED.md` | normalisation principle for the factor 4 | - | free | CONVENTION | a8ae416c6 |
| K357 | RR-39 | `real_research/FORCING_ROUTES_REWORKED.md` | bound saturation (max force / min accel / dS surface gravity) | {2.894, 1.447} | menu | MISS: never 32pi | a8ae416c6 |
| K365 | RR-47 | `real_research/coefficient_membrane_stress_route.py` | membrane balance T_rr(R_dS)/rho c^2 | - | free | CLOSURE: 1/2 needs an unforced RHS 1/(24pi) | eb0c3301e |
| K370 | RV-02 | `real_research/reviews/Z_boundary_geometry_2026.py` | dS4 d=3 boundary geometry synthesis | - | free | POSITED: the 2 is free | bfc5b92ba |
| K372 | RV-04 | `real_research/reviews/dS4_boundary_measure_Z_2026.py` | d=3 conformal-boundary measure | - | free | shape only | 5a17ea5f2 |
| K375 | RV-07 | `real_research/reviews/derive_Z_cleanest.py` | a0 = surface gravity of the free-fall horizon R*=c/sqrt(G rho) | - | free | VOID as derivation: 1/2 by a posited principle (J=1) | eb0c3301e |
| K377 | RV-09 | `real_research/reviews/derive_Z_firstprinciples.py` | route-by-route factor 2 | - | free | VOID: the 2 is a posit (half-derived) | eb0c3301e |
| K392 | RV-24 | `real_research/reviews/factor_of_two_horizon.py` | surface gravity of the Hubble-enclosed mass cH/2 | 1.447 | odd | MISS: a real horizon 2 but 2.9x too big | f1535b7d8 |
| K393 | RV-25 | `real_research/reviews/horizon_at_sqrt8pi3.py` | search for a horizon at sqrt(8pi/3) R_H | - | free | CLOSURE: none exists | cae38b598 |
| K415 | RV-47 | `real_research/reviews/project_Z_under_psr.py` | principle-of-sufficient-reason readings | 0.461 | odd | DATA-LEVEL landing (Z~2pi); O(1) unselected | c44951c49 |
| K433 | RV-66 | `real_research/reviews/mi_pi_free_area_2026.py` | pi-free horizon area + GHY | - | free | derives Milgrom r=1 then excluded | 143550dbe |
| K434 | RV-67 | `real_research/reviews/mi_geometric_lock_embedding_2026.py` | curvature-invariant / Frenet geometric lock | 1.633 | any | MISS (a0=cH_L/sqrt(pi) falsified) | 9d910f058 |
| K458 | RT-16 | `reviews/mi_horizon_entropy_route_2026.py` | C4 Komar/Tolman /rho+3p/=2rho | 0.707 | any | MISS | fdc822157 |
| K475 | NB-07 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T007 GHY-to-bulk ratios | - | free | 0/3 | b062ad4a2 |
| K496 | CFG264-R1 | `campaign_fresh_gravity/CFG264_rational_four` | deep-MOND virial + vacuum virial | - | free | SCOPED NO-GO | 236771412 |
| K497 | CFG264-R2 | `campaign_fresh_gravity/CFG264_rational_four` | two-sided Israel junction of a MOND wall with the vacuum | - | free | pi-free nearest miss: needs sigma=(4/3)a0/G; nothing supplies it | 236771412 |
| K500 | CFG380 | `campaign_fresh_gravity/CFG380_32pi_geometric_door` | Penrose / quasi-local / area bounds / Einstein manifolds | - | free | NO: nothing within 5% | 805445a61 |
| K501 | CFG417 | `campaign_fresh_gravity/CFG417_tolman_kappa_vs_desi` | Tolman reading kappa=1//1+3w0/ vs DESI DR2 | {0.66, 1.00, 0.79, 2.16} | menu | MENU on a measured w0 (forbidden input today); a chosen reading | cf12f7411 |
| K522 | AS005 | `deepseek_push/astra_spawn_ideas/results/AS005` | identity kappa Z_H = sqrt(8pi G_E/(3G_N)) | - | free | identity | 511efeb1d |
| K556 | q36-parity | `qwen_36_experiment/opus_orchestrator_oracle/LEDGER.md` | pi-evenness: local routes give rationals; BH-1/4 conjecture | - | free | VOID as derivation: conjecture (post hoc p=0.028) | 6b7edf77c |
| K574 | gemini-solve | `gemini_pi_puzzle/SOLVING_THE_PUZZLE.md` | Schwarzschild surface gravity c^2/2r at R* | - | free | VOID: postulate (J=1) | 47c437e8c |
| K576 | gemini-rh2 | `gemini_pi_puzzle/WHY_RH2_LAMBDA_8PI.md` | why r_H^2 Lambda = 8pi | - | free | bookkeeping | ab32041fc |
| K586 | R06 | `RETRACTIONS.md` | category / uniqueness search | - | free | form unique; xi free | 508a12052 |
| K733 | W4-18/B5 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Newton-Hooke (Bohlin-Arnold-Kasner) duality (a+3)(A+3) = 4; deep MOND is the self-dual point | - | nk | EXPONENT-ONLY: dual coupling k = 4h/s^2 carries a free time-reparametrisation scale | 918a2439d |
| K735 | W4-18/B7 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | lattice of touching horizons (brief X5 light part): single-neighbour pull a_nn^2 = G rho c^2 (V_s/d^3)(G m/(d c^2)), d = 2 r_s | {0.5, 0.4387, 0.4204} | menu | MENU: sc gives exactly 1/2 (pi-free) but densest packing fcc/hcp 0.420 and bcc 0.439, all in W_data; dust lattice (w = 0) not the vacuum; MU3 shows 1/2 is definitional | 918a2439d |
| K736 | W4-18/B8 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Lambda thresholds x MOND (brief X4 static part): zero-force radius and OSCO for Newton, deep MOND, simple, standard, RAR | - | nk | NO-GO: Newton 2 and 8 rho_Lambda exact; threshold accelerations scale as M^(1/4) or M^(1/3), none M-independent; no c, so none can fix kappa | 918a2439d |
| K744 | W4-20/V1 | `why_4_puzzle/W4_20_can_the_lattice_be_the_vacuum` | von Laue theorem applied to W4-18's touching-horizon lattice: static self-bound elements (vacuum ball + Laplace-balanced shell) | - | nk | CLOSURE: compressive shell, trace 0, positive active mass; any static self-bound lattice has w_eff = 0 (dust), so the lattice 1/2 cannot be rho_DE | b2da37a28 |
| K745 | W4-20/V2 | `why_4_puzzle/W4_20_can_the_lattice_be_the_vacuum` | touching-horizon lattice with an assigned element w (active mass m(1+3w)) | - | free | CLOSURE: kappa^2(w) = (1+3w)/4, horizon needs w > -1/3; at w = -1 active mass -2m, no horizon, touching undefined | b2da37a28 |
| K746 | W4-20/V3 | `why_4_puzzle/W4_20_can_the_lattice_be_the_vacuum` | frozen p-brane networks (solid dark energy, w = -p/3) as the lattice elements | - | nk | CLOSURE: Nambu-Goto string active density 0 (deficit 8piG mu/c^2), wall active -sigma with pull 2piG sigma (pi); no w<0 element keeps a pi-free pull | b2da37a28 |

## GB: Graviton bath / mode counting

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K081 | B | `sonnet55_push/puzzle_32pi/agents/B_gravitational_waves/` | 32pi as graviton/Isaacson normalisation; graviton bath | {1.45} | menu | MISS: bath ~1.45; energy route needs the f=1/(32pi) slot | 20bdc3eb0 |
| K126 | KS01a | `fable_independent_2026/kappa_slot_2026/KS01_slot_adjudication.py` | thermal variance as integral vs box mode sum | - | free | SLOT-NOT-LIVE: S_dS x eps double-counts | 75b678b6a |
| K127 | KS01b | `fable_independent_2026/kappa_slot_2026/KS01_sds_adjudication.py` | <h_uu^2> two ways (thermal coincidence / explicit mode sum) | - | free | SLOT-NOT-LIVE: horizon entropy divides; live only under a named holographic-coherence postulate | 958f352c3 |
| K133 | KS07 | `fable_independent_2026/kappa_slot_2026/KS07_sds_coherence_attempt.py` | S_dS enhancement from secular growth / coherent multiplicity | 1.447 | any | MISS: needs ~3e120 e-folds; rc=1 | 03cf59135 |
| K204 | QC3 | `qwen_claude_field_theory/closure_2026/a0_promotion_2026/GRAVITON_BATH_CTP_VERDICT.md` | CTP rectified graviton-bath drift in the dS patch | - | free | CLOSURE: O(hbar) and shapeless | 3fa2b8af9 |
| K408 | RV-40 | `real_research/reviews/mi_eps_tot_mode_counting_verdict_2026.py` | graviton mode counting for eps_tot=1/(32pi) | {0.013, 0.036, 2.047} | menu | MENU: TT gauge kills h00; indeterminate (161x spread) | 775db892b |
| K413 | RV-45 | `real_research/reviews/mi_lorentz_mode_sum_2026.py` | so(1,3) generator mode sum | - | free | ROUTE DIES | e7250e861 |
| K429 | RV-62 | `real_research/reviews/mi_graviton_bath_ctp_2026.py` | graviton-bath CTP drift kappa^2 = 8pi eps_tot | {0.5, 1.447, 2.047} | menu | VOID as a hit: normalisation A hit 1/2 only via a TT-gauge error; other normalisations 1.447/2.047 | cf910f379 |
| K480 | NB-12 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T003 graviton-bath cancellation | - | free | 7/7 assumptions load-bearing | b062ad4a2 |
| K521 | PD07 | `deepseek_push/lean/PD07_kappa_half_certified.lean` | kappa = 1/(channel count) = 1/2 | - | free | VOID: basis-dependent count; do not cite | 928c61c79 |
| K552 | R13-BE | `RETRACTIONS.md` | Bose-Einstein kernel / mirror | 0.0733 | any | MISS: 11.1 sigma low | 508a12052 |
| K563 | kimik3 | `kimik3_push/KAPPA_VERDICT.md` | photocount: 2 transverse modes kappa=1/slope | - | free | VOID: occupation assumed | 2cfd3e2fd |
| K568 | H017 | `hy4_push/lean/H017_why_n_is_two.lean` | n = D(D-3)/2 polarisation count | - | free | WITHDRAWN (H061) | 8a641ea74 |
| K573 | gemini38 | `gemini38_flash_push/FIRST_PRINCIPLES_DERIVATION_CHAIN_REPORT.md` | 2 TT polarisations photocount a0=s/2 | - | free | VOID: retracted class (H061/K01) | a754ee4e3 |
| K575 | gemini-spin2 | `gemini_pi_puzzle/SPIN2_PROJECTION_DERIVATION.md` | spin-2 trace projector P=1/2 | - | free | VOID: double-counts trace reversal | e8dadc3bf |

## TA: Topological / index / anomaly

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K011 | p10 | `sonnet55_push/puzzle_32pi/p10_instanton_link.py` | S^4 spin connection = size-L BPST instanton | - | free | CLOSURE: scale-free | 20bdc3eb0 |
| K080 | A | `sonnet55_push/puzzle_32pi/agents/A_instanton_gauge_gravity/` | instantons / CS level / theta / MacDowell-Mansouri | - | free | CLOSURE: quantisation fixes Lambda never a0 | 20bdc3eb0 |
| K094 | Q | `sonnet55_push/puzzle_32pi/agents/Q_yang_mills_anomaly/` | YM anomaly / transmutation / same-S^4 instanton | - | free | VOID: 1/2 per chirality by construction of 1/g^2 (the puzzle needs 4) | 243a089c9 |
| K140 | LN10 | `fable_independent_2026/lean_2026/MAGNETIZED_TORUS_3.lean` | Z^2 as a whole number of flux quanta | - | free | CLOSURE: needs M=16/3 | a8c71bef0 |
| K148 | FL5 | `fable_independent_2026/L40_coefficient_rigidity.py` | S10 coset / nonlinear realisation | 1.414 | any | MISS: sqrt2 refuted at 21 sigma | 3cb26cf41 |
| K169 | OR8 | `opus_48_extended_research/reviews/FRONTIER2_CROSS_SECTOR_ANOMALY_VERDICT_2026-06-15.md` | conformal anomaly / Sakharov induced gravity cross-term | - | free | CLOSURE | 735f3518e |
| K174 | OR13 | `opus_48_extended_research/reviews/TOE_STAGE2_CALC_VERDICT_2026-06-15.md` | Blanchet-Seraille gauge cubic quantised by level/anomaly | - | free | CLOSURE: the cubic is not topological | 52b809d9e |
| K182 | OR21 | `opus_48_extended_research/reviews/KAPPA_MECH4_COSMIC_STRING_CONICAL_ETA_VERDICT_2026-06-26.md` | cosmic-string conical deficit through the horizon | - | free | VOID: -1/2 only at a hand-inserted G mu=3/16 (~1e6 x CMB bound) | 60c4885cb |
| K183 | OR22 | `opus_48_extended_research/reviews/KAPPA_TOPOLOGICAL_ETA_DOOR_VERDICT_2026-06-26.md` | eta invariant / CS level / fixed-point index on dS S3 | - | free | CLOSURE: forced halves in the wrong slot (theorem-grade: deficiency indices (0,0)) | 60c4885cb |
| K245 | sol61-36 | `sol61_push/FINAL_5_PERCENT_SPRINT.md` | quantized planar Dirac mode count | - | free | FREE: coupling continuous | d1e19d49e |
| K303 | sol61-94 | `sol61_push/puzzle_32pi_flux_sectors_2026_10_14` | Gauss-Bonnet sequestering with integer flux sectors | - | free | CLOSURE: 16pi and 32pi sectors both valid | untracked |
| K306 | sol61-97 | `sol61_push/puzzle_32pi_weyl_cancellation_2026_10_14` | E4-C^2 cancellation; equal a/c anomaly | - | free | selects t=1 not beta | untracked |
| K307 | sol61-98 | `sol61_push/puzzle_32pi_wz_kinetic_2026_10_14` | Wess-Zumino anomaly completion | - | free | CLOSURE: negative kinetic term | untracked |
| K329 | RR-06 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | F2 flux quantisation integer n | - | free | CLOSURE: n cancels from Z | b35a41b7f |
| K330 | RR-08 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | APS eta/2 universal prefactor | - | free | VOID: geometry-blind 1/2 present in every APS formula | b35a41b7f |
| K331 | RR-09 | `real_research/KAPPA_FIVE_HAIL_MARY_VERDICT_2026-06.md` | Hopf base flux + parity anomaly | - | free | VOID: 1/2s inserted; mod-Z | b35a41b7f |
| K332 | RR-10 | `real_research/KAPPA_FIVE_HAIL_MARY_VERDICT_2026-06.md` | Witten SU(2) anomaly theta=pi | - | free | CLOSURE: 12 doublets even | b35a41b7f |
| K333 | RR-11 | `real_research/KAPPA_FIVE_HAIL_MARY_VERDICT_2026-06.md` | Chern-Simons framing anomaly c/24 | - | free | VOID: 1/2 needs inserted c=12 | b35a41b7f |
| K334 | RR-12 | `real_research/KAPPA_FIVE_HAIL_MARY_VERDICT_2026-06.md` | lens/Seifert eta | - | free | VOID: -1/2 only at q=4 (inserted) | b35a41b7f |
| K336 | RR-15 | `real_research/TOPOLOGICAL_KAPPA_ETA_VERDICT_2026-06.md` | CS winding level pi3(SO(4,1)) | - | free | CLOSURE: integer | 60c4885cb |
| K430 | RV-63 | `real_research/reviews/mi_index_multiplicity_half_2026.py` | integer index/multiplicity source for 1/2 | - | free | no derivation | 3041c518b |
| K542 | AS669 | `deepseek_push/astra_spawn_ideas/results/AS669` | topological flux integral vs volume | - | free | blind | 125014663 |
| K544 | AS651.C02 | `deepseek_push/astra_spawn_ideas/results/AS651.C02` | boundary-ensemble origin of q0 | - | free | NO-GO | e6d9add5c |
| K589 | R09 | `RETRACTIONS.md` | E8 / J3(O) embedding | - | free | hosts not forces | 508a12052 |

## QG: Quantum-gravity programmes (asymptotic safety, DSSYK, RG improvement)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K098 | U | `sonnet55_push/puzzle_32pi/agents/U_rg_improved_gravity/` | RG-improved gravity / asymptotic safety | - | free | TRADE: scheme-dependent cutoff constant inserted | 243a089c9 |
| K175 | OR14 | `opus_48_extended_research/reviews/TOE_STAGE3_KANATCHIKOV_LAMBDA_VERDICT_2026-06-15.md` | Kanatchikov precanonical QG ordering constant | 4.09 | any | MISS: Z_eff=0.707; a free UV scale absorbs the value | 9fc2a68e0 |
| K180 | OR19 | `opus_48_extended_research/reviews/KAPPA_CLASS3_DISPERSION_RELATION_VERDICT_2026-06-26.md` | deformed dispersion relations (rainbow / DSR / kappa-Poincare) | 5.79 | odd | MISS: temperature root 2cH_Lambda | 442a51c56 |
| K184 | OR23 | `opus_48_extended_research/reviews/toe_law/agentD4_coefficient_dssyk.md` | type II_1 / DSSYK structure | 2.894 | odd | MISS: Z data-selected | f1535b7d8 |
| K216 | sol61-07 | `sol61_push/TONIGHT_32PI_RESULTS.md` | Kanatchikov-Kholodnyi precanonical fluctuations | 4.1 | any | MISS: C=3/2 at lambda=3; RMS is not a mean force | 8c3efb551 |
| K217 | sol61-08 | `sol61_push/TONIGHT_32PI_RESULTS.md` | mean-magnitude modified-inertia response | - | free | CLOSURE: shape unselected | 8c3efb551 |
| K223 | sol61-14 | `sol61_push/SHARED_SCALE_RESULTS.md` | Gross-Neveu-Yukawa IR-attractive coupling ratio | - | free | BOUND kappa>2.9 in a model with no gravity/MOND map | 8fbd56a2c |
| K257 | sol61-48 | `sol61_push/puzzle_32pi/critical_sextic_selector_2026_10_06` | BMB large-N critical sextic | - | free | CLOSURE: wrong cubic sign | 4882e2ec6 |
| K283 | sol61-74 | `sol61_push/week_review_2026_10_08/threshold_continuum/REPORT.md` | supermembrane/matrix continuum source | - | free | CLOSURE | a51caafca |
| K297 | sol61-88 | `sol61_push/puzzle_32pi_critical_2026_10_14` | large-N O(N) critical amplitude ratio | 12 | any | MISS: factor 192pi off | untracked |
| K298 | sol61-89 | `sol61_push/puzzle_32pi_dilaton_2026_10_14` | dilaton / Coleman-Weinberg scale breaking | - | free | CLOSURE: needs non-unitary Delta | untracked |
| K341 | RR-22 | `real_research/ASYMPTOTIC_SAFETY_KAPPA_EXPONENT_VERDICT_2026-06.md` | kappa as a Reuter NGFP critical exponent | - | free | CLOSURE: type mismatch; scheme-dependent | 7e3e57053 |
| K342 | RR-23 | `real_research/ASYMPTOTIC_SAFETY_KAPPA_EXPONENT_VERDICT_2026-06.md` | kappa as an IR dS RG-attractor value | - | free | CLOSURE: MOND operator irrelevant | 7e3e57053 |
| K358 | RR-40 | `real_research/FORCING_ROUTES_REWORKED.md` | dimensional transmutation | - | free | CLOSURE: no running a0 coupling | a8ae416c6 |
| K417 | RV-49 | `real_research/reviews/project_dssyk_force_Z_verdict.py` | DSSYK DOS freezing | 3e-61 | any | COMPUTED TO FAIL (Z~1e61) | 2f8f8ef4e |
| K418 | RV-50 | `real_research/reviews/project_which_horizon_dssyk.py` | DSSYK static patch selects the event horizon | - | free | density choice only | ece947970 |
| K588 | R08 | `RETRACTIONS.md` | rapidity-gap modified inertia | - | free | lensing excludes at 21 sigma | 508a12052 |
| K592 | S01 | `STANDING.md` | Oppenheim-Russo postquantum gravity | {1.30, 1.45} | menu | MISS | a7a1e0e05 |
| K600 | CFG905 | `campaign_fresh_gravity/CFG905_kappa_D5_festina_lente` | gauged carrier U(1) + Festina Lente (recalled m^2 >~ sqrt6 g q M_P H; V form m^4 >= 2 s^2 e^2 V) with the carrier setting a0 (posited S_bridge) | - | free | CLOSURE: FL is a bound on V, G-free; applied: BOUND on the carrier, kappa-free; saturated: unique hbar-free e-free carrier acceleration = law unit so kappa = sqrt2 s N, N free (TRADE; pi-even only via premise A); FL acceleration hbar-bearing; Nariai X3 7.09/5.01; gauged q_b repels; natural menu sqrt2/pi = 0.450 not 1/2 | 89df85f82 |
| K609 | W4-01/F7 | `why_4_puzzle/W4_01_untouched_gravity_families` | Horava-Lifshitz gravity (projectable / non-projectable; detailed balance) | - | free | TRADE: Lambda free; detailed balance gives Lambda < 0 and needs a free soft-breaking term; no a0 scale | cafc0bf78 |
| K632 | W4-04/R2 | `why_4_puzzle/W4_04_microscopic_normalization` | common finite scalar/Dirac determinant inducing vacuum and Einstein coefficients with exact spectral cancellation | - | free | CLOSURE OF TEST MODEL: positive finite coefficients without regulator moments, but no positive MOND cubic; analytic gapped response, negative scalar spurion slope; constructed spectrum gives 3<H^2/M^2<4 outside low-curvature vacuum regime; finite curvature-coupling freedom remains | a811e18fb |
| K639 | W4-07/B3 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | weak-gravity conjecture saturated (m = sqrt2 g q M_P) + seesaw a0 = m^2/M_P | - | free | HBAR/TRADE: kappa^2 ~ hbar^-1, g and q free | 2e238ed36 |
| K640 | W4-07/B4 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | dS swampland conjecture /V'//V >= c/M_P | - | free | BOUND: an inequality on the quintessence slope; no a0 | 2e238ed36 |
| K641 | W4-07/B5 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | trans-Planckian censorship conjecture | - | free | BOUND: inequalities on Lambda and inflation; no a0 | 2e238ed36 |
| K642 | W4-07/B6 | `why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios` | species scale M_P/sqrt(N) + seesaw | - | free | HBAR/TRADE: kappa^2 ~ hbar^-1, N free | 2e238ed36 |
| K650 | W4-09/E6 | `why_4_puzzle/W4_09_dark_energy_models` | loop quantum cosmology bounce density sqrt3/(32pi^2 gamma^3) rho_Pl | - | free | HBAR: Planck-scale density, 3.5e122 x dark-energy scale | 01db38324 |
| K651 | W4-09/E7 | `why_4_puzzle/W4_09_dark_energy_models` | causal-set everpresent Lambda ~ alpha_s/sqrt(V4), a = cH | - | free | TRADE: hbar cancels, kappa^2 = 8pi/alpha_s with alpha_s a random O(1) amplitude | 01db38324 |
| K664 | W4-11/Q4 | `why_4_puzzle/W4_11_last_gravity_classes` | Weyl conformal geometry (Ghilencea) broken to Einstein-Proca | - | free | HBAR/TRADE: kappa^2 = 8pi c^3 q^2/(G hbar xi^2) | 1cbcd12ee |
| K754 | A0SEL-20261024/RG | `reviews/a0_selection_2026_10_24` | minimal matter-loop RG of positive curvature tracker | - | free | TRADE: invariant (xi+1/6)/lambda^(1/3) retains initial condition; no interacting fixed point in truncation; formal conformal limit outside positive tracker; massive decoupling not calculated | freeze:87e0c60793 |

## KS: Kinetic / settling / collective / cold-energy dynamics

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K104 | X2 | `sonnet55_push/puzzle_32pi/agents/X2_collective_analogies/` | Jeans / plasma / Debye scales of the vacuum | {0.46, 0.564} | menu | MENU: vacuum Jeans frequency is 0; near entries generic (53% of rescaled menus) | 1138d817f |
| K111 | N2 | `sonnet55_push/puzzle_32pi/agents/N2_nonlinear_eigenvalue/` | MOND-field existence thresholds in the dS patch | - | free | CLOSURE: a regular solution always exists (Galileon folds only) | e6d9add5c |
| K112 | N3 | `sonnet55_push/puzzle_32pi/agents/N3_mond_cosmology_fixed_points/` | MOND expansion fixed points with Lambda | - | free | CLOSURE: one saddle; needs an inserted f=1.705 | e6d9add5c |
| K115 | B4 | `sonnet55_push/puzzle_32pi/agents/B4_mond_sector_object/` | phantom radius / zero-force / hydrostatic cap / kink | - | free | CLOSURE: 0/39 roots; each object leaves a free scale | e6d9add5c |
| K210 | sol61-01 | `sol61_push/RESULTS_2026-09-29.md` | stream-driven coherent dipole response as the a0 carrier | - | free | CLOSURE: state selection missing | 8a295b11e |
| K214 | sol61-05 | `sol61_push/PUZZLE_32PI_RESULTS.md` | Route 4: orientation of stream-induced dipole response | - | free | CLOSURE: cross term cancels under stream reversal | 739a063b4 |
| K215 | sol61-06 | `sol61_push/SELECTION_RESULTS_2026-09-29.md` | streaming-instability pump + virial density dictionary | - | free | CONDITION: density alone cannot fix an acceleration | 0bc2cd294 |
| K268 | sol61-59 | `sol61_push/puzzle_32pi/flowing_clock_2026_10_06` | flowing-clock log-KGB + P2 exterior | - | free | FREE: A/H arbitrary | 80e794cd7 |
| K285 | sol61-76 | `sol61_push/microscopic_carrier_2026_10_10/REPORT.md` | Bonnor pressure-confined isothermal edge P_s=beta rho_DE c^2 | - | free | FREE: 1/2 needs Mc/Mb=0.0997; violates its own approximation | 4504e0516 |
| K286 | sol61-77 | `sol61_push/cold_stream_selection_2026_10_10/REPORT.md` | orbit traffic / residence time | - | free | CONDITION (translation) | 69f5997a3 |
| K287 | sol61-78 | `sol61_push/orbit_selection_2026_10_11/REPORT.md` | exponential torque construction | - | free | CONDITION: no vacuum coupling | 85ae78f2b |
| K291 | sol61-82 | `sol61_push/cold_production_2026_10_11/COLLISION_AGE_SELECTOR.md` | one collision per cosmic age | - | free | CLOSURE: scales as sqrt(V) | e2440ea30 |
| K311 | sol61-102 | `sol61_push/puzzle_32pi_density_micro_2026_10_14` | three-body condensate derivation of P(X) | - | free | CLOSURE | untracked |
| K312 | sol61-103 | `sol61_push/puzzle_32pi_coupled_medium_2026_10_14` | dynamical elastic medium | - | free | FREE | untracked |
| K315 | sol61-106 | `sol61_push/puzzle_32pi_tracking_force_2026_10_15` | tracking scalar as the MOND force (5 dirs) | - | free | CLOSURE | untracked |
| K316 | sol61-107 | `sol61_push/puzzle_32pi_broken_potential_2026_10_15` | negative h / reconstructed potential (3 dirs) | - | free | FREE; radial instability | untracked |
| K326 | RR-03 | `real_research/KAPPA_ALL_DOORS_VERDICT_2026-06.md` | F1(c) kinetic 1/2 mv^2 virial coefficient | - | free | CLOSURE: energy coefficient, wrong sector | b35a41b7f |
| K401 | RV-33 | `real_research/reviews/mi_N_count_and_kappa_iff_2026.py` | memory first-moment iff theorem | - | free | CONDITION: kappa=1/2 iff M1=(4/3)t_L (unproven) | 16d1ccfc6 |
| K402 | RV-34 | `real_research/reviews/mi_kappa_from_dimension_2026.py` | M1/t_L = (rho+p)/rho of a massless bath | - | free | VOID: 1/2 at D=4 from an unproven premise; superseded by RV-35 | 7474d9258 |
| K436 | RV-69 | `real_research/reviews/mi_local_source_for_K_2026.py` | local matter-side source for M1 | - | free | excluded by data | f5f935e95 |
| K437 | RV-70 | `real_research/reviews/mi_roundtrip_factor2_2026.py` | round-trip midpoint factor 2 | - | free | VOID: 1/2 only if the memory is normalised; EXCLUDED | dd6ee9934 |
| K506 | CFG666 | `campaign_fresh_gravity/CFG666_dark_energy_clock` | settled fraction clock a0=f^2 cH_L | - | free | arithmetic match; shape disfavoured | 0769d53dd |
| K515 | CFG893 | `campaign_fresh_gravity/CFG893_kappa_from_cold_energy_structure` | do the new cold-energy relations R1-R14 select kappa | - | free | NOT SELECTED: c-free sector invariant under S_lambda (a0 ~ G rho^(2/3) M^(1/3) or every a0); c enters only via sink (<=6e-6 of rho_DE c^2), causality (inequality), tau_psi (rejected) | 131bedf33 |
| K519 | GF1 | `deepseek_push/GF1_germ_flip` | 32pi^2 reduced to one integer kappa=1/n | - | free | VOID: n=2.000+-0.017 uses A0 = the kappa=1/2 footing (circular; p62) | f99dadac6 |
| K520 | GF2 | `deepseek_push/GF2_closure_half` | log branch + Poisson + hydrostatics sigma^2/v^2=1/2 | - | free | VOID (naming): the SIS ratio, not the law's kappa (AUDIT_GF2) | 5b173a046 |
| K548 | Q010 | `qwen38_push/Q010_kappa_referee` | referee of GF2 + GF1 web + junction | - | free | VOID as derivation (SIS class); says 'DERIVED (dynamical face)' and never engages AUDIT_GF2: UNRESOLVED CONFLICT | 0eb0b4d07 |
| K549 | Q001 | `qwen38_push/Q001_sound_speed_identity.py` | constitutive c_s^2 = 1/2 | - | free | VOID (naming): SIS-class ratio | ec8a02c12 |
| K550 | Q007 | `qwen38_push/Q007_virial_half.py` | virial amplitude half | - | free | VOID (naming): SIS-class ratio | 9e7e9604d |
| K577 | G001 | `glm53_push/G001_clockmaker_dilemma.py` | clock-derived kappa | - | free | closed | be5a58d00 |
| K583 | deepseek_moa | `deepseek_moa/HARVEST.md` | kappa = sigma^2/v^2 = c_s^2 = 1/2 | - | free | VOID (naming): SIS class | d78d7525a |
| K596 | CFG898 | `campaign_fresh_gravity/CFG898_kappa_D2_causality_saturation` | saturate CFG893 drift-causality ceiling (v_s = c) at rho_DE-defined loci x kernels x alpha* (causal bound / FP / BGK) | - | menu | NOT A SELECTION: menu 2.894-10.948 all miss; real field at loci gives kappa_sat 3.3e11-1.2e17 ~ M_b^-1 (mass-dependent, excluded); H-type a0 = N c H_L/(alpha c_nu) (horizon family, pi-parity forbids 1/2); alpha not fixed by IS closure | d663eb027 |
| K615 | W4-03/AS119 | `why_4_puzzle/W4_03_unrun_as_proposals` | max-ent {1, E[ln(1+u)] = c} -> Lomax (l-1)(1+u)^-l, n = 1/c; kappa = 1/n only if the kernel scale is s = c sqrt(G rho) (premise A) | - | free | REPARAMETRISATION (S5): exact max-ent, but its 1/2 is the committed MU2 kernel's n = 2 read back through premise A; from data c = 0.417+-0.095 -> n = 2.40+-0.55 | 3c96c6ce3 |
| K729 | W4-18/B1 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Mathieu parametric resonance: first tongue delta = 1/4 (mode at half the pump; Floquet-confirmed); pump = the vacuum's only rate H_Lambda | 1.447 | odd | MISS: kappa = sqrt(2pi/3), pi-odd, out of W_data | 918a2439d |
| K730 | W4-18/B2 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Fisher-KPP pulled front v* = 2 sqrt(D r) as an a0 front | - | free | FREE: the vacuum has no transport coefficient D; secondary reading (front at c, r = H) gives 2cH, kappa = Z = 5.789 pi-odd | 918a2439d |
| K732 | W4-18/B4 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Thomson/Eddington pi cancellation (sigma_T 8pi/3 vs flux 4pi): a0 as a gravity vs vacuum-momentum-transfer balance | - | nk | VOID: transfer ~ rho(1+w) = 0 at w = -1 (Lorentz-invariant vacuum) | 918a2439d |
| K734 | W4-18/B6 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | mean-field amplitude ratio 2, GL self-dual 1/sqrt2, critical damping gamma = 2 omega0 | - | nk | NO SLOT: no order parameter shared by a0 and rho_Lambda; damping reading = B3 edge | 918a2439d |
| K737 | W4-18/B9 | `why_4_puzzle/W4_18_borrowed_exact_numbers` | Maxwellian sqrt(pi) parity flip (effusion 1/4 n v_bar) | - | nk | VOID: the w = -1 source has no velocity distribution | 918a2439d |
| K741 | W4-19/L4 | `why_4_puzzle/W4_19_literature_addendum` | Luo 2026 (2602.14515): a0 = 2 beta^2 sqrt(Lambda/12) c^2 with virial beta^2 ~ 1/3 | 0.965 | odd | MISS: kappa = sqrt(8pi/27), pi-odd, out of window | 726716bac |

## CC: Cosmological consistency (horizons, epochs, H0, unimodular, sequestering)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K012 | p11 | `sonnet55_push/puzzle_32pi/p11_machian_cutoff_candidates.py` | horizon cutoffs a0=c^2/R_c (~6 candidates) | {0.55} | menu | MENU: particle-horizon diameter 0.96x SPARC; an 8% match among ~6 candidates happens ~55% of the time | 1138d817f |
| K015 | p13b | `sonnet55_push/puzzle_32pi/p13b_desi_dr2_a0z.py` | a0(z) ~ sqrt(rho_DE) under DESI DR2 table | - | nk | kappa-blind a0(z) test | 37b55b149 |
| K016 | p13c | `sonnet55_push/puzzle_32pi/p13c_desi_dr2_chains_a0z.py` | same with DESI DR2 chains | - | nk | kappa-blind a0(z) test | 5c037358f |
| K017 | p14 | `sonnet55_push/puzzle_32pi/p14_real_horizons.py` | real LCDM horizons vs A*Lambda=32pi^2 (particle horizon) | 0.55 | cont | MISS on its own terms: epoch coincidence; implied a0(2.5)/a0(0)=6 (opposite of FLAT); p15 worse than FLAT; uses measured cosmology | c40dfe1b6 |
| K018 | p15 | `sonnet55_push/puzzle_32pi/p15_particle_horizon_vs_a0z.py` | particle-horizon law vs the a0(z) record | - | nk | test of p14 | fd19e3afe |
| K065 | p59 | `sonnet55_push/puzzle_32pi/p59_a0z_drift_desi.py` | a0(z) drift under DESI w0-wa | - | nk | kappa-blind | d5409f201 |
| K107 | Z1 | `sonnet55_push/puzzle_32pi/agents/Z1_causal_horizon_a0z/` | cutoff laws as a0(z) laws | - | nk | discriminating a0(z) test; inconclusive | 1138d817f |
| K108 | Z6 | `sonnet55_push/puzzle_32pi/agents/Z6_memory_kernel_referee/` | is the record's memory kernel Sciama's? (2R* cutoff) | {0.375, 0.5, 0.75, 1.5} | menu | VOID as a hit: 1/2 for one kernel shape only; TRUE ONLY FOR THE MOMENT | 1138d817f |
| K135 | KS-L265 | `fable_independent_2026/kappa_slot_2026/L265_emergent_a0_lcdm.py` | emergent V^4/(G M_b) from published LCDM relations | {0.737, 0.612} | audit | SCORECARD on LCDM inputs (not framework-native) | 4bd09a54b |
| K156 | FL13 | `fable_independent_2026/L37_RECOMBINATION.md` | which density (rho_Lambda vs rho_tot) at recombination/BBN | - | free | footing survives; kappa not fixed | f64b01921 |
| K176 | OR15 | `opus_48_extended_research/reviews/KAPPA_SCALE_VS_FRACTION_VERDICT_2026-06-17.md` | 7 matching conditions on the dS-Unruh spectrum | {2.894, 5.79} | menu | MISS (its 'never the outside factor' later shown a parametrisation artefact, mi_kappa_linear_class) | 76d94a9ca |
| K220 | sol61-11 | `sol61_push/SHARED_SCALE_RESULTS.md` | induced-gravity scalar with stabilised vacuum | - | free | FREE RATIO: lambda cancels; 16pi/32pi/64pi all pass | 8fbd56a2c |
| K232 | sol61-23 | `sol61_push/CLOCK_COEFFICIENT_BOUND.md` | canonical preferred-clock order parameter (G_cosm vs G_N) | - | free | BOUND: 32pi branch excluded by BBN (kappa<0.145 in that construction) | c941c63d9 |
| K233 | sol61-24 | `sol61_push/VARIABLE_CLOCK_RESULTS.md` | scalar-dependent clock coupling | - | free | FREE | 64064c116 |
| K235 | sol61-26 | `sol61_push/GALAXY_SCALAR_MATCHING_RESULTS.md` | matched cosmological-background coefficient | - | free | FREE: D and ell free (illustrative 0.59/0.64) | b65b39182 |
| K237 | sol61-28 | `sol61_push/SELF_TUNING_GALAXY_BRIDGE_RESULTS.md` | well-tempered self-tuning scalar | - | free | CLOSURE | 73573446b |
| K238 | sol61-29 | `sol61_push/DERIVATIVE_BRIDGE_RESULTS.md` | rolling-scalar f(X) cubic coefficient | - | free | CLOSURE: coefficient drifts | e1354bea9 |
| K241 | sol61-32 | `sol61_push/EXPANSION_BRIDGE_MOND_RESULTS.md` | expansion-based scale bridge | - | free | CONDITION (restatement) | 5a027c670 |
| K242 | sol61-33 | `sol61_push/EXPANSION_BRIDGE_GAP_CHECKPOINT.md` | self-sourcing gapped cubic operator | - | free | CLOSURE: kills the MOND window | eb9936a4d |
| K269 | sol61-60 | `sol61_push/puzzle_32pi/flowing_clock_matching_2026_10_06` | exterior ODE toward cosmological flow | - | free | CLOSURE | 5a7ba806a |
| K271 | sol61-62 | `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding` | log-KGB vacuum-rescaling map | - | free | CLOSURE: not MOND scaling | 07fa64b44 |
| K272 | sol61-63 | `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/cuscuton` | cuscuton vacuum adjustment | - | free | CLOSURE | 07fa64b44 |
| K273 | sol61-64 | `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/generalized_aether` | smooth aether family | - | free | FREE: kinetic sign lost | 07fa64b44 |
| K276 | sol61-67 | `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/volume_form` | fixed-volume (unimodular) saddle | - | free | CONDITION V0 a0^4=3/128 unexplained | 81af81ba8 |
| K277 | sol61-68 | `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/retarded_curvature` | nonlocal box^-1 R memory | - | free | CLOSURE: prefactors renormalise together | 81af81ba8 |
| K280 | sol61-71 | `sol61_push/puzzle_32pi/selection_2026_10_06/timelike_spacelike` | one P(X) for galaxy cubic and vacuum condensate | - | free | CLOSURE: hyperbolicity lost | 310f0d1a4 |
| K364 | RR-46 | `real_research/coefficient_hubble_lock.py` | coefficient-H0 lock | - | audit | reframing: Z rides on the Hubble tension | 9bb08934b |
| K385 | RV-17 | `real_research/reviews/coefficient_vs_hubble_tension.py` | Z vs 1/6 fork against H0 tension | - | audit | swamped by H0 spread | 999f94dfe |
| K416 | RV-48 | `real_research/reviews/project_coefficient_event_horizon.py` | event vs apparent horizon density | - | free | relocates the density only | 7e2bbfb93 |
| K494 | CFG252 | `campaign_fresh_gravity/CFG252_timescape_between_the_bands` | timescape void-rate tie | - | free | NON-DIAGNOSTIC | cb6a4d243 |
| K551 | Q002 | `qwen38_push/Q002_omega_lambda_selector.py` | Omega_L from a0 picks the canonical footing | - | free | VOID: circular (canonical a0 built from Planck Omega_L) | 3e2ef826d |
| K566 | hunt-70 | `hunt_2026/WHAT_THE_HUNT_TAUGHT.md` | Lambda = 32pi a0^2/c^4 vs Planck | - | audit | consistency only | 0cc476387 |
| K581 | G052 | `glm53_push/STATE.md` | Omega_L from canonical a0 | - | free | VOID: circular (CFG835) | n/a |
| K594 | XR20 | `real_research/cross_thread_review_2026_09_26` | Henneaux-Teitelboim unimodular multiplier ties a0 to Lambda | - | free | TIED not derived: a0 constant, kappa still fitted | a075ad7f7 |
| K603 | W4-01/F1 | `why_4_puzzle/W4_01_untouched_gravity_families` | DGP brane-induced gravity: self-accelerating vacuum H=1/r_c with r_c=G5/(2G) (pi-free); a0 readings crossover c^2/r_c, 5D product G5 rho_DE (action G5), same with force-law G5N=4G5/(3pi); normal branch with a brane Lambda | {2.894, 0.691, 0.293} | menu | MENU: self-acc values all pi-odd (8pi/3, 3/(2pi), 8/(3pi^3)); rho_DE reaches a0 only via the brane Friedmann 8piG; 0.293 a spurious in-window landing; normal branch TRADE (r_c free) and a0 ~ rho breaks the LOCK | cafc0bf78 |
| K605 | W4-01/F3 | `why_4_puzzle/W4_01_untouched_gravity_families` | dRGT massive gravity / Hassan-Rosen bigravity self-accelerating branch (Lambda_eff = m^2 X); a0 = graviton Compton acceleration c^2 m | - | free | TRADE: kappa^2 = 8pi/X with X free in the potential parameters; pi-odd at any algebraic X, never 1/2 | cafc0bf78 |
| K606 | W4-01/F4 | `why_4_puzzle/W4_01_untouched_gravity_families` | mimetic gravity (constraint g^{mn} d_m phi d_n phi = 1; Lambda an integration constant or a free V scale) | - | free | TRADE: no intrinsic acceleration scale; Lambda is initial data | cafc0bf78 |
| K608 | W4-01/F6 | `why_4_puzzle/W4_01_untouched_gravity_families` | teleparallel f(T) = T + alpha(-T)^n: de Sitter vacuum (6H^2)^(1-n) = alpha(2n-1); a0 from the correction's scale /T_*/ = alpha^(1/(1-n)) | - | free | TRADE: kappa^2 = 16pi (2n-1)^(1/(n-1)) (alpha cancels), free in n; pi-odd at rational n, never 1/2 | cafc0bf78 |
| K620 | W4-03/AS698 | `why_4_puzzle/W4_03_unrun_as_proposals` | time vs scale-factor averaging prescriptions A_t, A_a | - | free | AMBIGUITY in the already-excluded global-average class: A_a/A_t = 1.164/1.284/1.321 at T = 10/100/1000 (a = t^2/3, L = H^2); only A_t is covariant | 3c96c6ce3 |
| K625 | W4-05/V2 | `why_4_puzzle/W4_05_self_determined_vacua` | f(R) = R - mu^4/R self-accelerating vacuum R = sqrt3 mu^2 (metric or Palatini); a = mu c^2 | 7.619 | odd | MISS: kappa^2 = 32pi/sqrt3 (pi x algebraic), kappa 7.619 | c506c58b3 |
| K626 | W4-05/V3 | `why_4_puzzle/W4_05_self_determined_vacua` | Brans-Dicke / scalar-tensor (G_eff = 1/phi; Lambda or V free) | - | free | TRADE: Lambda free, no intrinsic acceleration | c506c58b3 |
| K627 | W4-05/V4 | `why_4_puzzle/W4_05_self_determined_vacua` | Maggiore RR nonlocal gravity (m^2 R box^-2 R): rho_DE fixed by m through the expansion history | - | free | CONDITION: the m <-> rho_DE relation needs the measured matter history (forbidden upstream); rho_DE,RR(z) drifts at constant m, not tracking | c506c58b3 |
| K628 | W4-05/V5 | `why_4_puzzle/W4_05_self_determined_vacua` | Deser-Woodard nonlocal MOND (f(box^-1 R) built for MOND; a0 a parameter) | - | free | TRADE: a0 and Lambda both free | c506c58b3 |
| K629 | W4-05/V6 | `why_4_puzzle/W4_05_self_determined_vacua` | running vacuum (Shapiro-Sola) rho0 + 3 nu H^2/(8piG); a = cH | - | free | TRADE: rho0 and nu free; a = cH is H-type | c506c58b3 |
| K645 | W4-09/E1 | `why_4_puzzle/W4_09_dark_energy_models` | holographic dark energy (Li): rho = 3 c_H^2 M_P^2/L^2, a = c^2/L | - | free | TRADE: kappa^2 = 8pi/(3 c_H^2); saturated c_H = 1 gives 8pi/3 (H-type, = CKN) | 01db38324 |
| K646 | W4-09/E2 | `why_4_puzzle/W4_09_dark_energy_models` | agegraphic dark energy: rho = 3 n^2 M_P^2/T^2, a = c/T | - | free | TRADE: kappa^2 = 8pi/(3 n^2) | 01db38324 |
| K647 | W4-09/E3 | `why_4_puzzle/W4_09_dark_energy_models` | generalized Chaplygin gas p = -A/rho^alpha | - | free | TRADE: no intrinsic acceleration; A, alpha free | 01db38324 |
| K648 | W4-09/E4 | `why_4_puzzle/W4_09_dark_energy_models` | Cardassian expansion H^2 = (8piG/3)(rho + B rho^n) | - | free | TRADE: B, n free | 01db38324 |
| K649 | W4-09/E5 | `why_4_puzzle/W4_09_dark_energy_models` | exponential-potential scaling attractor Omega_phi = 3(1+w_b)/lambda^2, a = cH | - | free | TRADE: kappa^2 = 8pi lambda^2/(9(1+w_b)) | 01db38324 |
| K652 | W4-09/E8 | `why_4_puzzle/W4_09_dark_energy_models` | Dirac large-number hypothesis (G ~ 1/t, a0 ~ cH) | - | free | CLOSURE: G(t) excluded (recalled); a0 ~ cH is H-type | 01db38324 |
| K653 | W4-09/E9 | `why_4_puzzle/W4_09_dark_energy_models` | interacting dark energy Q = xi H rho_DE | - | free | TRADE: xi free, no scale | 01db38324 |
| K661 | W4-11/Q1 | `why_4_puzzle/W4_11_last_gravity_classes` | f(Q) = Q + alpha Q^n symmetric teleparallel (background = f(T)) | - | free | TRADE: kappa^2 = 16pi(2n-1)^(1/(n-1)), as f(T) | 1cbcd12ee |
| K662 | W4-11/Q2 | `why_4_puzzle/W4_11_last_gravity_classes` | f(R,T) = R + 2 lambda T | - | free | TRADE: GR in vacuum, Lambda free | 1cbcd12ee |
| K739 | W4-19/L2 | `why_4_puzzle/W4_19_literature_addendum` | Maeder 2023 (2302.06206) scale-invariant vacuum: a0 = ((1-Om)^2/4) n c H0, n ~ 1 | - | free | FREE: kappa = n Omega_L^(3/2) sqrt(pi/6) = 0.410 today, Omega-dependent (a0 evolves), pi-odd | 726716bac |
| K761 | SELFSELECT-20261024/KGB | `reviews/self_tuning_selector_2026_10_24` | constant-X tadpole-free KGB with direct B(X) response bridge | - | free | SCOPED NONSELECTION: stable logarithmic vacuum removes prior time drift; at fixed residual H, d ln a0_bare/dV=-B_X/(B K_X); constant response across bare-V interval forces constant B on branch, leaving normalization free; full local screening not solved | freeze:f458ddcc26 |
| K763 | LOCALSCREEN-20261024/FORCE | `reviews/local_screening_2026_10_24` | logarithmic KGB exact radial equations and leading screened metric force | - | audit | SCOPED CLOSURE: sourced weak-potential branch interpolates Newton to enhanced inverse-square force; crossover acceleration scales as source mass^(1/3); no MOND a0; exact global solution and local perturbation health remain open | freeze:70cf999088 |

## NU: Numerology and grammar searches (flagged)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K002 | p02 | `sonnet55_push/puzzle_32pi/p02_matching_scan.py` | 34-pair Schwarzschild x dS invariant matching scan | {0.5, 1} | menu | VOID as evidence: menu written knowing the target; decoys hit 9-18% | 4e233d832 |
| K046 | p40N | `sonnet55_push/puzzle_32pi/p40_selfconsistency_and_nice_numbers.py` | 20 'nice' pure-number turn-offs | {0.57} | menu | NUMEROLOGY: 5/20 within 1 sigma | 26510e942 |
| K066 | p60 | `sonnet55_push/puzzle_32pi/p60_principle_grammar_search.py` | 852-form principle grammar with look-elsewhere base rate | - | audit | CONTROL: 1/2 in 8 forms (0.94%); 1 in 15; 1/4 in 10: 1/2 not special | fca611502 |
| K082 | C | `sonnet55_push/puzzle_32pi/agents/C_census_32pi/` | census of 41 instances of 32pi | - | audit | NOTHING NEW: unrelated origins | 20bdc3eb0 |
| K130 | KS04 | `fable_independent_2026/kappa_slot_2026/KS04_look_elsewhere.py` | <=4-op expressions over a 12-symbol alphabet (18.9M values) | - | audit | CONTROL: 10.8% of <=3-op numbers in the 2 sigma band; 1.6% at +-5% | 958f352c3 |
| K152 | FL9 | `fable_independent_2026/L228_the_numerology_floor.py` | closed forms near b=6.684 | - | audit | CONTROL: 705 forms within 7.6%; 9 within 0.1% | 1a6cdad2e |
| K164 | OR3 | `opus_48_extended_research/reviews/route3_structure_8pi_4.py` | 32pi = 8pi x BH quarter | 0.25 | any | NUMEROLOGY: the 4 is 1/kappa^2; >=6 equally exact factorisations | 735f3518e |
| K222 | sol61-13 | `sol61_push/SHARED_SCALE_RESULTS.md` | four scalar components as the factor four | - | free | CLOSURE: not vacuum stress; ghost | 8fbd56a2c |
| K288 | sol61-79 | `sol61_push/kinetic_selector_2026_10_11/RESULT.txt` | Ito-transformation factor 1/2 | - | free | VOID: coincidental 1/2; file says NOT a derivation | 090879ed9 |
| K337 | RR-16 | `real_research/TOPOLOGICAL_KAPPA_ETA_VERDICT_2026-06.md` | kappa=1/chi(S4) | - | free | VOID: coincidence of unrelated 2s | 60c4885cb |
| K367 | RR-49 | `real_research/coefficient_uniqueness_test.py` | is 32pi/3 unique | - | audit | not unique | 87f84a131 |
| K379 | RV-11 | `real_research/reviews/the_one_quarter_target.py` | a0^2 = (1/4) c^2 G rho read as the BH 1/4 | - | free | VOID: target restated (lead only) | f1535b7d8 |
| K382 | RV-14 | `real_research/reviews/Z_provenance_audit_2026.py` | inscribed cube / octant stories | - | audit | numerology | 9b2c680b0 |
| K389 | RV-21 | `real_research/reviews/entropy_counting_and_the_cube.py` | factor 8 cube/orbifold posit | - | free | numerology (RV-14) | 999f94dfe |
| K394 | RV-26 | `real_research/reviews/is_Z_special.py` | swap Z across 64 'derivations' | - | audit | ~0 bits | 999f94dfe |
| K426 | RV-58 | `real_research/reviews/toe_boundary_2026_07/Z_SM_bridge_pslq.py` | PSLQ search for Z in SM data | - | audit | no bridge | 8ce52d6e9 |
| K435 | RV-68 | `real_research/reviews/mi_geometric_lock_price_2026.py` | lock search priced against chance | - | audit | no excess over chance | ff4459e2d |
| K453 | RT-11 | `reviews/run_kappa_session_2026-07-29.sh` | kappa forced in the atomos germ search | - | audit | relabel | c71350274 |
| K464 | RT-22 | `reviews/z_numerology_density_2026.py` | density of closed forms near Z | - | audit | CONTROL: 596 within 1% | 8787a385f |
| K465 | RT-23 | `reviews/z_numerology_steelman_2026.py` | steelmanned grammars | - | audit | cH0/7 beats Z | 8787a385f |
| K479 | NB-11 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T002 is eps_tot=1/(32pi) special | - | audit | CONTROL: 3 hits vs 2.23 expected | b062ad4a2 |
| K482 | NB-14 | `nbody_2026/stage66_kappa_rational_evidence_2026.py` | simplicity prior over rationals | - | audit | a bet: needs +-3.7% | dc8ae9f01 |
| K510 | CFG831-ph | `campaign_fresh_gravity/PARAMRED_2026-10-16/B_SUPPLY` | post hoc Omega_m/Omega_L = kappa sqrt(8/(3pi)) | - | free | POST-HOC | 62adebea9 |
| K554 | mm-bridge | `qwen_38_experiment/mm_results/kappa_bridge_base_c4.jsonl` | symbolic enumeration around 0.5006 | - | audit | CONTROL: 3 hits vs 5.0 expected | e79409f1f |
| K555 | interp_0027 | `qwen_38_experiment/LEDGER.md` | 'one kappa does two jobs' (SM targets) | - | free | DISCARD | b062ad4a2 |
| K557 | q36-spectral | `qwen_36_experiment/RESEARCH_LOG.md` | spectral density integrating to exactly 0.5 | - | free | VOID: ad hoc construction | 4e59df13c |
| K564 | atomos | `project_atomos/kappa_rerun` | kappa as a forced germ in SM search | - | audit | relabel | e58515025 |
| K579 | G019 | `glm53_push/G019_Z_derivation.py` | 'Z theorem' Z = sqrt(8pi Omega_L/3) | - | audit | identity | fb16b7db3 |
| K590 | R10 | `RETRACTIONS.md` | SM bridge / number field | - | audit | obstruction | 508a12052 |
| K743 | W4-19/L6 | `why_4_puzzle/W4_19_literature_addendum` | Funkhouser 2006 (physics/0502049): large-number scaling a0 ~ c Lambda^(1/2), factor b free | - | free | FREE: order statement; a0 = c H_Lambda reading gives sqrt(8pi/3) 2.894 pi-odd | 726716bac |

## OB: Observational determinations of kappa (NOT derivations)

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K004 | p03b | `sonnet55_push/puzzle_32pi/p03_egb_and_data.py` | SPARC amplitude vs 2pi / 6 / sqrt(32pi/3) / 3sqrt3 | 0.575 | obs | OBS: three candidates within 1 sigma | 9172fe05b |
| K019 | p16 | `sonnet55_push/puzzle_32pi/p16_gas_star_split_cause.py` | cause of the SPARC gas/star a0 split | 0.47 | obs | OBS: Upsilon_disk 0.6 closes the split | 2533aef96 |
| K039 | p34 | `sonnet55_push/puzzle_32pi/p34_sparc_energy_verlinde.py` | SPARC test of p33's local term | - | audit | test of p33: FAILS inside galaxies | 86f7b0a75 |
| K041 | p36 | `sonnet55_push/puzzle_32pi/p36_sparc_turnoff_fit.py` | SPARC fit of y_t | - | nk | y_t allowed not detected | f9b4c17fa |
| K042 | p37 | `sonnet55_push/puzzle_32pi/p37_transition_shape.py` | SPARC transition shape vs Upsilon | 0.67 | obs | OBS: shape and Upsilon degenerate | f0ea21e5a |
| K043 | p38 | `sonnet55_push/puzzle_32pi/p38_high_accel_turnoff.py` | ATLAS3D/SLACS sensitivity to the turn-off | - | nk | undetectable | 5f34068b8 |
| K047 | p41 | `sonnet55_push/puzzle_32pi/p41_pin_mass_to_light.py` | Upsilon-insensitive a0 from gas points | 0.48 | obs | OBS: cannot decide footings | 5865f3a41 |
| K048 | p42 | `sonnet55_push/puzzle_32pi/p42_kernel_on_gas_points.py` | kernel preference on gas points | 0.48 | obs | OBS | 178322a28 |
| K049 | p43 | `sonnet55_push/puzzle_32pi/p43_wallaby_gas_points.py` | WALLABY DR2 gas points | 0.39 | obs | OBS: distance-limited | 8d1f4a747 |
| K050 | p44 | `sonnet55_push/puzzle_32pi/p44_samplesize_and_bayes.py` | sample size + Bayes factors | 0.48 | obs | OBS: 1/2 / 6 / 2pi tied; revised by p46 | bc398045c |
| K052 | p46 | `sonnet55_push/puzzle_32pi/p46_gas_points_trgb.py` | gas points split by distance method | {0.62, 0.37} | obs | OBS: TRGB vs Hubble-flow split (distance-conditional) | 35b89edfd |
| K053 | p47 | `sonnet55_push/puzzle_32pi/p47_little_things_a0.py` | LITTLE THINGS a0 | 0.42 | obs | OBS: overlap check FAILED | 0eee0c46e |
| K054 | p48 | `sonnet55_push/puzzle_32pi/p48_meta_analysis.py` | random-effects meta-analysis | 0.44 | obs | OBS superseded: never quote the p48 pool | ba115c5c6 |
| K056 | p50 | `sonnet55_push/puzzle_32pi/p50_cf4_distances.py` | Cosmicflows-4 distances | 0.63 | obs | OBS post-hoc cut | cfe618f36 |
| K062 | p56 | `sonnet55_push/puzzle_32pi/p56_etno_turnoff.py` | extreme TNOs vs the turn-off | - | nk | y_t~129 likely excluded | 18a3fdc36 |
| K063 | p57 | `sonnet55_push/puzzle_32pi/p57_etno_secular_nbody.py` | secular detached-disk test | - | nk | INCONCLUSIVE | 6988a2ecb |
| K064 | p58 | `sonnet55_push/puzzle_32pi/p58_cassini_kappa_bound.py` | Cassini Q2 bound on kappa for the QUMOND class | - | obs | OBS bound kappa<0.17 (2 sigma) for that class: the V family's own class is rejected | 3df87c31a |
| K099 | V | `sonnet55_push/puzzle_32pi/agents/V_evidence_for_the_coefficient/` | data evidence on Z | 0.59 | obs | OBS Z_L=4.9+-0.6; only kappa=1 excluded | 243a089c9 |
| K159 | OV1 | `opus_48_extended_research/kappa_sparc_verify/V01_kappa_sparc_verify.py` | 175 SPARC galaxies, a0 free | 0.459 | obs | OBS 0.459 canonical / 0.381 alt | 31bf8ba5c |
| K188 | OR27 | `opus_48_extended_research/reviews/A0_LAW_OF_NATURE_2026-06-20.md` | BTFR zero point + coupling sweep | - | obs | OBS: empirical case only | 7c0f279b4 |
| K196 | OP8 | `opus_48_extended_research/papers/WIDE_BINARY_KAPPA_ROUTE.md` | wide binaries + Galactic acceleration | - | obs | OBS route: 3.9% floor; N>=136k | 775db892b |
| K197 | OP9 | `opus_48_extended_research/papers/RNAAS_COEFFICIENT_NOTE_2026-08-03.md` | rotation curves vs 1/2 and 1/(2pi) | - | obs | OBS: cannot yet fix | 74809037a |
| K248 | sol61-39 | `sol61_push/puzzle_32pi/README.md` | floor-aware sample size; distance split | - | obs | OBS forecast | cfa06dbfa |
| K261 | sol61-52 | `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06` | external-field multipoles to pin C | - | audit | identifiability only; bumps change C | 17b132964 |
| K262 | sol61-53 | `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/continuum_external_field` | Mellin sum rule for C | - | audit | identification not selection | 36b995761 |
| K263 | sol61-54 | `sol61_push/puzzle_32pi/claude_p58_audit_2026_10_06` | Q2 scaling and kappa limits | - | audit | UNREVIEWED operator tests | 12e49a17d |
| K264 | sol61-55 | `sol61_push/puzzle_32pi/projected_external_field_2026_10_06` | projected-action EFE / Solar Q2 | - | audit | operator discrimination only | 67e981cf7 |
| K368 | RR-50 | `real_research/kappa_gas_dominated_2026.py` | pre-registered gas-dominated SPARC a0-line | 0.413 | obs | OBS TLS 0.413+-0.095 (WLS 0.374; TRGB 0.537) | 93d2efbeb |
| K383 | RV-15 | `real_research/reviews/a0_cH0_Z_check.py` | a0=cH0/Z vs 2pi and 6 | - | obs | indistinguishable | f1535b7d8 |
| K395 | RV-27 | `real_research/reviews/kappa_h0_convention_audit_2026.py` | H0 convention inside kappa | - | audit | verdicts unchanged | ed238836d |
| K404 | RV-36 | `real_research/reviews/mi_kappa_error_budget_unlock_2026.py` | distance-free g_bar-axis estimator budget | - | obs | forecast +-0.032 | d3a2ef750 |
| K405 | RV-37 | `real_research/reviews/mi_kappa_sensitivity_census_2026.py` | census of kappa-sensitive observables | - | obs | mass floor caps at ~1-1.6 sigma | 62f905dd9 |
| K406 | RV-38 | `real_research/reviews/mi_btfr_intercept_kappa_door_2026.py` | deep BTFR intercept | 0.465 | obs | OBS superseded by 0.450+-0.073 (R1) | 62f905dd9 |
| K407 | RV-39 | `real_research/reviews/mi_lambda_inversion_z_test_2026.py` | Lambda = 3Z^2 a0^2/c^4 inversion | - | audit | circular for Z | 62f905dd9 |
| K414 | RV-46 | `real_research/reviews/mi_wb_gext_kappa_route_2026.py` | wide binaries + measured g_ext | - | obs | weak probe | 092f6c97c |
| K473 | NB-05 | `nbody_2026/stage49_kappa_remeasured_both_kernels_2026.py` | RAR-scatter remeasurement | - | obs | WITHDRAWN: degenerate estimator | 6b64a4d90 |
| K483 | NB-15 | `nbody_2026/stage67_kappa_precision_path_2026.py` | BTFR + distance-free combination | 0.530 | obs | OBS superseded | 93744ddc4 |
| K499 | CFG357 | `campaign_fresh_gravity/CFG357_heat_filter_cassini_q2` | Cassini Q2 in the filtered chassis | - | audit | no kappa constraint | ff82edd58 |
| K502 | CFG493 | `campaign_fresh_gravity/CFG493_kappa_combined` | GLS of 3 M/L-insensitive gas routes | 0.417 | obs | OBS PRIMARY: 0.417+-0.095 (rho_L) / 0.345+-0.078 (crit) | 01e24734d |
| K503 | CFG301/309 | `campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain` | MIGHTEE-HI width chain | 0.70 | obs | OBS (corrected 0.70 / 0.58) | 6b10c01c0 |
| K504 | CFG397 | `campaign_fresh_gravity/CFG397_gas_only_a0_rung` | M/L-free a0 rung | 0.59 | obs | NOT ESTABLISHED | d164d5de9 |
| K505 | CFG449 | `campaign_fresh_gravity/CFG449_a0_rung_iorio_edd` | LVG TRGB + Iorio a0 rung | 0.46 | obs | NOT ESTABLISHED | 65d579590 |
| K511 | CFG833 | `campaign_fresh_gravity/PARAMRED_2026-10-16/D_KAPPA` | CFG493 reproduced; footings | - | audit | NO REDUCTION | 62adebea9 |
| K514 | ST29-milgrom | `campaign_fresh_gravity/STANDING_2026-09-29.md` | profile likelihood like-for-like H0 | - | audit | 1/2 vs 1/(2pi) indistinguishable | 6f584770d |
| K558 | MNRAS-R1 | `qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.out` | BTFR / shape / profile (H0-consistent R1) | 0.450 | obs | OBS 0.450+-0.073; 0.58+-0.18; 0.43+-0.08 | 56008a859 |
| K565 | hunt-64 | `hunt_2026/WHAT_THE_HUNT_TAUGHT.md` | hunt item 64 | 0.482 | obs | OBS 0.482+-0.081 | 0cc476387 |
| K593 | S03 | `STANDING.md` | SPARC by shape | - | obs | 1/2 leans 1.55 sigma shape-free; does not resolve | a7a1e0e05 |
| K636 | W4-06 | `why_4_puzzle/W4_06_lensing_kappa` | kappa fitted to KiDS-1000 isolated blue lenses (B21 RAR, full covariance; CFG829 window, nu_simple): first route free of rotation-curve systematics | 0.520 | obs | OBS: kappa_Lambda 0.520 +-0.091 stat +-0.235 (lens M* +-0.2 dex), kappa_crit 0.430 +-0.075 +-0.195; consistent with CFG493 (z +0.38 total) and 1/2; 1/2 vs 0.461 not separated; lens-mass limited (48%), not decisive | 10931109e |
| K660 | W4-10 | `why_4_puzzle/W4_10_one_kappa_lensing` | kappa per KiDS-1000 isolated-lens subsample (colour, Sersic, 4 mass bins, hot gas, GAMA) with W4-06's estimator: is there one kappa? | - | obs | OBS: blue 0.520 vs red 1.293, n<2 0.571 vs n>2 1.320 (NOT UNIVERSAL >4 sigma, follows type not mass); mass bins 0.95-1.16 UNIVERSAL; B21 hot gas does not close it; post-hoc early-type IMF (CFG926 R5) brings red to 0.731 (z +1.8) | 3afae65f5 |
| K670 | p64-B | `sonnet55_push/puzzle_32pi/p64_raw_sparc_minimal` | H0-free kappa from the 10 TRGB/Cepheid/SN gas-dominated SPARC galaxies (omega_L x 3(100 km/s/Mpc)^2/(8piG); simple mu; E1-E4) | 0.557 | obs | OBS: E2 0.557 (Planck omega_L) / 0.541 (BAO+BBN); E1-E4 span 0.54-0.61; 1/2 inside 1 sigma in 7 of 8 cells; tau 0.23 dex; RAR 0.559 | 9b8efc6f7 |
| K671 | p64-A | `sonnet55_push/puzzle_32pi/p64_raw_sparc_minimal` | within-galaxy gas-vs-star a0 contrast (11 SPARC galaxies, frozen Upsilon x f_gas grid) | - | obs | OBS UNDETERMINED as frozen: Delta_g -0.408 +- 0.085 (4.8 sigma) at Upsilon 0.5, -0.152 (1.9 sigma) at 0.8/0.85; kernel-robust (RAR -0.406); gas points want ~2.5x lower a0 than star points at SPS M/L; never a detection | 9b8efc6f7 |
| K672 | p64-C | `sonnet55_push/puzzle_32pi/p64_raw_sparc_minimal` | one HI flux scale for the TRGB dwarfs (ALFALFA alpha.100 cross-match) | - | obs | UNTESTED: no SPARC coordinates on disk, no downloads | 9b8efc6f7 |
| K711 | W4-12 | `why_4_puzzle/W4_12_one_correction` | consistency map: can one universal stellar-mass factor k and gas factor f reconcile F1 gas-RC kappa, F2 blue lenses, F3 within-galaxy gas/star gap, F4 red/blue split? | - | obs | OBS NO SINGLE CORRECTION: red/blue split never closes under a universal factor (type-dependent physics needed); gap + RC/lens agreement only off the plausible range (Upsilon_d 0.71 with gas x0.71, or Upsilon_d >= 1) | 1f384166d |
| K712 | W4-13 | `why_4_puzzle/W4_13_gap_vs_law_shape` | within-galaxy gas/star a0 gap (p64 A) under declared law forms L0.5, L1, L1.5, L2 and RAR | - | obs | OBS GAP NOT LAW-SHAPE: Delta_g -0.376..-0.408 dex under every law; a planted law-shape mismatch gives only -0.022 dex; the gap is about baryon type or position-dependent mass errors | cb7136f07 |
| K713 | W4-14 | `why_4_puzzle/W4_14_gas_star_matched_acceleration` | gas vs star points at matched g_bar pooled across SPARC: is the within-galaxy gas/star a0 gap about baryon type or acceleration? | - | obs | OBS ACCELERATION: matched Delta -0.096 +- 0.111 vs within-galaxy -0.441 +- 0.059; inferred a0 falls outward within galaxies (EFE/outskirts-like), not baryon type; frozen M2 control failed by design, post-hoc control passes | a4b55c5ca |
| K714 | W4-15 | `why_4_puzzle/W4_15_outward_decline_vs_external_field` | outward a0 decline within SPARC galaxies vs Chae+2021 environmental external field e_N | - | obs | OBS INTERMEDIATE, opposite sign to EFE: rho -0.25 (p 0.03); post-hoc power puts an EFE-strength rho +0.3 ~4.7 sigma above; frozen M1 control failed by design | 3964e4178 |
| K719 | W4-16 | `why_4_puzzle/W4_16_what_drives_the_decline` | what drives the outward a0 decline inside SPARC galaxies (pressure support, radial M/L, beam smearing, warps, quality, universal slope) | - | obs | OBS UNRESOLVED: no signature at p<0.01; full-point decline M/L-sensitive (gone near Upsilon_d 0.7); gas-only points do not decline; D1 sign mis-declared and frozen M1 control failed (disclosed) | f2342c536 |
| K720 | W4-17 | `why_4_puzzle/W4_17_single_normalization_test` | single stellar-M/L normalisation test for the within-galaxy a0 residual (Delta_g, slope, radial split vs Upsilon) | - | obs | OBS population (130): single normalisation at Upsilon* 0.48-0.59; p64's 11 mixed galaxies: NOT single (gap survives any Upsilon <= 1.4); corrects the population-wide outward-decline reading | 876f08642 |

## AU: Audits, controls, meta-analyses

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K005 | p04 | `sonnet55_push/puzzle_32pi/p04_equivalence_web.py` | ten repo formulations shown to be one statement | - | audit | AUDIT: restatement web; rows 5-8 premise-conditional | 9172fe05b |
| K068 | p62 | `sonnet55_push/puzzle_32pi/p62_gf1_data_pin_audit.py` | audit of GF1's n=2 'data pin' | - | pend | PENDING: written, unrun; claims GF1's pin is circular | untracked |
| K084 | E | `sonnet55_push/puzzle_32pi/agents/E_literature_a0_coefficient/` | ~35 published a0 coefficients audited | - | audit | every published route inserts its coefficient | 20bdc3eb0 |
| K085 | F | `sonnet55_push/puzzle_32pi/agents/F_dimension_test/` | dimension as discriminator | - | audit | normalisation guarantees the d=3 lock | 20bdc3eb0 |
| K088 | I | `sonnet55_push/puzzle_32pi/agents/I_adversarial_audit/` | audit of README 1-11 and p01-p10 | - | audit | withdrawals H1/H3; scope H2 | 20bdc3eb0 |
| K100 | W | `sonnet55_push/puzzle_32pi/agents/W_fresh_ideas/` | 18 fresh mechanisms screened (W01-W18) | - | audit | NOTHING NEW (<=2% chance each); W03 and W11 listed separately | 1138d817f |
| K125 | KS00 | `fable_independent_2026/kappa_slot_2026/WORK_ORDER.md` | work order: is eps_tot=1/(32pi) live (kappa^2=8pi eps_tot) | - | audit | plan; rung 1 FITTED | 767ea14b6 |
| K129 | KS03 | `fable_independent_2026/kappa_slot_2026/KS03_rival_coefficients.py` | 8 published a0-Lambda coefficients as (kappa eps_tot) | - | audit | 5 inside 2 sigma; needs +-1.2% on kappa; H0-degenerate | 958f352c3 |
| K145 | FL2 | `fable_independent_2026/L32_kappa_necessary.py` | necessary conditions T1-T6 for any kappa derivation | - | audit | S1-S6 excluded; S8-S10 open then; 27/71 principle numbers in 3 sigma | 2b2c09f0f |
| K155 | FL12 | `fable_independent_2026/L260_seesaw_identity_audit.py` | audit of H019/H020 seesaw a0 = Lambda^2/M_Pl | - | audit | TAUTOLOGY for every kappa (0/6) | 9e5b2cb8e |
| K158 | OA2 | `opus_48_extended_research/kappa_audit_2026/CAPSTONE_kappa_nogo.md` | dust has no slip: engaged-response rank 1 | - | audit | CLOSES OA1 (GW170817 / alpha1 / KiDS); DHOST sliver | 96d7489a3 |
| K160 | OC1 | `opus_48_extended_research/THE_A0_COEFFICIENT_CONVENTION.md` | coefficient vs cH0 or cH_Lambda | - | audit | convention fix | f1535b7d8 |
| K161 | OC2 | `opus_48_extended_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md` | 59-file quoting audit | - | audit | 32 files conflate the two rates | f1535b7d8 |
| K162 | OR1 | `opus_48_extended_research/reviews/DERIVE_Z_FRESH_RUN_VERDICT_2026-06-15.md` | synthesis of 5 Z routes | - | audit | UNFORCED POSIT | 889f30c2b |
| K166 | OR5 | `opus_48_extended_research/reviews/ROUTE5_NULL_STEELMAN_Z_UNFORCED_2026-06-15.md` | every a0-from-Lambda route listed | - | audit | pinned only to O(1) | 889f30c2b |
| K189 | OP1 | `opus_48_extended_research/papers/KAPPA_ONE_PARAMETER_GEOMETRY.md` | synthesis: kernel forced; kappa residual | - | audit | provably one-parameter | b9064374d |
| K190 | OP2 | `opus_48_extended_research/papers/THE_COEFFICIENT_PAPER_2026-08-02.md` | SPARC comparison + two non-derivability theorems | - | audit | coefficient measured | a48c88db0 |
| K192 | OP4 | `opus_48_extended_research/papers/WHAT_CAN_FIX_THE_MOND_COEFFICIENT_2026-08-04.md` | relabelling theorem + 3 constructions | - | audit | all 3 fail; factor-2 hazard flagged | c62a91212 |
| K198 | OP10 | `opus_48_extended_research/papers/A0_HALF_THE_DARK_ENERGY_RATE.md` | restatement as cH_Lambda/Z | - | audit | presentation; fitted | 634ff85dd |
| K199 | OD1 | `opus_49_doorD/REFEREE.md` | referee of I14 stability wall | - | audit | KILLED I14 | 60b013a07 |
| K207 | KC3 | `kappa_closure/k03_half_vs_two_pi_precision.py` | can data separate 1/2 from 0.461 | - | audit | UNDECIDED: needs a0 to 2.8% vs 9.47% floor; H0-degenerate | a7a1e0e05 |
| K226 | sol61-17 | `sol61_push/CORE_REVIEW_2026-09-30.md` | footing audit (vacuum vs H-based) | - | audit | identity only | ea962ad3a |
| K239 | sol61-30 | `sol61_push/HORIZON_8PI_AUDIT.md` | r^2 Lambda for Hubble/dS/density/acceleration radii | - | audit | 8pi only via the density length; 1/2 is the target restated | 3adc1a305 |
| K267 | sol61-58 | `sol61_push/main_theory/center_dimension_2026_10_06/SCALE_IDENTIFIABILITY_LEMMA.md` | scale identifiability lemma | - | audit | every A gives identical evidence | 5a7ba806a |
| K318 | sol61-109 | `sol61_push/coefficient_coverage_2026_10_15` | 20-family route register | - | audit | first pass; unfinished | untracked |
| K319 | sol61-110 | `sol61_push/open_items_2026_10_15/RESULT.txt` | re-check of the C counterfamily | - | audit | repeats sol61-86 | untracked |
| K323 | sol61-114 | `sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md` | status statements | - | audit | kappa TARGET/fitted | 33ec30852 |
| K350 | RR-32 | `real_research/COEFFICIENT_DEFINITIVE_VERDICT.md` | number-field no-go | - | audit | route-dependent | f1535b7d8 |
| K359 | RR-41 | `real_research/DEEP_REVIEW_ASSERTED_VS_COMPUTED_2026-06.md` | re-ran asserted steps of eta / AS closures | - | audit | theorem-grade; 0 doors reopened | d560af569 |
| K360 | RR-42 | `real_research/TOE_DOORS_REANALYSIS_2026-06-06.md` | 42 frameworks re-checked | - | audit | 0 revived | a4badb5e0 |
| K362 | RR-44 | `real_research/coefficient_attribution.py` | literature credit | - | audit | attribution | 0c7f3265c |
| K369 | RV-01 | `real_research/reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md` | cH0 vs cH_L footing sweep | - | audit | 5 files fixed | 3d8c0388f |
| K374 | RV-06 | `real_research/reviews/executioner_Z_convention_sweep_2026.py` | 5 convention forks | - | audit | NOT FORCED | bfc5b92ba |
| K381 | RV-13 | `real_research/reviews/Z_is_one_pure_number.py` | density vs horizon base is a unit conversion | - | audit | audit | f1535b7d8 |
| K400 | RV-32 | `real_research/reviews/mi_2Z_is_the_friedmann_root_2026.py` | withdraws '2Z unnatural' | - | audit | audit | 260d3e155 |
| K403 | RV-35 | `real_research/reviews/mi_kappa_D_dependence_rigidity_2026.py` | framework kappa_D rigidity | - | audit | removes RV-34's support | 0c58cfb08 |
| K422 | RV-54 | `real_research/reviews/strained_horizon_redteam.py` | red-team of the strained-horizon obstructions | - | audit | all survive | eb0c3301e |
| K432 | RV-65 | `real_research/reviews/mi_number_field_theorem_2026.py` | pi-weight parity of competing coefficients | - | audit | presentation-dependent | f9c5cac61 |
| K440 | RV-73 | `real_research/reviews/mi_nariai_forcing_2026.py` | Nariai a0 shell re-run (same mechanism as K110) | - | audit | UNDECIDED; ~73% degenerate with H0 | 472f06c35 |
| K441 | RV-74 | `real_research/reviews/mi_local_floor_target_2026.py` | what a local derivation must deliver | - | audit | target spec | 2f672bd36 |
| K446 | RT-04 | `reviews/mi_kappa_spectral_reduction_2026.py` | 'derive Z' = 'derive kappa' | - | audit | reduction | 434f6fb85 |
| K452 | RT-10 | `reviews/mi_atomos_germ_provenance_2026.py` | atomos germ provenance | - | audit | framing | 4f951d457 |
| K463 | RT-21 | `reviews/z_dsunruh_convention_band_2026.py` | dS-Unruh convention band | - | audit | Z vs 2pi 0.53 sigma | 8787a385f |
| K468 | RT-26 | `reviews/mi_mechanism_audit_2026-07-30.py` | mu_fw = Milgrom 1999 eq.9 | - | audit | audit | f98e8f5a2 |
| K469 | NB-01 | `nbody_2026/stage43_kappa_reduction_one_factor_2026.py` | kappa=1/2 iff 32pi eps_tot=1 | - | audit | eps_tot route circular | c751d5d1e |
| K472 | NB-04 | `nbody_2026/stage48_kb_candidate_killed_2026.py` | kill of stage46 | - | audit | three kills | 8da68daa6 |
| K481 | NB-13 | `nbody_2026/stage65_kappa_programme_harvest_2026.py` | T009 pi-free obstruction | - | audit | CONFIRMED-NARROW | b062ad4a2 |
| K484 | DE-01 | `real_research/dark_energy_inverse_2026_09_26/scales/REPORT.md` | scale inverses | - | audit | kappa free | 968fb696a |
| K485 | DE-02 | `real_research/dark_energy_inverse_2026_09_26/spectral_inverse/REPORT.md` | inverse lapse reconstruction | - | audit | reconstruction only | 968fb696a |
| K487 | CFG103 | `campaign_fresh_gravity/CFG103_fluid_tie_rederivation` | re-derivation of CFG43 | - | audit | reproduces | a00ed3de1 |
| K491 | CFG181 | `campaign_fresh_gravity/CFG181_column_budget_referee` | referee of CFG174 | - | audit | any kappa 0.35-0.72 passes | 305d2c2ae |
| K495 | CFG263 | `campaign_fresh_gravity/CFG263_32pi_nogo_audit` | hostile audit of 8 no-gos | - | audit | rule: only-a-and-H mechanisms cannot give 1/2 | 35058745f |
| K509 | CFG830 | `campaign_fresh_gravity/PARAMRED_2026-10-16/A_INVENTORY` | parameter inventory | - | audit | kappa one of 4 free constants | 62adebea9 |
| K512 | CFG835 | `campaign_fresh_gravity/LEDGER.md` | errata CFG830/833 | - | audit | footing ratio circular | 83bea14d3 |
| K513 | AUDIT_GF2 | `campaign_fresh_gravity/AUDIT_GF2_kappa_claim_2026-10-09.md` | audit of GF2 'kappa derived' | - | audit | NOT a derivation (SIS ratio) | a755b66ca |
| K523 | AS053 | `deepseek_push/astra_spawn_ideas/results/AS053` | audit of PD08 | - | audit | slope free | 511efeb1d |
| K524 | AS055 | `deepseek_push/astra_spawn_ideas/results/AS055` | audit of PD01 | - | audit | assumes the freedom | 511efeb1d |
| K536 | AS075 | `deepseek_push/astra_spawn_ideas/results/AS075` | missing-premise work order | - | audit | obligations named | 511efeb1d |
| K546 | AS-FIND | `deepseek_push/astra_spawn_ideas/FINDINGS_FOR_REVIEW.md` | synthesis | - | audit | kappa is a datum | f14dd4b27 |
| K560 | route3B | `qwen_claude_field_theory/closure_2026/route3B_entropic_independent_2026.py` | independent rebuild of the 6 | - | audit | soft spot priced | e18afc17f |
| K571 | H061 | `hy4_push/H061_RECIPE_AMENDMENT.md` | retraction of kappa=1/nPol | - | audit | retraction | 763086b23 |
| K572 | H001 | `hy4_push/H001_CROSS_TRACK_AUDIT.md` | cross-track audit glm/gemini | - | audit | measured integer; Lean sorry | eb4a58376 |
| K584 | INV4 | `predictions_2026/INVENTORY_4_lensing_clusters_environment_kappa.md` | kappa inventory (L4-29..35) | - | audit | inventory; 0.551 superseded | c005dd00f |
| K585 | R05 | `RETRACTIONS.md` | pi-counting | - | audit | no leverage | 508a12052 |
| K597 | CFG891 | `campaign_fresh_gravity/CFG891_kappa_D3_c_term_census` | census of every c-a0 relation in the record (67 relations, 36 files; pi tracked) | - | audit | PI-FREE BUT NOT 1/2: the five pi-free rational halves carry the target; only target-free pi-free value CFG380 S4 kappa 1.278 (irrational, posit, miss); all horizon-type values pi-odd; no record equation gives exact 1/2 | 9bc3dbec4 |
| K599 | CFG904 | `campaign_fresh_gravity/CFG904_rt17_vs_rt19_audit` | RT-17 vs RT-19 recomputed; correction: K459 (RT-17 0.4607) reclassified MENU {0.4607, 0.921, 0.230, 2.894} (scale unfixed; I1 Unruh-inconsistent) | - | audit | RT-19 withdrawal stands; 4pi = 2pi (RT-17 S4) x 2 (DeltaT slope); both kappa^2 pi-odd; determinate in-window count drops by one on rerun of kappa_campaign_lee.py | c7e5c0e53 |
| K601 | CFG908 | `campaign_fresh_gravity/CFG908_kappa_derived_claims_audit` | audit of the four unaudited kappa-derived claims (Q010, G031, glm53 README/G002, gemini38) in sympy with rename and mutation controls | - | audit | none derives the law kappa: Q010 DIFFERENT QUANTITY (SIS ratio); G031 IDENTITY; G002 MEASUREMENT RELABELLED; gemini38 PREMISE-A INSERTION; 200 lines in 142 tracked files still say derived | c16f82613 |
| K612 | W4-02/portal/R3 | `why_4_puzzle/W4_02_independent_portal_audit` | explicit source-connected constitutive counterfamily after the vacuum zero mode is fixed; extension of CFG911 | - | audit | NONSELECTION PROOF: W_xi(0;epsilon) and source variations vanish for every xi>0; convexity and identical dimensionless simple-mu algebraic law survive xi rescaling in every spatial dimension n>=2; stiffness omitted only in algebraic reduction | 04d9b80a9 |
| K613 | W4-02/portal/DBI | `why_4_puzzle/W4_02_independent_portal_audit` | primary-source audit of Cai-Wang arXiv:1511.00627v3 screening-radius identification and dark-energy stress | - | audit | TRADE: xi=2pi eta^4/(g^2 gamma); transition-radius equality and canonical matter coupling are free; action has negative time kinetic Hessian; no healthy coefficient selection | 04d9b80a9 |
| K614 | W4-02/portal/PI | `why_4_puzzle/W4_02_independent_portal_audit` | qualification of H-only pi obstruction and rational-function extension | - | audit | RESTRICTED THEOREM: q=R(pi), R rational function over algebraic numbers, forbids exact half; H-only does not imply that grammar, since horizon-area prescription gives xi=2/3; no numerical selection or global no-go | 04d9b80a9 |
| K616 | W4-03/AS562 | `why_4_puzzle/W4_03_unrun_as_proposals` | hidden-hbar audit: Pi_quant = hbar/(M_b v R) | - | audit | AUDIT: dimensionless, 1.7e-100 for a 1e10 Msun / 100 km/s / 10 kpc galaxy; the law is hbar-free; an l_P = 1 entropy count carries hbar^-1 when restored | 3c96c6ce3 |
| K623 | W4-03/K547 | `deepseek_push/astra_spawn_ideas/results/AS025` | correction to K547: which of its nine proposals were unrun | - | audit | CORRECTION of K547: AS025 was executed 2026-09-28 (run_20260928T000953; dimensional uniqueness, kappa-blind); the other eight are now run in W4-03 (K615-K622) | 3c96c6ce3 |
| K635 | W4-04/R4 | `why_4_puzzle/W4_04_microscopic_normalization` | operational amplitude normalization from one mediator source and actual high/low-gradient force coefficients | - | audit | CONDITIONAL REDUCTION: xi=8Omega C2^3/(9epsilon C3^2); in4D quarter requires epsilon C3^2/C2^3=128pi/9; common factors cancel; no selecting law supplied; tensor-plus-scalar measured-G dictionary must be rederived | a811e18fb |
| K659 | W4-08/R1dyn | `why_4_puzzle/W4_08_positive_mond_amplitudes` | continuum mass bubble and gradient-source adiabatic range audit | - | audit | SCOPE: continuum kernel has k^2 sqrt(omegaE^2+v^2 k_parallel^2); hard finite-band projection unspecified; homogeneous convexity does not prove source dynamics; 53 exact checks and independent raw proof review | 4131def0e |
| K669 | p62 | `sonnet55_push/puzzle_32pi/p62_gf1_data_pin_audit.py` | RESULT of pending K068: audit of GF1's n = 2 'data pin' | - | audit | IDENTITY: GF1's A0 = c sqrt(G rho_L)/2, so n = 2 by construction; measured n_L 2.40 +- 0.54 (CFG493), consistent not pinned. Supersedes the PENDING status of K068 | b3aae484f |
| K673 | W4-08/R1stress | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal` | quantitative paired-band directional null stress and finite positive completion | - | audit | SCOPE: rho/2 < rho+p_parallel < rho; positive finite sums plus vacuum offsets and nonnegative extra null stress cannot form a vacuum; negative compensating stress required; no general NEC no-go | f77a0cd8d |
| K677 | W4-08/R5BMB | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal` | conditional timelike charged extension of K257 critical sextic large-N functional | - | audit | SCOPE: conditional leading-N P=N mu^3/(6pi), twice naive tree pressure; BMB zero-density direction has zero relative vacuum energy and is not finite-N beta zero; no current or vacuum normalization selector | f77a0cd8d |
| K678 | W4-08/Lean | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal` | four kernel-checked partial stress amplitude scale and cone modules with negative controls | - | lean | PARTIAL: 25 printed critical theorem axiom lists standard; normal control passes and two false controls reduce to False and fail; actual-pi adapter memory-deferred; physical selection and original goal remain open | f77a0cd8d |
| K681 | W4-08/R8neutralWard | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/current_interactions` | neutral off-shell conserved local current as a source proportional to gradient squared | - | audit | SCOPE: compact time interpolation excludes exact positive bulk J0 proportional to gradient squared modulo a divergence with trivial boundary flux; charged clocks and nontrivial sectors remain outside the result | 73cb47a32 |
| K685 | W4-08/Lean-current | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/current_interactions` | two kernel-checked current-energy and compact-flux algebra modules | - | lean | PARTIAL: nine critical theorem prints use only standard axioms; true controls pass and two false controls fail only at False; PDE variational and quantum bridges explicit; original microscopic normalization goal open | 73cb47a32 |
| K688 | W4-08/R13Fdeform | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | regular derivative-dependent chiral coefficient at the same positive vacuum fold | - | audit | NONSELECTION test: permitted local coefficient deformation varies nominal Taylor ratio while vacuum and imposed fold condition stay fixed; local scalar signs do not establish full health | 814cbf3fe |
| K691 | W4-08/Auxcritical | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | full auxiliary Hessian regularity and higher-criticality cusp discriminators | - | audit | SCOPE: invertible C2 elimination excludes cubic cusp; singular higher-criticality example disproves universal nonzero linear overlap necessity; ordinary energy minima obey a separate vacuum-trial upper bound; no global auxiliary no-go | 814cbf3fe |
| K692 | W4-08/Lean-fold | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_auxiliaries` | one kernel-checked chiral-fold module with all-root timelike obstruction and genuine controls | - | lean | PARTIAL: six critical theorem prints use only standard axioms; true controls pass and two false controls fail only at False; component-mode and force/gravity/quantum bridges remain analytic; original goal open | 814cbf3fe |
| K694 | W4-08/R15tilt | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | retained homogeneous unit-clock tilt at zero scalar momentum | - | audit | CLOSURE for fixed-metric derivative-only physical tilt class: omega2=-H2ja/((a+j)M)<0; positive finite vacuum time kinetic and zero static stiffness imply this near zero when coefficients continuous; full gravity and different invariants excluded | 65be2b68f |
| K695 | W4-08/R15chi | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | decoupled imaginary-scalar characteristic of the clock-projected branch | - | audit | BOUND: exact branch point x4/9 and r2/3 has principal speed squared75/67; no linear chi mixing; not a UV front-velocity theorem | 65be2b68f |
| K698 | W4-08/R16branches | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | fixed-flux boundary Legendre term and original versus convexified top-form branches | - | audit | SCOPE: original action has multiple Hamiltonian sheets; nearby inner branch has negative scalar radial stiffness; Fenchel prescription convexifies and changes theory; no universal propagating top-form ghost claim | 65be2b68f |
| K699 | W4-08/ClockGram | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | physical post-constraint spatial Gram matrix with zero scalar stiffness and healthy gapless clock | - | audit | SCOPED CLOSURE: nonzero constant spatial mixing gives negative generalized eigenvalue; time mixing alone counterexample; massive-clock low-frequency k4 and principal regimes distinguished; no all-clock exclusion | 65be2b68f |
| K700 | W4-08/Lean-clock | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/clock_flux` | one kernel-checked clock-tilt and conditional static amplitude module | - | lean | PARTIAL: seven critical theorem prints standard; true controls pass and stable-tilt and quarter-ratio mutations fail only at False; physical mode source and gravity bridges explicit; full goal open | 65be2b68f |
| K701 | W4-08/R17gravity | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/gravity_constraints` | covariant c1-only rational-clock Bianchi background and nonzero-k mode | - | audit | CONDITIONAL: consistent local Bianchi stress and lapse; frozen finite-k band grows; persistence at weak gravity requires regular harmonic-constraint reduction and validity window; full finite-coupling matrix and microscopic cutoff unproved | 590d17d77 |
| K702 | W4-08/BMlambda1 | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/gravity_constraints` | pure BM lambda1 lapse-shift reduction on its actual de Sitter vacuum | - | audit | SCOPE: finite nonzero k and H>0 retain positive scalar kinetic and no quadratic restoring term after redshift boundary; not gauge removal or full health; distinct from earlier flat lambda>1 work | 590d17d77 |
| K703 | W4-08/BMdeform | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/gravity_constraints` | cubic deformation invisible to homogeneous gravitational vacuum and all quadratic constraints | - | audit | NONSELECTION: f_delta preserves vacuum quadratic coefficients and UV constant while C3 scales1+delta and R scales(1+delta)^2; no claim every deformation has full physical health | 590d17d77 |
| K705 | W4-08/R17PPN | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/gravity_constraints` | independent local unscreened UV two-potential diagnostic of the normalization counterfactual | - | audit | CONDITIONAL CLOSURE: inferred-density target requires f>1/4 and gammaUV<1/2 for tensor-admissible r<1/2; disagrees with downstream Cassini if local unscreened UV assumptions apply; no q selection or all-MOND exclusion | 590d17d77 |
| K706 | W4-08/Lean-gravity | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/gravity_constraints` | one kernel-checked gravitational-constraint and physical-amplitude algebra module | - | lean | PARTIAL: fourteen standard-axiom critical prints; true controls and three genuine False mutants; actual pi and covariant PDE source density quantum bridges remain analytic or unproved; original goal open | 590d17d77 |
| K707 | W4-08/5Dprotected | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_normalization` | exact five-dimensional supersymmetric prepotential and gravitational CS normalization operator map | - | audit | SCOPED CLOSURE: protected cubic multiplies kinetic and CS operators; pure-electric FwedgeF zero; Coulomb vacuum zero; minimal ungauged SUGRA fixes relative coefficients but still gives Maxwell response and Ricci-flat vacuum; no all-gaugings exclusion | eeb8b9492 |
| K709 | W4-08/S4quantum | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/protected_normalization` | actual sphere determinant and retained interacting zero mode with bounded smooth scalar source profile | - | audit | SCOPED CLOSURE: gapped free relative determinant analytic and free zero mode logarithmic; finite-cutoff bounded quartic response analytic with negative variance; no positive leading local cubic in tested class; epsilon=W-HWH/4 and finite gravitational matching remain; Lorentzian continuum response unproved | eeb8b9492 |
| K716 | W4-08/geometric-deformation | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/geometric_source` | bounded same-field potential deformation and retained normal-fluid Euler equation in the covariant gravitational phase | - | audit | SCOPED NONSELECTION: positive U_A preserves chi0 vacuum UV and quadratic data while changing formal C3; full curved halo unproved; regular mass restores quadratic IR; displayed normal-fluid vacuum quadratic dynamics absent and static-rest ansatz fails subleading Euler condition; no all-superfluid exclusion | be8fc76cb |
| K717 | W4-08/integrable-Weyl | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/geometric_source` | integrable Weyl scalar invariant variables and off-shell matter unit-vector source normalization audit | - | audit | SCOPED CLOSURE/TRADE: consistent normalized-vector closure plus literal Einstein-metric matter has zero direct scalar charge; published external prescription needs separate bridge; even granted map xi=32pi/(lambda beta^2) leaves invariant free; finite-gradient positivity not regular vacuum quantum health | be8fc76cb |
| K718 | W4-08/curved-c1-clock | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/geometric_source` | actual de Sitter lapse shift reduction and controlled homogeneous near-vacuum Bianchi tilt of fixed c1 rational completion | - | audit | PARTIAL HEALTH REPAIR: constrained transverse and longitudinal clock-metric vacuum coefficients positive and fixed-k solutions future bounded; homogeneous tilt decays in explicit small-gradient basin; qualifies prior flat-window inference; finite-k finite-gradient scalar auxiliary quantum halo and selector gaps remain | be8fc76cb |
| K721 | W4-08/protect-N1 | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/symmetry_protection` | explicit local N1 completion of the exact eta amplitude-tail potential with fixed vacuum and quadratic data | - | audit | SCOPED NONSELECTION: constrained real superfield realizes exact U_eta; ordinary finite S,T sigma model has same potential and positive transverse bosonic vacuum masses; N1 permits operator; no renormalizable UV or full SUSY MOND portal and quantum health claimed | 99963e8f1 |
| K722 | W4-08/protect-Goldstone | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/symmetry_protection` | exact internal point and nonlinear DBI Galileon Ward identities with physical source and radial response | - | audit | SCOPED CLOSURE: inherited canonical action has only reflection; exact shifts remove required coefficients; flat DBI has no linear induced-matter charge; AdS DBI gives attractive geometric charge but quadratic IR and unselected gravitating height; sourced Galileon has different radial powers; no all-symmetry exclusion | 99963e8f1 |
| K723 | W4-08/protect-N2 | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/symmetry_protection` | four-dimensional electric magnetic FI partial-breaking action and protected Higgs geometry operator transfer | - | audit | SCOPED CLOSURE: full rigid APT potential retains 2mp and gapped Yukawa scalar; explicit allowed higher prepotential jet preserves vacuum quadratic data; protected Higgs metric has zero-energy vacuum and no derived gravitational NLO MOND operator; local SUGRA and microscopic bridge missing | 99963e8f1 |
| K724 | W4-08/protect-critical | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/symmetry_protection` | interacting dimension4/3 H1 source and protected anomaly large-charge duality amplitude tests | - | audit | SCOPED CLOSURE: exponent-matching bottom-source runs away on full Coulomb branch; stable common-domain affine source has inherited wrong leading sign; genuine F-terms have other dimensions; anomaly protects on-shell four-derivative observable; large-charge stress nonvacuum and dualization leaves coefficient free; other ensembles portals and microscopic constructions open | 99963e8f1 |
| K725 | W4-08/unified-matrix | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant` | common IKKT matrix action one-loop Einstein vacuum terms and actual fixed-background point-source Green response | - | audit | SCOPED NONSELECTION: displayed halo is linear in source mass rather than sqrt(M); isolated fixed-measure vacuum variation has preserved source-sign discrepancy; scalar frequency repair possible but full constrained stress nonlinear dilaton higher-spin background quantum health and operational cubic remain open | d51647e98 |
| K726 | W4-08/unified-induced | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant` | interacting seagull-corrected induced gravity and actual conserved-current covariant frame portals | - | audit | SCOPED CLOSURE: gapped metric functional has no local acceleration cubic; static acceleration connection is pure gauge; chemical-frame workaround alters actual Newton coefficient and total reservoir stress with minimal flat phase-frame instability; curved critical nonlocal microscopic completion remains open | d51647e98 |
| K727 | W4-08/unified-flux | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant` | six-dimensional Einstein-Maxwell flux sphere with canonical radion positive vacuum full bosonic linear spectrum and physical matter source | - | audit | SCOPED CLOSURE: stable positive vacuum and geometric scalar charge give Yukawa force; exact m_rad^2+9H^2=R_sphere^-2 removes broad 4D subcurvature unscreened window; critical fold is inflection; no operational MOND cubic or quantum UV completion claimed | d51647e98 |
| K728 | W4-08/unified-function | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant` | single generalized aether function actual dS scalar constraints same-state weak source and opposite-branch deformation | - | audit | SCOPED NONSELECTION: explicit positive dS toy has healthy linear tensor scalar coefficients but linear actual weak force; smooth negative-argument deformation preserves entire positive-argument flat-static MOND law and UV offset while moving vacuum; critical endpoint nonlinear same-state halo and microscopic branch relation remain open | d51647e98 |
| K747 | W4-21/screen | `why_4_puzzle/W4_21_pi_bookkeeping` | pi bookkeeping for the single-mediator ratio R = eps C3^2/C2^3 (W4-04 target 128pi/9); glued one-scale media | - | audit | SCREEN: if every pi rides with a scale (thermal pi theta, H-type 8piG/3) or a common factor, R is algebraic (1+2-3 = 0), so xi = 8 Omega_n/(9R) carries wt(Omega_n) >= 1 and is never 1/4 in any n; thermal 16/5 and the H-type routes are one failure; necessary condition wt eps + 2 wt C3 - 3 wt C2 = 1, shapes (1,0,0) (-1,1,0) (0,-1,-1); selects nothing | 4682ebfb1 |
| K748 | W4-08/critical-endpoint | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint` | alpha_eff = 2 same-state sourced response of the single-function khronometric action (clock flow kept: K = (r^2v)'/r^2, a = Phi' + vv'; khronon alpha_I K = 2K0) | - | audit | UNDETERMINED: regular F quartic (no MOND); cusp at I0 gives leading-order deep MOND above h_c = 18(/c2///c1/)H^2/a_M, but convective runaway beyond r_w = 0.82(GM a_M)^(1/4)/H and khronon back-reaction ~(/c1///c2/)Phi_N; full system diverges on the frozen grid; c_s^2 = 0 strong coupling | e786a6b06 |
| K749 | W4-08/critical-endpoint-amplitude | `why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint` | operational C2, C3, eps at the cusp endpoint and principles P1 kink self-tuning, P2 deep scale invariance, P3 opposite-branch deformation | - | audit | NOT SELECTED: R_amp = (4/3)(H/a_M)^2 = (4/27)(/c1///c2/)(/I0//x_a) free; tunings T1 criticality + T2 vacuum-at-cusp; deformation not excluded (alters only G_cos); target needs (/c1///c2/)(/I0//x_a) = 96pi | e786a6b06 |
| K751 | W4-22/K0 | `why_4_puzzle/W4_22_gauss_times_loop_model` | CORRECTION of K747: W4-21's three weight shapes | - | audit | CORRECTION: (1,0,0), (-1,1,0), (0,-1,-1) are one class modulo common-factor (1,1,1) and field-rescaling (0,3,2) shifts, which span the kernel of (1,2,-3); only wt R = 1 is invariant | f216b048f |
| K753 | W4-23/L | `why_4_puzzle/W4_23_gauss_law_flux_rescue` | duality and sign lemma for the Gauss-law route (W4-08 R3) | - | audit | AUDIT: every MOND law is convex in s = g^2 and concave in t = gN^2, so stable s-affine media cannot give ANY MOND interpolation; flux-affine = field-affine at fixed x, so a Gauss-law rewrite of the same attractive mediator does not escape; the escape is an opposite-sign flux sector = QUMOND's indefinite structure (X15, Cassini p58) | 439c6ba1d |
| K756 | A0SEL-20261024/RESPONSE | `reviews/a0_selection_2026_10_24` | dust-vacuum curvature projector versus preferred-clock cubic response | - | audit | AUDIT: exact dust projector isolates Lambda but material pressure contaminates it; symmetry-allowed cubic clock-acceleration coefficient shifts operational a0 while vanishing on homogeneous background; full covariant health not established | freeze:87e0c60793 |
| K757 | MICROMED-20261024/HEALTH | `reviews/microscopic_medium_2026_10_24` | common clock-solid medium at exact vacuum stress | - | audit | SCOPE: q^2 K-mu^2 S=(rho+p)/2 forbids positive kinetic and clock-gradient energy on nondegenerate first-derivative branch; derivative mixing cannot repair positive-elastic branch; higher k^4 stabilizer leaves an IR band in isolated example | freeze:36c2d800d1;continuation:0e132d0606 |
| K758 | MICROMED-20261024/VOLUME | `reviews/microscopic_medium_2026_10_24` | constrained determinant medium U(J) | - | audit | AUDIT: on invertible U-second-derivative-nonzero branch U-prime=C retains integration constant; stress is vacuum-like but no local J response; explicit quadratic example reproduces flux-type freedom | freeze:36c2d800d1;continuation:0e132d0606 |
| K760 | MICROMED-20261024/PARENT | `reviews/microscopic_medium_2026_10_24` | published vector-condensation higher-energy parent arXiv:1410.2408v2 | - | audit | SOURCE CHECK: equations 31 and 34-41 retain independent vacuum V0 versus response scale mu^2=m_A M_V; not an exact Lambda-medium or MOND completion | freeze:36c2d800d1;continuation:0e132d0606 |
| K762 | SELFSELECT-20261024/PROMOTE | `reviews/self_tuning_selector_2026_10_24` | remaining cubic response coefficient promoted to rigid or local variable | - | audit | AUDIT: rigid variation without potential enforces integral O3=0; W(b) inserts new potential and average; local positive-gradient model gives b_infinity-Q/(4pi Z r), retaining boundary normalization; not a general no-go | freeze:f458ddcc26 |
| K764 | LOCALSCREEN-20261024/MATCH | `reviews/local_screening_2026_10_24` | exact classical field rescaling of logarithmic KGB plus trial normalized-clock response | - | audit | REFINEMENT of K761: bare V disappears from full inhomogeneous base action after clock rescaling; h and alpha remain inputs; normalized-clock response operator is invariant separately and its coefficient is not fixed; no quantum or UV matching | freeze:70cf999088 |
| K765 | CONDJOINT-20261024/RABI | `reviews/condensate_joint_matching_2026_10_24` | ordinary analytic condensate mixing versus normalized phase vacuum interaction | - | audit | SCOPED CLOSURE: stable-mass NR bilinear mixing is degree one in densities and gives p_R=0; phase-only potential gives p=-U but changes microscopic interaction and retains independent amplitude and offset | freeze:fba75ecd27 |
| K766 | CONDJOINT-20261024/RATIO | `reviews/condensate_joint_matching_2026_10_24` | actual cubic force and conditional common-scale microscopic amplitude ratio | - | audit | CONDITIONAL REDUCTION: a0=q^3/(4pi G C) is field-normalization invariant; C=c3 Lambda and q=cb Lambda/Mpl and epsilon=c0 Lambda^4 cancel Lambda but leave kappa=2sqrt(8pi)cb^3/(c3 sqrt(c0)); amplitudes and absolute scale unselected | freeze:fba75ecd27 |
| K767 | CONDJOINT-20261024/PARENT | `reviews/condensate_joint_matching_2026_10_24` | two-field superfluid derivative parent arXiv:2009.03003v3 with finite amplitude regulator | - | audit | PARTIAL: amplitude elimination yields MOND cubic on large-amplitude branch; finite regulator has exact threshold x=1+1/sqrt(2) where amplitude gap closes; Lambda and Lambda_c and baryon portal remain inputs; no joint vacuum matching or UV completion | freeze:fba75ecd27;continuation:54785632d6 |
| K768 | RGJOINT-20261024/MATTER | `reviews/rg_joint_selector_2026_10_24` | matter-only functional RG vacuum offset | - | audit | SCOPED OBSTRUCTION: field-independent vacuum shift survives exactly on fixed external metric; dimensionless shift has exponent d and free dimensionful coefficient; metric fluctuations excluded | freeze:4020715cf3 |
| K769 | RGJOINT-20261024/RATIO | `reviews/rg_joint_selector_2026_10_24` | RG flow versus trajectory-independent MOND matching invariant | - | audit | CONDITIONAL CRITERION: beta log kappa zero is not selection; physical map must annihilate every free-direction projection (-1/2 -1 3); individual amplitudes need not be unique; no microscopic beta system computed | freeze:4020715cf3 |
| K770 | RGJOINT-20261024/AS | `reviews/rg_joint_selector_2026_10_24` | arXiv:2609.29369v1 gravitational coupling correlation | - | audit | SOURCE AUDIT: Horndeski relation selects CC trajectory within truncation but converged endpoint is negative; positive branch unresolved; nonanalytic MOND operator and baryon portal not matched | freeze:4020715cf3 |
| K771 | RGJOINT-20261024/IR | `reviews/rg_joint_selector_2026_10_24` | arXiv:2609.29979v1 IR screening plus conditional endpoint closure | - | audit | SOURCE AUDIT: reported vacuum attractor in frozen-G R2 single-mode truncation lacks MOND matching; Lambda=A k^2 with k=xi H and vacuum Einstein equation fixes xi for nonzero H but not H itself | freeze:4020715cf3 |
| K772 | FUNCQG-20261024/FUNCTIONAL | `reviews/functional_qg_matching_2026_10_24` | arXiv:2302.10989v1 functional kinetic fixed point | - | audit | SOURCE AUDIT: full kinetic-function study treats g externally and lambda=0; no joint vacuum/baryon matching; UV kinetic normalization does not prove physical IR quadratic coefficient or exclude nonuniform MOND limit | freeze:18c33c1688 |
| K773 | FUNCQG-20261024/FORCE | `reviews/functional_qg_matching_2026_10_24` | quadratic contamination of the sourced cubic force | - | audit | CONDITIONAL RESULT: exact g_phi^2+g_star g_phi=a0 g_N with g_star=qZ/C and a0=q^3/(4pi G C); finite positive g_star restores inverse-square low-gradient force; both invariant under field normalization; finite-domain viability requires suppression not necessarily exact zero | freeze:18c33c1688 |
| K774 | FUNCQG-20261024/PORTAL | `reviews/functional_qg_matching_2026_10_24` | arXiv:2009.13543v2 predictive scalar-fermion matter portal | - | audit | SOURCE AUDIT: FP3 predicts marginal matter interactions within truncation but retains mass/gravity directions; Higgs/Yukawa portal is not matched to MOND source q or cubic C; free parameter count alone is not a ratio nonselection proof | freeze:18c33c1688 |
| K775 | SYMGQG-20261024/CONFORMAL | `reviews/symmetry_gauge_matching_2026_10_24` | spatial conformal protection and arXiv:2601.04290v1 | - | audit | CONDITIONAL AUDIT: bare cubic symmetry leaves amplitude and source free; compensator permitting vacuum scale also permits quadratic operator; cited dS proposal has no computed vacuum or matching factor | freeze:4dde973a74 |
| K776 | SYMGQG-20261024/GAUGE | `reviews/symmetry_gauge_matching_2026_10_24` | arXiv:2502.14686v1 joint gauge coefficient matching | - | audit | SOURCE AUDIT AND CONDITIONAL MATCHING: cancellation sum rule does not fix particle product; vacuum normalization and stationary initial amplitudes remain in physical kappa; no microscopic joint selection | freeze:4dde973a74 |
| K777 | SYMGQG-20261024/RESIDUAL | `reviews/symmetry_gauge_matching_2026_10_24` | residual linear polarization response | - | audit | CONDITIONAL DIAGNOSTIC: isotropic D=delta g+g^2/a0 has low-gradient g_N/delta; finite MOND requires delta much smaller than g/a0; not a derived spherical Yang-Mills solution | freeze:4dde973a74 |
| K778 | QMETRIC-20261024/PROTECTION | `reviews/quantum_metric_protection_2026_10_24` | matter-induced metric kinetic and source matching | - | audit | CONDITIONAL OBSTRUCTION: after scalar-metric diagonalization pure-induced gravity removes both quadratic scalar and direct baryon charge; mixed gravity restores both; metricity does not impose additional cancellation counterterm | freeze:09a5823e84 |
| K779 | QMETRIC-20261024/VACUUM | `reviews/quantum_metric_protection_2026_10_24` | stationary vacuum of minimal two-metric induced action | - | audit | CONDITIONAL OBSTRUCTION: common vacuum coefficient rescaling preserves stationary scalar but changes energy; finite healthy positive-vacuum stationary point has m^2=-4H^2 in two-derivative truncation and is not a stable attractor | freeze:09a5823e84 |
| K780 | CONDCANCEL-20261024/BRANCH | `reviews/condensate_cancellation_2026_10_24` | timelike condensate sourced static MOND branch | - | audit | CONDITIONAL OBSTRUCTION: smooth healthy P(X) root gives opposite-sign y^3 static current; attractive MOND P_X=C y forces negative rest-frame time kinetic for y^2<v^2/2; fixed metric and P(X)-dominated regime only | freeze:ceec4e5b4b |
| K781 | CONDCANCEL-20261024/SOURCE | `reviews/condensate_cancellation_2026_10_24` | condensate source and vacuum matching | - | audit | CONDITIONAL AUDIT: nonderivative baryon source drives shift charge; constant derivative coupling to conserved current is a boundary term; vacuum offset remains; arXiv:1212.2185v2 stabilization has nonzero k^2 and unfixed stabilizer coefficient | freeze:ceec4e5b4b |
| K782 | AESTJOINT-20261024/SOURCE | `reviews/aest_joint_matching_2026_10_24` | AeST metric-vector-scalar baryonic source mixing | - | audit | PARTIAL MECHANISM: static diagonalization retains a baryonic scalar source without explicit shift-breaking portal; published stability is background/regime-limited and not a full sourced positive-vacuum theorem | freeze:0d491d43b2 |
| K783 | AESTJOINT-20261024/MATCH | `reviews/aest_joint_matching_2026_10_24` | AeST symmetry-preserving vacuum and spatial deformations | - | audit | CONDITIONAL NONSELECTION: constant Y and Y^(3/2) coefficients independent under stated symmetries; a0=Ghat/(gamma G_N); doubling gamma halves a0 with calibration fixed; positive quadratic coefficient restores lowest-gradient inverse-square response | freeze:0d491d43b2 |
| K784 | LIFSHITZLOOP-20261024/SHELL | `reviews/lifshitz_radiative_protection_2026_10_24` | finite-shell one-loop cubic-gradient scalar with k4 stabilizer | - | audit | CONDITIONAL RESULT: healthy nonzero-gradient quadratic fluctuations generate /grad phi/ and gradient-squared terms in formal finite-shell determinant; bare b=0 not automatically preserved; coefficients regulator dependent and higher-loop zero-gradient limit unresolved | freeze:5b11740a2a |
| K785 | LIFSHITZLOOP-20261024/SYMMETRY | `reviews/lifshitz_radiative_protection_2026_10_24` | polynomial-shift protection transfer test | - | audit | CONDITIONAL OBSTRUCTION: cubic-gradient Euler expression changes under linear spatial shift so known polynomial-shift protection does not transfer to this operator alone; constant shift leaves vacuum and force amplitude independent | freeze:5b11740a2a |
| K786 | SUSYLIF-20261024/PAIRING | `reviews/susy_lifshitz_matching_2026_10_24` | supersymmetric Lifshitz spectral pairing on gradient backgrounds | - | audit | CONDITIONAL CANCELLATION: equal full boson-fermion spectra cancel one-loop terms for arbitrary common gamma; illustrative splitting restores lower-gradient terms; no interacting MOND multiplet or positive-vacuum matching constructed | freeze:234b155255 |
| K787 | SUSYLIF-20261024/ACTION | `reviews/susy_lifshitz_matching_2026_10_24` | detailed-balance MOND operator and positive vacuum audit | - | audit | RESTRICTED OBSTRUCTION: derivative-only single-field local W has zero Euler derivative on affine backgrounds; additional auxiliary multiplets not excluded; unbroken rigid vacuum has zero algebraic energy; stable positive sourced amplitude remains unselected | freeze:234b155255 |

## LN: Logic / Lean formalisations

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K075 | L1 | `fable_independent_2026/lean_2026/PUZZLE_32pi_reductions.lean` | 11 theorems on the reductions | - | lean | algebra only | 4e233d832 |
| K076 | L2 | `fable_independent_2026/lean_2026/PUZZLE_32pi_chain_2026_10_05.lean` | SdS no-go / flux form / BIMOND vacuum / exchange symmetry | - | lean | premises => conclusions only | 38ba44ec2 |
| K077 | L3 | `fable_independent_2026/lean_2026/PUZZLE_32pi_postulate_status_2026_10_05.lean` | postulate independence: every kappa has a model | - | lean | kappa stays FITTED | b8b1080ce |
| K078 | L4 | `fable_independent_2026/lean_2026/PUZZLE_32pi_one_pi_obstruction_2026_10_05.lean` | one-pi obstruction: ~60 principles give q*pi^(+-1) | - | lean | fixes the shape of the missing principle | ff8b44018 |
| K087 | H | `sonnet55_push/puzzle_32pi/agents/H_lean_bridges/` | 110 bridge theorems | - | lean | algebra only | 20bdc3eb0 |
| K109 | H2 | `sonnet55_push/puzzle_32pi/agents/H2_lean_bridges_wave2_4/` | 203 theorems; 16 readings TFAE one OpenPremise | - | lean | not a theorem of the definitions | 1138d817f |
| K136 | LN1 | `fable_independent_2026/lean_2026/KAPPA_LOGIC_2026_10_20.lean` | independence theorem extended to the k04 four-form; premise->kappa^2 map | - | pend | PENDING: written, not compiled (32pi chat) | untracked |
| K138 | LN8 | `fable_independent_2026/lean_2026/REV_nariai_a0_shell.lean` | Nariai a0-radius = dS horizon (Lean recast of N1) | - | lean | postulated; no evidential weight | 23dc871c4 |
| K141 | LN11 | `fable_independent_2026/lean_2026/TOE_BEST_ATTEMPT_2026_10_12.lean` | kappa enters only as kappa^2 rho | - | lean | 'derived kappa' left as an unmet obligation | 5e0b67a13 |
| K142 | LN12 | `fable_independent_2026/lean_2026/XC4_recipe_decision_certificates.lean` | Z = sqrt(8pi/3)/kappa identity | - | lean | identity | 27bc6db4c |
| K201 | TL1 | `lean/theory_theory_of_gravity.lean` | Z = sqrt(8pi/3)/kappa | - | lean | identity | 358768f02 |
| K292 | sol61-83 | `sol61_push/gravity_architecture_lean_2026_10_12/Architecture.lean` | Lean a0=kappa c sqrt(G rho) | - | lean | identity | 33ec30852 |
| K293 | sol61-84 | `sol61_push/framework_certification_2026_10_12/RESULT.txt` | Lean offset theorem; tie W0=4a0^2/G | - | lean | condition only | untracked |
| K313 | sol61-104 | `sol61_push/puzzle_32pi_nonselection_2026_10_15` | Lean: offset invisible to all response tests | - | lean | non-selection theorem | untracked |
| K396 | RV-28 | `real_research/reviews/kappa_selection_2026_09_21/` | does the static auxiliary action select lambda=1 | - | lean | NOT ESTABLISHED | bf4bf8bed |
| K533 | AS072 | `deepseek_push/astra_spawn_ideas/results/AS072` | normalisation theorem under 5 premises | - | lean | each premise removable | 511efeb1d |

## EX: External pasted derivations

| id | source | path | mechanism | kappa (or options) | class | verdict | commit |
|---|---|---|---|---|---|---|---|
| K116 | EXT01 | `sonnet55_push/puzzle_32pi/external_notes/EXT01_gauge_vacuum_identity_and_clock_2026-10-02.md` | Ward identity Z_A; clock repair | - | free | self-labelled NOT DERIVED; never touches a0 | 45f71c83f |
| K117 | EXT02-P1 | `sonnet55_push/puzzle_32pi/external_notes/EXT02_pasted_32pi_derivations_2026-10-02.md` | postulate A*Lambda=32pi^2 ('Rindler disk') | - | free | VOID: the postulate is the target | 7055e4c6e |
| K118 | EXT02-P2 | `sonnet55_push/puzzle_32pi/external_notes/EXT02_pasted_32pi_derivations_2026-10-02.md` | same + GHY term + Lean axiom | - | free | VOID: target restated; the Lean axiom proves False | 7055e4c6e |
| K119 | EXT02-P3 | `sonnet55_push/puzzle_32pi/external_notes/EXT02_pasted_32pi_derivations_2026-10-02.md` | heat-kernel boundary anomaly | 0.28 | any | VOID (algebra slip; does not compile) although the number lands in the window | 7055e4c6e |
| K120 | EXT02-P4 | `sonnet55_push/puzzle_32pi/external_notes/EXT02_pasted_32pi_derivations_2026-10-02.md` | spin sum rule = 720 | 2.5 | any | VOID: miscounted; its Lean theorem is false | 7055e4c6e |
| K121 | EXT02-P5 | `sonnet55_push/puzzle_32pi/external_notes/EXT02_pasted_32pi_derivations_2026-10-02.md` | 'd=4 is unique' | - | free | VOID: d=4 built in (target restated) | 7055e4c6e |
| K122 | EXT02-P6 | `sonnet55_push/puzzle_32pi/external_notes/EXT02_pasted_32pi_derivations_2026-10-02.md` | Vol(D2xS2)/Vol(S4)=16pi | - | free | VOID: 'fraction' > 1; target restated | 7055e4c6e |
| K123 | EXT03 | `sonnet55_push/puzzle_32pi/external_notes/ext03_check.py` | scalar-Euler action + trace anomaly in dS | - | free | RESTATED: a0^2=3/(32 G a_E) needs a_E~3e122 | 725683231 |
| K124 | EXT04 | `sonnet55_push/puzzle_32pi/external_notes/ext04_check.py` | two-potential flat-rotation trace solution | - | free | CLOSURE: one speed per QFT; no BTFR | 876a36ecd |

