import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! V3_PICTURE_2026_10_23 MUTATE twin: four false versions of the certified statements. Each must FAIL to compile.
  M1 the stiffened saddle (L★ > 0) has a k-independent rate (false: it is unbounded);
  M2 the growth kernel INCREASES with f₀ (false: it strictly decreases);
  M3 Q6's crossings obey a μ² law to 0.1 % (false: the law is linear);
  M4 α = 1 has an acceleration floor x > 1 (false: it is the a₀-line, x → 0 as b → 0). -/

open Real

namespace V3PictureMutate

noncomputable def omega2 (G ρ M L k : ℝ) : ℝ := 4 * π * G * ρ * (M - 1 + L ^ 2 * k ^ 2 / 2)

theorem M1_stiffened_saddle_bounded_MUTATE (G ρ M L k : ℝ) (hL : 0 < L) :
    -omega2 G ρ M L k = -(4 * π * G * ρ * (M - 1)) := by
  simp only [omega2]; ring

noncomputable def kernel (μ f0 k : ℝ) : ℝ := (μ ^ 2 - f0 * k ^ 2) / ((1 - f0) * k ^ 2 + μ ^ 2)

theorem M2_kernel_increases_with_f0_MUTATE (μ f0 f1 k : ℝ) (hμ : μ ≠ 0) (hk : k ≠ 0) (h01 : f0 < f1) (hf1 : f1 ≤ 1) :
    kernel μ f0 k < kernel μ f1 k := by
  unfold kernel
  have hμ2 : 0 < μ ^ 2 := by positivity
  have hk2 : 0 < k ^ 2 := by positivity
  have hD1 : 0 < (1 - f1) * k ^ 2 + μ ^ 2 := by nlinarith
  have hD0 : 0 < (1 - f0) * k ^ 2 + μ ^ 2 := by nlinarith
  rw [div_lt_div_iff₀ hD0 hD1]
  have key : (μ ^ 2 - f0 * k ^ 2) * ((1 - f1) * k ^ 2 + μ ^ 2) - (μ ^ 2 - f1 * k ^ 2) * ((1 - f0) * k ^ 2 + μ ^ 2)
      = (f1 - f0) * (k ^ 2) ^ 2 := by ring
  have : 0 < (f1 - f0) * (k ^ 2) ^ 2 := by
    have : 0 < f1 - f0 := by linarith
    positivity
  linarith

theorem M3_crossings_quadratic_MUTATE :
    |((1 + 1854.4 : ℝ) * (2542 / 14.8) ^ 2 - (1 + 318684)) / (1 + 318684)| < 1 / 1000 := by
  norm_num [abs_lt]

noncomputable def balance (α x : ℝ) : ℝ := (α - 1 + x / (1 + x)) * x

theorem M4_law_has_floor_MUTATE (x b : ℝ) (hx : 0 < x) (hb : 0 < b) (h : balance 1 x = b) : 1 < x := by
  have h1x : 0 < 1 + x := by linarith
  simp only [balance] at h
  nlinarith [h]

end V3PictureMutate
