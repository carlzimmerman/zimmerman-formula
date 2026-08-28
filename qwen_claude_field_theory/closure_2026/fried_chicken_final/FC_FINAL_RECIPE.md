# 🍗 FC-FINAL — MASTER RECIPE (canonical ingredient list + honest gate ledger)

**Candidate under adversarial closure attack.** This file is the *specification* (what FC-FINAL IS)
plus the *honest current status* of every gate. It is **not** a closure claim. The verdict is produced
by the closure workflow (`fried_chicken_final/`, run `wwxi4ckm0`) → `closure_results.json`.

> **STATUS BANNER (2026-08-28, commit `4199d712`, sympy 1.13.1, py 3.13.9).**
> FC-FINAL = **spatially-covariant constraint-first MMG + Laplacian homogeneous completion + μ₁₀ MOND
> constraint**. It is **NOT AeST**, **NOT** the retarded/nonlocal `Φ=□⁻¹_ret R_uu` theory, **NOT** the
> exponential-kernel MMG.
> **What is genuinely established:** the μ₁₀ constitutive positivity, the second-class MOND constraint
> mechanism, and `N_grav=2` on the *generic non-degenerate branch* (`y>0, k≠0`).
> **What is already FAILED (committed, this session), and is the reason this is not yet fried:** the
> **k≠0 relativistic sector inherits three kernel-blind, Laplacian-blind contradictions** from the
> H⊥-deletion that buys the 2-DOF count — `γ_PPN=0` (lensing, M24 KiDS Δχ²=+403..+498 ≈ 20σ; Cassini
> ≈43,000σ), `α₁=+4 / α₃=−1`, and **matter non-conservation at Newtonian order**. These are **not** μ₁₀
> problems and **not** k=0 problems, so neither the sharp kernel nor the Laplacian completion repairs
> them (see gates Z, AA, Y). The Laplacian completion is a genuine new ingredient but it fixes **only**
> the k=0 homogeneous sector (gate G/T). **Per Carl's own outcome rule (AM), this architecture is
> currently heading to `BURNED — FAILED` or `NO-GO`, not `CLOSED`** — pending the workflow's formal
> adjudication and the one authorized minimal repair (S₂′=D²(q+ln N), which the committed record says
> restores γ_PPN=1 but does **not** repair α₃=−1).

Legend for per-gate **STATUS**: `ESTABLISHED` (derived + committed certificate) · `PARTIAL` ·
`OPEN` · `FAILED` (committed adverse certificate) · `ASSUMED` (phenomenological input, labelled).
Provenance points to committed scripts under `openai_push/final_closure/` (MMG chassis),
`qwen_claude_field_theory/closure_2026/` (constraint construction), `fc8_closure_2026/` (AeST comparison).

---

## A. Candidate identity
$$\text{FC-FINAL} = \text{spatially covariant MMG} + \text{Laplacian auxiliary completion} + \mu_{10}\text{ MOND constraint}$$
Not AeST · not `Φ=□⁻¹_ret R_uu` · not exponential-kernel MMG.
**STATUS:** identity frozen. The prior stored MMG freeze uses `μ=1−e⁻ʸ` and is only *conditionally
closed*; FC-FINAL is a **new specialization** (`μ₁₀ + Laplacian`), not yet frozen-and-closed.

## B. Fundamental geometric variables
$$\gamma_{ij},\ \pi^{ij};\quad \{\gamma_{ij}(x),\pi^{kl}(y)\}=\delta^k_{(i}\delta^l_{j)}\delta^3(x-y);\quad N^i,\pi_i.$$
Residual gauge = **spatial diffeomorphisms only** (preferred foliation; NOT full refoliation invariance).
$$q=-\tfrac16\ln\det\gamma_{ij},\qquad p_q=-2\gamma_{ij}\pi^{ij}\ \text{(normalization to be re-checked from the symplectic form).}$$
**STATUS:** ESTABLISHED (geometric scalar construction present in the committed constraint chain).
Refoliation invariance = **False by construction** (`09_legendre_check.py`, self-classified) — load-bearing
for gate Y (matter conservation) and gate Z (α-sector).

