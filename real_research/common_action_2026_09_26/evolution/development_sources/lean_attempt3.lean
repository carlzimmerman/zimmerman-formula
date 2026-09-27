import Mathlib

/-! Conditional scalar and finite-Markov bridges. No PDE, action variation,
invariant-region or global-existence theorem is claimed. -/
namespace EvolutionBridge20260926

theorem strong_monotonicity_norm_bridge (du df : ℝ)
    (hf : 0 ≤ df) (hm : du ^ 2 ≤ df * du) : du ≤ df := by
  nlinarith

theorem resolvent_complement_bound (u v : ℝ) (hm : 0 ≤ u * v) :
    u ^ 2 + v ^ 2 ≤ (u + v) ^ 2 := by
  nlinarith

theorem two_site_Jensen_identity (C₁ C₂ f g : ℝ) :
    ((3 * C₁ + C₂) / 4 * f ^ 2 + (C₁ + 3 * C₂) / 4 * g ^ 2) -
      (C₁ * ((3 * f + g) / 4) ^ 2 + C₂ * ((f + 3 * g) / 4) ^ 2) =
      3 / 16 * (C₁ + C₂) * (f - g) ^ 2 := by
  ring

theorem two_site_Jensen_bound (C₁ C₂ f g : ℝ)
    (h₁ : 0 ≤ C₁) (h₂ : 0 ≤ C₂) :
    C₁ * ((3 * f + g) / 4) ^ 2 + C₂ * ((f + 3 * g) / 4) ^ 2 ≤
      (3 * C₁ + C₂) / 4 * f ^ 2 + (C₁ + 3 * C₂) / 4 * g ^ 2 := by
  have hp : 0 ≤ 3 / 16 * (C₁ + C₂) * (f - g) ^ 2 := by positivity
  have hid := two_site_Jensen_identity C₁ C₂ f g
  linarith

theorem convex_composition_Hessian (Gp Gpp Jpp tangent : ℝ)
    (h₁ : 0 ≤ Gp) (h₂ : 0 ≤ Gpp) (h₃ : 0 ≤ Jpp) :
    0 ≤ Gp * Jpp + Gpp * tangent ^ 2 := by
  positivity

theorem active_small_field_transversality (J ell lap theta : ℝ)
    (he : 0 < ell) (hJ : J ≤ theta / 2)
    (ha : 0 < J + ell * lap - theta) : theta / (2 * ell) < lap := by
  apply (div_lt_iff₀ (mul_pos (by norm_num) he)).2
  nlinarith

theorem finite_alpha_negative_branch (a b C : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hC : 0 ≤ C)
    (hcross : 2 < a * (1 + C)) :
    b * (2 - a * (1 + C)) / ((2 + 3 * b) * (a + (a + 2) * C)) < 0 := by
  apply div_neg_of_neg_of_pos
  · exact mul_neg_of_pos_of_neg hb (by linarith)
  · positivity

theorem positive_C_is_not_sufficient :
    (1 / 100 : ℝ) * (2 - (1 / 10) * (1 + 30)) /
      ((2 + 3 * (1 / 100)) * ((1 / 10) + ((1 / 10) + 2) * 30)) < 0 := by
  norm_num

theorem repaired_host_positive (a b C : ℝ)
    (ha : 0 < a) (ha2 : a < 2) (hb : 0 < b) (hC : 0 ≤ C) :
    0 < b * (2 - a) / ((2 + 3 * b) * (a + 2 * C)) := by
  have hn : 0 < 2 - a := sub_pos.mpr ha2
  positivity

theorem repaired_effective_coefficient_interval (a C : ℝ)
    (ha : 0 < a) (ha2 : a < 2) (hC : 0 ≤ C) :
    0 < (a + 2 * C) / (1 + C) ∧ (a + 2 * C) / (1 + C) < 2 := by
  have hd : 0 < 1 + C := by linarith
  constructor
  · positivity
  · apply (div_lt_iff₀ hd).2
    linarith

theorem compensated_cross_window (ell r : ℝ)
    (he : 0 < ell) (he4 : ell < 4) (hr : 0 ≤ r) (hr1 : r ≤ 1) :
    0 < 1 - ell * r / 4 ∧ 1 - ell * r / 4 ≤ 1 := by
  have hp := mul_nonneg (le_of_lt he) hr
  have hgap := mul_nonneg (le_of_lt he) (sub_nonneg.mpr hr1)
  constructor <;> nlinarith

theorem compensated_effective_coefficient_window (a Q D : ℝ)
    (ha : 0 < a) (ha2 : a < 2) (hQ : 0 < Q) (hQ1 : Q ≤ 1) (hD : 1 ≤ D) :
    a ≤ 2 - (2 - a) * Q ^ 2 / D ∧ 2 - (2 - a) * Q ^ 2 / D < 2 := by
  have hd : 0 < D := by linarith
  have hn : 0 < 2 - a := by linarith
  have hsq : Q ^ 2 ≤ D := by nlinarith
  have hfrac : (2 - a) * Q ^ 2 / D ≤ 2 - a := by
    apply (div_le_iff₀ hd).2
    nlinarith [mul_nonneg (le_of_lt hn) (sub_nonneg.mpr hsq)]
  have hpos : 0 < (2 - a) * Q ^ 2 / D := by positivity
  constructor <;> linarith

end EvolutionBridge20260926
#print axioms EvolutionBridge20260926.strong_monotonicity_norm_bridge
#print axioms EvolutionBridge20260926.resolvent_complement_bound
#print axioms EvolutionBridge20260926.two_site_Jensen_identity
#print axioms EvolutionBridge20260926.two_site_Jensen_bound
#print axioms EvolutionBridge20260926.convex_composition_Hessian
#print axioms EvolutionBridge20260926.active_small_field_transversality
#print axioms EvolutionBridge20260926.finite_alpha_negative_branch
#print axioms EvolutionBridge20260926.positive_C_is_not_sufficient

#print axioms EvolutionBridge20260926.repaired_host_positive
#print axioms EvolutionBridge20260926.repaired_effective_coefficient_interval

#print axioms EvolutionBridge20260926.compensated_cross_window
#print axioms EvolutionBridge20260926.compensated_effective_coefficient_window
