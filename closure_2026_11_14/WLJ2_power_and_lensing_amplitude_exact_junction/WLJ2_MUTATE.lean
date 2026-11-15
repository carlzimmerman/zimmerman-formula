/-
WLJ2 MUTATE twin: the statements of WLJ2.lean, each with one false change (a factor, a threshold, an inequality or a
hypothesis direction) and the same proof script. Every theorem is false and must fail (expected: exit 1, an error in
every theorem). TEST lane; adopts nothing.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace WLJ2_MUTATE

theorem p4_width_identity_mut (a b c s : ℝ) (ha : 0 < a) :
    (a * s ^ 2 + b * s + c) - (a * (-b / (2 * a)) ^ 2 + b * (-b / (2 * a)) + c) =
      2 * ((s - (-b / (2 * a))) / (1 / Real.sqrt a)) ^ 2 := by
  have hs : Real.sqrt a ^ 2 = a := Real.sq_sqrt ha.le
  have ha' : a ≠ 0 := ha.ne'
  rw [div_div_eq_mul_div, div_one, mul_pow, hs]
  field_simp
  ring

theorem twl_tot_doubles_mut (Rbar Rcold Rtot Rcold' Rtot' : ℝ) (h1 : Rtot = Rbar * Rcold)
    (h2 : Rcold' = 1 + 2 * (Rcold - 1)) (h3 : Rtot' = Rbar * Rcold') :
    Rtot' - Rbar = Rtot - Rbar := by
  rw [h3, h2, h1]
  ring

theorem twl_linear_bites_mut (Tr Te Tt : ℝ) (h : Tt - Tr = 2 * (Te - Tr)) :
    2 * |Te - Tr| ≤ |Tt - Te| := by
  have e : Tt - Te = Te - Tr := by linarith
  rw [e]
  have := abs_nonneg (Te - Tr)
  linarith

theorem three_words_partition_mut (lo hi x : ℝ) (h : lo ≤ hi) :
    (x < lo ∨ (lo ≤ x ∧ x < hi) ∨ hi ≤ x) ∧ ¬ (x < hi ∧ lo ≤ x) ∧ ¬ (x < lo ∧ hi ≤ x) ∧
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

theorem surv_consistent_excludes_mut (g : ℝ) (h : |g| ≤ 2) : ¬ (1 < g) ∧ ¬ (g < -2) := by
  rw [abs_le] at h
  constructor <;> intro h' <;> linarith [h.1, h.2]

theorem tension_stat_exclusive_mut (Δ δ : ℝ) (hδ : 0 ≤ δ) :
    ¬ (δ < Δ ∧ Δ < -δ) ∧ ((¬ (δ < Δ) ∧ ¬ (Δ < -δ)) ↔ |Δ| < δ) := by
  constructor
  · rintro ⟨h1, h2⟩
    linarith
  · rw [abs_le]
    constructor
    · rintro ⟨h1, h2⟩
      exact ⟨by linarith [not_lt.mp h2], not_lt.mp h1⟩
    · rintro ⟨h1, h2⟩
      exact ⟨not_lt.mpr h2, not_lt.mpr (by linarith)⟩

theorem exact_excess_outside_mut (CBi CRi CR Ctot t : ℝ) (hden : CRi < Ctot) (hlaw : CBi < CRi)
    (hCR : CR ≤ Ctot) (ht : t * (Ctot - CRi) = Ctot - CBi) :
    t ≤ 1 ∧ CR ≤ CBi + t * (CR - CRi) := by
  have ht1 : t ≤ 1 := by
    by_contra hc
    have hc' : 1 < t := lt_of_not_ge hc
    nlinarith [mul_lt_mul_of_pos_right hc' (sub_pos.mpr hden)]
  refine ⟨ht1, ?_⟩
  nlinarith [mul_nonneg (sub_nonneg.mpr ht1) (sub_nonneg.mpr hCR)]

end WLJ2_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
