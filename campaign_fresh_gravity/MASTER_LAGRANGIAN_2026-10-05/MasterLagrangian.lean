import Mathlib

/-!
# Master Lagrangian of candidate B: what Lean can certify

Scalar pieces of the master action (MASTER_LAGRANGIAN.md), as real functions of their scalar arguments.
Lean certifies algebra, inequalities and reductions only. It does not certify that nature obeys the action,
nor any analytic PDE property beyond the stated inequalities.

Sections
* A. the RAR branch of the kernel (nu_mono = nu_RAR below the phantom peak y_p, L340 A1):
     nu > 1, nu - 1 <= 1/sqrt y (Newtonian limit), deep-MOND sandwich 1 <= sqrt y * nu <= 1 + sqrt y.
* B. nu_mono's tail: the phantom slope max(h_RAR', delta h_p/(y+y_p)) is > 0, so the phantom is strictly
     increasing (C_L > 0), the L340 monotonicity condition.
* C. a0 -> 0: the kernel term 2 alpha^2 qt(p/alpha) vanishes under the deep bound qt(s) <= M s sqrt s.
* D. the switch potential (CFG337 inverted symmetron): OFF state stable for 0 < U < 1, broken minimum
     stable for U > 1, f = 0 at sigma = 0; trigger concavity.
* E. reductions of the total scalar density: switch OFF + FRW (a^2 = 0, K = <K>) gives R - 2 Lambda + L_m.
* F. kinetic / principal coefficients: L340 tracking speed, CFG292 c_S^2 at beta = 0, CFG329 lapse coefficient,
     CFG337 switch kinetic matrix, L340 P1 window as rational inequalities.
* G. kappa = 1/2 with rho_Lambda = Lambda c^2/(8 pi G) gives a0 = c^2 sqrt(Lambda/(32 pi)) (algebraic identity).
-/

open Real Filter Topology Set

namespace MasterLagrangian

/-! ## A. the RAR branch of the kernel -/

/-- nu_RAR(y) = 1/(1 - exp(-sqrt y)) (L340 `nu_rar`). -/
noncomputable def nuRAR (y : ℝ) : ℝ := 1 / (1 - Real.exp (-Real.sqrt y))

lemma denom_pos {y : ℝ} (hy : 0 < y) : 0 < 1 - Real.exp (-Real.sqrt y) := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have : Real.exp (-Real.sqrt y) < 1 := by
    have h := Real.exp_lt_exp.mpr (show -Real.sqrt y < 0 by linarith)
    simpa using h
  linarith

lemma denom_lt_one {y : ℝ} (hy : 0 < y) : 1 - Real.exp (-Real.sqrt y) < 1 := by
  have := Real.exp_pos (-Real.sqrt y); linarith

/-- C_T = nu - 1 > 0 on the RAR branch. -/
theorem nuRAR_gt_one {y : ℝ} (hy : 0 < y) : 1 < nuRAR y := by
  unfold nuRAR
  rw [lt_div_iff₀ (denom_pos hy)]
  linarith [denom_lt_one hy]

/-- Newtonian-side bound: nu - 1 <= 1/sqrt y (from x + 1 <= e^x). -/
theorem nuRAR_sub_one_le {y : ℝ} (hy : 0 < y) : nuRAR y - 1 ≤ 1 / Real.sqrt y := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hd := denom_pos hy
  set x := Real.sqrt y with hx
  have hexp : x + 1 ≤ Real.exp x := by linarith [Real.add_one_le_exp x]
  have hprod : Real.exp x * Real.exp (-x) = 1 := by rw [← Real.exp_add]; simp
  have he : 0 < Real.exp (-x) := Real.exp_pos _
  -- (x+1) e^{-x} <= 1
  have key : (x + 1) * Real.exp (-x) ≤ 1 := by nlinarith
  unfold nuRAR
  rw [← hx]
  rw [div_sub_one (ne_of_gt hd), div_le_div_iff₀ hd hs]
  nlinarith

