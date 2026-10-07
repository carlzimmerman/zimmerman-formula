import Mathlib

/-! # Cert: the epoch-elasticity of completeness (T12) — closed form

Certifies the ALGEBRA of the sensitivity function: with the settling law

    f = 1 - e^{-x},   x := Gamma t        (CFG382's law; T10 heat-mode)

the completeness-to-epoch elasticity

    eps(f) = d ln f / d ln t = x e^{-x}/(1 - e^{-x})

is an exact function of f ALONE (Gamma and t cancel):

    eps(f) = (1 - f) * (-ln(1 - f)) / f

This file certifies that identity given the law; the derivative step
itself rides in the lane script (house pattern: calculus carries in the
lane, the algebraic closed form is certified).

Values at the record's clocks (lane): MW floor 0.14 -> 0.9265; groups
0.60 -> 0.6109; clusters 0.43 -> 0.7451; the single-lambda consistency
window [0.0215, 0.0432] contains CFG382's lambda = 0.028.

Zero sorry; axioms = {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

variable {x f : ℝ}

/-- Given the settling law 1 - f = e^{-x} (x := Gamma t), the elasticity
equals the closed form in f alone:  x e^{-x}/(1 - e^{-x}) =
(1 - f)*(-ln(1 - f))/f. -/
theorem epoch_elasticity_closed (hf : f ≠ 0)
    (hlaw : 1 - f = Real.exp (-x)) :
    x * Real.exp (-x) / (1 - Real.exp (-x)) = (1 - f) * (-Real.log (1 - f)) / f := by
  have hlog : Real.log (1 - f) = -x := by
    rw [hlaw, Real.log_exp]
  have hden : 1 - Real.exp (-x) = f := by linarith
  rw [hden, ← hlaw, hlog]
  norm_num
  field_simp [hf]

end