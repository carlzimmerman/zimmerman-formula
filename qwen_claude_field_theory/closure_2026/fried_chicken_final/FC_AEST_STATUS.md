# FC-FINAL — session capstone: the constraint-first no-go + AeST+J₁₀ conditional closure (2026-08-28)

**Frozen candidate under test:** FC-AeST = AeST (Skordis–Złośnik, 6 physical DOF) + `𝓕(Y,Q)=𝓕_Q★(Q)+a₀²J₁₀(√Y/a₀)`,
`μ₁₀(y)=y/(1+y¹⁰)^{1/10}`, **a₀ constant**. Matter minimally coupled to the single metric g. All verdicts below are backed
by committed, re-run scripts in `fried_chicken_final/` (and subdirs) unless marked EXTERNAL-INPUT.

---

## Part I — The constraint-first 2-DOF program is closed on the lensing axis (scoped no-go, verified)

Every attempt to realize relativistic MOND with only **2 gravitational DOF** (a constraint-first / MMG chassis) fails to lens,
by a single unified mechanism (`fc_isotropic_legendre/`, `fc_final_4ac/`, `fc_no_go_Hperp_unsources_Phi.py`; 37/37 + 28/28 + 14/14 + 12/12, all exit 0):

> **THEOREM (scoped).** An isotropic MOND law couples to the metric only through `s=√(γ^ij D_iq D_jq)`, so the *same* constitutive
> object `μ=J'/s` controls both the AQUAL Gauss law and the on-shell traceless metric stress `Σ_P`. Both exhaustive local classes
> force `Σ_P≠0`: covariant/QUMOND carrier → `Σ_P=−μs²`; lapse-tied 4-AC → `Σ_P=yμ'`, slip `(μ+yμ')/μ: 1→3/2→2`.
> `Σ_P=0 ⟺ μ=0` (no MOND) or `μ'=0` (linear). **⇒ Φ≠Ψ is forced in every local ≤2-derivative 2-DOF constraint MOND construction.**

This subsumes the three earlier no-gos (source-free γ_PPN=0; lapse-slip; covariant carrier). **Scope (honest):** local, action-based,
≤2-derivative, second-class/Legendre class. **Two flagged open residuals** (NOT "theory closed"): a fully general symmetric-tensor
Lagrange multiplier forcing Φ=Ψ (only the mimetic instance certified to add a dust DOF); and the non-local QUMOND-as-phantom-density route.

**Why AeST escapes (the mechanism, derived):** AeST reaches Φ=Ψ with the *same* yμ' Hessian because its MOND invariant contracts with
the **metric-independent aether-orthogonal projector** `h^μν=g^μν+A^μA^ν` (A unit-timelike); at O(ε²) zero metric-shear coupling, the
cancelling traceless stress carried by the **transverse aether mode** (∝Q=A^μ∂_μφ, →0 as A→0). Cancelling Σ_P *requires* a field with
independent traceless stress = unit-timelike vector + transverse mode = **4 extra DOF → 6, not 2**. **The 6 DOF are exactly what sources
correct lensing.** So AeST+J₁₀ is not just *a* surviving candidate — it is essentially the *necessary* form.

---

## Part II — FC-AeST + J₁₀: CONDITIONALLY CLOSED (all derived gates pass; α₂ + finite-k characteristic are the named unproved gates)

| Gate | Verdict | Basis / provenance |
|---|---|---|
| Exact J₁₀ MOND interpolation, BTFR `v⁴=G_N M a₀` | **PASS** | committed (fc8) |
| Φ=Ψ (weak-field, incl. non-spherical) | **PASS** | AeST reduction; M24 KiDS RAR χ²/dof=0.64 @ canonical a₀ (`fc_lensing_rar_mu10_2026.py`) |
| c_T = 1 (GW170817) | **PASS** (exact, kernel-indep) | committed |
| 6 nonlinear DOF (4 FC + 4 SC) | **PASS** | EXTERNAL-INPUT (PRD 110.044015) |
| δ²J₁₀ on FLRW (Y=0) | **= 0** | J₁₀=O(Y^{3/2})=O(δφ³); F_YQ=0 (separable) ⇒ MOND sector does NOT contaminate the quadratic FLRW Hessian; F_YY→∞ is a Y-chart coordinate feature |
| IR low-k mode (k<k*) | **nonpropagating** (`ω_Y=0`, Jeans-like constraint mode), NOT a propagating ghost | EXTERNAL-INPUT (2109.13287) + `fc_flrw_ir_sign_certificate.py` 20/20 |
| de Sitter k→0 dilution | **PASS** (repair argument, NOT an all-k theorem): χ bounded, `E=Π²/(2K₀)a⁻³→0` even for K₀<0 | `fc_flrw_ir_sign_certificate.py` |
| Healthy scalar region | **nonempty** `c_s²=(2−K_B)(1+K_Bλ_s/2)/(K₂K_B)`; e.g. (K_B,λ_s,K₂)=(0.1,1,20)→c_s²≈0.998 (subluminal) | DERIVATION |
| Healthy vector region | **PASS** `ω_V²=k²+(2−K_B)(1+λ_s)Q₀²/K_B>0` for 0<K_B<2 | EXTERNAL-INPUT (2109.13287) |
| **α₁ exact FC-AeST** | **OPEN** — the naive c₁₃=0 Einstein-aether substitution is ILLEGAL (lands on the singular c₁₂₃=0 chart; the scalar Q-sector mixes in) | needs the scalar-retained AeST 1PN |
| **α₂ exact FC-AeST** | **OPEN — the decisive gate** — could still kill it | needs `f₂(K_B,K₂,λ_s,Q₀)` from the full scalar+aether PPN system |
| Full finite-k FLRW characteristic matrix (H≪k<k*) | **OPEN** | the exact time-dependent K/B/Ω not certified |

