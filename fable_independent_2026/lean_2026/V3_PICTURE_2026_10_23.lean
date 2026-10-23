import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The full picture of the screened theory v3: algebraic certificates (2026-10-23)

These are the algebraic cores of v3's failure mechanisms, as derived in the rebuild lanes. The numbers that feed them are
numerical results of those lanes and are not certified here. The pass side (the law, its inverse, slopes, the a₀-line's
uniqueness, the exact EFE cubic, a₀ = c²√(Λ/32π) at κ = ½, leaf convexity) is already certified in EQB_S1, EQB_A0LINE,
EQB_S5, TOE_BEST_ATTEMPT_2026_10_12, KAPPA_LOGIC_2026_10_20, XC2 and XC5.

1. **Saddles (H4).** At μ_K = 0 the khronon/dust pair obeys ω² = 4πGρ_τ(M − 1 + L★²k²/2).
   * `saddle_unbounded`: if ρ_τ < 0 and L★ > 0, the growth rate −ω² exceeds every bound: Hadamard ill-posed.
   * `saddle_no_stiffness`: with L★ = 0, −ω² does not depend on k: bounded.
   * `switched_*`: with the stiffness switched on only where D·P ≥ 0, and a non-negative dust density, the growth rate is
     k-independent wherever ρ_τ < 0, stable wherever ρ_τ ≥ 0 and M ≥ 1, and identical to v3 wherever D·P ≥ 0, which covers
     every screened region. This is pointwise, leading-WKB order only; the interface and the statics are lane X3's.
2. **Growth (M1).** The exact dust kernel is s(k; f₀) = (μ² − f₀k²)/((1 − f₀)k² + μ²).
   * `kernel_at_zero`: s = 1 at k = 0, so large scales grow as dust.
   * `kernel_Jx_*`: for J_x (f₀ = 0), s = μ²/(k² + μ²) lies in (0, 1], is strictly decreasing in k, and is below μ²/k²:
     modes above μ are not held.
   * `kernel_anti_f0`: s strictly decreases in f₀, so J′(0) = 0 (f₀ = 1) holds the dust less than J_x (f₀ = 0).
3. **Early universe (Q6).** The literal K carries a stiff partner ρ_s = A a⁻⁶ with A ∝ μ_K⁻².
   * `stiff_beats_radiation_iff`: A a⁻⁶ > R a⁻⁴ ⟺ a² < A/R.
   * `crossing_redshift_linear`: 1 + z_× is proportional to μ_K.
   * `record_crossings_consistent`: Q6's 1854.4 (μ_K 14.8) and 318684 (μ_K 2542) obey that law to 0.1 %.
4. **Clusters (S4).** The static dust's first oscillation sits at r_C ∝ (r_M)^{1/3} with r_M ∝ M^{1/2}.
   * `onset_exponent`: (M^{1/2})^{1/3} = M^{1/6}, and r_C strictly increases with M: lighter systems are hit at smaller
     radii, galaxies before clusters.
5. **The dust coupling (X6, X-D3).** Static held dust with weight α on Ξ gives (α − 1 + μ(x))x = b, μ(x) = x/(1 + x),
   x = g/a₀, b = g_N/a₀.
   * `coupling_one_is_law`: α = 1 is exactly the a₀-line b(1 + x) = x².
   * `coupling_floor`: α < 1 forces x > (1 − α)/α, an acceleration floor however small b is.
   * `coupling_newtonian`: α > 1 forces x < b/(α − 1), and so x < √b once b < (α − 1)²: never the deep law.
6. **Hosted systems (U1 T3, X6 X-D5).** In a static host the khronon charge feels no host force.
   * `fall_rate` / `dusty_unit_lags`: a bound unit of baryons M_b and held dust M_τ > 0 falls at g·M_b/(M_b + M_τ) < g, so it
     cannot fall with its host and keep its dust.

κ = ½ is FITTED; footings never pooled; no dark-matter particle; the theory is not closed.
-/

open Real

namespace V3Picture

/-! ## 1. Saddles (H4) and the switched stiffness (X3) -/

/-- H4's dispersion at μ_K = 0: ω² = 4πGρ(M − 1 + L²k²/2). -/
noncomputable def omega2 (G ρ M L k : ℝ) : ℝ := 4 * π * G * ρ * (M - 1 + L ^ 2 * k ^ 2 / 2)

