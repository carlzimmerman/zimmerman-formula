import Mathlib

/-!
# XC5 — the MOND constraint with a non-constant lapse: certificates

SCOPE. Lean certifies the inequalities behind `real_research/extra_crispy_2026/XC5_lapse_weighted_convexity.py`. The
counterexample to lapse-weighted contraction (E1), the random checks (E2), the kernels' numbers (E3, E4) and the
numerical minimisations (E5, E6) are computed in that lane.

* `contrast_bound`: if each weight lies in [Nmin, Nmax] (0 < Nmin ≤ Nmax) and a map does not raise the UNWEIGHTED energy
  (∑ a ≤ ∑ b, entries ≥ 0), then ∑ N a ≤ (Nmax/Nmin) ∑ N b — the lapse-contrast bound (XC5 E2).
* `convex_for_monotone_kernel`: with constitutive coefficients C_T, C_L ≥ 0 the pointwise second variation
  4N|Dδ|² + N(4 C_T s⊥ + 4 C_L s∥) is at least 4N|Dδ|² for any N ≥ 0 — no contrast condition (XC5 E3).
* `mu_exp_CL_floor`: if u ≤ e^{−2} and 1 + u > 0 then 1/(1+u) − 1 ≥ −1/(e² + 1): the QUMOND form of μ_exp has
  C_L ≥ −1/(e²+1), so its contrast threshold is e² + 1 (XC5 E4, the lead's bound).
* `sqrt_ode_two_solutions`: x ≡ 0 and x(t) = t²/4 both solve ẋ = √x from x(0) = 0 — a Hölder-½ right-hand side does not
  determine its solution, which is why an open zero-field region (response ∝ √ε, XC5 E6) needs care beyond Osgood.
-/

theorem contrast_bound {n : ℕ} (N a b : Fin n → ℝ) (Nmin Nmax : ℝ) (hmin : 0 < Nmin) (hmm : Nmin ≤ Nmax)
    (hN : ∀ i, Nmin ≤ N i ∧ N i ≤ Nmax) (ha : ∀ i, 0 ≤ a i) (hb : ∀ i, 0 ≤ b i)
    (hab : ∑ i, a i ≤ ∑ i, b i) :
    ∑ i, N i * a i ≤ (Nmax / Nmin) * ∑ i, N i * b i := by
  have h1 : ∑ i, N i * a i ≤ Nmax * ∑ i, a i := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum; intro i _
    exact mul_le_mul_of_nonneg_right (hN i).2 (ha i)
  have hNmax : 0 ≤ Nmax := le_trans hmin.le hmm
  have h2 : Nmax * ∑ i, a i ≤ Nmax * ∑ i, b i := mul_le_mul_of_nonneg_left hab hNmax
  have h3 : ∑ i, b i ≤ (1 / Nmin) * ∑ i, N i * b i := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum; intro i _
    have : b i = (1 / Nmin) * (Nmin * b i) := by field_simp
    rw [this]
    apply mul_le_mul_of_nonneg_left _ (by positivity)
    have := (hN i).1
    nlinarith [hb i]
  calc ∑ i, N i * a i ≤ Nmax * ∑ i, b i := le_trans h1 h2
    _ ≤ Nmax * ((1 / Nmin) * ∑ i, N i * b i) := mul_le_mul_of_nonneg_left h3 hNmax
    _ = (Nmax / Nmin) * ∑ i, N i * b i := by ring

theorem convex_for_monotone_kernel (N d sT sL CT CL : ℝ) (hN : 0 ≤ N) (hsT : 0 ≤ sT) (hsL : 0 ≤ sL)
    (hCT : 0 ≤ CT) (hCL : 0 ≤ CL) :
    4 * N * d ≤ 4 * N * d + N * (4 * CT * sT + 4 * CL * sL) := by
  have : 0 ≤ N * (4 * CT * sT + 4 * CL * sL) := by positivity
  linarith

theorem mu_exp_CL_floor (u : ℝ) (hu : u ≤ Real.exp (-2)) (hpos : 0 < 1 + u) :
    -1 / (Real.exp 2 + 1) ≤ 1 / (1 + u) - 1 := by
  have he2 : 0 < Real.exp 2 := Real.exp_pos 2
  have hinv : Real.exp (-2) = 1 / Real.exp 2 := by rw [Real.exp_neg]; ring
  rw [hinv] at hu
  have hden : 0 < Real.exp 2 + 1 := by linarith
  have key : 1 / (1 + 1 / Real.exp 2) ≤ 1 / (1 + u) :=
    one_div_le_one_div_of_le hpos (by linarith)
  have hrw : 1 / (1 + 1 / Real.exp 2) - 1 = -1 / (Real.exp 2 + 1) := by field_simp; ring
  linarith

theorem sqrt_ode_two_solutions (t : ℝ) (ht : 0 ≤ t) :
    HasDerivAt (fun s : ℝ => s ^ 2 / 4) (Real.sqrt (t ^ 2 / 4)) t ∧
    HasDerivAt (fun _ : ℝ => (0 : ℝ)) (Real.sqrt 0) t := by
  constructor
  · have hs : Real.sqrt (t ^ 2 / 4) = t / 2 := by
      rw [show t ^ 2 / 4 = (t / 2) ^ 2 by ring]
      exact Real.sqrt_sq (by linarith)
    rw [hs]
    have h := (hasDerivAt_pow 2 t).div_const 4
    refine h.congr_deriv ?_
    norm_num
    ring
  · simpa using hasDerivAt_const t (0 : ℝ)

#print axioms contrast_bound
#print axioms convex_for_monotone_kernel
#print axioms mu_exp_CL_floor
#print axioms sqrt_ode_two_solutions
