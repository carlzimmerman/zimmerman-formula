import Mathlib
import Mathlib.Tactic

noncomputable section
open Real

#check pow_ne_zero
#check mul_self_ne_zero
#check mul_self_pos
#check sq_pos_of_pos
#check pow_two
#check pow_pos
#check div_mul_div_comm
#check mul_div_assoc
#check div_mul_eq_mul_div
#check nlinarith

example (a : ℝ) (ha : a ≠ 0) : a * a ≠ 0 := by
  exact mul_self_ne_zero ha

example (a : ℝ) (ha : 0 < a) : a ^ 2 ≠ 0 := by
  exact ne_of_gt (sq_pos_of_pos ha)

example (a b c d : ℝ) : (a / b) * (c / d) = a * c / (b * d) := by
  exact div_mul_div_comm

end