/-
ABS1: Lean statements for the algebra of the absolute fit of the forest gate's reference model to the DESI P1D points,
and of the gate re-evaluated with d' = (r - 1) x P_ref,model in place of d = (r - 1) x P_data. They certify the
algebra, not the physics, and no number or label of the lane. TEST lane; adopts nothing.

  gate_scale_const      : the gate statistic D = d^T W d (W the inverse covariance) with d_i = (r_i - 1) P_i: putting
                          c P_i in place of P_i at every point multiplies D by exactly c^2 (TW4: 1.2 -> 1.44).
  gate_blockwise_bounds : with the gate read bin by bin (D = sum of per-bin blocks D_j >= 0, as for a block-diagonal
                          W) and one ratio c_j per bin with 0 <= lo <= c_j <= hi, D' = sum c_j^2 D_j lies between
                          lo^2 D and hi^2 D. (The lane's full covariance keeps cross-bin terms; this bound is for the
                          blockwise reading only.)
  chi2_amp_expand       : for a symmetric W, the chi-square of the model A m against the data P is
                          A^2 (m W m) - 2 A (m W P) + (P W P).
  chi2_amp_min          : for a = m W m > 0 the best amplitude is A = b / a (b = m W P) and the minimum chi-square is
                          c - b^2 / a (c = P W P); no amplitude does better.
  amp_fit_scale_invariant : scaling the model by l (nonzero) divides the best amplitude by l and leaves the minimum
                          chi-square unchanged (TW2).
  twin_tw1              : the model times 6/5 raises the no-nuisance chi-square by (11/25) m W m - (2/5) m W P; with the
                          data as model the chi-square is (1/25) P W P (TW1).
  holds_line_scale      : if D and SE both scale by l, the HOLDS line D' + 2 SE' < 4 is met exactly when
                          l < 4 / (D + 2 SE) (the scale factor the script reports).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

open Matrix

namespace ABS1

theorem gate_scale_const {n : ℕ} (W : Matrix (Fin n) (Fin n) ℝ) (r P : Fin n → ℝ) (c : ℝ) :
    (fun i => (r i - 1) * (c * P i)) ⬝ᵥ (W *ᵥ (fun i => (r i - 1) * (c * P i))) =
      c ^ 2 * ((fun i => (r i - 1) * P i) ⬝ᵥ (W *ᵥ (fun i => (r i - 1) * P i))) := by
  have h : (fun i => (r i - 1) * (c * P i)) = c • (fun i => (r i - 1) * P i) := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul]
    ring
  rw [h, mulVec_smul, dotProduct_smul, smul_dotProduct, smul_eq_mul, smul_eq_mul]
  ring

theorem gate_blockwise_bounds {J : ℕ} (c Dj : Fin J → ℝ) (lo hi : ℝ) (hlo : 0 ≤ lo)
    (hD : ∀ j, 0 ≤ Dj j) (hc : ∀ j, lo ≤ c j ∧ c j ≤ hi) :
    lo ^ 2 * ∑ j, Dj j ≤ ∑ j, c j ^ 2 * Dj j ∧ ∑ j, c j ^ 2 * Dj j ≤ hi ^ 2 * ∑ j, Dj j := by
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

theorem chi2_amp_expand {n : ℕ} (W : Matrix (Fin n) (Fin n) ℝ) (hW : Wᵀ = W) (m P : Fin n → ℝ) (A : ℝ) :
    (A • m - P) ⬝ᵥ (W *ᵥ (A • m - P)) =
      A ^ 2 * (m ⬝ᵥ (W *ᵥ m)) - 2 * A * (m ⬝ᵥ (W *ᵥ P)) + P ⬝ᵥ (W *ᵥ P) := by
  have hs : P ⬝ᵥ (W *ᵥ m) = m ⬝ᵥ (W *ᵥ P) := by
    rw [dotProduct_mulVec, ← mulVec_transpose, hW, dotProduct_comm]
  simp only [mulVec_sub, mulVec_smul, sub_dotProduct, dotProduct_sub, smul_dotProduct, dotProduct_smul,
    smul_eq_mul]
  rw [hs]
  ring

theorem chi2_amp_min (a b c A : ℝ) (ha : 0 < a) :
    c - b ^ 2 / a ≤ a * A ^ 2 - 2 * b * A + c ∧ a * (b / a) ^ 2 - 2 * b * (b / a) + c = c - b ^ 2 / a := by
  have ha' : a ≠ 0 := ha.ne'
  constructor
  · have h : a * A ^ 2 - 2 * b * A + c - (c - b ^ 2 / a) = (a * A - b) ^ 2 / a := by
      field_simp
      ring
    have h0 : 0 ≤ (a * A - b) ^ 2 / a := div_nonneg (sq_nonneg _) ha.le
    linarith
  · field_simp
    ring

theorem amp_fit_scale_invariant (a b c l : ℝ) (ha : 0 < a) (hl : l ≠ 0) :
    (l * b) / (l ^ 2 * a) = (b / a) / l ∧ c - (l * b) ^ 2 / (l ^ 2 * a) = c - b ^ 2 / a := by
  have ha' : a ≠ 0 := ha.ne'
  constructor
  · field_simp
  · field_simp

theorem twin_tw1 (a b c : ℝ) :
    ((6 / 5) ^ 2 * a - 2 * (6 / 5) * b + c) - (a - 2 * b + c) = 11 / 25 * a - 2 / 5 * b ∧
    (6 / 5) ^ 2 * c - 2 * (6 / 5) * c + c = 1 / 25 * c := by
  constructor <;> ring

theorem holds_line_scale (D SE l : ℝ) (hpos : 0 < D + 2 * SE) :
    l * D + 2 * (l * SE) < 4 ↔ l < 4 / (D + 2 * SE) := by
  rw [lt_div_iff₀ hpos]
  constructor <;> intro h <;> linarith

end ABS1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
