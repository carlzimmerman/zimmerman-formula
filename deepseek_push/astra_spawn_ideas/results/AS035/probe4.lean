import Mathlib

noncomputable section
open Filter
open scoped Topology

-- what exactly is tendsto_inv_atTop_zero's function?
#check tendsto_inv_atTop_zero
#check Real.tendsto_sqrt_atTop
#check Function.comp

-- (i) exact with defeq beta
example : Tendsto (fun z : ℝ => (Real.sqrt z)⁻¹) atTop (𝓝 0) :=
  tendsto_inv_atTop_zero.comp Real.tendsto_sqrt_atTop

-- (ii) comp applied form
example : Tendsto (fun z : ℝ => (Real.sqrt z)⁻¹) atTop (𝓝 0) := by
  simpa using tendsto_inv_atTop_zero.comp Real.tendsto_sqrt_atTop

-- (iii) funext-style rfl for comp
example (yp : ℝ) : (fun y : ℝ => Real.log (y + yp)) = Real.log ∘ (fun y : ℝ => y + yp) := by
  funext z; rfl

-- (iv) hlog1 fully, derivative in inv form
example (yp : ℝ) (y : ℝ) (hyy : 0 < y + yp) :
    HasDerivAt (fun y : ℝ => Real.log (y + yp)) ((y + yp)⁻¹) y := by
  have hin : HasDerivAt (fun z : ℝ => z + yp) 1 y := by
    simpa [id_eq] using ((hasDerivAt_id y).add_const yp)
  have hc1 := HasDerivAt.comp (x := y) (hh₂ := Real.hasDerivAt_log hyy.ne') (hh := hin)
  simpa [mul_one] using hc1
