import Mathlib

noncomputable section
open Filter
open scoped Topology

-- instance-path rfl checks for the final convert
example : Real.instAddCommGroup = Real.normedAddCommGroup.toAddCommGroup := by rfl

example : Semiring.toModule = RCLike.toInnerProductSpaceReal.toModule := by rfl

#check Filter.Eventually.of_forall
