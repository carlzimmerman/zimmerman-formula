import Mathlib

/-!
# EQB_S1 -- the RAR landmark triplet of the framework law (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/eqbook_S1_algebraic.py`, checks E-S1.4 (slope, line 78-80),
E-S1.5 (curvature and its maximum, lines 85-93), E-S1.6 (reciprocity, lines 96-97), E-S1.7 (sum rule, lines 100-101),
E-S1.8 (anchor, lines 104-105); write-up `prep_2026/equation_book/MINE_M1.md` (item 1).

PREMISE (a declared law of the framework, NOT certified as physics here): the a0-line
    g_obs^2 = g_bar^2 + a0 g_bar,     y = g_bar/a0 > 0,     g_obs/a0 = sqrt(y^2 + y).
CERTIFIED (premises => conclusions, pure real analysis):
  * `slope_hasDeriv`   : d ln(g_obs/a0) / d ln y = (2y+1)/(2(y+1))   (the log-log slope, as a real derivative in ell = ln y)
  * `curv_hasDeriv`    : d slope / d ln y = y/(2(y+1)^2)
  * `curv_le` / `curv_eq_iff` : the curvature is <= 1/8 and equals 1/8 iff y = 1 (its maximum is exactly at g_bar = a0)
  * `slope_at_one`, `curv_at_one` : slope(1) = 3/4, curvature(1) = 1/8
  * `curv_reciprocal`  : curvature(1/y) = curvature(y)   (even in ln(g_bar/a0))
  * `slope_sum_rule`   : slope(y) + slope(1/y) = 3/2 for every y > 0
  * `slope_bounds`     : 1/2 < slope < 1 for y > 0 (deep-MOND and Newtonian limits are the bounds)
  * `anchor`           : the law at g_bar = a0 gives g_obs = sqrt 2 * a0
NOT certified: that any of this is the RAR of nature; the numerical comparison with McGaugh's or the "simple" nu (the script
computes those numerically: they break the sum rule or the symmetry -- that discrimination is NOT a Lean statement here);
any data; kappa = 1/2 (FITTED) does not enter.
-/

open Real

noncomputable section

/-- log-log slope of the law, as a function of y = g_bar/a0. -/
def sigma (y : ℝ) : ℝ := (2 * y + 1) / (2 * (y + 1))

/-- log-log curvature (derivative of the slope with respect to ln y). -/
def curv (y : ℝ) : ℝ := y / (2 * (y + 1) ^ 2)

