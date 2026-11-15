/-
WLJ2: Lean statements for the algebra of the matter-power (row 24) and weak-lensing-amplitude (row 25) rows read with
the exact junction. They certify the algebra, not the physics, and no number or label of the lane. XJ1.lean's theorems
on the exact junction are not restated. TEST lane; adopts nothing.

  p4_width_identity     : the P4 scan fits chi^2(s) = a s^2 + b s + c (a > 0), best s_b = -b / (2a), width 1 / sqrt a;
                          the statistic T1 = (s_pinned - s_b) / width is the square root of the chi-square rise from
                          the best fit to the pinned sigma8: chi^2(s_pinned) - chi^2(s_b) = T1^2.
  twl_tot_doubles       : twin TW-L (R_cold' - 1 = 2 (R_cold - 1), R_tot' = R_bar R_cold', R_tot = R_bar R_cold)
                          doubles the layout's change of the total power: R_tot' - R_bar = 2 (R_tot - R_bar).
  twl_linear_bites      : if a statistic responds linearly to the doubled change (T_TWL - T_REF = 2 (T_Ec2 - T_REF)),
                          the bite rule |T_TWL - T_Ec2| >= (1/2) |T_Ec2 - T_REF| holds.
  three_words_partition : a statistic against two lines lo <= hi falls in exactly one of x < lo, lo <= x < hi,
                          hi <= x (C5 d_cold: CONSISTENT / TENSION / EXCLUDED at 4 and 9; P4 p: EXCLUDED / TENSION /
                          CONSISTENT at 0.0027 and 0.05).
  surv_consistent_excludes : a survey reading with |g| <= 2 (CONSISTENT) can be neither GAP STAYS (g > 2) nor
                          OVERSHOOT (g < -2).
  tension_stat_exclusive : with a floor delta >= 0 (0.02 for T1, T6, T7), one statistic's Delta cannot count both
                          toward WORSENS (Delta > delta) and toward RELIEVES (Delta < -delta), and it counts toward
                          neither exactly when |Delta| <= delta.
  exact_excess_outside  : outside R_set, when the law's enclosed cold mass at R_set is at least the reference's and
                          C_R(R_set) < C_tot and C_R(r) <= C_tot, then t <= 1 and the exact junction encloses at least
                          the reference's cold mass at r (the difference is (1 - t) (C_tot - C_R(r)) >= 0).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace WLJ2

theorem p4_width_identity (a b c s : ℝ) (ha : 0 < a) :
    (a * s ^ 2 + b * s + c) - (a * (-b / (2 * a)) ^ 2 + b * (-b / (2 * a)) + c) =
      ((s - (-b / (2 * a))) / (1 / Real.sqrt a)) ^ 2 := by
  have hs : Real.sqrt a ^ 2 = a := Real.sq_sqrt ha.le
  have ha' : a ≠ 0 := ha.ne'
  rw [div_div_eq_mul_div, div_one, mul_pow, hs]
  field_simp
  ring

theorem twl_tot_doubles (Rbar Rcold Rtot Rcold' Rtot' : ℝ) (h1 : Rtot = Rbar * Rcold)
    (h2 : Rcold' = 1 + 2 * (Rcold - 1)) (h3 : Rtot' = Rbar * Rcold') :
    Rtot' - Rbar = 2 * (Rtot - Rbar) := by
  rw [h3, h2, h1]
  ring

theorem twl_linear_bites (Tr Te Tt : ℝ) (h : Tt - Tr = 2 * (Te - Tr)) :
    1 / 2 * |Te - Tr| ≤ |Tt - Te| := by
  have e : Tt - Te = Te - Tr := by linarith
  rw [e]
  have := abs_nonneg (Te - Tr)
  linarith

theorem three_words_partition (lo hi x : ℝ) (h : lo ≤ hi) :
    (x < lo ∨ (lo ≤ x ∧ x < hi) ∨ hi ≤ x) ∧ ¬ (x < lo ∧ lo ≤ x) ∧ ¬ (x < lo ∧ hi ≤ x) ∧
    ¬ ((lo ≤ x ∧ x < hi) ∧ hi ≤ x) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rcases lt_or_ge x lo with h1 | h1
    · exact Or.inl h1
    · rcases lt_or_ge x hi with h2 | h2
      · exact Or.inr (Or.inl ⟨h1, h2⟩)
      · exact Or.inr (Or.inr h2)
  · rintro ⟨h1, h2⟩
    linarith
  · rintro ⟨h1, h2⟩
    linarith
  · rintro ⟨⟨_, h1⟩, h2⟩
    linarith

theorem surv_consistent_excludes (g : ℝ) (h : |g| ≤ 2) : ¬ (2 < g) ∧ ¬ (g < -2) := by
  rw [abs_le] at h
  constructor <;> intro h' <;> linarith [h.1, h.2]

theorem tension_stat_exclusive (Δ δ : ℝ) (hδ : 0 ≤ δ) :
    ¬ (δ < Δ ∧ Δ < -δ) ∧ ((¬ (δ < Δ) ∧ ¬ (Δ < -δ)) ↔ |Δ| ≤ δ) := by
  constructor
  · rintro ⟨h1, h2⟩
    linarith
  · rw [abs_le]
    constructor
    · rintro ⟨h1, h2⟩
      exact ⟨by linarith [not_lt.mp h2], not_lt.mp h1⟩
    · rintro ⟨h1, h2⟩
      exact ⟨not_lt.mpr h2, not_lt.mpr (by linarith)⟩

theorem exact_excess_outside (CBi CRi CR Ctot t : ℝ) (hden : CRi < Ctot) (hlaw : CRi ≤ CBi)
    (hCR : CR ≤ Ctot) (ht : t * (Ctot - CRi) = Ctot - CBi) :
    t ≤ 1 ∧ CR ≤ CBi + t * (CR - CRi) := by
  have ht1 : t ≤ 1 := by
    by_contra hc
    have hc' : 1 < t := lt_of_not_ge hc
    nlinarith [mul_lt_mul_of_pos_right hc' (sub_pos.mpr hden)]
  refine ⟨ht1, ?_⟩
  nlinarith [mul_nonneg (sub_nonneg.mpr ht1) (sub_nonneg.mpr hCR)]

end WLJ2

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
