import Mathlib
import Mathlib.Tactic

noncomputable section
open Real

#check Real.one_rpow
#check Real.rpow_def
#check Real.exp_zero
#check Real.log_one
#check sub_self
#check sub_pos
#check sq_ne_zero
#check ne_of_gt
#check ne_of_gt
#check mul_ne_zero
#check div_self
#check ring_nf

example (x : ℝ) : x = x * 1 := by ring
example (a b : ℝ) : a - b = a + -b := by ring
example (x : ℝ) (h : x ≠ 0) : x / x = 1 := by exact div_self h

-- rpow_def construction route for 1^a = 1:
example (a : ℝ) : (1 : ℝ) ^ a = 1 := by
  rw [Real.rpow_def]
  rw [Real.log_one]
  rw [mul_zero]
  rw [Real.exp_zero]

end