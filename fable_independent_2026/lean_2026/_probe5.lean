import Mathlib
import Mathlib.Tactic

noncomputable section

-- A: inv then .deriv with simpa
example (u : ℝ) (hu : 1 + u ≠ 0) : deriv (fun x : ℝ => (1 + x)⁻¹) u = -1 / (1 + u)^2 := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  have hinv0 := hlin.inv hu
  simpa [Pi.inv_apply] using hinv0.deriv

-- B: div route for (1)/(1+x)^2
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt (fun x : ℝ => (1 : ℝ) / (1 + x)^2) (-2 * (1 + u) / ((1 + u)^2)^2) u := by
  have hnum : HasDerivAt (fun x : ℝ => (1 : ℝ)) 0 u := hasDerivAt_const u (1 : ℝ)
  have hden : HasDerivAt (fun x : ℝ => (1 + x)^2) (2 * (1 + u) * 1) u := by
    have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
    simpa using hlin.pow 2
  have hdenne : (1 + u)^2 ≠ 0 := pow_ne_zero 2 hu
  have h := hnum.div hden hdenne
  simpa using h

-- C: hasDerivAt_pow works?
example (u : ℝ) : HasDerivAt (fun x : ℝ => x ^ 2) (2 * u) u := by
  simpa using hasDerivAt_pow 2 u

-- D: quotient rule for mu2 directly
def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt mu2 (((2 + 2 * u) * (1 + u)^2 - (u * (2 + u)) * (2 * (1 + u) * 1)) / ((1 + u)^2)^2) u := by
  unfold mu2
  have hn : HasDerivAt (fun x : ℝ => x * (2 + x)) ((1) * (2 + u) + u * (0 + 1)) u := by
    exact (hasDerivAt_id u).mul ((hasDerivAt_const u (2 : ℝ)).add (hasDerivAt_id u))
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  have hd : HasDerivAt (fun x : ℝ => (1 + x)^2) (2 * (1 + u) * 1) u := by
    simpa using hlin.pow 2
  exact hn.div hd (pow_ne_zero 2 hu)

-- E: is there a direct name for derivative of inv?
-- #check hasDerivAt_inv
-- #check HasDerivAt.inv
#check hasDerivAt_inv
#check hasDerivAt_div
#check HasDerivAt.div
