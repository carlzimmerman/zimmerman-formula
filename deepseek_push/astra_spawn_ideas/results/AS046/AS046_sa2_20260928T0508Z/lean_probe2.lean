import Mathlib
import Mathlib.Tactic
noncomputable section
open Real

-- probe 1: mu2 derivative via fun_prop
example (x : ℝ) (hx : 1 + x / 2 ≠ 0) :
    HasDerivAt (fun z : ℝ => 1 - 1 / (1 + z / 2) ^ 2) (1 / (1 + x / 2) ^ 3) x := by
  fun_prop
  field_simp [hx]
  ring

-- probe 2: mu_s derivative via fun_prop
example (x : ℝ) :
    HasDerivAt (fun z : ℝ => z / Real.sqrt (1 + z ^ 2))
      (1 / ((1 + x ^ 2) * Real.sqrt (1 + x ^ 2))) x := by
  fun_prop

-- probe 3: muQ derivative at 1 via fun_prop
example :
    HasDerivAt (fun z : ℝ => ((Real.sqrt (1 + 4 * z ^ 2) - 1) / 2) / z)
      ((Real.sqrt 5 - 1) / (2 * Real.sqrt 5)) 1 := by
  fun_prop
  norm_num [Real.sq_sqrt]

-- probe 4: kappa_Q bounds 1 < kappa < 2
example (y : ℝ) (hy : 0 < y) : 1 < 2 * (y + 1) / (2 * y + 1) := by
  have h2y : 2 * y + 1 ≠ 0 := by nlinarith
  field_simp [h2y]
  nlinarith

example (y : ℝ) (hy : 0 < y) : 2 * (y + 1) / (2 * y + 1) < 2 := by
  have h2y : 2 * y + 1 ≠ 0 := by nlinarith
  field_simp [h2y]
  nlinarith

-- probe 5: relative-conditioning total-differential identity
example (x y d : ℝ) (hy : y ≠ 0) (hd : d ≠ 0) :
    (x / (y * d)) * (d * y / x) = 1 := by
  field_simp [hy, hd]
  ring
end