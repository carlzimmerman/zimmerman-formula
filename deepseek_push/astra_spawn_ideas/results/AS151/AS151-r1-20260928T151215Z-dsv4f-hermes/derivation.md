# AS151 — Extract all primary constraints of the localized action

- Run: `AS151-r1-20260928T151215Z-dsv4f-hermes` (worker: dsv4f-hermes, DeepSeek V4-Flash 0731 on OpenRouter)
- Task file: `deepseek_push/astra_spawn_ideas/AS151_extract_all_primary_constraints_of_the_localized_action.md`
  sha256 `1eb57dbb758b4246815003d1905ecd3eb55edc33f32e5b60c732d6f92868964c` (verified at start and re-verified at finish)
- Status: **derived for the bounded prototype domain** (classification: derived for the declared finite domain; no premature DOF/closure claim)
- Seed classification (per task): "no premature final DOF claim"; the primary-constraint list below carries an explicit function space and bounded domain.

---

## 0. Framework cell

- **Branch**: CA5-GNC-R canonical candidate (as the task declares; no separate spectral-lapse or trace-mixing diagnostic selected).
- **κ**: `a0 = κ c sqrt(G ρ_Λ)`, ρ_Λ = mass density; κ = 1/2 **adopted** (task condition, not derived here). `r_M = sqrt(G M_b/a0)`, `v_flat^4 = G M_b a0` (deep regime).
- **Both footings, kept distinct** (they cannot share fixed vacuum density AND fixed κ):
  - canonical: a0 = 9.3619e-11 m/s² → ρ_Λ = 5.84441e-27 kg/m³, ε_Λ = 5.25270e-10, Λ = 1.09080e-52 m⁻²; κ = 1/2 at own ρ.
  - alternative: a0 = 1.1279e-10 m/s² → ρ_Λ = 8.48309e-27 kg/m³, ε_Λ = 7.62422e-10, Λ = 1.58328e-52 m⁻².
  - Cross-check: κ_effective = 0.602388 when the alternative a0 is evaluated at the canonical ρ_Λ with κ free — i.e. the two footings are genuinely independent (recorded in residuals.json).
