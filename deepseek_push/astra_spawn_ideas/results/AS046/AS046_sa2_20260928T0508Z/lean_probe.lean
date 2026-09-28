import Mathlib
import Mathlib.Tactic
noncomputable section
open Real

#check HasDerivAt.rpow
#check Real.hasDerivAt_rpow_const
#check Real.rpow_neg
#check Real.rpow_add
#check Real.sqrt_eq_rpow
#check Real.sq_sqrt
#check zpow_neg
#check zpow_natCast
#check HasDerivAt.inv
#check HasDerivAt.div
#check HasDerivAt.pow
#check HasDerivAt.sub_const
#check HasDerivAt.const_sub
#check HasDerivAt.const_mul
#check hasDerivAt_id
#check Real.hasDerivAt_sqrt
#check Real.differentiableAt_sqrt
#check Real.sqrt_ne_zero_of_pos
#check Real.sqrt_pos.2
#check one_div
#check inv_eq_one_div
#check div_eq_div_iff
end