/-- Newtonian limit: nu_RAR -> 1 as y -> infinity (GR/Newton regained at high acceleration). -/
theorem nuRAR_tendsto_one : Tendsto nuRAR atTop (𝓝 1) := by
  have hsq : Tendsto (fun y : ℝ => Real.sqrt y) atTop atTop := by
    refine tendsto_atTop_atTop.mpr (fun b => ⟨b ^ 2, fun a ha => ?_⟩)
    calc b ≤ |b| := le_abs_self b
      _ = Real.sqrt (b ^ 2) := (Real.sqrt_sq_eq_abs b).symm
      _ ≤ Real.sqrt a := Real.sqrt_le_sqrt ha
  have hinv : Tendsto (fun y : ℝ => 1 / Real.sqrt y) atTop (𝓝 0) := by
    have h := tendsto_inv_atTop_zero.comp hsq
    simpa [one_div, Function.comp_def] using h
  have hup : Tendsto (fun y : ℝ => 1 + 1 / Real.sqrt y) atTop (𝓝 1) := by
    simpa using (tendsto_const_nhds (x := (1 : ℝ))).add hinv
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds hup ?_ ?_
  · filter_upwards [eventually_gt_atTop 0] with y hy
    exact le_of_lt (nuRAR_gt_one hy)
  · filter_upwards [eventually_gt_atTop 0] with y hy
    linarith [nuRAR_sub_one_le hy]

/-- Deep-MOND sandwich: with g_N = y a0 and g = nu g_N, g / sqrt(g_N a0) = sqrt y * nu lies in [1, 1 + sqrt y]. -/
theorem deep_mond_sandwich {y : ℝ} (hy : 0 < y) :
    1 ≤ Real.sqrt y * nuRAR y ∧ Real.sqrt y * nuRAR y ≤ 1 + Real.sqrt y := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hd := denom_pos hy
  set x := Real.sqrt y with hx
  have hlow : 1 - x ≤ Real.exp (-x) := by linarith [Real.add_one_le_exp (-x)]
  have hexp : x + 1 ≤ Real.exp x := by linarith [Real.add_one_le_exp x]
  have hprod : Real.exp x * Real.exp (-x) = 1 := by rw [← Real.exp_add]; simp
  have he : 0 < Real.exp (-x) := Real.exp_pos _
  unfold nuRAR
  rw [← hx]
  constructor
  · rw [mul_one_div, le_div_iff₀ hd]; linarith
  · rw [mul_one_div, div_le_iff₀ hd]
    -- x <= (1+x)(1 - e^{-x})  <=>  (1+x) e^{-x} <= 1
    nlinarith

/-- Deep-MOND limit: sqrt y * nu_RAR(y) -> 1 as y -> 0+, i.e. g -> sqrt(g_N a0). -/
theorem deep_mond_limit : Tendsto (fun y => Real.sqrt y * nuRAR y) (𝓝[>] 0) (𝓝 1) := by
  have hs : Tendsto (fun y : ℝ => 1 + Real.sqrt y) (𝓝[>] 0) (𝓝 1) := by
    have h0 : Tendsto (fun y : ℝ => Real.sqrt y) (𝓝 0) (𝓝 0) := by
      simpa using (Real.continuous_sqrt.tendsto 0)
    simpa using (tendsto_const_nhds (x := (1 : ℝ))).add (h0.mono_left nhdsWithin_le_nhds)
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds hs ?_ ?_
  · filter_upwards [self_mem_nhdsWithin] with y hy using (deep_mond_sandwich hy).1
  · filter_upwards [self_mem_nhdsWithin] with y hy using (deep_mond_sandwich hy).2

/-! ## B. nu_mono's monotone tail (L340 A1) -/

