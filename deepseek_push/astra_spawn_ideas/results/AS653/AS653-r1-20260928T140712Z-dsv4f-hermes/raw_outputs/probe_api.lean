import Mathlib
import Mathlib.Tactic

noncomputable section
open Real

#check Real.rpow_add
#check Real.rpow_sub
#check Real.rpow_zero
#check Real.rpow_one
#check Real.rpow_ne_zero
#check Real.rpow_pos_of_pos
#check Real.rpow_mul
#check Real.hasDerivAt_rpow_const
#check Real.log_rpow
#check Real.log_one
#check Real.log_ne_zero_of_pos_ne_one
#check Real.log_eq_zero
#check hasDerivAt_const
#check HasDerivAt.const_mul
#check HasDerivAt.mul_const
#check HasDerivAt.rpow_const
#check mul_left_cancel₀
#check mul_right_cancel₀
#check mul_ne_zero
#check mul_eq_zero.mp
#check div_eq_mul_inv
#check div_eq_iff
#check inv_eq_one_div
#check div_div_eq_mul_div
#check one_div

end