import Mathlib

/-! Exact normalization-window and preferred-frame algebra.
The exponential bound is proved for all real x; action variation, PPN
identification, nonlinear constraints and physical causality remain analytic
dependencies in the accompanying report. -/
namespace PushNewton20260926

theorem exponential_longitudinal_upper (x : ℝ) :
    1 + (x-1)*Real.exp (-x) ≤ 1 + Real.exp (-2) := by
  have h : x-1 ≤ Real.exp (x-2) := by
    convert Real.add_one_le_exp (x-2) using 1 <;> ring
  have hm := mul_le_mul_of_nonneg_right h (le_of_lt (Real.exp_pos (-x)))
  have he : Real.exp (x-2)*Real.exp (-x) = Real.exp (-2) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [he] at hm
  linarith

theorem exponential_longitudinal_positive (x : ℝ) (hx : 0 < x) :
    0 < 1 + (x-1)*Real.exp (-x) := by
  have he : Real.exp (-x) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  have hp := mul_pos hx (Real.exp_pos (-x))
  nlinarith

theorem longitudinal_maximum_attained :
    1 + ((2:ℝ)-1)*Real.exp (-(2:ℝ)) = 1+Real.exp (-2) := by norm_num

theorem renormalized_tangent_interval (C mu bound : ℝ)
    (hc : 0 < C) (hm : 0 < mu) (hb : mu ≤ bound) (hcb : C*bound < 1) :
    0 < 2*(1-C*mu) ∧ 2*(1-C*mu) < 2 := by
  have hmul := mul_le_mul_of_nonneg_left hb hc.le
  have hp := mul_pos hc hm
  constructor <;> nlinarith

theorem exponential_renormalized_interval (C x : ℝ)
    (hc : 0 < C) (hx : 0 < x)
    (hbound : C*(1+Real.exp (-2)) < 1) :
    0 < 2*(1-C*(1+(x-1)*Real.exp (-x))) ∧
      2*(1-C*(1+(x-1)*Real.exp (-x))) < 2 := by
  exact renormalized_tangent_interval C _ _ hc
    (exponential_longitudinal_positive x hx)
    (exponential_longitudinal_upper x) hbound

theorem scalar_speed_positive (E kappa : ℝ)
    (he0 : 0 < E) (he2 : E < 2) (hk : 0 < kappa) :
    0 < 2*(2-E)/(kappa*E) := by
  apply div_pos
  · nlinarith
  · positivity

theorem measured_Newton_relation (Gbare C : ℝ) (hc : C ≠ 0) :
    Gbare/(1-(2*(1-C))/2) = Gbare/C := by
  congr 1
  ring

theorem preferred_frame_cost (C d : ℝ) (hc : 0 < C) (hd : 0 < d)
    (hwindow : C*(1+d) < 1) :
    8*d/(1+d) < |-8*(1-C)| := by
  have hcd : 0 < C*d := mul_pos hc hd
  have hc1 : C < 1 := by nlinarith
  have hnegative : -8*(1-C) < 0 := by linarith
  rw [abs_of_neg hnegative]
  apply (div_lt_iff₀ (by linarith : 0 < 1+d)).mpr
  nlinarith

#print axioms exponential_longitudinal_upper
#print axioms exponential_longitudinal_positive
#print axioms longitudinal_maximum_attained
#print axioms renormalized_tangent_interval
#print axioms exponential_renormalized_interval
#print axioms scalar_speed_positive
#print axioms measured_Newton_relation
#print axioms preferred_frame_cost
end PushNewton20260926

