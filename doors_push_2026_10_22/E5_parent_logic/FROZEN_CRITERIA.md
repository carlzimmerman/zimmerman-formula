# E5_parent_logic FROZEN CRITERIA (written before any script or number of this lane)

Wave E audit, item (4) "no covariant parent" (`BRIEF.md`, `BRIEF_E_AUDIT.md`). κ = ½ is FITTED (κ = Z/4π is a postulate,
Z = 5.78881). Footings a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt; AG6C's values), never pooled. Cold energy is the
extra mass; no particle species. Not "theory closed". Nothing here says the data favour the framework over ΛCDM. Anything
true by construction is flagged and carries no verdict weight.

## 0. Target and question

The **screened theory** = PAPER49's static action WITH stiffness (PAPER49 §2):
L = −|∇Φ − KP|²/2K − ρ_bΦ − W_rem(K|P|) − (γ/2)|∇P|², γ = KL★²/2, L★ ∈ [24 pc, 90 pc] (CFG820 floor; D8 ceiling), with
1 kpc carried as the old upper end (D9), and the kinematic identity ∂_tP = −j ⇒ ∇·P = ρ_c − ρ̄ (PAPER49 eq. 1).
Questions: (1) for each no-go used against a parent (NG1, NG2 incl. D9's Λ_LV, D-T, WT-02, D9b's double count / unique M\*),
list its hypotheses and test whether it applies to the screened theory, not only to the L★ → 0 law; (2) can the R3θ ghost
(CFG944) be removed by the stiffness or by a gate without new fitted numbers; (3) classify "EFT without a parent" as
(a) theorem for stated classes, (b) only for the L★ → 0 law, or (c) open.

Record checked before freezing: D9 README + MAP + FROZEN_CRITERIA; D9b README + FROZEN_CRITERIA; AG6C README and
`ag6c_s0_saddle.py/.out`; CFG941 README + DERIVATION §1–4; CFG944 README + DERIVATION; WT-02 README; CFG938 DERIVATION §3
(τ_μν = D_μD_νχ − ⅓h D²χ with D_μD^μχ ≡ h^{μν}∇_μ∇_νχ); PAPER49 TeX §2–3 and DEPOSIT (v1.2); AG7 README; E2 criteria
(γ = 0 static branch = AQUAL μ = x/(1+x)). No committed lane has solved the saddle WITH the stiffness, or computed the
stiffness's contribution to the R3θ kinetic matrix or to NG2's cone.

## 1. Checks (script `e5_parent_logic.py`, sympy + numpy/scipy, deterministic, single thread)

### Saddle (NG1 with stiffness). Method, declared now
Linearise the stiffened static equations about the γ = 0 (AQUAL) solution. At leading order in u/a₀ (deep regime, where the
saddle is) the stiffness enters the AQUAL flux equation as an extra effective source (γ/K)∇²ρ_ph0 = (L★²/2)∇²ρ_ph0, while the
phantom stays ρ_ph = ∇²Φ/K − ρ_b (derivation checked symbolically in E1 below; the dropped term is O(u/a₀) relative). In
AG6C's deep units (G = M = d = 1, GMa₀ = 1) the added source is (λ/2)∇̂²Ĉ with λ ≡ L★²/(r_M d), r_M = √(GM/a₀). AG6C's
deep two-body solver (grid HF = 0.0025, b = 0.01, R,z ≤ 60) is copied (read-only reuse; AG6C files are not touched).
The source is applied only outside r_cut of each mass (deep-MOND is invalid inside ~r_M); r_cut ∈ {0.05, 0.1} d.
Response coefficient C₁(R) ≡ δĈ(R, 0)/λ at mid-plane R = 0.1, 0.2, 0.3 d from λ_num ∈ {1e-5, 2e-5}
(fallback declared now: if the linearity line fails, rerun at {1e-6, 2e-6} and report both).

| id | test | PASS line |
|---|---|---|
| K0 | copied solver reproduces AG6C mid-plane Ĉ(0.1, 0.2, 0.3) = −0.40432, −0.24012, −0.11399 and negative column −0.20640 | each within 1% |
| E1 | sympy: linearised stiffened system gives ∇·[A∇δΦ] = γ∇²ρ_ph0 − ∇·[Aγ∇²P0], A = linearised AQUAL tensor; A → (u/a₀)(I + ĝĝ) in the deep limit; stiffness-screening lengths ℓ_∥ = L★√(a₀/4u), ℓ_⊥ = L★√(a₀/2u) | symbolic residual 0 |
| S1 | linearity: C₁(R) from the two λ_num agree | within 5% at R = 0.1, 0.2, 0.3 (both r_cut) |
| S2 | robustness to the core cut: C₁(0.2) at r_cut = 0.05 vs 0.1 | within 20% |
| S3 | **NG1 survives the stiffness**: |λC₁(0.2)| ≤ 0.1|Ĉ(0.2)| for F1 (8e10 M☉ each, 0.77 Mpc) and F2 (2e13 M☉, 5 Mpc), both footings, L★ = 24 and 90 pc (r_cut = 0.1) | all 8 cases |
| S4 | the stiffness-dominated core around the null point: R_core where ℓ_⊥(R) = R on the mid-plane (u/a₀ = (r_M/d)ĝ) | R_core < 0.1 d at L★ ≤ 90 pc, all fiducials and footings |
| — | reported, no pass line: δĈ/Ĉ at 1 kpc; first-order L★,crit where λC₁(0.2) = −Ĉ(0.2) (if C₁ has that sign; otherwise "stiffness deepens the trough") | — |

