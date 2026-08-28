# FINAL_THEORY — The Winning Frozen Action (Architecture A) and Why It Won

**Adjudication date:** 2026-08-28
**Program:** relativistic-MOND closure, four-architecture adversarial filter (A/B/C/D).
**Winner:** A = AeST (Skordis–Zlosnik) + frozen J_10 in the F(Y,Q) Y-sector.
**Status of winner:** CONDITIONALLY-VIABLE (survives the whole Tier-1 filter that kills the other three; blocked from closure by genuine unresolved consistency conditions — see §4).
**Overall program verdict:** INCONCLUSIVE. Not CLOSED, not BURNED, not a whole-program NO-GO. See FINAL_CLOSURE_REPORT.md §7.

All certificates cited below were re-run THIS session (exit 0). Nothing is asserted; every load-bearing
line traces to a runnable script printing a sympy `simplify(...)==0` or a numerical residual.

---

## 1. The frozen winning action

The winner is the Aether-Scalar-Tensor host (Skordis–Zlosnik 2021, PRD 106.104041; 6 physical DOF general-F
theorem PRD 110.044015 / 2307.15126) with the MOND sector supplied by the **single frozen constitutive
function** built from the frozen kernel `mu_10`.

**Metric + unit-timelike aether A^μ (A_μ A^μ = −1) + scalar φ; matter minimally coupled to g_μν:**

```
S = (c^4 / 16πG) ∫ d^4x √(−g) [ R − (K_B/2) F_{μν}F^{μν} + 2(2 − K_B) J^μ ∂_μ φ − (2 − K_B) Y
                                 + F(Y, Q) ]  +  S_matter[g_μν, ψ]

    F_{μν} = 2 ∂_[μ A_ν]                       (aether field strength)
    J^μ    = A^ν ∇_ν A^μ                         (aether "acceleration")
    Q      = A^μ ∂_μ φ                            (shift-charge invariant; carries the dark sector / w→−1)
    Y      = (g^{μν} + A^μ A^ν) ∂_μ φ ∂_ν φ       (spatial-gradient invariant; carries MOND)

    FROZEN MOND SECTOR:   F(Y,Q) ⊃ F_M = a0^2 J_10( √Y / a0 ),
      J_10 fixed by the frozen kernel mu_10(y)=y/(1+y^10)^(1/10):
      deep-MOND  F_M → (2/(3 a0)) Y^{3/2} + …   (so δ^2 F_M = 0 at quadratic order — kernel invisible there)
    Q-SECTOR:   F(Y,Q) ⊃ K(Q)  with K_QQ = 2K2 ≠ 0  (dark-energy / dS sector, w→−1 at the minimum)
```

Free parameters: `K_B` (aether kinetic, → PPN α_1 = −4K_B, LLR bound K_B < 2.5e-5), `K2 = ½K_QQ`
(scalar stiffness), `a0` (MOND scale, **INPUT** — `a0^2 = κ^2 c^2 G ρ_Λ` and `a0(z) ~ √ρ_DE` are
TARGET/phenomenological, never derived; κ=½, Z≈21 are FITTED). `Λ = 32π a0^2/c^4` is a MODEL-ASSUMPTION.

**What is genuinely new vs. bare AeST:** the MOND constitutive function is *frozen* to J_10 (sharp μ_10,
n=10), not left free. The certificate `fc_A_certificate.py` (CERT2, this session, exit 0) proves
`δ^2 S_MOND = 0` for an **arbitrary** admissible prefactor J — so the freeze changes the deep-MOND/lensing
phenomenology (where it acts) but is provably **inert** at quadratic order (where the theory is fragile).

---

## 2. Why A beat B, C, D — the elimination order

Hard-gate order; eliminate on the earliest irreparable structural fail. Full table in FINAL_CLOSURE_REPORT.md.

