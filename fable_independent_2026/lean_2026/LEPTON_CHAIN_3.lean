import Mathlib

/-!
# LEPTON_CHAIN_3: the symmetry behind TM1 (criteria LEPTON_CHAIN_3_CRITERIA.md, 3199be948)

Setting (ASSUMED, standard): S4 in the basis where its Z3 generator T is diagonal, so the charged leptons are diagonal.
The 3-dim generators, with factors of 3 cleared:
  S3m := 3S = [[-1,2,2],[2,-1,2],[2,2,-1]],   Um := U = swap(μ, τ),   G := 3·(S U) = [[-1,2,2],[2,2,-1],[2,-1,2]].
H stands for the Hermitian matrix that U_PMNS diagonalises: M†M (Majorana, νᵀMν) or MM† (Dirac, ν̄_L M ν_R, the atomos branch).
In Lean it is any complex 3×3 matrix. Sign convention: King–Luhn's rep 3 has U = −swap, so SU = −G/3. Then v1 is SU's +1
eigenvector rather than its −1; either way it is SU's NON-DEGENERATE eigenvector, and the commutant is the same. "Residual symmetry X" means H commutes with X.

CERTIFIED (zero sorry, standard axioms):
(S1) `G_sq`: G·G = 9·1, so SU is an involution (a Z2). `G_eq`: G = S3m·Um.
(S2) `G_v1`: G v1 = −3 v1 for v1 = (2, −1, −1). `G_trace`: tr G = 3. Given S1 (SU² = 1, so the eigenvalues are ±1), tr(SU) = 1
     means (1, 1, −1). That inference is informal; `G_neg_line` is what certifies the line.
     `G_neg_line`: every x with G x = −3 x is a multiple of v1. The −1 eigenspace of SU is exactly the line through v1.
(S3) `z2_forces_tm1_column`: H·G = G·H ⇒ ∃ c, H v1 = c v1. A residual Z2 = SU makes v1 a mass eigenvector.
(S4) `tm1_column_moduli`: (2/√6)² = 2/3 and (1/√6)² = 1/6. The normalised v1 has TM1's moduli² (2/3, 1/6, 1/6), which is
     exactly the TM1 hypothesis of LEPTON_CHAIN's L4 and LEPTON_CHAIN_2's L9/L10. The chain reads: residual Z2(SU) ⇒ TM1 ⇒ the
     octant decides δ's half-plane ⇒ cos²δ ≤ 0.21 and |J| ≥ 0.0277 (on the 3σ box). The chain links through the moduli; it is
     not one formal theorem across files.
(S5) `full_klein_forces_theta13_zero`: if H commutes with G and with Um (the full Klein group {1, S, U, SU}), then
     ∃ c', H w = c' w for w = (0, 1, −1). The commutation with Um alone already forces this (`U_neg_line`).
     `w_no_electron`: w's electron component is 0. Whichever PMNS column w is, it has U_ei = 0, while the data have no
     zero electron entry (s13² ≥ 0.020, quoted). The full
     residual Klein symmetry (tri-bimaximal) is excluded by θ13. TM1 is the Z2(SU) breaking of it.
(S6) `S_forces_tm2_column`: H commuting with S3m alone ⇒ H u ∝ u for u = (1, 1, 1), whose normalised moduli² are 1/3 each
     (`tm2_column_moduli`), i.e. TM2's |U_e2|² = 1/3. LEPTON_CHAIN L3 (`tm2_s12_floor`) gives s12² ≥ 1/3 from that, and FS14
     puts it 3–4σ off JUNO. `U_forces_w`: H commuting with Um alone ⇒ H w ∝ w, so θ13 = 0.
     Of the Klein group's three Z2s, only SU survives the data.
DEVIATIONS FROM THE FROZEN CRITERIA (disclosed): the criteria's `other_z2_tm2` became `S_forces_tm2_column` +
`tm2_column_moduli` + `U_forces_w`. Helpers were added (G_eq, G_neg_line, Um_w, U_neg_line, w_no_electron, S3m_u, S_pos_line),
plus `G_alone_allows_theta13`. All strengthen the result; none is weakened.
NOT CERTIFIED:
- that S4 and the T-diagonal basis are nature's choice;
- any dynamics (no flavon potential);
- a non-degenerate spectrum, which v1 needs in order to BE a PMNS column;
- which mass v1 belongs to (first column = the TM1 assignment);
- exactness.
The residual Z2 is a hypothesis, not derived from the framework.
-/

