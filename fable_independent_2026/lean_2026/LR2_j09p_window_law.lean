import Mathlib

/-!
# LR2 — J09p general-p window law, Lean certificate (M-roads Lean roadmap)

SCOPE (I-series precedent): Lean certifies the ALGEBRA. The physics input — that the
generalized-p atom window reads `W_p(q) = (1 + q/(p+1)) / (1/2 + q/(p+2))` — is a
hypothesis; its Monte-Carlo verification (J09p, 21/21, `J09p_general_p.py` exit 0,
falsifier: measured deviation > 5 SE from `(p+2)/(p+1)` at any p ∈ {1,2,4}) is the
empirical leg and is NOT re-proven here. LR1 (banked) is the p = 2 instance.

Content (`p ≥ 1`, `q ≥ 0`):
* `denom_pos_p` — the denominator `1/2 + q/(p+2)` is positive.
* `Wp_le_two` — `W_p(q) ≤ 2` (q = 0 endpoint).
* `Wp_ge_limit` — `W_p(q) ≥ (p+2)/(p+1)` (the q → ∞ limit).
* `Wp_antitone_q` — strictly decreasing in q; cross-difference exactly
  `(b - a) * p / (2 * (p+1) * (p+2))`.
* `Wp_mem` — the J09p band `[(p+2)/(p+1), 2]`.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

noncomputable def Wp (p q : ℝ) : ℝ := (1 + q / (p + 1)) / (1 / 2 + q / (p + 2))

theorem denom_pos_p (p : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) : 0 < 1 / 2 + q / (p + 2) := by
  have h2 : 0 < p + 2 := by linarith
  have hqn : 0 ≤ q / (p + 2) := div_nonneg hq h2.le
  linarith

theorem Wp_le_two (p : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) : Wp p q ≤ 2 := by
  have hden : 0 < 1 / 2 + q / (p + 2) := denom_pos_p p hp hq
  have h1 : 0 < p + 1 := by linarith
  have h2 : 0 < p + 2 := by linarith
  have hp0 : 0 ≤ p := by linarith
  have hqp : 0 ≤ q * p := by nlinarith [hq, hp0]
  have hq3 : q / (p + 1) ≤ 2 * (q / (p + 2)) := by
    have h4 : 2 * (q / (p + 2)) = 2 * q / (p + 2) := by ring
    rw [h4, div_le_div_iff₀ h1 h2]
    linarith [hqp]
  rw [Wp, div_le_iff₀ hden, show 2 * (1 / 2 + q / (p + 2)) = 1 + 2 * (q / (p + 2)) by ring]
  linarith [hq3]

theorem Wp_ge_limit (p : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) :
    (p + 2) / (p + 1) ≤ Wp p q := by
  have hden : 0 < 1 / 2 + q / (p + 2) := denom_pos_p p hp hq
  have h1 : 0 < p + 1 := by linarith
  have h2 : 0 < p + 2 := by linarith
  rw [Wp, div_le_div_iff₀ h1 hden]
  field_simp
  linarith

theorem Wp_prod (p : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) : Wp p q
    = 2 * (p + 2) * (p + 1 + q) / ((p + 1) * (p + 2 + 2 * q)) := by
  have h1 : 0 < p + 1 := by linarith
  have h2 : 0 < p + 2 + 2 * q := by nlinarith
  rw [Wp]
  field_simp

theorem Wp_antitone_q (p : ℝ) (hp : 1 ≤ p) {a b : ℝ} (hab : 0 ≤ a) (hab' : a < b) :
    Wp p b < Wp p a := by
  have h1 : 0 < p + 1 := by linarith
  have hp0 : 0 < p := by linarith
  have hba : 0 < b - a := by linarith
  have hbp : 0 < (b - a) * p := by nlinarith [hba, hp0]
  have hdiff : (p + 1 + b) * (p + 2 + 2 * a)
      = (p + 1 + a) * (p + 2 + 2 * b) - (b - a) * p := by ring
  have key : (p + 1 + b) * (p + 2 + 2 * a) < (p + 1 + a) * (p + 2 + 2 * b) := by
    linarith [hdiff, hbp]
  have hC : 0 < 2 * (p + 2) * (p + 1) := by nlinarith
  have hd1 : 0 < (p + 1) * (p + 2 + 2 * b) := by
    have : 0 < p + 2 + 2 * b := by nlinarith
    nlinarith
  have hd2 : 0 < (p + 1) * (p + 2 + 2 * a) := by
    have : 0 < p + 2 + 2 * a := by nlinarith
    nlinarith
  rw [Wp_prod p hp (by linarith), Wp_prod p hp hab, div_lt_div_iff₀ hd1 hd2]
  nlinarith [key, hC]

theorem Wp_mem (p : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) :
    (p + 2) / (p + 1) ≤ Wp p q ∧ Wp p q ≤ 2 :=
  ⟨Wp_ge_limit p hp hq, Wp_le_two p hp hq⟩

#print axioms denom_pos_p
#print axioms Wp_le_two
#print axioms Wp_ge_limit
#print axioms Wp_prod
#print axioms Wp_antitone_q
#print axioms Wp_mem
