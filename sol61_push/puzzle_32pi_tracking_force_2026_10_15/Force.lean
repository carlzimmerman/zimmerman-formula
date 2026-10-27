import Mathlib
noncomputable section
namespace TrackingForce

theorem strength_bound (F t : ℝ) (hf : 0 < F) (ht : 0 ≤ t) :
    2*t/(F+6*t) < (1:ℝ)/3 := by
  have hd : 0 < F+6*t := by linarith
  apply (div_lt_iff₀ hd).2
  linarith

theorem enhancement_bound (B y : ℝ) (hb : 0 ≤ B) (hb' : B < (1:ℝ)/3)
    (hy : 0 ≤ y) (hy' : y ≤ 1) :
    1 ≤ 1+B*y ∧ 1+B*y < (4:ℝ)/3 := by
  have h1 : 0 ≤ B*y := mul_nonneg hb hy
  have h2 : B*y ≤ B := by nlinarith [mul_nonneg hb (sub_nonneg.mpr hy')]
  constructor <;> linarith

theorem slope_bound (B x e : ℝ) (hb : 0 ≤ B) (hx : 0 ≤ x) (he : 0 ≤ e) :
    -2-B*x^2*e/(1+B*(1+x)*e) ≤ (-2:ℝ) := by
  have h : 0 ≤ B*x^2*e/(1+B*(1+x)*e) := by positivity
  linarith

#print axioms strength_bound
#print axioms enhancement_bound
#print axioms slope_bound
end TrackingForce
