import Mathlib
import Mathlib.Tactic

noncomputable section

-- C1: deriv of inverse
example (u : ℝ) (hu : 1 + u ≠ 0) : deriv (fun x : ℝ => (1 + x)⁻¹) u = -(1 + u)⁻² := by
  simp [deriv_inv, hu]

-- C2: HasDerivAt.inv form
example (u : ℝ) (hu : 1 + u ≠ 0) : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(1 + u)⁻¹ * (1 + u)⁻¹) u := by
  have h : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  simpa [pow_two] using h.inv hu

-- C3: derivative of squared inverse
example (u : ℝ) (hu : 1 + u ≠ 0) : HasDerivAt (fun x : ℝ => ((1 + x)⁻¹)^2) (2 * (1 + u)⁻¹ * (-(1 + u)⁻¹ * (1 + u)⁻¹)) u := by
  have h : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(1 + u)⁻¹ * (1 + u)⁻¹) u := by
    have h0 : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
    simpa [pow_two] using h0.inv hu
  simpa using h.pow 2

-- C4: full mu2 derivative via 1 - (1+u)^{-2}
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt (fun x : ℝ => 1 - ((1 + x)⁻¹)^2) (2 * (1 + u)⁻³) u := by
  have h : HasDerivAt (fun x : ℝ => ((1 + x)⁻¹)^2) (2 * (1 + u)⁻¹ * (-(1 + u)⁻¹ * (1 + u)⁻¹)) u := by
    have h0 : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
    have h1 : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(1 + u)⁻¹ * (1 + u)⁻¹) u := by
      simpa [pow_two] using h0.inv hu
    simpa using h1.pow 2
  convert h.const_sub 1 using 1
  ring_nf
  field_simp [hu]

end
