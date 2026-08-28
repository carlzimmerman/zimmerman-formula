# FC-FINAL — Publication-Grade Theorem Package (scaffold, 2026-08-28)

**Purpose.** Audit-grade record separating **mathematical closure** (theorem about the exact theory) from
**physical viability** (evidence the theory works). The two are never mixed. Status is one of:

- **CERTIFIED** — an algebraic certificate exists (`simplify(derived − claimed)==0`, not an asserted answer),
  committed and runnable.
- **OPEN(spec)** — genuine research-grade proof not completed; the exact object to prove is specified. **No
  "likely / benign / numerically healthy" is allowed to stand in for an algebraic proof here.**

**Permanent freeze:** FC-FINAL is a **six-DOF AeST-type** relativistic theory. The MMG `20−12−4=2`
constraint-first count belongs to a *different, failed* construction (`../FINAL_THEORY_MMG_CONSOLIDATED`,
γ_PPN=0, retracted) and MUST NOT be imported. Target: **6 nonlinear DOF + healthy sectors + exact μ₁₀ MOND**.

---

## §1. The frozen action (canonical — the paper states exactly this, nothing else)

$$
S=\frac{c^3}{16\pi\tilde G}\int d^4x\sqrt{-g}\Big[R-\tfrac{K_B}{2}F_{\mu\nu}F^{\mu\nu}+(2-K_B)(2J^\mu\nabla_\mu\phi-Y)-\mathcal F(Y,Q)-\lambda(A_\mu A^\mu+1)\Big]+S_m[g,\psi]
$$

$$
\mathcal F(Y,Q)=J_{10}(Y)+K(Q),\quad K(Q)=-2\Lambda+\mathcal K_2(Q-Q_0)^2,\quad
\mu_{10}(y)=\frac{y}{(1+y^{10})^{1/10}},\ y=\sqrt Y/a_0
$$

$$
Y=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\phi\nabla_\nu\phi,\quad Q=A^\mu\nabla_\mu\phi,\quad
F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]},\quad J^\mu=A^\nu\nabla_\nu A^\mu
$$

`a₀` a **fundamental constant**; matter minimally coupled to the single metric `g`. **No exponential kernel,
no MMG C_M, no nonlocal Φ.** (`a₀²=κ²c²Gρ_Λ` stays labelled INPUT/postulate — not derived.)

## §2. The central theorem (stated to the standard we will hold)

> On the explicitly-defined regular region `𝒟_reg` (§3), the FC-FINAL Hamiltonian has the stated first/
> second-class constraint structure, the Dirac algorithm terminates without further constraints, and the
> physical phase-space dimension is **six** gravitational DOF per spatial point. The `Y=0` boundary is
> treated separately in the primal `D_iφ` chart.

It does **not** say two DOF; does **not** claim the Legendre chart is globally regular; does **not** hide
`Y=0` inside a `Y>0` proof.

## §3. The regular domain (explicit)

$$
\boxed{\ \mathcal D_{\rm reg}=\{\,Y>0,\ \ Q\in\mathcal Q_{\rm reg}\ (\mathcal K_2 Q_0\neq0),\ \ \Xi\neq0,\ \ \det C^{AB}\neq0\,\}\ }
$$

with `Ξ=χ²ν−(2(2−K_B)/K_B+μ)|A|²` [2307.15126 Eq.32]. The `Y=0` stratum is **excluded** from `𝒟_reg` and
carries its own boundary theorem (§Gate 9).

---

## §4. Gate ledger (the 16-point standard, honest current status)

