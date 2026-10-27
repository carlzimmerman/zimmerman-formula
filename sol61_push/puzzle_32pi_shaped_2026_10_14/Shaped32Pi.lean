import Mathlib

/-! Conditional polynomial bounds. The geometric and perturbation dictionaries
are derived in RESULT.txt/check.py, not formalized in this certificate. -/
namespace Shaped32Pi

theorem shape_bounds (A t : ℝ) (hA : 0 ≤ A) (hA' : A ≤ 1/16)
    (ht : -1 ≤ t) (ht' : t ≤ 1) :
    15/16 ≤ 1-A*t^2 ∧
    11/8 ≤ 2-2*A*t^2+t*(1-t^2)/2 ∧
    2-2*A*t^2+t*(1-t^2)/2 ≤ 5/2 := by
  have hs : t^2 ≤ 1 := by nlinarith [sq_nonneg t]
  have hnon : 0 ≤ 1-t^2 := by linarith
  have hprod : 0 ≤ A*t^2 := mul_nonneg hA (sq_nonneg t)
  have hup : A*t^2 ≤ 1/16 := by
    have := mul_le_mul_of_nonneg_left hs hA
    nlinarith
  have hlow : -1 ≤ t*(1-t^2) := by
    have := mul_nonneg (by linarith : 0 ≤ t+1) hnon
    nlinarith [sq_nonneg t]
  have hhigh : t*(1-t^2) ≤ 1 := by
    have := mul_nonneg (by linarith : 0 ≤ 1-t) hnon
    nlinarith [sq_nonneg t]
  constructor
  · nlinarith
  constructor <;> nlinarith

theorem both_speeds_positive (w q : ℝ) (hw : 0 ≤ w) (hw' : w ≤ 1)
    (hq : 11/8 ≤ q) (hq' : q ≤ 5/2) :
    1/2 ≤ 1+w*(2-q) ∧ 3/8 ≤ 1-w^2*(2-q) := by
  have hws : w^2 ≤ 1 := by nlinarith [sq_nonneg (w-1)]
  have ht := mul_nonneg hw (by linarith : 0 ≤ (5/2:ℝ)-q)
  have hs := mul_nonneg (sq_nonneg w) (by linarith : 0 ≤ q-(11/8:ℝ))
  constructor <;> nlinarith

theorem shape_keeps_value (A : ℝ) : 3/(1-A*0^2)=3 := by norm_num

theorem mass_positive (n eps : ℝ) (hn : 0<n) (he : 0 ≤ eps) :
    0 < 6*n/(eps+6) := by positivity

theorem coefficient_cancels (M C b x : ℝ) (hC : C ≠ 0) (hb : b ≠ 0)
    (hM : M ≠ 0) (hx : x ≠ 0) :
    (-3*M^2/(16*C*(b*x)^2))*(2*C*b^2/3)/M^2 = -1/(8*x^2) := by
  field_simp
  ring

theorem second_stationary (n t : ℝ) (hn : n ≠ 0)
    (ht : 4*n*(1-t^2)=t) :
    2-t^2/(8*n)+t*(1-t^2)/2=2 := by
  field_simp
  have ht2 := congrArg (fun z : ℝ => t*z) ht
  nlinarith [ht2]

#print axioms shape_bounds
#print axioms both_speeds_positive
#print axioms shape_keeps_value
#print axioms mass_positive
#print axioms coefficient_cancels
#print axioms second_stationary
end Shaped32Pi
