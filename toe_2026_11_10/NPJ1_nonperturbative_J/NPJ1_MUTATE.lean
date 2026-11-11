/-
NPJ1 MUTATE twin: false statements that must FAIL to compile (each one an error). Adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

-- false: the wrong inverse map, x = p/(1+p), does not give back p (p = 1/2: x = 1/3, x/(1+x) = 1/4)
theorem npj1_false_moebius : ((1/2:ℝ) / (1 + 1/2)) / (1 + (1/2) / (1 + 1/2)) = 1/2 := by norm_num

-- false: C-loc without the (1 + x) factor (cg = 1, x = 1, a0 = 1, GM = 1: left side 2, right side 1)
theorem npj1_false_cloc : ((1:ℝ) * 1 * 1) ^ 2 * (1 * (1 + 1) / (1 ^ 2 * 1)) = 1 ^ 2 * (1 * 1) := by norm_num

-- false: wrong sign of the A^2 term at the GN minimum (M = 1, q = 1, pi replaced by 1 to stay numeric)
theorem npj1_false_gn : -((1:ℝ) / 1) * (1 ^ 2 - 1) + (2 / (3 * 1)) * 1 ^ 3 = -(1 ^ 3) / (3 * 1) - (1 / 1) * 1 := by
  norm_num

-- false: BK's a0' with 4 pi in place of 8 pi (all symbols 1, pi replaced by 1)
theorem npj1_false_bk : ((1:ℝ) * 1 / 1) ^ 2 * (1 * 1 / (8 * 1 * 1 * 1 ^ 2)) / (1 / (1 ^ 2 * 1 ^ 2))
    = 1 ^ 3 * 1 ^ 2 / (4 * 1 * 1) := by norm_num
