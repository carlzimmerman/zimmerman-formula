import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination

namespace CorrectedPressure

theorem tracked_pressure (U s gamma q qprime : ℝ) :
    -U+s*(U-2*gamma*q^2*qprime)+2*gamma*q^2*(s*qprime)
      = U*(s-1) := by ring

theorem clock_rate_from_tracked_pressure (U margin s gamma q qprime w : ℝ)
    (hU : U ≠ 0) (hm : margin ≠ 0)
    (hstate : w*(U/margin) =
      -U+s*(U-2*gamma*q^2*qprime)+2*gamma*q^2*(s*qprime)) :
    s-1 = w/margin := by
  rw [tracked_pressure] at hstate
  field_simp at hstate ⊢
  linear_combination -hstate

#print axioms tracked_pressure
#print axioms clock_rate_from_tracked_pressure
end CorrectedPressure
