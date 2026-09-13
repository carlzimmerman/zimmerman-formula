import Mathlib

theorem tiny_test (a : ℝ) (ha : 0 < a) : 0 < Real.sqrt a := Real.sqrt_pos.mpr ha

#check Real.pi
