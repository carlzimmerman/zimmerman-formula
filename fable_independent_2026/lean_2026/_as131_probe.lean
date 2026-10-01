import Mathlib
open scoped intervalIntegral Real
open Set intervalIntegral
noncomputable section

#check ContinuousLinearMap.hasDerivAt
#check ContinuousLinearMap.hasFDerivAt
#check ContinuousLinearMap.differentiableAt
#check Complex.ofRealCLM
#check HasDerivAt.exp
#check HasDerivAt.deriv
#check DifferentiableAt.hasDerivAt
#check DifferentiableAt.add
#check DifferentiableAt.exp
#check intervalIntegral.integral_deriv_eq_sub'
#check intervalIntegral.integral_add
#check intervalIntegral.integral_const_mul
#check intervalIntegral.integral_congr
#check Complex.exp_int_mul
#check Complex.exp_two_pi_mul_I
#check Complex.exp_add
#check Complex.exp_zero
#check Complex.exp.continuous
#check Continuous.cexp
#check Continuous.mul
#check Continuous.add
#check Continuous.continuousOn
#check DifferentiableAt.continuousAt
#check ContinuousLinearMap.continuous
#check Real.cos_periodic
#check Function.Periodic
#check deriv_eq
#check intervalIntegral.intervalIntegrable_iff
#check Continuous.intervalIntegrable
