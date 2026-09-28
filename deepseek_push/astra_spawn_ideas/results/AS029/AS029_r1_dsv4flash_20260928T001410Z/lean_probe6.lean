import Mathlib
import Mathlib.Data.Real.Basic

open Polynomial
noncomputable section

def Ppoly (y : ℝ) : Polynomial ℝ := X^3 + C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)

#check Polynomial.degree_neg

/-- probe B: full two_pow_neg_two -/
lemma two_pow_neg_two {x : ℝ} (hx2 : x + 2 ≠ 0) :
    (1 + x / 2) ^ (-2 : ℤ) = 4 / (x + 2)^2 := by
  have hz : (1 + x / 2 : ℝ) ^ (-2 : ℤ) = ((1 + x / 2 : ℝ) ^ (2 : ℤ))⁻¹ := by
    simpa using (zpow_neg (a := (1 + x / 2 : ℝ)) (n := (2 : ℤ)))
  rw [hz]
  have hz2 : (1 + x / 2 : ℝ) ^ (2 : ℤ) = (1 + x / 2 : ℝ)^2 := by norm_num
  rw [hz2, inv_eq_one_div]
  have hs : (1 + x / 2 : ℝ)^2 = (x + 2)^2 / 4 := by ring
  rw [hs]
  field_simp [hx2]

/-- probe D: Ppoly_coeff3 -/
lemma Ppoly_coeff3 (y : ℝ) : (Ppoly y).coeff 3 = 1 := by
  unfold Ppoly
  rw [coeff_sub, coeff_sub, coeff_add]
  rw [coeff_mul_X_pow (p := C (4 - y)) (n := 2) (d := 1)]
  rw [coeff_mul_X_pow (p := C (4 * y)) (n := 1) (d := 2)]
  rw [coeff_sub]
  simp

/-- probe E: full degree bound with nested grouping -/
lemma Ppoly_degree_le (y : ℝ) : (Ppoly y).degree ≤ (3 : WithBot ℕ) := by
  have hd1 : ((X : Polynomial ℝ)^3).degree ≤ (3 : WithBot ℕ) := by simp
  have hd2a : (C (4 - y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 - y = 0
    · simp [h]
    · rw [degree_C h]
  have hd2b : ((X : Polynomial ℝ)^2).degree = (2 : WithBot ℕ) := by simp
  have hd2 : (C (4 - y) * X^2).degree ≤ (2 : WithBot ℕ) := by
    exact le_trans (degree_mul_le (C (4 - y)) (X^2)) (by
      rw [hd2b]
      exact add_le_add hd2a le_rfl)
  have hd3a : (C (4 * y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 * y = 0
    · simp [h]
    · rw [degree_C h]
  have hd3b : (X : Polynomial ℝ).degree = (1 : WithBot ℕ) := by simp
  have hd3 : (C (4 * y) * X).degree ≤ (1 : WithBot ℕ) := by
    exact le_trans (degree_mul_le (C (4 * y)) X) (by
      rw [hd3b]
      exact add_le_add hd3a le_rfl)
  have hd4 : (C (4 * y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 * y = 0
    · simp [h]
    · rw [degree_C h]
  have hnegC : degree (-(C (4 * y) * X)) ≤ (1 : WithBot ℕ) := by
    rw [degree_neg]
    exact hd3
  have ht1 : (X^3 + C (4 - y) * X^2).degree ≤ (3 : WithBot ℕ) := by
    exact le_trans (degree_add_le (X^3) (C (4 - y) * X^2))
      (max_le_iff.mpr ⟨hd1, le_trans hd2 (by norm_num)⟩)
  have ht2 : (X^3 + C (4 - y) * X^2 - C (4 * y) * X).degree ≤ (3 : WithBot ℕ) := by
    exact le_trans (degree_add_le (X^3 + C (4 - y) * X^2) (-(C (4 * y) * X)))
      (max_le_iff.mpr ⟨ht1, le_trans hnegC (by norm_num)⟩)
  have hnegD : degree (-(C (4 * y))) ≤ (0 : WithBot ℕ) := by
    rw [degree_neg]
    exact hd4
  unfold Ppoly
  exact le_trans (degree_add_le (X^3 + C (4 - y) * X^2 - C (4 * y) * X) (-(C (4 * y))))
    (max_le_iff.mpr ⟨ht2, le_trans hnegD (by norm_num)⟩)

example (y : ℝ) : (Ppoly y).degree ≤ (3 : WithBot ℕ) := Ppoly_degree_le y

/-- probe F: uIcc membership -/
example (a b : ℝ) (ha : a ≤ (0 : ℝ)) (hb : (0 : ℝ) ≤ b) :
    (0 : ℝ) ∈ Set.uIcc a b := by
  exact Set.mem_uIcc.mpr (Or.inl ⟨ha, hb⟩)

/-- probe G: card simp closure -/
example (r1 r2 rp : ℝ) (t3 : Multiset ℝ)
    (hroots : (r1 ::ₘ r2 ::ₘ rp ::ₘ t3 : Multiset ℝ).card = 3) :
    t3.card = 0 := by
  have hc' : t3.card + 3 = 3 := by
    simpa [Multiset.card_cons, add_assoc, add_comm, add_left_comm] using hroots
  omega

/-- probe H: exact_mod_cast WithBot -> Nat -/
example (p : Multiset ℝ) (hp : (p.card : WithBot ℕ) ≤ (3 : WithBot ℕ)) : p.card ≤ 3 := by
  exact_mod_cast hp
