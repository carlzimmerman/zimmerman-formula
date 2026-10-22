/-
Copyright (c) 2026 Carl Zimmerman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: A83 lane
-/

import Mathlib

/-!
# A83 Block A — the A68 quadratic form: the 2×2 kinetic matrix, the α = γ single-stiffness conditio

Part of the A83 algebraic-spine formalization; see `A83_Spine.lean` for the sources and
the statement of what is and is not formalized.  No `axiom` declarations, no proof
holes, no kernel-bypassing evaluation.
-/

open Filter Matrix
open scoped Topology

noncomputable section

namespace A83

/-! ## Block A — the A68 quadratic form

A68 §3.1 gives the scalar-sector quadratic Lagrangian, with `A ≡ 2+3β`:
```
L/a³ = [−3A(ζ̇ − Hn)² + 2A(ζ̇ − Hn)Y − βY² + 2p²ζ² + 4p²nζ] / (4K)
       + p² n σ + (ηp²/2) σ̇² − ((Kp² + αp⁴)/2) σ² .
```
The kinetic block in the longitudinal/conformal pair `(ζ̇, σ̇)` is therefore the
2×2 matrix `Kmat` below (the `−3Aζ̇²` coefficient is A68 D1). -/

/-- A68 §3.1: the 2×2 longitudinal/conformal kinetic matrix, coefficients quoted
verbatim from the quadratic action (`K_ijK^ij − (1+β)θ² = −3Aζ̇² + …` at `Y = 0`,
and the P kinetic term `(ηp²/2)σ̇²`). -/
def Kmat (β η K p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-(3 * (2 + 3 * β)) / (4 * K), 0; 0, η * p ^ 2 / 2]

/-- Determinant of the A68 kinetic matrix: `−(3(2+3β)ηp²)/(8K)`. -/
theorem Kmat_det (β η K p : ℝ) (hK : K ≠ 0) :
    (Kmat β η K p).det = -(3 * (2 + 3 * β) * η * p ^ 2) / (8 * K) := by
  simp [Kmat, Matrix.det_fin_two]
  field_simp
  ring

/-- The A68 kinetic matrix is degenerate exactly when the θ-Legendre map is singular
(`2 + 3β = 0`, i.e. `β = −2/3`), or when the P kinetic term vanishes (`η = 0`), or at
zero momentum.  `K ≠ 0`. -/
theorem Kmat_det_eq_zero_iff (β η K p : ℝ) (hK : K ≠ 0) :
    (Kmat β η K p).det = 0 ↔ 2 + 3 * β = 0 ∨ η = 0 ∨ p = 0 := by
  rw [Kmat_det β η K p hK]
  have h8 : (8 : ℝ) * K ≠ 0 := mul_ne_zero (by norm_num) hK
  constructor
  · intro h
    have hnum : 3 * (2 + 3 * β) * η * p ^ 2 = 0 := by
      by_contra hc
      exact (div_ne_zero (neg_ne_zero.mpr hc) h8) h
    rcases mul_eq_zero.mp hnum with h1 | h1
    · rcases mul_eq_zero.mp h1 with h2 | h2
      · rcases mul_eq_zero.mp h2 with h3 | h3
        · norm_num at h3
        · exact Or.inl (by linarith)
      · exact Or.inr (Or.inl h2)
    · exact Or.inr (Or.inr ((pow_eq_zero_iff (n := 2) (by norm_num)).mp h1))
  · rintro (h | h | h)
    · have : 3 * (2 + 3 * β) * η * p ^ 2 = 0 := by rw [h]; ring
      rw [this]; ring
    · have : 3 * (2 + 3 * β) * η * p ^ 2 = 0 := by rw [h]; ring
      rw [this]; ring
    · have : 3 * (2 + 3 * β) * η * p ^ 2 = 0 := by rw [h]; ring
      rw [this]; ring

