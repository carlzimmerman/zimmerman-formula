import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CubicHomogeneousGap

/- These theorems concern the normalized real-algebra gap only. They do not
formalize the action, Legendre transform, or normalization. They establish no
physical kinetic positivity, spatial ellipticity, global inverse, or DOF count. -/

def denominator (R z : ℝ) : ℝ := R - 6*z + 6*z^2

def numerator (R v z : ℝ) : ℝ :=
  R*(1-v) + (2*R+6*v)*z + (R-6*v)*z^2

noncomputable def gap (R v z : ℝ) : ℝ := (1+z)^2 / denominator R z - v/R

/-- The exact common-denominator identity requires both denominators nonzero. -/
theorem gap_identity (R v z : ℝ)
    (hR : R ≠ 0) (hD : denominator R z ≠ 0) :
    gap R v z = numerator R v z / (R * denominator R z) := by
  unfold gap numerator
  field_simp [hR, hD]
  unfold denominator
  ring

/-- Positive denominators make the gap and its numerator have the same sign. -/
theorem gap_positive_iff_numerator_positive (R v z : ℝ)
    (hR : 0 < R) (hD : 0 < denominator R z) :
    0 < gap R v z ↔ 0 < numerator R v z := by
  rw [gap_identity R v z (ne_of_gt hR) (ne_of_gt hD)]
  exact div_pos_iff_of_pos_right (mul_pos hR hD)

/-- A sufficient algebraic condition; no physical hypotheses are inferred. -/
theorem gap_positive (R v z : ℝ)
    (hR : 0 < R) (hD : 0 < denominator R z)
    (hv0 : 0 ≤ v) (hv1 : v < 1) (hz : 0 ≤ z) (hRv : 6*v ≤ R) :
    0 < gap R v z := by
  apply (gap_positive_iff_numerator_positive R v z hR hD).2
  have hconstant : 0 < R*(1-v) := mul_pos hR (by linarith)
  have hlinear : 0 ≤ (2*R+6*v)*z := mul_nonneg (by linarith) hz
  have hquadratic : 0 ≤ (R-6*v)*z^2 :=
    mul_nonneg (by linarith) (sq_nonneg z)
  unfold numerator
  linarith

#print axioms gap_identity
#print axioms gap_positive_iff_numerator_positive
#print axioms gap_positive

end CubicHomogeneousGap
