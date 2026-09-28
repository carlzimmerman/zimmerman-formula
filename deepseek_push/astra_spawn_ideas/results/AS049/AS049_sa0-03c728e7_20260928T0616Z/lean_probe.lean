import Mathlib
import Mathlib.Tactic

noncomputable section
open Real
open scoped Topology Filter

-- API probe for the AS049 certificate (compiled from the run dir)
#check Real.hasDerivAt_sqrt
#check Real.deriv_sqrt
#check Real.differentiableAt_sqrt
#check intervalIntegral.integral_eq_sub_of_hasDerivAt
#check intervalIntegral.integral_eq_sub_of_hasDerivAt'
#check intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le
#check Real.tendsto_arctan_atTop
#check tendsto_inv_atTop_zero
#check nhdsWithin_le_nhds
#check HasDerivAt.inv₀
#check sq_eq_sq_iff_abs_eq_abs
#check mul_self_eq_mul_self_iff
#check deriv_comp
#check (hasDerivAt_id (0 : ℝ)).mul_const
#check HasDerivAt.div_const
#check Real.hasDerivAt_arctan
#check intervalIntegral.integral_congr
#check intervalIntegral.integral_of_le
#check Filter.Tendsto.const_mul
#check Filter.Tendsto.const_sub