namespace LeptonChain3
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

theorem G_v1 : G *ᵥ v1 = (-3 : ℂ) • v1 := by
  ext i; fin_cases i <;> norm_num [G, v1, Matrix.mulVec, dotProduct, Fin.sum_univ_three, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail]

theorem G_neg_line (x : Fin 3 → ℂ) (hx : G *ᵥ x = (-3 : ℂ) • x) : x = (-(x 1)) • v1 := by
  have e0 := congrFun hx 0; have e1 := congrFun hx 1; have e2 := congrFun hx 2
  simp [G, Matrix.mulVec, dotProduct, Fin.sum_univ_three] at e0 e1 e2
  have a : x 2 = x 1 := by linear_combination (e2 - e1) / 6
  have b : x 0 = -2 * x 1 := by linear_combination e0 / 2 - (e2 - e1) / 6
  ext i; fin_cases i <;> (simp [v1, a, b]; try ring)

theorem z2_forces_tm1_column (H : Matrix (Fin 3) (Fin 3) ℂ) (h : H * G = G * H) : ∃ c : ℂ, H *ᵥ v1 = c • v1 := by
  refine ⟨-((H *ᵥ v1) 1), G_neg_line _ ?_⟩
  rw [Matrix.mulVec_mulVec, ← h, ← Matrix.mulVec_mulVec, G_v1, Matrix.mulVec_smul]

theorem tm1_column_moduli : (2 / Real.sqrt 6) ^ 2 = 2 / 3 ∧ (1 / Real.sqrt 6) ^ 2 = 1 / 6 := by
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

theorem U_forces_w (H : Matrix (Fin 3) (Fin 3) ℂ) (hU : H * Um = Um * H) : ∃ c : ℂ, H *ᵥ w = c • w := by
  refine ⟨(H *ᵥ w) 1, U_neg_line _ ?_⟩
  rw [Matrix.mulVec_mulVec, ← hU, ← Matrix.mulVec_mulVec, Um_w, Matrix.mulVec_smul]

theorem full_klein_forces_theta13_zero (H : Matrix (Fin 3) (Fin 3) ℂ) (_hG : H * G = G * H) (hU : H * Um = Um * H) :
    ∃ c : ℂ, H *ᵥ w = c • w := by
  refine ⟨(H *ᵥ w) 1, U_neg_line _ ?_⟩
  rw [Matrix.mulVec_mulVec, ← hU, ← Matrix.mulVec_mulVec, Um_w, Matrix.mulVec_smul]

theorem w_no_electron : w 0 = 0 := by simp [w]

/-- q = (1, 2, 0) lies in G's +3 eigenspace; H = q qᵀ commutes with G. -/
def Hq : Matrix (Fin 3) (Fin 3) ℂ := !![1, 2, 0; 2, 4, 0; 0, 0, 0]

theorem G_alone_allows_theta13 : Hq * G = G * Hq ∧ ¬ ∃ c : ℂ, Hq *ᵥ w = c • w := by
  refine ⟨?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> norm_num [Hq, G, Matrix.mul_apply, Fin.sum_univ_three, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail]
  · rintro ⟨c, hc⟩
    have := congrFun hc 0
    norm_num [Hq, w, Matrix.mulVec, dotProduct, Fin.sum_univ_three, Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail] at this

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

end LeptonChain3

#print axioms LeptonChain3.G_eq
#print axioms LeptonChain3.G_sq
#print axioms LeptonChain3.G_trace
#print axioms LeptonChain3.G_v1
#print axioms LeptonChain3.G_neg_line
#print axioms LeptonChain3.z2_forces_tm1_column
#print axioms LeptonChain3.tm1_column_moduli
#print axioms LeptonChain3.U_neg_line
#print axioms LeptonChain3.U_forces_w
#print axioms LeptonChain3.full_klein_forces_theta13_zero
#print axioms LeptonChain3.w_no_electron
#print axioms LeptonChain3.G_alone_allows_theta13
#print axioms LeptonChain3.S_pos_line
#print axioms LeptonChain3.S_forces_tm2_column
#print axioms LeptonChain3.tm2_column_moduli
