import Mathlib

noncomputable section
open Filter
open scoped Topology

-- probe 1: correct comp argument order for log (y + c)
example (yp : ℝ) {y : ℝ} (hyy : 0 < y + yp) :
    HasDerivAt (fun y : ℝ => Real.log (y + yp)) (1 / (y + yp)) y := by
  have hin : HasDerivAt (fun z : ℝ => z + yp) 1 y := by
    simpa using (hasDerivAt_id y).add (hasDerivAt_const y yp)
  simpa using (Real.hasDerivAt_log hyy.ne').comp hin

-- probe 2: ratio derivative
example (yp ys : ℝ) {y : ℝ} (hyy : 0 < y + yp) (hysp : 0 < ys + yp) :
    HasDerivAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) (1 / (y + yp)) y := by
  have hin : HasDerivAt (fun z : ℝ => z + yp) 1 y := by
    simpa using (hasDerivAt_id y).add (hasDerivAt_const y yp)
  have hdiv : HasDerivAt (fun z : ℝ => (z + yp) / (ys + yp)) (1 / (ys + yp)) y :=
    hin.div_const (ys + yp)
  have hpos : 0 < (y + yp) / (ys + yp) := div_pos hyy hysp
  have hc := (Real.hasDerivAt_log hpos.ne').comp hdiv
  convert hc using 1
  · rfl
  · field_simp [hyy.ne', hysp.ne']
