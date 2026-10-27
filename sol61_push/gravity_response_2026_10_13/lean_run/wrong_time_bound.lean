import Mathlib

/-! Conditional finite-time response bounds. The field reduction and Poisson
completion remain analytical/physical hypotheses, not formalized field theory. -/
noncomputable section
namespace GravityResponse

theorem stable_step_bound (J w t : ℝ) (hJ : 0 ≤ J) (hw : w ≠ 0) :
    2 * J * Real.sin (w * t / 2) ^ 2 / w ^ 2 ≤ J * t ^ 2 / 4 := by
  have hs : Real.sin (w * t / 2) ^ 2 ≤ (w * t / 2) ^ 2 := Real.sin_sq_le_sq
  have hmul := mul_le_mul_of_nonneg_left hs (show 0 ≤ 2 * J by positivity)
  apply (div_le_iff₀ (sq_pos_of_ne_zero hw)).mpr
  nlinarith [hmul]

theorem response_nonnegative (J w t : ℝ) (hJ : 0 ≤ J) :
    0 ≤ 2 * J * Real.sin (w * t / 2) ^ 2 / w ^ 2 := by positivity

theorem static_gain (J omega2 : ℝ) (hw : omega2 ≠ 0) :
    1 + J / omega2 = (omega2 + J) / omega2 := by field_simp

theorem density_time_requirement (R G rho t : ℝ)
    (h : R ≤ (4 * Real.pi * G * rho) * t ^ 2 / 2)
    (hG : 0 < G) (ht : t ≠ 0) :
    R / (2 * Real.pi * G * t ^ 2) ≤ rho := by
  apply (div_le_iff₀ (by positivity : 0 < 2 * Real.pi * G * t ^ 2)).mpr
  nlinarith [h]

theorem density_amplitude_force (G eta rho L : ℝ) (hL : L ≠ 0) :
    4 * Real.pi * G * (eta * rho) / (2 * Real.pi / L) = 2 * G * eta * rho * L := by
  field_simp
  ring

end GravityResponse
#print axioms GravityResponse.stable_step_bound
#print axioms GravityResponse.response_nonnegative
#print axioms GravityResponse.static_gain
#print axioms GravityResponse.density_time_requirement
#print axioms GravityResponse.density_amplitude_force