/-- The nu_mono phantom slope max(h_RAR', delta h_p/(y + y_p)) is strictly positive (C_L > 0). -/
theorem mono_slope_pos (d δ hp yp y : ℝ) (hδ : 0 < δ) (hhp : 0 < hp) (hyp : 0 < yp) (hy : 0 ≤ y) :
    0 < max d (δ * hp / (y + yp)) :=
  lt_of_lt_of_le (by positivity) (le_max_right _ _)

/-- Any phantom h with derivative max(d y, delta h_p/(y + y_p)) on y > 0 is strictly increasing there. -/
theorem mono_phantom_strictMono (h d : ℝ → ℝ) (δ hp yp : ℝ) (hδ : 0 < δ) (hhp : 0 < hp) (hyp : 0 < yp)
    (hder : ∀ y, 0 < y → HasDerivAt h (max (d y) (δ * hp / (y + yp))) y) :
    StrictMonoOn h (Ioi 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ioi 0)
  · intro y hy; exact (hder y hy).continuousAt.continuousWithinAt
  · intro y hy
    rw [interior_Ioi] at hy
    rw [(hder y hy).deriv]
    exact mono_slope_pos _ _ _ _ _ hδ hhp hyp (le_of_lt hy)

/-- C_T = h/y > 0 wherever the phantom h is positive. -/
theorem CT_pos (h y : ℝ) (hh : 0 < h) (hy : 0 < y) : 0 < h / y := div_pos hh hy

/-! ## C. a0 -> 0 removes the MOND sector -/

/-- Kernel term with alpha = a0/c^2 and field strength p >= 0: 2 alpha^2 qt(p/alpha), qt(s) = q(s^2).
Under the deep bound 0 <= qt(s) <= M s sqrt s (q ~ (4/3) s^(3/2), CFG329 T1) it is <= 2 M p sqrt p sqrt alpha. -/
theorem kernel_term_bound (qt : ℝ → ℝ) (M p α : ℝ) (hα : 0 < α) (hp : 0 ≤ p)
    (hq : qt (p / α) ≤ M * (p / α) * Real.sqrt (p / α)) :
    2 * α ^ 2 * qt (p / α) ≤ 2 * M * p * Real.sqrt p * Real.sqrt α := by
  have hsa : 0 < Real.sqrt α := Real.sqrt_pos.mpr hα
  have hsq : Real.sqrt α * Real.sqrt α = α := Real.mul_self_sqrt (le_of_lt hα)
  have hdiv : Real.sqrt (p / α) = Real.sqrt p / Real.sqrt α := Real.sqrt_div' p (le_of_lt hα)
  have h2 : 0 ≤ 2 * α ^ 2 := by positivity
  calc 2 * α ^ 2 * qt (p / α) ≤ 2 * α ^ 2 * (M * (p / α) * Real.sqrt (p / α)) :=
        mul_le_mul_of_nonneg_left hq h2
    _ = 2 * M * p * Real.sqrt p * Real.sqrt α := by
        rw [hdiv]
        set s := Real.sqrt α with hs
        have hαs : α = s ^ 2 := by rw [sq, hsq]
        rw [hαs]; field_simp

theorem kernel_term_vanishes (qt : ℝ → ℝ) (M p : ℝ) (hp : 0 ≤ p)
    (hq0 : ∀ s, 0 ≤ s → 0 ≤ qt s) (hq : ∀ s, 0 ≤ s → qt s ≤ M * s * Real.sqrt s) :
    Tendsto (fun α => 2 * α ^ 2 * qt (p / α)) (𝓝[>] 0) (𝓝 0) := by
  have hup : Tendsto (fun α : ℝ => 2 * M * p * Real.sqrt p * Real.sqrt α) (𝓝[>] 0) (𝓝 0) := by
    have h0 : Tendsto (fun α : ℝ => Real.sqrt α) (𝓝 0) (𝓝 0) := by
      simpa using (Real.continuous_sqrt.tendsto 0)
    simpa using ((h0.mono_left nhdsWithin_le_nhds).const_mul (2 * M * p * Real.sqrt p))
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds hup ?_ ?_
  · filter_upwards [self_mem_nhdsWithin] with α hα
    have hα' : (0 : ℝ) < α := hα
    have := hq0 (p / α) (div_nonneg hp (le_of_lt hα'))
    positivity
  · filter_upwards [self_mem_nhdsWithin] with α hα
    have hα' : (0 : ℝ) < α := hα
    exact kernel_term_bound qt M p α hα' hp (hq _ (div_nonneg hp (le_of_lt hα')))

/-- The RAR branch obeys the slope bound behind the deep bound: q'(s^2) = nu - 1 <= 1/sqrt y. -/
theorem rar_branch_slope_bound {y : ℝ} (hy : 0 < y) : 0 < nuRAR y - 1 ∧ nuRAR y - 1 ≤ 1 / Real.sqrt y :=
  ⟨by linarith [nuRAR_gt_one hy], nuRAR_sub_one_le hy⟩

/-! ## D. the switch potential (CFG337) -/

/-- Trigger T(U) = 1 - 1/U. -/
noncomputable def T (U : ℝ) : ℝ := 1 - 1 / U

/-- V = -(1/2) mu0^2 T(U) sigma^2 + (lambda/4) sigma^4. -/
noncomputable def V (μ0 lam U σ : ℝ) : ℝ := -(1 / 2) * μ0 ^ 2 * T U * σ ^ 2 + lam / 4 * σ ^ 4
noncomputable def V1 (μ0 lam U σ : ℝ) : ℝ := -μ0 ^ 2 * T U * σ + lam * σ ^ 3
noncomputable def V2 (μ0 lam U σ : ℝ) : ℝ := -μ0 ^ 2 * T U + 3 * lam * σ ^ 2

