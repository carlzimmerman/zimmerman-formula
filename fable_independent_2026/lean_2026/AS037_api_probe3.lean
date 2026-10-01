import Mathlib
noncomputable section
open Real Filter

-- variant A: target fn written as FUNCTION power (what HasDerivAt.pow produces)
example (u : ℝ) : HasDerivAt (((fun v : ℝ => 1 + v) ^ (2:ℕ))) (2 * (1 + u)) u := by
  have hlin : HasDerivAt (fun v : ℝ => 1 + v) 1 u := (hasDerivAt_id u).const_add 1
  simpa using hlin.pow 2

-- variant B: pointwise target like probe 4's (id shape via const_add on pow? same class as A but different fn)
example (u : ℝ) : HasDerivAt (fun v : ℝ => 1 + v ^ (2:ℕ)) (2 * u) u := by
  have hid : HasDerivAt (fun v : ℝ => v) 1 u := hasDerivAt_id u
  simpa using (hid.pow 2).const_add 1

-- variant C: without pow lemma — derivative of (fun v => (1+v)*(1+v)) via hlin.mul hlin
example (u : ℝ) : HasDerivAt (fun v : ℝ => (1 + v) * (1 + v)) (2 * (1 + u)) u := by
  have hlin : HasDerivAt (fun v : ℝ => 1 + v) 1 u := (hasDerivAt_id u).const_add 1
  have hmul := hlin.mul hlin
  simpa [two_mul] using hmul

end