## C. Frozen MOND interpolation (the active kernel)
$$\mu_{10}(y)=\frac{y}{(1+y^{10})^{1/10}},\qquad y=\frac{c^2}{a_0}\sqrt{D_iq\,D^iq}.$$
$$\mu_{10}'(y)=(1+y^{10})^{-11/10},\qquad \mu_{10}+y\mu_{10}'=\frac{y(y^{10}+2)}{(1+y^{10})^{11/10}}.$$
Both `μ₁₀>0` and `μ₁₀+yμ₁₀'>0` for all `y>0`.
**STATUS:** ESTABLISHED (sympy; `fc8_symbolic_audit.py` A6, `13_kernel_swap_ellipticity.py` exit 0 this
session). This is the one place the sharp kernel genuinely helps (strict ellipticity on `y>0`).

## D. Kernel asymptotics
Deep-MOND `μ₁₀=y−(1/10)y¹¹+O(y²¹)`; Newtonian `μ₁₀=1−1/(10y¹⁰)+O(y⁻²⁰)`.
**STATUS:** ESTABLISHED (series, committed). The `y⁻¹⁰` tail = deliberately sharp Solar-System screening
(no direct-MOND PPN leak; the PPN failures at gate Z are **preferred-frame**, not screening).

## E. Action-level primitive
$$\partial J_{10}/\partial Y=\mu_{10}(\sqrt Y/a_0),\quad J_{10}(Y)=2a_0^2\!\int\! \frac{y^2}{(1+y^{10})^{1/10}}dy=\frac{2}{3a_0}Y^{3/2}-\frac{1}{65a_0^{11}}Y^{13/2}+\cdots$$
Differentiate the primitive back to `μ₁₀` as a check.
**STATUS:** ESTABLISHED near `Y=0`; closed form via hypergeometric ${}_2F_1$ (controlled). Consequence
`J₁₀=O(Y^{3/2})=O(δ³) ⇒ δ²J₁₀=0` (kernel invisible at quadratic order) — **load-bearing**: it means μ₁₀
cannot fix any quadratic-order pathology (relevant to AeST-IR *and* to the fact that swapping kernels
cannot move the k≠0 MMG kills).

## F. MOND auxiliary constraint
$$\mathcal C_M=\frac{c^4}{4\pi G}\sqrt\gamma\,D_i[\mu_{10}(y)D^iq]-\sqrt\gamma\,c^2\rho_{\rm src}\approx0.$$
`ρ_src` must be **derived**, not hard-coded (`ρ_m` vs `δρ_m` vs `ρ_m−ρ_bg`) — settled only after the
homogeneous sector (G).
**STATUS:** structure ESTABLISHED; **source term OPEN** and load-bearing (gate G).

## G. Homogeneous / Laplacian completion (the genuine NEW ingredient)
Goal: `k=0` homogeneous cosmology must **not** be forced through the inhomogeneous MOND divergence;
`k≠0` retains the second-class MOND constraint. Laplacian-multiplier construction (2026-MMG *template*,
derived independently), target split `k=0: cosmology`, `k≠0: MOND`. No arbitrary background subtraction
unless it follows from the completed theory.
**STATUS:** **OPEN / PROPOSED.** The old form FAILS at `k=0` (gate T). The Laplacian completion is the
proposed fix and is the one honestly-new mathematical object to derive. **Crucial scoping (committed
lensing mechanism):** the multiplier `D²λ` annihilates the k=0 mode but has **zero support on the k≠0
Φ-sourcing equation**, so it does **not** touch the γ_PPN=0 / α₃ kills (gates Z, AA). It fixes cosmology,
not lensing.

## H. Dirac constraint chain
Primaries `π_i≈0 ⇒ H_i≈0`; then `C_M≈0`; preservation `Ċ_M={C_M,H}≈0 ⇒ C_P≈0`; compute
`Δ_M(x,y)={C_M(x),C_P(y)}`; require **no tertiary** scalar constraint.
**STATUS:** ESTABLISHED for the exponential kernel on the generic branch; **μ₁₀ version must be re-run
from scratch** (workflow is doing this). ⚠️ Referee-flagged residual: the `{D²q, H_i}` inhomogeneous
piece `(1/3)D²(D·ξ)` is **uncomputed** — if the E-mode is physical, the 2-DOF certificate itself collapses.

## I. Principal constitutive tensor
$$A^{ij}_{10}=\mu_{10}\gamma^{ij}+y\mu_{10}'\hat u^i\hat u^j,\quad \lambda_\perp=\mu_{10}>0,\ \lambda_\parallel=\mu_{10}+y\mu_{10}'>0\ (y>0).$$
**STATUS:** ESTABLISHED (eigenvalues positive; `04_rank_and_ellipticity.py` → μ₁₀ via Gate 13).

