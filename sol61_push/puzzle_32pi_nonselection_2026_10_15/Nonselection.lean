import Mathlib
noncomputable section
namespace VacuumNonselection

-- D = M_Pl^2 * a0^2; E is the independently adjustable vacuum energy.
def ratio (E D : ℝ) : ℝ := E / D

theorem any_positive_ratio (D target : ℝ) (hD : 0 < D) (ht : 0 < target) :
    ∃ E : ℝ, 0 < E ∧ ratio E D = target := by
  refine ⟨target*D, mul_pos ht hD, ?_⟩
  unfold ratio
  exact mul_div_cancel_right₀ target (ne_of_gt hD)

-- Explicit assumption: the acceptance test depends on response parameters,
-- but not on E. This is not an assertion about all gravitational models.
theorem diagnostics_cannot_select {P : Type*} (accepted : P → Prop)
    (p : P) (hp : accepted p) (D : ℝ) (hD : 0 < D) :
    ∃ E₁ E₂ : ℝ, accepted p ∧ 0 < E₁ ∧ 0 < E₂ ∧
      ratio E₁ D ≠ ratio E₂ D := by
  refine ⟨D, 2*D, hp, hD, by positivity, ?_⟩
  unfold ratio
  simp [ne_of_gt hD]

theorem explicit_32pi_64pi (D : ℝ) (hD : 0 < D) :
    ratio (32*Real.pi*D) D = 32*Real.pi ∧
    ratio (64*Real.pi*D) D = 64*Real.pi ∧
    32*Real.pi ≠ 64*Real.pi := by
  unfold ratio
  constructor
  · exact mul_div_cancel_right₀ _ (ne_of_gt hD)
  constructor
  · exact mul_div_cancel_right₀ _ (ne_of_gt hD)
  · nlinarith [Real.pi_pos]

-- Round S4 identity gives a0^4 Omega = 24*pi^2 / (Lambda/a0^2)^2.
theorem round_sphere_values :
    24*Real.pi^2/(32*Real.pi)^2 = (3:ℝ)/128 ∧
    24*Real.pi^2/(64*Real.pi)^2 = (3:ℝ)/512 := by
  have hp : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  constructor <;> field_simp <;> ring

theorem reference_gradient_passes :
    0 < (-200*(1:ℝ)^4-200*1^3-298*1^2+9702*1-99) := by norm_num

#print axioms any_positive_ratio
#print axioms diagnostics_cannot_select
#print axioms explicit_32pi_64pi
#print axioms round_sphere_values
#print axioms reference_gradient_passes
end VacuumNonselection
