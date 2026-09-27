import Mathlib

noncomputable section
namespace ReciprocalVacuum20260926

def F (t : ℝ) := 1 + (t + 1 / t - 2)^2
def curvature (t : ℝ) := 2 - 8 / t^3 + 6 / t^4

theorem quartic_identity (t : ℝ) (ht : t ≠ 0) :
    F t = 1 + (t-1)^4/t^2 := by
  unfold F
  field_simp
  ring

theorem inverse_identity (t : ℝ) (ht : t ≠ 0) : F (1/t) = F t := by
  unfold F
  field_simp
  ring

theorem positive_floor (t : ℝ) : 1 ≤ F t := by
  unfold F
  nlinarith [sq_nonneg (t + 1/t - 2)]

theorem curvature_factor (t : ℝ) (ht : t ≠ 0) :
    curvature t = 2*(t-1)^2*(t^2+2*t+3)/t^4 := by
  unfold curvature
  field_simp
  ring

theorem curvature_nonnegative (t : ℝ) (ht : 0 < t) : 0 ≤ curvature t := by
  rw [curvature_factor t (ne_of_gt ht)]
  positivity

theorem vacuum_value : F 1 = 1 := by norm_num [F]
theorem zero_curvature : curvature 1 = 0 := by norm_num [curvature]

theorem Laurent_selection (a t : ℝ) (ht : t ≠ 0) :
    a*(t^2+1/t^2)-4*a*(t+1/t)+(1+6*a) = 1+a*(F t-1) := by
  unfold F
  field_simp
  ring

end ReciprocalVacuum20260926
#print axioms ReciprocalVacuum20260926.quartic_identity
#print axioms ReciprocalVacuum20260926.inverse_identity
#print axioms ReciprocalVacuum20260926.positive_floor
#print axioms ReciprocalVacuum20260926.curvature_factor
#print axioms ReciprocalVacuum20260926.curvature_nonnegative
#print axioms ReciprocalVacuum20260926.vacuum_value
#print axioms ReciprocalVacuum20260926.zero_curvature
#print axioms ReciprocalVacuum20260926.Laurent_selection
