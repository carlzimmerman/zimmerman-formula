/- QX6 MUTATE twin: three false claims that must fail. kappa = 1/2 FITTED; not theory closed. -/
import Mathlib

namespace QX6M

/-- FALSE: N^-2 <= 1 + 1.9 d (the true coefficient is about 2 + 3d). -/
theorem lapse_bound_false {d : ℝ} (h0 : 0 ≤ d) (h1 : d ≤ 1 / 100) :
    1 / (1 - d) ^ 2 ≤ 1 + 19 / 10 * d := by
  have hpos : 0 < (1 - d) ^ 2 := by
    have : 0 < 1 - d := by linarith
    positivity
  rw [div_le_iff₀ hpos]
  nlinarith [mul_nonneg h0 h0, mul_nonneg (mul_nonneg h0 h0) h0]

/-- FALSE: a mu_K meeting both the galaxy bound and the CMB need exists. -/
theorem route1_window_false : ∃ mu : ℝ, mu ≤ 1 / 10 ∧ 39800 ≤ mu := by
  exact ⟨1 / 10, le_refl _, by norm_num⟩

/-- FALSE: sqrt(G1) lies below the galaxy keys. -/
theorem route3_below_false : Real.sqrt (697 / 1000000000000) < (4615 / 1000000000 : ℝ) := by
  rw [Real.sqrt_lt' (by norm_num)]; norm_num

end QX6M

#print axioms QX6M.lapse_bound_false
#print axioms QX6M.route1_window_false
#print axioms QX6M.route3_below_false
