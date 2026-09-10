import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Sign certificate for the reduced exact F(Q)Theta scalar sector. -/

namespace ExactFQThetaReducedEnergy

theorem longitudinal_stiffness_pos
    (y : ℝ) (hy : 0 < y) :
    0 < 1 + (y - 1) * Real.exp (-y) := by
  by_cases h : 1 ≤ y
  · have hy1 : 0 ≤ y - 1 := by linarith
    have he : 0 < Real.exp (-y) := Real.exp_pos _
    have hmul : 0 ≤ (y - 1) * Real.exp (-y) :=
      mul_nonneg hy1 (le_of_lt he)
    linarith
  · have hy1 : y < 1 := lt_of_not_ge h
    have hneg : -y < 0 := by linarith
    have hleft : 1 - y < 1 := by linarith
    have hleft_pos : 0 < 1 - y := by linarith
    have hright : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr hneg
    have hmul : (1 - y) * Real.exp (-y) < (1 - y) * 1 :=
      mul_lt_mul_of_pos_left hright hleft_pos
    have hprod : (1 - y) * Real.exp (-y) < 1 := by
      have hrightprod : (1 - y) * 1 < 1 := by simpa using hleft
      exact lt_trans hmul hrightprod
    have hrewrite :
        1 + (y - 1) * Real.exp (-y) =
          1 - (1 - y) * Real.exp (-y) := by ring
    rw [hrewrite]
    linarith

theorem reduced_kinetic_negative
    (M2 k Q0 A : ℝ)
    (hM2 : 0 < M2) (hk : k ≠ 0) (hQ0 : Q0 ≠ 0) (hA : 0 < A) :
    -2 * M2 * k ^ 2 / (Q0 ^ 2 * A) < 0 := by
  have hk2 : 0 < k ^ 2 := sq_pos_of_ne_zero hk
  have hq2 : 0 < Q0 ^ 2 := sq_pos_of_ne_zero hQ0
  have hden : 0 < Q0 ^ 2 * A := mul_pos hq2 hA
  have hnum : 0 < 2 * M2 * k ^ 2 := by positivity
  have hnum' : -2 * M2 * k ^ 2 < 0 := by nlinarith [hnum]
  exact div_neg_of_neg_of_pos hnum' hden

theorem mixed_principal_kinetic_negative
    (Upp Unz Q0 k : ℝ)
    (hUpp : 0 < Upp) (hUnz : Unz ≠ 0) (hQ0 : Q0 ≠ 0) (hk : k ≠ 0) :
    -(Unz ^ 2 * k ^ 2) / (2 * Q0 ^ 2 * Upp) < 0 := by
  have hnum : 0 < Unz ^ 2 * k ^ 2 :=
    mul_pos (sq_pos_of_ne_zero hUnz) (sq_pos_of_ne_zero hk)
  have hden : 0 < 2 * Q0 ^ 2 * Upp := by
    positivity
  have hneg : -(Unz ^ 2 * k ^ 2) < 0 := by nlinarith [hnum]
  exact div_neg_of_neg_of_pos hneg hden

end ExactFQThetaReducedEnergy
