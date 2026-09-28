import Mathlib

noncomputable section
open Filter
open scoped Topology

#check HasDerivAt.add_const
#check HasDerivAt.congr_of_eventuallyEq
#check HasDerivAt.const_mul
#check inv_div
#check one_div

-- probe A: hnum via add_const
example (yp : ℝ) (y : ℝ) : HasDerivAt (fun y : ℝ => y + yp) (1 : ℝ) y := by
  simpa [id_eq] using ((hasDerivAt_id y).add_const yp)

-- probe B: hz via comp, plain simpa
example : Tendsto (fun z : ℝ => (1 : ℝ) / Real.sqrt z) atTop (𝓝 0) := by
  simpa using (tendsto_inv_atTop_zero.comp Real.tendsto_sqrt_atTop)

-- probe C: the hlog expression via congr_of_eventuallyEq
example (yp ys : ℝ) (y : ℝ) (hyy : 0 < y + yp) (hysp : 0 < ys + yp) :
    HasDerivAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) (1 / (y + yp)) y := by
  have hnum : HasDerivAt (fun y : ℝ => y + yp) (1 : ℝ) y := by
    simpa [id_eq] using ((hasDerivAt_id y).add_const yp)
  have hf : HasDerivAt (fun y : ℝ => (y + yp) / (ys + yp)) (1 / (ys + yp)) y :=
    hnum.div_const (ys + yp)
  have hfpos : 0 < (y + yp) / (ys + yp) := div_pos hyy hysp
  have hc := HasDerivAt.comp (x := y) (hh₂ := Real.hasDerivAt_log hfpos.ne') (hh := hf)
  refine hc.congr_of_eventuallyEq ?_ ?_
  · filter_upwards [lt_mem_nhds hyy] with z hz
    rfl
  · rw [inv_div]
    field_simp [hyy.ne', hysp.ne']

-- probe D: hmain value-eq + add_const chain
example (δ hp : ℝ) (yp ys y : ℝ) (hyy : 0 < y + yp) (hysp : 0 < ys + yp) :
    HasDerivAt (fun y : ℝ => hR + δ * hp * Real.log ((y + yp) / (ys + yp)))
      (δ * hp / (y + yp)) y := by
  have hnum : HasDerivAt (fun y : ℝ => y + yp) (1 : ℝ) y := by
    simpa [id_eq] using ((hasDerivAt_id y).add_const yp)
  have hf : HasDerivAt (fun y : ℝ => (y + yp) / (ys + yp)) (1 / (ys + yp)) y :=
    hnum.div_const (ys + yp)
  have hfpos : 0 < (y + yp) / (ys + yp) := div_pos hyy hysp
  have hc := HasDerivAt.comp (x := y) (hh₂ := Real.hasDerivAt_log hfpos.ne') (hh := hf)
  have hlog : HasDerivAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) (1 / (y + yp)) y := by
    refine hc.congr_of_eventuallyEq ?_ ?_
    · filter_upwards [lt_mem_nhds hyy] with z hz
      rfl
    · rw [inv_div]
      field_simp [hyy.ne', hysp.ne']
  have hmain : HasDerivAt (fun y : ℝ => δ * hp * Real.log ((y + yp) / (ys + yp)))
      (δ * hp / (y + yp)) y := by
    refine (hlog.const_mul (δ * hp)).congr_of_eventuallyEq ?_ ?_
    · filter_upwards with z; rfl
    · simp
  refine hmain.const_add hR
