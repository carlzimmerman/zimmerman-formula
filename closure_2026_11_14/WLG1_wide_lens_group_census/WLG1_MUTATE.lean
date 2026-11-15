/-
WLG1 MUTATE twin: the statements of WLG1.lean with one sign, factor, power or direction changed. Every theorem is
false and must fail (expected: exit 1, an error in every theorem). TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace WLG1_MUTATE

theorem crossing_speed_meets_law_mut (a0 X H0 Ez G Mb v : ℝ) (hX : 0 < 1 + X) (hH : 0 < H0) (hE : 0 < Ez)
    (hv : v = a0 / (10 * (1 + X) * H0) / Ez) (h3 : v ^ 3 = 10 * G * (1 + X) * Mb * (H0 * Ez)) :
    v = a0 / (10 * (1 + X) * (H0 * Ez)) ∧ v ^ 4 = 2 * G * Mb * a0 := by
  have hv' : v = a0 / (10 * (1 + X) * (H0 * Ez)) := by
    rw [hv]
    field_simp
  refine ⟨hv', ?_⟩
  have h4 : v ^ 4 = v * v ^ 3 := by ring
  rw [h4, h3, hv']
  field_simp

theorem speed_ratio_cube_root_mut (k M l : ℝ) (hk : 0 ≤ k) (hM : 0 ≤ M) (hl : 0 ≤ l) :
    (k * (l * M)) ^ ((1 : ℝ) / 3) = l ^ ((1 : ℝ) / 2) * (k * M) ^ ((1 : ℝ) / 3) := by
  rw [show k * (l * M) = l * (k * M) by ring]
  exact Real.mul_rpow hl (mul_nonneg hk hM)

theorem speed_ratio_monotone_mut (k M1 M2 s1 s2 : ℝ) (hk : 0 < k) (_hs1 : 0 ≤ s1) (hs2 : 0 ≤ s2)
    (h1 : s1 ^ 3 = k * M1) (h2 : s2 ^ 3 = k * M2) (hM : M1 ≤ M2) : s2 ≤ s1 := by
  by_contra hc
  have hlt : s2 < s1 := lt_of_not_ge hc
  have hc3 : s2 ^ 3 < s1 ^ 3 := by
    have := pow_lt_pow_left₀ hlt hs2 (by norm_num : (3 : ℕ) ≠ 0)
    exact this
  have : k * M1 ≤ k * M2 := mul_le_mul_of_nonneg_left hM hk.le
  linarith

theorem virial_identity_mut (G M H R : ℝ) (hR : R ^ 3 * (100 * H ^ 2) = G * M) :
    (G * M) ^ 3 = (100 * G * M * H) ^ 2 * R ^ 3 := by
  linear_combination (-(G * M) ^ 2) * hR

theorem nested_rule_bracket_mut (X Mb Ml : ℝ) (hX : 0 ≤ X) (hl : 0 ≤ Ml) :
    X * (Mb - Ml) ≤ X * Mb ∧ X * Mb - X * (Mb - Ml) = -(X * Ml) := by
  constructor
  · nlinarith
  · ring

theorem ka6_pooled_between_mut (a c n m : ℝ) (hn : 0 < n) (hm : 0 < m) (h : a / n ≤ c / m) :
    ((a + c) / (n + m) ≤ a / n ∧ (a + c) / (n + m) ≤ c / m) ∧
    ((89 : ℝ) / 100 < 0.90 ∧ (0.90 : ℝ) ≤ (89 + 99) / (100 + 100)) := by
  have hnm : 0 < n + m := by linarith
  rw [div_le_div_iff₀ hn hm] at h
  refine ⟨⟨?_, ?_⟩, ?_⟩
  · rw [div_le_div_iff₀ hn hnm]
    nlinarith
  · rw [div_le_div_iff₀ hnm hm]
    nlinarith
  · constructor <;> norm_num

theorem label_rule_mut (lo hi Mo : ℝ) (hlh : lo ≤ hi) (hMo : 0 < Mo) :
    ¬ (1 ≤ lo ∧ hi < 1) ∧
    ¬ (0.10 < lo ∧ hi < -0.10) ∧
    ((¬ (0.10 < lo) ∧ ¬ (hi < -0.10)) ↔ (lo ≤ 0.10 ∧ -0.10 ≤ hi)) ∧
    Real.logb 10 (Mo / Mo) = 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rintro ⟨h1, h2⟩
    linarith
  · rintro ⟨h1, h2⟩
    linarith
  · constructor
    · rintro ⟨h1, h2⟩
      exact ⟨not_lt.mp h1, not_lt.mp h2⟩
    · rintro ⟨h1, h2⟩
      exact ⟨not_lt.mpr h1, not_lt.mpr h2⟩
  · rw [div_self hMo.ne', Real.logb_one]

end WLG1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
