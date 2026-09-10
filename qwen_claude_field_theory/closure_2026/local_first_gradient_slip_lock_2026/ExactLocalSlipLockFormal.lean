import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith

/-! Algebraic slip-lock certificate for local first-gradient carriers. -/

namespace ExactLocalSlipLock

theorem equal_flux_locks_traceless_coefficient
    (Lu Lv Lw mu : ℝ)
    (hA : 2 * Lu + Lw = mu)
    (hB : 2 * Lv + Lw = mu) :
    Lu + Lv + Lw = mu := by
  linarith

theorem exponential_mu_pos (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hneg : -y < 0 := by linarith
  have hexp : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr hneg
  linarith

theorem exponential_locked_tf_nonzero
    (Lu Lv Lw y : ℝ)
    (hy : 0 < y)
    (hA : 2 * Lu + Lw = 1 - Real.exp (-y))
    (hB : 2 * Lv + Lw = 1 - Real.exp (-y)) :
    Lu + Lv + Lw ≠ 0 := by
  have hlock : Lu + Lv + Lw = 1 - Real.exp (-y) :=
    equal_flux_locks_traceless_coefficient Lu Lv Lw (1 - Real.exp (-y)) hA hB
  have hpos : 0 < 1 - Real.exp (-y) := exponential_mu_pos y hy
  rw [hlock]
  exact ne_of_gt hpos

end ExactLocalSlipLock
