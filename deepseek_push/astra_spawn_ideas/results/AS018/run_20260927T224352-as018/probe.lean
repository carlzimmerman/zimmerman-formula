import Mathlib

open MeasureTheory

-- T1: annotated-exact idiom
example {f : ℝ → ℝ} {f' x c : ℝ} (hf : HasDerivAt f f' x) :
    HasDerivAt (fun y : ℝ => f y + c) f' x := by
  have h : HasDerivAt (fun y : ℝ => f y + c) (f' + 0) x := by
    exact hf.add (hasDerivAt_const x c)
  simpa [add_zero] using h

-- comp: annotated-exact idiom
example {r r_ref : ℝ} (hr : 0 < r) (hr0 : r_ref ≠ 0) :
    HasDerivAt (fun s : ℝ => Real.log (s / r_ref)) ((r / r_ref)⁻¹ * (1 / r_ref)) r := by
  have hx : r / r_ref ≠ 0 := div_ne_zero (ne_of_gt hr) hr0
  have hlog : HasDerivAt Real.log ((r / r_ref)⁻¹) (r / r_ref) := by
    exact Real.hasDerivAt_log hx
  have hdiv : HasDerivAt (fun s : ℝ => s / r_ref) (1 / r_ref) r := by
    simpa using (hasDerivAt_id r).div_const r_ref
  have hc : HasDerivAt (fun s : ℝ => Real.log (s / r_ref))
      ((r / r_ref)⁻¹ * (1 / r_ref)) r := by
    exact HasDerivAt.comp r hlog hdiv
  convert hc using 1
  field_simp [ne_of_gt hr, hr0]

-- const_mul on IntegrableOn via restricted measure
example {s : Set ℝ} {μ : Measure ℝ} {ρ : ℝ → ℝ} (hρ : IntegrableOn ρ s μ) :
    IntegrableOn (fun x : ℝ => 3 * ρ x) s μ := by
  exact hρ.const_mul 3
