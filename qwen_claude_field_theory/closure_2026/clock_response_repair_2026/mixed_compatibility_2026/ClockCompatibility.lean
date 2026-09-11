/- UNVERIFIED DRAFT: the local Mathlib cache fails while importing MeanValue,
   before elaborating these declarations. See lean_attempt_001/manifest.json. -/
import Mathlib.Analysis.Calculus.MeanValue

/- At fixed time, f represents u_t and g represents (N Q)_r.
   These identifications and the covariant action are NOT formalized here.
   The derivative bound is required throughout the interval, not at grid
   points alone. This is a continuum consistency lemma, not a gravity proof. -/
namespace ClockCompatibility
noncomputable section

/-- A uniform mixed-jet defect controls the rate defect from the center. -/
theorem rate_error_bound (f g : ℝ → ℝ) (r eps : ℝ) (hr : 0 ≤ r)
    (hf : ∀ x ∈ Set.Icc 0 r, DifferentiableAt ℝ f x)
    (hg : ∀ x ∈ Set.Icc 0 r, DifferentiableAt ℝ g x)
    (hb : ∀ x ∈ Set.Icc 0 r, ‖deriv f x - deriv g x‖ ≤ eps)
    (hc : f 0 = g 0) : ‖f r - g r‖ ≤ eps * r := by
  have h := Convex.norm_image_sub_le_of_norm_deriv_le
    (f := fun x => f x - g x)
    (fun x hx => (hf x hx).sub (hg x hx))
    (fun x hx => by simpa only [deriv_sub (hf x hx) (hg x hx)] using hb x hx)
    (convex_Icc (0 : ℝ) r) (Set.left_mem_Icc.mpr hr) (Set.right_mem_Icc.mpr hr)
  simpa [hc, Real.norm_eq_abs, abs_of_nonneg hr] using h

/-- Equal mixed jets and the same center value leave no rate freedom. -/
theorem rate_unique (f g : ℝ → ℝ) (r : ℝ) (hr : 0 ≤ r)
    (hf : ∀ x ∈ Set.Icc 0 r, DifferentiableAt ℝ f x)
    (hg : ∀ x ∈ Set.Icc 0 r, DifferentiableAt ℝ g x)
    (he : ∀ x ∈ Set.Icc 0 r, deriv f x = deriv g x)
    (hc : f 0 = g 0) : f r = g r := by
  have h := rate_error_bound f g r 0 hr hf hg
    (fun x hx => by simp [he x hx]) hc
  have hz : ‖f r - g r‖ = 0 := le_antisymm (by simpa using h) (norm_nonneg _)
  exact sub_eq_zero.mp (norm_eq_zero.mp hz)

#print axioms rate_error_bound
#print axioms rate_unique
end
end ClockCompatibility
