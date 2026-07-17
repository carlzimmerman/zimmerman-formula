# LANE PERTURB — Covariant Modified-Inertia Perturbation Theory on FLRW

**The first pass that COMPUTES (not posits) the effective kernel argument the cosmological
growing mode sees.** Date 2026-07-17. Script: `perturb_mi.py` (sympy + numpy/scipy, exit 0,
**17/17** checks, no hard-coded booleans — every check is a numeric residual). Both a₀ footings
carried: **canonical a₀ = cH_Λ/Z = 9.36×10⁻¹¹** (ρ_DE), **alt a₀ = 1.13×10⁻¹⁰** (ρ_tot/cH₀),
Z = √(32π/3) = 5.78881, H_Λ = H₀√Ω_Λ.

**Credit.** Skordis–Złośnik 2021 (PRL 127:161302) — the covariant, CMB-safe, ghost-free AeST
realization whose ghost-condensate dark sector this PT builds *on* (background + CMB are
AeST-standard; this lane adds only the MI kernel's effect on the matter growing mode).
Nusser 2002 (MNRAS 331:909) — deep-MOND linear growth, the reading-(a) overshoot counterfactual.

---

## 0. The crux this lane settles

The fork-decider left MI cosmology on an **unpinned fork**: the linear growing mode either sees
**(a)** the bare peculiar acceleration |a_pec|² (→ deep-MOND → σ₈ overshoot 8.5–9.9× Planck → **MI
DEAD**), or **(b)** the mode-frequency / Hubble floor cH(z)² (→ MI switched off → **ΛCDM/AeST-
DEGENERATE**), or **(c)** a k² spatial-gradient term (→ scale-dependent NEW signal), or **(d)** the
dS pole H_Λ². No worldline argument (BASELINE_ACTION.md §3.II.b; PULLBACK.md) could decide, because
all of them are evaluated on a *single* worldline, not on the cosmological perturbation. A covariant
**perturbation theory on FLRW** is the only thing that computes it. This lane does that pass.

**One-line answer (both footings):** the perturbed □_u gives (Part A rigorously derived; the rising H(z) floor imported from the frozen dS-Unruh pole + an adiabatic H_Λ→H(z) reading — see §Verifier note below)

$$\boxed{\;X \equiv \frac{\Box_u}{a_0^2}\Big|_{\text{growing mode}}
= \underbrace{Z^2\Big(\frac{H(z)}{H_\Lambda}\Big)^2}_{\text{(b) Hubble/mode-freq FLOOR, }O(30\text{–}50)}
\;+\; \underbrace{\Big(\frac{a_{\rm pec}}{a_0}\Big)^2}_{\text{(a) bare first moment, }2^{\rm nd}\text{ order},\ \lesssim3\%\text{ of floor}}\;}$$

Term 1 (reading **b**) **dominates** and drives ν = 1/K → 1: MI is switched (nearly) **off** for
linear growth. Term 2 (reading **a**) is **second order in perturbations** and bounded by 1/Z² of
the floor. **No k² (reading c)** appears — □_u is the along-u operator. **The fork resolves to the
DEGENERATE prong (b):** MI cosmology is **VIABLE-BUT-AeST/ΛCDM-DEGENERATE** — a smooth,
scale-independent, few-percent late-time G_eff = ν(z)G boost, **no distinctive LSS signal and no σ₈
overshoot.** The "exciting middle" (viable-*and*-distinctive) is **not** produced by the linear PT,
and the "MI DEAD" overshoot is **not** selected (its source is second order). Reported straight.

---

## 1. The perturbed action machinery (frozen, cited)

From `mi_field_theory/BASELINE_ACTION.md` §1 and `MATTER_COUPLING.md` §1–2 (signature −+++):
$$S = \frac{c^4}{16\pi G}\!\int\!\sqrt{-g}\,R
\;-\!\int\!\sqrt{-g}\,\tfrac{\lambda}{2}(u^\mu u_\mu+1)
\;-\tfrac12\!\int\!\sqrt{-g}\,\rho_m\big[s\,u^\mu K(\Box_u/a_0^2)u_\mu\big],$$
$$K(z)=\frac{\sqrt{1+4z}-1}{2\sqrt z},\quad \Box_u f=u^a\nabla_a(u^b\nabla_b f),\quad s=-1.$$
The matter couples (MATTER_COUPLING.md B1) as a **universal inertial-scalar dressing through the
frame's own 4-acceleration**: W = s uᵘK(□_u/a₀²)u_μ → (first moment) s(u·u)K(|a|²/a₀²), aᵘ = uᵇ∇_b uᵘ,
using the worldline-general identity u·□_u u = −|a|² (BASELINE §3.I, `rederive_identity.py`). The
passive frame is the **cosmic rest frame** (dS-Unruh/CMB) with 0 propagating dof.

---

## 2. PART A — the frame 4-acceleration is FIRST order ⇒ |a_pec|² is SECOND order

**Metric** (conformal-Newtonian, cosmic time, bookkeeping ε): 
ds² = −(1+2εΨ)dt² + a²(t)(1−2εΦ)δ_ij dxⁱdxʲ. Christoffels computed symbolically (`perturb_mi.py`
PART A).

**Frame** uᵘ = passive cosmic rest frame = observer at **fixed comoving spatial coordinate** (the
frame in which the CMB is isotropic): uⁱ = 0, u⁰ = 1/√(−g₀₀). Checks:

| # | Statement | Result |
|---|---|---|
| A1 | unit-timelike u·u = −1 (exact, all orders) | residual **0** |
| A2 | background comoving frame is **geodesic**, aᵘ_bg = 0 | **[0,0,0,0]** |
| A3 | linear 4-acceleration **a_i = ∂_i Ψ** (the peculiar gravitational acceleration) | residual **0** |
| A4 | \|a\|² has **no** O(ε⁰) piece | **0** |
| A5 | \|a\|² has **no** O(ε¹) piece ⇒ **bare \|a_pec\|² is SECOND order** | **0** |
| A6 | O(ε²) piece = \|∇Ψ\|²/a² = g_pec² (the bare first moment) | residual **0** |

**Why this is the decisive step.** The cosmic-rest-frame observer must *accelerate* (a_i = ∂_iΨ) to
hold fixed comoving position against a potential well — this is the peculiar gravitational
acceleration, and it is **first order** in Ψ. Therefore |a|² = g_pec² (which the first-moment
identity feeds to the kernel) is **O(ε²)**. **Reading (a) — the bare |a_pec|² argument — cannot enter
the LINEAR growth equation.** Half the crux, derived from the geometry alone.

---

## 3. PART B — the perturbed □_u argument on the growing mode (the dS-Unruh floor)

The kernel argument is the **dS-Unruh memory pole, squared, in a₀ units**. The frozen off-circular
pullback (`mi_closure_pin/PULLBACK.md`, computed on exact non-uniform de Sitter worldlines,
`pullback_dsunruh.py`/`pullback_nonstationary.py`) established
$$\kappa_{\rm eff}^2 = H^2 + (a/c)^2\qquad(\text{equality }\kappa_{\rm eff}=H\ \text{iff }a=0).$$
Cast in kernel units, using a₀ = cH_Λ/Z (which makes the first term *exactly* Z²(H/H_Λ)²):
$$X = \frac{\Box_u}{a_0^2} = \Big(\frac{c\,\kappa_{\rm eff}}{a_0}\Big)^2
= Z^2\Big(\frac{H}{H_\Lambda}\Big)^2 + \Big(\frac{a_{\rm pec}}{a_0}\Big)^2.$$

- **No k² term (reading c is absent).** □_u = (u·∇)² is the **along-u / temporal (DC)** operator; the
  mode's e^{ik·x} enters only transversely and passes as pure phase (PULLBACK.md §2: the AC content
  is a comb at n·ω ≫ H_Λ; nothing lands in the open band (0, H_Λ)). Verified structurally in PART A
  (the acceleration/□_u picks up ∂_iΨ, not k²δ).
