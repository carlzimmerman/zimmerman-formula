import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith

/-! Lean certificate for the constructive scalar branch of the double-multiplier action. -/

namespace EllipticDoubleMultiplier

theorem nonzero_mode_slip
    (k Phi Psi chi : ℝ)
    (hk : k ≠ 0)
    (h1 : k ^ 2 * (chi - Psi) = 0)
    (h2 : k ^ 2 * (chi - Phi) = 0) :
    Phi = Psi ∧ chi = Phi := by
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  have hchiPsi : chi - Psi = 0 := (mul_eq_zero.mp h1).resolve_left hk2
  have hchiPhi : chi - Phi = 0 := (mul_eq_zero.mp h2).resolve_left hk2
  constructor <;> linarith

theorem aqual_reduction
    (f fp mu mup rho C : ℝ)
    (hphi : 2 * fp - (2 * ((1 - mu) * fp - mup * f)) = 8 * C * rho) :
    mu * fp + mup * f = 4 * C * rho := by
  linarith

theorem exponential_mu_pos (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hneg : -y < 0 := by linarith
  have hexp : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr hneg
  linarith

theorem luminal_ratio (M2 : ℝ) (hM2 : 0 < M2) : M2 / M2 = 1 := by
  exact div_self (ne_of_gt hM2)

theorem tf_residual_nonzero (M2 y : ℝ) (hM2 : 0 < M2) (hy : 0 < y) :
    -2 * M2 * (1 - Real.exp (-y)) ≠ 0 := by
  have hmu : 0 < 1 - Real.exp (-y) := exponential_mu_pos y hy
  have hprod : 0 < 2 * M2 * (1 - Real.exp (-y)) := by positivity
  nlinarith

end EllipticDoubleMultiplier
