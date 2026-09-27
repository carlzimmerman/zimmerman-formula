import Mathlib

/-! Exact regularization identities used by PERSPECTIVE_REPAIR.md.
These are algebraic certificates, not an elliptic existence formalization. -/
namespace BarrierBridge20260926

def fLow (d t : ℝ) := (t^2/d^2-3*t/d+3)/d
def dfLow (d t : ℝ) := 2*t/d^3-3/d^2

theorem regularization_positive_decomposition (d t : ℝ) (hd : d ≠ 0) :
    fLow d t = ((2*t-3*d)^2+3*d^2)/(4*d^3) := by
  unfold fLow
  field_simp
  ring

theorem regularization_virial_identity (d t : ℝ) (hd : d ≠ 0) :
    fLow d t + t*dfLow d t = 3*(t-d)^2/d^3 := by
  unfold fLow dfLow
  field_simp
  ring

theorem regularization_dominated (d t : ℝ) (hd : d ≠ 0) (ht : t ≠ 0) :
    1/t-fLow d t = (1-t/d)^3/t := by
  unfold fLow
  field_simp
  ring

end BarrierBridge20260926
#print axioms BarrierBridge20260926.regularization_positive_decomposition
#print axioms BarrierBridge20260926.regularization_virial_identity
#print axioms BarrierBridge20260926.regularization_dominated
