/-
AKD1 MUTATE twin (criteria d88d310eb1): one FALSE version of each theorem in AKD1.lean, each given a proof attempt in
the same style. Every one must fail to compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib.Tactic

namespace AKD1_MUTATE

-- ghost_law with the threshold reversed (false at k2 = 0)
theorem ghost_law_false (M R k2 : ℝ) (hM : 0 < M) (hR : 1 < R) (hk : k2 < M / (R - 1)) :
    M + k2 * (1 - R) < 0 := by
  have hR1 : 0 < R - 1 := by linarith
  have := (lt_div_iff₀ hR1).mp hk
  nlinarith

-- healthy_law claimed for R > 1 (false at large k2)
theorem healthy_law_false (M R k2 : ℝ) (hM : 0 < M) (hR : 1 < R) (hk : 0 ≤ k2) :
    0 < M + k2 * (1 - R) := by
  nlinarith

-- ghost_P0 with R < 0 (false)
theorem ghost_P0_false (M R k2 : ℝ) (hM : 0 < M) (hR : R < 0) (hk : 0 < k2) :
    M - k2 * R < 0 := by
  nlinarith

-- mu1 claimed to be a ghost (false)
theorem mu1_ghost_false (M R c k2 : ℝ) (hM : 0 < M) (hR : R ≤ 0) (hc : 0 ≤ c) (hk : 0 ≤ k2) :
    M + k2 * (c - R) < 0 := by
  nlinarith

-- Az_sign with the sign flipped
theorem Az_sign_false (a N0 ad FQQ FY k : ℝ) (ha : 0 < a) (hN : 0 < N0) (hd : 0 < ad) :
    a ^ 3 * (FQQ * a ^ 2 + 2 * k ^ 2 * FY * N0 ^ 2) / (4 * N0 * ad ^ 2) < 0 ↔
      0 < FQQ * a ^ 2 + 2 * k ^ 2 * FY * N0 ^ 2 := by
  have hden : 0 < 4 * N0 * ad ^ 2 := by positivity
  rw [div_neg_iff]
  constructor <;> intro h <;> nlinarith

-- flat dispersion claimed stable
theorem flat_dispersion_false (KG m R k2 : ℝ) (hKG : 0 < KG) (hm : 0 < m) (hR : 1 < R) (hk : m / (R - 1) < k2) :
    0 < KG * ((1 - (1 - R)) * k2 - m) / (m + (1 - R) * k2) := by
  have hR1 : 0 < R - 1 := by linarith
  have hk' := (div_lt_iff₀ hR1).mp hk
  apply div_pos <;> nlinarith

-- transverse_ghost with the inequality on W reversed
theorem transverse_ghost_false (u q Mp : ℝ) (hu : 0 ≤ u) (hMp : Mp < 0) :
    1 / (1 + u) + Mp * q ^ 2 < 0 ↔ (-Mp) * q ^ 2 * (1 + u) < 1 := by
  have h1u : 0 < 1 + u := by linarith
  constructor
  · intro h
    have h' : 1 / (1 + u) < (-Mp) * q ^ 2 := by linarith
    rw [div_lt_iff₀ h1u] at h'
    linarith
  · intro h
    have h' : 1 / (1 + u) < (-Mp) * q ^ 2 := by
      rw [div_lt_iff₀ h1u]
      linarith
    linarith

-- g_c rule landing on the wrong value
theorem gc_rule_p2_false (mu0 muK Mf gmin s gc2 : ℝ) (hden : 0 < muK ^ 2 - Mf ^ 2) (hs : 1 < s)
    (hss : s ^ 2 = mu0 ^ 2 / (muK ^ 2 - Mf ^ 2)) (hg : gc2 = gmin ^ 2 / (s - 1)) (hgm : gmin ≠ 0) :
    mu0 ^ 2 / (1 + gmin ^ 2 / gc2) ^ 2 + Mf ^ 2 = muK ^ 2 + Mf ^ 2 := by
  have hs1 : s - 1 ≠ 0 := by linarith
  have h1 : 1 + gmin ^ 2 / gc2 = s := by
    rw [hg]
    field_simp
    ring
  have hmu : mu0 ^ 2 ≠ 0 := by
    intro h0
    rw [h0, zero_div] at hss
    nlinarith
  rw [h1, hss, div_div_eq_mul_div, mul_div_cancel_left₀ _ hmu]
  ring

-- rate_shape claiming the rate stays below the bound
theorem rate_shape_false (B k2 X : ℝ) (hB : 0 < B) (hk : 0 < k2) (hX : 0 < X) :
    let S := -(B * k2) / (2 * X)
    S < 0 ∧ B * k2 / (-S) < X := by
  intro S
  have hBk : 0 < B * k2 := mul_pos hB hk
  constructor
  · simp only [S]
    have : 0 < B * k2 / (2 * X) := div_pos hBk (by linarith)
    rw [neg_div]
    linarith
  · simp only [S]
    rw [neg_div, neg_neg, div_div_eq_mul_div, div_lt_iff₀ hBk]
    nlinarith

end AKD1_MUTATE
