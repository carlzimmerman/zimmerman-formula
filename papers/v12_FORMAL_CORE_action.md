# v12 Formal Core — The Geometric Action and Compactification Data

**Date:** 2026-05-31
**Status:** the explicit action principle for v12, as a *geometric* (higher-dimensional
field-theory) framework — not string theory. Steps 1–2 of the roadmap, made concrete.

**Honest status up front.** This is a higher-dimensional **Einstein–Yang–Mills–Dirac**
theory. Gravity in D > 4 is non-renormalizable, so this is an **effective field theory**:
real and predictive below a cutoff Λ ≈ M_*, not UV-complete. It is "TOE-unify" in the
effective sense (one action → 4D gravity + SM-like gauge + 3 chiral generations). It does
**not** derive the parameter values (moduli-dependent), and Z² = 32π/3 enters as the value of
a geometric modulus (the volume), an **input**.

---

## 1. Spacetime and dimension

Total space **M = M₄ × K**, with internal space

> **K = (T²)³ / (Z₂×Z₂)** — six real internal dimensions.

So **D = 4 + 6 = 10**. (Note: this is a genuine change from the original 7-dimensional
M₄ × T³/Z₂. The even-dimensional internal space is *required* for a chiral index — the odd
T³/Z₂ has none — so the corrected framework is 10-dimensional. A minimal alternative is
M₄ × T² with magnetic flux, D = 6, giving generations from flux alone; the (T²)³/(Z₂×Z₂)
version is the one that realizes "three generations from three planes.")

Coordinates: x^μ (μ = 0..3) on M₄; three complex coordinates z_i = y^{2i−1} + τ_i y^{2i}
(i = 1,2,3), each parameterizing a T² with complex-structure modulus τ_i and area A_i.

---

## 2. The action

$$
S \;=\; \int_{M_{10}} d^{10}X \,\sqrt{-g}\;
\Big[\; \underbrace{\frac{1}{2\kappa_{10}^2}\,R}_{\text{gravity}}
\;-\; \underbrace{\frac{1}{4 g_{10}^2}\,\mathrm{Tr}\,F_{MN}F^{MN}}_{\text{gauge}}
\;+\; \underbrace{i\,\bar\Psi\,\Gamma^M D_M \Psi}_{\text{fermions}}
\;+\; \mathcal{L}_{\text{SUSY/Higgs}} \;\Big]
$$

with M, N = 0..9, and:

- **g_MN** — 10D metric; **R** — Ricci scalar; **κ₁₀²** = 8πG₁₀ (10D gravitational coupling).
- **Gauge group G** (an *input choice* — unlike string theory, a field-theory orbifold does
  not fix G by anomaly cancellation). Natural GUT choice: **G = E₆** (or SO(10)), to be
  broken toward the SM by the orbifold + Wilson lines. **F_MN** = ∂_M A_N − ∂_N A_M +
  [A_M, A_N]; **g₁₀** = 10D gauge coupling.
