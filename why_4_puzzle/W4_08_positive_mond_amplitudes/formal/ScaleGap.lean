module

public import Mathlib.Data.Real.Basic
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Ring.Basic

@[expose] public section

/-!
Ordered-field implications of the explicitly stated scale/gap Hessian.
The differentiated potential-to-Hessian dictionary is an input here;
the microscopic origin of that potential is not asserted.
-/

namespace Why4.ScaleGap

def Positive2 (a b c : ℝ) : Prop :=
  ∀ x y : ℝ, x ≠ 0 ∨ y ≠ 0 → 0 < a * x ^ 2 + 2 * b * x * y + c * y ^ 2

theorem first_diagonal_positive {a b c : ℝ} (h : Positive2 a b c) : 0 < a := by
  simpa using h 1 0 (Or.inl one_ne_zero)

theorem second_diagonal_positive {a b c : ℝ} (h : Positive2 a b c) : 0 < c := by
  simpa using h 0 1 (Or.inr one_ne_zero)

theorem schur_positive {a b c : ℝ} (h : Positive2 a b c) : 0 < a - b ^ 2 / c := by
  have hc := second_diagonal_positive h
  have htest := h 1 (-b / c) (Or.inl one_ne_zero)
  have hid : a * 1 ^ 2 + 2 * b * 1 * (-b / c) + c * (-b / c) ^ 2
      = a - b ^ 2 / c := by
    field_simp [ne_of_gt hc]
    <;> ring1
  rwa [hid] at htest

theorem positive_energy_requires_running
    (D F Ft Ftt Ftd Fdd : ℝ)
    (hD : 0 < D) (hF : 0 < F) (hstationary : D * F + Ft = 0)
    (hstable : Positive2 (D * Ft + Ftt) Ftd Fdd) :
    Ft < 0 ∧ D * |Ft| + Ftd ^ 2 / Fdd < Ftt := by
  have hDF : 0 < D * F := mul_pos hD hF
  have ht : Ft < 0 := by linarith
  have hs := schur_positive hstable
  constructor
  · exact ht
  · rw [abs_of_neg ht]
    linarith

theorem single_log_positive_energy_negative_curvature
    (D F B : ℝ)
    (hD : 0 < D) (hF : 0 < F) (hstationary : D * F + B = 0) :
    D * B < 0 := by
  have hB : B < 0 := by linarith [mul_pos hD hF]
  exact mul_neg_of_pos_of_neg hD hB

theorem no_single_log_positive_minimum
    (D F B Bprime Fdd : ℝ)
    (hD : 0 < D) (hF : 0 < F) (hstationary : D * F + B = 0) :
    ¬ Positive2 (D * B) Bprime Fdd := by
  intro hstable
  have hDB := first_diagonal_positive hstable
  have hneg := single_log_positive_energy_negative_curvature D F B hD hF hstationary
  linarith

theorem scale_invariant_stationary_zero
    (D F : ℝ) (hD : 0 < D) (hstationary : D * F = 0) : F = 0 := by
  exact (mul_eq_zero.mp hstationary).resolve_left (ne_of_gt hD)

#check @schur_positive
#check @positive_energy_requires_running
#check @single_log_positive_energy_negative_curvature
#check @no_single_log_positive_minimum
#check @scale_invariant_stationary_zero
#print axioms schur_positive
#print axioms positive_energy_requires_running
#print axioms single_log_positive_energy_negative_curvature
#print axioms no_single_log_positive_minimum
#print axioms scale_invariant_stationary_zero

end Why4.ScaleGap
