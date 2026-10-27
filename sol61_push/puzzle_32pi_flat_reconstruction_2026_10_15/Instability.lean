import Mathlib
noncomputable section
namespace FlatReconstruction

theorem rayleigh_identity (p L : ℝ) (hL : L ≠ 0) :
    p^2/(2*L)-7*L/8 = (4*p^2-7*L^2)/(8*L) := by
  field_simp
  <;> ring

theorem negative_trial_form (p L : ℝ) (hL : 0 < L)
    (hspan : 4*p^2 < 7*L^2) : p^2/(2*L)-7*L/8 < 0 := by
  rw [rayleigh_identity p L (ne_of_gt hL)]
  exact div_neg_of_neg_of_pos (by linarith) (by positivity)

theorem log_profile_curvature_negative (r : ℝ) (hr : 0 < r) :
    -(2:ℝ)/r^2 < 0 := by
  exact div_neg_of_neg_of_pos (by norm_num) (by positivity)

#print axioms rayleigh_identity
#print axioms negative_trial_form
#print axioms log_profile_curvature_negative
end FlatReconstruction
