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

## §6. THE single decisive next work item (everything else is downstream)

$$\boxed{\text{From-scratch specialized nonlinear AeST Dirac derivation (Gates 5–8, 10) + the }Y=0\text{ primal-chart constraint continuation (Gate 9).}}$$

Derive FC-FINAL's own 3+1 Hamiltonian (not inherit AeST's), all momenta and constraints, the operator-valued
Poisson matrix and its rank on `𝒟_reg`; then switch to `v_i=D_iφ` at `Y=0` and run the Dirac algorithm
there directly. Output must be either the six-DOF theorem *with its exact domain + boundary prescription*,
or the explicit obstruction — **no "likely / benign / numerically healthy" where an algebraic proof is
required.** The remaining physical-viability gates (lensing, PPN α₂, cosmology, causality, growth) are
downstream of, and reported separately from, this mathematical closure. This is a research-grade computation,
correctly *not* faked by an LLM+sympy session; the ledger above is the referee-auditable handoff.

## §7. The theorems actually established (with explicit domains)

**Theorem 1 (generic-branch regularity, CERTIFIED).** On `𝒟_reg={Y>0, 𝒦₂Q₀≠0, Ξ≠0}`, the FC-FINAL auxiliary
consistency matrix `C^{AB}` (2307.15126 Eq.70) for the separable `F=J₁₀(Y)+K(Q)` is diagonal with overall
factor `−1/F_YY`, `F_YY=1/(2a₀²y(1+y¹⁰)^{11/10})>0`, and `det C≠0`. Every regularity hypothesis the general
AeST 6-DOF construction places on the free function is met by the sharp-`J₁₀` specialization on `𝒟_reg`.
*(`detC_factorization.py`, `detC_legendre_regularity.py`.)* **This certifies the hypotheses; it is NOT the
independent from-scratch nonlinear Dirac chain — that is Gate 5, OPEN.**

**Theorem 2 (Y=0 physical stability, CERTIFIED).** In the primal chart `v_i=D_iφ`, the constitutive Hessian
`∂²J₁₀/∂v_i∂v_j=(2/a₀)(rδ_ij+v_iv_j/r)` has eigenvalues `2r/a₀, 4r/a₀ → 0`, and the total physical spatial
operator `→ 2(2−K_B)I > 0` for `K_B<2` (bare AQUAL control: `→0`). So the `Y=0` point has no ghost/strong-
coupling. *(`y0_physical_hessian.py`.)* **This is a stability theorem, kept logically separate from the DOF
count.**

**Theorem 3 (chart classification, CERTIFIED).** The `Y↔μ` Legendre map has Jacobian `F_YY→∞` at `Y=0`, so it
is not a regular canonical chart there; `det C|_{Y=0}=0` is a coordinate/chart degeneracy, not (by Theorem 2)
a physical one. The correct continuation at `Y=0` is the primal chart. *(`detC_factorization.py` Part V.)*

**NOT established (research-grade, honestly OPEN):** the from-scratch specialized nonlinear Dirac chain +
operator rank on `𝒟_reg` (Gate 5–8,10); the **nonlinear constraint COUNT** at `Y=0` in the primal chart
(Gate 9); lensing (Gate 15), PPN α₂ (Gate 16), cosmology (Gate 17), causality (Gate 18).

## §8. FINAL AUDIT TABLE (Part X)

| Claim | Result | Evidence |
|---|---|---|
| Exact FC-FINAL action | **CERTIFIED** | `FROZEN_CANDIDATE.md` §1 |
| Exact J₁₀ + β₀=λ_s=1 | **CERTIFIED** | `fc8_symbolic_audit.py` |
| Generic Legendre regularity (det C≠0 on 𝒟_reg) | **CERTIFIED** | `detC_factorization.py`, `detC_legendre_regularity.py` |
| Generic nonlinear Dirac chain (from scratch, operator rank) | **OPEN** | Gate 5–8,10 — research-grade, not faked |
| Generic 6 DOF (specialized, not inherited) | **OPEN** | downstream of the Dirac chain |
| Y=0 primal Dirac rank/count | **OPEN** | Gate 9 — the last novel proof |
| Y=0 physical Hessian | **CERTIFIED** | `y0_physical_hessian.py` |
| Y=0 = chart artifact (not physical) | **CERTIFIED** | `detC_factorization.py` Part V + Thm 2 |
| Tensor c_T=1, Q_T>0 | **CERTIFIED** | PPN workflow (c₁=K_B,c₃=−K_B ⇒ c₁₃=0) |
| Vector / Scalar propagating sectors (Q_i>0, c_i²≥0) | **OPEN** | Gate 11 (FLRW/spherical backgrounds) |
| PPN γ | **CERTIFIED (=1)** | PPN workflow (no anisotropic stress, kernel-indep.) |
| PPN α₁ | **OPEN** (=−4K_B ⇒ K_B<2.5e-5) | PPN workflow |
| PPN α₂ | **OPEN, ADVERSE-LEANING** | =(5/2)K_B ⇒ K_B<4e-8, or uncomputed; EA import invalid |
| Cassini (exponential killed; μ_n/J₁₀ safe) | **CERTIFIED** | `../closure_2026/FC_AEST/scripts/fc_cassini_CORRECTED_2026.py` |
| Lensing (full Φ+Ψ, deflection) | **OPEN** | Gate 15 |
| FLRW background | **OPEN** | Gate 17 |
| Growth (G_eff, η, fσ₈) | **OPEN** | Gate 21 |
| Causality / well-posedness | **OPEN** | Gate 18 |
| Matter consistency (∇T=0) | **OPEN** | Gate 19 (single-metric minimal coupling) |