- **Ψ** — a 10D Majorana–Weyl fermion in a rep **R of G** (for E₆: the **27**, one
  generation's worth; for SO(10): the **16**). **Γ^M** — 10D Dirac matrices;
  **D_M = ∂_M + ¼ω_M^{ab}Γ_{ab} + A_M** (spin + gauge connection).
- **ℒ_SUSY/Higgs** — optional N = 1 (10D) SUSY completion (gravitino, gauginos), which the
  SUSY orbifold reduces to 4D N = 1; and/or a bulk scalar (Higgs) sector. Minimal version:
  drop SUSY, keep gravity + gauge + one bulk fermion.

This is the entire fundamental input: **one metric, one gauge field, one fermion multiplet,
three couplings (κ₁₀, g₁₀, and the GUT scale).**

---

## 3. The orbifold action (Z₂×Z₂) on the fields

The internal T⁶ = (T²)³ is acted on by the Klein four-group {1, θ, ω, θω}:

$$
\theta:(z_1,z_2,z_3)\mapsto(z_1,-z_2,-z_3),\qquad
\omega:(z_1,z_2,z_3)\mapsto(-z_1,z_2,-z_3),
$$

each with det = +1 (∈ SU(3)) — the condition that preserves N = 1 SUSY
(`reviews/z2z2_three_generations.py`). Three non-trivial elements → **three twisted
sectors**, one per 2-plane → family triplication.

The action lifts to the fields with a **gauge embedding**:

$$
\theta:\ \Psi \mapsto e^{2\pi i\,V_\theta\cdot H}\,\gamma_\theta\,\Psi,\qquad
\omega:\ \Psi \mapsto e^{2\pi i\,V_\omega\cdot H}\,\gamma_\omega\,\Psi,
$$

where γ_θ, γ_ω implement the spatial action on the 10D spinor index (the Clifford/chirality
piece — `reviews/orbifold_chirality_bridge.py`) and **V_θ, V_ω are shift vectors in the
Cartan subalgebra of G** (the gauge embedding — an *input choice*). Keeping only
(Z₂×Z₂)-invariant modes:
- breaks **G → H** (the unbroken 4D gauge group), and
- projects the higher-D fermion onto **4D chiral matter.**

---

## 4. Compactification data (the choices that define a model)

| Datum | Symbol | Role |
|---|---|---|
| Bulk gauge group | G (e.g. E₆) | input; broken to H ⊃ SM |
| Gauge embedding | V_θ, V_ω (Cartan shifts) | sets H and the matter reps |
| Magnetic fluxes | N_i = (1/2π)∫_{T²_i} F | chiral index → generations (`magnetized_torus_generations.py`) |
| Wilson lines | W_a (discrete holonomies) | H → SM; projects fixed-point multiplicity 16 → 1 |
| Discrete torsion | ε = ±1 | swaps (h^{1,1}, h^{2,1}); a sign choice |
| Complex structures | τ_i | moduli; set Yukawa textures |
| Areas / volume | A_i, V(K)=∏A_i | moduli; **Z² = 32π/3 is the volume in Planck units (input)** |

---

## 5. What reduces to 4D (schematic outcome)

KK reduction on K, keeping the orbifold-invariant zero modes:

- **4D gravity** (from g_μν) + **gauge group H ⊃ SU(3)×SU(2)×U(1)** (from A_μ, after embedding
  + Wilson lines).
- **Three chiral generations** (three twisted sectors; flux index N_i; Wilson-line projection
  16 → 1). The "exactly 3" requires the Wilson-line choice — a model-building input, not
  forced (`reviews/generation_number_tadpole_anomaly.py`).
- **Yukawa couplings** Y_{ijk}(τ_i, N_i) = wavefunction overlap integrals (Jacobi
  θ-functions of the moduli/flux) → mass hierarchies and mixings as **functions of the
  moduli.**
- **4D gauge coupling** 1/g₄² = V(K)/g₁₀² → α depends on the **volume modulus** (this is
  where "Z² = volume" would enter the gauge coupling — as an input value, not a derivation).

---

## 6. Honest accounting of this formal core

- **Real action principle:** yes — Einstein–Yang–Mills–Dirac, geometric, no strings. ✓
- **UV status:** effective field theory below Λ ≈ M_* (gravity non-renormalizable in D>4).
  Not a fundamental TOE; needs a UV completion at Λ (string theory is one option, not
  required for the EFT to be predictive below Λ).
- **Derived (structure):** 4D gauge group, chiral spectrum, generation triplication — from
  G + the orbifold + the embedding (the latter are choices).
- **Not derived (values):** all ~26 SM parameters — moduli-dependent (τ_i, fluxes, Wilson
  lines, volume). Same landscape limit as any compactification.
- **Z² = 32π/3:** the volume modulus VEV — an **input/ansatz**, not produced by the action.
- **The testable science is elsewhere:** the evolving-a₀ prediction (z > 10), independent of
  all of the above.

---

## 7. The honest next checkable step

Pick a **specific** (G, V_θ, V_ω, N_i, W_a) and *run steps 3–5*: compute the actual unbroken
group H, the chiral spectrum, and check whether it gives **SM × (hidden) with exactly 3
generations** and no exotics. That is a concrete, falsifiable model-building calculation
(it succeeds or it doesn't for a given choice), and it is the first place this formal core
makes contact with "is there a consistent model at all." It still will not derive the
parameter values — but it would establish the framework as a *real, explicit construction*.