- **Branches**: Q, RAR, MU2, EXP, MONO kept distinct (criterion B = filtered MONO per the amended target); this seed's conclusions use only the CA5-GNC-R declared branch. No branch translation used.
- **Pinned sources** (sha256 verified before use): `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (must be b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e) and `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md`; conventions read from CANONICAL_AUXILIARY.md; branching protocol read from FIRST_PRINCIPLES_AND_BRANCHING.md; amendment spec read from FRIED_CHICKEN_SPEC.md (filtered MONO, criterion B).
- **Units**: SI (kg, m, s); a0 in m/s²; all coefficients dimensionless in the prototype except G, c which enter only via the footings above.

## 1. Bounded prototype and conventions (task step 1)

Leaf Σ = 2-cell oriented ring × 2 heat slices (r0, r1). Orthonormal-frame prototype (identity leaf metric h = δ) for the algebra; the fiber theorems are proven for general symmetric h with h^{ab} h_{ab} = 3 (see §2). Ring operators (exact on the ring):

- D_i f = f_i − f_{i+1} (ring derivative), Δ_i f = 2(f_{i+1} − f_i) (lattice Laplacian),
- product rule (div(N Dg))_i = N_i Δg_i + (DN)_i (Dg)_i — **verified exactly on the ring** (used in the lapse identity, §3a).

Physical-time velocities (8 total): carrier φ̇ (pd_0, pd_1), trace k̇ (kd_0, kd_1), shift components (u1̇, u2̇ per cell). **Every other field is static** (no physical-time velocity; unitary clock gauge, N-velocity U = 0 kin-level).

Localized ADM density (2-cell × 2-slice, terms per cell i):

- g-metric sector: (M2/2) N_i (ka1_i² + ka2_i² − 6 k_i²) − (c2 M2/2) N_i Q_K i², Q_K i = trace mean ⟨k⟩-deviation (N-weighted), M2 = M_P²√h/2 (>0), c2 ≥ 0.
- lapse/aux sector: α|a − DZ|² + 4 a·DZ − 2|DZ|² − 4 cN DZ·DU (with the exact square completion, verified: = α|a|² − 2 cN|DZ−(a−DU)|² + 2 cN|a−DU|²), a = D ln N (lapse differential).
- gate + compensator: cN N_i [G(Y_i) + ℓ a_i·DW_b,i], Y_i = J(DW_b,i) + ℓ ΔW_b,i − 1, J(p) = p² + p⁴, G = 0.04-ramp (G″ ≠ 0 in the transition window), ℓ = 0.04.
- heat constraint terms (r-slice coupling): cN N_i [L0f_i (∂_rW − ΔW = vW_i − lW0_i) + L1f_i (vW_i − lWb_i)] with L0f, L1f free heat-source components (NO t-velocity).
- clock-matter: t_i (pd_i − s_i Dφ_i)²/(2 N_i) − N_i (Dφ_i²/2 + 1)/t_i − N_i V0 (1 + (t_i + 1/t_i − 2)²), V0F(t) barrier, F flat to 3rd order at t = 1: F′(1)=F″(1)=F‴(1)=0, F⁗(1) = 24 (verified).
- λ0 term: cN N_i λ_i (W0_i − U_i) (heat projection on slice r0).

Deterministic seed 151; numeric sample PT0 (recorded in script): t0 = −(Z0−Z1+2)/2, t1 = (Z0−Z1+2)/2 at PT0: det(velocity–momentum) = 38904500000/812017791 > 0.

## 2. Step 2 — differentiate w.r.t. every physical-time velocity

Exact sympy momenta (velocity–momentum map H = ∂π/∂v, 8×8):

- π_kd0 = 3 M2 (3 N0² c2 kd1 − 3 N0 N1 c2 kd0 + 3 N0 N1 c2 kd1 − 8 N0 N1 kd0 − 3 N1² c2 kd0)/(4 N0² N1)
- π_kd1 = −3 M2 (3 N0² c2 kd1 − 3 N0 N1 c2 kd0 + 3 N0 N1 c2 kd1 + 8 N0 N1 kd1 − 3 N1² c2 kd0)/(4 N0 N1²)
- π_u1 = M2 u1/N (per cell, exact), π_u2 = M2 u2/N (per cell, exact)
- π_pd0 = −(Z0 − Z1 + 2)(−pd0 + s0(φ0−φ1))/(2 N0), π_pd1 = −(Z0 − Z1 − 2)(pd1 + s1(φ0−φ1))/(2 N1)

**Symbolic rank of the 8×8 velocity–momentum matrix: 8 (full)**; det at PT0 = 38904500000/812017791 > 0; inversion residual: velocities recovered from π via H⁻¹ (residual **0.0**, with the affine shift offset s_i Dφ subtracted — shifts enter π only through offsets, verified).

**Null directions of the velocity–momentum map: none.** Every physical-time velocity is momentized 1:1. All primary constraints of the localized action therefore come from the **static sector** (fields without t-velocities): augmented Hessian over the 26 slots has rank 8 → **18 null directions** (18 fields π_X^t = 0 at kin level). This is the Dirac–Bergmann primary set: π_N, π_n(i), π_Z, π_U, π_W(r0),π_W(r1), π_L(r0),π_L(r1), π_λ0, π_G, π_a, π_t (sectorial identification; exact count depends on the declared 26-slot model).

**Trace sector (metric fiber) — no hidden primary.** With h = identity frame:

- π^{ij} := ∂𝔏/∂(∂_t K_{ij})… model momentum = (M2√h/2)(K^{ij} − K h^{ij}), K := K^{ab} h_{ab} (single trace combination, two tensor modes = traceless 5 ⊕ trace 1);
- tr π = −(2A + 3B) K + 3B A_K/N with A = M2√h/2, B = c2 M2√h/2, A_K = N-weighted trace deviation (verified: fiber_trace_coefficient, exact symbolic);
- traceless block = A·id on the traceless 5 (fiber_traceless_block, exact);
- **inversion** (the algebraic content): K = (1/A)(π − tr_h(π) h/2), h^{ab} h_{ab} = 3:
  - identity metric: T_A∘S_A = id, S_A∘T_A = id — exact symbolic, **Lean-certified** (below);
  - general symmetric h (numeric): residual 5.55e-16 (≤ 1e-12);
  - tr(T_A K) = −2A·tr K (Lean-certified lemma).
- **c2 trace-mean system** (two cells, π = 0): (8A N1 + 3B S) K1 = 3B S K2 ∧ 3B S K1 = (8A N2 + 3B S) K2, S = N1+N2; det = 2A(8A N0 N1 + 3B(N0+N1)²) = (1/4)(64A² N0 N1 + 24AB(N0+N1)²) > 0 for A > 0, B ≥ 0, N0, N1 > 0 → **trivial kernel** (mean_kernel_trivial, exact; **Lean-certified**); inversion residual 5.55e-17.
- convention audit: model momentum = 2 × (the (14)-style trace momentum), factor velocity-independent and exact (model_momentum_proportional_to_14trace).

## 3. Step 3 — primary relations vs heat-elimination identities

**Primary (absent velocities, π^t = 0):** the 18 static fields (lapse, shift, Z, U, W0, W1, L0, L1, λ0, t-local, gate/aux): the rank evidence is the augmented Hessian rank 8/26 (null_directions_count). The heat equations (∂_r W − L = 0; Δ-coupling) are **not** t-time primaries: they involve r-shifts only and enter the canonical structure only after heat elimination.

**Identities arising only after spatial/heat elimination (all verified, residuals recorded):**

- (a) **Lapse density identity** (action (12)): δ_{lnN}∫N√h[G + ℓa·DW_b] = ∫N√h δlnN[G − ℓΔW_b]. Exact in the continuum (a = D ln N = DN/N; analytic cancellation of the DN·DW_b shift terms). On the ring, residual = the **Leibniz defect** ℓ N0 DW_b0 (DlnN − DN/N)₀: measured 9.365065e-4 = predicted 9.365065e-4 (12-significant-digit match); transition sample (Y0 = 0.04095, G″ ≠ 0): measured 2.43e-3 = predicted 2.43e-3 (relative 1.3e-9 ≤ 0.05). **Refined once** (2-ring → log-interpolated 4-ring): defect ratio 0.122 (consistent with ~h² → continuum zero).
- (b) rho_R lapse density: d(N√h 𝔏_d)/d ln N = −N√h ρ_R, ρ_R = tK_d + W/t + V0F(t), K_d ~ N⁻² (rhoR_lapse_density, exact).
- (c) σ_R = d𝔏_d/dt (sigmaR_is_dL_dt, exact; R3).
- (d) Z → Z + c(t): exact redundancy of the localized density; ⟨Z⟩ is a global normalization, not a primary (Z_constant_shift_invariance).
- (e) Projector solvability ∫N√h[σ_R − ⟨Nσ_R⟩_h/N] ≡ 0 (projector_solvability, residual 5.6e-17; R4).

**Primary-constraint list (deliverable, bounded domain):**

| sector | fields | t-time primary |
|---|---|---|
| lapse | N_i | π_N = 0 |
| shift | n^i (u1,u2)_i | π_n = 0 |
| clock | t_i | π_t = 0 |
| heat aux | Z_i, U_i, λ0_i | π_Z = π_U = π_λ0 = 0 |
| heat sources | W(r0)_i, W(r1)_i | π_W(r0) = π_W(r1) = 0 |
| heat multiplier | L(r0)_i, L(r1)_i | π_L(r0) = π_L(r1) = 0 |
| metric trace | k_i | none (invertible kinetic map; kernel trivial) |
| metric traceless | 5-dim | none (A·id) |
| gate/compensator | G(Y), a_i | π_G = π_a = 0 (static auxiliaries) |

Function space (declared): C∞ leaf fields on Σ = S¹-ring × {r0, r1}; prototype = 2 cells × 2 slices; fiber identities hold for general symmetric h; global lift is the next unresolved implication (§7). **No premature final DOF claim.**

## 4. Step 4 — falsifiable negative control (auxiliary r as physical time)

Treat r as time: ∂_rW is the only r-derivative; introduce vW_i := W1_i − W0_i (r-velocity) and rebuild the heat terms (spatial operators untouched):

- π_W^{(r)} = cN N (L0 + L1) ≠ 0 (r_time_W_momentum_nonzero): W acquires a spurious momentum.
- **r-kinetic Hessian = [[0,0],[0,0]] identically** (r_kinetic_hessian_degenerate): the +4 spurious pairs (W0_i, W1_i with shared frozen momentum) are kinetically frozen — not canonical.
- Count contamination: t-time primaries 18 → r-time 10 (primary_constraint_shift 8); the heat equation is reclassified as evolution (negative_control_contaminates PASS).
- Capable of failing: the symbolic Hessian was derived before evaluation (zero matrix); π_W^{(r)} symbolic and ≠ 0; had either failed the control intended to fail, the t-time count would be corroborated differently — as executed, the control behaves as required (contamination exhibited with explicit residual-free symbolic evidence).

## 5. Bounds and environment (actually enforced — recorded honestly)

- Threads: 1 — enforced via `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1` (all set in the run command).
- Wall: actual 14.42 s (≪ 120 s prototype budget). BIOS/OS-level timeout NOT applied (macOS has no GNU `timeout`); bounded by construction (max matrix 8×8, 26 slots) — stated as a bound by construction, not a claim of an enforced OS limit.
- Memory: RLIMIT_AS 512 MB attempted inside the script; macOS refused with `RLIMIT_AS not settable: current limit exceeds maximum limit` — recorded verbatim in residuals.json (`memory_limit_enforced`). Measured peak RSS (ru_maxrss, bytes on macOS) = 95,469,568 B = 91.0 MiB ≪ 512 MB; sample sizes are fixed (26-slot prototype).
- Refinement: lapse checks refined once (2-ring → 4-ring); deterministic seed 151.

## 6. Lean certificates (verified, hard bar met)

Compiled with `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` (exit 0, both files). **Zero sorry; `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}** for every theorem:

