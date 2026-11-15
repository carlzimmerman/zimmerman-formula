/-
RRL3R MUTATE twin: the statements of RRL3R.lean with one sign, factor or direction changed. Every theorem is false
and must fail (expected: exit 1, an error in every theorem). TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace RRL3R_MUTATE

theorem broken_closed_form_at_break_mut (V2 rb ai ao b : ℝ) (hrb : 0 < rb) (hao : ao - 2 * b ≠ 0) :
    (V2 * rb ^ ai * (rb ^ (2 * b - ai) - rb ^ (2 * b - ai)) / (2 * b - ai)
        + V2 * rb ^ (2 * b) / (ao - 2 * b)) / ((rb / rb) ^ (-ai) * rb ^ (2 * b))
      = V2 / (ao + 2 * b) := by
  have hp : 0 < rb ^ (2 * b) := Real.rpow_pos_of_pos hrb _
  rw [div_self hrb.ne', Real.one_rpow, sub_self, mul_zero, zero_div, zero_add, one_mul]
  field_simp

theorem los_prediction_beta_order_mut (a s b1 b2 : ℝ) (h12 : b2 ≤ b1) (ha : 2 * b1 < a) (hs : a * s ≤ 2) :
    (1 - b1 * s) / (a - 2 * b1) ≤ (1 - b2 * s) / (a - 2 * b2) := by
  have h1 : 0 < a - 2 * b1 := by linarith
  have h2 : 0 < a - 2 * b2 := by linarith
  rw [div_le_div_iff₀ h2 h1]
  have key : (1 - b2 * s) * (a - 2 * b1) - (1 - b1 * s) * (a - 2 * b2) = (b1 - b2) * (a * s - 2) := by ring
  have hneg : (b1 - b2) * (a * s - 2) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (by linarith) (by linarith)
  linarith

theorem f_rises_when_prediction_falls_mut (f1 f2 P1 P2 D : ℝ) (hf1 : 0 < f1) (hf2 : 0 < f2) (hP2 : 0 < P2)
    (hP : P2 ≤ P1) (h1 : f1 ^ 2 * P1 = D) (h2 : f2 ^ 2 * P2 = D) : f2 ≤ f1 := by
  by_contra hc
  have hlt : f2 < f1 := lt_of_not_ge hc
  have hsq : f2 ^ 2 < f1 ^ 2 := by nlinarith
  have : f2 ^ 2 * P2 < f1 ^ 2 * P2 := by nlinarith
  have : f1 ^ 2 * P2 ≤ f1 ^ 2 * P1 := by nlinarith
  linarith

theorem anisotropy_factor_pieces_mut (b0 b1 L x : ℝ) :
    (x ≤ L → 2 * b0 * x + 2 * (b1 - b0) * max (x - L) 0 = 2 * b0 * x) ∧
    (L ≤ x → 2 * b0 * x + 2 * (b1 - b0) * max (x - L) 0 = 2 * b0 * L + 2 * b1 * (x + L)) := by
  constructor
  · intro h
    rw [max_eq_right (by linarith)]
    ring
  · intro h
    rw [max_eq_left (by linarith)]
    ring

theorem count_two_builds_agree_mut (s rb a ai ao : ℝ) (hs : 0 < s) (hrb : 0 < rb) :
    Real.log ((s / rb) ^ (-a)) = a * Real.log (s / rb) ∧
    -ai * Real.log (rb / rb) = -ao * Real.log (rb / rb) := by
  constructor
  · exact Real.log_rpow (div_pos hs hrb) _
  · rw [div_self hrb.ne', Real.log_one, mul_zero, mul_zero]

theorem label_rule_mut (f s : ℝ) (hs : 0 ≤ s) :
    ¬ (1 + 2 * s < f ∧ f < 1 - 2 * s) ∧
    ((¬ (1 + 2 * s < f) ∧ ¬ (f < 1 - 2 * s)) ↔ |f - 1| ≤ s) := by
  constructor
  · rintro ⟨h1, h2⟩
    linarith
  · rw [abs_le]
    constructor
    · rintro ⟨h1, h2⟩
      constructor <;> linarith [not_lt.mp h1, not_lt.mp h2]
    · rintro ⟨h1, h2⟩
      constructor <;> intro h <;> linarith

theorem slope_window_counts_mut (k q : ℝ) :
    ((0.16 ≤ k / 200 ∧ k / 200 ≤ 0.84) ↔ (32 ≤ k ∧ k ≤ 169)) ∧
    ((0.16 ≤ q ∧ q ≤ 0.84) ↔ (0.16 ≤ 1 - q ∧ 1 - q ≤ 0.84)) := by
  constructor
  · constructor
    · rintro ⟨h1, h2⟩
      constructor <;> linarith
    · rintro ⟨h1, h2⟩
      constructor <;> linarith
  · constructor
    · rintro ⟨h1, h2⟩
      constructor <;> linarith
    · rintro ⟨h1, h2⟩
      constructor <;> linarith

theorem pull_test_iff_mut (x t e : ℝ) (he : 0 < e) : |x - t| ≤ 2 * e ↔ |(x - t) / e| ≤ 1 := by
  rw [abs_div, abs_of_pos he, div_le_iff₀ he]

end RRL3R_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