**Key structural facts that make α₂ the *whole* game:** in the Solar System `1−μ₁₀~1/(10y¹⁰)~10⁻⁴⁰`, so J₁₀ is negligible there ⇒
**the preferred-frame parameters are pure AeST-background — no kernel tweak (10→8→12) can touch α₁,α₂.** And there is *no PPN no-go*: a
closely-related scalar-Einstein-aether theory has an **exact α₁=α₂=0 surface over a nonempty, positive-energy region** (the scalar is
retained, not discarded), so "healthy aether+scalar ⇒ α₂≠0" is **false**. But that precedent is *not* an AeST derivation — the AeST-specific
`f₁,f₂` must be computed. As of this session the `fc_alpha2_scalar_retained.py` derivation is **incomplete** (fails an intermediate
unit-constraint check; no final f₁,f₂ emitted) — so **α₂ remains genuinely underived**, and no α₂=0 may be claimed.

---

## Why μ₁₀ specifically (empirical, committed): Cassini selects the sharp kernel
The exponential-kernel FC-AeST is **KILLED by the Solar-System Cassini/EFE phantom quadrupole** — μ=1−e⁻ʸ gives Q₂/ceiling=**3.76×**
(FAIL), RouteA/MS08 6.23× (FAIL), FC-tanh 6.09× (FAIL). The sharp family μ_n=y/(1+yⁿ)^{1/n} PASSES for n≥4: μ₅=0.31×, **μ₁₀=0.06×
(comfortable PASS)** (`FC_AEST/scripts/fc_cassini_quadrupole_2026.py`, committed; verified this session). **The structural trap:** the gradual
(exponential) transition that removes the old ks/(1−2s) pole is the SAME shape that maximizes the phantom quadrupole — one kernel can't do both;
only a sharp μ_n clears Cassini. So **μ₁₀ is the empirically-selected kernel**, not just tolerated: it is the safest Cassini member of the
surviving family. (Liabilities inherited: RAR scatter 0.108→0.123/0.127 dex; the registered wide-binary γ_v discriminator = the empirical
falsifier, DR4.) The exponential branch is retired; the 2-DOF constraint-first branch stays dead (Part I).

## The c₂ preferred-frame repair candidate (VERIFIED reference sector; full-AeST OPEN)
To address α₂, add a direct `c₂(∇_μA^μ)²` term with **c₂=K_B/(1−2K_B)** on the Maxwell locus (c₁=K_B, c₃=−K_B, c₄=0), K_B<2.5×10⁻⁵.
**Reference Einstein-aether sector — VERIFIED by sympy this session:** `α₁=−4K_B, α₂=0 EXACTLY, c_T²=c_V²=1, c_S²∈[1−K_B,1]` (healthy,
~luminal, non-superluminal; positive kinetic coefficients). **But this is NOT the full AeST answer** (Carl): the scalar (Q=A^μ∇φ, the
J^μ∇φ acceleration coupling) contributes `α₂^full = α₂^ae(=0) + Δα₂^(φA)`, and **the c₂ term changes the constraint structure — the 6-DOF
count must be RE-DERIVED** (c₁₂₃=0→c₂ liberates the spin-0 aether mode; possible 7th DOF/ghost). The Sagi 2009 generalized-TeVeS PPN
calculation (arXiv:0905.4001) proves scalar-aether α₁=α₂=0 is achievable in a finite region ⇒ **no general PPN no-go** — but it does not
place AeST on that surface. **Final-oven decision table** (running workflow wu1m3w9nx): 6-DOF + |α₂|<1e-7 + healthy finite-k ⇒ GOLDEN CORNER;
6-DOF + |α₂|>1e-7 throughout ⇒ PPN NO-GO; extra-DOF/degenerate Hessian ⇒ REPAIR FAILS; can't complete from the exact action ⇒ α₂-OPEN.
The decisive quantity is the **β₀-scaling of Δα₂^(φA)**: O(β₀)/O(K_B Q₀) screened (λ_s≫10⁷) ⇒ viable; O(1) ⇒ dies. J₁₀ is out of this calc.

## The one remaining calculation (the last lock)

$$\text{Derive } f_1=\alpha_1^{\rm AeST}(K_B,K_2,\lambda_s,Q_0),\ f_2=\alpha_2^{\rm AeST}(K_B,K_2,\lambda_s,Q_0)\text{ from the full }(g,A,\phi)\text{ 1PN system, then intersect } f_1=0,\ |f_2|<10^{-7}\text{ with } \{0<K_B<2,\ K_2>0,\ \lambda_s>0,\ 0<c_s^2\le1,\ c_T=1\}.$$

- Intersection **nonempty** ⇒ FC-AeST+J₁₀ has a genuinely complete viable parameter point → **FRIED**.
- Intersection **empty** ⇒ FC-AeST+J₁₀ **dies cleanly at the preferred-frame gate** (a clean reason the 6-DOF structure wasn't enough).
- Not another architecture, not another kernel — a finite algebraic intersection problem.

## Verdict

> **FC-AeST + J₁₀ = CONDITIONALLY CLOSED / GOLDEN-CORNER CANDIDATE.** A viable parameter region exists at the level of every gate
> derived so far; the AeST-specific α₂ (decisive) and the full finite-k characteristic closure remain **unproved** — one of them (α₂)
> could still kill it. Crispy candidate, honestly conditional — not a fabricated "fully proven" theory.
