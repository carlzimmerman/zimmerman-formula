import Mathlib
import ChainCert.Certificates
import ChainCert.Kernel

/-!
# ChainCert.CalibrationWall -- the baryon-calibration wall (CFG240), as implications from declared premises

WHAT LEAN CERTIFIES HERE, AND WHAT IT DOES NOT.
CERTIFIED (premises => conclusions): for the DECLARED law `g_obs = (f g) nu((f g)/a0)` (`gObs`: f > 0 is one multiplicative
calibration of g_bar, the same f and a0 at every point), (T1) the deep-regime law, its dependence on (f, a0) only through f*a0,
the exact P2 identity g_obs^2 = f^2 g^2 + (f a0) g with the exact relative-difference bound between equal-product pairs, and the
asymptotic form of the wall for ANY kernel with C2's deep premise; (T2) exact two-point injectivity of (f, a0) for P2, its failure
at one point and for the deep kernel, a kernel-general two-point injectivity from strict convexity of log(e^u nu(e^u)), proved
for P2 and for nu_mono; the closed-form Jacobian (rows (1 - b, b), determinant b(y2) - b(y1)) and its degeneration; (T3) the
Newtonian limit; (T4) a design bound on the Fisher matrix, sigma(log a0) >= 3 sigma / sqrt(N) with f free.
NOT CERTIFIED: that a calibration factor f exists in any survey, its size, its redshift dependence, that a0 is the same for all
points, that nature follows P2 or nu_mono, any statistical statement beyond the algebra of the Fisher matrix as defined here
(the numeric companion campaign_fresh_gravity/CFG240_calibration_wall computes it; Lean does not), any other systematic
(selection, mass-to-light, gas, non-circular motion), non-multiplicative calibrations (offsets, g-dependent f), and kappa
(= 1/2 is FITTED). Lean has no data and says nothing about whether the wall binds any real sample: the wall is a statement about
what the declared law CAN identify.

Notation: s = log f, t = log a0, y = f g/a0 at the TRUE (f, a0) (the argument fed to nu), b(y) = 1 - d log(y nu(y))/d log y.
P2: b = 1/(2(1+y)); nu_mono: b = sqrt(y)/(2(exp(sqrt y) - 1)).  Fisher rows (1 - b_i, b_i) in (log f, log a0).
-/

open Filter Topology

namespace CalibrationWall