/-- The log-log slope: with ell = ln y, d/d ell ln(sqrt(y^2 + y)) = (2y+1)/(2(y+1)). -/
theorem slope_hasDeriv (ℓ : ℝ) :
    HasDerivAt (fun t : ℝ => Real.log (Real.sqrt (Real.exp t ^ 2 + Real.exp t)))
      (sigma (Real.exp ℓ)) ℓ := by
  have hpos : ∀ t : ℝ, 0 < Real.exp t ^ 2 + Real.exp t := fun t => by positivity
  have hfun : (fun t : ℝ => Real.log (Real.sqrt (Real.exp t ^ 2 + Real.exp t)))
      = fun t : ℝ => Real.log (Real.exp t ^ 2 + Real.exp t) / 2 := by
    funext t
    exact Real.log_sqrt (hpos t).le
  rw [hfun]
  have h0 : HasDerivAt (fun t : ℝ => Real.exp t ^ 2) (2 * Real.exp ℓ * Real.exp ℓ) ℓ := by
    have := (Real.hasDerivAt_exp ℓ).pow 2
    exact this.congr_deriv (by ring)
  have h1 : HasDerivAt (fun t : ℝ => Real.exp t ^ 2 + Real.exp t)
      (2 * Real.exp ℓ * Real.exp ℓ + Real.exp ℓ) ℓ := h0.add (Real.hasDerivAt_exp ℓ)
  have h2 := (h1.log (hpos ℓ).ne').div_const 2
  refine h2.congr_deriv ?_
  have hy : 0 < Real.exp ℓ := Real.exp_pos ℓ
  have hy1 : Real.exp ℓ + 1 ≠ 0 := by positivity
  simp only [sigma]
  field_simp

/-- The curvature: d/d ell of the slope is y/(2(y+1)^2). -/
theorem curv_hasDeriv (ℓ : ℝ) :
    HasDerivAt (fun t : ℝ => sigma (Real.exp t)) (curv (Real.exp ℓ)) ℓ := by
  have hy : 0 < Real.exp ℓ := Real.exp_pos ℓ
  have hne : 2 * (Real.exp ℓ + 1) ≠ 0 := by positivity
  have h1 : HasDerivAt (fun t : ℝ => 2 * Real.exp t + 1) (2 * Real.exp ℓ) ℓ :=
    (((Real.hasDerivAt_exp ℓ).const_mul 2).add_const 1).congr_deriv (by ring)
  have h2 : HasDerivAt (fun t : ℝ => 2 * (Real.exp t + 1)) (2 * Real.exp ℓ) ℓ :=
    (((Real.hasDerivAt_exp ℓ).add_const 1).const_mul 2).congr_deriv (by ring)
  have h3 := h1.div h2 hne
  have hfun : (fun t : ℝ => sigma (Real.exp t)) = fun t : ℝ => (2 * Real.exp t + 1) / (2 * (Real.exp t + 1)) := by
    funext t; rfl
  rw [hfun]
  refine h3.congr_deriv ?_
  have : Real.exp ℓ + 1 ≠ 0 := by positivity
  simp only [curv]
  field_simp
  ring

theorem curv_le (y : ℝ) : curv y ≤ 1 / 16 := by
  unfold curv
  by_cases h : y + 1 = 0
  · have : y = -1 := by linarith
    subst this; norm_num
  · have hp : 0 < 2 * (y + 1) ^ 2 := by positivity
    rw [div_le_iff₀ hp]
    nlinarith [sq_nonneg (y - 1)]

theorem curv_eq_iff {y : ℝ} (hy : 0 < y) : curv y = 1 / 8 ↔ y = 1 := by
  unfold curv
  have hp : 0 < 2 * (y + 1) ^ 2 := by positivity
  rw [div_eq_iff hp.ne']
  constructor
  · intro h
    have : (y - 1) ^ 2 = 0 := by nlinarith
    have := pow_eq_zero_iff (two_ne_zero) |>.mp this
    linarith
  · intro h; subst h; norm_num

theorem curv_max_unique {y : ℝ} (hy : 0 < y) (hy1 : y ≠ 1) : curv y < curv 1 := by
  have h1 : curv 1 = 1 / 8 := by unfold curv; norm_num
  rw [h1]
  refine lt_of_le_of_ne (curv_le y) ?_
  intro h
  exact hy1 ((curv_eq_iff hy).mp h)

theorem slope_at_one : sigma 1 = 3 / 4 := by unfold sigma; norm_num
theorem curv_at_one : curv 1 = 1 / 8 := by unfold curv; norm_num

theorem curv_reciprocal {y : ℝ} (hy : 0 < y) : curv (1 / y) = curv y := by
  unfold curv
  have h1 : y + 1 ≠ 0 := by positivity
  have h2 : 1 / y + 1 ≠ 0 := by positivity
  have hy0 : y ≠ 0 := hy.ne'
  field_simp
  ring

theorem slope_sum_rule {y : ℝ} (hy : 0 < y) : sigma y + sigma (1 / y) = 3 / 2 := by
  unfold sigma
  have h1 : y + 1 ≠ 0 := by positivity
  have hy0 : y ≠ 0 := hy.ne'
  field_simp
  ring

theorem slope_bounds {y : ℝ} (hy : 0 < y) : 1 / 2 < sigma y ∧ sigma y < 1 := by
  unfold sigma
  have hp : 0 < 2 * (y + 1) := by positivity
  constructor
  · rw [lt_div_iff₀ hp]; nlinarith
  · rw [div_lt_iff₀ hp]; nlinarith

/-- the anchor: the law at g_bar = a0 gives g_obs = sqrt 2 * a0. -/
theorem anchor {a0 : ℝ} (ha : 0 < a0) : Real.sqrt (a0 ^ 2 + a0 * a0) = Real.sqrt 2 * a0 := by
  have : a0 ^ 2 + a0 * a0 = 2 * a0 ^ 2 := by ring
  rw [this, Real.sqrt_mul (by norm_num), Real.sqrt_sq ha.le]

end

#print axioms slope_hasDeriv
#print axioms curv_hasDeriv
#print axioms curv_le
#print axioms curv_eq_iff
#print axioms curv_max_unique
#print axioms curv_reciprocal
#print axioms slope_sum_rule
#print axioms slope_bounds
#print axioms anchor