| # | Gate | Status | Evidence / exact OPEN spec |
|---|------|--------|-----------------------------|
| 1 | Exact action + J₁₀ frozen | **CERTIFIED** | §1; `fc8_symbolic_audit.py`, `detC_legendre_regularity.py` |
| 2 | Variational field equations | **OPEN(spec)** | derive δS=0 for g,A,φ,λ explicitly (not yet committed in full covariant form) |
| 3 | Constitutive algebra: μ₁₀'=(1+y¹⁰)⁻¹¹ᐟ¹⁰; μ₁₀+yμ₁₀'>0; J₁₀=x³/3+…; β₀=λ_s=1 | **CERTIFIED** | `fc8_symbolic_audit.py`, `detC_legendre_regularity.py` |
| 4 | Generic Legendre regularity on 𝒟_reg (det map ≠0) | **CERTIFIED** | `detC_legendre_regularity.py`: det ∝ K₂Q₀/(Q²·2a₀²y(1+y¹⁰)^{11/10}) ≠0 for Y>0,Q≠0,K₂Q₀≠0 |
| 5 | **Full nonlinear Dirac chain (from scratch, all constraints, all momenta)** | **OPEN(spec)** | derive π's for (q,A,φ,μ,ν,N,Nⁱ); list ALL primaries; preserve each; show primary→secondary→(tertiary?)→**termination**. NOT to be replaced by citing 2307.15126 |
| 6 | Operator-valued constraint rank on 𝒟_reg | **OPEN(spec)** | prove rank Δ_AB(x,y) as an operator (not a Fourier scalar) on 𝒟_reg; det_operator Δ≠0 |
| 7 | No hidden tertiary constraints | **OPEN(spec)** | show Φ̇_I≈0 solves uniquely for λ^I (no new Ψ(Γ)); if Ψ appears, verify Ψ̇≈0 closes |
| 8 | 6 nonlinear DOF = (2N−2F−S)/2, F/S identified | **OPEN(spec)** | full count from §5–7; identify the 6 as 2 tensor + vector/scalar sectors; verify J₁₀ doesn't change it |
| 9 | **Y=0 primal-chart constraint continuation** | **OPEN(spec)** | switch to v_i=D_iφ; run the Dirac algorithm AT Y=0 in the primal chart; prove N_phys(Y=0)=N_phys(Y>0⁺) or give the obstruction. *This is the one genuinely novel proof.* |
| — | Y=0 physical Hessian finite-positive (H_phys→2(2−K_B)I) | **CERTIFIED** | `y0_physical_hessian.py`: MOND eigenvalues 2r/a₀,4r/a₀→0; seed finite ⇒ H_phys(0)>0 for K_B<2 |
| — | Y=0 auxiliary det C=0 is a CHART degeneracy (not a DOF jump) | **CERTIFIED** | `detC_legendre_regularity.py` + `y0_physical_hessian.py` |
| 10 | Chart invariance of rank/DOF under regular canonical transf. | **OPEN(spec)** | prove invariance for regular (q,p)→(Q,P); state Y=0 NOT covered by the Y↔μ Legendre map ⇒ primal chart |
| 11 | Quadratic stability all sectors (Q_i>0, c_i²≥0) on claimed backgrounds | **PARTIAL** | tensor c_T=1, Q_T>0 CERTIFIED; scalar/vector Q_V,Q_S,c_V²,c_S² on FLRW/spherical = OPEN(spec) |
| 12 | Exact weak-field MOND: ∇·[μ₁₀(|∇Ψ|/a₀)∇Ψ]=4πG_Nρ; spherical; deep-MOND g²=a₀g_N; BTFR | **PARTIAL** | spherical/BTFR CERTIFIED (`fc8_symbolic_audit.py`); full derivation from δS=0 with backreaction OPEN(spec) |
| 13 | Newtonian normalization / sharp recovery 1−μ₁₀=O((a₀/g)¹⁰) | **CERTIFIED** | `fc8_symbolic_audit.py` |
| 14 | γ_PPN=1 (lensing slip Φ=Ψ) | **CERTIFIED** | PPN workflow: no anisotropic stress from the dark sector; ∂_i∂_j(Φ−Ψ)=0, kernel-independent |
| 15 | Full metric/lensing Φ+Ψ from the FULL relativistic equations | **OPEN(spec)** | derive Φ,Ψ + null deflection from g/A/φ eqs; do NOT infer from the MOND scalar eq |
| 16 | **PPN α₁,α₂,β actual expansion** | **OPEN(spec), α₂ ADVERSE-LEANING** | α₁=−4K_B (K_B<2.5e-5); α₂=(5/2)K_B (K_B<4e-8) or uncomputed on consistent bg — EA import INVALID (scalar mixing outside EA family). β 2PN uncomputed. |
| 17 | Cosmology from lapse variation (vary N before N=1); H²,Ḣ,ρ_eff,p_eff; role of K(Q) | **OPEN(spec)** | homogeneous aligned bg Y=0,Q=φ̇; derive, don't assume |
| 18 | Causality / well-posedness | **OPEN(spec)** | characteristic/hyperbolicity analysis on 𝒟_reg |
| 19 | Matter consistency (∇_μT^{μν}=0 as identity) | **OPEN(spec)** | single-metric minimal coupling ⇒ expected, but derive |
| 20 | Strong-field (BH/NS) | **OPEN(spec) / SCOPE OUT** | solve or explicitly scope the theorem away |
| 21 | Structure formation G_eff(k,a), η(k,a), fσ₈ | **OPEN(spec)** | linear-theory functions on the intended range |
| 22 | Numerical + independent-route replication (§15,§16 of the standard) | **PARTIAL** | Route A (Lagrangian/Dirac) ⟷ Route B (auxiliary Legendre) must independently give N=6; only the Legendre side is certified so far |

## §5. Honest bottom line

**Certified now (certificate-grade):** the frozen action; the sharp-J₁₀ constitutive algebra incl. β₀=λ_s=1;
the generic-branch Legendre regularity defining `𝒟_reg`; the `Y=0` physical Hessian finite-positive (the
feared pathology resolved as a chart artifact); Newtonian/deep-MOND/BTFR limits; γ_PPN=1; c_T=1.

**The two load-bearing proofs that remain genuinely research-grade (no obstruction found, but NOT proven):**
(i) the **full from-scratch nonlinear Dirac chain + operator rank** for the J₁₀ specialization (Gates 5–8,10)
— not a citation of the AeST theorem; (ii) the **Y=0 primal-chart constraint continuation** (Gate 9) — the
one novel piece. Plus the physical-viability gates (lensing, **α₂**, cosmology, causality, growth), of which
**α₂ is the live adverse-leaning risk.**

**Therefore, per the standard, FC-FINAL may NOT yet carry the word "PROVEN" on a title page.** It is a fully
specified, sharp-kernel, six-DOF-AeST candidate with no known structural kill — crispy as a candidate, not
yet a watertight published theorem. The remaining work is *specified*, not hand-waved.
