/-
TK1 MUTATE twin (criteria 98f2ab2b6e): one false version of each TK1.lean statement. Every one must fail to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
  M1 rhoK_form with (1 - theta M'/M) for (1 + theta M'/M)   (the MU1 code mutation: theta F_theta dropped, sign)
  M2 trace zero at F = 1/(6K)
  M3 lambda_eff = -1/3 at the degenerate point
  M4 Az numerator without the - F_QQ term
  M5 g4 > 0 when F_thth > 0
  M6 the outside reply's 10x slip: sqrt(M_sun a0/G) = 259,140 M_sun per kpc
  M7 M_f inside the group window
-/
import Mathlib.Tactic

namespace TK1M

theorem rhoK_form_bad (K M n th Mp : ℝ) (hK : K ≠ 0) (hM : M ≠ 0) :
    let q := 1 + K * n / M
    q * (M * (q - 1) / K) + th * Mp * (q - 1) ^ 2 / (2 * K) - M * (q - 1) ^ 2 / (2 * K)
      = n + K * n ^ 2 / (2 * M) * (1 - th * Mp / M) := by
  intro q
  simp only [q]
  field_simp
  ring

theorem trace_zero_bad (K F N a : ℝ) (hK : 0 < K) (hN : 0 < N) (ha : 0 < a) :
    (3 * K * F - 1) / (4 * K * N * a) = 0 ↔ F = 1 / (6 * K) := by
  have h4 : 4 * K * N * a ≠ 0 := by positivity
  rw [div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · field_simp; linarith
    · exact absurd h h4
  · intro h; left; rw [h]; field_simp; ring

theorem lam_bad (K F : ℝ) (hK : 0 < K) : F = 1 / (3 * K) ↔ -2 * K * F = -1 / 3 := by
  have hK' : K ≠ 0 := hK.ne'
  constructor
  · intro h; rw [h]; field_simp; ring
  · intro h; field_simp; linarith

theorem Az_numerator_bad (K FQQ Fthth : ℝ) (hK : K ≠ 0) :
    3 * K * FQQ * Fthth = 3 * K * FQQ * (Fthth - 1 / (3 * K)) := by
  field_simp
  ring

theorem g4_pos_bad (Fthth N0 a Den : ℝ) (hF : 0 < Fthth) (hN : 0 < N0) (ha : 0 < a) (hD : Den < 0) :
    0 < Fthth * N0 ^ 3 * a / (4 * Den) := by
  apply div_pos
  · positivity
  · linarith

theorem a4_constant_bad :
    (259140 : ℝ) ^ 2 < (93603 / 10 ^ 15) * (30856775814913673 * 10 ^ 3) ^ 2 / (132712440018 * 10 ^ 9) := by
  norm_num

theorem groups_inside_bad : (912 : ℝ) / 1000 ≤ 1 / 1000 := by
  norm_num

end TK1M
