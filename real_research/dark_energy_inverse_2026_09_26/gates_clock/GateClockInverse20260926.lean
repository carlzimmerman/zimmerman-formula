import Mathlib

/-! Conditional algebraic inverses. This file does not derive the dispersion,
stress tensor or environment model from a physical action. -/
namespace GateClockInverse20260926

theorem two_environment_inverse (D₁ D₂ b p l₁ l₂ : ℝ)
    (h₁ : D₁ = b - p * l₁) (h₂ : D₂ = b - p * l₂)
    (hne : l₁ ≠ l₂) : p = (D₂ - D₁) / (l₁ - l₂) := by
  apply (eq_div_iff (sub_ne_zero.mpr hne)).2
  rw [h₁, h₂]
  ring

theorem stress_sum_and_shift (K V C delta : ℝ) :
    (K + V + C) + (K - V - C) = 2 * K ∧
    (K + V + (C + delta)) + (K - V - (C + delta)) = 2 * K := by
  constructor <;> ring

theorem dispersion_total_inverse (u q : ℝ) (hu : 0 < u) (hq : 0 < q) :
    (1 - u / (u + 4 * q)) ^ 2 / (16 * q ^ 2 / (u + 4 * q) ^ 3) =
      u + 4 * q := by
  have hA : u + 4 * q ≠ 0 := ne_of_gt (by positivity)
  have hq0 : q ≠ 0 := ne_of_gt hq
  field_simp
  ring

theorem dispersion_charge_inverse (u q : ℝ) (hu : 0 < u) (hq : 0 < q) :
    (1 - u / (u + 4 * q)) ^ 3 / (4 * (16 * q ^ 2 / (u + 4 * q) ^ 3)) =
      q := by
  have hA : u + 4 * q ≠ 0 := ne_of_gt (by positivity)
  have hq0 : q ≠ 0 := ne_of_gt hq
  field_simp
  ring

end GateClockInverse20260926
#print axioms GateClockInverse20260926.two_environment_inverse
#print axioms GateClockInverse20260926.stress_sum_and_shift
#print axioms GateClockInverse20260926.dispersion_total_inverse
#print axioms GateClockInverse20260926.dispersion_charge_inverse