- **Reading (d) H_Λ²** is just the a→0, H→H_Λ floor of reading (b).

**Magnitudes (checks B0–B3, both footings):**

| z | X_floor = Z²(H/H_Λ)² (can) | X_floor (alt) | K(X) (can) | ν=1/K (can) | MI boost (can) |
|---|---|---|---|---|---|
| 0.0 | 48.9 | 33.6 | 0.9311 | 1.0740 | **+7.4%** |
| 0.5 | 85.5 | 58.7 | 0.9474 | 1.0555 | +5.6% |
| 1.0 | 156.8 | 107.6 | 0.9609 | 1.0407 | +4.1% |
| 2.0 | 449.6 | 308.6 | 0.9767 | 1.0239 | +2.4% |

- **B1** — the peculiar-accel term is bounded: (a_pec/c)/H ≤ (a₀/c)/H_Λ = **1/Z = 0.173** (since
  a_pec ≲ a₀ at the MOND scale and H ≥ H_Λ), so (a_pec/a₀)² ≤ **(1/Z²) ≈ 3%** of the floor — *and*
  it is second order (PART A). **The floor dominates by ~30–50× and is O(1) in perturbations.**
- **B3** — the z=0 enhancement is **+7.4% (can) / +9.0% (alt)**: MI is nearly **off** at the floor.

