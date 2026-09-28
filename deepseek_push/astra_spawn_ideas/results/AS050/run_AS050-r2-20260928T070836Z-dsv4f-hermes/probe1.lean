import Mathlib

noncomputable section
open scoped Real
namespace Probe

-- strategy test: comp of exp with neg-sqrt, assigned via convert
theorem t1 {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => Real.exp (-Real.sqrt U))
      (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X)))) X := by
  have hw : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hw
  have hneg : HasDerivAt (fun U : ℝ => -Real.sqrt U) (-(1 / (2 * Real.sqrt X))) X := hsq.neg
  have hc' : HasDerivAt (Real.exp ∘ fun U : ℝ => -Real.sqrt U)
      (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X)))) X :=
    (Real.hasDerivAt_exp (-Real.sqrt X)).comp X hneg
  convert hc' using 1
  · ext U; simp
  · rfl

end Probe