### D-T and NG2 with the stiffness
| id | test | PASS line |
|---|---|---|
| T1 | sympy: Newtonian cold medium + tether with linear coefficient c₂ + stiffness γ: ω² = (σ² + γρ₀)k² + (c₂ − 1)Kρ₀ (no-dispersion: σ = 0). The self-gravity coefficient is independent of γ; the law's deep limit forces c₂ = 1 at scales ≫ ℓ (DT1 reproduced) | symbolic residual 0 (reproduces CFG941/D9b T1; low weight) |
| N1 | sympy: for L(X), v_X² − 1 = −2XL_XX/(L_X + 2XL_XX); the law's dual L_dark (AG6C) has L_XX < 0 for all X > 0 (Adams et al. 2006 positivity sign; external theorem, labelled) | symbolic |
| N2 | dark-sector curl stiffness carried by the U(1) field (needed: AG6C's C1 carries only (∇·P)², S0.3). X-mode (k ⊥ ê): (i) canonical H ⊃ (γ/2)|∇×D|² ⇒ ω²/k² = N_⊥(1/ε_∥ + γk²) (unbounded); (ii) local-Lagrangian truncation −(γ/2)|∇×D(E)|² ⇒ kinetic coefficient ε_∥(1 − γε_∥k²) (< 0 for k² > 1/γε_∥); both → N_⊥/ε_∥ = 1 + g/a₀ as k → 0 | symbolic; i.e. stiffness never brings v ≤ c inside the EFT band |

### R3θ ghost vs stiffness and gates (CFG944)
| id | test | PASS line |
|---|---|---|
| G1 | sympy: longitudinal plane wave, medium L = ½ρ₀ξ̇² + F(θ) + V(ξ, ∇ξ) with any stiffness V free of ξ̇: kinetic coefficient = ρ₀ + F_θθk², independent of γ | symbolic |
| G2 | sympy, flat space, χ = χ̇̄t + δχ, medium 4-velocity (1, v): τ_ij at linear order (a) Hessian reading h h∇∇χ (CFG938's definition): no v-term; (b) iterated reading D_i(h∂χ): τ ⊃ χ̇̄σ_ij. Stiffness F_θθ contribution: 0 (a), −(γ/K²)(2/3)·(3/2)χ̇̄²/… computed exactly (b); sign ≤ 0 in both | sign ≤ 0 in both readings (no cure); (b)'s ghost wavenumber k_gL★ on FRW reported |
| G3 | Theorem G′: CFG944's bound with stiffness, L(θ, u, τ) convex in θ and the static law: B ≥ W(u*) + S(τ*) ≥ W(u*) (sympy on the convexity step with a generic S ≥ 0) | symbolic; the record's B/B_e = 15.0 / 25.3 can only grow |
| G4 | gating the stiffness too (R3θ as written: s(θ)[W + S]) changes F_θθ to −s″(W + S): ghost wavenumber k_g decreases by √(W/(W + S)) | symbolic |
| G5 | the only parameter-free u-gate scale u_c = a₀ vs CFG944 C4's window (slip u_c ≤ 0.22 / 0.16 a₀ at frozen profile, ≤ 0.46 / 0.34 a₀ absolute; c-amp u_c ≥ 29.3 / 24.3 a₀), read from `cfg944_results.json` | u_c = a₀ outside the window on both footings |

`E5_PARENT_LOGIC COMPLETE: N/M checks PASS.`; exit 0 iff all pass. Outputs `e5_parent_logic.out`, `e5_parent_logic_results.json`.
MUTATE (`E5_MUTATE=1`): (i) L★ × 1000 in S3/S4 (S3 and S4 must FAIL); (ii) the stiffness sign in G2(b) flipped (G2 must FAIL).
Outputs `e5_parent_logic_MUTATE.out`, `e5_parent_logic_results_MUTATE.json`.

## 2. Hypothesis audit (README table; reasoning, not a check)
For NG1, NG2 (+ D9 Λ_LV), D-T, WT-02, D9b (double count, unique M\*): every hypothesis, marked HOLDS / FAILS / NOT TESTED for
the screened theory, with explicit attention to minimal coupling, U(1) structure, static ansatz, phantom-as-gravity,
ΛCDM background, and which causality criterion (A: v ≤ c; B: owner's medium-frame criterion) each no-go uses.

## 3. Input ledger (README) and the verdict rule
Inputs classified RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY with source.
Verdict on the statement "the screened theory is an EFT without a parent":
- **(a) theorem for stated classes** if S3, S4, T1, N1, N2, G1–G5 pass: each no-go is shown to hold WITH the stiffness at
  L★ ≤ 90 pc for its stated class; the classes not covered are listed as open.
- **(b) only for the L★ → 0 law** if S3 or S4 fails at L★ ≤ 90 pc (the stiffness removes NG1), or N2 shows the stiffness
  restores v ≤ c, or G1/G2 show the stiffness cures the ghost.
- **(c) open** otherwise (e.g. S1/S2 robustness fails so the saddle answer is undecided).
Lane verdict word: SCOPED NO-GO for (a), CRISP FINDING for (b), NOTHING NEW / RUNNABLE NOW for (c), as the README states.
"Established parent": none, under any outcome.
