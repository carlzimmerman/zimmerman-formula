/-
KO1 MUTATE twin: five false versions of statements in KO1.lean, each with the true statement's proof script. Every one must
fail to compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
  ratio_lt_one_iff_M    : the crossover put at 1 / (c (c + 1)) instead of 1 / (c (c - 1)).
  ratio_strictMono_M    : the exterior made to fall with y instead of rise.
  ratio_le_sqrt_M       : the bound c sqrt(y) replaced by c y.
  u_scale_ge_M          : the lower bound sqrt(k) replaced by k.
  shell_unsupported_M   : the deep-regime factor 2/3 replaced by 3/2 on one side only.
-/
import Mathlib

namespace KO1M

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)
noncomputable def u (y : ℝ) : ℝ := y / 2 + Real.sqrt (y ^ 2 / 4 + y)

theorem nu_gt_one (y : ℝ) (hy : 0 < y) : 1 < nu y := by
  unfold nu
  have h1 : (1 / 2 : ℝ) = Real.sqrt (1 / 4) := by
    rw [show (1 / 4 : ℝ) = (1 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have h2 : Real.sqrt (1 / 4) < Real.sqrt (1 / 4 + 1 / y) := by
    apply Real.sqrt_lt_sqrt (by norm_num)
    have : 0 < 1 / y := by positivity
    linarith
  linarith
theorem nu_pos (y : ℝ) (hy : 0 < y) : 0 < nu y := lt_trans one_pos (nu_gt_one y hy)
theorem nu_strictAnti (y₁ y₂ : ℝ) (h1 : 0 < y₁) (h12 : y₁ < y₂) : nu y₂ < nu y₁ := by
  unfold nu
  have h2 : 0 < y₂ := lt_trans h1 h12
  have hinv : 1 / y₂ < 1 / y₁ := one_div_lt_one_div_of_lt h1 h12
  have h0 : (0 : ℝ) ≤ 1 / 4 + 1 / y₂ := by positivity
  have hs : Real.sqrt (1 / 4 + 1 / y₂) < Real.sqrt (1 / 4 + 1 / y₁) :=
    Real.sqrt_lt_sqrt h0 (by linarith)
  linarith
theorem nu_mul_sqrt_ge_one (y : ℝ) (hy : 0 < y) : 1 ≤ nu y * Real.sqrt y := by
  unfold nu
  have hsy : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have h1 : Real.sqrt (1 / y) ≤ Real.sqrt (1 / 4 + 1 / y) := Real.sqrt_le_sqrt (by linarith)
  have h2 : Real.sqrt (1 / y) * Real.sqrt y = 1 := by
    rw [← Real.sqrt_mul (by positivity) y]
    have : 1 / y * y = 1 := by field_simp
    rw [this, Real.sqrt_one]
  have h3 : Real.sqrt (1 / y) * Real.sqrt y ≤ Real.sqrt (1 / 4 + 1 / y) * Real.sqrt y :=
    mul_le_mul_of_nonneg_right h1 hsy.le
  nlinarith

-- FALSE 1
theorem ratio_lt_one_iff_M (c y : ℝ) (hc : 1 < c) (hy : 0 < y) : c / nu y < 1 ↔ y < 1 / (c * (c + 1)) := by
  rw [div_lt_one (nu_pos y hy)]
  unfold nu
  have hK : 0 < c * (c + 1) := by positivity
  have hc2 : (0 : ℝ) ≤ c - 1 / 2 := by linarith
  have hstep : c < 1 / 2 + Real.sqrt (1 / 4 + 1 / y) ↔ (c - 1 / 2) ^ 2 < 1 / 4 + 1 / y := by
    rw [← Real.lt_sqrt hc2]
    constructor <;> intro h <;> linarith
  rw [hstep]
  constructor
  · intro h
    have h1 : c * (c + 1) < 1 / y := by nlinarith
    have h2 : c * (c + 1) * y < 1 := by
      have h3 := mul_lt_mul_of_pos_right h1 hy
      have h4 : 1 / y * y = 1 := by field_simp
      linarith
    rw [lt_div_iff₀ hK]
    linarith
  · intro h
    have h2 : y * (c * (c + 1)) < 1 := by
      rw [lt_div_iff₀ hK] at h
      exact h
    have h1 : c * (c + 1) < 1 / y := by
      rw [lt_div_iff₀ hy]
      linarith
    nlinarith

-- FALSE 2
theorem ratio_strictMono_M (c y₁ y₂ : ℝ) (hc : 0 < c) (h1 : 0 < y₁) (h12 : y₁ < y₂) : c / nu y₂ < c / nu y₁ := by
  have h2 : 0 < y₂ := lt_trans h1 h12
  exact div_lt_div_of_pos_left hc (nu_pos y₂ h2) (nu_strictAnti y₁ y₂ h1 h12)

-- FALSE 3
theorem ratio_le_sqrt_M (c y : ℝ) (hc : 0 ≤ c) (hy : 0 < y) : c / nu y ≤ c * y := by
  have hnu : 0 < nu y := nu_pos y hy
  rw [div_le_iff₀ hnu]
  have h := nu_mul_sqrt_ge_one y hy
  nlinarith [mul_le_mul_of_nonneg_left h hc]

-- FALSE 4
theorem u_scale_ge_M (k y : ℝ) (hk : 1 ≤ k) (hy : 0 < y) : k * u y ≤ u (k * y) := by
  unfold u
  have hk0 : 0 ≤ k := by linarith
  have hsk : Real.sqrt k ≤ k := by
    rw [Real.sqrt_le_left hk0]
    nlinarith
  have h1 : Real.sqrt (k * (y ^ 2 / 4 + y)) ≤ Real.sqrt ((k * y) ^ 2 / 4 + k * y) := by
    apply Real.sqrt_le_sqrt
    nlinarith [mul_nonneg (mul_nonneg hk0 (sub_nonneg.mpr hk)) (sq_nonneg y)]
  have h2 : Real.sqrt (k * (y ^ 2 / 4 + y)) = Real.sqrt k * Real.sqrt (y ^ 2 / 4 + y) := Real.sqrt_mul hk0 _
  rw [h2] at h1
  have h3 : Real.sqrt k * (y / 2) ≤ k * y / 2 := by nlinarith
  nlinarith

-- FALSE 5
theorem shell_unsupported_M (X y : ℝ) (hX : 0 < X) (hy : 0 < y) :
    3 / 2 * Real.sqrt y < y * (X * (1 + X / 2)) ↔ 2 / (3 * (X * (1 + X / 2))) < Real.sqrt y := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hK : 0 < X * (1 + X / 2) := by positivity
  have hsq : Real.sqrt y * Real.sqrt y = y := Real.mul_self_sqrt hy.le
  rw [div_lt_iff₀ (by positivity)]
  constructor
  · intro h
    have h1 : 3 / 2 * Real.sqrt y < Real.sqrt y * Real.sqrt y * (X * (1 + X / 2)) := by rw [hsq]; exact h
    have h2 : 3 / 2 < Real.sqrt y * (X * (1 + X / 2)) := by
      by_contra hc
      have hc' := not_lt.mp hc
      have := mul_le_mul_of_nonneg_left hc' hs.le
      nlinarith
    nlinarith
  · intro h
    have h2 : 3 / 2 < Real.sqrt y * (X * (1 + X / 2)) := by nlinarith
    have h3 := mul_lt_mul_of_pos_left h2 hs
    nlinarith

end KO1M
