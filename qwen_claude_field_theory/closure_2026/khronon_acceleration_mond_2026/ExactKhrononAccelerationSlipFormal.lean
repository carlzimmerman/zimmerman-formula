import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith

/-! Lean certificate for the 3-D acceleration-khronon traceless-stress obstruction. -/

namespace ExactKhrononAccelerationSlip

theorem exponential_mu_pos (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hneg : -y < 0 := by linarith
  have hexp : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr hneg
  linarith

theorem acceleration_tf_nonzero (M2 y : ℝ)
    (hM2 : 0 < M2) (hy : 0 < y) :
    -2 * M2 * (1 - Real.exp (-y)) ≠ 0 := by
  have hmu : 0 < 1 - Real.exp (-y) := exponential_mu_pos y hy
  have hpos : 0 < 2 * M2 * (1 - Real.exp (-y)) := by positivity
  have hneg : -2 * M2 * (1 - Real.exp (-y)) < 0 := by linarith
  exact ne_of_lt hneg

end ExactKhrononAccelerationSlip
