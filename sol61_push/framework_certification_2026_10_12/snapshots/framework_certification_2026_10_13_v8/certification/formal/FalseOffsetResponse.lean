import Mathlib
/- EXPECTED FAILURE: adding offset 5 to W(x)=x does not add 5 to its derivative. -/
example : deriv (fun x : ℝ => 5 + x) 0 = 6 := by
  have h : HasDerivAt (fun x : ℝ => 5 + x) 1 0 :=
    (hasDerivAt_id (0 : ℝ)).const_add 5
  rw [h.deriv]
  norm_num
