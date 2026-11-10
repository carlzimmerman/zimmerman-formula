/-
AKD1 (criteria d88d310eb1): Lean statements for the closed forms. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Notation: M = M_2(0) Q0^2 > 0 (the dust's inertia, times K), R = -M_2'(0) q0^2 = p (mu_0 q0 / g_c)^2 (the candidate's
weight), c = the law's weight (1 unscreened, 0 with P held at 0), k2 = k_phys^2 >= 0.
K * (FQQ Q0^2 + 2 F_Y k^2) = M + k2 (c - R)  (K4's A_z up to a positive factor; KA4).

  ghost_law        : law on (c = 1), R > 1, k2 > M/(R - 1)  ->  M + k2 (1 - R) < 0   (A_z < 0: a ghost)
  healthy_law      : law on, R <= 1, M > 0, k2 >= 0       ->  M + k2 (1 - R) > 0
  ghost_P0         : law held at P = 0, R > 0, k2 > M/R    ->  M - k2 R < 0
  mu1_healthy      : sign of p flipped (R <= 0), c >= 0   ->  M + k2 (c - R) > 0
  Az_sign          : a, N0, adot > 0  ->  (A_z = a^3 (FQQ a^2 + 2 k^2 FY N0^2)/(4 N0 adot^2) < 0 iff FQQ a^2 + 2 k^2 FY N0^2 < 0)
  flat_dispersion  : SCS1's omega^2 = K G [(1 - Km) k2 - m] / (m + Km k2) with Km = 1 - R, R > 1, k2 > m/(R - 1), K G > 0
                     -> omega^2 < 0 (growth)
  transverse_ghost : in a static well, law's transverse weight 1/(1+u) plus the candidate's M_2' q^2 (M_2' < 0) is
                     negative iff W = |M_2'| q^2 (1+u) > 1
  gc_rule_p2       : p = 2, s = sqrt(mu0^2/(muK^2 - Mf^2)) > 1, g_c^2 = gmin^2/(s - 1)  ->  M_2(gmin^2) = muK^2
  rate_shape       : with B > 0 and S(k) < 0 the decoupling growth rate^2 B k2 / |S| exceeds any bound as S -> 0-:
                     for every bound X > 0 there is S in (-B k2 / X, 0) with B k2 / (-S) > X  (stated as the inequality)
-/
import Mathlib.Tactic

namespace AKD1

theorem ghost_law (M R k2 : ℝ) (hM : 0 < M) (hR : 1 < R) (hk : M / (R - 1) < k2) :
    M + k2 * (1 - R) < 0 := by
  have hR1 : 0 < R - 1 := by linarith
  have := (div_lt_iff₀ hR1).mp hk
  nlinarith

theorem healthy_law (M R k2 : ℝ) (hM : 0 < M) (hR : R ≤ 1) (hk : 0 ≤ k2) :
    0 < M + k2 * (1 - R) := by
  have : 0 ≤ k2 * (1 - R) := mul_nonneg hk (by linarith)
  linarith

theorem ghost_P0 (M R k2 : ℝ) (hM : 0 < M) (hR : 0 < R) (hk : M / R < k2) :
    M - k2 * R < 0 := by
  have := (div_lt_iff₀ hR).mp hk
  linarith

theorem mu1_healthy (M R c k2 : ℝ) (hM : 0 < M) (hR : R ≤ 0) (hc : 0 ≤ c) (hk : 0 ≤ k2) :
    0 < M + k2 * (c - R) := by
  have : 0 ≤ k2 * (c - R) := mul_nonneg hk (by linarith)
  linarith

theorem Az_sign (a N0 ad FQQ FY k : ℝ) (ha : 0 < a) (hN : 0 < N0) (hd : 0 < ad) :
    a ^ 3 * (FQQ * a ^ 2 + 2 * k ^ 2 * FY * N0 ^ 2) / (4 * N0 * ad ^ 2) < 0 ↔
      FQQ * a ^ 2 + 2 * k ^ 2 * FY * N0 ^ 2 < 0 := by
  have hden : 0 < 4 * N0 * ad ^ 2 := by positivity
  have ha3 : 0 < a ^ 3 := by positivity
  rw [div_neg_iff]
  constructor
  · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩)
    · linarith
    · by_contra hc
      push_neg at hc
      have : 0 ≤ a ^ 3 * (FQQ * a ^ 2 + 2 * k ^ 2 * FY * N0 ^ 2) := mul_nonneg ha3.le hc
      linarith
  · intro h
    right
    exact ⟨mul_neg_of_pos_of_neg ha3 h, hden⟩

theorem flat_dispersion (KG m R k2 : ℝ) (hKG : 0 < KG) (hm : 0 < m) (hR : 1 < R) (hk : m / (R - 1) < k2) :
    KG * ((1 - (1 - R)) * k2 - m) / (m + (1 - R) * k2) < 0 := by
  have hR1 : 0 < R - 1 := by linarith
  have hk' := (div_lt_iff₀ hR1).mp hk
  have hk0 : 0 < k2 := by
    have : 0 < m / (R - 1) := div_pos hm hR1
    linarith
  have hnum : 0 < KG * ((1 - (1 - R)) * k2 - m) := by
    apply mul_pos hKG
    nlinarith
  have hden : m + (1 - R) * k2 < 0 := by nlinarith
  exact div_neg_of_pos_of_neg hnum hden

theorem transverse_ghost (u q Mp : ℝ) (hu : 0 ≤ u) (hMp : Mp < 0) :
    1 / (1 + u) + Mp * q ^ 2 < 0 ↔ 1 < (-Mp) * q ^ 2 * (1 + u) := by
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

theorem gc_rule_p2 (mu0 muK Mf gmin s gc2 : ℝ) (hden : 0 < muK ^ 2 - Mf ^ 2) (hs : 1 < s)
    (hss : s ^ 2 = mu0 ^ 2 / (muK ^ 2 - Mf ^ 2)) (hg : gc2 = gmin ^ 2 / (s - 1)) (hgm : gmin ≠ 0) :
    mu0 ^ 2 / (1 + gmin ^ 2 / gc2) ^ 2 + Mf ^ 2 = muK ^ 2 := by
  have hs1 : s - 1 ≠ 0 := by linarith
  have hgm2 : gmin ^ 2 ≠ 0 := pow_ne_zero 2 hgm
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

theorem rate_shape (B k2 X : ℝ) (hB : 0 < B) (hk : 0 < k2) (hX : 0 < X) :
    let S := -(B * k2) / (2 * X)
    S < 0 ∧ X < B * k2 / (-S) := by
  intro S
  have hBk : 0 < B * k2 := mul_pos hB hk
  constructor
  · simp only [S]
    have : 0 < B * k2 / (2 * X) := div_pos hBk (by linarith)
    rw [neg_div]
    linarith
  · simp only [S]
    rw [neg_div, neg_neg]
    rw [div_div_eq_mul_div]
    rw [lt_div_iff₀ hBk]
    nlinarith

end AKD1

#print axioms AKD1.ghost_law
#print axioms AKD1.healthy_law
#print axioms AKD1.ghost_P0
#print axioms AKD1.mu1_healthy
#print axioms AKD1.Az_sign
#print axioms AKD1.flat_dispersion
#print axioms AKD1.transverse_ghost
#print axioms AKD1.gc_rule_p2
#print axioms AKD1.rate_shape
