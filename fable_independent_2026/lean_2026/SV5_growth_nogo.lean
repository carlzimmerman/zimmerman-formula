import Mathlib

/-!
# SV5 -- Lean certificate for the growth / CMB-lensing escape classes (closure_2026_11_06/SV5_growth_mechanism)

CERTIFIED (algebra only):
* iter_1 (class W, a0 law on the linear web):
  - `weighted_sum_ge`: weights nu_i >= m on nonnegative x_i give m * sum x <= sum nu x (pointwise nu >= nu_min on the grid).
  - `proj_inner`: a symmetric P with P gN = gN gives <P v, gN> = <v, gN> (QUMOND's longitudinal projection fixes g_N).
  - `cs_power_bound`, `law_on_power_bound`: if <g, gN> >= m |gN|^2 with m >= 0, then |g|^2 >= m^2 |gN|^2.
  - `nu_lawS`: x = nu(y) y with nu(y) = 1/2 + sqrt(1/4 + 1/y) solves x^2 = y (x + 1) (law S, EQUATIONS 4.1).
  - `nu_antitone`: nu is antitone on y > 0, so nu >= nu(y_max) wherever |g_N| <= y_max a0.
  - `nu_ge_two`: 0 < y <= 1/2 gives nu(y) >= 2, so the integrated power boost is >= 4 on such a field.
* iter_2 (class C, charge-switched Jeans scale):
  - `deep_point_flux`, `deep_point_flux_deriv`: r^2 (c/r) = c r and d/dr = c, i.e. the deep-MOND point-mass phantom density
    is c/(4 pi G r^2) with c = sqrt(a0 G M).
  - `deep_point_rho_antitone`: that density decreases with r (host charge is lowest at r_ta inside r_ta).
  - `switch_ordering`, `switch_no_window`: with k_J = mu(Sigma) antitone, Sigma_host <= Sigma_web gives mu(Sigma_web) <=
    mu(Sigma_host); a host needing mu <= k_hi and a web needing mu >= k_lo > k_hi cannot both hold.
* iter_3 (class T, time only through a0):
  - `time_only_coincidence`: equal a0 gives equal lambda_J.
  - `stiff_on_preimage`: if F(r(z)) >= L on Z_H and r(z') lies in r(Z_H), then F(r(z')) >= L (member M* is the most generous).
  - `ivt_crossing`: a continuous history with r(z1) > 1 > r(z2) returns to today's a0 at some z_c in [z1, z2].
NOT CERTIFIED: the CLASS spectra, the growth ODE, the FFT field, the QX10 hydrostatics, any number graded against data.
Zero sorry; axioms printed below.
-/

open scoped RealInnerProductSpace

theorem weighted_sum_ge {ι : Type*} (s : Finset ι) (nu x : ι → ℝ) (m : ℝ)
    (hnu : ∀ i ∈ s, m ≤ nu i) (hx : ∀ i ∈ s, 0 ≤ x i) :
    m * ∑ i ∈ s, x i ≤ ∑ i ∈ s, nu i * x i := by
  rw [Finset.mul_sum]
  exact Finset.sum_le_sum fun i hi => mul_le_mul_of_nonneg_right (hnu i hi) (hx i hi)

theorem proj_inner {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] (P : E → E)
    (hsym : ∀ u w : E, ⟪P u, w⟫ = ⟪u, P w⟫) (v gN : E) (hfix : P gN = gN) :
    ⟪P v, gN⟫ = ⟪v, gN⟫ := by
  rw [hsym, hfix]

theorem cs_power_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] (g gN : E) (m : ℝ)
    (hm : 0 ≤ m) (h : m * ‖gN‖ ^ 2 ≤ ⟪g, gN⟫) : m ^ 2 * ‖gN‖ ^ 2 ≤ ‖g‖ ^ 2 := by
  have hcs : ⟪g, gN⟫ ≤ ‖g‖ * ‖gN‖ := real_inner_le_norm g gN
  have hn : 0 ≤ ‖gN‖ := norm_nonneg gN
  have hg : 0 ≤ ‖g‖ := norm_nonneg g
  rcases eq_or_lt_of_le hn with h0 | hpos
  · rw [← h0]; simp
  · have h1 : m * ‖gN‖ ≤ ‖g‖ := by
      have : m * ‖gN‖ * ‖gN‖ ≤ ‖g‖ * ‖gN‖ := by nlinarith
      exact le_of_mul_le_mul_right this hpos
    have h2 : 0 ≤ m * ‖gN‖ := mul_nonneg hm hn
    nlinarith [mul_le_mul h1 h1 h2 hg]

theorem law_on_power_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] (P : E → E)
    (hsym : ∀ u w : E, ⟪P u, w⟫ = ⟪u, P w⟫) (v gN : E) (hfix : P gN = gN) (m : ℝ) (hm : 0 ≤ m)
    (hv : m * ‖gN‖ ^ 2 ≤ ⟪v, gN⟫) : m ^ 2 * ‖gN‖ ^ 2 ≤ ‖P v‖ ^ 2 := by
  apply cs_power_bound (P v) gN m hm
  rw [proj_inner P hsym v gN hfix]; exact hv

