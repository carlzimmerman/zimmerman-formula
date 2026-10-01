import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Tactic

noncomputable section

def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2

-- A: add of const and id
example (u : ℝ) : HasDerivAt (fun x : ℝ => 2 + x) (0 + 1) u := by
  simpa using (hasDerivAt_const u (2 : ℝ)).add (hasDerivAt_id u)

-- B: mul of hlin hlin
example (u : ℝ) : HasDerivAt (fun x : ℝ => (1 + x) * (1 + x))
    (1 * (1 + u) + (1 + u) * 1) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  simpa [Pi.mul_apply] using hlin.mul hlin

-- C: quotient rule for mu2
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt mu2
      (((1 * (2 + u) + u * (0 + 1)) * ((1 + u)^2)
        - (u * (2 + u)) * (1 * (1 + u) + (1 + u) * 1)) / (((1 + u)^2)^2)) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have h2x : HasDerivAt (fun x : ℝ => 2 + x) (0 + 1) u := by
    simpa using (hasDerivAt_const u (2 : ℝ)).add (hasDerivAt_id u)
  have hn : HasDerivAt (fun x : ℝ => x * (2 + x)) (1 * (2 + u) + u * (0 + 1)) u :=
    (hasDerivAt_id u).mul h2x
  have hd : HasDerivAt (fun x : ℝ => (1 + x) * (1 + x))
      (1 * (1 + u) + (1 + u) * 1) u := by
    simpa [Pi.mul_apply] using hlin.mul hlin
  have hq := hn.div hd (mul_ne_zero hu hu)
  simpa [mu2] using hq