theorem V_hasDeriv (μ0 lam U σ : ℝ) : HasDerivAt (V μ0 lam U) (V1 μ0 lam U σ) σ := by
  have h := ((hasDerivAt_pow 2 σ).const_mul (-(1 / 2) * μ0 ^ 2 * T U)).add
    ((hasDerivAt_pow 4 σ).const_mul (lam / 4))
  unfold V V1
  exact h.congr_deriv (by norm_num; ring)

theorem V1_hasDeriv (μ0 lam U σ : ℝ) : HasDerivAt (V1 μ0 lam U) (V2 μ0 lam U σ) σ := by
  have h := ((hasDerivAt_id σ).const_mul (-μ0 ^ 2 * T U)).add ((hasDerivAt_pow 3 σ).const_mul lam)
  unfold V1 V2
  exact h.congr_deriv (by norm_num; ring)

/-- sigma = 0 is always a stationary point. -/
theorem off_stationary (μ0 lam U : ℝ) : V1 μ0 lam U 0 = 0 := by unfold V1; ring

/-- FRW (0 < U < 1): the OFF state has positive mass^2 = mu0^2 (1/U - 1) > 0. -/
theorem frw_off_stable (μ0 lam U : ℝ) (hμ : μ0 ≠ 0) (hU0 : 0 < U) (hU1 : U < 1) :
    0 < V2 μ0 lam U 0 := by
  unfold V2 T
  have hT : 1 - 1 / U < 0 := by
    have : 1 < 1 / U := by rw [lt_div_iff₀ hU0]; linarith
    linarith
  have hm : 0 < μ0 ^ 2 := by positivity
  nlinarith

theorem frw_mass_formula (μ0 lam U : ℝ) (hU : U ≠ 0) : V2 μ0 lam U 0 = μ0 ^ 2 * (1 / U - 1) := by
  unfold V2 T; ring

/-- Bound interior (U > 1): sigma_b^2 = mu0^2 T/lambda is stationary with mass^2 = 2 mu0^2 T > 0. -/
theorem broken_min (μ0 lam U σ : ℝ) (hμ : μ0 ≠ 0) (hl : 0 < lam) (hU : 1 < U)
    (hσ : σ ^ 2 = μ0 ^ 2 * T U / lam) :
    V1 μ0 lam U σ = 0 ∧ V2 μ0 lam U σ = 2 * μ0 ^ 2 * T U ∧ 0 < V2 μ0 lam U σ := by
  have hT : 0 < T U := by
    unfold T
    have : 1 / U < 1 := by rw [div_lt_one (by linarith)]; exact hU
    linarith
  have hm : 0 < μ0 ^ 2 := by positivity
  have hl' : lam ≠ 0 := ne_of_gt hl
  have hs : lam * σ ^ 2 = μ0 ^ 2 * T U := by rw [hσ]; field_simp
  have e1 : V1 μ0 lam U σ = 0 := by
    unfold V1
    have : lam * σ ^ 3 = (lam * σ ^ 2) * σ := by ring
    rw [this, hs]; ring
  have e2 : V2 μ0 lam U σ = 2 * μ0 ^ 2 * T U := by
    unfold V2
    have : 3 * lam * σ ^ 2 = 3 * (lam * σ ^ 2) := by ring
    rw [this, hs]; ring
  refine ⟨e1, e2, ?_⟩
  rw [e2]; positivity

/-- Switch factor f = sigma^2/v^2 vanishes in the OFF state. -/
noncomputable def fsw (σ v2 : ℝ) : ℝ := σ ^ 2 / v2
theorem f_off (v2 : ℝ) : fsw 0 v2 = 0 := by unfold fsw; simp

/-- At the broken minimum f = T(U) (v^2 = mu0^2/lambda). -/
theorem f_broken (μ0 lam U σ : ℝ) (hμ : μ0 ≠ 0) (hl : 0 < lam) (hσ : σ ^ 2 = μ0 ^ 2 * T U / lam) :
    fsw σ (μ0 ^ 2 / lam) = T U := by
  unfold fsw; rw [hσ]; have : μ0 ^ 2 ≠ 0 := by positivity
  field_simp

