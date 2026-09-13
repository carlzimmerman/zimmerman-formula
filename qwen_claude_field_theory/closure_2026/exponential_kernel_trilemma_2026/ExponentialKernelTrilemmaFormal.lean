import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace ExponentialKernelTrilemma

/-! Algebraic pieces of the local single-metric trilemma.  Transcendental
series and functional analysis are deliberately left to the executable
SymPy certificate; these lemmas certify the exact constitutive zero and the
rotational and regulator implications. -/

theorem exponential_mu_zero : (1 - Real.exp 0) = 0 := by simp

theorem regulator_exact_zero {c : ℝ} (h : c + (1 - Real.exp 0) = 0) : c = 0 := by
  simpa using h

theorem nonzero_regulator_breaks_exact_zero {c : ℝ} (hc : c ≠ 0) :
    c + (1 - Real.exp 0) ≠ 0 := by
  simpa using hc

theorem isotropic_90deg_zero {x y : ℝ}
    (hx : -y = x) (hy : x = y) : x = 0 ∧ y = 0 := by
  constructor <;> linarith

theorem local_regulator_no_slip_forces_zero {F R P d : ℝ}
    (hR : R ≠ 0) (hP : P ≠ 0)
    (hslip : P * d + F * (-R / P) = 0)
    (hd : d = 0) : F = 0 := by
  have hprod : F * (-R / P) = 0 := by simpa [hd] using hslip
  have hquot : (-R / P) ≠ 0 := by
    exact div_ne_zero (neg_ne_zero.mpr hR) hP
  exact (mul_eq_zero.mp hprod).resolve_right hquot

end ExponentialKernelTrilemma