- `AS151_adm_trace_inversion.lean`: `T_S_identity`, `S_T_identity` (A ≠ 0), `T_one_S_one_identity`, `S_one_T_one_identity`, `trm_T` (tr(T_A K) = −2A·tr K). Axioms: {propext, Classical.choice, Quot.sound}.
- `AS151_two_cell_mean_kernel.lean`: `two_cell_mean_kernel` (h1 ∧ h2 ⇒ K1 = K2 = 0 for A>0, B≥0, N1,N2>0), `mean_det_pos`. Axioms: {propext, Classical.choice, Quot.sound}.

Compile host only; no files written into `fable_independent_2026/lean_2026/`.

## 7. Classification, limitations, next implication

- **Classification: derived** for the bounded prototype domain (24/24 checks PASS with residuals above; the lapse identity is exact in the continuum, its lattice residual is exactly the predicted Leibniz defect and decays under refinement). Not promoted to complete gravity closure.
- **Limitations**: (i) prototype = 2 cells × 2 slices; (ii) identity-metric frame for the kinetic algebra (general-metric fiber checks numeric, not symbolic); (iii) the lattice Leibniz defect is O(h²) — continuum statements rely on the analytic identities, not the lattice residuals; (iv) the shift/u sector in the prototype is a 2-dim slice of the full spatial shift; (v) no claim about secondary constraints or Dirac–Bergmann propagation beyond the primary list.
- **Next unresolved implication**: the exact primary-constraint list of the localized action **in the continuum on a general compact leaf** — needs (i) the lift of the ring operator calculus (product rule, D ln N = DN/N) to the global heat operator on W over [0,b], and (ii) the global function-space statement of the heat-elimination identities (a)-(e). The lattice evidence here bounds the discrete version only.
- **Suggested follow-up / child (proposed, NOT dispatched)**: **AS151.C01** — "Global primary-constraint list on a general compact leaf": prove the list of §3 with the heat-elimination identities in global Sobolev spaces, using the Lean-certified fiber kernels; dependency: this run (parent); branch CA5-GNC-R; new target: continuum analogue of (12) with the global heat operator; controls: substitute-back of the projected Z-equation (R4) and the negative control of §4 in the continuum. Per the branching protocol, the child must be dispatched by an actual worker; no dispatch was performed here.