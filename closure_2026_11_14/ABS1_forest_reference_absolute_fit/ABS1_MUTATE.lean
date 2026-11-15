/-
ABS1 MUTATE twin: the statements of ABS1.lean, each with one false change (a factor, a sign or an inequality
direction) and the same proof script. Every theorem is false and must fail (expected: exit 1, an error in every
theorem). TEST lane; adopts nothing.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

open Matrix

namespace ABS1_MUTATE

theorem gate_scale_const_mut {n : ℕ} (W : Matrix (Fin n) (Fin n) ℝ) (r P : Fin n → ℝ) (c : ℝ) :
    (fun i => (r i - 1) * (c * P i)) ⬝ᵥ (W *ᵥ (fun i => (r i - 1) * (c * P i))) =
      c * ((fun i => (r i - 1) * P i) ⬝ᵥ (W *ᵥ (fun i => (r i - 1) * P i))) := by
  have h : (fun i => (r i - 1) * (c * P i)) = c • (fun i => (r i - 1) * P i) := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul]
    ring
  rw [h, mulVec_smul, dotProduct_smul, smul_dotProduct, smul_eq_mul, smul_eq_mul]
  ring

theorem gate_blockwise_bounds_mut {J : ℕ} (c Dj : Fin J → ℝ) (lo hi : ℝ) (hlo : 0 ≤ lo)
    (hD : ∀ j, 0 ≤ Dj j) (hc : ∀ j, lo ≤ c j ∧ c j ≤ hi) :
    lo * ∑ j, Dj j ≤ ∑ j, c j ^ 2 * Dj j ∧ ∑ j, c j ^ 2 * Dj j ≤ hi ^ 2 * ∑ j, Dj j := by
  rw [Finset.mul_sum, Finset.mul_sum]
  constructor
  · apply Finset.sum_le_sum
    intro j _
    have h1 : lo ^ 2 ≤ c j ^ 2 := by nlinarith [hc j]
    exact mul_le_mul_of_nonneg_right h1 (hD j)
  · apply Finset.sum_le_sum
    intro j _
    have h2 : c j ^ 2 ≤ hi ^ 2 := by nlinarith [hc j]
    exact mul_le_mul_of_nonneg_right h2 (hD j)

theorem chi2_amp_expand_mut {n : ℕ} (W : Matrix (Fin n) (Fin n) ℝ) (hW : Wᵀ = W) (m P : Fin n → ℝ) (A : ℝ) :
    (A • m - P) ⬝ᵥ (W *ᵥ (A • m - P)) =
      A ^ 2 * (m ⬝ᵥ (W *ᵥ m)) + 2 * A * (m ⬝ᵥ (W *ᵥ P)) + P ⬝ᵥ (W *ᵥ P) := by
  have hs : P ⬝ᵥ (W *ᵥ m) = m ⬝ᵥ (W *ᵥ P) := by
    rw [dotProduct_mulVec, ← mulVec_transpose, hW, dotProduct_comm]
  simp only [mulVec_sub, mulVec_smul, sub_dotProduct, dotProduct_sub, smul_dotProduct, dotProduct_smul,
    smul_eq_mul]
  rw [hs]
  ring

theorem chi2_amp_min_mut (a b c A : ℝ) (ha : 0 < a) :
    c + b ^ 2 / a ≤ a * A ^ 2 - 2 * b * A + c ∧ a * (b / a) ^ 2 - 2 * b * (b / a) + c = c - b ^ 2 / a := by
  have ha' : a ≠ 0 := ha.ne'
  constructor
  · have h : a * A ^ 2 - 2 * b * A + c - (c - b ^ 2 / a) = (a * A - b) ^ 2 / a := by
      field_simp
      ring
    have h0 : 0 ≤ (a * A - b) ^ 2 / a := div_nonneg (sq_nonneg _) ha.le
    linarith
  · field_simp
    ring

theorem amp_fit_scale_invariant_mut (a b c l : ℝ) (ha : 0 < a) (hl : l ≠ 0) :
    (l * b) / (l ^ 2 * a) = (b / a) * l ∧ c - (l * b) ^ 2 / (l ^ 2 * a) = c - b ^ 2 / a := by
  have ha' : a ≠ 0 := ha.ne'
  constructor
  · field_simp
  · field_simp

theorem twin_tw1_mut (a b c : ℝ) :
    ((6 / 5) ^ 2 * a - 2 * (6 / 5) * b + c) - (a - 2 * b + c) = 9 / 25 * a - 2 / 5 * b ∧
    (6 / 5) ^ 2 * c - 2 * (6 / 5) * c + c = 1 / 25 * c := by
  constructor <;> ring

theorem holds_line_scale_mut (D SE l : ℝ) (hpos : 0 < D + 2 * SE) :
    l * D + 2 * (l * SE) < 4 ↔ 4 / (D + 2 * SE) < l := by
  rw [lt_div_iff₀ hpos]
  constructor <;> intro h <;> linarith

end ABS1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
