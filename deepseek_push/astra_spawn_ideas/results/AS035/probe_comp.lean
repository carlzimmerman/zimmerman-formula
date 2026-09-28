import Mathlib

noncomputable section
open Filter
open scoped Topology

#check HasDerivAt.comp

example (yp ys : ℝ) {y : ℝ} (hyy : 0 < y + yp) (hysp : 0 < ys + yp) :
    HasDerivAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) (1 / (y + yp)) y := by
  have hin : HasDerivAt (fun z : ℝ => z + yp) 1 y := by
    simpa [id] using ((hasDerivAt_id y).add (hasDerivAt_const y yp))
  have hdiv : HasDerivAt (fun z : ℝ => (z + yp) / (ys + yp)) (1 / (ys + yp)) y :=
    hin.div_const (ys + yp)
  have hpos : 0 < (y + yp) / (ys + yp) := div_pos hyy hysp
  have hc := HasDerivAt.comp (Real.hasDerivAt_log hpos.ne') hdiv
  -- hc : HasDerivAt (Real.log ∘ fun z => (z+yp)/(ys+yp)) (((y+yp)/(ys+yp))⁻¹ * (1/(ys+yp))) y
  convert hc using 1
  · rfl
  · field_simp [hyy.ne', hysp.ne']
