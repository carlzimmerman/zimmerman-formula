import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Algebraic Euler--Lagrange certificate for the C4 slip-lock toy action. -/

namespace SlipLockMultiplier

def ePhi (k2 Phi Psi lambda M J : ℝ) : ℝ :=
  2 * k2 * Psi - 2 * k2 * Phi + M + k2 * lambda - J

def ePsi (k2 Phi Psi lambda Sigma : ℝ) : ℝ :=
  2 * k2 * Phi - 2 * k2 * Psi + Sigma - k2 * lambda

def eLambda (k2 Phi Psi : ℝ) : ℝ := k2 * (Phi - Psi)

theorem direct_multiplier_variations
    (k2 Phi Psi _lambda _M _Sigma _J : ℝ) :
    eLambda k2 Phi Psi = k2 * (Phi - Psi) := by
  rfl

theorem no_slip_from_multiplier
    (k2 Phi Psi : ℝ) (hk2 : k2 ≠ 0)
    (hconstraint : eLambda k2 Phi Psi = 0) :
    Phi = Psi := by
  have hfactor : k2 * (Phi - Psi) = 0 := by
    simpa [eLambda] using hconstraint
  have hsub : Phi - Psi = 0 := (mul_eq_zero.mp hfactor).resolve_left hk2
  exact sub_eq_zero.mp hsub

theorem summed_metric_equation
    (k2 Phi Psi lambda M Sigma J : ℝ) :
    ePhi k2 Phi Psi lambda M J + ePsi k2 Phi Psi lambda Sigma =
      M + Sigma - J := by
  simp [ePhi, ePsi]
  ring

theorem exact_mond_and_metric_equations_force_zero_stress
    (k2 Phi Psi lambda M Sigma J : ℝ)
    (hPhi : ePhi k2 Phi Psi lambda M J = 0)
    (hPsi : ePsi k2 Phi Psi lambda Sigma = 0)
    (hMond : M = J) :
    Sigma = 0 := by
  have hsum := summed_metric_equation k2 Phi Psi lambda M Sigma J
  rw [hPhi, hPsi, hMond] at hsum
  linarith

end SlipLockMultiplier
