# FC-8R — FROZEN CANDIDATE (Reduced Potential-Locked AeST, 2026-08-28)

**This directory is a closure lane, not a construction lane.** FC-8R is frozen. The task is to derive its
field equations and run falsification gates until each returns **PASS / FAIL / OPEN** — nothing else. Do
**not** improve the theory here. See `REQUIREMENTS.md`. This does **not** supersede the MMG closure in
`../closure_2026/` (a separate result with its own conditional status).

---

## The frozen action (auxiliary fields eliminated exactly)

FC-8R is the exact reduction of FC-8: the lock `α²=κ²GV(χ)` is solved and substituted. Because
`V(χ)=V₀+½m_χ²(χ−χ₀)² > 0` everywhere (V₀>0, m_χ²≥0), `α(χ)=κ√(GV(χ))` is globally single-valued and the
elimination is exact (α,ζ are non-dynamical ⇒ no boundary terms). **Fundamental fields: `g_{μν}, A_μ, φ, χ`.
No fundamental α. No fundamental ζ.**

$$
\boxed{\,S_{\rm FC8R}=S_{\rm AeST}^{\star}+S_m[g,\psi]-\int d^4x\sqrt{-g}\Big[\tfrac12(\nabla\chi)^2+V(\chi)\Big]+S_{\rm MOND}^{R}\,}
$$

**Gravity/aether-scalar sector** (established AeST chassis, nonlinear 6-DOF baseline, PRD 110.044015):

$$
S_{\rm AeST}^{\star}=\frac{c^3}{16\pi\tilde G}\int d^4x\sqrt{-g}\Big[
R-\tfrac{K_B}{2}F_{\mu\nu}F^{\mu\nu}+2(2-K_B)J^\mu\nabla_\mu\phi-(2-K_B)Y-K(Q)-\lambda(A_\mu A^\mu+1)\Big]
$$

`Q=A^μ∇_μφ`, `Y=(g^{μν}+A^μA^ν)∇_μφ∇_νφ`, `F_{μν}=2∇_[μA_ν]`, `J^μ=A^ν∇_νA^μ`; **frozen AeST Q-sector**
`K(Q)=−2Λ+𝒦₂(Q−Q₀)²` (SZ21 quadratic, 𝒦₂>0).

**The reduced MOND sector (the only new interaction):**

$$
\boxed{\,S_{\rm MOND}^{R}=-\frac{c^3}{16\pi\tilde G}\int d^4x\sqrt{-g}\;\mathcal A(\chi)\,J_{10}\!\Big(\frac{\sqrt Y}{\sqrt{\mathcal A(\chi)}}\Big)\,},\qquad
\boxed{\,\mathcal A(\chi)=\kappa^2 G\,V(\chi)=a_0(\chi)^2\,}
$$

**MOND interpolation (frozen — sharp, Cassini-safe n=10):**

$$
\boxed{\,\mu_{10}(y)=\frac{y}{(1+y^{10})^{1/10}}\,}\quad
\boxed{\,x=\frac y2\big(2-\mu_{10}(y)\big)\,}\quad
\boxed{\,J_{10}'(x)=2x\,\frac{\mu_{10}(y(x))}{2-\mu_{10}(y(x))}\,}
$$

(bridge `x=g_φ/a₀`, committed `fc_aest_kernel_bridge.py`; `(2−μ₁₀)` is correct, an earlier `(1+μ₁₀)` was a typo.)

**Cosmological scalar (canonical, ordinary dynamical field):**

$$
S_\chi=-\int d^4x\sqrt{-g}\Big[\tfrac12\nabla_\mu\chi\nabla^\mu\chi+V(\chi)\Big],\qquad
\boxed{\,V(\chi)=V_0+\tfrac12 m_\chi^2(\chi-\chi_0)^2\,},\ V_0>0
$$

**The locked MOND scale (encoded directly, not a field):**

$$
\boxed{\,a_0(\chi)^2=\kappa^2 G\,V(\chi)\,}\ \Rightarrow\ a_{0,0}^2=\kappa^2 G V_0\ \text{at }\chi=\chi_0;\qquad
\frac{\dot a_0}{a_0}=\frac12\frac{V'(\chi)\dot\chi}{V(\chi)}
$$

**Matter:** `S_m[g_{μν},ψ]` — universal metric coupling (photons and matter see the same `g_{μν}`).

**Frozen parameters:** `{K_B, 𝒦₂, Q_0, Λ, V_0, m_χ, χ_0, κ}` (AeST scalar mass `μ` fixed by 𝒦₂,Q₀; the
`μ⁻¹≳Mpc` health condition is to be *tested*, not tuned away).

---

## What is already established (inputs, re-checked by `fc8_symbolic_audit.py` — NOT the closure)

From committed `../closure_2026/FC_AEST/` (`fc8_clean_lock_2026.py`, `fc7_groundstate_closure_2026.py`,
`fc7_reduced_action_rank_2026.py`, all exit 0):

- `μ_10(y)=y+O(y¹¹)` ⇒ `J_10(x)=x³/3+O(x¹³)` ⇒ `L_MOND^R=O(Y^{3/2})=O(δ³)` ⇒ **δ²S_MOND^R=0** on `Y=0,χ=χ₀`.
- `𝒜(χ)=κ²GV(χ)` depends on **χ, not χ̇, and has no ∇χ** ⇒ `L_MOND^R` contributes **identically zero to
  every kinetic entry AND the χ gradient entry, at all orders** ⇒ velocity Hessian block-diagonal, `K_χ=+1`.
- The aether-orthogonal projector `(g^{μν}+A^μA^ν)` removes φ̇ from `Y` exactly ⇒ MOND term adds no φ–χ mixing.
- Constant-a₀ vacuum `a_{0,0}²=κ²GV₀`; BTFR `v⁴=Ga₀M_b`; ground-state DOF `6+1=7` (LOCAL only).
- Solar System: `1−μ_10=O((a₀/g)¹⁰)` ⇒ MOND operator vanishes ultra-fast at high g ⇒ PPN ≈ AeST baseline.

## The intentional cosmological prediction (to be tested, NOT assumed healthy)

`a₀²=κ²GV(χ)` ⇒ `a₀²∝ρ_χ` only when **potential-dominated** (χ̇²≪V); during kination `a₀²≁ρ_χ`. The FLRW
gate must answer: **does the cosmological solution stay potential-dominated enough for a₀(z) to behave
acceptably?** This is where FC-8R becomes an interesting cosmology or gets killed.

---

## DO NOT (during the closure run)

```
DO NOT re-introduce alpha/zeta, or replace a0^2=kappa^2 G V(chi) with a0^2=kappa^2 G rho_chi.
DO NOT replace mu_10.        DO NOT introduce a new MOND field.
DO NOT modify the matter coupling.   DO NOT add a hand-tuned PPN counterterm.
DO NOT select boundary conditions solely to remove a pathology.
DO NOT inherit a PASS from ordinary AeST.
DO NOT import Einstein-aether PPN formulas without deriving the FC-8R -> EA parameter map.
DO NOT convert OPEN into PASS.
```
