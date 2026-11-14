/-
MASS_BUDGET MUTATE twin: the statements of MASS_BUDGET.lean with a sign, a factor or an inequality changed. Every
theorem is false and must fail (expected: exit 1, one error per theorem). The second one is the reversed
inequality that versions 1.3 and 1.4 of PAPER72 carried. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace MASS_BUDGET_MUTATE

theorem crossing_speed_flip (G q Mb H a0 v : ℝ) (hG : 0 < G) (hq : 0 < q) (hM : 0 < Mb) (hH : 0 < H)
    (h3 : v ^ 3 = 10 * G * q * Mb * H) (h4 : v ^ 4 = G * Mb * a0) : v = a0 / (5 * q * H) := by
  have hden : (5 * q * H) ≠ 0 := by positivity
  have hGM : (G * Mb) ≠ 0 := by positivity
  rw [eq_div_iff hden]
  have e : v ^ 4 = v * v ^ 3 := by ring
  rw [h3, h4] at e
  have e2 : (G * Mb) * (v * (5 * q * H)) = (G * Mb) * a0 := by nlinarith [e]
  exact mul_left_cancel₀ hGM e2

theorem law_exceeds_share_reversed (g gN a0 q : ℝ) (hg : 0 < g) (hgN : 0 < gN) (hq : 1 ≤ q)
    (hlaw : g ^ 2 = gN * (a0 + g)) (ha : q * (q - 1) * gN < a0) : g < q * gN := by
  by_contra hle
  push_neg at hle
  have h2 : 0 ≤ (q - 1) * gN := mul_nonneg (by linarith) hgN.le
  nlinarith [mul_pos hgN (sub_pos.mpr ha), mul_nonneg (sub_nonneg.mpr hle) (by linarith : (0:ℝ) ≤ g + (q - 1) * gN), hlaw]

theorem budget_bound_flip (C Q b k r : ℝ) (hC : 0 ≤ C) (hQ : 0 ≤ Q) (hb : 0 ≤ b) (hdef : C * (C + b) = k * b * r ^ 2) :
    C ≤ Q ↔ Q * (Q + b) ≤ k * b * r ^ 2 := by
  rw [← hdef]
  constructor
  · intro h
    nlinarith [mul_nonneg (sub_nonneg.mpr h) (by linarith : (0:ℝ) ≤ Q + C + b)]
  · intro h
    by_contra hlt
    push_neg at hlt
    nlinarith [mul_pos (sub_pos.mpr hlt) (by linarith : (0:ℝ) < C + Q + b)]

theorem transport_identity_flip (adot CE CR a CRp CEp v : ℝ) (hden : (1 - a) * CRp + a * CEp ≠ 0)
    (hv : v * ((1 - a) * CRp + a * CEp) = -adot * (CE - CR)) :
    adot * (CE - CR) - v * ((1 - a) * CRp + a * CEp) = 0 := by
  linarith

end MASS_BUDGET_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
