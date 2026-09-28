import Mathlib
import Mathlib.Data.Real.Basic

open Polynomial
noncomputable section

/-- probe: degree lemmas exact statements -/
#check Polynomial.degree_X_pow
#check Polynomial.degree_C
#check Polynomial.degree_mul_le
#check Polynomial.degree_add_le
#check Polynomial.degree_sub_le
#check Polynomial.coeff_mul_X_pow
#check Set.mem_uIcc
#check Set.uIcc
#check WithBot.coe_le_coe
#check WithBot.coe_lt_coe

def Ppoly (y : ℝ) : Polynomial ℝ := X^3 + C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)

example (y : ℝ) : ((X : Polynomial ℝ)^3).degree ≤ (3 : WithBot ℕ) := by
  simp [degree_X_pow]

example (y : ℝ) : (C (4 - y)).degree ≤ (0 : WithBot ℕ) := by
  by_cases h : 4 - y = 0
  · simp [h]
  · rw [degree_C h]
    exact le_rfl

example (y : ℝ) : ((X : Polynomial ℝ)^2).degree = (2 : WithBot ℕ) := by
  simp [degree_X_pow]

example (y : ℝ) :
    (C (4 - y) * X^2).degree ≤ (2 : WithBot ℕ) := by
  have hd2a : (C (4 - y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 - y = 0
    · simp [h]
    · rw [degree_C h]
  have hd2b : ((X : Polynomial ℝ)^2).degree = (2 : WithBot ℕ) := by simp
  exact le_trans (degree_mul_le (C (4 - y)) (X^2)) (by
    rw [hd2b]
    exact add_le_add hd2a le_rfl)

example : (1 : WithBot ℕ) ≤ (2 : WithBot ℕ) := by
  norm_num

/-- probe: exact_mod_cast from WithBot ℕ to ℕ -/
example (p : Multiset ℝ) (hp : (p.card : WithBot ℕ) ≤ (3 : WithBot ℕ)) : p.card ≤ 3 := by
  exact_mod_cast hp

example (y : ℝ) : (Ppoly y).degree ≤ (3 : WithBot ℕ) := by
  have hd1 : ((X : Polynomial ℝ)^3).degree ≤ (3 : WithBot ℕ) := by simp [degree_X_pow]
  have hd2a : (C (4 - y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 - y = 0
    · simp [h]
    · rw [degree_C h]; exact le_rfl
  have hd2b : ((X : Polynomial ℝ)^2).degree = (2 : WithBot ℕ) := by simp [degree_X_pow]
  have hd2 : (C (4 - y) * X^2).degree ≤ (2 : WithBot ℕ) := by
    exact le_trans (degree_mul_le (C (4 - y)) (X^2)) (by
      rw [hd2b]
      exact add_le_add hd2a le_rfl)
  have hd3a : (C (4 * y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 * y = 0
    · simp [h]
    · rw [degree_C h]; exact le_rfl
  have hd3b : (X : Polynomial ℝ).degree = (1 : WithBot ℕ) := by simp [degree_X_pow]
  have hd3 : (C (4 * y) * X).degree ≤ (1 : WithBot ℕ) := by
    exact le_trans (degree_mul_le (C (4 * y)) X) (by
      rw [hd3b]
      exact add_le_add hd3a le_rfl)
  have hd4 : (C (4 * y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 * y = 0
    · simp [h]
    · rw [degree_C h]; exact le_rfl
  have hrest1 : (C (4 - y) * X^2 - C (4 * y) * X).degree ≤ (2 : WithBot ℕ) := by
    exact le_trans (degree_sub_le _ _) (by
      exact max_le_iff.mpr ⟨hd2, le_trans hd3 (by norm_num)⟩)
  have hrest : (C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)).degree ≤ (2 : WithBot ℕ) := by
    exact le_trans (degree_sub_le _ _) (by
      exact max_le_iff.mpr ⟨hrest1, le_trans hd4 (by norm_num)⟩)
  unfold Ppoly
  exact le_trans (degree_add_le _ _) (max_le_iff.mpr ⟨hd1, hrest⟩)

lemma Ppoly_coeff3 (y : ℝ) : (Ppoly y).coeff 3 = 1 := by
  unfold Ppoly
  rw [coeff_add, coeff_sub, coeff_sub]
  rw [coeff_mul_X_pow (p := C 4 - C y) (n := 2) (m := 1)]
  rw [coeff_mul_X_pow (p := C (4 * y)) (n := 1) (m := 2)]
  rw [coeff_sub]
  simp

/-- probe: uIcc membership construction -/
example (a b : ℝ) (ha : a ≤ (0 : ℝ)) (hb : (0 : ℝ) ≤ b) :
    (0 : ℝ) ∈ Set.uIcc a b := by
  exact (Set.mem_uIcc.mpr (Or.inl ⟨ha, hb⟩))

/-- probe: two_pow_neg_two -/
lemma two_pow_neg_two {x : ℝ} (hx2 : x + 2 ≠ 0) :
    (1 + x / 2) ^ (-2 : ℤ) = 4 / (x + 2)^2 := by
  rw [zpow_neg (a := (1 + x / 2 : ℝ)) (n := (2 : ℤ))]
  rw [inv_eq_one_div]
  have hs : (1 + x / 2 : ℝ)^2 = (x + 2)^2 / 4 := by ring
  rw [hs]
  field_simp [hx2]
  ring

/-- probe: card-cons simp closure -/
example (r1 r2 rp : ℝ) (t3 : Multiset ℝ) (h : (r1 ::ₘ r2 ::ₘ rp ::ₘ t3).card = 3) :
    t3.card = 0 := by
  have hc' : t3.card + 3 = 3 := by
    simpa [Multiset.card_cons, add_assoc, add_comm, add_left_comm] using h
  omega