/-- the P2 kernel (the record's kernel; equals `nuBeta 1` for y > 0, `nuP2_eq_nuBeta`) -/
noncomputable def nuP2 (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)
/-- the deep-MOND kernel nu y = 1 / sqrt y -/
noncomputable def nuDeep (y : ℝ) : ℝ := 1 / Real.sqrt y
/-- observed acceleration when g_bar is mis-calibrated by f: g_obs = (f g) nu(f g / a0) -/
noncomputable def gObs (ν : ℝ → ℝ) (f a0 g : ℝ) : ℝ := (f * g) * ν (f * g / a0)
/-- y at the TRUE (f, a0) = (e^s, e^t): the argument actually fed to nu -/
noncomputable def yOf (s t g : ℝ) : ℝ := Real.exp s * g / Real.exp t

theorem nuP2_eq_nuBeta {y : ℝ} (hy : 0 < y) : nuP2 y = nuBeta 1 y :=
  (C2_nuBeta_one y hy).symm

theorem T1_deep_law {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    gObs nuDeep f a0 g = Real.sqrt (f * a0 * g) := by
  have hx : 0 < f * g := mul_pos hf hg
  have hsx : 0 < Real.sqrt (f * g) := Real.sqrt_pos.mpr hx
  have hsa : 0 < Real.sqrt a0 := Real.sqrt_pos.mpr ha
  have e : f * a0 * g = (f * g) * a0 := by ring
  unfold gObs nuDeep
  rw [Real.sqrt_div hx.le, e, Real.sqrt_mul hx.le]
  have h2 : Real.sqrt (f * g) * Real.sqrt (f * g) = f * g := Real.mul_self_sqrt hx.le
  field_simp
  nlinarith [h2]

theorem T1_deep_equal_products {f a0 f' a0' g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg : 0 < g) (hp : f * a0 = f' * a0') :
    gObs nuDeep f a0 g = gObs nuDeep f' a0' g := by
  rw [T1_deep_law hf ha hg, T1_deep_law hf' ha' hg, hp]

theorem T1_deep_iff {f a0 f' a0' : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f') (ha' : 0 < a0') :
    (∀ g : ℝ, 0 < g → gObs nuDeep f a0 g = gObs nuDeep f' a0' g) ↔ f * a0 = f' * a0' := by
  constructor
  · intro h
    have := h 1 one_pos
    rw [T1_deep_law hf ha one_pos, T1_deep_law hf' ha' one_pos] at this
    have h1 : 0 ≤ f * a0 * 1 := by positivity
    have h2 : 0 ≤ f' * a0' * 1 := by positivity
    have := (Real.sqrt_inj h1 h2).mp this
    linarith
  · intro h g hg
    exact T1_deep_equal_products hf ha hf' ha' hg h

theorem T1_deep_drift {f a0 c g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hc : 0 < c) (hg : 0 < g) :
    gObs nuDeep (c * f) a0 g = Real.sqrt c * gObs nuDeep f a0 g ∧
    gObs nuDeep f (c * a0) g = Real.sqrt c * gObs nuDeep f a0 g ∧
    Real.log (gObs nuDeep (c * f) a0 g) = Real.log (gObs nuDeep f a0 g) + Real.log c / 2 ∧
    Real.log (gObs nuDeep f (c * a0) g) = Real.log (gObs nuDeep f a0 g) + Real.log c / 2 := by
  have hcf : 0 < c * f := mul_pos hc hf
  have hca : 0 < c * a0 := mul_pos hc ha
  have hX : 0 < f * a0 * g := by positivity
  have e1 : c * f * a0 * g = c * (f * a0 * g) := by ring
  have e2 : f * (c * a0) * g = c * (f * a0 * g) := by ring
  have s1 : gObs nuDeep (c * f) a0 g = Real.sqrt c * gObs nuDeep f a0 g := by
    rw [T1_deep_law hcf ha hg, T1_deep_law hf ha hg, e1, Real.sqrt_mul hc.le]
  have s2 : gObs nuDeep f (c * a0) g = Real.sqrt c * gObs nuDeep f a0 g := by
    rw [T1_deep_law hf hca hg, T1_deep_law hf ha hg, e2, Real.sqrt_mul hc.le]
  have hs : 0 < Real.sqrt c := Real.sqrt_pos.mpr hc
  have hpos : 0 < gObs nuDeep f a0 g := by
    rw [T1_deep_law hf ha hg]; exact Real.sqrt_pos.mpr hX
  have lg : Real.log (Real.sqrt c * gObs nuDeep f a0 g) =
      Real.log (gObs nuDeep f a0 g) + Real.log c / 2 := by
    rw [Real.log_mul hs.ne' hpos.ne', Real.log_sqrt hc.le]; ring
  refine ⟨s1, s2, ?_, ?_⟩
  · rw [s1, lg]
  · rw [s2, lg]

theorem gObs_nuP2_pos {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    0 < gObs nuP2 f a0 g := by
  unfold gObs nuP2
  have : 0 < 1 + 1 / (f * g / a0) := by positivity
  exact mul_pos (mul_pos hf hg) (Real.sqrt_pos.mpr this)

theorem P2_sq {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    gObs nuP2 f a0 g ^ 2 = f ^ 2 * g ^ 2 + (f * a0) * g := by
  unfold gObs nuP2
  have hx : 0 < f * g := mul_pos hf hg
  have h0 : (0:ℝ) ≤ 1 + 1 / (f * g / a0) := by positivity
  rw [mul_pow, Real.sq_sqrt h0]
  field_simp

theorem P2_sq_y {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    gObs nuP2 f a0 g ^ 2 = (f * a0) * g * (1 + f * g / a0) := by
  rw [P2_sq hf ha hg]
  field_simp
  ring

theorem T1_P2_ratio {f a0 f' a0' g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg : 0 < g) (hp : f * a0 = f' * a0') :
    gObs nuP2 f' a0' g ^ 2 * (f ^ 2 * g + f * a0) = gObs nuP2 f a0 g ^ 2 * (f' ^ 2 * g + f * a0) := by
  rw [P2_sq hf' ha' hg, P2_sq hf ha hg, ← hp]
  ring

theorem T1_P2_bound {f a0 f' a0' g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg : 0 < g) (hp : f * a0 = f' * a0') :
    |gObs nuP2 f' a0' g ^ 2 - gObs nuP2 f a0 g ^ 2| * (f * a0) ≤
      |f' ^ 2 - f ^ 2| * g * gObs nuP2 f a0 g ^ 2 := by
  have e : gObs nuP2 f' a0' g ^ 2 - gObs nuP2 f a0 g ^ 2 = (f' ^ 2 - f ^ 2) * g ^ 2 := by
    rw [P2_sq hf' ha' hg, P2_sq hf ha hg, ← hp]; ring
  rw [e, abs_mul, abs_of_nonneg (sq_nonneg g), P2_sq hf ha hg]
  have h1 : g ^ 2 * (f * a0) ≤ g * (f ^ 2 * g ^ 2 + f * a0 * g) := by
    nlinarith [mul_pos (mul_pos hf hf) (pow_pos hg 3), mul_pos hf ha, sq_nonneg g]
  calc |f' ^ 2 - f ^ 2| * g ^ 2 * (f * a0) = |f' ^ 2 - f ^ 2| * (g ^ 2 * (f * a0)) := by ring
    _ ≤ |f' ^ 2 - f ^ 2| * (g * (f ^ 2 * g ^ 2 + f * a0 * g)) :=
        mul_le_mul_of_nonneg_left h1 (abs_nonneg _)
    _ = |f' ^ 2 - f ^ 2| * g * (f ^ 2 * g ^ 2 + f * a0 * g) := by ring

theorem T1_general_limit (ν : ℝ → ℝ) (hν : Tendsto (fun y : ℝ => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1))
    {f a0 : ℝ} (hf : 0 < f) (ha : 0 < a0) :
    Tendsto (fun g : ℝ => gObs ν f a0 g / Real.sqrt (f * a0 * g)) (𝓝[>] 0) (𝓝 1) := by
  have hy : Tendsto (fun g : ℝ => f * g / a0) (𝓝[>] 0) (𝓝[>] 0) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨?_, ?_⟩
    · have hc : Continuous (fun g : ℝ => f * g / a0) := by fun_prop
      have := (hc.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0:ℝ)))
      simpa using this
    · filter_upwards [self_mem_nhdsWithin] with g hg
      have : 0 < g := hg
      have h0 : 0 < f * g / a0 := by positivity
      exact h0
  refine (hν.comp hy).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with g hg
  have hg' : 0 < g := hg
  have hy0 : 0 < f * g / a0 := by positivity
  have e : f * a0 * g = a0 ^ 2 * (f * g / a0) := by field_simp
  have hsq : Real.sqrt (f * a0 * g) = a0 * Real.sqrt (f * g / a0) := by
    rw [e, Real.sqrt_mul (sq_nonneg a0), Real.sqrt_sq ha.le]
  have hs : 0 < Real.sqrt (f * g / a0) := Real.sqrt_pos.mpr hy0
  have hss : Real.sqrt (f * g / a0) * Real.sqrt (f * g / a0) = f * g / a0 :=
    Real.mul_self_sqrt hy0.le
  simp only [Function.comp, gObs]
  rw [hsq, eq_div_iff (mul_pos ha hs).ne']
  rw [show ν (f * g / a0) * Real.sqrt (f * g / a0) * (a0 * Real.sqrt (f * g / a0)) =
      a0 * ν (f * g / a0) * (Real.sqrt (f * g / a0) * Real.sqrt (f * g / a0)) by ring, hss]
  field_simp

theorem T1_general_equal_products_limit (ν : ℝ → ℝ)
    (hν : Tendsto (fun y : ℝ => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1))
    {f a0 f' a0' : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f') (ha' : 0 < a0') (hp : f * a0 = f' * a0') :
    Tendsto (fun g : ℝ => gObs ν f' a0' g / gObs ν f a0 g) (𝓝[>] 0) (𝓝 1) := by
  have h1 := T1_general_limit ν hν hf ha
  have h2 := T1_general_limit ν hν hf' ha'
  have := h2.div h1 one_ne_zero
  rw [div_one] at this
  refine this.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with g hg
  have hg' : 0 < g := hg
  have hX : 0 < f * a0 * g := by positivity
  have hs : Real.sqrt (f * a0 * g) ≠ 0 := (Real.sqrt_pos.mpr hX).ne'
  simp only [Pi.div_apply]
  rw [show f' * a0' * g = f * a0 * g by rw [hp]]
  rw [div_div_div_cancel_right₀ hs]

theorem nuP2_deep : Tendsto (fun y : ℝ => nuP2 y * Real.sqrt y) (𝓝[>] 0) (𝓝 1) := by
  have h : Tendsto (fun y : ℝ => Real.sqrt (y + 1)) (𝓝[>] 0) (𝓝 1) := by
    have hc : Continuous (fun y : ℝ => Real.sqrt (y + 1)) := by fun_prop
    have := (hc.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0:ℝ)))
    simpa using this
  refine h.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with y hy
  have hy' : 0 < y := hy
  unfold nuP2
  rw [← Real.sqrt_mul (by positivity)]
  congr 1
  field_simp

theorem T1_P2_limit {f a0 f' a0' : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hp : f * a0 = f' * a0') :
    Tendsto (fun g : ℝ => gObs nuP2 f' a0' g / gObs nuP2 f a0 g) (𝓝[>] 0) (𝓝 1) :=
  T1_general_equal_products_limit nuP2 nuP2_deep hf ha hf' ha' hp

theorem T2a_inversion {f a0 g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg1 : 0 < g1) (hg2 : 0 < g2) :
    gObs nuP2 f a0 g1 ^ 2 / g1 - gObs nuP2 f a0 g2 ^ 2 / g2 = f ^ 2 * (g1 - g2) := by
  rw [P2_sq hf ha hg1, P2_sq hf ha hg2]
  field_simp
  ring

theorem T2a_P2_injective {f a0 f' a0' g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg1 : 0 < g1) (hg2 : 0 < g2) (hne : g1 ≠ g2)
    (h1 : gObs nuP2 f a0 g1 = gObs nuP2 f' a0' g1) (h2 : gObs nuP2 f a0 g2 = gObs nuP2 f' a0' g2) :
    f = f' ∧ a0 = a0' := by
  have e1 := P2_sq hf ha hg1
  have e1' := P2_sq hf' ha' hg1
  have e2 := P2_sq hf ha hg2
  have e2' := P2_sq hf' ha' hg2
  rw [h1] at e1; rw [h2] at e2
  have k1 : f^2*g1^2 + f*a0*g1 = f'^2*g1^2 + f'*a0'*g1 := by rw [← e1, ← e1']
  have k2 : f^2*g2^2 + f*a0*g2 = f'^2*g2^2 + f'*a0'*g2 := by rw [← e2, ← e2']
  have d1 : f^2*g1 + f*a0 = f'^2*g1 + f'*a0' :=
    mul_left_cancel₀ hg1.ne' (show g1 * (f^2*g1 + f*a0) = g1 * (f'^2*g1 + f'*a0') by nlinarith)
  have d2 : f^2*g2 + f*a0 = f'^2*g2 + f'*a0' :=
    mul_left_cancel₀ hg2.ne' (show g2 * (f^2*g2 + f*a0) = g2 * (f'^2*g2 + f'*a0') by nlinarith)
  have hsq : f^2 = f'^2 := by
    have : (f^2 - f'^2) * (g1 - g2) = 0 := by nlinarith
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · exact absurd (by linarith) hne
  have hff : f = f' := by nlinarith [sq_nonneg (f - f'), mul_pos hf hf']
  subst hff
  refine ⟨rfl, ?_⟩
  have : f * a0 = f * a0' := by nlinarith
  exact mul_left_cancel₀ hf.ne' this

