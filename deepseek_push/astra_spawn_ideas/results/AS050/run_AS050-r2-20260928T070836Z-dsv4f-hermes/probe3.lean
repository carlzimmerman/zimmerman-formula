import Mathlib

noncomputable section
open scoped Real
namespace Probe

/-- pointwise add, folded: (fun U => f U + g U)' = f' + g' -/
lemma add_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U + g U) (f' + g') x := by
  have h := hf.add hg
  convert h using 1
  · funext U; simp [Pi.add_apply]
  · rfl

/-- pointwise sub, folded: (fun U => f U - g U)' = f' - g' -/
lemma sub_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U - g U) (f' - g') x := by
  have h := hf.sub hg
  convert h using 1
  · funext U; simp [Pi.sub_apply]
  · rfl

/-- pointwise mul, folded: (fun U => f U * g U)' = f' * g + f * g' -/
lemma mul_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U * g U) (f' * g x + f x * g') x := by
  have h := hf.mul hg
  convert h using 1
  · funext U; simp [Pi.mul_apply]
  · rfl

end Probe