import Mathlib
noncomputable section
namespace KineticBound
-- Algebraic bound only; the analytic reduction is in RESULT.txt.
theorem sharp_identity (x : ℝ) :
 32*(1+x)^3-27*x*(x+2)^2=(x-2)^2*(5*x+8) := by ring

theorem sharp_bound (x : ℝ) (hx : 0 ≤ x) :
 27*x*(x+2)^2 ≤ 32*(1+x)^3 := by
 have h : 0 ≤ (x-2)^2*(5*x+8) := mul_nonneg (sq_nonneg _) (by linarith)
 rw [← sharp_identity] at h
 linarith

theorem strict_headroom : (32:ℝ)/27 < (9/8)^2 := by norm_num

theorem radial_squared_bound (x : ℝ) (hx : 0 ≤ x) :
 x*(x+2)^2/(1+x)^3 < (9/8)^2 := by
 have hp : 0 < (1+x)^3 := by positivity
 apply (div_lt_iff₀ hp).2
 have h := sharp_bound x hx
 nlinarith

theorem transverse_squared_bound (x : ℝ) (hx : 0 ≤ x) :
 x/(1+x) < (9/8)^2 := by
 apply (div_lt_iff₀ (by positivity : 0 < 1+x)).2
 nlinarith

#print axioms sharp_identity
#print axioms sharp_bound
#print axioms strict_headroom
#print axioms radial_squared_bound
#print axioms transverse_squared_bound
end KineticBound
