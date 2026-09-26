import Mathlib

/-!
# XC2 — nonlinear well-posedness of C-H/K, scoped: algebraic and analytic certificates

SCOPE. Lean certifies the inequalities behind `real_research/extra_crispy_2026/XC2_wellposedness_scoping.py`. The
Hessian of the q-integrand (B1), the numerical demonstrations (B4, B5) and the zero-field quadratures (B7) are computed
in that lane.

* `mode_contraction`, `dirichlet_contraction`: the heat filter e^{bΔ} multiplies each Laplacian eigenmode's Dirichlet
  energy by e^{-2bλ} ≤ 1, so ‖D S f‖² ≤ ‖D f‖² on any closed leaf (XC2 B2).
* `second_variation_lower_bound`, `strict_convexity`: with s = ‖D S δ‖² ≤ d = ‖D δ‖² and the constitutive coefficient
  C ≥ C_min, the second variation 4d + 4Cs is at least 4(1 + min(0, C_min)) d, hence positive when C_min > −1: the
  MOND constraint is strictly convex, so it has exactly one solution (XC2 B3).
* `threshold_iff_increasing`: C_T = ν − 1 > −1 ⟺ ν > 0 and C_L = (yν)′ − 1 > −1 ⟺ (yν)′ > 0 — the threshold is exactly
  "g(g_N) strictly increasing", so every physical kernel qualifies.
* `mu_exp_CL_bound`: (x − 1) e^{−x} ≤ e^{−2} for every real x, so the QUMOND form of μ_exp has
  C_L = 1/(1 + (x−1)e^{−x}) − 1 ≥ 1/(1 + e^{−2}) − 1 ≈ −0.119 (XC2 B3's table).
* `khronon_cone`, `alpha_zero_symbol`: the decoupling-limit khronon symbol k²(α_c ω² − c₂k²) vanishes on the finite cone
  ω² = (c₂/α_c) k² for α_c > 0; at α_c = 0 it is −c₂k⁴ with no ω — the elliptic lapse of minimal Hořava gravity (XC2 B6).
* `osgood_diverges`: ∫₁^X u^{−1/2} du = 2(√X − 1) is unbounded — the log-Lipschitz modulus ε√ln(1/ε) of the planar
  zero-field case satisfies Osgood's uniqueness criterion (XC2 B7).
-/

theorem mode_contraction (l b : ℝ) (hl : 0 ≤ l) (hb : 0 ≤ b) : l * Real.exp (-2 * b * l) ≤ l := by
  have h : Real.exp (-2 * b * l) ≤ 1 := by
    rw [Real.exp_le_one_iff]; nlinarith
  calc l * Real.exp (-2 * b * l) ≤ l * 1 := mul_le_mul_of_nonneg_left h hl
    _ = l := by ring

theorem dirichlet_contraction {n : ℕ} (l g : Fin n → ℝ) (b : ℝ) (hl : ∀ j, 0 ≤ l j) (hb : 0 ≤ b) :
    ∑ j, l j * Real.exp (-2 * b * l j) * g j ^ 2 ≤ ∑ j, l j * g j ^ 2 := by
  apply Finset.sum_le_sum
  intro j _
  exact mul_le_mul_of_nonneg_right (mode_contraction (l j) b (hl j) hb) (sq_nonneg _)

theorem second_variation_lower_bound (d s C Cmin : ℝ) (hd : 0 ≤ d) (hs0 : 0 ≤ s) (hsd : s ≤ d)
    (hC : Cmin ≤ C) : 4 * (1 + min 0 Cmin) * d ≤ 4 * d + 4 * C * s := by
  by_cases hC0 : 0 ≤ C
  · have h1 : min 0 Cmin ≤ 0 := min_le_left _ _
    have h2 : 0 ≤ 4 * C * s := by positivity
    nlinarith
  · rw [not_le] at hC0
    have hCs : C * d ≤ C * s := by nlinarith
    have hmin : min 0 Cmin ≤ Cmin := min_le_right _ _
    have h3 : min 0 Cmin * d ≤ Cmin * d := mul_le_mul_of_nonneg_right hmin hd
    have h4 : Cmin * d ≤ C * d := mul_le_mul_of_nonneg_right hC hd
    nlinarith

theorem strict_convexity (d s C Cmin : ℝ) (hd : 0 < d) (hs0 : 0 ≤ s) (hsd : s ≤ d) (hC : Cmin ≤ C)
    (hthr : -1 < Cmin) : 0 < 4 * d + 4 * C * s := by
  have hlb := second_variation_lower_bound d s C Cmin hd.le hs0 hsd hC
  have hm : -1 < min 0 Cmin := lt_min (by norm_num) hthr
  have : 0 < 4 * (1 + min 0 Cmin) * d := by
    have : 0 < 1 + min 0 Cmin := by linarith
    positivity
  linarith

theorem threshold_iff_increasing (nu dynu : ℝ) :
    (-1 < nu - 1 ↔ 0 < nu) ∧ (-1 < dynu - 1 ↔ 0 < dynu) := by
  constructor <;> constructor <;> intro h <;> linarith

theorem mu_exp_CL_bound (x : ℝ) : (x - 1) * Real.exp (-x) ≤ Real.exp (-2) := by
  have h := Real.add_one_le_exp (x - 2)
  have hpos : 0 < Real.exp (-x) := Real.exp_pos _
  have he : Real.exp (x - 2) * Real.exp (-x) = Real.exp (-2) := by
    rw [← Real.exp_add]; ring_nf
  calc (x - 1) * Real.exp (-x) = ((x - 2) + 1) * Real.exp (-x) := by ring
    _ ≤ Real.exp (x - 2) * Real.exp (-x) := mul_le_mul_of_nonneg_right h hpos.le
    _ = Real.exp (-2) := he

theorem khronon_cone (α c2 ω k : ℝ) (hα : 0 < α) (hk : k ≠ 0) :
    k ^ 2 * (α * ω ^ 2 - c2 * k ^ 2) = 0 ↔ ω ^ 2 = c2 / α * k ^ 2 := by
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  have hα' : α ≠ 0 := ne_of_gt hα
  constructor
  · intro h
    have h1 : α * ω ^ 2 - c2 * k ^ 2 = 0 := by
      rcases mul_eq_zero.mp h with h0 | h0
      · exact absurd h0 hk2
      · exact h0
    field_simp
    linarith
  · intro h
    rw [h]
    field_simp
    ring

theorem alpha_zero_symbol (c2 ω k : ℝ) : k ^ 2 * (0 * ω ^ 2 - c2 * k ^ 2) = -c2 * k ^ 4 := by
  ring

theorem osgood_diverges (M : ℝ) : ∃ X : ℝ, 1 ≤ X ∧ M < 2 * (Real.sqrt X - 1) := by
  refine ⟨(|M| / 2 + 2) ^ 2, ?_, ?_⟩
  · have : 2 ≤ |M| / 2 + 2 := by have := abs_nonneg M; linarith
    nlinarith
  · have hnn : 0 ≤ |M| / 2 + 2 := by have := abs_nonneg M; linarith
    rw [Real.sqrt_sq hnn]
    have := le_abs_self M
    linarith

#print axioms mode_contraction
#print axioms dirichlet_contraction
#print axioms second_variation_lower_bound
#print axioms strict_convexity
#print axioms threshold_iff_increasing
#print axioms mu_exp_CL_bound
#print axioms khronon_cone
#print axioms alpha_zero_symbol
#print axioms osgood_diverges
