import Mathlib
noncomputable section
open Real

example {x : ℝ} (hx : 0 < x) : 1 < 1 + 4 * x ^ 2 := by
  nlinarith [pow_pos hx 2]

example {x : ℝ} (hx : 0 < x) : (1:ℝ) < Real.sqrt (1 + 4 * x ^ 2) := by
  rw [← Real.sqrt_one]
  exact Real.sqrt_lt_sqrt (by norm_num) (by nlinarith [pow_pos hx 2])

end