/-- With ρ_τ < 0 and L★ > 0 the growth rate −ω² is unbounded in k (Hadamard ill-posed). -/
theorem saddle_unbounded (G ρ M L : ℝ) (hG : 0 < G) (hρ : ρ < 0) (hL : 0 < L) :
    ∀ B : ℝ, ∃ k : ℝ, B < -omega2 G ρ M L k := by
  intro B
  set c0 : ℝ := -(4 * π * G * ρ * (M - 1)) with hc0
  set c1 : ℝ := 2 * π * G * (-ρ) * L ^ 2 with hc1
  have hc1pos : 0 < c1 := by
    have : 0 < -ρ := by linarith
    positivity
  set K : ℝ := (|B| + |c0| + 1) / c1 with hK
  have hKnn : 0 ≤ K := by positivity
  refine ⟨Real.sqrt K, ?_⟩
  have hk2 : (Real.sqrt K) ^ 2 = K := Real.sq_sqrt hKnn
  have hform : -omega2 G ρ M L (Real.sqrt K) = c0 + c1 * (Real.sqrt K) ^ 2 := by
    simp only [omega2, hc0, hc1]; ring
  rw [hform, hk2, hK, mul_div_cancel₀ _ (ne_of_gt hc1pos)]
  have h1 : B ≤ |B| := le_abs_self B
  have h2 : 0 ≤ c0 + |c0| := by have := neg_abs_le c0; linarith
  linarith

/-- With L★ = 0 the growth rate does not depend on k: bounded. -/
theorem saddle_no_stiffness (G ρ M k : ℝ) : -omega2 G ρ M 0 k = -(4 * π * G * ρ * (M - 1)) := by
  simp only [omega2]; ring

/-- The switched stiffness: −(γ_L/2)[max(D·P, 0)]², so the k² term is present only where D·P ≥ 0. ρ_τ = D·P + d. -/
noncomputable def omega2Switched (G DP d M L k : ℝ) : ℝ :=
  4 * π * G * (DP + d) * (M - 1 + (if 0 ≤ DP then L ^ 2 else 0) * k ^ 2 / 2)

/-- Where ρ_τ < 0 and the dust density is non-negative, D·P < 0, so the switched rate is k-independent (bounded). -/
theorem switched_bounded_where_negative (G DP d M L k : ℝ) (hd : 0 ≤ d) (hρ : DP + d < 0) :
    -omega2Switched G DP d M L k = -(4 * π * G * (DP + d) * (M - 1)) := by
  have hDP : ¬ (0 ≤ DP) := by intro h; linarith
  simp only [omega2Switched, hDP, if_false]; ring

/-- Where ρ_τ ≥ 0 and M ≥ 1 the switched pair is stable: ω² ≥ 0 for every k. -/
theorem switched_stable_where_positive (G DP d M L k : ℝ) (hG : 0 ≤ G) (hρ : 0 ≤ DP + d) (hM : 1 ≤ M) :
    0 ≤ omega2Switched G DP d M L k := by
  simp only [omega2Switched]
  have hs : 0 ≤ (if 0 ≤ DP then L ^ 2 else 0) := by split_ifs <;> positivity
  have h1 : 0 ≤ M - 1 + (if 0 ≤ DP then L ^ 2 else 0) * k ^ 2 / 2 := by
    have : 0 ≤ (if 0 ≤ DP then L ^ 2 else 0) * k ^ 2 / 2 := by positivity
    linarith
  have hπ : 0 ≤ π := Real.pi_pos.le
  have : 0 ≤ 4 * π * G * (DP + d) := by positivity
  exact mul_nonneg this h1

/-- Wherever D·P ≥ 0 (every screened region) the switched dispersion is v3's. -/
theorem switched_agrees_where_screened (G DP d M L k : ℝ) (hDP : 0 ≤ DP) :
    omega2Switched G DP d M L k = omega2 G (DP + d) M L k := by
  simp only [omega2Switched, omega2, hDP, if_true]

