import Mathlib

noncomputable section
open scoped Real
namespace Probe

lemma q_aux2 {X : ℝ} (hX : 0 < X)
    (hvv2 : (Real.sqrt (1 + 4 * X)) ^ 2 = 1 + 4 * X)
    (hww2 : (Real.sqrt X) ^ 2 = X) :
    4 * ((Real.sqrt (1 + 4 * X)) ^ 2 + (Real.sqrt X) ^ 2 * 4)
          * (2 * Real.sqrt X + Real.sqrt (1 + 4 * X))
        + 2 * (2 * Real.sqrt (1 + 4 * X) + Real.sqrt X * 4)
        - 2 * 4 * Real.sqrt (1 + 4 * X) * (2 * Real.sqrt X + Real.sqrt (1 + 4 * X))
    = 2 * 4 * Real.sqrt (1 + 4 * X) * (2 * Real.sqrt X + Real.sqrt (1 + 4 * X))
        * (Real.sqrt (1 + 4 * X) - 1) := by
  nlinarith [hvv2, hww2]

end Probe