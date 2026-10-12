import Mathlib

/-!
# CFG665: the GW messenger theorems (photon vs graviton arrival through the framework's own deep-MOND tilt)

Criteria: campaign_fresh_gravity/CFG665_gw_messenger_lean/FROZEN_CRITERIA.md (committed alone, 1bbc63af3).
Source lane: prep_2026/gw170817_check/gw170817_lineintegral.py (photons on g~ = g + B u u, gravitons on g;
|c_gamma - c_gw|/c = 1 - sqrt(1-B); grad|B| = 4 (nu - 1) g_bar / c^2; void boundary condition B -> 0).

CERTIFIED (premises => conclusions; mathematics only):
* T1 `local_lag`: 0 <= B < 1 => B/2 <= 1/sqrt(1-B) - 1.
* T2 `path_delay`: B >= Bmin on [a,b] => Bmin (b-a)/2 <= integral of the lag; `shared_metric_zero`: B = 0 => lag integral = 0.
* T3 `floor_mono`, `floor_sqrt`: for y = g/a0 > 0 and both kernels (nu_mono = 1/2 + sqrt(1/4 + 1/y), nu_sqrt = sqrt(1 + 1/y)),
  (nu - 1) y >= min(sqrt y, 1)/(1 + sqrt 2); `floor_mono_deep`: nu_mono has the sharper deep floor sqrt y / phi.
  `grad_floor`: physical form, (nu - 1) g >= sqrt(a0 G M)/((1 + sqrt 2) s) whenever g >= G M/s^2 and G M/s^2 <= a0.
* T4 `accumulated_tilt`: B continuous on [r1,R], B' <= -K/s inside, B(R) >= 0 => B(r) >= K log(R/r) on [r1,R].
* T5 `no_hiding_direction`: straight sightline from x (|x| >= R2) to the Sun y (|y| <= rs <= R2): some t1 in [0,1] has |p t1| = R2,
  every later point has |p t| <= R2, and the remaining length |y - p t1| >= R2 - rs. Independent of direction.
* T6 `mw_delay_canonical`, `mw_delay_alt`: Milky Way only, M_enc >= 5e10 Msun, shell [10, 110] kpc (100 kpc), void at 300 kpc
  (`log_ratio_ge_one`: log(300/110) >= 1): delay >= 2.3e6 s (canonical a0) and >= 2.5e6 s (alt a0), i.e. >= 1.3e6 x the 1.7 s bound.