/-- So the switched growth rate is bounded, uniformly in k, at every point: by 4πG|ρ_τ||M − 1|. -/
theorem switched_uniform_bound (G DP d M L k : ℝ) (hG : 0 ≤ G) (hd : 0 ≤ d) (hM : 1 ≤ M) :
    -omega2Switched G DP d M L k ≤ 4 * π * G * |DP + d| * |M - 1| := by
  have hπ : 0 ≤ π := Real.pi_pos.le
  by_cases hρ : DP + d < 0
  · rw [switched_bounded_where_negative G DP d M L k hd hρ]
    have hM1 : |M - 1| = M - 1 := abs_of_nonneg (by linarith)
    have hρa : |DP + d| = -(DP + d) := abs_of_neg hρ
    rw [hM1, hρa]; nlinarith [mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 4) hπ) hG]
  · push_neg at hρ
    have h0 := switched_stable_where_positive G DP d M L k hG hρ hM
    have : 0 ≤ 4 * π * G * |DP + d| * |M - 1| := by positivity
    linarith

/-! ## 2. The growth kernel (M1) -/

/-- s(k; f₀) = (μ² − f₀k²)/((1 − f₀)k² + μ²). -/
noncomputable def kernel (μ f0 k : ℝ) : ℝ := (μ ^ 2 - f0 * k ^ 2) / ((1 - f0) * k ^ 2 + μ ^ 2)

theorem kernel_at_zero (μ f0 : ℝ) (hμ : μ ≠ 0) : kernel μ f0 0 = 1 := by
  have : μ ^ 2 ≠ 0 := pow_ne_zero 2 hμ
  simp [kernel, this]

theorem kernel_Jx (μ k : ℝ) : kernel μ 0 k = μ ^ 2 / (k ^ 2 + μ ^ 2) := by
  simp [kernel]

theorem kernel_Jx_pos_le_one (μ k : ℝ) (hμ : μ ≠ 0) : 0 < kernel μ 0 k ∧ kernel μ 0 k ≤ 1 := by
  rw [kernel_Jx]
  have hμ2 : 0 < μ ^ 2 := by positivity
  have hden : 0 < k ^ 2 + μ ^ 2 := by positivity
  refine ⟨div_pos hμ2 hden, ?_⟩
  rw [div_le_one hden]; nlinarith [sq_nonneg k]

theorem kernel_Jx_strictAnti (μ k₁ k₂ : ℝ) (hμ : μ ≠ 0) (h0 : 0 ≤ k₁) (h12 : k₁ < k₂) :
    kernel μ 0 k₂ < kernel μ 0 k₁ := by
  rw [kernel_Jx, kernel_Jx]
  have hμ2 : 0 < μ ^ 2 := by positivity
  have hsq : k₁ ^ 2 < k₂ ^ 2 := by nlinarith
  apply div_lt_div_of_pos_left hμ2 (by positivity) (by linarith)

theorem kernel_Jx_le_inv_sq (μ k : ℝ) (hk : k ≠ 0) : kernel μ 0 k ≤ μ ^ 2 / k ^ 2 := by
  rw [kernel_Jx]
  have hk2 : 0 < k ^ 2 := by positivity
  exact div_le_div_of_nonneg_left (sq_nonneg μ) hk2 (by nlinarith [sq_nonneg μ])

/-- s strictly decreases in f₀ (for k ≠ 0, μ ≠ 0, f₀ < f₁ ≤ 1). -/
theorem kernel_anti_f0 (μ f0 f1 k : ℝ) (hμ : μ ≠ 0) (hk : k ≠ 0) (h01 : f0 < f1) (hf1 : f1 ≤ 1) :
    kernel μ f1 k < kernel μ f0 k := by
  unfold kernel
  have hμ2 : 0 < μ ^ 2 := by positivity
  have hk2 : 0 < k ^ 2 := by positivity
  have hD1 : 0 < (1 - f1) * k ^ 2 + μ ^ 2 := by nlinarith
  have hD0 : 0 < (1 - f0) * k ^ 2 + μ ^ 2 := by nlinarith
  rw [div_lt_div_iff₀ hD1 hD0]
  have key : (μ ^ 2 - f0 * k ^ 2) * ((1 - f1) * k ^ 2 + μ ^ 2) - (μ ^ 2 - f1 * k ^ 2) * ((1 - f0) * k ^ 2 + μ ^ 2)
      = (f1 - f0) * (k ^ 2) ^ 2 := by ring
  have : 0 < (f1 - f0) * (k ^ 2) ^ 2 := by
    have : 0 < f1 - f0 := by linarith
    positivity
  linarith