/-- Trigger concavity: T''(U) = -2/U^3 < 0 for U > 0. -/
theorem trigger_concave (U : ℝ) (hU : 0 < U) : -2 / U ^ 3 < 0 := by
  have : 0 < U ^ 3 := by positivity
  exact div_neg_of_neg_of_pos (by norm_num) this

/-! ## E. reductions of the total scalar density -/

/-- Total scalar density (units c^3/16 pi G dropped): R - 2 Lambda + f L_MOND + alpha_c a^2 - c_2 (K - <K>)^2 + L_m.
L_MOND stands for the C-H sector 2|DU - a|^2 + 2 alpha^2 q + heat slice + lambda_0 (W - U). -/
def Ltot (R Λ f Lmond αc a2 c2 K Kb Lm : ℝ) : ℝ := R - 2 * Λ + f * Lmond + αc * a2 - c2 * (K - Kb) ^ 2 + Lm

/-- Switch OFF (f = 0) on FRW (a^2 = 0, K = <K> on every leaf): GR + Lambda + matter. -/
theorem switch_off_frw (R Λ Lmond αc c2 K Lm : ℝ) :
    Ltot R Λ 0 Lmond αc 0 c2 K K Lm = R - 2 * Λ + Lm := by unfold Ltot; ring

/-- Static slices (K = <K> = 0): the c_2 term drops; only alpha_c a^2 remains (G renormalisation, L340 H5). -/
theorem static_reduction (R Λ f Lmond αc a2 c2 Lm : ℝ) :
    Ltot R Λ f Lmond αc a2 c2 0 0 Lm = R - 2 * Λ + f * Lmond + αc * a2 + Lm := by unfold Ltot; ring

/-- MOND sector removed (L_MOND = 0, the a0 -> 0 limit of section C) with alpha_c = c_2 = 0: GR + matter. -/
theorem mond_removed_gr (R Λ f a2 K Kb Lm : ℝ) :
    Ltot R Λ f 0 0 a2 0 K Kb Lm = R - 2 * Λ + Lm := by unfold Ltot; ring

/-! ## F. kinetic / principal coefficients -/

/-- L340 tracking speed c_s^2/c^2 = c_2/(C (2 + 3 c_2)) > 0 for c_2 > 0, C > 0. -/
theorem tracking_speed_pos (c2 C : ℝ) (hc : 0 < c2) (hC : 0 < C) : 0 < c2 / (C * (2 + 3 * c2)) := by
  positivity

/-- CFG292 c_S^2 at beta = 0: c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) > 0 for c_2 > 0, 0 < alpha_c < 2. -/
theorem cS2_pos (c2 αc : ℝ) (hc : 0 < c2) (ha : 0 < αc) (ha2 : αc < 2) :
    0 < c2 * (2 - αc) / (αc * (2 + 3 * c2)) := by
  have : 0 < 2 - αc := by linarith
  positivity

/-- ... and fails for alpha_c < 0 (the sign condition CFG292 derives). -/
theorem cS2_neg_of_alpha_neg (c2 αc : ℝ) (hc : 0 < c2) (ha : αc < 0) (hd : 0 < 2 + 3 * c2) :
    c2 * (2 - αc) / (αc * (2 + 3 * c2)) < 0 := by
  have h1 : 0 < c2 * (2 - αc) := by nlinarith
  have h2 : αc * (2 + 3 * c2) < 0 := by nlinarith
  exact div_neg_of_pos_of_neg h1 h2

/-- CFG292 leading-matrix factor alpha (2 + 3 c_2)/(2 alpha - 1) at beta = 0 is nonzero in the window. -/
theorem leading_det_ne (c2 αc : ℝ) (hc : 0 < c2) (ha : 0 < αc) (ha2 : αc < 1 / 2) :
    αc * (2 + 3 * c2) / (2 * αc - 1) ≠ 0 := by
  have : 2 * αc - 1 < 0 := by linarith
  have : 0 < αc * (2 + 3 * c2) := by positivity
  exact div_ne_zero (ne_of_gt this) (by linarith)

/-- CFG329 lapse coefficient (2C + alpha_c (1 + C))/(1 + C) > 0 (elliptic lapse equation). -/
theorem lapse_coeff_pos (C αc : ℝ) (hC : 0 < C) (ha : 0 < αc) : 0 < (2 * C + αc * (1 + C)) / (1 + C) := by
  positivity

