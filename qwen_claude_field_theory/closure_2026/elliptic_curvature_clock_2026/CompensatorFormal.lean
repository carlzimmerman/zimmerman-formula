import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Conditional principal-symbol proofs, not full nonlinear gravity closure. -/
namespace EllipticCurvatureClock

noncomputable def scalarSpeedSquared (mu : ℝ) : ℝ := 2*mu/(3*(1+mu))

theorem scalar_speed_positive_and_subluminal (mu : ℝ) (h : 0 < mu) :
    0 < scalarSpeedSquared mu ∧ scalarSpeedSquared mu < 2/3 := by
  have hd : 0 < (3 : ℝ)*(1+mu) := by nlinarith
  constructor
  · exact div_pos (by linarith) hd
  · unfold scalarSpeedSquared
    apply (div_lt_iff₀ hd).2
    nlinarith

theorem zero_field_speed : scalarSpeedSquared 0 = 0 := by
  norm_num [scalarSpeedSquared]

theorem tensor_kinetic_positive (m chi : ℝ) (hm : 0 < m) :
    0 < m * Real.exp (2*chi) / 2 := by
  exact div_pos (mul_pos hm (Real.exp_pos _)) (by norm_num)

noncomputable def spatialRemainder (mt ml Z : ℝ) : ℝ :=
  -(4*(ml-mt)^5*Z^5)/(9*(1+mt)^5)

theorem anisotropic_remainder_nonzero
    (mt ml Z : ℝ) (ht : 0 < mt) (hl : mt < ml) (hZ : 0 < Z) :
    spatialRemainder mt ml Z < 0 := by
  have hp : 0 < (4 : ℝ)*(ml-mt)^5*Z^5 :=
    mul_pos (mul_pos (by norm_num) (pow_pos (by linarith) _)) (pow_pos hZ _)
  have hd : 0 < (9 : ℝ)*(1+mt)^5 :=
    mul_pos (by norm_num) (pow_pos (by linarith) _)
  exact div_neg_of_neg_of_pos (neg_neg_of_pos hp) hd

#print axioms scalar_speed_positive_and_subluminal
#print axioms tensor_kinetic_positive
#print axioms anisotropic_remainder_nonzero
end EllipticCurvatureClock