/-! ## 3. The early universe (Q6) -/

theorem stiff_beats_radiation_iff (A R a : ℝ) (hA : 0 < A) (hR : 0 < R) (ha : 0 < a) :
    R * a⁻¹ ^ 4 < A * a⁻¹ ^ 6 ↔ a ^ 2 < A / R := by
  have ha2 : 0 < a ^ 2 := by positivity
  have ha4 : 0 < a ^ 4 := by positivity
  have ha6 : 0 < a ^ 6 := by positivity
  rw [inv_pow, inv_pow, ← div_eq_mul_inv, ← div_eq_mul_inv, div_lt_div_iff₀ ha4 ha6, lt_div_iff₀ hR]
  constructor
  · intro h
    have h6 : a ^ 6 = a ^ 2 * a ^ 4 := by ring
    rw [h6] at h
    nlinarith
  · intro h
    have h6 : a ^ 6 = a ^ 2 * a ^ 4 := by ring
    rw [h6]
    nlinarith

/-- With A = C/μ² (C > 0), the crossing a_× = √(A/R) gives 1/a_× = μ √(R/C): linear in μ. -/
theorem crossing_redshift_linear (C R μ : ℝ) (hC : 0 < C) (hR : 0 < R) (hμ : 0 < μ) :
    1 / Real.sqrt ((C / μ ^ 2) / R) = μ * Real.sqrt (R / C) := by
  have h1 : (C / μ ^ 2) / R = (C / R) / μ ^ 2 := by ring
  have hs : Real.sqrt ((C / R) / μ ^ 2) = Real.sqrt (C / R) / μ := by
    rw [Real.sqrt_div (by positivity : (0:ℝ) ≤ C / R), Real.sqrt_sq hμ.le]
  have hr : Real.sqrt (R / C) = (Real.sqrt (C / R))⁻¹ := by
    rw [← Real.sqrt_inv, inv_div]
  rw [h1, hs, hr, one_div, inv_div, div_eq_mul_inv]

/-- Q6's own crossings (1 + z at μ_K 14.8 and 2542 h/Mpc) obey the linear law to better than 0.1 %. -/
theorem record_crossings_consistent :
    |((1 + 1854.4 : ℝ) * (2542 / 14.8) - (1 + 318684)) / (1 + 318684)| < 1 / 1000 := by
  norm_num [abs_lt]

/-! ## 4. Cluster ordering (S4) -/

theorem onset_exponent (M : ℝ) (hM : 0 ≤ M) : (M ^ (1 / 2 : ℝ)) ^ (1 / 3 : ℝ) = M ^ (1 / 6 : ℝ) := by
  rw [← Real.rpow_mul hM]; norm_num

theorem onset_strictMono (k M₁ M₂ : ℝ) (hk : 0 < k) (h0 : 0 ≤ M₁) (h12 : M₁ < M₂) :
    k * M₁ ^ (1 / 6 : ℝ) < k * M₂ ^ (1 / 6 : ℝ) := by
  have := Real.rpow_lt_rpow h0 h12 (by norm_num : (0:ℝ) < 1 / 6)
  exact mul_lt_mul_of_pos_left this hk

/-! ## 5. The dust coupling (X6, X-D3) -/

/-- The static balance for held dust with weight α on Ξ, in units of a₀: (α − 1 + x/(1+x)) x = b. -/
noncomputable def balance (α x : ℝ) : ℝ := (α - 1 + x / (1 + x)) * x

/-- α = 1 is exactly the a₀-line b(1 + x) = x² (g_N(g + a₀) = g²). -/
theorem coupling_one_is_law (x b : ℝ) (hx : 0 < x) : balance 1 x = b ↔ b * (1 + x) = x ^ 2 := by
  have h1x : 0 < 1 + x := by linarith
  simp only [balance]
  constructor
  · intro h; rw [← h]; field_simp; ring
  · intro h; field_simp; nlinarith [h]