## J. Second-class bracket
$$\{\mathcal C_M,\mathcal C_P\}\sim[D_iA^{ij}_{10}D_j]^2\ \xrightarrow{\text{Fourier}}\ (A^{ij}k_ik_j)^2>0\quad(y>0,k\neq0).$$
**STATUS:** ESTABLISHED principal symbol (exponential); μ₁₀ re-run in progress. **Do NOT infer global
invertibility from the principal symbol alone** (lower-order terms + the H-bracket must be checked).

## K. Exact DOF target
$$N_{\rm grav}=\frac{12-6-2}{2}=2.$$
**STATUS:** PARTIAL — PASS on the *stated* generic branch (`03_dirac_matrix.py`, `05_dof_count.py`,
`det Δ=(L_N K)²≠0`), **conditional** on the unverified `{D²q,H_i}` first-class hypothesis (gate H) and
**excluding** `k=0` and `y=0`.

## L. Physical modes
$$N^{\rm grav}_{\rm scalar}=0,\ N^{\rm grav}_{\rm vector}=0,\ N_{\rm tensor}=2\ \text{(TT gravitons)}.$$
**STATUS:** target; inherits K's conditionality.

## M. y=0 branch
`μ₁₀(0)=0 ⇒ A^{ij}_{10}→0`: strict ellipticity fails at exactly zero gradient. Separate
**Legendre/kinetic regularity** from **elliptic nondegeneracy** — this is an **elliptic degenerate
boundary**, not a propagating ghost.
**STATUS:** ESTABLISHED as a boundary (not a ghost); controlled weak-solution prescription through `y=0`
= **OPEN**. (`sf55_mmg_y0_degenerate_branch_2026.py`.)

## N. Physical Hessian at y=0
`W_i=D_iq`, `Y∼W²`, `J₁₀∼|W|³ ⇒ ∂²J₁₀/∂W_i∂W_j ∼ |W| → 0`. So `J_YY→∞` (invariant chart) does **not**
imply a divergent physical velocity Hessian.
**STATUS:** ESTABLISHED (mirrors the AeST `y0_physical_hessian.py` result; chart artifact, not pathology).

## O–Q. Newtonian limit / deep-MOND / Newtonian recovery
`q=Ψ/c²+O(c⁻⁴)`, `y=|∇Ψ|/a₀`, and (source normalization derived)
$$\nabla\!\cdot[\mu_{10}(|\nabla\Psi|/a_0)\nabla\Psi]=4\pi G_N\rho_b,\quad v_\infty^4=G_NM_ba_0,\quad \nabla^2\Psi=4\pi G_N\rho_b+O[(a_0/g)^{10}].$$
**STATUS:** ESTABLISHED (exact AQUAL; `02_newtonian_limit.py`, c² factors cancel). BTFR exact. This
**nonrelativistic core is healthy** — it is the part that survives the FAILED relativistic completion.

## R. Measured Newton constant
Derive `G_N=𝒢(G, MMG params)`; require `G_Cav=G_orbital=G_MOND`.
**STATUS:** PARTIAL (Newtonian `G_N` clean; multi-probe consistency not fully certified). ⚠️ Interacts
with gate Y: the matter χ-force forces a `G_bare=G_lab/2` absorption at `κ_bare=0.6285` (+1.8/+2.15σ).

## S. Tensor sector
$$Q_T>0,\qquad c_T^2=1.$$
**STATUS:** ESTABLISHED for the MMG chassis (`07_tensor_sector.py`, `ω²=c²k²`). **Never transfer** to
other hosts. **Do NOT adopt the 2026 Laplacian-MMG superluminal `c_T>1` subclass** — enforce luminal from
the start (gate AK).

## T. Cosmological background
`γ_ij=a²(t)δ_ij ⇒ D_iq=0 ⇒ y=0`. Need `H(a), Ḣ(a), ρ_eff, p_eff`; the target sequence
`radiation → matter → acceleration`.
**STATUS:** **OLD-FORM FAILED** — with total `ρ_m` on the RHS the constraint demands `0=4πG ρ̄_m` (the
homogeneous MOND divergence vanishes but `ρ̄_m>0`); on a compact slice `∫√γ D_i(μD^iq)=0 ≠ ∫√γ 4πGρ_m`.
This is **the** motivation for the Laplacian completion (G). Homogeneous sector = OPEN.
Committed: linear scalar sector is **EMPTY** (`μ(0)=0` kills the linearized flux ⇒ no linear Poisson, no
`G_eff`, no growth) — a real obstruction to confronting CMB/growth at linear order.