/-- The simple-law nu: nu(y) = 1/2 + sqrt(1/4 + 1/y). -/
noncomputable def nuS (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

theorem nu_lawS (y : ℝ) (hy : 0 < y) : (nuS y * y) ^ 2 = y * (nuS y * y + 1) := by
  unfold nuS
  have hq : 0 ≤ 1 / 4 + 1 / y := by positivity
  have hs : Real.sqrt (1 / 4 + 1 / y) ^ 2 = 1 / 4 + 1 / y := Real.sq_sqrt hq
  have hy0 : y ≠ 0 := ne_of_gt hy
  have e1 : ((1 / 2 + Real.sqrt (1 / 4 + 1 / y)) * y) ^ 2
      = (1 / 4 + Real.sqrt (1 / 4 + 1 / y) + Real.sqrt (1 / 4 + 1 / y) ^ 2) * y ^ 2 := by ring
  rw [e1, hs]
  field_simp
  ring

theorem nu_antitone (y1 y2 : ℝ) (h1 : 0 < y1) (h12 : y1 ≤ y2) : nuS y2 ≤ nuS y1 := by
  unfold nuS
  have : 1 / y2 ≤ 1 / y1 := one_div_le_one_div_of_le h1 h12
  have := Real.sqrt_le_sqrt (by linarith : 1 / 4 + 1 / y2 ≤ 1 / 4 + 1 / y1)
  linarith

theorem nu_ge_two (y : ℝ) (hy : 0 < y) (hle : y ≤ 1 / 2) : 2 ≤ nuS y := by
  unfold nuS
  have h2 : 2 ≤ 1 / y := by rw [le_div_iff₀ hy]; linarith
  have h9 : (3 / 2 : ℝ) ^ 2 ≤ 1 / 4 + 1 / y := by nlinarith
  have := Real.sqrt_le_sqrt h9
  rw [Real.sqrt_sq (by norm_num : (0:ℝ) ≤ 3 / 2)] at this
  linarith

theorem deep_point_flux (c r : ℝ) (hr : r ≠ 0) : r ^ 2 * (c / r) = c * r := by
  field_simp

theorem deep_point_flux_deriv (c r : ℝ) : HasDerivAt (fun s : ℝ => c * s) c r := by
  simpa using (hasDerivAt_id r).const_mul c

theorem deep_point_rho_antitone (c K r1 r2 : ℝ) (hc : 0 ≤ c) (hK : 0 < K) (h1 : 0 < r1) (h12 : r1 ≤ r2) :
    c / (K * r2 ^ 2) ≤ c / (K * r1 ^ 2) := by
  apply div_le_div_of_nonneg_left hc (by positivity)
  have : r1 ^ 2 ≤ r2 ^ 2 := by nlinarith
  nlinarith

theorem switch_ordering (mu : ℝ → ℝ) (hmu : Antitone mu) (sh sw : ℝ) (h : sh ≤ sw) : mu sw ≤ mu sh :=
  hmu h

theorem switch_no_window (mu : ℝ → ℝ) (hmu : Antitone mu) (sh sw khi klo : ℝ) (h : sh ≤ sw)
    (hhost : mu sh ≤ khi) (hweb : klo ≤ mu sw) (hgap : khi < klo) : False := by
  have := hmu h
  linarith

theorem time_only_coincidence (F r : ℝ → ℝ) (z1 z2 : ℝ) (h : r z1 = r z2) : F (r z1) = F (r z2) := by
  rw [h]

theorem stiff_on_preimage (F r : ℝ → ℝ) (ZH : Set ℝ) (L z' : ℝ) (hH : ∀ z ∈ ZH, L ≤ F (r z))
    (him : r z' ∈ r '' ZH) : L ≤ F (r z') := by
  obtain ⟨z, hz, hrz⟩ := him
  rw [← hrz]; exact hH z hz

theorem ivt_crossing (r : ℝ → ℝ) (z1 z2 : ℝ) (h12 : z1 ≤ z2) (hc : ContinuousOn r (Set.Icc z1 z2))
    (ha : 1 < r z1) (hb : r z2 < 1) : ∃ zc ∈ Set.Icc z1 z2, r zc = 1 := by
  have := intermediate_value_Icc' h12 hc
  exact this ⟨hb.le, ha.le⟩

#print axioms weighted_sum_ge
#print axioms proj_inner
#print axioms cs_power_bound
#print axioms law_on_power_bound
#print axioms nu_lawS
#print axioms nu_antitone
#print axioms nu_ge_two
#print axioms deep_point_flux
#print axioms deep_point_flux_deriv
#print axioms deep_point_rho_antitone
#print axioms switch_ordering
#print axioms switch_no_window
#print axioms time_only_coincidence
#print axioms stiff_on_preimage
#print axioms ivt_crossing
