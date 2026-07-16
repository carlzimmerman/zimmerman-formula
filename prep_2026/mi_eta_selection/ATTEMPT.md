# LANE eta-SELECTION — does a relational/thermal BATH reduction SELECT the weighting eta(beta), or is it a theory CONSTANT?

**Date:** 2026-07-16. **Framework:** Carl Zimmerman's de Sitter–Unruh **MODIFIED INERTIA**, judged on its
own terms (own interpolation ν(y)=√(1+1/y), μ(x)=K(x²), horizon-derived a₀=cH_Λ/Z). **Both footings
carried throughout:** canonical **a₀ = cH_Λ/Z = 9.36×10⁻¹¹** (ρ_DE), alt **a₀ = 1.13×10⁻¹⁰** (ρ_tot/cH₀),
Z=√(32π/3), T_dS=H_Λ/2π, κ_eff=√(H_Λ²+(a/c)²). Sign **s=−1** and **a₀'s value** remain **POSTULATES**
(untouched by this lane). Not a TOE / SM claim — gravitational-inertial sector only.

**Scripts (all exit 0, no hard-coded verdict booleans — every `chk` reads a computed number; grep-audited):**

| script | checks | candidate | verdict |
|---|---|---|---|
| `q1a_maxentropy.py`            | 7/7  | (a) max-entropy-production / min-dissipation at fixed KMS T | **WEIGHTING-BLIND** |
| `q1b_feynman_vernon.py`        | 15/15| (b) Feynman–Vernon influence functional (the core)         | **WEIGHTING-BLIND** |
| `q1c_fdt_split.py`             | 5/5  | (c) fluctuation-dissipation theorem at T_dS                 | **WEIGHTING-BLIND** |
| `q1d_passivity_analyticity.py` | 6/6  | (d) passivity + analyticity of the reduced response        | **WEIGHTING-BLIND** |
| `q2_massive_pole.py`           | 12/12| Q2 general-mass dS pole-location robustness                 | **NULL is mass-robust** |

*(`_common.py` = shared footing + the framework kernel K and its Herglotz spectral density ρ(t).)*

---

## 0. The question and the premise

The pullback lane (`mi_closure_pin/PULLBACK.md`, `CONSEQUENCES.md`) established, by direct computation on
exact non-uniform de Sitter worldlines, that **KINEMATICS is exhausted**: the dS-Unruh memory pole sits at
**κ_eff = √(H_Λ²+(a/c)²) ≥ H_Λ** for **every** eccentricity, **every** anisotropy, and **every** reduction
weighting (Pythagorean; acceleration moves the pole UP, never into the (0,H_Λ) amplitude-MOND band). So no
weighting is **kinematically** selected. The theory is complete **up to one bounded reduction-weighting
function η(β)** on 2-D orbit-shape space (eccentricity × velocity-anisotropy), bracketed between closure A
(instantaneous |a|, dSph offset **0.000 dex**) and closure B (residence-averaged, **≈ −0.02…−0.05 dex**).

**This lane tests DYNAMICS instead of kinematics:** does coupling S_matter to the relational/thermal
dS-Unruh **bath** (the environment the Herglotz kernel already encodes — *not* a new ad-hoc field) SELECT a
unique η(β) via a ghost-free, KMS/detailed-balance-consistent, causality-respecting mechanism? Four
candidate selection principles are tested **each explicitly**.

---

## 1. Q1 — the one structural fact that runs through all four candidates

**η(β) is a NONLINEAR operator-ordering (Jensen-gap) degree of freedom, while every ghost-free KMS-passive
bath reduction is a 2nd-cumulant (quadratic / 2-point) operation.** They live in orthogonal data.

Precisely: the slow bath (τ_mem ~ 1/H_Λ ≈ 15–18 Gyr ≫ orbital period) integrates the fast orbit and retains
a moment of the acceleration history. The two closures differ by the **Jensen gap**

  **G(β) = ⟨K(z)⟩ − K(⟨z⟩)**,  z = |a|²/a₀²,  leading term = ½ K''(⟨z⟩)·Var(z) + …

