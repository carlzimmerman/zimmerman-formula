import Mathlib

/-! MUTATE for KOIDE_PHASE: both claims are FALSE and must fail.
(1) the Z3 cubic sum with the wrong coefficient 3/2 instead of 3/4.
(2) the measured ratio placed ABOVE the Koide+Brannen prediction (206.7683 > 206.771 is false). -/
open Real

theorem mutate_cubic (d : ℝ) :
    cos d ^ 3 + cos (d + 2 * π / 3) ^ 3 + cos (d - 2 * π / 3) ^ 3 = (3 / 2) * cos (3 * d) := by
  have h3 : √3 ^ 2 = 3 := sq_sqrt (by norm_num)
  have hs : sin d ^ 2 = 1 - cos d ^ 2 := by rw [← sin_sq_add_cos_sq d]; ring
  have e : 2 * π / 3 = π - π / 3 := by ring
  rw [cos_add, cos_sub, e, cos_pi_sub, sin_pi_sub, cos_pi_div_three, sin_pi_div_three, cos_three_mul]
  linear_combination (-3 / 4 * cos d * sin d ^ 2) * h3 + (-9 / 4 * cos d) * hs

theorem mutate_measured : (105.6583755 + 0.0000023 : ℝ) / 0.51099895 > 206.771 := by norm_num
