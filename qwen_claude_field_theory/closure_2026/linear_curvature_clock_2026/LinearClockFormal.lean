import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Conditional real inequalities; neither the action variation nor global
    curved-background existence is formalized in this file. -/
namespace LinearCurvatureClock

theorem exponential_longitudinal_upper (y : ℝ) :
    1+(y-1)*Real.exp (-y) ≤ 1+Real.exp (-2) := by
  have h : y-1 ≤ Real.exp (y-2) := by
    have h' := Real.add_one_le_exp (y-2)
    linarith
  have hm := mul_le_mul_of_nonneg_right h (le_of_lt (Real.exp_pos (-y)))
  have he : Real.exp (y-2)*Real.exp (-y) = Real.exp (-2) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [he] at hm
  linarith

theorem exp_neg_two_lt_half : Real.exp (-2) < (1:ℝ)/2 := by
  have h : (3:ℝ) ≤ Real.exp 2 := by
    have h' := Real.add_one_le_exp (2:ℝ)
    linarith
  have hm := mul_le_mul_of_nonneg_right h (le_of_lt (Real.exp_pos (-2)))
  have he : Real.exp (2:ℝ)*Real.exp (-2) = 1 := by
    rw [← Real.exp_add]
    norm_num
  rw [he] at hm
  linarith

theorem local_scalar_cone_inside_light_cone
    (y theta : ℝ) (hy : 0 < y) (h0 : 0 ≤ theta) (h1 : theta ≤ 1) :
    0 < 2*(1-Real.exp (-y)+y*Real.exp (-y)*theta)/3 ∧
    2*(1-Real.exp (-y)+y*Real.exp (-y)*theta)/3 < 1 := by
  have he : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  have hp : 0 < y*Real.exp (-y) := mul_pos hy (Real.exp_pos _)
  have hn := mul_nonneg (le_of_lt hp) h0
  have hu := mul_le_mul_of_nonneg_left h1 (le_of_lt hp)
  have hl := exponential_longitudinal_upper y
  have hh := exp_neg_two_lt_half
  constructor <;> nlinarith

theorem beam_exterior_tail_positive (delta m R : ℝ)
    (hd : 0 < delta) (hm : 0 < m) (hR : 0 < R) :
    0 < 3*delta/(4*Real.pi*m*R^5) := by
  exact div_pos (mul_pos (by norm_num) hd)
    (mul_pos (mul_pos (mul_pos (by norm_num) Real.pi_pos) hm) (pow_pos hR _))

#print axioms exponential_longitudinal_upper
#print axioms local_scalar_cone_inside_light_cone
#print axioms beam_exterior_tail_positive
end LinearCurvatureClock
