/-
AC21: algebraic core of the 3D-admissible smoothing of the v3s / AC2q stiffness switch.
Kappa = 1/2 FITTED; not theory closed. Lane: action_search_2026_11_05/AC21_smooth_3d.
Standard axioms only; MUTATE twin AC21_smooth_3d_MUTATE.lean.
-/
import Mathlib

namespace AC21

/-- H^s count: transverse data w0 ~ x^((m-1)/2) lies in H^s iff s < m/2; Kato needs s > d/2 + 1.
A window exists iff m > d + 2. -/
theorem window_iff (m d : ℕ) : ((d : ℚ) / 2 + 1 < (m : ℚ) / 2) ↔ d + 2 < m := by
  constructor
  · intro h
    have : ((d : ℚ) + 2) < m := by linarith
    exact_mod_cast this
  · intro h
    have : ((d : ℚ) + 2) < m := by exact_mod_cast h
    linarith

theorem max_form_fails_3d : ¬ (3 + 2 < 2) := by norm_num
theorem contact_m4_fails_3d : ¬ (3 + 2 < 4) := by norm_num
theorem contact_m4_ok_1d : 1 + 2 < 4 := by norm_num
theorem power6_ok_3d : 3 + 2 < 6 := by norm_num

/-- Pure power: with w = (2/(m-1)) k t and c = k t, c = ((m-1)/2) w (c linear in w, smooth). -/
theorem pure_power_c_linear (m k t : ℝ) (hm : 1 < m) :
    k * t = ((m - 1) / 2) * ((2 / (m - 1)) * k * t) := by
  have : m - 1 ≠ 0 := by linarith
  field_simp

/-- 1D principal block of the Makino-variable system is symmetric. -/
theorem principal_symmetric (v c : ℝ) : (!![v, c; c, v] : Matrix (Fin 2) (Fin 2) ℝ).transpose = !![v, c; c, v] := by
  ext i j; fin_cases i <;> fin_cases j <;> rfl

/-- PN weight in the layer: local quadratic stiffness beta s + C s^2/2 with beta = F' - s F'', C = F''. -/
theorem B_identity (γ s F1 F2 : ℝ) :
    (1 + γ * (F1 - s * F2) / 2) * s + (F2 * γ / 2) * s ^ 2 = s + γ * s * F1 / 2 := by ring

theorem B_ge_s (γ s F1 F2 : ℝ) (hγ : 0 ≤ γ) (hs : 0 ≤ s) (hF : 0 ≤ F1) :
    s ≤ (1 + γ * (F1 - s * F2) / 2) * s + (F2 * γ / 2) * s ^ 2 := by
  rw [B_identity]; have : 0 ≤ γ * s * F1 / 2 := by positivity
  linarith

theorem Aeff_nonneg (N γ C β s μ K : ℝ) (hN : 0 < N) (hγ : 0 < γ) (hC : 0 < C) (hK : 0 < K) :
    0 ≤ N * (2 + γ * (β + C * s)) ^ 2 / (2 * C * γ) + μ ^ 2 / (K * N) := by positivity

/-- AC2q FRW exactness: if F = (γ/2) Π^2 for Π ≥ b and 0 < b < 2X, the stiffness equals AC2q's on |D| < 2X - b. -/
theorem frw_exact (F : ℝ → ℝ) (γ b X D : ℝ) (hF : ∀ P, b ≤ P → F P = γ / 2 * P ^ 2)
    (hD : |D| < 2 * X - b) :
    F (D + 2 * X) - γ / 2 * (2 * X) ^ 2 = γ / 2 * ((D + 2 * X) ^ 2 - (2 * X) ^ 2) := by
  have h1 : b ≤ D + 2 * X := by
    have := neg_abs_le D; linarith
  rw [hF _ h1]; ring

/-- C^4 smoothstep in Bernstein form: S and 1 - S are nonnegative on [0, 1]. -/
def S (x : ℝ) : ℝ := x ^ 5 * (126 - 420 * x + 540 * x ^ 2 - 315 * x ^ 3 + 70 * x ^ 4)

theorem S_bernstein (x : ℝ) :
    S x = 126 * x ^ 5 * (1 - x) ^ 4 + 84 * x ^ 6 * (1 - x) ^ 3 + 36 * x ^ 7 * (1 - x) ^ 2
      + 9 * x ^ 8 * (1 - x) + x ^ 9 := by unfold S; ring

theorem one_sub_S_bernstein (x : ℝ) :
    1 - S x = (1 - x) ^ 9 + 9 * x * (1 - x) ^ 8 + 36 * x ^ 2 * (1 - x) ^ 7 + 84 * x ^ 3 * (1 - x) ^ 6
      + 126 * x ^ 4 * (1 - x) ^ 5 := by unfold S; ring

theorem S_nonneg (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) : 0 ≤ S x := by
  rw [S_bernstein]; have : 0 ≤ 1 - x := by linarith
  positivity

theorem one_sub_S_nonneg (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) : 0 ≤ 1 - S x := by
  rw [one_sub_S_bernstein]; have : 0 ≤ 1 - x := by linarith
  positivity

/-- Structural positivity of the iter_6 layer: A q^4 (1 - S z) + B x^5 (1-x)^5 + S y >= 0. -/
theorem layer_nonneg (A B q x y z : ℝ) (hA : 0 ≤ A) (hB : 0 ≤ B) (hx0 : 0 ≤ x) (hx1 : x ≤ 1)
    (hy0 : 0 ≤ y) (hy1 : y ≤ 1) (hz0 : 0 ≤ z) (hz1 : z ≤ 1) :
    0 ≤ A * q ^ 4 * (1 - S z) + B * x ^ 5 * (1 - x) ^ 5 + S y := by
  have h1 := one_sub_S_nonneg z hz0 hz1
  have h2 := S_nonneg y hy0 hy1
  have h3 : 0 ≤ 1 - x := by linarith
  have h4 : 0 ≤ A * q ^ 4 * (1 - S z) := by positivity
  have h5 : 0 ≤ B * x ^ 5 * (1 - x) ^ 5 := by positivity
  linarith

/-- The iter_6 winner (tau 1/2, x1 1/4, x0 4/5, n 5) solves its exact moment system (coefficients from sympy). -/
def Aw : ℚ := 734183424 / 8922115
def Bw : ℚ := 3165142806 / 44610575

theorem winner_moment1 : (266841 / 23429120 : ℚ) * Aw + (1 / 5544) * Bw + 1 / 20 = 1 := by
  unfold Aw Bw; norm_num
theorem winner_moment2 : (3385469 / 562298880 : ℚ) * Aw + (1 / 22176) * Bw + 3 / 2200 = 1 / 2 := by
  unfold Aw Bw; norm_num
theorem winner_A_pos : 0 < Aw := by unfold Aw; norm_num
theorem winner_B_pos : 0 < Bw := by unfold Bw; norm_num

end AC21

#print axioms AC21.window_iff
#print axioms AC21.pure_power_c_linear
#print axioms AC21.principal_symmetric
#print axioms AC21.B_ge_s
#print axioms AC21.Aeff_nonneg
#print axioms AC21.frw_exact
#print axioms AC21.S_nonneg
#print axioms AC21.one_sub_S_nonneg
#print axioms AC21.layer_nonneg
#print axioms AC21.winner_moment1
#print axioms AC21.winner_moment2
#print axioms AC21.winner_A_pos
#print axioms AC21.winner_B_pos
#print axioms AC21.max_form_fails_3d
#print axioms AC21.contact_m4_fails_3d
#print axioms AC21.power6_ok_3d