/-- CFG337 switch kinetic matrix diag(rho, 1) positive definite (no ghost). -/
theorem switch_kinetic_pos (ρ x y : ℝ) (hρ : 0 < ρ) (hxy : x ≠ 0 ∨ y ≠ 0) : 0 < ρ * x ^ 2 + 1 * y ^ 2 := by
  rcases hxy with h | h
  · have : 0 < x ^ 2 := by positivity
    nlinarith [sq_nonneg y]
  · have : 0 < y ^ 2 := by positivity
    nlinarith [sq_nonneg x]

/-- L340 P1 window: alpha_min = 9.6e-14 < alpha_c < 3.2e-9 and 7.2e-3 < c_2 < 1/15 imply the preferred-frame
bounds |alpha_1| = 4 alpha_c < 1.1e-5, |alpha_2| = alpha_c/2 < 1.6e-9, BBN 1.5 c_2 < 0.1, alpha_c < 1/2, and the
positivity of every coefficient above. -/
theorem P1_window (αc c2 C : ℝ) (ha0 : (96 : ℝ) / 10 ^ 15 < αc) (ha1 : αc < (32 : ℝ) / 10 ^ 10)
    (hc0 : (72 : ℝ) / 10 ^ 4 < c2) (hc1 : c2 < 1 / 15) (hC : 0 < C) :
    4 * αc < (11 : ℝ) / 10 ^ 6 ∧ αc / 2 < (16 : ℝ) / 10 ^ 10 ∧ 3 / 2 * c2 < 1 / 10 ∧
    0 < c2 / (C * (2 + 3 * c2)) ∧ 0 < c2 * (2 - αc) / (αc * (2 + 3 * c2)) ∧
    0 < (2 * C + αc * (1 + C)) / (1 + C) ∧ αc * (2 + 3 * c2) / (2 * αc - 1) ≠ 0 := by
  have ha : 0 < αc := lt_trans (by norm_num) ha0
  have hc : 0 < c2 := lt_trans (by norm_num) hc0
  have hah : αc < 1 / 2 := lt_trans ha1 (by norm_num)
  refine ⟨by linarith, by linarith, by linarith, tracking_speed_pos c2 C hc hC,
    cS2_pos c2 αc hc ha (by linarith), lapse_coeff_pos C αc hC ha, leading_det_ne c2 αc hc ha hah⟩

/-! ## G. kappa = 1/2 and a0 = c^2 sqrt(Lambda/(32 pi)) -/

/-- With rho_Lambda = Lambda c^2/(8 pi G), a0 = kappa c sqrt(G rho_Lambda) at kappa = 1/2 equals
c^2 sqrt(Lambda/(32 pi)). kappa = 1/2 is FITTED; this is an identity, not a derivation. -/
theorem a0_identity (c G Λ : ℝ) (hc : 0 < c) (hG : 0 < G) (hΛ : 0 ≤ Λ) :
    (1 / 2) * c * Real.sqrt (G * (Λ * c ^ 2 / (8 * π * G))) = c ^ 2 * Real.sqrt (Λ / (32 * π)) := by
  have hπ : 0 < π := Real.pi_pos
  have e1 : G * (Λ * c ^ 2 / (8 * π * G)) = c ^ 2 * (4 * (Λ / (32 * π))) := by
    field_simp; ring
  rw [e1, Real.sqrt_mul (by positivity), Real.sqrt_sq (le_of_lt hc), Real.sqrt_mul (by norm_num)]
  have : Real.sqrt 4 = 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [this]; ring

/-- The same identity in the form G rho_Lambda = 4 a0^2/c^2 at kappa = 1/2 (no square roots). -/
theorem a0_identity_sq (c G ρ a0 : ℝ) (hc : 0 < c) (h : a0 = (1 / 2) * c * Real.sqrt (G * ρ)) (hρ : 0 ≤ G * ρ) :
    G * ρ = 4 * a0 ^ 2 / c ^ 2 := by
  rw [h]; field_simp
  rw [Real.sq_sqrt hρ]; ring

end MasterLagrangian

#print axioms MasterLagrangian.nuRAR_tendsto_one
#print axioms MasterLagrangian.deep_mond_limit
#print axioms MasterLagrangian.mono_phantom_strictMono
#print axioms MasterLagrangian.kernel_term_vanishes
#print axioms MasterLagrangian.broken_min
#print axioms MasterLagrangian.switch_off_frw
#print axioms MasterLagrangian.P1_window
#print axioms MasterLagrangian.a0_identity
#print axioms MasterLagrangian.a0_identity_sq
