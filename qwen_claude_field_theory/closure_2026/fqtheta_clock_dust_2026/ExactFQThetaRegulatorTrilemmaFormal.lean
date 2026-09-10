import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-! Formal sign certificate for the mixed F(Q)Theta regulator trilemma. -/

namespace ExactFQThetaRegulatorTrilemma

theorem mixed_branch_ghost_and_oscillatory
    (Upp Uzz Unz Q0 k : ℝ)
    (hUpp : 0 < Upp) (hUzz : 0 < Uzz)
    (hUnz : Unz ≠ 0) (hQ0 : Q0 ≠ 0) (hk : k ≠ 0) :
    (-(Unz ^ 2 * k ^ 2) / (2 * Q0 ^ 2 * Upp) < 0) ∧
      (0 < Q0 ^ 2 * Upp * Uzz / Unz ^ 2) := by
  constructor
  · have hnum : 0 < Unz ^ 2 * k ^ 2 :=
      mul_pos (sq_pos_of_ne_zero hUnz) (sq_pos_of_ne_zero hk)
    have hden : 0 < 2 * Q0 ^ 2 * Upp := by positivity
    have hneg : -(Unz ^ 2 * k ^ 2) < 0 := by nlinarith [hnum]
    exact div_neg_of_neg_of_pos hneg hden
  · have hnum : 0 < Q0 ^ 2 * Upp * Uzz := by positivity
    have hden : 0 < Unz ^ 2 := sq_pos_of_ne_zero hUnz
    exact div_pos hnum hden

theorem flipped_stiffness_gradient_instability
    (Upp Uzz Unz Q0 : ℝ)
    (hUpp : Upp < 0) (hUzz : 0 < Uzz)
    (hUnz : Unz ≠ 0) (hQ0 : Q0 ≠ 0) :
    Q0 ^ 2 * Upp * Uzz / Unz ^ 2 < 0 := by
  have hq : 0 < Q0 ^ 2 := sq_pos_of_ne_zero hQ0
  have hu : 0 < Q0 ^ 2 * Uzz := mul_pos hq hUzz
  have hnum : Q0 ^ 2 * Upp * Uzz < 0 := by
    have hneg : (Q0 ^ 2 * Uzz) * Upp < 0 := mul_neg_of_pos_of_neg hu hUpp
    simpa [mul_assoc, mul_left_comm, mul_comm] using hneg
  have hden : 0 < Unz ^ 2 := sq_pos_of_ne_zero hUnz
  exact div_neg_of_neg_of_pos hnum hden

end ExactFQThetaRegulatorTrilemma
