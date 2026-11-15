/-
RRL3R (covering the pair RRL2 and RRL3R): Lean statements for the algebra of the spherical Jeans step with the RR
Lyrae star-count slope and one constant or the measured per-bin anisotropy. They certify the algebra, not the physics,
and no number or label of the lane. TEST lane; adopts nothing.

  broken_closed_form_at_break : the closed form for a broken star-count law in a flat curve at constant beta (KA-4)
                                gives V^2 / (a_out - 2 beta) at the break radius, the outer law's value (continuity).
  los_prediction_beta_order   : at fixed slope a, for the line-of-sight factor (1 - beta sin^2 eta)/(a - 2 beta), a
                                lower beta gives a lower prediction when a sin^2 eta <= 2 (the sign of the change is
                                (beta1 - beta2)(a sin^2 eta - 2)).
  f_rises_when_prediction_falls : f^2 P = D at fixed measured D: a lower prediction P gives a higher ratio f.
  anisotropy_factor_pieces    : ln I = 2 b0 x + 2 (b1 - b0) max(x - L, 0) is 2 b0 x before the edge and
                                2 b0 L + 2 b1 (x - L) after it (exact product of power laws, continuous at the edge).
  count_two_builds_agree      : RRL2's star count (s/rb)^(-a) and RRL3R's ln n = -a ln(s/rb) are the same law, and
                                the broken law's two pieces agree at the break.
  label_rule                  : HOT (f > 1 + 2s) and COLD (f < 1 - 2s) never both apply for s >= 0, and PASS (neither)
                                is exactly |f - 1| <= 2s.
  slope_window_counts         : over 200 profile draws the NO VERDICT window 0.16 <= k/200 <= 0.84 (edges included)
                                is exactly 32 <= k <= 168 passing draws, and it is symmetric under q -> 1 - q.
  pull_test_iff               : amendment A1's per-seed test |x - t| <= 2 e is |pull| <= 2 with pull = (x - t)/e, e > 0.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace RRL3R

theorem broken_closed_form_at_break (V2 rb ai ao b : ℝ) (hrb : 0 < rb) (hao : ao - 2 * b ≠ 0) :
    (V2 * rb ^ ai * (rb ^ (2 * b - ai) - rb ^ (2 * b - ai)) / (2 * b - ai)
        + V2 * rb ^ (2 * b) / (ao - 2 * b)) / ((rb / rb) ^ (-ai) * rb ^ (2 * b))
      = V2 / (ao - 2 * b) := by
  have hp : 0 < rb ^ (2 * b) := Real.rpow_pos_of_pos hrb _
  rw [div_self hrb.ne', Real.one_rpow, sub_self, mul_zero, zero_div, zero_add, one_mul]
  field_simp

theorem los_prediction_beta_order (a s b1 b2 : ℝ) (h12 : b2 ≤ b1) (ha : 2 * b1 < a) (hs : a * s ≤ 2) :
    (1 - b2 * s) / (a - 2 * b2) ≤ (1 - b1 * s) / (a - 2 * b1) := by
  have h1 : 0 < a - 2 * b1 := by linarith
  have h2 : 0 < a - 2 * b2 := by linarith
  rw [div_le_div_iff₀ h2 h1]
  have key : (1 - b2 * s) * (a - 2 * b1) - (1 - b1 * s) * (a - 2 * b2) = (b1 - b2) * (a * s - 2) := by ring
  have hneg : (b1 - b2) * (a * s - 2) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (by linarith) (by linarith)
  linarith

theorem f_rises_when_prediction_falls (f1 f2 P1 P2 D : ℝ) (hf1 : 0 < f1) (hf2 : 0 < f2) (hP2 : 0 < P2)
    (hP : P2 ≤ P1) (h1 : f1 ^ 2 * P1 = D) (h2 : f2 ^ 2 * P2 = D) : f1 ≤ f2 := by
  by_contra hc
  have hlt : f2 < f1 := lt_of_not_ge hc
  have hsq : f2 ^ 2 < f1 ^ 2 := by nlinarith
  have : f2 ^ 2 * P2 < f1 ^ 2 * P2 := by nlinarith
  have : f1 ^ 2 * P2 ≤ f1 ^ 2 * P1 := by nlinarith
  linarith

theorem anisotropy_factor_pieces (b0 b1 L x : ℝ) :
    (x ≤ L → 2 * b0 * x + 2 * (b1 - b0) * max (x - L) 0 = 2 * b0 * x) ∧
    (L ≤ x → 2 * b0 * x + 2 * (b1 - b0) * max (x - L) 0 = 2 * b0 * L + 2 * b1 * (x - L)) := by
  constructor
  · intro h
    rw [max_eq_right (by linarith)]
    ring
  · intro h
    rw [max_eq_left (by linarith)]
    ring

theorem count_two_builds_agree (s rb a ai ao : ℝ) (hs : 0 < s) (hrb : 0 < rb) :
    Real.log ((s / rb) ^ (-a)) = -a * Real.log (s / rb) ∧
    -ai * Real.log (rb / rb) = -ao * Real.log (rb / rb) := by
  constructor
  · exact Real.log_rpow (div_pos hs hrb) _
  · rw [div_self hrb.ne', Real.log_one, mul_zero, mul_zero]

theorem label_rule (f s : ℝ) (hs : 0 ≤ s) :
    ¬ (1 + 2 * s < f ∧ f < 1 - 2 * s) ∧
    ((¬ (1 + 2 * s < f) ∧ ¬ (f < 1 - 2 * s)) ↔ |f - 1| ≤ 2 * s) := by
  constructor
  · rintro ⟨h1, h2⟩
    linarith
  · rw [abs_le]
    constructor
    · rintro ⟨h1, h2⟩
      constructor <;> linarith [not_lt.mp h1, not_lt.mp h2]
    · rintro ⟨h1, h2⟩
      constructor <;> intro h <;> linarith

theorem slope_window_counts (k q : ℝ) :
    ((0.16 ≤ k / 200 ∧ k / 200 ≤ 0.84) ↔ (32 ≤ k ∧ k ≤ 168)) ∧
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

theorem pull_test_iff (x t e : ℝ) (he : 0 < e) : |x - t| ≤ 2 * e ↔ |(x - t) / e| ≤ 2 := by
  rw [abs_div, abs_of_pos he, div_le_iff₀ he]

end RRL3R

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