/-- Under the physical hypotheses `η ≠ 0`, `p ≠ 0`, `K ≠ 0`, the A68 kinetic matrix is
degenerate **iff** `β = −2/3` — A54's L8 / A68 §3.4 singular point of the θ Legendre
map. -/
theorem Kmat_degenerate_iff_beta (β η K p : ℝ) (hK : K ≠ 0) (hη : η ≠ 0) (hp : p ≠ 0) :
    (Kmat β η K p).det = 0 ↔ β = -(2 / 3) := by
  rw [Kmat_det_eq_zero_iff β η K p hK]
  constructor
  · rintro (h | h | h)
    · linarith
    · exact absurd h hη
    · exact absurd h hp
  · intro h; exact Or.inl (by linarith)

/-- A68 §3.1: the 2×2 gradient (stiffness) matrix of the two P polarizations, quoted
from the frozen action's `−(α/2)(D_iP^i)² − (γ/4)F_ijF^ij` block.  In the
`(longitudinal, transverse)` basis, `(D·P)² ↦ p⁴σ²` and `F² ↦ 2p²|P_T|²`, so the two
diagonal stiffnesses are `αp⁴` and `γp²` (A68 D16, D17). -/
def Gmat (α γ p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![α * p ^ 4, 0; 0, γ * p ^ 2]

/-- Determinant of the P-sector stiffness matrix: `αγp⁶`. -/
theorem Gmat_det (α γ p : ℝ) : (Gmat α γ p).det = α * γ * p ^ 6 := by
  simp [Gmat, Matrix.det_fin_two]
  ring

/-- The stiffness block is non-degenerate iff both gradient coefficients and the
momentum are non-zero. -/
theorem Gmat_det_ne_zero_iff (α γ p : ℝ) :
    (Gmat α γ p).det ≠ 0 ↔ α ≠ 0 ∧ γ ≠ 0 ∧ p ≠ 0 := by
  rw [Gmat_det]
  constructor
  · intro h
    refine ⟨?_, ?_, ?_⟩
    · intro hα; exact h (by rw [hα]; ring)
    · intro hγ; exact h (by rw [hγ]; ring)
    · intro hp; exact h (by rw [hp]; ring)
  · rintro ⟨hα, hγ, hp⟩
    exact mul_ne_zero (mul_ne_zero hα hγ) (pow_ne_zero 6 hp)

/-- A68 D16: the frozen action carries **one** stiffness in front of both gradient
operators iff `α = γ`.  Precisely: the stiffness matrix equals `γ` times the reference
matrix `diag(p⁴, p²)`. -/
theorem Gmat_single_stiffness_iff (α γ p : ℝ) (hp : p ≠ 0) :
    Gmat α γ p = γ • Gmat 1 1 p ↔ α = γ := by
  constructor
  · intro h
    have h00 : Gmat α γ p 0 0 = (γ • Gmat 1 1 p) 0 0 := by rw [h]
    have h00' : α * p ^ 4 = γ * p ^ 4 := by simpa [Gmat] using h00
    exact mul_right_cancel₀ (pow_ne_zero 4 hp) h00'
  · intro h
    rw [h]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Gmat]

/-- A68 §3.2: the fifth mode's kinetic coefficient `Z = Q = B + ηp²`,
`B = K(2+3β)/β`. -/
def Z (β η K p : ℝ) : ℝ := K * (2 + 3 * β) / β + η * p ^ 2

/-- A54's `Q₀ = (2+3β)/(Kβ) + ηk²/K²`; it is `Z/K²` (both appear in the record:
A54 uses `Q₀` for the `ζ` variable, A68 uses `Z` for `σ`). -/
def Q0 (β η K p : ℝ) : ℝ := (2 + 3 * β) / (K * β) + η * p ^ 2 / K ^ 2

/-- `Z > 0` for `K > 0`, `β > 0`, `η ≥ 0`, any `p`. -/
theorem Z_pos (β η K p : ℝ) (hK : 0 < K) (hβ : 0 < β) (hη : 0 ≤ η) :
    0 < Z β η K p := by
  unfold Z
  have h1 : 0 < K * (2 + 3 * β) / β := by positivity
  have h2 : 0 ≤ η * p ^ 2 := by positivity
  linarith

/-- A54's `Q₀` is exactly `Z/K²`. -/
theorem Q0_eq_Z_div_K_sq (β η K p : ℝ) :
    Q0 β η K p = Z β η K p / K ^ 2 := by
  unfold Q0 Z
  field_simp

