import Mathlib
noncomputable section
namespace WeylCancellation

theorem curvature_identity (riem ric R : ℝ) :
    (riem - 4*ric + R^2) - (riem - 2*ric + R^2/3) =
    2*R^2/3 - 2*ric := by ring

theorem einstein_value (R : ℝ) :
    2*R^2/3 - 2*(R^2/4) = R^2/6 := by ring

theorem source_cancellation (H w : ℝ) :
    (24*H^4+w)-w=24*H^4 := by ring

theorem cancellation_selects_relative_coefficient (H w t : ℝ) (hw : w ≠ 0) :
    (24*H^4+w)-t*w=24*H^4 ↔ t=1 := by
  constructor
  · intro h
    have he : (1-t)*w=0 := by nlinarith
    have ht : 1-t=0 := (mul_eq_zero.mp he).resolve_right hw
    linarith
  · intro h
    subst t
    ring

#print axioms curvature_identity
#print axioms einstein_value
#print axioms source_cancellation
#print axioms cancellation_selects_relative_coefficient
end WeylCancellation