- K is **concave** (K''(1) = −3/8 + 19√5/200 < 0, computed in `q1b` §2), so G ≠ 0 whenever Var(z) > 0.
- **Var(z)** is a **connected 4-point** of the worldline acceleration, and it grows monotonically with orbit
  shape (computed Kepler table, `q1b` §2): Var(z)/⟨z⟩² = 0.00 (e=0) → 0.82 → 5.23 → 65.9 (e=0.9). So η(β) is
  a **real** degree of freedom, not a phantom.
- A Gaussian, KMS-passive, Herglotz-positive bath has **all cumulants above the 2nd equal to zero**
  (`q1b` §1: κ₁=0, κ₂=σ², κ₃=κ₄=κ₅=κ₆=0). Its Feynman–Vernon influence functional is **exactly quadratic**
  in the system path → it fixes the ⟨z⟩ (2-point) structure and is **identically blind to Var(z)** (the
  4-point). Hence **d(bath term)/dη = 0** (computed, `q1b` §3), and the reduction supplies **no
  η-restoring term** (the Jensen gap is linear in η → extremum at the A/B endpoints, not an interior value).

### Candidate-by-candidate (each FORCES-η? or WEIGHTING-BLIND, with the computed reason)

**(a) Max-entropy-production / min-dissipation at fixed KMS T — WEIGHTING-BLIND** (`q1a_maxentropy.py`).
The entropy-production rate σ = (1/T)∫dω ω Im[χ(ω)]|F(ω)|² is **quadratic** in the trajectory
(d³σ/dF³ = 0, computed) and positive (2nd law). Its extremum reproduces the linear reduced EOM but is
**flat along η**: dσ/dη = 0 and dσ/dVar(z) = 0 (computed). Closures A and B have **identical dissipated
power and identical entropy production** on a fixed orbit (σ_A = σ_B to 1e-12, both footings). Fixed KMS T
does not lift the tie: 1/T is a common prefactor (dσ/dη|_T = 0). **MaxEP does not force η.**

**(b) Feynman–Vernon influence functional — WEIGHTING-BLIND** (`q1b_feynman_vernon.py`, the core). The
Herglotz measure ρ IS the bath spectral density J. Integrating out the Gaussian bath gives a **unique linear
retarded friction kernel γ(t)** (computed, monotone-decaying, both footings) — the LINEAR (2-point) response
is fixed. But the influence functional is quadratic and therefore blind to the 4-point Var(z) that η weights:
d(S_infl)/dη = 0, d(S_infl)/dVar(z) = 0 (computed). The **|a|-vs-history ambiguity SURVIVES** the reduction
as an irreducible operator-ordering freedom.

**(c) Fluctuation–dissipation theorem at T_dS — WEIGHTING-BLIND** (`q1c_fdt_split.py`). FDT/detailed balance
S_>(ω)/S_<(ω) = e^{ω/T} (verified symbolically) fixes the reactive/dissipative **split** uniquely
(Kramers-Kronig-locked; χ'' odd/causal, S_sym even — computed). But that split is **2-point** data. The
Gaussian KMS bath's **4th cumulant = 0** (computed) → there is **no 4th-order FDT relation** to constrain
Var(z). Detailed balance holds **identically** for closures A and B (they share the 2-point structure; T_eff
at a=a₀ is the closure-independent Pythagorean κ_eff/2π, both footings). **FDT does not force η.**

**(d) Passivity + analyticity of the reduced response — WEIGHTING-BLIND** (`q1d_passivity_analyticity.py`).
The reduced worldline response is passive/Herglotz (Im χ(ω) ≥ 0 at all sampled ω>0, sum rule ∫dμ/|t|=1 —
computed). Passivity is a **2-point** constraint satisfied **identically** by A and B (same measure). The
**adversarial construction** (honesty rail): sweep the full one-parameter family of admissible positive
Herglotz measures dμ_λ — the LINEAR friction γ(1) genuinely **moves** across the family (they are different
baths), but the η-distinguisher c₂ = ½K''(⟨z⟩) has **ZERO spread** (max−min = 0, computed) because it is a
property of the SYSTEM kernel K, orthogonal to the bath's 2-point data. No admissible bath giving a different
η can be built. **Passivity does not force η.**