/-- `Q₀ > 0` under the same hypotheses. -/
theorem Q0_pos (β η K p : ℝ) (hK : 0 < K) (hβ : 0 < β) (hη : 0 ≤ η) :
    0 < Q0 β η K p := by
  rw [Q0_eq_Z_div_K_sq]
  exact div_pos (Z_pos β η K p hK hβ hη) (pow_pos hK 2)

/-- A68 §3.2: the fifth mode's dispersion `ω² = αp⁴/Z`. -/
def omegaSq (α β η K p : ℝ) : ℝ := α * p ^ 4 / Z β η K p

/-- `ω² > 0` for `α > 0`, `p ≠ 0` and healthy `Z` (A68 D7). -/
theorem omegaSq_pos (α β η K p : ℝ) (hα : 0 < α) (hK : 0 < K) (hβ : 0 < β) (hη : 0 ≤ η)
    (hp : p ≠ 0) : 0 < omegaSq α β η K p := by
  have hp4 : 0 < p ^ 4 := by
    have h2 : 0 < p ^ 2 := by positivity
    calc 0 < (p ^ 2) ^ 2 := by positivity
      _ = p ^ 4 := by ring
  unfold omegaSq
  exact div_pos (mul_pos hα hp4) (Z_pos β η K p hK hβ hη)

/-- Exact factorization of the dispersion: `ω² = p⁴ · (α/Z)`. -/
theorem omegaSq_eq_p4_mul (α β η K p : ℝ) :
    omegaSq α β η K p = p ^ 4 * (α / Z β η K p) := by
  unfold omegaSq
  ring

/-- `ω²(0) = 0`: the first half of "vanishes to order 4 at `p = 0`". -/
theorem omegaSq_zero (α β η K : ℝ) : omegaSq α β η K 0 = 0 := by
  simp [omegaSq]

/-- The ratio `ω²/p⁴` tends to `αβ/(K(2+3β))` as `p → 0` through non-zero `p`.
Together with `omegaSq_zero` this is the precise statement that `ω²` **vanishes to
order exactly 4** at `p = 0`: order-4 vanishing means `ω²(p)/p⁴` has a finite
non-zero limit.  The punctured filter `𝓝[≠] 0` (not `𝓝 0`) is required because
Lean's division is total: `ω²/p⁴` is defined to be `0` at `p = 0`, so the ratio is
discontinuous at the origin even though its punctured limit is non-zero. -/
theorem omegaSq_div_p4_tendsto (α β η K : ℝ) (hβ : 0 < β) (hK : 0 < K) :
    Tendsto (fun p : ℝ => omegaSq α β η K p / p ^ 4) (𝓝[≠] 0)
      (𝓝 (α * β / (K * (2 + 3 * β)))) := by
  have hZ0 : Z β η K 0 = K * (2 + 3 * β) / β := by simp [Z]
  have hZ0ne : Z β η K 0 ≠ 0 := by
    rw [hZ0]; positivity
  have hcont : ContinuousAt (fun p : ℝ => Z β η K p) 0 := by
    unfold Z; fun_prop
  have hlim : Tendsto (fun p : ℝ => α / Z β η K p) (𝓝[≠] 0) (𝓝 (α / Z β η K 0)) :=
    (Tendsto.div tendsto_const_nhds hcont.tendsto hZ0ne).mono_left nhdsWithin_le_nhds
  have hval : α / Z β η K 0 = α * β / (K * (2 + 3 * β)) := by
    rw [hZ0]
    field_simp
  rw [hval] at hlim
  have heq : (fun p : ℝ => α / Z β η K p) =ᶠ[𝓝[≠] 0]
      (fun p : ℝ => omegaSq α β η K p / p ^ 4) := by
    filter_upwards [self_mem_nhdsWithin] with p hp
    have hp' : p ≠ 0 := by simpa using hp
    by_cases hZ : Z β η K p = 0
    · simp [omegaSq, hZ]
    · unfold omegaSq
      field_simp [hZ, hp', pow_ne_zero 4 hp']
  exact Tendsto.congr' heq hlim

end A83
