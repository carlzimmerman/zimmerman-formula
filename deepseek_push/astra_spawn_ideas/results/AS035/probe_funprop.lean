import Mathlib

noncomputable section
open Filter
open scoped Topology

-- probe: fun_prop for log derivative computations
example (yp ys : ℝ) {y : ℝ} (hyy : 0 < y + yp) (hysp : 0 < ys + yp) :
    HasDerivAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) (1 / (y + yp)) y := by
  fun_prop

example (hδ : 0 < δ) (hhp : 0 < hp) (hysp : 0 < ys + yp) {y : ℝ} (hy : -yp < y) :
    HasDerivAt (fun y : ℝ => hR + δ * hp * Real.log ((y + yp) / (ys + yp)))
      (δ * hp / (y + yp)) y := by
  fun_prop

example (hδ : 0 < δ) (hhp : 0 < hp) (hysp : 0 < ys + yp) {y : ℝ} (hy : -yp < y) :
    HasDerivAt (fun y : ℝ => hR + δ * hp * Real.log ((y + yp) / (ys + yp)))
      (δ * hp / (y + yp)) y := by
  have hyy : 0 < y + yp := by linarith
  have hpos : 0 < (y + yp) / (ys + yp) := by positivity
  fun_prop