### Q1 synthesis — CONSTANT (a NULL / no-selection), with a no-selection theorem

> **η(β) is a genuine irreducible theory CONSTANT.** All four ghost-free, KMS/detailed-balance-consistent,
> causality-respecting bath-reduction principles are **weighting-blind**, for one common, computed reason:

**No-selection theorem (sketch, proven both directions in the scripts).** Any ghost-free KMS-passive bath is
Herglotz-positive, hence a positive superposition of harmonic modes, hence **Gaussian** — its connected
cumulants above the 2nd vanish (`q1b` §1, `q1c` §2). Its Feynman–Vernon reduction is therefore an **exactly
quadratic** influence functional, which fixes the LINEAR (2-point) reduced response **uniquely** (the same
object for every candidate: friction kernel γ from the measure, FDT split, passive Herglotz χ) but contributes
**identically** to closures A and B, because they differ only by the **Jensen gap G(β) = ⟨K(z)⟩ − K(⟨z⟩)**, a
functional of the **connected 4-point Var(z)** that a quadratic functional cannot generate. To SELECT η you
would need a connected 4-point bath vertex = a **non-Gaussian** bath (κ₄ ≠ 0) = a **new self-interacting
field**, which the framework forbids (the bath is the dS-Unruh environment the kernel already encodes) **and**
which breaks the exact Herglotz/KL positivity that makes the reduction ghost-free. The adversarial sweep over
the full admissible Herglotz family confirms the η-distinguisher is invariant (zero spread). **∎ (as a
sketch — the load-bearing steps are the exit-0 computations, not this prose.)**

**Consequence for the numbers (unchanged, both footings):** the theory is **complete UP TO its constants
{s, a₀, Z, η}**. The dSph offset stays the bracket **[0.000 dex (closure A) … −0.02…−0.05 dex (closure B)]**;
overall sign of η free; the one forced, η-independent survivor is **d(offset)/d(radial-anisotropy) > 0**
(radially-anisotropic systems run hotter) — **MG-impossible**, and untouched by this lane.

---

## 2. Q2 — the eta-free NULL does not rest on the massless-conformal choice (mass-robustness)

`q2_massive_pole.py` (12/12, exit 0). The pullback used the massless conformal scalar as the representative dS
2-point function. Confirmed for **general mass**:

1. **The pole location is geometric.** The accelerated-worldline embedding gives the dS invariant
   **Z(Δτ) = s²cosh(κ_eff Δτ) + (1−s²)**, with **κ_eff² = H² + a² exactly** (computed, sympy) — the field
   mass **never enters**. Z = 1 ⟺ cosh(κ_eff Δτ) = 1 ⟺ κ_eff Δτ = 2πi n → nearest pole at
   **Δτ = 2πi/κ_eff** (verified).
2. **The massive dS Wightman function G(Z) = (H²/16π²)Γ(h₊)Γ(h₋)·₂F₁(h₊,h₋;2;(1+Z)/2)**, h± = 3/2 ± ν,
   ν=√(9/4 − m²/H²), is singular **only at coincidence Z=1** and its KMS images. Since c−a−b = −1, it is a
   **simple pole**, and the **LEADING coincidence coefficient is mass-independent** (Hadamard universality:
   d(coeff)/dν = 0, computed sympy — the Γ-factors cancel).
3. **Numerically**, across the conformal point (ν=1/2), complementary series (ν=1.2, 1.49), and the heavy
   **principal series** (ν=i·1.5), the full G(Z(Δτ)) **blows up at exactly Im(Δτ)=2π/κ_eff** in every case
   (|G| → 1.0×10⁵ at the pole vs O(1) off it), while |G(Z=0.5)| off the pole **differs** across masses
   (0.011 → 1.28): the mass shifts **residues / Matsubara weights**, **not the pole LOCATION**.
