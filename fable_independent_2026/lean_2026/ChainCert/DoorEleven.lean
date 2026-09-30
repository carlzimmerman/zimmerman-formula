import Mathlib

/-!
# ChainCert.DoorEleven -- a vacuum-like medium (w = -1) carries no momentum flux in any frame, so it cannot "flow"

Door 11 asked whether the vacuum can act as a flowing medium.  Pure algebra of special-relativistic stress tensors:

* 1+1 boosts (`boost2 γ β`, with `γ^2 (1 - β^2) = 1` where needed): a perfect fluid at rest, `T = diag(ρ, p)`, seen from a boosted
  frame has momentum flux `T'^{01} = -(ρ + p) γ^2 β` (`boosted_flux`).  It vanishes for every boost when `p = -ρ`
  (`vacuum_no_flux`), and for a nonzero boost ONLY then (`flux_zero_iff`); the w = -1 tensor is boost-invariant
  (`vacuum_boost_invariant`): it has no rest frame, so no velocity field is defined by it.
* 1+3, covariant: for `T^{μν} = -ρ η^{μν}` and ANY unit timelike `u` (`u·η·u = -1`), the momentum density an observer with
  4-velocity u measures, `h^μ_α T^{αβ} u_β` with `h = δ + u u η`, is zero (`vacuum_momentum_density_zero`).
Conventions: signature (-,+,+,+); η = diag(-1, 1, 1, 1) is its own inverse (`eta4_mul_self`).
NOT certified: anything about a medium with w ≠ -1, the Door-11 flow models themselves, or any claim beyond this algebra.
-/

namespace DoorEleven

open Matrix

/-- the 1+1 Lorentz boost with Lorentz factor γ and speed β -/
def boost2 (γ β : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![γ, -(γ * β); -(γ * β), γ]

/-- a perfect fluid at rest in 1+1: T^{μν} = diag(ρ, p) -/
def fluidRest (ρ p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![ρ, 0; 0, p]

/-- the momentum flux of a fluid at rest, seen from a boosted frame: T'^{01} = -(ρ + p) γ^2 β -/
theorem boosted_flux (γ β ρ p : ℝ) :
    (boost2 γ β * fluidRest ρ p * (boost2 γ β)ᵀ) 0 1 = -(ρ + p) * γ ^ 2 * β := by
  simp [boost2, fluidRest, Matrix.mul_apply, Fin.sum_univ_two]
  ring

/-- w = -1: zero momentum flux in every boosted frame -/
theorem vacuum_no_flux (γ β ρ : ℝ) : (boost2 γ β * fluidRest ρ (-ρ) * (boost2 γ β)ᵀ) 0 1 = 0 := by
  rw [boosted_flux]; ring

/-- for a nonzero boost, zero momentum flux holds ONLY for w = -1 -/
theorem flux_zero_iff {γ β : ℝ} (hγ : γ ≠ 0) (hβ : β ≠ 0) (ρ p : ℝ) :
    (boost2 γ β * fluidRest ρ p * (boost2 γ β)ᵀ) 0 1 = 0 ↔ p = -ρ := by
  rw [boosted_flux]
  constructor
  · intro h
    have hγ2 : γ ^ 2 * β ≠ 0 := mul_ne_zero (pow_ne_zero 2 hγ) hβ
    have : -(ρ + p) * (γ ^ 2 * β) = 0 := by rw [← mul_assoc]; exact h
    have := (mul_eq_zero.mp this).resolve_right hγ2
    linarith
  · intro h; rw [h]; ring

/-- the w = -1 tensor is invariant under every Lorentz boost (γ^2 (1 - β^2) = 1): it defines no rest frame -/
theorem vacuum_boost_invariant {γ β : ℝ} (hL : γ ^ 2 * (1 - β ^ 2) = 1) (ρ : ℝ) :
    boost2 γ β * fluidRest ρ (-ρ) * (boost2 γ β)ᵀ = fluidRest ρ (-ρ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [boost2, fluidRest, Matrix.mul_apply, Fin.sum_univ_two] <;>
    first | ring1 | linear_combination ρ * hL | linear_combination (-ρ) * hL

/-- the 1+3 Minkowski metric, signature (-,+,+,+) -/
def eta4 : Matrix (Fin 4) (Fin 4) ℝ := Matrix.diagonal ![-1, 1, 1, 1]

theorem eta4_mul_self : eta4 * eta4 = 1 := by
  rw [eta4, Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
  congr 1
  ext i
  fin_cases i <;> simp

/-- the momentum density measured by an observer with 4-velocity u: h^μ_α T^{αβ} u_β, h = δ + u u_·, u_β = (η u)_β -/
def momDensity (T : Matrix (Fin 4) (Fin 4) ℝ) (u : Fin 4 → ℝ) : Fin 4 → ℝ :=
  T *ᵥ (eta4 *ᵥ u) + (dotProduct (eta4 *ᵥ u) (T *ᵥ (eta4 *ᵥ u))) • u

/-- 1+3: T^{μν} = -ρ η^{μν} (w = -1) has ZERO momentum density for EVERY unit timelike observer u -/
theorem vacuum_momentum_density_zero (ρ : ℝ) (u : Fin 4 → ℝ) (hu : dotProduct (eta4 *ᵥ u) u = -1) :
    momDensity ((-ρ) • eta4) u = 0 := by
  have hw : ((-ρ) • eta4) *ᵥ (eta4 *ᵥ u) = (-ρ) • u := by
    rw [Matrix.smul_mulVec, Matrix.mulVec_mulVec, eta4_mul_self, Matrix.one_mulVec]
  rw [momDensity, hw, dotProduct_smul, hu]
  ext i
  simp

end DoorEleven
