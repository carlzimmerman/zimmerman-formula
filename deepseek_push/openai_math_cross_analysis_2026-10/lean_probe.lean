import Mathlib

-- Smoke probe: toolchain sanity only. No physics content.
example : (1:ℝ)/2 = 2⁻¹ := by norm_num

example (a : ℝ) : 0 ≤ a * a := mul_self_nonneg a

theorem smoke_probe : (4:ℝ) = 2^2 := by norm_num