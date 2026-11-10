/-
TK1 (criteria 98f2ab2b6e): Lean statements for the closed forms. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  rhoK_form        : the clock's energy density at fixed charge n = M (q - 1)/K, q = 1 + K n / M:
                     q F_Q + theta F_theta - F = n + K n^2/(2M) (1 + theta M'/M), F = M (q-1)^2/(2K).
  rhoK_const       : with M' = 0 it is MK1's n + K n^2/(2M).
  trace_zero_iff   : the trace eigenvalue (3 K F - 1)/(4 K N a) of the velocity Hessian vanishes iff F = 1/(3K).
  lam_iff          : F = 1/(3K) iff lambda_eff = -2 K F = -2/3.
  Az_numerator     : 3 K F_QQ F_thth - F_QQ = 3 K F_QQ (F_thth - 1/(3K))  (K4's numerator at F_Qth = 0).
  g4_neg           : F_thth > 0, Den < 0, N0 > 0, a > 0  ->  g4 = F_thth N0^3 a / (4 Den) < 0.
  g4_over_Az_neg   : and with A_z > 0, g4 / A_z < 0 (the k^4 term destabilises).
  a4_constant      : 25914^2 < a0 kpc^2 / (G M_sun) < 25915^2 (canonical a0, IAU GM_sun, kpc in m):
                     sqrt(M_sun a0 / G) = 25,914 M_sun per kpc.
  groups_outside   : M_f = 1e-3 per Mpc lies below MK1's group window (0.912 canonical, 0.759 alt).
-/
import Mathlib.Tactic

namespace TK1

theorem rhoK_form (K M n th Mp : ℝ) (hK : K ≠ 0) (hM : M ≠ 0) :
    let q := 1 + K * n / M
    q * (M * (q - 1) / K) + th * Mp * (q - 1) ^ 2 / (2 * K) - M * (q - 1) ^ 2 / (2 * K)
      = n + K * n ^ 2 / (2 * M) * (1 + th * Mp / M) := by
  intro q
  simp only [q]
  field_simp
  ring

theorem rhoK_const (K M n th : ℝ) (hK : K ≠ 0) (hM : M ≠ 0) :
    let q := 1 + K * n / M
    q * (M * (q - 1) / K) + th * 0 * (q - 1) ^ 2 / (2 * K) - M * (q - 1) ^ 2 / (2 * K)
      = n + K * n ^ 2 / (2 * M) := by
  intro q
  simp only [q]
  field_simp
  ring

theorem trace_zero_iff (K F N a : ℝ) (hK : 0 < K) (hN : 0 < N) (ha : 0 < a) :
    (3 * K * F - 1) / (4 * K * N * a) = 0 ↔ F = 1 / (3 * K) := by
  have h4 : 4 * K * N * a ≠ 0 := by positivity
  rw [div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · field_simp; linarith
    · exact absurd h h4
  · intro h; left; rw [h]; field_simp; ring

theorem lam_iff (K F : ℝ) (hK : 0 < K) : F = 1 / (3 * K) ↔ -2 * K * F = -2 / 3 := by
  have hK' : K ≠ 0 := hK.ne'
  constructor
  · intro h; rw [h]; field_simp
  · intro h
    have : F = (-2 * K * F) / (-2 * K) := by field_simp
    rw [this, h]; field_simp

theorem Az_numerator (K FQQ Fthth : ℝ) (hK : K ≠ 0) :
    3 * K * FQQ * Fthth - FQQ = 3 * K * FQQ * (Fthth - 1 / (3 * K)) := by
  field_simp

theorem g4_neg (Fthth N0 a Den : ℝ) (hF : 0 < Fthth) (hN : 0 < N0) (ha : 0 < a) (hD : Den < 0) :
    Fthth * N0 ^ 3 * a / (4 * Den) < 0 := by
  apply div_neg_of_pos_of_neg
  · positivity
  · linarith

theorem g4_over_Az_neg (g4 Az : ℝ) (hg : g4 < 0) (hA : 0 < Az) : g4 / Az < 0 :=
  div_neg_of_neg_of_pos hg hA

-- a0 = 9.3603e-11 m/s^2, kpc = 3.0856775814913673e19 m, GM_sun = 1.32712440018e20 m^3/s^2
theorem a4_constant :
    (25914 : ℝ) ^ 2 < (93603 / 10 ^ 15) * (30856775814913673 * 10 ^ 3) ^ 2 / (132712440018 * 10 ^ 9) ∧
    (93603 / 10 ^ 15) * (30856775814913673 * 10 ^ 3) ^ 2 / (132712440018 * 10 ^ 9) < (25915 : ℝ) ^ 2 := by
  constructor <;> norm_num

theorem groups_outside : (1 : ℝ) / 1000 < 912 / 1000 ∧ (1 : ℝ) / 1000 < 759 / 1000 := by
  constructor <;> norm_num

end TK1

#print axioms TK1.rhoK_form
#print axioms TK1.trace_zero_iff
#print axioms TK1.lam_iff
#print axioms TK1.Az_numerator
#print axioms TK1.g4_neg
#print axioms TK1.a4_constant
