import Mathlib
import Mathlib.Tactic

noncomputable section
open Real

#check tendsto_log_mul_self_nhdsLT_zero
#check tendsto_log_mul_rpow_nhdsGT_zero
#check tendsto_log_mul_self_nhdsGT_zero
#check Real.tendsto_log_mul_self_nhdsGT_zero
#check Real.log_inv
#check Real.log_div
#check Real.log_lt_sub_one_of_pos
#check Real.one_sub_inv_le_log_of_pos
#check one_lt_div
#check div_lt_one
#check Bound.div_lt_one_of_pos_of_lt
#check intervalIntegral.integral_deriv_eq_sub'
#check intervalIntegral.integral_congr
#check Set.mem_uIcc
#check min_eq_left
#check Real.deriv_log'
#check deriv_const_mul
#check deriv_mul_const
#check inv_div
#check div_eq_mul_inv
#check Real.log_mul
#check Real.continuousAt_log
#check DifferentiableAt.mul
#check fun_prop
#check tendsto_nhdsWithin_of_tendsto_nhds
end