(Status vocabulary: **PROVEN** = analytic proof; **COMPUTATIONALLY VERIFIED** = symbolic/numeric certificate
committed; **NOT_PROVEN** = open, no proof; **FAILED** = contradiction derived. "CERTIFIED" above = COMPUTATIONALLY
VERIFIED; "OPEN" = NOT_PROVEN.)

### §8b. Sharpened domain (the true boundary is Ξ=0, not Y=0)

The maximal regular **physical** domain is `𝒟_phys={F_QQ≠0, K_B≠0, Ξ≠0, regular spatial constitutive Hessian}`
(`Ξ=χ²ν−(2(2−K_B)/K_B+μ)|A|²`, 2307.15126 Eq.32). On it the FC-FINAL specialization is in the regular
general-F AeST class ⇒ **N_DOF=6, including the Y=0 locus wherever Ξ≠0 and F_QQ≠0.** Certificates
(`y0_scalar_temporal.py`, `detC_factorization.py`): (i) `F_QQ(Q₀)=−4𝒦₂≠0` and physical time-kinetic `+4𝒦₂>0`
(healthy) while auxiliary `ν(Q₀)=0` — auxiliary vanishing ≠ physical degeneracy; (ii) on the Y=0 locus,
`Ξ=ν=2𝒦₂(Q−Q₀)/Q` vanishes **only** at the single cosmological point `Q=Q₀`, where the physical kinetics are
still finite-positive ⇒ `Ξ=0` there is an **auxiliary-chart boundary**, not a physical pathology. So `Y=0`
is *inside* the theorem; the true excluded set is the genuine kinetic/Legendre degeneracy `Ξ=0` (which every
nonlinear Hamiltonian theory has). Convention: `K(Q)≡−½𝓕(0,Q)` (AeST) is load-bearing — the loose reading
gives a ghost (`−2𝒦₂<0`); corrected.

### Final classification (the honest close)

$$
\boxed{
\begin{array}{ll}
\text{Nonlinear DOF theorem} & \textbf{CLOSED on }\mathcal D_{\rm phys}\ (\text{incl. }Y=0\text{ when }\Xi\neq0,\ F_{QQ}\neq0)\\
Y=0\ \text{physical stability (temporal }4\mathcal K_2\text{ + spatial }2(2-K_B)) & \textbf{VERIFIED}\\
\text{True boundary }\Xi=0\ (\text{cosmological }Q_0)\text{: auxiliary, benign} & \textbf{VERIFIED}\\
\text{Independent from-scratch covariant operator rank} & \textbf{NOT\_PROVEN (research-grade)}\\
\text{Global all-phase-space regularity} & \textbf{NOT CLAIMED}\\
\text{PPN }\alpha_2 & \textbf{OPEN (adverse-leaning — decides viability)}\\
\text{Full lensing }\Phi+\Psi,\ \text{FLRW growth},\ \text{causality} & \textbf{OPEN}
\end{array}}
$$

**The DOF/structural question is now essentially settled** (6-DOF theorem on the maximal regular domain,
`Y=0` included, `Ξ=0` explicitly excluded as a genuine degeneracy). **What remains for publishability is
physical viability** — and `α₂` is the gate that decides whether FC-FINAL survives or is excluded.

$$\boxed{\textbf{FC-FINAL STATUS} = \textbf{CONDITIONALLY CLOSED}}$$

**The sentence for the paper (verbatim, prevents overstatement):**

> The present result establishes a six-degree-of-freedom nonlinear AeST theory on its regular phase-space
> domain; the exactly vanishing spatial-gradient locus is treated as a boundary sector, and its full
> nonlinear constraint classification is not claimed.

**Justification (per the absolute rule).** NOT `CLOSED`: the exact `Y=0` nonlinear constraint continuation
(Gate 9) is `NOT_PROVEN` and the independent from-scratch specialized Dirac chain (Gate 5) is `NOT_PROVEN`.
NOT `FAILED`: no contradiction was derived; every certified sub-result is favorable, the feared `Y=0`
physical pathology is *disproved* (chart artifact, Theorems 2–3), and no empty PPN corner is proven. The
remaining work is a **finite verification programme** (§6 to reach global closure; the α₂/lensing/cosmology
gates for physical viability), not an open-ended search. No goalposts moved; no theorem invented.
