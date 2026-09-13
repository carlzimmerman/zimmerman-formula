import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Algebraic certificate for the scoped no-slip/Ward phantom trilemma. -/

namespace PhantomNoSlipWard

theorem trace_forces_pressure_zero {G p : ℝ} (hG : 0 < G)
    (htrace : 8 * Real.pi * G * (3 * p) = 0) : p = 0 := by
  have hprod : (24 * Real.pi * G) * p = 0 := by
    calc
      (24 * Real.pi * G) * p = 8 * Real.pi * G * (3 * p) := by ring
      _ = 0 := htrace
  have hcoeff : (24 * Real.pi * G : ℝ) ≠ 0 := by positivity
  exact (mul_eq_zero.mp hprod).resolve_left hcoeff

theorem ward_forces_density_zero {rho grad : ℝ} (hgrad : grad ≠ 0)
    (hward : (rho + 0) * grad = 0) : rho = 0 := by
  have hprod : rho * grad = 0 := by simpa using hward
  exact (mul_eq_zero.mp hprod).resolve_right hgrad

theorem exponential_phantom_witness_nonzero {G : ℝ} (hG : 0 < G) :
    -Real.exp (-2 : ℝ) / (4 * Real.pi * G) ≠ 0 := by
  apply div_ne_zero
  · exact neg_ne_zero.mpr (ne_of_gt (Real.exp_pos (-2 : ℝ)))
  · positivity

theorem trilemma_contradiction {G p rho grad : ℝ} (hG : 0 < G)
    (hgrad : grad ≠ 0) (htrace : 8 * Real.pi * G * (3 * p) = 0)
    (hward : (rho + p) * grad = 0) (hrho : rho ≠ 0) : False := by
  have hp : p = 0 := trace_forces_pressure_zero hG htrace
  have hrho_zero : rho = 0 := by
    apply ward_forces_density_zero hgrad
    simpa [hp] using hward
  exact hrho hrho_zero

end PhantomNoSlipWard