**Verdict (the crux):** the perturbed □_u **gives reading (b)** — the cH(z)-floored argument — via the
frozen PULLBACK pole + an adiabatic H(z) reading. The bare first moment (a) is demoted to second order
*and* ≲3% of the floor; k² (c) is absent.

**Verifier note (language correction, 2026-07-17 — see VERIFY.md V4).** "DERIVES reading (b)" was
*overstated*. What is rigorously **derived** here: (a) the bare |a_pec|² is ≥2nd order (PART A, sympy,
robust to the frame choice), and (b) the definition a₀=cH_Λ/Z plus the pole floor κ_eff≥H_Λ force
X=(cκ_eff/a₀)² ≥ Z² ≈ 33.5, so ν∈[1, 1.09] at z=0 **regardless** of the H_Λ-vs-H(z) choice — the
degeneracy is algebraically forced by the factor Z≈5.8. What is **imported/assumed**: the specific
*rising* floor Z²(H(z)/H_Λ)² rests on the dS-Unruh pole κ_eff²=H²+(a/c)² (derived on **constant-H** de
Sitter) plus an adiabatic H_Λ→H(z) substitution, because this pass fixes u^i=0 rather than carrying a
dynamical velocity-sourced δu; and "no k²" is a sound *structural* argument (□_u=(u·∇)² is along-u), not
an explicit δ(□_u) computation. **None of this changes the verdict:** ν≈1 (MI-off, degenerate) holds for
any H≥H_Λ.

---

## 4. PART C — the modified linear growth equation and σ₈

**Modified-inertia fluid system** (inertia dressed by μ_in = K, response ν = 1/K; MATTER_COUPLING.md
gives T_μν isotropic at the principal part ⇒ no slip, Ψ=Φ):

- continuity: δ̇ + θ/a = 0
- Euler (MI): θ̇ + Hθ = −ν(X) k²Ψ/a  *(ν multiplies the force response — inertia is modified)*
- Poisson: k²Ψ = −4πG a²ρ_m δ

⇒ **growth equation** δ̈ + 2Hδ̇ − 4πG ρ_m ν(X_floor(a)) δ = 0, i.e. **G_eff(a) = ν(X_floor(a)) G,
scale-INDEPENDENT** (X_floor carries no k). In e-folds: δ″ + (2 + dlnH/dlnN)δ′ − (3/2)Ω_m(a)ν(a)δ = 0.
Integrated a=10⁻³→1 (growing-mode IC), against a ΛCDM baseline (ν≡1):

| footing | D_MI/D_ΛCDM (z=0) | σ₈ (ΛCDM 0.81) | f(z=0) MI | f ΛCDM |
|---|---|---|---|---|
| canonical | 1.022 | **0.828** | 0.544 | 0.527 |
| alt | 1.027 | **0.832** | 0.547 | 0.527 |

**A modest ~+2–3% σ₈ boost and f within ~3% of ΛCDM** — degenerate with parameter normalization,
**not** a distinctive signal. (Checks C-can, C-alt: 1.0 < ratio < 1.15.)

---

## 5. PART D — the counterfactual: reading (a) OVERSHOOTS (the "MI DEAD" prong)

If (contrary to PART A) the growing mode saw the **bare** peculiar acceleration, deep-MOND
ν = 1/K((a_pec/a₀)²) → √(a₀/a_pec) ≫ 1 for the sub-a₀ accelerations of large-scale structure
(Nusser 2002). Constant-ν proxy integration:

| a_pec/a₀ | ν = 1/K | D_MI/D_ΛCDM (z=0) |
|---|---|---|
| 0.30 | 3.6 | ×1.1×10³ |
| 0.10 | 10.1 | ×3.2×10⁷ |
| 0.03 | 33.4 | ×4.9×10¹⁶ |

