import Mathlib

/-! MUTATE for LEPTON_CHAIN_3: three FALSE statements. Each must FAIL.
(M7) G v1 = +3 v1. FALSE: G v1 = (-6, 3, 3) = -3 v1.
(M8) commuting with G alone forces H w ∝ w for w = (0, 1, -1). FALSE: H = q qᵀ with q = (1, 2, 0) commutes with G
     and H w = (2, 4, 0) (certified as `G_alone_allows_theta13` in the main file).
(M9) v1/√6 has moduli² (1/3, 1/3). FALSE: they are (2/3, 1/6). -/

namespace LeptonChain3Mutate
open Matrix


def G : Matrix (Fin 3) (Fin 3) ℂ := !![-1, 2, 2; 2, 2, -1; 2, -1, 2]
def S3m : Matrix (Fin 3) (Fin 3) ℂ := !![-1, 2, 2; 2, -1, 2; 2, 2, -1]
def Um : Matrix (Fin 3) (Fin 3) ℂ := !![1, 0, 0; 0, 0, 1; 0, 1, 0]
def v1 : Fin 3 → ℂ := ![2, -1, -1]
def w : Fin 3 → ℂ := ![0, 1, -1]
def u : Fin 3 → ℂ := ![1, 1, 1]

theorem G_eq : G = S3m * Um := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [G, S3m, Um, Matrix.mul_apply, Fin.sum_univ_three]

theorem G_sq : G * G = (9 : ℂ) • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [G, Matrix.mul_apply, Fin.sum_univ_three, Matrix.one_apply, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail]

theorem G_trace : Matrix.trace G = 3 := by
  simp [Matrix.trace, G, Fin.sum_univ_three]; norm_num

theorem G_v1 : G *ᵥ v1 = (3 : ℂ) • v1 := by
  ext i; fin_cases i <;> norm_num [G, v1, Matrix.mulVec, dotProduct, Fin.sum_univ_three, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail]

theorem G_neg_line (x : Fin 3 → ℂ) (hx : G *ᵥ x = (-3 : ℂ) • x) : x = (-(x 1)) • v1 := by
  have e0 := congrFun hx 0; have e1 := congrFun hx 1; have e2 := congrFun hx 2
  simp [G, Matrix.mulVec, dotProduct, Fin.sum_univ_three] at e0 e1 e2
  have a : x 2 = x 1 := by linear_combination (e2 - e1) / 6
  have b : x 0 = -2 * x 1 := by linear_combination e0 / 2 - (e2 - e1) / 6
  ext i; fin_cases i <;> simp [v1, a, b] <;> ring

theorem z2_forces_tm1_column (H : Matrix (Fin 3) (Fin 3) ℂ) (h : H * G = G * H) : ∃ c : ℂ, H *ᵥ v1 = c • v1 := by
  refine ⟨-((H *ᵥ v1) 1), G_neg_line _ ?_⟩
  rw [Matrix.mulVec_mulVec, ← h, ← Matrix.mulVec_mulVec, G_v1, Matrix.mulVec_smul]

theorem tm1_column_moduli : (2 / Real.sqrt 6) ^ 2 = 1 / 3 ∧ (1 / Real.sqrt 6) ^ 2 = 1 / 3 := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ 6 by norm_num)
  constructor <;> rw [div_pow, h] <;> norm_num

theorem Um_w : Um *ᵥ w = (-1 : ℂ) • w := by
  ext i; fin_cases i <;> norm_num [Um, w, Matrix.mulVec, dotProduct, Fin.sum_univ_three, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail]

theorem U_neg_line (x : Fin 3 → ℂ) (hx : Um *ᵥ x = (-1 : ℂ) • x) : x = (x 1) • w := by
  have e0 := congrFun hx 0; have e1 := congrFun hx 1; have e2 := congrFun hx 2
  simp [Um, Matrix.mulVec, dotProduct, Fin.sum_univ_three] at e0 e1 e2
  have a : x 0 = 0 := by linear_combination e0 / 2
  have b : x 2 = -x 1 := by linear_combination e1
  ext i; fin_cases i <;> simp [w, a, b]

theorem full_klein_forces_theta13_zero (H : Matrix (Fin 3) (Fin 3) ℂ) (hG : H * G = G * H) :
    ∃ c : ℂ, H *ᵥ w = c • w := by
  refine ⟨(H *ᵥ w) 1, U_neg_line _ ?_⟩
  rw [Matrix.mulVec_mulVec, ← hG, ← Matrix.mulVec_mulVec, Um_w, Matrix.mulVec_smul]

theorem w_no_electron : w 0 = 0 := by simp [w]

theorem S3m_u : S3m *ᵥ u = (3 : ℂ) • u := by
  ext i; fin_cases i <;> norm_num [S3m, u, Matrix.mulVec, dotProduct, Fin.sum_univ_three, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail]

theorem S_pos_line (x : Fin 3 → ℂ) (hx : S3m *ᵥ x = (3 : ℂ) • x) : x = (x 0) • u := by
  have e0 := congrFun hx 0; have e1 := congrFun hx 1; have e2 := congrFun hx 2
  simp [S3m, Matrix.mulVec, dotProduct, Fin.sum_univ_three] at e0 e1 e2
  have a : x 1 = x 0 := by linear_combination (e0 - e1) / 6
  have b : x 2 = x 0 := by linear_combination (e0 - e2) / 6
  ext i; fin_cases i <;> simp [u, a, b]

theorem S_forces_tm2_column (H : Matrix (Fin 3) (Fin 3) ℂ) (h : H * S3m = S3m * H) : ∃ c : ℂ, H *ᵥ u = c • u := by
  refine ⟨(H *ᵥ u) 0, S_pos_line _ ?_⟩
  rw [Matrix.mulVec_mulVec, ← h, ← Matrix.mulVec_mulVec, S3m_u, Matrix.mulVec_smul]

theorem tm2_column_moduli : (1 / Real.sqrt 3) ^ 2 = 1 / 3 := by
  rw [div_pow, Real.sq_sqrt (by norm_num)]; norm_num

end LeptonChain3Mutate