4. **The KMS temperature T_eff = κ_eff/2π** is therefore mass-independent; at a=a₀ the pole ratio is
   **κ_eff/H_Λ = √(1+1/Z²) = 1.01481** identically in **both footings** — matching the massless pullback.

**Q2 verdict:** the Pythagorean pole κ_eff = √(H²+a²) ≥ H_Λ — the fact that makes the pullback weighting-blind
— is **robust to the field mass**. The NULL does not rest on the massless choice.

---

## 3. Ledger

| # | Statement | Status |
|---|---|---|
| E-1 | η(β) is a nonlinear ordering (Jensen gap G=⟨K(z)⟩−K(⟨z⟩)); K concave, Var(z)↑ with orbit shape | **DERIVED** (q1b) |
| E-2 | Gaussian KMS-passive bath: cumulants n≥3 vanish → FV influence functional exactly quadratic | **DERIVED** (q1b,q1c) |
| E-3 | (a) MaxEP / min-dissipation: dσ/dη = 0, σ_A=σ_B → WEIGHTING-BLIND | **DERIVED** (q1a) |
| E-4 | (b) Feynman–Vernon: d(S_infl)/dη = d/dVar = 0; friction γ unique but 2-point → WEIGHTING-BLIND | **DERIVED** (q1b) |
| E-5 | (c) FDT split KK-locked but 2-point; κ₄=0, detailed balance common to A,B → WEIGHTING-BLIND | **DERIVED** (q1c) |
| E-6 | (d) Passivity 2-point; adversarial Herglotz sweep leaves η-distinguisher invariant → WEIGHTING-BLIND | **DERIVED** (q1d) |
| E-7 | **No-selection theorem:** any ghost-free KMS-passive (Gaussian) bath reduction is weighting-blind | **DERIVED (the crux)** |
| Q2-1 | κ_eff²=H²+a² geometric; massive G singular only at Z=1; leading coeff mass-independent | **DERIVED** (q2) |
| Q2-2 | Pole LOCATION Δτ=2πi/κ_eff mass-independent (conformal/complementary/principal); residues shift | **DERIVED** (q2) |
| P-1 | s=−1, a₀'s value, Z | **POSTULATE** (untouched) |

**Bottom line.** DYNAMICS does not do what KINEMATICS could not. Each of the four ghost-free,
KMS/detailed-balance-consistent, causality-respecting bath-reduction principles — max-entropy-production,
Feynman–Vernon, FDT, passivity+analyticity — is **weighting-blind**: it fixes the LINEAR (2-point) reduced
response uniquely but leaves the NONLINEAR operator-ordering **η(β)** (a connected-4-point Jensen gap) free.
This is a genuine **no-selection result**, proven as a theorem (any Gaussian KMS-passive reduction is
weighting-blind) rather than a failure to find a mechanism, and it is verified as rigorously as a "bath
selects η" WIN would have been — the adversarial construction of an alternative admissible bath giving a
different η **fails by computation**. The general-mass check confirms the NULL does not rest on the massless
choice. **The theory is complete UP TO its constants {s, a₀, Z, η}.** Both footings throughout; s=−1 and
a₀'s value remain postulates; c_T=1 and Cassini respected; no "theory complete/closed/proved" language.

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_eta_selection && for s in q1a_maxentropy
q1b_feynman_vernon q1c_fdt_split q1d_passivity_analyticity q2_massive_pole; do python3 $s.py; done` (all
exit 0). Sources read (frozen read-only repo + local prep, cited inline): `mi_closure_pin/PULLBACK.md`,
`CONSEQUENCES.md`, `pullback_dsunruh.py`, `ostro_nonlocal_verify.py`; `mi_field_theory/CLOSURE_MAP.md`,
`MATTER_COUPLING.md`; `opus_48_extended_research/reviews/mi_kernel_bath/theta_from_bath.py`,
`kernel_shape_from_wightman.py` (the repo's own bath work). Both a₀ footings throughout.*
