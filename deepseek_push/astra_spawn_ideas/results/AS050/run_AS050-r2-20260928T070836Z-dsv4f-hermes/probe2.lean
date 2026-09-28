import Mathlib

noncomputable section
open scoped Real
namespace Probe

theorem t2 {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => 1 + Real.sqrt U) (1 / (2 * Real.sqrt X)) X := by
  have hwid : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hwid
  exact (hasDerivAt_const X (1 : ℝ)).add hsq

theorem t3 {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => Real.exp (-Real.sqrt U))
      (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X)))) X := by
  have hwid : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hwid
  have hneg : HasDerivAt (fun U : ℝ => -Real.sqrt U) (-(1 / (2 * Real.sqrt X))) X := hsq.neg
  exact (Real.hasDerivAt_exp (-Real.sqrt X)).comp X hneg

theorem t4 {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => 1 + Real.sqrt U / 2) (1 / (2 * Real.sqrt X) / 2) X := by
  have hwid : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hwid
  exact (hasDerivAt_const X (1 : ℝ)).add (hsq.div_const 2)

end Probe