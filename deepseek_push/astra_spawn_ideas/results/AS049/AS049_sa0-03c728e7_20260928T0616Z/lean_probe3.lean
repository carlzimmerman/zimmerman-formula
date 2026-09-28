import Mathlib
import Mathlib.Tactic

noncomputable section
open Real
open scoped Topology Filter

#check ContinuousOn.intervalIntegrable
#check intervalIntegral.intervalIntegrable_iff
#check MeasureTheory.IntegrableOn
#check MeasureTheory.ContinuousOn.integrableOn
#check ContinuousOn.integrableOn
#check integral_deriv_eq_sub
#check intervalIntegral.integral_deriv_eq_sub
#check tendsto_nhdsWithin_of_tendsto_nhds
#check eventually_of_forall
#check Filter.Tendsto.of_tendsto_comp
#check Real.continuous_arctan
#check arctan_center
#check Real.arctan_zero
#check Real.neg_div
#check div_neg
#check Filter.Tendsto.atTop_nhdsWithin_Ioi
#check Filter.Tendsto.atTop_mul_const