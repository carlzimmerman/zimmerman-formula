/-
QG1 MUTATE twin: false statements that must FAIL to compile (each one an error). Adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

-- false: with beta = 1/10 the shift coefficient is not zero
theorem qg1_false_shift : (1 - (1/10:ℝ)) - (1 + 0) = 0 := by norm_num

-- false: a nonzero charge does not give omega^2 = 0 (G = 1, k = 1, a = 1, b = 2)
theorem qg1_false_omega2 : (1:ℝ) * 1 ^ 2 * (2 - 1) / (1 * 2) = 0 := by norm_num

-- false: wrong sign in the Delta mu identity at u = 1, eps = 1
theorem qg1_false_dmu : 1 / (1 + (1:ℝ)) - 1 / ((1 + 1) * (1 + 1)) = -(1 / ((1 + 1) * (1 + 1))) := by norm_num

-- false: alpha_a = 2 point misplaced (1 - K m0 at u = 1 is not 0)
theorem qg1_false_alpha2 : 1 - 1 / (1 + (1:ℝ)) ^ 2 = 0 := by norm_num
