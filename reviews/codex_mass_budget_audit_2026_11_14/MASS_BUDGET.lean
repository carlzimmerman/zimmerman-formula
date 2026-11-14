/-
MASS_BUDGET: Lean statements for the algebra of the crossing-speed correction and of the charge-budget bound audited
in this folder. They certify the algebra, not the physics, and no number of the audit. Written by the lead.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.

  crossing_speed      : v^3 = 10 G q M_b H and v^4 = G M_b a0 meet only at v = a0 / (10 q H).
  equal_share_point   : for the law g^2 = g_N (a0 + g), the law's enclosed mass equals the share's (g = q g_N)
                        exactly when a0 = q (q - 1) g_N.
  law_exceeds_share   : and it exceeds the share when a0 > q (q - 1) g_N (slow systems: the corrected direction).
  law_below_share     : and falls short of it when a0 < q (q - 1) g_N (fast systems).
  budget_bound        : with C (C + b) = k b r^2, C <= Q exactly when k b r^2 <= Q (Q + b).
  transport_identity  : the kinematic interpolation's velocity satisfies partial_t C + v partial_r C = 0.
-/
import Mathlib

namespace MASS_BUDGET

theorem crossing_speed (G q Mb H a0 v : ℝ) (hG : 0 < G) (hq : 0 < q) (hM : 0 < Mb) (hH : 0 < H)
    (h3 : v ^ 3 = 10 * G * q * Mb * H) (h4 : v ^ 4 = G * Mb * a0) : v = a0 / (10 * q * H) := by
  have hden : (10 * q * H) ≠ 0 := by positivity
  have hGM : (G * Mb) ≠ 0 := by positivity
  rw [eq_div_iff hden]
  have e : v ^ 4 = v * v ^ 3 := by ring
  rw [h3, h4] at e
  have e2 : (G * Mb) * (v * (10 * q * H)) = (G * Mb) * a0 := by nlinarith [e]
  exact mul_left_cancel₀ hGM e2

theorem equal_share_point (g gN a0 q : ℝ) (hg : 0 < g) (hgN : 0 < gN) (hq : 1 ≤ q)
    (hlaw : g ^ 2 = gN * (a0 + g)) : g = q * gN ↔ a0 = q * (q - 1) * gN := by
  constructor
  · intro h
    rw [h] at hlaw
    have e : gN * (q ^ 2 * gN) = gN * (a0 + q * gN) := by nlinarith [hlaw]
    have e2 := mul_left_cancel₀ hgN.ne' e
    nlinarith [e2]
  · intro h
    have e : (g - q * gN) * (g + (q - 1) * gN) = 0 := by nlinarith [hlaw, h]
    rcases mul_eq_zero.mp e with h1 | h1
    · linarith
    · exfalso
      have h2 : 0 ≤ (q - 1) * gN := mul_nonneg (by linarith) hgN.le
      linarith

theorem law_exceeds_share (g gN a0 q : ℝ) (hg : 0 < g) (hgN : 0 < gN) (hq : 1 ≤ q)
    (hlaw : g ^ 2 = gN * (a0 + g)) (ha : q * (q - 1) * gN < a0) : q * gN < g := by
  by_contra hle
  push_neg at hle
  have h2 : 0 ≤ (q - 1) * gN := mul_nonneg (by linarith) hgN.le
  nlinarith [mul_pos hgN (sub_pos.mpr ha), mul_nonneg (sub_nonneg.mpr hle) (by linarith : (0:ℝ) ≤ g + (q - 1) * gN), hlaw]

theorem law_below_share (g gN a0 q : ℝ) (hg : 0 < g) (hgN : 0 < gN) (hq : 1 ≤ q)
    (hlaw : g ^ 2 = gN * (a0 + g)) (ha : a0 < q * (q - 1) * gN) : g < q * gN := by
  by_contra hle
  push_neg at hle
  have h2 : 0 ≤ (q - 1) * gN := mul_nonneg (by linarith) hgN.le
  nlinarith [mul_pos hgN (sub_pos.mpr ha), mul_nonneg (sub_nonneg.mpr hle) (by linarith : (0:ℝ) ≤ g + (q - 1) * gN), hlaw]

theorem budget_bound (C Q b k r : ℝ) (hC : 0 ≤ C) (hQ : 0 ≤ Q) (hb : 0 ≤ b) (hdef : C * (C + b) = k * b * r ^ 2) :
    C ≤ Q ↔ k * b * r ^ 2 ≤ Q * (Q + b) := by
  rw [← hdef]
  constructor
  · intro h
    nlinarith [mul_nonneg (sub_nonneg.mpr h) (by linarith : (0:ℝ) ≤ Q + C + b)]
  · intro h
    by_contra hlt
    push_neg at hlt
    nlinarith [mul_pos (sub_pos.mpr hlt) (by linarith : (0:ℝ) < C + Q + b)]

theorem transport_identity (adot CE CR a CRp CEp v : ℝ) (hden : (1 - a) * CRp + a * CEp ≠ 0)
    (hv : v * ((1 - a) * CRp + a * CEp) = -adot * (CE - CR)) :
    adot * (CE - CR) + v * ((1 - a) * CRp + a * CEp) = 0 := by
  linarith

end MASS_BUDGET

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