* T7 `double_count`: F >= g_bar > 0 => 1 <= (2F - g_bar)/F < 2 (the non-lensing branch counts the law twice; CFG663's x1.8).

NOT certified (premises, stated): the disformal metric and grad|B| = 4(nu-1)g/c^2 (UNIFICATION.md); B non-increasing outward;
curved photon paths (radius 1-Lipschitz in arclength: cited); M_enc >= 5e10 Msun outside 10 kpc (input); the 1.7 s bound itself.
kappa = 1/2 is FITTED; nothing here says the theory is closed or that the data favour it.
-/

namespace CFG665

open Real Set

/-! ## T1: local lag -/

theorem local_lag (B : ℝ) (h0 : 0 ≤ B) (h1 : B < 1) : B / 2 ≤ 1 / Real.sqrt (1 - B) - 1 := by
  set s := Real.sqrt (1 - B) with hsdef
  have hpos : 0 < 1 - B := by linarith
  have hs : 0 < s := Real.sqrt_pos.mpr hpos
  have hs2 : s ^ 2 = 1 - B := Real.sq_sqrt hpos.le
  have hsle : s ≤ 1 := by nlinarith
  have key : (B / 2 + 1) * s ≤ 1 := by nlinarith [sq_nonneg (1 - s), mul_nonneg hs.le (sq_nonneg (1 - s))]
  have : B / 2 + 1 ≤ 1 / s := by rw [le_div_iff₀ hs]; linarith
  linarith

/-! ## T2: path delay -/

/-- the photon lag per unit length -/
noncomputable def lag (B : ℝ) : ℝ := 1 / Real.sqrt (1 - B) - 1

theorem path_delay (B : ℝ → ℝ) (a b Bmin : ℝ) (hab : a ≤ b) (hBmin : 0 ≤ Bmin)
    (hB : ∀ x ∈ Icc a b, Bmin ≤ B x ∧ B x < 1)
    (hint : IntervalIntegrable (fun x => lag (B x)) MeasureTheory.volume a b) :
    Bmin * (b - a) / 2 ≤ ∫ x in a..b, lag (B x) := by
  have hc : IntervalIntegrable (fun _ : ℝ => Bmin / 2) MeasureTheory.volume a b := intervalIntegrable_const
  have hmono := intervalIntegral.integral_mono_on hab hc hint (fun x hx => by
    obtain ⟨h1, h2⟩ := hB x hx
    have := local_lag (B x) (le_trans hBmin h1) h2
    unfold lag; linarith)
  rw [intervalIntegral.integral_const, smul_eq_mul] at hmono
  linarith

theorem shared_metric_zero (a b : ℝ) : ∫ _x in a..b, lag 0 = 0 := by
  simp [lag]

/-! ## T3: kernel floors (dimensionless y = g/a0) -/

noncomputable def nuMono (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)
noncomputable def nuSqrt (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)

theorem floor_sqrt (y : ℝ) (hy : 0 < y) :
    min (Real.sqrt y) 1 / (1 + Real.sqrt 2) ≤ (nuSqrt y - 1) * y := by
  unfold nuSqrt
  set t := Real.sqrt (1 + 1 / y)
  set q := Real.sqrt y
  have h1y : 0 < 1 / y := by positivity
  have ht2 : t ^ 2 = 1 + 1 / y := Real.sq_sqrt (by positivity)
  have ht1 : 1 ≤ t := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_le_sqrt (by linarith)
  have hq2 : q ^ 2 = y := Real.sq_sqrt hy.le
  have hq : 0 < q := Real.sqrt_pos.mpr hy
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r2p : 0 < Real.sqrt 2 := by positivity
  -- (t - 1) y = 1/(t+1)
  have hid : (t - 1) * y * (t + 1) = 1 := by
    have : y * (t ^ 2 - 1) = 1 := by rw [ht2]; field_simp; ring
    nlinarith
  have hden : 0 < 1 + Real.sqrt 2 := by positivity
  rw [div_le_iff₀ hden]
  -- need min(q,1) ≤ (t-1) y (1 + √2); multiply through by (t+1) > 0
  have htp : 0 < t + 1 := by linarith
  have goal' : min q 1 * (t + 1) ≤ 1 + Real.sqrt 2 := by
    rcases le_total q 1 with hq1 | hq1
    · rw [min_eq_left hq1]
      -- q t = sqrt(y + 1) ≤ sqrt 2 since y = q^2 ≤ 1
      have hqt2 : (q * t) ^ 2 = y + 1 := by
        rw [mul_pow, hq2, ht2]; field_simp
      have hqt : q * t ≤ Real.sqrt 2 := by
        have : (q * t) ^ 2 ≤ Real.sqrt 2 ^ 2 := by rw [hqt2, r2]; nlinarith
        nlinarith [mul_pos hq (by linarith : (0:ℝ) < t)]
      nlinarith
    · rw [min_eq_right hq1]
      -- t^2 = 1 + 1/y ≤ 2 since y ≥ 1
      have hy1 : 1 ≤ y := by nlinarith
      have : 1 / y ≤ 1 := by rw [div_le_one hy]; exact hy1
      have : t ≤ Real.sqrt 2 := by nlinarith
      linarith
  have : min q 1 ≤ (t - 1) * y * (1 + Real.sqrt 2) := by
    have e : (t - 1) * y = 1 / (t + 1) := by
      field_simp; linarith [hid]
    rw [e, div_mul_eq_mul_div, one_mul, le_div_iff₀ htp]; exact goal'
  linarith

theorem floor_mono (y : ℝ) (hy : 0 < y) :
    min (Real.sqrt y) 1 / (1 + Real.sqrt 2) ≤ (nuMono y - 1) * y := by
  unfold nuMono
  set t := Real.sqrt (1 / 4 + 1 / y)
  set q := Real.sqrt y
  have h1y : 0 < 1 / y := by positivity
  have ht2 : t ^ 2 = 1 / 4 + 1 / y := Real.sq_sqrt (by positivity)
  have ht0 : 1 / 2 ≤ t := by
    rw [show (1/2:ℝ) = Real.sqrt (1/4) by
      rw [show (1/4:ℝ) = (1/2)^2 by norm_num, Real.sqrt_sq (by norm_num)]]
    exact Real.sqrt_le_sqrt (by linarith)
  have hq2 : q ^ 2 = y := Real.sq_sqrt hy.le
  have hq : 0 < q := Real.sqrt_pos.mpr hy
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r2p : 0 < Real.sqrt 2 := by positivity
  have r2g : 1 < Real.sqrt 2 := by nlinarith
  have hid : (t - 1 / 2) * y * (t + 1 / 2) = 1 := by
    have : y * (t ^ 2 - 1 / 4) = 1 := by rw [ht2]; field_simp; ring
    nlinarith
  have hden : 0 < 1 + Real.sqrt 2 := by positivity
  rw [div_le_iff₀ hden]
  have htp : 0 < t + 1 / 2 := by linarith
  have goal' : min q 1 * (t + 1 / 2) ≤ 1 + Real.sqrt 2 := by
    rcases le_total q 1 with hq1 | hq1
    · rw [min_eq_left hq1]
      -- (q t)^2 = y/4 + 1 ≤ 5/4 < (1/2 + √2)^2 ... use q t ≤ 3/2 ≤ 1/2 + √2
      have hqt2 : (q * t) ^ 2 = y / 4 + 1 := by
        rw [mul_pow, hq2, ht2]; field_simp
      have hy1 : y ≤ 1 := by nlinarith
      have hqt : q * t ≤ 3 / 2 := by
        nlinarith [mul_pos hq (by linarith : (0:ℝ) < t)]
      nlinarith
    · rw [min_eq_right hq1]
      have hy1 : 1 ≤ y := by nlinarith
      have : 1 / y ≤ 1 := by rw [div_le_one hy]; exact hy1
      have : t ≤ 3 / 2 := by nlinarith
      linarith
  have : min q 1 ≤ (t - 1 / 2) * y * (1 + Real.sqrt 2) := by
    have e : (t - 1 / 2) * y = 1 / (t + 1 / 2) := by
      field_simp; linarith [hid]
    rw [e, div_mul_eq_mul_div, one_mul, le_div_iff₀ htp]; exact goal'
  linarith

/-- the sharper deep floor of nu_mono: (nu - 1) y >= sqrt y / phi for 0 < y <= 1 -/
theorem floor_mono_deep (y : ℝ) (hy : 0 < y) (hy1 : y ≤ 1) :
    Real.sqrt y / ((1 + Real.sqrt 5) / 2) ≤ (nuMono y - 1) * y := by
  unfold nuMono
  set t := Real.sqrt (1 / 4 + 1 / y)
  set q := Real.sqrt y
  have ht2 : t ^ 2 = 1 / 4 + 1 / y := Real.sq_sqrt (by positivity)
  have ht0 : 0 ≤ t := Real.sqrt_nonneg _
  have hq2 : q ^ 2 = y := Real.sq_sqrt hy.le
  have hq : 0 < q := Real.sqrt_pos.mpr hy
  have hq1 : q ≤ 1 := by nlinarith
  have r5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have r5p : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg _
  have hid : (t - 1 / 2) * y * (t + 1 / 2) = 1 := by
    have : y * (t ^ 2 - 1 / 4) = 1 := by rw [ht2]; field_simp; ring
    nlinarith
  have hqt2 : (q * t) ^ 2 = y / 4 + 1 := by rw [mul_pow, hq2, ht2]; field_simp
  have hqt : q * t ≤ Real.sqrt 5 / 2 := by
    have : (q * t) ^ 2 ≤ (Real.sqrt 5 / 2) ^ 2 := by rw [hqt2, div_pow, r5]; nlinarith
    nlinarith [mul_nonneg hq.le ht0]
  have htp : 0 < t + 1 / 2 := by linarith
  have hphi : 0 < (1 + Real.sqrt 5) / 2 := by positivity
  have e : (t - 1 / 2) * y = 1 / (t + 1 / 2) := by field_simp; linarith [hid]
  rw [show 1 / 2 + t - 1 = t - 1 / 2 by ring, e, div_le_div_iff₀ hphi htp]
  nlinarith

/-- physical form of the floor (both kernels): g >= G M / s^2 and G M / s^2 <= a0 =>
    (nu(g/a0) - 1) g >= sqrt(a0 G M) / ((1 + sqrt 2) s). Written for a generic kernel obeying the T3 floor. -/
theorem grad_floor (nu : ℝ → ℝ) (hfloor : ∀ y, 0 < y → min (Real.sqrt y) 1 / (1 + Real.sqrt 2) ≤ (nu y - 1) * y)
    (a0 GM s g : ℝ) (ha : 0 < a0) (hGM : 0 < GM) (hs : 0 < s)
    (hg : GM / s ^ 2 ≤ g) (hdeep : GM / s ^ 2 ≤ a0) :
    Real.sqrt (a0 * GM) / ((1 + Real.sqrt 2) * s) ≤ (nu (g / a0) - 1) * g := by
  have hgp : 0 < g := lt_of_lt_of_le (by positivity) hg
  have hy : 0 < g / a0 := by positivity
  have hf := hfloor (g / a0) hy
  -- min(sqrt(g/a0), 1) >= sqrt(GM/(s^2 a0))
  set y0 := GM / s ^ 2 / a0 with hy0
  have hy0le1 : y0 ≤ 1 := by rw [hy0, div_le_one ha]; exact hdeep
  have hy0le : y0 ≤ g / a0 := by rw [hy0]; exact div_le_div_of_nonneg_right hg ha.le
  have hmin : Real.sqrt y0 ≤ min (Real.sqrt (g / a0)) 1 := by
    apply le_min (Real.sqrt_le_sqrt hy0le)
    rw [show (1:ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_le_sqrt hy0le1
  have hsq : Real.sqrt (a0 * GM) / s = a0 * Real.sqrt y0 := by
    rw [hy0, eq_comm, show GM / s ^ 2 / a0 = (a0 * GM) / (a0 * s) ^ 2 by field_simp,
      Real.sqrt_div' _ (by positivity : (0:ℝ) ≤ (a0 * s) ^ 2), Real.sqrt_sq (by positivity)]
    field_simp
  have hden : 0 < 1 + Real.sqrt 2 := by positivity
  calc Real.sqrt (a0 * GM) / ((1 + Real.sqrt 2) * s)
      = a0 * (Real.sqrt y0 / (1 + Real.sqrt 2)) := by
        rw [mul_comm (1 + Real.sqrt 2) s, ← div_div, hsq]; ring
    _ ≤ a0 * (min (Real.sqrt (g / a0)) 1 / (1 + Real.sqrt 2)) := by
        gcongr
    _ ≤ a0 * ((nu (g / a0) - 1) * (g / a0)) := by gcongr
    _ = (nu (g / a0) - 1) * g := by field_simp

/-! ## T4: accumulated tilt -/

theorem accumulated_tilt (B B' : ℝ → ℝ) (K r1 R : ℝ) (hK : 0 < K) (hr1 : 0 < r1) (hr : r1 < R)
    (hcont : ContinuousOn B (Icc r1 R))
    (hderiv : ∀ s ∈ Ioo r1 R, HasDerivAt B (B' s) s)
    (hslope : ∀ s ∈ Ioo r1 R, B' s ≤ -K / s)
    (hR : 0 ≤ B R) :
    ∀ r ∈ Icc r1 R, K * Real.log (R / r) ≤ B r := by
  intro r hr'
  let h : ℝ → ℝ := fun s => B s + K * Real.log s
  have hpos : ∀ s ∈ Icc r1 R, 0 < s := fun s hs => lt_of_lt_of_le hr1 hs.1
  have hhcont : ContinuousOn h (Icc r1 R) := by
    apply hcont.add
    apply ContinuousOn.mul continuousOn_const
    exact Real.continuousOn_log.mono (fun s hs => ne_of_gt (hpos s hs))
  have hhder : ∀ s ∈ Ioo r1 R, HasDerivAt h (B' s + K * s⁻¹) s := by
    intro s hs
    have hs0 : s ≠ 0 := ne_of_gt (lt_trans hr1 hs.1)
    exact (hderiv s hs).add ((Real.hasDerivAt_log hs0).const_mul K)
  have hanti : AntitoneOn h (Icc r1 R) := by
    apply antitoneOn_of_deriv_nonpos (convex_Icc r1 R) hhcont
    · rw [interior_Icc]; intro s hs; exact (hhder s hs).differentiableAt.differentiableWithinAt
    · rw [interior_Icc]; intro s hs
      rw [(hhder s hs).deriv]
      have hsp : 0 < s := lt_trans hr1 hs.1
      have := hslope s hs
      have e : -K / s = -(K * s⁻¹) := by rw [neg_div, div_eq_mul_inv]
      linarith
  have hRmem : R ∈ Icc r1 R := ⟨hr.le, le_rfl⟩
  have hle := hanti hr' hRmem hr'.2
  have hrp := hpos r hr'
  have hRp : 0 < R := lt_trans hr1 hr
  simp only [h] at hle
  rw [Real.log_div hRp.ne' hrp.ne']
  nlinarith

/-! ## T5: no hiding sky direction -/

theorem no_hiding_direction (x y : EuclideanSpace ℝ (Fin 3)) (R2 rs : ℝ)
    (hx : R2 ≤ ‖x‖) (hy : ‖y‖ ≤ rs) (hrs : rs ≤ R2) :
    ∃ t1 ∈ Icc (0:ℝ) 1,
      ‖x + t1 • (y - x)‖ = R2 ∧
      (∀ t ∈ Icc t1 1, ‖x + t • (y - x)‖ ≤ R2) ∧
      R2 - rs ≤ ‖y - (x + t1 • (y - x))‖ := by
  let p : ℝ → EuclideanSpace ℝ (Fin 3) := fun t => x + t • (y - x)
  have hpc : Continuous fun t => ‖p t‖ := by fun_prop
  have h0 : ‖p 0‖ = ‖x‖ := by simp [p]
  have h1 : ‖p 1‖ = ‖y‖ := by simp [p]
  -- IVT on [0,1] (values go from >= R2 down to <= rs <= R2)
  have hivt : R2 ∈ Icc (‖p 1‖) (‖p 0‖) := ⟨by rw [h1]; linarith, by rw [h0]; exact hx⟩
  obtain ⟨t1, ht1, hpt1⟩ :=
    intermediate_value_Icc' (zero_le_one) hpc.continuousOn hivt
  refine ⟨t1, ht1, hpt1, ?_, ?_⟩
  · -- convexity of the norm along the line: for t in [t1,1], p t is a convex combination of p t1 and p 1
    intro t ht
    by_cases hte : t1 = 1
    · have : t = 1 := le_antisymm ht.2 (hte ▸ ht.1)
      subst this; rw [← hpt1, hte]
    have hlt : t1 < 1 := lt_of_le_of_ne ht1.2 hte
    set w := (t - t1) / (1 - t1)
    have hw0 : 0 ≤ w := div_nonneg (by linarith [ht.1]) (by linarith)
    have hw1 : w ≤ 1 := by rw [div_le_one (by linarith)]; linarith [ht.2]
    have hcomb : p t = (1 - w) • p t1 + w • p 1 := by
      simp only [p]
      have : t = (1 - w) * t1 + w * 1 := by
        simp only [w]; field_simp; ring
      rw [this]; module
    calc ‖p t‖ = ‖(1 - w) • p t1 + w • p 1‖ := by rw [hcomb]
      _ ≤ ‖(1 - w) • p t1‖ + ‖w • p 1‖ := norm_add_le _ _
      _ = (1 - w) * ‖p t1‖ + w * ‖p 1‖ := by
          rw [norm_smul, norm_smul, Real.norm_of_nonneg (by linarith), Real.norm_of_nonneg hw0]
      _ ≤ (1 - w) * R2 + w * R2 := by
          have e1 : ‖p t1‖ = R2 := hpt1
          rw [e1, h1]; gcongr; linarith
      _ = R2 := by ring
  · have := norm_sub_norm_le (x + t1 • (y - x)) y
    rw [norm_sub_rev] at this
    have e : ‖x + t1 • (y - x)‖ = R2 := hpt1
    linarith

/-! ## T6: Milky Way numeric corollary (both footings) -/

/-- log(300/110) >= 1, i.e. the shell out to 110 kpc keeps B >= K under a void at 300 kpc -/
theorem log_ratio_ge_one : 1 ≤ Real.log (300 / 110) := by
  rw [Real.le_log_iff_exp_le (by norm_num)]
  have := Real.exp_one_lt_d9
  norm_num at this ⊢; linarith

/-- the delay bound Dt >= K L /(2c), K = 4 sqrt(a0 G M)/((1+sqrt2) c^2), with conservative inputs:
    G >= 6.674e-11, Msun >= 1.988e30, M_enc >= 5e10 Msun, L = 100 kpc >= 3.0856e21 m, c = 2.99792458e8. -/
noncomputable def delayLo (a0 : ℝ) : ℝ :=
  4 * Real.sqrt (a0 * (6.674e-11 * (5e10 * 1.988e30))) / ((1 + Real.sqrt 2) * 2.99792458e8 ^ 2)
    * 3.0856e21 / (2 * 2.99792458e8)

theorem sqrt2_le : Real.sqrt 2 ≤ 1.4143 := by
  rw [Real.sqrt_le_left (by norm_num)]; norm_num

theorem mw_delay_generic (a0 slo : ℝ) (hslo : 0 ≤ slo) (hsq : slo ^ 2 ≤ a0 * (6.674e-11 * (5e10 * 1.988e30))) :
    4 * slo / (2.4143 * 2.99792458e8 ^ 2) * 3.0856e21 / (2 * 2.99792458e8) ≤ delayLo a0 := by
  unfold delayLo
  have hs : slo ≤ Real.sqrt (a0 * (6.674e-11 * (5e10 * 1.988e30))) := Real.le_sqrt_of_sq_le hsq
  have h2 := sqrt2_le
  have h2p : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hd : (1 + Real.sqrt 2) * 2.99792458e8 ^ 2 ≤ 2.4143 * 2.99792458e8 ^ 2 := by nlinarith
  have hdp : 0 < (1 + Real.sqrt 2) * (2.99792458e8:ℝ) ^ 2 := by positivity
  have step : 4 * slo / (2.4143 * 2.99792458e8 ^ 2) ≤
      4 * Real.sqrt (a0 * (6.674e-11 * (5e10 * 1.988e30))) / ((1 + Real.sqrt 2) * 2.99792458e8 ^ 2) := by
    calc 4 * slo / (2.4143 * 2.99792458e8 ^ 2) ≤ 4 * slo / ((1 + Real.sqrt 2) * 2.99792458e8 ^ 2) :=
          div_le_div_of_nonneg_left (by positivity) hdp hd
      _ ≤ _ := by gcongr
  have := mul_le_mul_of_nonneg_right step (by norm_num : (0:ℝ) ≤ 3.0856e21)
  exact div_le_div_of_nonneg_right this (by norm_num)

theorem mw_delay_canonical : 2.3e6 ≤ delayLo 9.3603e-11 := by
  refine le_trans ?_ (mw_delay_generic 9.3603e-11 2.49e10 (by norm_num) (by norm_num))
  norm_num

theorem mw_delay_alt : 2.5e6 ≤ delayLo 1.1312e-10 := by
  refine le_trans ?_ (mw_delay_generic 1.1312e-10 2.739e10 (by norm_num) (by norm_num))
  norm_num

/-- ratio to the GW170817 arrival bound (1.7 s), both footings -/
theorem mw_ratio : 1.3e6 * 1.7 ≤ delayLo 9.3603e-11 ∧ 1.3e6 * 1.7 ≤ delayLo 1.1312e-10 := by
  constructor
  · exact le_trans (by norm_num) mw_delay_canonical
  · exact le_trans (by norm_num) mw_delay_alt

/-! ## T7: CFG663 double count -/

theorem double_count (F gb : ℝ) (hgb : 0 < gb) (hF : gb ≤ F) :
    1 ≤ (2 * F - gb) / F ∧ (2 * F - gb) / F < 2 := by
  have hFp : 0 < F := lt_of_lt_of_le hgb hF
  constructor
  · rw [le_div_iff₀ hFp]; linarith
  · rw [div_lt_iff₀ hFp]; linarith

end CFG665

#print axioms CFG665.local_lag
#print axioms CFG665.path_delay
#print axioms CFG665.shared_metric_zero
#print axioms CFG665.floor_sqrt
#print axioms CFG665.floor_mono
#print axioms CFG665.floor_mono_deep
#print axioms CFG665.grad_floor
#print axioms CFG665.accumulated_tilt
#print axioms CFG665.no_hiding_direction
#print axioms CFG665.log_ratio_ge_one
#print axioms CFG665.mw_delay_canonical
#print axioms CFG665.mw_delay_alt
#print axioms CFG665.mw_ratio
#print axioms CFG665.double_count
