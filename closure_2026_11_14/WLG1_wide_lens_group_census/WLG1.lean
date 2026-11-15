/-
WLG1 (covering the pair WLG1 and WLG1R): Lean statements for the algebra of the wide-lens group census: the group's
speed against the crossing speed v*(z), the reference layout's Einstein mass, and the known-answer and label rules.
They certify the algebra, not the physics, and no number or label of the lane. TEST lane; adopts nothing.

  crossing_speed_meets_law : with H = H0 E(z), v*(z) = v*(0)/E(z) and v*(0) = a0/(10 (1 + X) H0) give
                             v* = a0/(10 (1 + X) H); a speed with v^3 = 10 G (1 + X) M_b H equal to it has
                             v^4 = G M_b a0 (the crossing speed is where the virial speed meets the law).
  speed_ratio_cube_root    : s = (k M_b)^(1/3) scales as the exact cube root of the baryon mass, s(l M) = l^(1/3) s(M).
  speed_ratio_monotone     : s^3 = k M_b with k > 0: fewer baryons (no gas, M_b - M_gas with M_gas >= 0) never give a
                             higher speed ratio.
  virial_identity          : KA-7: at the 200 rho_crit radius, R^3 (100 H^2) = G M, (G M)^3 = (10 G M H)^2 R^3,
                             i.e. (G M / R)^3 = (10 G M H)^2, so sqrt(G M / R) = (10 G M H)^(1/3).
  nested_rule_bracket      : rule N-B builds the reference halo from M_b - M*_lens, never more cold mass than N-A's
                             X M_b, short of it by exactly X M*_lens.
  ka6_pooled_between       : KA-6 read pooled, (a + c)/(n + m), lies between the two class fractions a/n and c/m, so a
                             class can sit below the 0.90 line while the pooled fraction sits above it (an example is
                             given with numbers that are not the lane's).
  label_rule               : with lo <= hi, FAST (lo >= 1) and SLOW (hi < 1) never both apply; UNDER (lo > 0.10) and
                             OVER (hi < -0.10) never both apply; FITS (neither) is exactly overlap with [-0.10, 0.10];
                             TW-INJ's M_obs = M_ref gives r = log10(M_obs / M_ref) = 0.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace WLG1

theorem crossing_speed_meets_law (a0 X H0 Ez G Mb v : ℝ) (hX : 0 < 1 + X) (hH : 0 < H0) (hE : 0 < Ez)
    (hv : v = a0 / (10 * (1 + X) * H0) / Ez) (h3 : v ^ 3 = 10 * G * (1 + X) * Mb * (H0 * Ez)) :
    v = a0 / (10 * (1 + X) * (H0 * Ez)) ∧ v ^ 4 = G * Mb * a0 := by
  have hv' : v = a0 / (10 * (1 + X) * (H0 * Ez)) := by
    rw [hv]
    field_simp
  refine ⟨hv', ?_⟩
  have h4 : v ^ 4 = v * v ^ 3 := by ring
  rw [h4, h3, hv']
  field_simp

theorem speed_ratio_cube_root (k M l : ℝ) (hk : 0 ≤ k) (hM : 0 ≤ M) (hl : 0 ≤ l) :
    (k * (l * M)) ^ ((1 : ℝ) / 3) = l ^ ((1 : ℝ) / 3) * (k * M) ^ ((1 : ℝ) / 3) := by
  rw [show k * (l * M) = l * (k * M) by ring]
  exact Real.mul_rpow hl (mul_nonneg hk hM)

theorem speed_ratio_monotone (k M1 M2 s1 s2 : ℝ) (hk : 0 < k) (_hs1 : 0 ≤ s1) (hs2 : 0 ≤ s2)
    (h1 : s1 ^ 3 = k * M1) (h2 : s2 ^ 3 = k * M2) (hM : M1 ≤ M2) : s1 ≤ s2 := by
  by_contra hc
  have hlt : s2 < s1 := lt_of_not_ge hc
  have hc3 : s2 ^ 3 < s1 ^ 3 := by
    have := pow_lt_pow_left₀ hlt hs2 (by norm_num : (3 : ℕ) ≠ 0)
    exact this
  have : k * M1 ≤ k * M2 := mul_le_mul_of_nonneg_left hM hk.le
  linarith

theorem virial_identity (G M H R : ℝ) (hR : R ^ 3 * (100 * H ^ 2) = G * M) :
    (G * M) ^ 3 = (10 * G * M * H) ^ 2 * R ^ 3 := by
  linear_combination (-(G * M) ^ 2) * hR

theorem nested_rule_bracket (X Mb Ml : ℝ) (hX : 0 ≤ X) (hl : 0 ≤ Ml) :
    X * (Mb - Ml) ≤ X * Mb ∧ X * Mb - X * (Mb - Ml) = X * Ml := by
  constructor
  · nlinarith
  · ring

theorem ka6_pooled_between (a c n m : ℝ) (hn : 0 < n) (hm : 0 < m) (h : a / n ≤ c / m) :
    (a / n ≤ (a + c) / (n + m) ∧ (a + c) / (n + m) ≤ c / m) ∧
    ((89 : ℝ) / 100 < 0.90 ∧ (0.90 : ℝ) ≤ (89 + 99) / (100 + 100)) := by
  have hnm : 0 < n + m := by linarith
  rw [div_le_div_iff₀ hn hm] at h
  refine ⟨⟨?_, ?_⟩, ?_⟩
  · rw [div_le_div_iff₀ hn hnm]
    nlinarith
  · rw [div_le_div_iff₀ hnm hm]
    nlinarith
  · constructor <;> norm_num

theorem label_rule (lo hi Mo : ℝ) (hlh : lo ≤ hi) (hMo : 0 < Mo) :
    ¬ (1 ≤ lo ∧ hi < 1) ∧
    ¬ (0.10 < lo ∧ hi < -0.10) ∧
    ((¬ (0.10 < lo) ∧ ¬ (hi < -0.10)) ↔ (lo ≤ 0.10 ∧ -0.10 ≤ hi)) ∧
    Real.logb 10 (Mo / Mo) = 0 := by
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

end WLG1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
