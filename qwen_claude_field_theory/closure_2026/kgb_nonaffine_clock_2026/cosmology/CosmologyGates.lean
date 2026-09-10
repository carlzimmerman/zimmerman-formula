import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/- Conditional algebra only: no field-theory, perturbation, DOF or CMB claim. -/
namespace NonaffineCosmology

theorem quadratic_field_jacobian (X j : ℝ) :
    (1 + X / 10 + j * (X - 1 / 2)^2) -
      X * (1 / 10 + 2 * j * (X - 1 / 2)) =
        1 + j * (1 / 4 - X^2) := by ring

theorem connected_positive_jacobian_bound (X j : ℝ)
    (h : 0 < 1 + j * (1 / 4 - X^2)) :
    j * (X^2 - 1 / 4) < 1 := by nlinarith

theorem negative_curvature_positive_F_bound (X J : ℝ)
    (h : 0 < 21 / 40 + (X - 1 / 2) / 20 - J * (X - 1 / 2)^2 / 2) :
    J * (X - 1 / 2)^2 < 21 / 20 + (X - 1 / 2) / 10 := by nlinarith

theorem dust_homogeneous_kinetic_negative (rho C C1 C2 X D : ℝ)
    (hr : 0 < rho) (hd : 0 < D) (hn : C1 * D + 2 * X * C * C2 < 0) :
    rho * (C1 * D + 2 * X * C * C2) / (2 * D^3) < 0 := by
  apply div_neg_of_neg_of_pos
  · exact mul_neg_of_pos_of_neg hr hn
  · positivity

theorem radiation_trace_zero (rho : ℝ) : -rho + 3 * (rho / 3) = 0 := by ring

end NonaffineCosmology
