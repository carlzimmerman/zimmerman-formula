import Mathlib

/-! CFG312 MUTATE: the dust threshold moved from 2/3 to 3/4 and the universal fluid bound without the
null-energy hypothesis. Both statements are false, so this file must NOT compile. -/

theorem dust_pos_mutated (ρ X : ℝ) (hρ : 0 < ρ) (hX : X < 3 / 4) : 0 < ρ * (2 - 3 * X) := by
  apply mul_pos hρ; linarith

theorem fluid_bound_mutated (ρ p c X : ℝ) (hρ : 0 ≤ ρ) (hc : 0 ≤ c) (hX : 0 ≤ X) (hth : (2 - c) * X ≤ 1) :
    2 * ρ * (1 - X) ^ 2 ≤ 2 * ρ - 3 * ρ * X + p * X - 2 * p * X ^ 2 + (ρ + p) * c * X ^ 2 := by
  nlinarith
