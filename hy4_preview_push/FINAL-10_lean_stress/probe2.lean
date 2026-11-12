import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic
open Real

-- A: affine via const_add
example (x : ℝ) : HasDerivAt (fun t : ℝ => 1 + t) 1 x := by
  simpa using (hasDerivAt_id x).const_add (1 : ℝ)

-- B: affine written as t + 1
example (x : ℝ) : HasDerivAt (fun t : ℝ => t + 1) 1 x := by
  simpa using (hasDerivAt_id x).add_const (1 : ℝ)

-- C: cube via pow
example (x : ℝ) : HasDerivAt (fun t : ℝ => t ^ 3) (3 * x ^ 2) x := by
  simpa using (hasDerivAt_id x).pow 3

-- D: square via pow
example (x : ℝ) : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by
  simpa using (hasDerivAt_id x).pow 2

-- E: log of affine
example (x : ℝ) (h1p : (1 + x : ℝ) ≠ 0) :
    HasDerivAt (fun t : ℝ => Real.log (1 + t)) (1 / (1 + x)) x := by
  have hlin : HasDerivAt (fun t : ℝ => t + 1) 1 x := by
    simpa using (hasDerivAt_id x).add_const (1 : ℝ)
  simpa [one_div, add_comm] using hlin.log h1p

-- F: quotient
example (x : ℝ) (h1p : (1 + x : ℝ) ≠ 0) :
    HasDerivAt (fun t : ℝ => t ^ 2 / (1 + t))
      (((2 * x) * (1 + x) - x ^ 2 * 1) / (1 + x) ^ 2) x := by
  have hnum : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by
    simpa using (hasDerivAt_id x).pow 2
  have hden : HasDerivAt (fun t : ℝ => t + 1) 1 x := by
    simpa using (hasDerivAt_id x).add_const (1 : ℝ)
  simpa [add_comm, mul_comm, mul_left_comm, mul_assoc] using hnum.div hden h1p

-- G: full residual derivative, built from combinators, then value by ring
noncomputable def resF : ℝ → ℝ :=
  (fun u : ℝ => 2 * u) - (fun u : ℝ => 2 * Real.log (1 + u)) - (fun u : ℝ => u ^ 2 / (1 + u))

example (x : ℝ) (hx : 0 < x) : HasDerivAt resF (x ^ 2 / (1 + x) ^ 2) x := by
  have h1p : (1 + x : ℝ) ≠ 0 := by linarith
  have hlin : HasDerivAt (fun t : ℝ => t + 1) 1 x := by
    simpa using (hasDerivAt_id x).add_const (1 : ℝ)
  have h2t : HasDerivAt (fun t : ℝ => 2 * t) (2 * 1) x := (hasDerivAt_id x).const_mul (2 : ℝ)
  have hlog : HasDerivAt (fun t : ℝ => Real.log (1 + t)) (1 / (1 + x)) x := by
    simpa [one_div, add_comm] using hlin.log h1p
  have h2log : HasDerivAt (fun t : ℝ => 2 * Real.log (1 + t)) (2 * (1 / (1 + x))) x :=
    hlog.const_mul (2 : ℝ)
  have hsq : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by simpa using (hasDerivAt_id x).pow 2
  have hquot : HasDerivAt (fun t : ℝ => t ^ 2 / (1 + t))
      ((((2 * x) * (1 + x)) - x ^ 2 * 1) / (1 + x) ^ 2) x := by
    simpa [add_comm, one_mul] using hsq.div hlin h1p
  have h := (h2t.sub h2log).sub hquot
  have h' : HasDerivAt resF
      (2 * 1 - 2 * (1 / (1 + x)) - (((2 * x) * (1 + x) - x ^ 2 * 1) / (1 + x) ^ 2)) x := by
    simpa [resF] using h
  have hval : (2 * 1 - 2 * (1 / (1 + x)) - (((2 * x) * (1 + x) - x ^ 2 * 1) / (1 + x) ^ 2))
      = x ^ 2 / (1 + x) ^ 2 := by
    field_simp [h1p]
    ring
  simpa [hval] using h'

-- H: monotone-from-derivative application
example : StrictMonoOn (fun s : ℝ => Real.sinh s - s) (Set.Ici (0 : ℝ)) := by
  refine strictMonoOn_of_deriv_pos (convex_Ici (0 : ℝ)) ?_ ?_
  · fun_prop
  · intro x hx
    have hx0 : 0 < x := by simpa [interior_Ici] using hx
    have hd : deriv (fun s : ℝ => Real.sinh s - s) x = Real.cosh x - 1 := by
      simpa using ((Real.hasDerivAt_sinh x).sub (hasDerivAt_id x)).deriv
    rw [hd]
    have hc : 1 < Real.cosh x := (Real.one_lt_cosh).2 (ne_of_gt hx0)
    linarith

example : Convex ℝ (Set.Ici (0 : ℝ)) := convex_Ici (0 : ℝ)
example : Continuous Real.sinh := by fun_prop
example (x : ℝ) (hx : x ∈ interior (Set.Ici (0:ℝ))) : 0 < x := by simpa [interior_Ici] using hx
