import Mathlib
import Mathlib.Tactic

noncomputable section
open Real
open scoped Topology Filter

#check HasDerivAt.inv
#check hasDerivAt_inv₀
#check hasDerivAt_inv
#check HasDerivAt.neg
#check HasDerivAt.const_mul
#check HasDerivAt.const_add
#check MeasureTheory.ContinuousOn.integrableOn
#check intervalIntegral.intervalIntegrable_of_continuousOn
#check intervalIntegral.intervalIntegrable_iff_integrableOn_Icc_of_le
#check intervalIntegral.IntegrableOn.intervalIntegrable
#check Filter.Tendsto.mono_right
#check Filter.Tendsto.mono_left
#check Filter.Tendsto.sub
#check tendsto_const_nhds
#check Real.pi_pos
#check Real.tendsto_arctan_atTop
#check nhdsWithin_le_nhds
#check Ioi_mem_nhds
#check tendsto_inv_atTop_zero
#check Tendsto.const_mul
#check tendsto_nhds_of_eventually_eq
#check Set.EqOn