/-- α < 1 (α > 0): every solution with b > 0 sits above the floor x > (1 − α)/α. -/
theorem coupling_floor (α x b : ℝ) (hα0 : 0 < α) (hx : 0 < x) (hb : 0 < b) (h : balance α x = b) :
    (1 - α) / α < x := by
  have h1x : 0 < 1 + x := by linarith
  simp only [balance] at h
  have hpos : 0 < α - 1 + x / (1 + x) := by
    by_contra hc; push_neg at hc
    have : (α - 1 + x / (1 + x)) * x ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hc hx.le
    linarith
  have hfrac : x / (1 + x) > 1 - α := by linarith
  rw [gt_iff_lt, lt_div_iff₀ h1x] at hfrac
  rw [div_lt_iff₀ hα0]; nlinarith

/-- α > 1: every solution has x < b/(α − 1) (rescaled Newton). -/
theorem coupling_newtonian (α x b : ℝ) (hα : 1 < α) (hx : 0 < x) (h : balance α x = b) :
    x < b / (α - 1) := by
  have h1x : 0 < 1 + x := by linarith
  simp only [balance] at h
  have hfr : 0 < x / (1 + x) := div_pos hx h1x
  rw [lt_div_iff₀ (by linarith)]
  nlinarith [mul_pos hfr hx]

/-- …and so, for α > 1 and b < (α − 1)², x < √b: the deep law x ≈ √b is never reached. -/
theorem coupling_not_deep (α x b : ℝ) (hα : 1 < α) (hx : 0 < x) (hb : 0 < b) (hsmall : b < (α - 1) ^ 2)
    (h : balance α x = b) : x < Real.sqrt b := by
  have hN := coupling_newtonian α x b hα hx h
  have hα1 : 0 < α - 1 := by linarith
  have hsb : 0 < Real.sqrt b := Real.sqrt_pos.mpr hb
  have hsq : Real.sqrt b < α - 1 := by
    rw [show α - 1 = Real.sqrt ((α - 1) ^ 2) from (Real.sqrt_sq hα1.le).symm]
    exact Real.sqrt_lt_sqrt hb.le hsmall
  have : b / (α - 1) < Real.sqrt b := by
    rw [div_lt_iff₀ hα1]
    have hb' : b = Real.sqrt b * Real.sqrt b := (Real.mul_self_sqrt hb.le).symm
    nlinarith
  linarith

/-! ## 6. Hosted systems (U1 T3, X6 X-D5) -/

/-- Baryons feel the host's g; held dust feels nothing: the bound unit falls at g·M_b/(M_b + M_τ). -/
theorem fall_rate (g Mb Mt : ℝ) : (Mb * g + Mt * 0) / (Mb + Mt) = g * (Mb / (Mb + Mt)) := by
  rw [mul_zero, add_zero, mul_comm Mb g, mul_div_assoc]

theorem dusty_unit_lags (g Mb Mt : ℝ) (hg : 0 < g) (hb : 0 < Mb) (ht : 0 < Mt) : g * (Mb / (Mb + Mt)) < g := by
  have hs : 0 < Mb + Mt := by linarith
  have : Mb / (Mb + Mt) < 1 := by rw [div_lt_one hs]; linarith
  nlinarith

end V3Picture

#print axioms V3Picture.saddle_unbounded
#print axioms V3Picture.saddle_no_stiffness
#print axioms V3Picture.switched_bounded_where_negative
#print axioms V3Picture.switched_stable_where_positive
#print axioms V3Picture.switched_agrees_where_screened
#print axioms V3Picture.switched_uniform_bound
#print axioms V3Picture.kernel_at_zero
#print axioms V3Picture.kernel_Jx
#print axioms V3Picture.kernel_Jx_pos_le_one
#print axioms V3Picture.kernel_Jx_strictAnti
#print axioms V3Picture.kernel_Jx_le_inv_sq
#print axioms V3Picture.kernel_anti_f0
#print axioms V3Picture.stiff_beats_radiation_iff
#print axioms V3Picture.crossing_redshift_linear
#print axioms V3Picture.record_crossings_consistent
#print axioms V3Picture.onset_exponent
#print axioms V3Picture.onset_strictMono
#print axioms V3Picture.coupling_one_is_law
#print axioms V3Picture.coupling_floor
#print axioms V3Picture.coupling_newtonian
#print axioms V3Picture.coupling_not_deep
#print axioms V3Picture.fall_rate
#print axioms V3Picture.dusty_unit_lags