## U. a₀–dark-energy relation
$$a_0=\tfrac12 c\sqrt{G\rho_\Lambda}\quad\Longleftrightarrow\quad \Lambda=\frac{32\pi a_0^2}{c^4}.$$
**STATUS:** **ASSUMED** (external phenomenological input; `κ=½`, `Z~21` FITTED). The derived MMG
background is **a₀-blind** (no dark energy; Λ by hand) → the tie is **not** realized in this chassis.
Keep labelled ASSUMED — never "derived".

## V. FLRW perturbations (decisive gate)
`S⁽²⁾=½∫dt d³k a³[q̇ᵀK_eff q̇ − (k²/a²)qᵀG_eff q − qᵀM²_eff q]`; require `λ_i(K_eff)>0`, real dispersion;
test `k≫aH`, `k∼aH`, `k≪aH`.
**STATUS:** **OPEN** (rides on the uncertified k=0 prescription; empty linear scalar sector makes even the
setup ill-posed until G is completed).

## W. IR stability
Target: `Ω^grav_scalar=0` (no independent gravitational scalar) — prove via the **reduced symplectic
form**, not words. If true, the AeST low-k scalar oscillator is *architecturally absent* (the one real
advantage of constraint-first over AeST).
**STATUS:** OPEN — but structurally favorable *if* K/H survive (no scalar pair ⇒ no AeST-type IR mode).
This is the prize the whole pivot chases; it is **downstream** of the unresolved lensing/PPN kills.

## X. Hyperbolicity / causality
Principal symbol `P(ξ)`; real characteristics; well-posed evolution; keep elliptic MOND constraint
separate from hyperbolic tensor evolution.
**STATUS:** OPEN (tensor `c_T=1` clean; full characteristic matrix not done for μ₁₀+Laplacian).

## Y. Matter consistency  ⚠️ FAILED
Derive `{H_m,C_M}`, `{H_i,H_m}`; do **not** assume `∇_μT^{μν}=0` (preferred foliation).
**STATUS:** **FAILED (committed).** `∇_μT^{μi}|_g=−ρD^iX` at **Newtonian order** (Gate 10's O(v²/c²)
claim falsified, commit `3c771f0a`); unrescaled 1-AU anomaly `1.62e11×` the Sereno–Jetzer bound
(`gate_matter_conservation_derivation.py`). Sourced by `C_M`'s instantaneous response — i.e. by the MOND
law itself. **Kernel-blind.** Not repaired by μ₁₀ or by the Laplacian completion.

## Z. PPN  ⚠️ FAILED
Derive `γ, β, α₁, α₂, ξ` from the actual theory (no Einstein-aether import).
**STATUS:** **FAILED (committed, kernel-independent to <1e-19).** `γ=0, β=1, α₁=+4 (4×10⁴× bound),
α₃=−1 (2.5×10¹⁹× pulsar bound, momentum non-conservation), Mercury perihelion 1/3 GR (716σ)`
(`ppn_mmg_gate_2026.py`, cross-checked vs committed `b6b3ced2`). The `α₃=−1` is sourced by `C_M` itself.
**No frozen-sanctioned flexibility repairs it** (the Gate-13 μ_n swap only clears the EFE-Q2 quadrupole).

## AA. Lensing  ⚠️ FAILED
Derive `Φ, Ψ` from the full weak-field system; `α_lens(b)=(2/c²)∫∇_⊥(Φ+Ψ)dz`; test spherical /
axisymmetric / nonspherical. Never infer lensing from the MOND force law.
**STATUS:** **FAILED (committed, re-run exit 0 THIS session).** The second-class constraint `D²q=0`
forces `Φ=0` at all accelerations (the deleted `H⊥` is precisely the equation that sourced Φ); slip
`η=Φ/Ψ=0 ⇒ γ_PPN=0`; light sees **half** the potential. `M24 KiDS lensing RAR Δχ²=+403..+498 (≈20σ)`;
Cassini Shapiro `≈43,000σ`; 0.875″ solar deflection (dead at 1919 precision); cluster shortfall doubles
to `3.44–4.16×`. Derived twice independently (`gate_lensing_weakfield_derivation.py` commit `b6b3ced2`;
PPN gate). **Kernel-blind AND Laplacian-blind** (the completion touches only k=0). This is the **primary
kill**; the "MMG analogue of the York ν²-gap in harder form: the ij sector is not under-supplied, it is
UNSOURCED."

## AB. External-field effect
Derive the EFE from the actual constraint (do not assume standard MOND EFE); check `g_ext∼a₀`.
**STATUS:** OPEN (nonrelativistic EFE is derived and healthy in the AQUAL core; relativistic EFE not
certified for this completion).

