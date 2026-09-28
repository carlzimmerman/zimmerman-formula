import Mathlib
import Mathlib.Tactic
noncomputable section
open Real Filter
open scoped Topology
#check ContinuousOn.div
#check ContinuousOn.div₀
#check ContinuousOn.neg
#check ContinuousOn.inv₀
#print Filter.EventuallyEq
#check EventuallyEq.symm
#check Set.uIcc
#check min_eq_left
#check max_eq_right