theorem T2a_one_point_fails {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    ∃ f' a0' : ℝ, 0 < f' ∧ 0 < a0' ∧ f' ≠ f ∧ gObs nuP2 f' a0' g = gObs nuP2 f a0 g := by
  have hf' : 0 < f / 2 := by positivity
  have ha' : 0 < 3 / 2 * f * g + 2 * a0 := by positivity
  refine ⟨f / 2, 3 / 2 * f * g + 2 * a0, hf', ha', ?_, ?_⟩
  · intro h; linarith
  · have p1 := gObs_nuP2_pos hf' ha' hg
    have p2 := gObs_nuP2_pos hf ha hg
    have hsq : gObs nuP2 (f / 2) (3 / 2 * f * g + 2 * a0) g ^ 2 = gObs nuP2 f a0 g ^ 2 := by
      rw [P2_sq hf' ha' hg, P2_sq hf ha hg]; ring
    exact (sq_eq_sq₀ p1.le p2.le).mp hsq

theorem T2b_deep_not_injective :
    ∃ f a0 f' a0' : ℝ, 0 < f ∧ 0 < a0 ∧ 0 < f' ∧ 0 < a0' ∧ f ≠ f' ∧
      ∀ g : ℝ, 0 < g → gObs nuDeep f a0 g = gObs nuDeep f' a0' g := by
  refine ⟨1, 1, 2, 1 / 2, one_pos, one_pos, two_pos, by norm_num, by norm_num, ?_⟩
  intro g hg
  exact T1_deep_equal_products one_pos one_pos two_pos (by norm_num) hg (by norm_num)


/-! ## T2c: the conditioning (P2) -/

noncomputable def dlogf (y : ℝ) : ℝ := (1 + 2 * y) / (2 * (1 + y))
noncomputable def dloga (y : ℝ) : ℝ := 1 / (2 * (1 + y))

/-- log g_obs for P2 as a sum, with f = e^s, a0 = e^t -/
theorem log_gObs_nuP2 (s t g : ℝ) (hg : 0 < g) :
    Real.log (gObs nuP2 (Real.exp s) (Real.exp t) g) =
      (s + Real.log g + Real.log (Real.exp s * g + Real.exp t)) / 2 := by
  have hf := Real.exp_pos s
  have ha := Real.exp_pos t
  have hsq := P2_sq hf ha hg
  have hpos := gObs_nuP2_pos hf ha hg
  have h1 : gObs nuP2 (Real.exp s) (Real.exp t) g =
      Real.sqrt (Real.exp s * g * (Real.exp s * g + Real.exp t)) := by
    rw [← Real.sqrt_sq hpos.le, hsq]; congr 1; ring
  rw [h1, Real.log_sqrt (by positivity), Real.log_mul (by positivity) (by positivity),
    Real.log_mul (Real.exp_pos s).ne' hg.ne', Real.log_exp]

theorem T2c_dlogf (s t g : ℝ) (hg : 0 < g) :
    HasDerivAt (fun s' : ℝ => Real.log (gObs nuP2 (Real.exp s') (Real.exp t) g))
      (dlogf (yOf s t g)) s := by
  have hfun : (fun s' : ℝ => Real.log (gObs nuP2 (Real.exp s') (Real.exp t) g)) =
      fun s' => (s' + Real.log g + Real.log (Real.exp s' * g + Real.exp t)) / 2 := by
    funext s'; exact log_gObs_nuP2 s' t g hg
  rw [hfun]
  have hpos : 0 < Real.exp s * g + Real.exp t := by positivity
  have h1 : HasDerivAt (fun s' : ℝ => Real.exp s' * g + Real.exp t) (Real.exp s * g) s := by
    simpa using ((Real.hasDerivAt_exp s).mul_const g).add_const (Real.exp t)
  have h2 := h1.log hpos.ne'
  have h3 := ((hasDerivAt_id s).add_const (Real.log g)).add h2
  have h4 := h3.div_const 2
  refine h4.congr_deriv ?_
  unfold dlogf yOf
  have he := Real.exp_pos t
  field_simp
  ring

theorem T2c_dloga (s t g : ℝ) (hg : 0 < g) :
    HasDerivAt (fun t' : ℝ => Real.log (gObs nuP2 (Real.exp s) (Real.exp t') g))
      (dloga (yOf s t g)) t := by
  have hfun : (fun t' : ℝ => Real.log (gObs nuP2 (Real.exp s) (Real.exp t') g)) =
      fun t' => (s + Real.log g + Real.log (Real.exp s * g + Real.exp t')) / 2 := by
    funext t'; exact log_gObs_nuP2 s t' g hg
  rw [hfun]
  have hpos : 0 < Real.exp s * g + Real.exp t := by positivity
  have h1 : HasDerivAt (fun t' : ℝ => Real.exp s * g + Real.exp t') (Real.exp t) t :=
    (Real.hasDerivAt_exp t).const_add (Real.exp s * g)
  have h2 := h1.log hpos.ne'
  have h3 : HasDerivAt (fun t' : ℝ => s + Real.log g + Real.log (Real.exp s * g + Real.exp t'))
      (Real.exp t / (Real.exp s * g + Real.exp t)) t := by
    simpa using h2.const_add (s + Real.log g)
  have h4 := h3.div_const 2
  refine h4.congr_deriv ?_
  unfold dloga yOf
  have he := Real.exp_pos t
  field_simp
  ring

