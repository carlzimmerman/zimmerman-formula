# chk_v0_2026 — V0, the one covariant action for the C-H/K branch

On 2026-09-26 the author decided to run two branches, never pooled (recipe, second user-decision block). One is the C-H/K
branch: the C-H/K khronon with the leaf average, the vacuum gate and the region kernel, with kernel ν_mono and
causality criterion B. The other is the lead track's IC28 sector.

The C-H/K branch had no single action. Its pieces were separate constructions on different chassis:
- C-H (ACTION.md);
- L340's BPS terms;
- L350's leaf average;
- L353's kernel-invisible pair;
- L361's region kernel;
- the vacuum gate (L359, and the lead track's C^∞ W(t)).

The cross-thread review (`real_research/cross_thread_review_2026_09_26/`, XR3 calc 1) lists V0 as orphaned and sets its
pass criteria:
1. Zero symbolic residual for three reductions:
   - (i) the operative requirement-1 equations on gate-on plateaus;
   - (ii) L361's Euler–Lagrange equations with f varied;
   - (iii) L340's static block.
2. The source/force operator named.
3. The homogeneous zero shown to lie on the off-plateau.

This directory builds V0 one step at a time. Each lane has a MUTATE control and a Lean certificate of its algebra in
`fable_independent_2026/lean_2026/CV*_*.lean`.

| Lane | Content | Status |
|---|---|---|
| CV1 | the non-relativistic action V0 must reduce to; reductions (i) and (ii) at f prescribed; C7 named; the off-plateau | **6/6** (MUTATE rc = 1); Lean 8 thm |
| CV2 | the covariant action; its NR limit = CV1; L340's static block (iii); FRW with the leaf average | **4/4** (MUTATE rc = 1); Lean 5 thm |
| CV3 | the gate as a varied action term: what it may read; reduction (ii) with f varied | **7/7** (MUTATE rc = 1); Lean 4 thm |
| CV4 | the khronon's K around bound regions (the K-only gate door) | **3/3** (MUTATE rc = 1) |

## CV1 — the non-relativistic action on C-H's chassis (6/6; MUTATE ungated source fails A3, rc = 1)

`CV1_nr_assembly.py` (+ `.out`, `_MUTATE.out`, results JSON; about 12 s). Lean:
`CV1_gate_offplateau_certificates.lean` (8 theorems, zero `sorry`, standard axioms).

**The Lagrangian.** S is C-H's heat filter, M² = m²(1 − f), q′(Z) = ν_mono(√Z) − 1, and f is the gate:

    L = −(ρ_b + ρ_d)Φ − [2∇Φ·∇u − |∇u|²]/(8πG)                 C-H's chassis
        + a₀² f q(|∇Sw|²/a₀²)/(8πG)                              the region kernel
        + Ψ[(∇² − M²)w − f∇²(u − v)]/(8πG)                       the region field
        + λ[∇²v − 4πG(ρ_d − ⟨ρ_d⟩)]/(8πG)                        L353's pair, projected source
        − σ M² w²/(8πG)                                          L361's web self-term

Baryons couple only to the metric potential Φ (requirement 11). The dark component couples to Φ and, through L353's
pair, to λ.

- **A1, the field equations** (sympy, residual 0):
  - the kernel reads w, with (∇² − M²)w = 4πG f(ρ_b − ⟨ρ_b⟩): the gate-weighted baryon field, screened in the web;
  - baryons feel Φ = u + fP, where P = Ψ/2 is the gated phantom;
  - the dark component feels u, Newtonian only. This is L353's reciprocity carried over to the region kernel.
- **A2, reduction (i):** on a gate-on plateau these are the operative requirement-1 equations exactly.
- **A3, reduction (ii) at prescribed f:** at σ = 1, CV1's solution solves L361's committed Euler–Lagrange equations with
  zero residual (φ = u, χ = w, ψ = P + w), and each species feels the same potential.
  - L361 is therefore CV1 at σ = 1, now with minimally coupled baryons.
  - Its self-term is one explicit web mass term. σ = 0 differs by exactly M²w in the phantom's equation.
- **A4, the filter:** the discrete action's gradient matches the stated equations to 4×10⁻¹⁰, with the kernel's force
  entering as Sᵀ div[f(ν − 1)∇Sw]. A wrong adjoint is detected.
- **A5, C7 named.**
  - V0's operator restricts the source to the gate-weighted baryons, screens it in the web, and weights the response
    by f. The PM runs instead mask the response of the all-baryon field; XR5 measured that difference at static scope.
  - In a spherical region:
    - inside the plateau the baryon force is ν_mono(g_N/a₀)g_N to 1×10⁻⁴;
    - beyond the transition it is exactly Newtonian;
    - σ acts only inside the transition layer.
  - **But σ is not negligible there.** It moves the baryon force by 1.4 g_N at 1/m = 100 kpc and 0.8 g_N at 500 kpc, a
    sizeable fraction of the deep-MOND phantom. σ is a physical edge choice. V0 declares σ = 1, the record's
    construction, and edge-sensitive observables (L352's compensated lensing) must say which σ they assume.
- **A6, the homogeneous zero is off-plateau.**
  - The gate W and all its derivatives vanish at t → 0⁺, and W = 0 for t ≤ 0.
  - On flat FRW the curvature variable is 0, so f, its source and the phantom are absent from the background and from
    its perturbation theory to every order. XC5 E6's √ε response never arises there.
  - Lean certifies this to every order (`gate_flat_at_homogeneous`, via Mathlib's `Real.smoothTransition`).
  - This is shown for the curvature-based gate variable. Under the "all doors" decision, each other gate variable must
    show its own homogeneous background is off-plateau.

**Scope.** Non-relativistic, with f prescribed. On a closed leaf the Poisson sources carry the leaf mean, so the kernel's
source is the gated baryon contrast; for an isolated system that equals L361's fρ_b.

**The record's σ is inconsistent, and this has to be declared per result.** From the L361/L353 owner's review of CV1
and a check of L370:
- L361's action (R0) is σ = 1: χ is screened with the same M² as w, so that χ = w everywhere.
- No KiDS score on the record includes the σ = 1 layer:
  - L352, L360 and AT3 (through L360's fit_comb) use L352's hard-edge, Gauss-compensated profile, which is σ = 0 in
    the Dirichlet limit;
  - L361's R3 has no edge at all (isolated QUMOND with the transmitted EFE).
- L370's `phantom_felt` (Harvey, inherited by AT3) is also σ = 0: a hard region mask, the region's source unscreened
  and the response masked.
- The σ = 1 layer's lensing, a finite shell in the Dirichlet limit, is unscored.

## CV2 — the covariant action and three reductions (4/4; MUTATE without the leaf average fails B3, rc = 1)

`CV2_covariant_action.py` (+ `.out`, `_MUTATE.out`, results JSON; seconds). Lean:
`CV2_covariant_reduction_certificates.lean` (5 theorems, zero `sorry`, standard axioms).

    I_V0 = c³/(16πG) ∫ d⁴x √−g { R − 2Λ + 2h^{μν}(D_μU − a_μ)(D_νU − a_ν)
             + α_c a_μa^μ − c₂(K − ⟨K⟩_h)²
             + 2α² f q(h^{μν}D_μW_b D_νW_b/α²) + ∫₀^b dz L(∂_zW − Δ_hW) + λ₀(W₀ − Y)
             + 2Ψ[(Δ_h − m²(1 − f))Y − fΔ_h(U − V)] − 2σm²(1 − f)Y²
             + 2Λ_d[Δ_hV − (4πG/c⁴)(ε_d − ⟨ε_d⟩_h)] } + GHY + S_matter[g] + S_dark[g; dark state]

Here ε_d = n_μn_νT_d^{μν}. The gate f is a prescribed function of the leaf geometry (R^(3) + σ_ijσ^ij, K). Every
added field (Y, Ψ, V, Λ_d) is a leafwise auxiliary, like C-H's W, L and λ₀.

- **B1, the non-relativistic limit.** The leaf curvature of the conformally flat leaf, computed from Christoffel
  symbols, gives N√h R^(3) = e^{φ−ψ}(2|∇ψ|² − 4∇φ·∇ψ) + a divergence. The ψ equation gives ψ = Φ, so lensing equals
  dynamics for both species. At leading order the action is CV1's Lagrangian exactly, every factor of c included.
  Reductions (i) and (ii) at prescribed f therefore carry over from CV1.
- **B2, reduction (iii).**
  - On a gate-on plateau, where f = 1 with every derivative zero (Lean CV1 `gate_flat_above_one`), the constraint
    Δ_h(Y − U) = 0 gives Y = U + const for every leaf metric (Lean `periodic_laplacian_kernel_const`, a discrete
    analogue). So V0 is C-H/K there.
  - On L340's own block (its E-list copied verbatim) the exact elimination of (Y, Ψ) returns L340's 4×4 matrix and
    source. The determinant picks up only −4k⁴, independent of ω. The ω → 0 limit is L340's static MOND solution, with no
    frozen mode.
- **B3, FRW.**
  - With the gate off, the auxiliaries vanish consistently and exert no force. α_c a² = 0, and the leaf-averaged
    λ-term is identically zero, so the Friedmann equation is GR's: G_cos = G (Lean `frw_leaf_average`).
  - The control, the plain −c₂K², gives H²(1 + 3c₂/2) (L350 G1; Lean `frw_plain_c2`).
  - This settles the background only. k ≠ 0 perturbations still carry c₂ (XR3 item 7's recheck).
- **B4, the dark source.** On a closed leaf, Δ_hV = (4πG/c⁴)(ε_d − ⟨ε_d⟩) is solvable for a positive density (residual
  6×10⁻¹⁴). The unprojected source is not, because its zero mode is nonzero.

**Open after CV2, in order:**
- CV3, the gate varied as an action term (B δf with δf = f_R δR + f_K δK), which needs the dark-energy thread's gate
  functional and normalisation;
- the σ = 1 layer's lensing;
- the Dirac count (XR3 calc 2);
- the dark state at action level under criterion B (XR3 calc 7). A multistreaming state made of the clock's own dust
  would fold the foliation.

## CV4 — the khronon's K around a bound region: the K-only gate is blind (3/3; MUTATE c₂ = 0 fails K1, rc = 1)

`CV4_khronon_K_profile.py` (+ `.out`, `_MUTATE.out`, results JSON; about a second). Two peer sessions asked for this. The
dark-energy thread's DE7 (095ab610a) found that a gate on the leaf curvature carries slip and needs a repair that is
itself slip. Its escape was a gate on the khronon's K alone, f(Ω_Λ(K)), which works only if K separates bound regions from
the Hubble flow.

- **K1, the static equation.** Varying τ in −c₂∫√−g(K − ⟨K⟩)² gives c₂∇²(δK) = 0 on each leaf. The leaf average only adds
  a leaf constant. The linear K of the foliation τ = t + π on perturbed FRW is 3H(1 − Φ) − 3Ψ_t − ∇²π/a², derived from the
  definition. So in a quasi-static region K is harmonic and equals its Hubble-flow value 3H(z): the khronon's tilt absorbs
  the matter's non-expansion, and its leaves are constant-mean-curvature. α_c enters only through time derivatives, and
  the MOND sector has no O(π) term on a static background (XC3 C1).
- **K2, moving sources.** L340's own block gives δK = 0 exactly at ω = 0. At first order in ω = v·k it gives
  δK = ω G₁ ψ_N, with G₁ = 2i(Cα_c + 2C + α_c)/[c₂(Cα_c + α_c − 2)], about −2iC/c₂ (a dipole in the direction of motion).
- **K3, the numbers** at the linear gate's edge (p = 1, x_c0 = 2.5), for L340's window corners, both α_c ends and
  c₂ = 7.3×10⁻³ and 0.067:

  | System | Speed | z | Edge radius | Largest \|K/3H − 1\| |
  |---|---|---|---|---|
  | 10¹¹ M☉ galaxy | 600 km/s | 0.25 | 1.35 Mpc | 2×10⁻⁴ |
  | 10¹¹ M☉ galaxy | 600 km/s | 2.5 | 124 kpc | 6.5×10⁻⁴ |
  | 10¹⁴ M☉ cluster | 1000 km/s | 0.25 | 7.6 Mpc | 1.9×10⁻³ |
  | 10¹⁴ M☉ cluster | 1000 km/s | 2.5 | 0.70 Mpc | 4.8×10⁻³ |

  α_c changes these by ≤ 2×10⁻⁷.

**So K does not separate bound regions from the Hubble flow.** A K-only gate is blind in L340's window. The door would need
the non-perturbative branch in which halo leaves are maximal (K ≈ 0), and that has no source in the linear khronon
equation. DE1's assumption that K = 3H at the galaxy stands.

## CV3 — the gate varied: what it may read, and V0's default gate (7/7; MUTATE carrier-reading fails G1, rc = 1)

`CV3_gate_varied.py` (+ `.out`, `_MUTATE.out`, results JSON; about 3 min). Lean: `CV3_gate_rule_certificates.lean`
(4 theorems, zero `sorry`, standard axioms). The Euler–Lagrange equations are derived symbolically for a generic gate W
and generic fields. The identities among them are then checked by substituting concrete smooth fields, constants and
gate shapes and evaluating at three points to 40 digits; the residuals are 10⁻¹⁷².

**The rule.** V0's static action has three multiplier–field pairs, (Φ, u), (Ψ, w) and (λ, v), and each multiplier enters
linearly.
- A gate that reads only the constrained fields u, v and w leaves every multiplier's diagonal block zero. The
  constraint Hessian's determinant is then a²b² for every gate shape (Lean `multiplier_rule_four`).
- A gate that reads a multiplier makes that determinant gate-dependent, and DE7's T1 (W″ takes both signs) then puts a
  zero on every transition.

- **G1, readings A+ and A.**
  - A+ reads C[∇²(u − v) + ∇·((ν − 1)∇Sw)], baryons plus their phantom built from the constrained fields.
  - A reads C∇²(u − v), baryons only.
  - Both keep u, v and w constrained and give no slip (ψ = Φ). The gate's parts of the u- and v-equations cancel in the
    dark component's potential, so there is no leak (Lean `carrier_blind`). The check is not vacuous: the gate's own
    part is 0.035.
  - Reading A's gate force on Φ is −4πG C B W′.
- **G2, reading B, MS1's ∇²(Φ − v).** It is leak-free too (MS1's A3 reproduced). But it reads the multiplier Φ, so u is
  no longer constrained: ∇²u = 4πGρ − 4πG C ∇²(BW′).
- **G3, the rule, symbolically.** Reading B's (Φ, u) symbol vanishes at k² = 1/(4πG C² B W″) (Lean `reading_B_singular`).
- **G3b, reading B's global operator.** On a real transition (linear gate, w = 0.25, a 10¹¹ M☉ galaxy) an eigenvalue
  crosses zero once as z runs from 0.25 to 4, the same on 500- and 1000-point grids. At that epoch the lapse's response
  to a generic density source diverges. Reading A's operator never crosses. At generic epochs both operators are
  invertible.
- **G4, reading A+'s cost.** The gate's second variation acts on the matter density only:
  δΦ_g = −(4πG)²C²BW″δρ. That is a local pressure of either sign, so stability needs σ_v² > c_g² where W″ > 0.
  At a 10¹¹ M☉ edge with w = 0.25 (the width DE9's window needs at x_c0 = 2.5):

  | z | c_g | σ_v²/c_g² at 200 km/s | at 10 km/s |
  |---|---|---|---|
  | 0.25 | 91 km/s | 4.8 | 0.012 |
  | 2.5 | 302 km/s | 0.44 | 0.001 |
  | 4 | 507 km/s | 0.16 | 0.0004 |

  **This is a new pincer.** The window wants a narrow gate, but c_g ∝ 1/w, so matter stability wants a wide one. It is
  a one-edge estimate; the dark-energy thread computes the margins on DE7's real transitions.
- **G5, reduction (ii) with f varied.** On both plateaus W is constant, every gate term vanishes, and V0's equations are
  CV1's, which are L361's at σ = 1, exactly.
- **G6, MS3's cap inside the gate.** Two concrete cap-like gates built from the constrained fields, one of them
  U/(1 + v_loc²-like), keep everything above. G3's rule covers every such gate.

**V0's default gate is reading A+.** It is leak-free and slip-free, keeps every constraint invertible, and holds the cap.
Its open cost is the matter-sector condition of G4. The curvature reading (DE7 slip + repair, MS1 leak), the K reading
(CV4, blind) and reading B (G2–G3b, singular epochs) are recorded as labelled alternatives.
