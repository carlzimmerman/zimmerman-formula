import Mathlib.Data.Real.Basic
import Mathlib.Tactic

noncomputable section
open scoped Real

/-- First doc comment: the leftover N * M does NOT vanish (witness below). -/

/-- Second doc comment: concrete witness = -57/50 != 0. -/
theorem probe_witness :
    10 * (-(7 / 20) * (21 / 50) - (3 / 20) * (-(11 / 50))) ≠ 0 := by
  norm_num

/-- Third: a plain ring theorem. -/
theorem probe_ring (a b : ℝ) (hb : b = a) : a - b = 0 := by
  rw [hb]
  ring

end