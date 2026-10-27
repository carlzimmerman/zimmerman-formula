import Mathlib

noncomputable section
namespace FrameworkEventStress

/-- Projection of completed-event particle stress, with conserved source
energy E₁+E₂ and source momentum projection a+b. -/
def stressJump (E₁ E₂ a b : ℝ) : ℝ :=
  a ^ 2 / E₁ + b ^ 2 / E₂ - (a + b) ^ 2 / (E₁ + E₂)

theorem completed_stress_identity (E₁ E₂ a b : ℝ)
    (h₁ : E₁ ≠ 0) (h₂ : E₂ ≠ 0) (hs : E₁ + E₂ ≠ 0) :
    stressJump E₁ E₂ a b =
      E₁ * E₂ / (E₁ + E₂) * (a / E₁ - b / E₂) ^ 2 := by
  unfold stressJump
  field_simp
  ring

theorem completed_stress_nonnegative (E₁ E₂ a b : ℝ)
    (h₁ : 0 < E₁) (h₂ : 0 < E₂) : 0 ≤ stressJump E₁ E₂ a b := by
  rw [completed_stress_identity E₁ E₂ a b h₁.ne' h₂.ne' (by positivity)]
  positivity

theorem projected_relative_motion_strict (E₁ E₂ a b : ℝ)
    (h₁ : 0 < E₁) (h₂ : 0 < E₂) (hv : a / E₁ ≠ b / E₂) :
    0 < stressJump E₁ E₂ a b := by
  rw [completed_stress_identity E₁ E₂ a b h₁.ne' h₂.ne' (by positivity)]
  exact mul_pos (by positivity) (sq_pos_of_ne_zero (sub_ne_zero.mpr hv))

/-- Every finite-dimensional spatial projection is nonnegative: PSD in
particular for three-dimensional completed particle events. -/
theorem every_spatial_projection_nonnegative {ι : Type*} (s : Finset ι)
    (E₁ E₂ : ℝ) (p₁ p₂ z : ι → ℝ) (h₁ : 0 < E₁) (h₂ : 0 < E₂) :
    0 ≤ (∑ i ∈ s, z i * p₁ i) ^ 2 / E₁ +
      (∑ i ∈ s, z i * p₂ i) ^ 2 / E₂ -
        (∑ i ∈ s, z i * (p₁ i + p₂ i)) ^ 2 / (E₁ + E₂) := by
  simp_rw [mul_add, Finset.sum_add_distrib]
  exact completed_stress_nonnegative E₁ E₂ _ _ h₁ h₂

end FrameworkEventStress
#print axioms FrameworkEventStress.completed_stress_identity
#print axioms FrameworkEventStress.completed_stress_nonnegative
#print axioms FrameworkEventStress.projected_relative_motion_strict
#print axioms FrameworkEventStress.every_spatial_projection_nonnegative

theorem false_unrelated_source : (0 : ℝ) ≤ 0 ^ 2 / 1 + 0 ^ 2 / 1 - 1 ^ 2 / 2 := by
  norm_num