## AC. Large-radius behavior
Determine any extra transition scale `r_μ`; require non-MOND far-field outside the constrained galactic
regime.
**STATUS:** OPEN.

## AD. Strong-field solutions
Vacuum spherical / neutron star / black hole; track `det H, det Δ, Q_T, c_i²`.
**STATUS:** OPEN (not exercised).

## AE. EFT cutoff
Canonical-normalize modes; find `Λ_sc`; require `H_cosm, k_gal, k_Solar ≪ Λ_sc`.
**STATUS:** OPEN.

## AF. Structure formation
Only after FLRW passes: `G_eff(k,a), η=Φ/Ψ, Σ(k,a)`; solve the growth ODE; `fσ8, P(k,z)`.
**STATUS:** OPEN — **blocked upstream** (rides on the uncertified k=0 prescription and the empty linear
scalar sector, gate T/V).

## AG. Parameter freeze
Freeze `{a₀, G, Λ, all MMG coefficients, all auxiliary-sector coefficients}`; any remaining fitted
parameter labelled fitted.
**STATUS:** `a₀` (with `κ=½`, `Z~21`) FITTED/declared; Λ ASSUMED (gate U); MMG coefficients minimal.

## AH. Independent verification
Two routes per load-bearing calc (`analytic ↔ symbolic ↔ numerical`); precision doubling, grid
refinement, parameter continuation, alt ICs, branch searches, residual checks. No PASS on a single run.
**STATUS:** enforced (the closure workflow runs A/B implementations; committed gates carry re-run logs).

## AI. Referee-zero-day
≥50 hostile objections, each `objection → equation → calculation → answer`.
**STATUS:** produced by the workflow → `REFEREE_ZERO_DAY.md`.

## AJ. Existing repo pieces to PRESERVE
Two-DOF generic MMG branch · second-class MOND constraint · positive constitutive operator · `c_T=1`
(on the original construction's stated branch). Repo keeps the old theory **conditionally closed**, not
globally closed.

## AK. Things that must NOT be carried forward as "final"
`μ=1−e⁻ʸ` (unless it independently beats μ₁₀) · `Φ=□⁻¹_ret R_uu` / old localization fields (generated a
genuine scalar pole) · AeST's six-DOF count as the MMG count · the 2026 Laplacian-MMG **superluminal
`c_T>1`** branch.

## AL. Final canonical action/constraint package (to be produced AFTER the completed Hamiltonian)
$$q=-\tfrac16\ln\det\gamma,\quad y=\tfrac{c^2}{a_0}\sqrt{D_iqD^iq},\quad \mu=\tfrac{y}{(1+y^{10})^{1/10}},$$
$$\mathcal C_M^{(10)}=0,\quad \mathcal C_P^{(10)}=\{\mathcal C_M^{(10)},H\}=0,\quad \mathcal C_{\rm Lap}=0,\quad \{\mathcal C_M^{(10)},\mathcal C_P^{(10)}\}\neq0,\quad N_{\rm grav}=2,\ N_T=2,\ c_T=1.$$
**STATUS:** the local (`y>0,k≠0`) pieces are established; the package is **not** frozen because T/V/Y/Z/AA
are not passed.

## AM. Closure outcomes (only these)
`FRIED CHICKEN — CLOSED` (all structural gates pass) · `FRIED CHICKEN — CONDITIONALLY CLOSED` (all
structural pass; only an explicitly-labelled phenomenological input remains) · `BURNED — FAILED` (a
structural gate fails and the one minimal repair fails) · `NO-GO` (the architecture space is
mathematically obstructed).

---

### One-line repo status
> **Repo = older conditional exponential-MMG construction. Target FC-FINAL = Laplacian-MMG + μ₁₀ — a NEW
> specialization, NOT yet frozen-and-closed.** Local constraint machinery + μ₁₀ ellipticity are earned;
> the k≠0 relativistic sector currently reproduces three committed, kernel-blind, Laplacian-blind
> structural kills (lensing γ_PPN=0, α₁/α₃, Newtonian-order matter non-conservation) traceable to the
> H⊥-deletion that buys 2-DOF. **The decisive question the closure attack must answer: is that
> deletion-vs-lensing trade a general NO-GO for constraint-first relativistic MOND, or is there a minimal
> within-family repair that restores γ_PPN=1 AND α₃=0 without adding a propagating scalar?** Verdict →
> `closure_results.json`.