theorem T2c_rows {y : ℝ} (hy : 0 < y) : dlogf y = 1 - dloga y := by
  unfold dlogf dloga
  field_simp
  ring

theorem T2c_det {y1 y2 : ℝ} (h1 : 0 < y1) (h2 : 0 < y2) :
    dlogf y1 * dloga y2 - dloga y1 * dlogf y2 = (y1 - y2) / (2 * (1 + y1) * (1 + y2)) ∧
    dlogf y1 * dloga y2 - dloga y1 * dlogf y2 = (1 / (1 + y2) - 1 / (1 + y1)) / 2 := by
  unfold dlogf dloga
  constructor <;> (field_simp; ring)

theorem T2c_det_ne_zero_iff {y1 y2 : ℝ} (h1 : 0 < y1) (h2 : 0 < y2) :
    dlogf y1 * dloga y2 - dloga y1 * dlogf y2 ≠ 0 ↔ y1 ≠ y2 := by
  rw [(T2c_det h1 h2).1]
  have hd : 2 * (1 + y1) * (1 + y2) ≠ 0 := by positivity
  rw [div_ne_zero_iff, sub_ne_zero]
  simp [hd]

theorem T2c_det_bounds {y1 y2 : ℝ} (h1 : 0 < y1) (h2 : 0 < y2) :
    |dlogf y1 * dloga y2 - dloga y1 * dlogf y2| ≤ |y1 - y2| / 2 ∧
    |dlogf y1 * dloga y2 - dloga y1 * dlogf y2| ≤ 1 / (2 * (1 + min y1 y2)) ∧
    |dlogf y1 * dloga y2 - dloga y1 * dlogf y2| < 1 / 2 := by
  have hq1 : 0 < 1 / (1 + y1) := by positivity
  have hq2 : 0 < 1 / (1 + y2) := by positivity
  have hq1' : 1 / (1 + y1) < 1 := by rw [div_lt_one (by positivity)]; linarith
  have hq2' : 1 / (1 + y2) < 1 := by rw [div_lt_one (by positivity)]; linarith
  refine ⟨?_, ?_, ?_⟩
  · rw [(T2c_det h1 h2).1, abs_div, abs_mul, abs_mul, abs_of_pos (by norm_num : (0:ℝ) < 2),
      abs_of_pos (by linarith : (0:ℝ) < 1 + y1), abs_of_pos (by linarith : (0:ℝ) < 1 + y2)]
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    have : 0 ≤ |y1 - y2| := abs_nonneg _
    nlinarith [mul_nonneg this (mul_nonneg h1.le h2.le), mul_nonneg this h1.le, mul_nonneg this h2.le]
  · have key : |1 / (1 + y2) - 1 / (1 + y1)| ≤ 1 / (1 + min y1 y2) := by
      rcases le_total y1 y2 with h | h
      · rw [min_eq_left h]
        have hle : 1 / (1 + y2) ≤ 1 / (1 + y1) := one_div_le_one_div_of_le (by linarith) (by linarith)
        rw [abs_le]; constructor <;> linarith
      · rw [min_eq_right h]
        have hle : 1 / (1 + y1) ≤ 1 / (1 + y2) := one_div_le_one_div_of_le (by linarith) (by linarith)
        rw [abs_le]; constructor <;> linarith
    rw [(T2c_det h1 h2).2, abs_div, abs_of_pos (by norm_num : (0:ℝ) < 2)]
    have hm : 0 < 1 + min y1 y2 := by have := lt_min h1 h2; linarith
    calc |1 / (1 + y2) - 1 / (1 + y1)| / 2 ≤ 1 / (1 + min y1 y2) / 2 := by linarith
      _ = 1 / (2 * (1 + min y1 y2)) := by field_simp
  · rw [(T2c_det h1 h2).2, abs_div, abs_of_pos (by norm_num : (0:ℝ) < 2)]
    have : |1 / (1 + y2) - 1 / (1 + y1)| < 1 := by rw [abs_lt]; constructor <;> linarith
    linarith

