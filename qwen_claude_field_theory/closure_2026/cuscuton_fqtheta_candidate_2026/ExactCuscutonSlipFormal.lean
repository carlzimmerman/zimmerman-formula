import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-! Formal no-slip obstruction for the explicit cuscuton-F(Q)Theta candidate. -/

namespace ExactCuscutonSlip

theorem exponential_mu_pos (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hneg : -y < 0 := by linarith
  have hexp : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr hneg
  linarith

theorem cuscuton_no_slip_impossible
    (M2 Q0 sigma y : ℝ)
    (hM2 : 0 < M2) (hQ0 : 0 < Q0) (hy : 0 < y)
    (hzero : M2 * (1 - Real.exp 0) - sigma / (2 * Q0) = 0)
    (hfinite : M2 * (1 - Real.exp (-y)) -
      sigma / (2 * Real.sqrt (Q0 ^ 2 - y ^ 2)) = 0) : False := by
  have hdiv : -sigma / (2 * Q0) = 0 := by
    simpa using hzero
  have hden : 2 * Q0 ≠ 0 := by positivity
  have hsigma : sigma = 0 := by
    field_simp [hden] at hdiv
    linarith
  have hmu : 0 < 1 - Real.exp (-y) := exponential_mu_pos y hy
  rw [hsigma] at hfinite
  have hres : 0 < M2 * (1 - Real.exp (-y)) := mul_pos hM2 hmu
  have : M2 * (1 - Real.exp (-y)) = 0 := by
    simpa using hfinite
  linarith

end ExactCuscutonSlip
