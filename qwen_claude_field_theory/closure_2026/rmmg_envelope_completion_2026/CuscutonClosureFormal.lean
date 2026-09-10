import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
  Kernel-checked core of the closure-forces-cuscuton argument.  The
  hypotheses encode the two coefficient matches of the displayed smeared
  bracket; this file does not claim to derive the full functional bracket.
-/

namespace RMMGEnvelope

theorem bracket_closure_forces_constant_kernel
    (A Ader mu muder : ℝ) (hA : A ≠ 0)
    (_hmatch : A * mu = 1) (hzero : A * Ader = 0)
    (hderiv : Ader * mu + A * muder = 0) :
    muder = 0 := by
  have hAder : Ader = 0 := (mul_eq_zero.mp hzero).resolve_left hA
  have hprod : A * muder = 0 := by
    simpa [hAder] using hderiv
  exact (mul_eq_zero.mp hprod).resolve_left hA

theorem exponential_kernel_derivative_positive
    (s a0 : ℝ) (ha : 0 < a0) :
    0 < Real.exp (-s / a0) / a0 := by
  positivity

theorem no_canonical_exponential_closure
    (A Ader mu muder s a0 : ℝ) (hA : A ≠ 0)
    (hmatch : A * mu = 1) (hzero : A * Ader = 0)
    (hderiv : Ader * mu + A * muder = 0)
    (hmuder : muder = Real.exp (-s / a0) / a0)
    (ha : 0 < a0) : False := by
  have hforced : muder = 0 :=
    bracket_closure_forces_constant_kernel A Ader mu muder hA hmatch hzero hderiv
  have hpositive : 0 < muder := by
    rw [hmuder]
    exact exponential_kernel_derivative_positive s a0 ha
  linarith

end RMMGEnvelope