theorem T2c_yratio {s t g1 g2 : ℝ} (hg2 : 0 < g2) : yOf s t g1 / yOf s t g2 = g1 / g2 := by
  unfold yOf
  have := Real.exp_pos s
  have := Real.exp_pos t
  field_simp

theorem T2c_det_general (b1 b2 : ℝ) : (1 - b1) * b2 - b1 * (1 - b2) = b2 - b1 := by ring

theorem fisher_sum_id {n : ℕ} (b : Fin n → ℝ) :
    ∑ i, ∑ j, (b i - b j) ^ 2 = 2 * n * ∑ i, b i ^ 2 - 2 * (∑ i, b i) ^ 2 := by
  have : ∀ i, ∑ j, (b i - b j) ^ 2 = n * b i ^ 2 - 2 * b i * ∑ j, b j + ∑ j, b j ^ 2 := by
    intro i
    simp only [sub_sq, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_const,
      Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  simp only [this, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.sum_mul, ← Finset.mul_sum,
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  ring

theorem sum_one_sub_sq {n : ℕ} (b : Fin n → ℝ) :
    ∑ i, (1 - b i) ^ 2 = n - 2 * ∑ i, b i + ∑ i, b i ^ 2 := by
  simp only [sub_sq, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  ring

theorem T2c_fisher_det {n : ℕ} (b : Fin n → ℝ) :
    (∑ i, (1 - b i) ^ 2) * (∑ i, b i ^ 2) - (∑ i, (1 - b i) * b i) ^ 2
      = (1 / 2) * ∑ i, ∑ j, (b i - b j) ^ 2 := by
  have e3 : ∑ i, (1 - b i) * b i = ∑ i, b i - ∑ i, b i ^ 2 := by
    simp only [← Finset.sum_sub_distrib]; exact Finset.sum_congr rfl fun i _ => by ring
  rw [fisher_sum_id, sum_one_sub_sq, e3]; ring

theorem T2c_fisher_singular_iff {n : ℕ} (b : Fin n → ℝ) :
    (∑ i, (1 - b i) ^ 2) * (∑ i, b i ^ 2) - (∑ i, (1 - b i) * b i) ^ 2 = 0 ↔ ∀ i j, b i = b j := by
  rw [T2c_fisher_det]
  constructor
  · intro h i j
    have h0 : ∑ i, ∑ j, (b i - b j) ^ 2 = 0 := by linarith
    have hnn : ∀ i ∈ Finset.univ, 0 ≤ ∑ j, (b i - b j) ^ 2 :=
      fun i _ => Finset.sum_nonneg fun j _ => sq_nonneg _
    have hi := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp h0 i (Finset.mem_univ i)
    have hij := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg (b i - b j))).mp hi j
      (Finset.mem_univ j)
    have : b i - b j = 0 := by simpa using hij
    linarith
  · intro h
    have : ∑ i, ∑ j, (b i - b j) ^ 2 = 0 :=
      Finset.sum_eq_zero fun i _ => Finset.sum_eq_zero fun j _ => by rw [h i j]; ring
    rw [this]; ring

theorem T4_design_bound {n : ℕ} (b : Fin n → ℝ) (h0 : ∀ i, 0 ≤ b i) (h1 : ∀ i, b i ≤ 1 / 2) :
    9 * ∑ i, ∑ j, (b i - b j) ^ 2 ≤ 2 * n * ∑ i, (1 - b i) ^ 2 := by
  have hQ : ∑ i, b i ^ 2 ≤ (∑ i, b i) / 2 := by
    rw [Finset.sum_div]; exact Finset.sum_le_sum fun i _ => by nlinarith [h0 i, h1 i]
  rw [fisher_sum_id, sum_one_sub_sq]
  nlinarith [sq_nonneg ((n:ℝ) - 3 * ∑ i, b i), (Nat.cast_nonneg n : (0:ℝ) ≤ n)]

/-! ## T3: the Newtonian limit -/

theorem T3_newton_limit (ν : ℝ → ℝ) (hν : Tendsto ν atTop (𝓝 1)) {f a0 : ℝ} (hf : 0 < f) (ha : 0 < a0) :
    Tendsto (fun g : ℝ => gObs ν f a0 g / g) atTop (𝓝 f) := by
  have hy : Tendsto (fun g : ℝ => f * g / a0) atTop atTop :=
    (tendsto_id.const_mul_atTop hf).atTop_div_const ha
  have := (hν.comp hy).const_mul f
  rw [mul_one] at this
  refine this.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with g hg
  simp only [Function.comp, gObs]
  field_simp

theorem T3_newton_limit_a0 (ν : ℝ → ℝ) (hν : Tendsto ν atTop (𝓝 1)) {f a0 a0' : ℝ} (hf : 0 < f)
    (ha : 0 < a0) (ha' : 0 < a0') :
    Tendsto (fun g : ℝ => gObs ν f a0 g / gObs ν f a0' g) atTop (𝓝 1) := by
  have hy : Tendsto (fun g : ℝ => f * g / a0) atTop atTop :=
    (tendsto_id.const_mul_atTop hf).atTop_div_const ha
  have hy' : Tendsto (fun g : ℝ => f * g / a0') atTop atTop :=
    (tendsto_id.const_mul_atTop hf).atTop_div_const ha'
  have := (hν.comp hy).div (hν.comp hy') one_ne_zero
  rw [div_one] at this
  refine this.congr' ?_
  filter_upwards [eventually_gt_atTop 0, (hν.comp hy').eventually_ne one_ne_zero] with g hg hne
  simp only [Function.comp, gObs, Pi.div_apply] at *
  have hfg : f * g ≠ 0 := (mul_pos hf hg).ne'
  rw [mul_div_mul_left _ _ hfg]

theorem nuP2_tendsto_one : Tendsto nuP2 atTop (𝓝 1) := by
  have h : Tendsto (fun y : ℝ => Real.sqrt (1 + 1 / y)) atTop (𝓝 (Real.sqrt (1 + 0))) := by
    have : Tendsto (fun y : ℝ => 1 + 1 / y) atTop (𝓝 (1 + 0)) := by
      simp only [one_div]
      exact tendsto_const_nhds.add tendsto_inv_atTop_zero
    exact this.sqrt
  rw [add_zero, Real.sqrt_one] at h
  exact h


/-! ## T4 in terms of the Fisher matrix -/

/-- the (log f, log a0) Fisher matrix entries of a sample with rows (1 - b_i, b_i) and error sigma -/
noncomputable def fisher11 {n : ℕ} (σ : ℝ) (b : Fin n → ℝ) : ℝ := (∑ i, (1 - b i) ^ 2) / σ ^ 2
noncomputable def fisher12 {n : ℕ} (σ : ℝ) (b : Fin n → ℝ) : ℝ := (∑ i, (1 - b i) * b i) / σ ^ 2
noncomputable def fisher22 {n : ℕ} (σ : ℝ) (b : Fin n → ℝ) : ℝ := (∑ i, b i ^ 2) / σ ^ 2

/-- the marginal variance of log a0 is (F⁻¹)₂₂ = F₁₁ / det F -/
theorem T4_var_a0_closed_form {n : ℕ} {σ : ℝ} (hσ : σ ≠ 0) (b : Fin n → ℝ) :
    fisher11 σ b * fisher22 σ b - fisher12 σ b ^ 2 =
      ((1 / 2) * ∑ i, ∑ j, (b i - b j) ^ 2) / σ ^ 4 := by
  unfold fisher11 fisher12 fisher22
  rw [← T2c_fisher_det]
  field_simp

/-- T4, stated on the covariance: for any sample of n >= 1 points with f free and b_i in [0, 1/2]
(true for P2 and nu_mono), if F is invertible then var(log a0) = F11/det F >= 9 sigma^2 / n. -/
theorem T4_sigma_floor {n : ℕ} (hn : 0 < n) {σ : ℝ} (hσ : 0 < σ) (b : Fin n → ℝ)
    (h0 : ∀ i, 0 ≤ b i) (h1 : ∀ i, b i ≤ 1 / 2)
    (hdet : 0 < fisher11 σ b * fisher22 σ b - fisher12 σ b ^ 2) :
    9 * σ ^ 2 / n ≤ fisher11 σ b / (fisher11 σ b * fisher22 σ b - fisher12 σ b ^ 2) := by
  have hσ' : σ ≠ 0 := hσ.ne'
  rw [T4_var_a0_closed_form hσ'] at hdet ⊢
  have hS : 0 < ∑ i, ∑ j, (b i - b j) ^ 2 := by
    have : 0 < ((1 / 2) * ∑ i, ∑ j, (b i - b j) ^ 2) / σ ^ 4 := hdet
    have h4 : 0 < σ ^ 4 := by positivity
    have := (div_pos_iff_of_pos_right h4).mp this
    linarith
  have hT := T4_design_bound b h0 h1
  have hnr : (0:ℝ) < n := by exact_mod_cast hn
  unfold fisher11
  have e : ((∑ i, (1 - b i) ^ 2) / σ ^ 2) / (((1 / 2) * ∑ i, ∑ j, (b i - b j) ^ 2) / σ ^ 4) =
      2 * σ ^ 2 * (∑ i, (1 - b i) ^ 2) / ∑ i, ∑ j, (b i - b j) ^ 2 := by
    field_simp
  rw [e, div_le_div_iff₀ hnr hS]
  have := mul_le_mul_of_nonneg_left hT (sq_nonneg σ)
  nlinarith [this]


/-! ## T2e: kernel-general two-point injectivity from strict convexity -/

theorem convex_increment {L : ℝ → ℝ} (hL : StrictConvexOn ℝ Set.univ L) {h x x' : ℝ} (hh : 0 < h)
    (hx : x < x') : L (x + h) - L x < L (x' + h) - L x' := by
  have s1 := hL.secant_strict_mono (a := x) (x := x + h) (y := x' + h) trivial trivial trivial
    (by linarith) (by linarith) (by linarith)
  have s2 := hL.secant_strict_mono (a := x' + h) (x := x) (y := x') trivial trivial trivial
    (by linarith) (by linarith) hx
  have hd : 0 < x' + h - x := by linarith
  have e2 : (L x - L (x' + h)) / (x - (x' + h)) = (L (x' + h) - L x) / (x' + h - x) := by
    rw [show x - (x' + h) = -(x' + h - x) by ring,
      show L x - L (x' + h) = -(L (x' + h) - L x) by ring, neg_div_neg_eq]
  have e3 : (L x' - L (x' + h)) / (x' - (x' + h)) = (L (x' + h) - L x') / h := by
    rw [show x' - (x' + h) = -h by ring, show L x' - L (x' + h) = -(L (x' + h) - L x') by ring,
      neg_div_neg_eq]
  rw [e2, e3] at s2
  rw [show x + h - x = h by ring] at s1
  have : (L (x + h) - L x) / h < (L (x' + h) - L x') / h := lt_trans s1 s2
  exact (div_lt_div_iff_of_pos_right hh).mp this

theorem two_point_core {L : ℝ → ℝ} (hL : StrictConvexOn ℝ Set.univ L) {m m' u1 u2 : ℝ}
    (hu : u1 < u2) (h : L (m + u1) - L (m + u2) = L (m' + u1) - L (m' + u2)) : m = m' := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have := convex_increment hL (h := u2 - u1) (by linarith) (show m + u1 < m' + u1 by linarith)
    rw [show m + u1 + (u2 - u1) = m + u2 by ring, show m' + u1 + (u2 - u1) = m' + u2 by ring] at this
    linarith
  · have := convex_increment hL (h := u2 - u1) (by linarith) (show m' + u1 < m + u1 by linarith)
    rw [show m + u1 + (u2 - u1) = m + u2 by ring, show m' + u1 + (u2 - u1) = m' + u2 by ring] at this
    linarith

theorem log_gObs_general (ν : ℝ → ℝ) (hν : ∀ y : ℝ, 0 < y → 0 < ν y) {f a0 g : ℝ}
    (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    Real.log (gObs ν f a0 g) = Real.log a0 +
      Real.log (Real.exp ((Real.log f - Real.log a0) + Real.log g) *
        ν (Real.exp ((Real.log f - Real.log a0) + Real.log g))) := by
  have hy : Real.exp ((Real.log f - Real.log a0) + Real.log g) = f * g / a0 := by
    rw [Real.exp_add, Real.exp_sub, Real.exp_log hf, Real.exp_log ha, Real.exp_log hg]
    field_simp
  rw [hy]
  have hy0 : 0 < f * g / a0 := by positivity
  have hn := hν _ hy0
  have : gObs ν f a0 g = a0 * (f * g / a0 * ν (f * g / a0)) := by
    unfold gObs; field_simp
  rw [this, Real.log_mul ha.ne' (by positivity)]

theorem T2e_injective_of_strictConvex (ν : ℝ → ℝ) (hν : ∀ y : ℝ, 0 < y → 0 < ν y)
    (hL : StrictConvexOn ℝ Set.univ (fun u : ℝ => Real.log (Real.exp u * ν (Real.exp u))))
    {f a0 f' a0' g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f') (ha' : 0 < a0')
    (hg1 : 0 < g1) (hg2 : 0 < g2) (hne : g1 ≠ g2)
    (h1 : gObs ν f a0 g1 = gObs ν f' a0' g1) (h2 : gObs ν f a0 g2 = gObs ν f' a0' g2) :
    f = f' ∧ a0 = a0' := by
  set L : ℝ → ℝ := fun u => Real.log (Real.exp u * ν (Real.exp u)) with hLdef
  have e1 := congrArg Real.log h1
  have e2 := congrArg Real.log h2
  rw [log_gObs_general ν hν hf ha hg1, log_gObs_general ν hν hf' ha' hg1] at e1
  rw [log_gObs_general ν hν hf ha hg2, log_gObs_general ν hν hf' ha' hg2] at e2
  have hdiff : L ((Real.log f - Real.log a0) + Real.log g1) - L ((Real.log f - Real.log a0) + Real.log g2)
      = L ((Real.log f' - Real.log a0') + Real.log g1) - L ((Real.log f' - Real.log a0') + Real.log g2) := by
    simp only [hLdef]; linarith
  have hm : Real.log f - Real.log a0 = Real.log f' - Real.log a0' := by
    rcases lt_or_gt_of_ne hne with hlt | hgt
    · exact two_point_core hL (Real.log_lt_log hg1 hlt) hdiff
    · exact two_point_core hL (Real.log_lt_log hg2 hgt) (by linarith)
  have hA : Real.log a0 = Real.log a0' := by
    rw [hm] at e1; linarith
  have ha0 : a0 = a0' := Real.log_injOn_pos (Set.mem_Ioi.mpr ha) (Set.mem_Ioi.mpr ha') hA
  refine ⟨?_, ha0⟩
  have : Real.log f = Real.log f' := by linarith
  exact Real.log_injOn_pos (Set.mem_Ioi.mpr hf) (Set.mem_Ioi.mpr hf') this

/-! ## nu_mono -/

theorem nuMono_pos {y : ℝ} (hy : 0 < y) : 0 < nuMono y := by
  unfold nuMono
  have h : Real.exp (-Real.sqrt y) < 1 := by
    have := Real.exp_lt_exp.mpr (show -Real.sqrt y < 0 by have := Real.sqrt_pos.mpr hy; linarith)
    simpa using this
  exact one_div_pos.mpr (by linarith)

theorem nuMono_tendsto_one : Tendsto nuMono atTop (𝓝 1) := by
  have h0 : Tendsto (fun y : ℝ => Real.exp (-Real.sqrt y)) atTop (𝓝 0) :=
    Real.tendsto_exp_neg_atTop_nhds_zero.comp Real.tendsto_sqrt_atTop
  have h := (tendsto_const_nhds (x := (1:ℝ))).div (tendsto_const_nhds.sub h0) (by norm_num : (1:ℝ) - 0 ≠ 0)
  rw [sub_zero, div_one] at h
  refine h.congr' (Filter.Eventually.of_forall fun y => ?_)
  simp [nuMono]


/-! ## nu_mono: strict convexity of log(e^u nu_mono(e^u)) -/

/-- the closed form of L for nu_mono: with w = e^(u/2), L(u) = u + w - log(e^w - 1) -/
noncomputable def LmonoF (u : ℝ) : ℝ :=
  u + Real.exp (u / 2) - Real.log (Real.exp (Real.exp (u / 2)) - 1)

theorem Lmono_eq (u : ℝ) : Real.log (Real.exp u * nuMono (Real.exp u)) = LmonoF u := by
  have hw : 0 < Real.exp (u / 2) := Real.exp_pos _
  have hsq : Real.sqrt (Real.exp u) = Real.exp (u / 2) := (Real.exp_half u).symm
  set w := Real.exp (u / 2) with hwdef
  have hexp : 1 < Real.exp w := by
    have := Real.exp_lt_exp.mpr hw; rwa [Real.exp_zero] at this
  have hD : 0 < 1 - Real.exp (-w) := by
    have := Real.exp_lt_exp.mpr (show -w < 0 by linarith)
    rw [Real.exp_zero] at this; linarith
  have hD2 : 1 - Real.exp (-w) = (Real.exp w - 1) * Real.exp (-w) := by
    rw [sub_mul, ← Real.exp_add]; simp
  have hE : 0 < Real.exp w - 1 := by linarith
  unfold nuMono LmonoF
  rw [hsq, one_div, Real.log_mul (Real.exp_pos u).ne' (inv_pos.mpr hD).ne', Real.log_exp,
    Real.log_inv, hD2, Real.log_mul hE.ne' (Real.exp_pos _).ne', Real.log_exp]
  ring

theorem LmonoF_hasDeriv (u : ℝ) :
    HasDerivAt LmonoF (1 - (Real.exp (u / 2) / 2) / (Real.exp (Real.exp (u / 2)) - 1)) u := by
  have hw : 0 < Real.exp (u / 2) := Real.exp_pos _
  have hexp : 1 < Real.exp (Real.exp (u / 2)) := by
    have := Real.exp_lt_exp.mpr hw; rwa [Real.exp_zero] at this
  have hE : Real.exp (Real.exp (u / 2)) - 1 ≠ 0 := by linarith
  have w1 : HasDerivAt (fun x : ℝ => Real.exp (x / 2)) (Real.exp (u / 2) / 2) u := by
    have := ((hasDerivAt_id u).div_const 2).exp
    simpa [div_eq_mul_inv, mul_comm] using this
  have e1 : HasDerivAt (fun x : ℝ => Real.exp (Real.exp (x / 2)))
      (Real.exp (Real.exp (u / 2)) * (Real.exp (u / 2) / 2)) u := w1.exp
  have e2 := (e1.sub_const 1).log hE
  have F1 := ((hasDerivAt_id u).add w1).sub e2
  refine (F1.congr_deriv ?_).congr_of_eventuallyEq ?_
  · field_simp
    ring
  · exact Filter.Eventually.of_forall fun x => by simp [LmonoF]

theorem nuMono_logslope_strictConvex :
    StrictConvexOn ℝ Set.univ (fun u : ℝ => Real.log (Real.exp u * nuMono (Real.exp u))) := by
  have hfun : (fun u : ℝ => Real.log (Real.exp u * nuMono (Real.exp u))) = LmonoF := funext Lmono_eq
  rw [hfun]
  refine StrictMonoOn.strictConvexOn_of_deriv convex_univ ?_ ?_
  · exact continuous_iff_continuousAt.mpr (fun u => (LmonoF_hasDeriv u).continuousAt) |>.continuousOn
  · rw [interior_univ]
    intro a _ b _ hab
    rw [(LmonoF_hasDeriv a).deriv, (LmonoF_hasDeriv b).deriv]
    have hwa : 0 < Real.exp (a / 2) := Real.exp_pos _
    have hwab : Real.exp (a / 2) < Real.exp (b / 2) := Real.exp_lt_exp.mpr (by linarith)
    set wa := Real.exp (a / 2)
    set wb := Real.exp (b / 2)
    have hwb : 0 < wb := by linarith
    have hA : 0 < Real.exp wa - 1 := by
      have := Real.exp_lt_exp.mpr hwa; rw [Real.exp_zero] at this; linarith
    have hB : 0 < Real.exp wb - 1 := by
      have := Real.exp_lt_exp.mpr hwb; rw [Real.exp_zero] at this; linarith
    have hs := strictConvexOn_exp.secant_strict_mono (a := 0) (x := wa) (y := wb) trivial trivial trivial
      hwa.ne' hwb.ne' hwab
    rw [Real.exp_zero, sub_zero, sub_zero, div_lt_div_iff₀ hwa hwb] at hs
    have : wb / 2 / (Real.exp wb - 1) < wa / 2 / (Real.exp wa - 1) := by
      rw [div_lt_div_iff₀ hB hA]; nlinarith
    linarith

theorem T2e_nuMono_injective {f a0 f' a0' g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg1 : 0 < g1) (hg2 : 0 < g2) (hne : g1 ≠ g2)
    (h1 : gObs nuMono f a0 g1 = gObs nuMono f' a0' g1) (h2 : gObs nuMono f a0 g2 = gObs nuMono f' a0' g2) :
    f = f' ∧ a0 = a0' :=
  T2e_injective_of_strictConvex nuMono (fun _ hy => nuMono_pos hy) nuMono_logslope_strictConvex
    hf ha hf' ha' hg1 hg2 hne h1 h2


/-! ## P2: strict convexity of log(e^u nu_P2(e^u)) (cross-check of T2a through T2e) -/

noncomputable def LP2F (u : ℝ) : ℝ := (u + Real.log (Real.exp u + 1)) / 2

theorem LP2_eq (u : ℝ) : Real.log (Real.exp u * nuP2 (Real.exp u)) = LP2F u := by
  have he := Real.exp_pos u
  have h1 : Real.exp u * nuP2 (Real.exp u) = Real.sqrt (Real.exp u * (Real.exp u + 1)) := by
    unfold nuP2
    have : Real.exp u * Real.sqrt (1 + 1 / Real.exp u) = Real.sqrt (Real.exp u ^ 2 * (1 + 1 / Real.exp u)) := by
      rw [Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq he.le]
    rw [this]; congr 1; field_simp
  rw [h1, Real.log_sqrt (by positivity), Real.log_mul he.ne' (by positivity), Real.log_exp]
  unfold LP2F; ring

theorem LP2F_hasDeriv (u : ℝ) :
    HasDerivAt LP2F ((1 + Real.exp u / (Real.exp u + 1)) / 2) u := by
  have he := Real.exp_pos u
  have h1 : HasDerivAt (fun x : ℝ => Real.exp x + 1) (Real.exp u) u := (Real.hasDerivAt_exp u).add_const 1
  have h2 := h1.log (by positivity)
  have h3 := ((hasDerivAt_id u).add h2).div_const 2
  exact h3.congr_deriv (by simp)

theorem nuP2_logslope_strictConvex :
    StrictConvexOn ℝ Set.univ (fun u : ℝ => Real.log (Real.exp u * nuP2 (Real.exp u))) := by
  have hfun : (fun u : ℝ => Real.log (Real.exp u * nuP2 (Real.exp u))) = LP2F := funext LP2_eq
  rw [hfun]
  refine StrictMonoOn.strictConvexOn_of_deriv convex_univ ?_ ?_
  · exact continuous_iff_continuousAt.mpr (fun u => (LP2F_hasDeriv u).continuousAt) |>.continuousOn
  · rw [interior_univ]
    intro a _ b _ hab
    rw [(LP2F_hasDeriv a).deriv, (LP2F_hasDeriv b).deriv]
    have hab' : Real.exp a < Real.exp b := Real.exp_lt_exp.mpr hab
    have ha := Real.exp_pos a
    have : Real.exp a / (Real.exp a + 1) < Real.exp b / (Real.exp b + 1) := by
      rw [div_lt_div_iff₀ (by positivity) (by positivity)]; nlinarith
    linarith

end CalibrationWall
