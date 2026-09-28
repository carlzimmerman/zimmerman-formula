import Mathlib

noncomputable section
open scoped Real
namespace Probe

example {f g : ℝ → ℝ} : (fun U : ℝ => f U + g U) = (f + g) := by
  funext U; rfl

example : True := by
  have e1 : (Real.instAddCommGroup = Real.normedAddCommGroup.toAddCommGroup) := by rfl
  have e2 : (Semiring.toModule = (NormedAlgebra.toNormedSpace ℝ).toModule) := by rfl
  trivial

lemma add_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U + g U) (f' + g') x := by
  have h : HasDerivAt (f + g) (f' + g') x := hf.add hg
  convert h using 1
  · rfl
  · funext U; rfl
  · rfl

end Probe