| Arch | Host | Died at | Cause | Certificate (re-run this session) |
|------|------|---------|-------|-----------------------------------|
| **A** | AeST, 6 DOF, diff-covariant | — (survives) | — | clears Tier 1; c_T=1, γ_PPN=1, KiDS χ²/dof=0.64 |
| **B** | constraint-first MMG, 2 DOF | Tier 1 / Tier 6 | CONSTRAINT-ARCHITECTURE | `gate_lensing_weakfield_derivation.py` γ_PPN=0 ~20σ; `ppn_mmg_gate_2026.py` α_3=−1; `gate_matter_conservation_derivation.py` Newtonian-order non-conservation |
| **C** | Laplacian-auxiliary MMG | Tier 1 / Tier 6 | CONSTRAINT-ARCHITECTURE | same kills + `fc_C_laplacian_orthogonality_certificate.py`: the D² completion is Fourier-orthogonal to the Φ-sourcing sector ⇒ cannot repair B |
| **D** | BIMOND + DBI/khronon | Tier 1 | HOST | `route6_bimond_twin_2026.py` 30/30: sum-rule F_b+F_TM=1≠2 ⇒ twin sector cannot carry Ω_dm; DOF/c_T largely OPEN-adverse |

A is the **only** architecture that clears Tier 1 (well-posedness + healthy DOF + no ghost + Legendre).
It then survives Tier 3 (c_T=1 exact, GW170817), the derived parts of Tier 4 (γ_PPN=1), and Tier 6
(Φ=Ψ non-spherical, M24 KiDS χ²/dof=0.64). B, C, D never reach Tier 3 with a viable weak-field limit.

---

## 3. The structural no-go that eliminated the constraint-first branch (B and C)

**THEOREM (H_perp-deletion unsources Φ).** Proven in `fc_no_go_Hperp_unsources_Phi.py` (12/12, exit 0,
re-run this session), four independent sympy legs.

> Any spatially-covariant, constraint-first theory that reaches N_grav = 2 by **removing the Hamiltonian
> constraint H_perp** and imposing in its place a **source-free elliptic constraint** on the conformal
> spatial factor q = −(1/6) ln det γ (schematically `D² q ≈ 0`, or `D²(q + f[N]) ≈ 0`, with **no matter
> density on the RHS**) forces, in the static weak-field limit with decaying boundary conditions,
> **q ≡ 0 ⇒ Φ ≡ 0 ⇒ γ_PPN = Φ/Ψ = 0**, with light seeing exactly **half** the dynamical potential.

Four legs:
1. GR baseline: q = Φ at linear order; H_perp carries ρ onto Φ (Φ̂ = 4πGρ/k²) ⇒ γ_PPN = 1.
2. Source-free replacement −k² q̂ = 0 ⇒ q̂(k≠0)=0 ⇒ Φ=0 ⇒ γ_PPN=0.
3. **KERNEL-BLIND:** μ(y) enters ONLY the lapse/AQUAL constraint C_M (the Ψ sector); the q-constraint
   S_2 = D²q is the flat Laplacian, dS_2/dμ ≡ 0. Swapping μ_exp → μ_10 leaves γ_PPN=0 invariant
   (repo cert < 1e-19 for μ_5, μ_10). Classification: **CONSTRAINT-ARCHITECTURE, not KERNEL.**
4. **LAPLACIAN-BLIND:** faking a smooth k≠0 curvature source needs multiplier λ̂ = −S0/k² — a 1/k² pole
   singular at k=0 — so the D²-completion (architecture C) is Fourier-orthogonal to the Φ-sourcing
   equation and cannot restore Φ (`fc_C_laplacian_orthogonality_certificate.py`, exit 0).

**Scope.** UNCONDITIONAL for the source-free 2-DOF class; B and C are instances, eliminated at Tier 1/Tier 6
(M24 KiDS Δχ²=+403…+498 ~20σ; Cassini γ−1=−1 ⇒ 43,479σ, `gate_lensing_weakfield_derivation.py` this session).
It is a **sharp obstruction with a named escape** for the general 2-DOF class: the only escape is a
ρ-sourced constraint `D²q ≈ +4πGρ` — but that IS H_perp's Poisson-for-curvature content reintroduced,
which brackets second-class with π_N differently and demands a full Dirac re-certification of the
20−12−4=4⇒2 count. **No such certified architecture exists in the committed record.**

You may have {2 DOF via a source-free q-constraint} **OR** {γ_PPN = 1}, **not both.**