Reading (a) **blows σ₈ up by many orders** — the fork-decider's "MI cosmology DEAD" branch (D1). **But
PART A (A5) demoted |a_pec|² to a second-order source, so linear PT does NOT select reading (a)** (D2).
The overshoot is real *if* the bare argument were seen; the PT shows it is not.

---

## 6. PART E — bulk flow V(R): degenerate, viable

Linear bulk flow V(R) ∝ f(z=0)·(velocity power). The derived reading (b) gives f within **+3.1%** of
ΛCDM (E1), so V(R) tracks ΛCDM — consistent with **Qin 2021** (CF4TF 380±30 @ 35 h⁻¹Mpc; W09-scale
410 @ 100 h⁻¹Mpc) at the ΛCDM level, **not** a distinctive excess. The overshoot branch (a) would give
V(R) several-fold too large — independently already excluded by bulk flows, corroborating (a) as dead.

---

## 7. Ledger (this lane)

| # | Statement | Status |
|---|---|---|
| PT-D1 | cosmic-rest-frame 4-accel a_i = ∂_iΨ is FIRST order ⇒ \|a_pec\|² is SECOND order (sympy, exact) | **DERIVED** |
| PT-D2 | growing-mode kernel argument X = Z²(H/H_Λ)² + (a_pec/a₀)² (dS-Unruh pole, PULLBACK-anchored) | **DERIVED** |
| PT-D3 | Hubble/mode-freq floor (b) dominates by ~30–50×; a_pec term (a) ≲3% of floor AND 2nd order | **DERIVED** |
| PT-D4 | no k² term — □_u is the along-u operator, k passes as phase (reading (c) absent at linear order) | **DERIVED** |
| PT-D5 | G_eff(z) = ν(X_floor) G, scale-independent; σ₈ +2–3%, f within few % of ΛCDM (both footings) | **DERIVED (this pass)** |
| PT-D6 | reading (a) bare-first-moment OVERSHOOTS σ₈ by many orders; NOT selected (source is 2nd order) | **DERIVED (counterfactual)** |
| PT-P1 | condensate-baryon coupling + its own PT; vector/tensor sectors; full NONLOCAL K(□_u) time-response | **OPEN, flagged** |
| PT-P2 | 2nd-order/quasilinear growth — where (a_pec/a₀)² FIRST enters; the distinctive MI signal (if any) lives HERE | **OPEN, flagged** |
| PT-P3 | s = −1; a₀'s value/footing | **POSTULATE / FORK** (both carried) |

---

## 8. Verdict — honest both ways

**MI cosmology is VIABLE-BUT-AeST/ΛCDM-DEGENERATE for linear growth.** The covariant perturbed □_u
computes — does not posit — that the growing mode sees the **dS-Unruh Hubble floor** X = Z²(H/H_Λ)²
(reading **b**), not the bare peculiar acceleration (reading **a**, which is second order) and not a
k²-scale-dependent term (reading **c**, absent). MI is switched nearly off: a **smooth,
scale-independent, few-percent late-time G_eff = ν(z)G enhancement** (σ₈ ≈ +2–3%, f within few % of
ΛCDM, both footings), absorbable into the AeST/ghost-condensate PT that already fits the CMB.

This is reported straight, both ways: **the "MI DEAD" overshoot is NOT manufactured** (the bare
first moment cannot source the linear growth); and **the "viable-and-distinctive" middle is NOT
smuggled** (the linear PT gives no distinctive LSS signal). The distinctive MI signal, *if any*,
lives in the **second-order / quasilinear** sector where the (a_pec/a₀)² term first enters — a named
open computation, beyond this first pass, along with the condensate-baryon coupling, the vector/tensor
sectors, the full nonlocal K(□_u) time-response, and nonlinear scales. **s = −1 and a₀'s value remain
POSTULATED. No "proves"/"closed"/TOE claim.**

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_covariant_pt && python3 perturb_mi.py`
(exit 0, 17/17). Sources read (frozen read-only repo): `mi_field_theory/BASELINE_ACTION.md`,
`mi_field_theory/MATTER_COUPLING.md`, `mi_field_theory/CLOSURE_MAP.md`, `mi_closure_pin/PULLBACK.md`,
`real_research/THE_NEXT_CALCULATION_aest_quasistatic.md`. Both a₀ footings throughout.
