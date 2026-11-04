import Std
/- Deliberately false: the same two-channel count does not remove normalization. -/
example : (1 : Rat) / (2 * 2) = 1 / 2 := by decide +kernel
