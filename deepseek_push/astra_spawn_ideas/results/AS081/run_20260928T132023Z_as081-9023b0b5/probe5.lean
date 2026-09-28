import Mathlib
import Mathlib.Tactic
noncomputable section
open Real
open scoped Topology Filter

#check inv_pow
#check one_lt_div

example (x : ℝ) : x⁻¹ ^ 2 = (x ^ 2)⁻¹ := by
  exact inv_pow x 2

example (G M_b x : ℝ) : G * M_b / x ^ 2 = G * M_b * (x⁻¹ ^ 2) := by
  rw [inv_pow x 2]