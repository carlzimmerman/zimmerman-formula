/-
WV1 MUTATE twin: false versions of WV1.lean's statements. Every theorem here must FAIL to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib.Tactic

namespace WV1M

-- false: an uncharged frame has a nonzero frequency
theorem dispersion_zero_charge_false (k a b : ℝ) : (0 : ℝ) * k ^ 2 * (b - a) / (a * b) = 1 := by
  ring

-- false: the off branch is stable
theorem v1_offbranch_positive (J t : ℝ) (hJ : 0 < J) (ht : 0 ≤ t) :
    0 < J * t / (1 + 1 * t) - J := by
  have hd : 0 < 1 + 1 * t := by linarith
  positivity

-- false: the off branch is C5's dispersion
theorem v1_screen1_is_C5 (J t : ℝ) : J * t / (1 + 1 * t) - J = J * t - J := by
  simp

-- false: growth faster than the Jeans rate is allowed
theorem v1_rate_exceeds (J t c : ℝ) (hJ : 0 < J) (ht : 0 ≤ t) (hc0 : 0 ≤ c) (hc1 : c ≤ 1) :
    J < -(J * t / (1 + c * t) - J) := by
  nlinarith

-- false: the density stays non-negative
theorem density_nonneg (m n C D : ℝ) (hm : 0 < m) (hC : C = m * n + D) (hD : D > C) : 0 ≤ n := by
  nlinarith

-- false: an advected zero becomes one
theorem advected_one (Y : ℕ → ℝ) (h : ∀ k, Y (k + 1) = Y k) (h0 : Y 0 = 0) : Y 5 = 1 := by
  simp [h, h0]

-- false: the window is not empty
theorem window_nonempty : ∃ nu : ℝ, (30 : ℝ) ≤ nu ∧ nu ≤ 25 := by
  exact ⟨27, by norm_num, by norm_num⟩

-- false: wrong sign in the law's algebra
theorem mu_identity_false (g a0 : ℝ) (ha : 0 < a0) (hg : 0 ≤ g) :
    g + a0 * g / (a0 + g) = ((g / a0) / (1 + g / a0)) * g := by
  field_simp
  ring

end WV1M
