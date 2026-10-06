import Mathlib

/-!
# CFG351 -- certificates for the cold three-axis (full-rank sigma_c) switch

sigma_c = sum_s w_s (v_s - vbar)(v_s - vbar)^T (fine-grained stream sum); smooth flow: sigma = G sigma0 G^T.

* T1 single stream: G 0 G^T = 0 (sigma_c = 0 stays 0; FRW and linear parcels stay OFF).
* T2 sheet (rank 1) and T3 filament (two directions): det = 0 for a sum of two outer products in 3D.
* T4 three streams: the differences p, q, p + q give det = 0 (N streams give rank <= N - 1; rank 3 needs >= 4 streams).
* T5 isotropic eps I: det = eps^3 > 0; T5f the smooth route equals 1 there.
* T6 congruence: det (G S G^T) = det G ^ 2 det S, so det = 0 stays 0 and det > 0 stays > 0 (rank invariance).
* T7 FRW-off identity: H(det 0) = 0 for R-3; the MUTATE reader H(tr) is ON on a sheet.
* T8 switch stress: sigma adj(sigma) = det(sigma) I, so det = 0 gives sigma adj sigma = 0 and adj sigma kills range sigma.
* T9 conservation: periodic telescoping sum of flux differences is 0.
* T10 positivity: 0 <= 27 a b c <= (a + b + c)^3 for a, b, c >= 0 (smooth route in [0, 1] on diagonal PSD states).
* T11 ZA: an axis that has crossed (lambda D >= 1) has passed turnaround (lambda D = 1/2): third-axis crossing
  implies turnaround along all axes.
-/

open Matrix

noncomputable def Hs (x : ℝ) : ℝ := if 0 < x then 1 else 0

theorem T1_single_stream (Gm : Matrix (Fin 3) (Fin 3) ℝ) : Gm * (0 : Matrix (Fin 3) (Fin 3) ℝ) * Gmᵀ = 0 := by
  simp

theorem T3_two_axes (a b : ℝ) (u w : Fin 3 → ℝ) :
    (a • vecMulVec u u + b • vecMulVec w w).det = 0 := by
  rw [det_fin_three]; simp [vecMulVec_apply]; ring

theorem T2_sheet (a : ℝ) (u : Fin 3 → ℝ) : (a • vecMulVec u u).det = 0 := by
  have h := T3_two_axes a 0 u u
  simpa using h

theorem T4_three_streams (a b c : ℝ) (p q : Fin 3 → ℝ) :
    (a • vecMulVec p p + b • vecMulVec q q + c • vecMulVec (p + q) (p + q)).det = 0 := by
  rw [det_fin_three]; simp [vecMulVec_apply]; ring

theorem T5_isotropic (ε : ℝ) (h : 0 < ε) : 0 < (ε • (1 : Matrix (Fin 3) (Fin 3) ℝ)).det := by
  rw [det_smul, det_one]; simp; positivity

theorem T5f_isotropic_smooth (ε : ℝ) (h : 0 < ε) : 27 * ε ^ 3 / (3 * ε) ^ 3 = 1 := by
  field_simp; ring

theorem T6_congruence (Gm S : Matrix (Fin 3) (Fin 3) ℝ) :
    (Gm * S * Gmᵀ).det = Gm.det ^ 2 * S.det := by
  rw [det_mul, det_mul, det_transpose]; ring

theorem T6a_rank_deficient_stays (Gm S : Matrix (Fin 3) (Fin 3) ℝ) (hS : S.det = 0) :
    (Gm * S * Gmᵀ).det = 0 := by
  rw [T6_congruence, hS, mul_zero]

theorem T6b_full_rank_stays (Gm S : Matrix (Fin 3) (Fin 3) ℝ) (hG : Gm.det ≠ 0) (hS : 0 < S.det) :
    0 < (Gm * S * Gmᵀ).det := by
  rw [T6_congruence]; exact mul_pos (by positivity) hS

theorem T7_frw_off : Hs ((0 : Matrix (Fin 3) (Fin 3) ℝ).det) = 0 := by
  simp [Hs]

theorem T7m_mutate_on_sheet (a : ℝ) (ha : 0 < a) :
    Hs (trace (a • vecMulVec (![1, 0, 0] : Fin 3 → ℝ) ![1, 0, 0])) = 1 := by
  simp [Hs, trace, Fin.sum_univ_three, ha]

theorem T8_stress (S : Matrix (Fin 3) (Fin 3) ℝ) : S * adjugate S = S.det • (1 : Matrix (Fin 3) (Fin 3) ℝ) :=
  mul_adjugate S

theorem T8a_stress_zero (S : Matrix (Fin 3) (Fin 3) ℝ) (h : S.det = 0) : S * adjugate S = 0 := by
  rw [mul_adjugate, h, zero_smul]

theorem T8b_no_force (S : Matrix (Fin 3) (Fin 3) ℝ) (h : S.det = 0) (w : Fin 3 → ℝ) :
    (adjugate S).mulVec (S.mulVec w) = 0 := by
  rw [mulVec_mulVec, adjugate_mul, h, zero_smul, zero_mulVec]

theorem T9_conservative (n : ℕ) [NeZero n] (F : Fin n → ℝ) :
    ∑ i, (F (i + 1) - F i) = 0 := by
  rw [Finset.sum_sub_distrib, sub_eq_zero]
  exact Fintype.sum_equiv (Equiv.addRight 1) _ _ (fun _ => rfl)

theorem T10_positivity (a b c : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) :
    0 ≤ 27 * (a * b * c) ∧ 27 * (a * b * c) ≤ (a + b + c) ^ 3 := by
  refine ⟨by positivity, ?_⟩
  nlinarith [mul_nonneg ha hb, mul_nonneg hb hc, mul_nonneg ha hc, mul_nonneg (mul_nonneg ha hb) hc,
    sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (a - c),
    mul_nonneg ha (sq_nonneg (b - c)), mul_nonneg hb (sq_nonneg (a - c)), mul_nonneg hc (sq_nonneg (a - b)),
    mul_nonneg (add_nonneg ha hb) (sq_nonneg (a - b)), mul_nonneg (add_nonneg hb hc) (sq_nonneg (b - c)),
    mul_nonneg (add_nonneg ha hc) (sq_nonneg (a - c))]

theorem T11_crossing_after_turnaround (lam D : ℝ) (h : 1 ≤ lam * D) :
    1 - 2 * (lam * D) < 0 ∧ (1 : ℝ) / 2 < lam * D := by
  constructor <;> linarith

#print axioms T1_single_stream
#print axioms T2_sheet
#print axioms T3_two_axes
#print axioms T4_three_streams
#print axioms T5_isotropic
#print axioms T5f_isotropic_smooth
#print axioms T6_congruence
#print axioms T6a_rank_deficient_stays
#print axioms T6b_full_rank_stays
#print axioms T7_frw_off
#print axioms T7m_mutate_on_sheet
#print axioms T8_stress
#print axioms T8a_stress_zero
#print axioms T8b_no_force
#print axioms T9_conservative
#print axioms T10_positivity
#print axioms T11_crossing_after_turnaround
