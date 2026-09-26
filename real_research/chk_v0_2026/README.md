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
| CV2 | the covariant action; its NR limit = CV1; L340's static block (iii); FRW with the leaf average | next |
| CV3 | the gate as a varied action term (the dark-energy thread's piece); L361's EL equations with f varied (ii) | awaiting the gate functional |

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