**Why A is immune.** A is diffeomorphism-covariant, **retains H_perp** among its four first-class
constraints (so Φ is sourced and Φ=Ψ is derived), and pays for it with **6 (+1) DOF instead of 2**.
A never enters the no-go's hypothesis. The price A pays for keeping H_perp is exactly the fragility of
§4 (the extra propagating scalar whose IR sign is the decisive open).

---

## 4. Why the winner is CONDITIONALLY-VIABLE, not CLOSED

Three surviving liabilities, ALL classified **HOST** (AeST's own {K_B, K(Q), μ} sector), **none KERNEL**
(J_10 is provably inert at quadratic order, CERT2). Each is a genuine *consistency condition*, not a
phenomenological input — which is why the program verdict is INCONCLUSIVE and **not** CONDITIONALLY-CLOSED.

1. **Gate 14 — FLRW IR-sign (DECISIVE, partially rescued, still OPEN).**
   AeST's known low-k unbounded-Hamiltonian scalar mode (arXiv 2109.13287, EXTERNAL): Hamiltonian unbounded
   below for k < k_*, k_*² = (1+λ_s)/λ_s · μ², μ² = 2K2 Q0²/(2−K_B). The closure lane
   (`fc_flrw_ir_sign_certificate.py`, 20/20, exit 0) proved the **k→0 limit is RESCUED** on the de Sitter
   attractor: shift symmetry makes k→0 an exact flat direction, the background Q0(a)=q_m−C/a³ attracts to dS,
   and on dS the a³ measure + 3H friction give χ̇ ~ a⁻³, χ→finite const (bounded), energy ~ a⁻³ → 0.
   **But the finite-k band H ≪ k_phys < k_* (wavelengths ≳ μ⁻¹ ≳ ~1 Mpc) remains OPEN** — the single
   dichotomy (nondynamical/constraint ⇒ full rescue ⇒ PASS) vs (dynamical, ω²<0, |ω|~k_phys≫H ⇒ Mpc-scale
   runaway ⇒ FAIL) is UNCOMPUTED. Proven kernel-blind (δ²J_10=0) ⇒ property of the AeST host alone.

2. **Gate 10 — PPN α_2 (uncomputed, adverse-leaning).** THEOREM (`fc_ctensor_map_2026.py`, exit 0): the
   certified AeST→Einstein-aether c-tensor map (c1,c2,c3,c4)=(K_B,0,−K_B,0) gives c13=0 ⇒ c_T²=1 and
   **α_1 = −4K_B (DERIVED)**; but the pure-vector EA α_2 ~ 1/c123 is **singular** (c123=c2=0, residue≠0),
   so the scalar φ (F_QQ=2K2) MUST regularise it to a **finite** α_2(K_B,K2,Q0). The coefficient is
   **uncomputed**: the direct O(w²) machine (`fc_alpha2_preferred_frame_2026.py`) reproduces γ_PPN=1 and the
   static sector but **fails its own internal PPN consistency** (D1/D2 FAIL under the isotropic-metric
   ansatz — anisotropic aether stress at O(w²) requires the generic-metric solve). α_2 is finite-but-open;
   adverse IF α_2 ~ K_B/2 (would force K_B < 4e-8), a magnitude NOT established.

3. **Gate 5 — superluminal quasi-static scalar characteristic.** c_s² ∝ 1/K_B → ~3c at the α_1/LLR K_B
   ceiling (fc8 RESULTS.md Gate H). Real characteristic set by K2, kernel-independent (δ²J_10=0). Not
   auto-excluded (AeST has a preferred foliation) but needs a **DERIVED** global-time causal-structure
   argument, not asserted. HOST (K2/aether).

Plus one benign completeness item: the **all-branches covariant Legendre/Dirac regularity theorem**
(physical Hessian H_phys(Y=0)=2(2−K_B)I>0 already shown at the Y=0 auxiliary chart, `y0_physical_hessian.py`;
the formal all-branch covariant proof on the singular boundary is OPEN, referee-vulnerable but not a known
pathology).

Because the decisive liability (Gate 14 finite-k) can still go either way, **turning it into a PASS would
violate the honesty rules.** A is structurally alive and the smallest surviving candidate — but it is not a
watertight theorem. Verdict: **INCONCLUSIVE**, with A the unique conditionally-viable survivor and the
constraint-first branch eliminated by a proven structural no-go.
