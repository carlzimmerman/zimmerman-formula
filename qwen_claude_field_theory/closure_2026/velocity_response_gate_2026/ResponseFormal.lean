import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Conditional algebraic consequences of the separately varied scalar action.
    This file does not formalize that variation or relativistic causality. -/
namespace VelocityResponse

theorem vanishing_stress_contact_forces_zero_braid
    (b den : ℝ) (hd : den ≠ 0) (h : (-3*b^2)/den = 0) : b = 0 := by
  have hn : -3*b^2 = 0 := (div_eq_zero_iff.mp h).resolve_right hd
  have hb : b^2 = 0 := by nlinarith
  rcases mul_eq_zero.mp (show b*b = 0 by nlinarith) with h | h
  · exact h
  · exact h

theorem healthy_tuned_kinetic (m mu : ℝ) (hm : 0 < m) (hu : 0 < mu) :
    0 < 3*m*mu/(1+mu) := by
  exact div_pos (mul_pos (mul_pos (by norm_num) hm) hu) (by linarith)

theorem zero_field_tuned_kinetic (m : ℝ) :
    3*m*(0:ℝ)/(1+0) = 0 := by norm_num

theorem angular_contact_not_constant
    (mt ml : ℝ) (ht : 0 < mt) (hl : mt < ml) :
    1/ml < 1/mt := by
  exact one_div_lt_one_div_of_lt ht hl

theorem matched_family_remainder_negative
    (d mt ml Z : ℝ) (hd : 1 < d) (ht : 0 < mt)
    (hl : mt < ml) (hZ : 0 < Z) :
    -(d^2*(d-1)^2*(ml-mt)^5*Z^5)/(9*(d-1+mt)^5) < 0 := by
  have hp : 0 < d^2*(d-1)^2*(ml-mt)^5*Z^5 :=
    mul_pos (mul_pos (mul_pos (pow_pos (by linarith) _)
      (pow_pos (by linarith) _)) (pow_pos (by linarith) _)) (pow_pos hZ _)
  have hden : 0 < (9:ℝ)*(d-1+mt)^5 :=
    mul_pos (by norm_num) (pow_pos (by linarith) _)
  exact div_neg_of_neg_of_pos (neg_neg_of_pos hp) hden

#print axioms vanishing_stress_contact_forces_zero_braid
#print axioms healthy_tuned_kinetic
#print axioms zero_field_tuned_kinetic
#print axioms angular_contact_not_constant
#print axioms matched_family_remainder_negative
end VelocityResponse
