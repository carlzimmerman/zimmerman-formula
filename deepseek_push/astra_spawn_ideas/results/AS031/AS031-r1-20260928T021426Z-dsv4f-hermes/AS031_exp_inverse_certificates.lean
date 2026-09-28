import Mathlib

/-!
AS031 — Historical exponential AQUAL inversion: Lean certificate.

Branch (RETIRED comparison, never the operative target): EXP constitutive response
    mu_EXP(x) = 1 - exp(-x),   y(x) = x * mu_EXP(x) = x * (1 - exp(-x)),   x = g/a0 >= 0.
The algebraic response y(x) is strictly increasing on [0, inf), so its inverse
x(y) on [0, inf) exists and is unique. Certified here:
  (A) exp_deriv_ident    : dy/dx = 1 + (x-1)*exp(-x)         (HasDerivAt, exact)
  (B) exp_deriv_pos      : dy/dx > 0 for all x > 0          (strict positivity)
  (C) exp_forward_strict_mono : StrictMonoOn yExp (Ici 0)   (injectivity of the response)
  (D) exp_forward_bounds : x^2/(1+x) <= y(x) <= x^2 for x >= 0
                           (universal inversion bracket: sqrt(y) <= x <= (y+sqrt(y^2+4y))/2)
  (E) exp_deriv2_ident   : d2y/dx2 = exp(-x)*(2-x)          (slope maximum at x = 2)
  (F) exp_deriv2_sign_below/above : slope increases on [0,2), decreases on (2,inf)
  (G) exp_mu_param       : exact inverse in mu-parametrization:
                           y = -mu*ln(1-mu) with mu = 1 - exp(-x) (equivalently x = -ln(1-mu))
-/

noncomputable def yExp (x : ℝ) : ℝ := x * (1 - Real.exp (-x))

/-- (G) mu-parametrization identity: y = -mu*ln(1-mu) at mu = 1 - exp(-x). -/
lemma exp_mu_param (x : ℝ) :
    -(1 - Real.exp (-x)) * Real.log (1 - (1 - Real.exp (-x))) = yExp x := by
  have hlog : Real.log (Real.exp (-x)) = -x := Real.log_exp (-x)
  have hsub : 1 - (1 - Real.exp (-x)) = Real.exp (-x) := by ring
  rw [hsub, hlog, yExp]
  ring_nf

/-- derivative helper: d/dt exp(-t) = -exp(-t). -/
lemma exp_neg_deriv (x : ℝ) :
    HasDerivAt (fun t : ℝ => Real.exp (-t)) (-Real.exp (-x)) x := by
  simpa [mul_comm] using ((hasDerivAt_id x).neg).exp

/-- (A) dy/dx = 1 + (x-1)*exp(-x), exact HasDerivAt. -/
lemma exp_deriv_ident (x : ℝ) :
    HasDerivAt yExp (1 + (x - 1) * Real.exp (-x)) x := by
  have hE := exp_neg_deriv x
  have hM' : HasDerivAt (fun t : ℝ => (1 : ℝ) - Real.exp (-t)) (0 - (-Real.exp (-x))) x :=
    (hasDerivAt_const (x := x) (1 : ℝ)).sub hE
  have hM : HasDerivAt (fun t : ℝ => (1 : ℝ) - Real.exp (-t)) (Real.exp (-x)) x := by
    simpa using hM'
  have hd : HasDerivAt (fun t : ℝ => t * (1 - Real.exp (-t)))
      (1 * (1 - Real.exp (-x)) + x * Real.exp (-x)) x := (hasDerivAt_id x).mul hM
  have hslope : 1 * (1 - Real.exp (-x)) + x * Real.exp (-x) = 1 + (x - 1) * Real.exp (-x) := by ring
  rw [hslope] at hd
  change HasDerivAt (fun t : ℝ => t * (1 - Real.exp (-t))) (1 + (x - 1) * Real.exp (-x)) x
  exact hd

/-- (B) dy/dx > 0 for all x > 0. -/
lemma exp_deriv_pos {x : ℝ} (hx : 0 < x) : 0 < 1 + (x - 1) * Real.exp (-x) := by
  by_cases hxlt : x < 1
  · have hExp : Real.exp (-x) < 1 := by
      rw [← Real.exp_zero]
      exact (Real.exp_strictMono.lt_iff_lt).mpr (by linarith)
    have h1mx : 0 < 1 - x := by linarith
    have hmul : (1 - x) * Real.exp (-x) < (1 - x) * 1 := mul_lt_mul_of_pos_left hExp h1mx
    have hmul1 : (1 - x) * 1 < 1 := by nlinarith
    nlinarith [lt_trans hmul hmul1]
  · have hxge : 1 ≤ x := by linarith
    have hnonneg : 0 ≤ (x - 1) * Real.exp (-x) :=
      mul_nonneg (by linarith) (le_of_lt (Real.exp_pos _))
    nlinarith

/-- (C) the EXP constitutive response is strictly increasing on [0, inf)
(hence injective there: the inverse x(y) exists and is unique on [0, inf)). -/
lemma exp_forward_strict_mono : StrictMonoOn yExp (Set.Ici (0 : ℝ)) := by
  refine strictMonoOn_of_deriv_pos (D := Set.Ici (0 : ℝ)) (convex_Ici 0) ?_ ?_
  · exact ((continuous_id.mul (continuous_const.sub (Real.continuous_exp.comp continuous_neg))).continuousOn)
  · intro x hx
    have hx0 : 0 < x := by simpa [interior_Ici, Set.mem_Ioi] using hx
    have hd : HasDerivAt yExp (1 + (x - 1) * Real.exp (-x)) x := exp_deriv_ident x
    rw [hd.deriv]
    exact exp_deriv_pos hx0

/-- corollary of (C): strict monotonicity of y(x) on [0, inf). -/
lemma exp_forward_lt {x1 x2 : ℝ} (hx1 : 0 ≤ x1) (h12 : x1 < x2) :
    yExp x1 < yExp x2 := by
  have hx2 : 0 ≤ x2 := le_trans hx1 (le_of_lt h12)
  exact exp_forward_strict_mono (Set.mem_Ici.mpr hx1) (Set.mem_Ici.mpr hx2) h12

/-- corollary of (C): y is injective on [0, inf) (unique inverse on the physical branch). -/
lemma exp_forward_injective_nonneg : Set.InjOn yExp (Set.Ici (0 : ℝ)) :=
  exp_forward_strict_mono.injOn

/-- (D-upper) y(x) <= x^2 for x >= 0 (from exp(-x) >= 1 - x, i.e. add_one_le_exp). -/
lemma exp_forward_upper {x : ℝ} (hx : 0 ≤ x) : yExp x ≤ x ^ 2 := by
  have hle : 1 - Real.exp (-x) ≤ x := by
    have h := Real.add_one_le_exp (-x)
    linarith
  have hm := mul_le_mul_of_nonneg_left hle hx
  simpa [yExp, pow_two] using hm

/-- (D-lower) x^2/(1+x) <= y(x) for x >= 0 (from exp(-x) <= 1/(1+x), i.e. add_one_le_exp).
Equivalently the inversion bracket  x <= (y + sqrt(y^2 + 4y))/2. -/
lemma exp_forward_lower {x : ℝ} (hx : 0 ≤ x) : x ^ 2 / (1 + x) ≤ yExp x := by
  rcases eq_or_lt_of_le hx with rfl | hx0
  · norm_num [yExp]
  · have hprod : (1 + x) * Real.exp (-x) ≤ 1 := by
      calc
        (1 + x) * Real.exp (-x) ≤ Real.exp x * Real.exp (-x) := by
          exact mul_le_mul_of_nonneg_right (by simpa [add_comm] using Real.add_one_le_exp x)
            (le_of_lt (Real.exp_pos _))
        _ = 1 := by rw [← Real.exp_add, add_neg_cancel, Real.exp_zero]
    have h1px : 0 < 1 + x := by linarith
    have hc : x ≤ (1 - Real.exp (-x)) * (1 + x) := by
      have h2 : (1 - Real.exp (-x)) * (1 + x) = (1 + x) - (1 + x) * Real.exp (-x) := by ring
      rw [h2]
      nlinarith [hprod]
    have hle : x / (1 + x) ≤ 1 - Real.exp (-x) := (div_le_iff₀ h1px).mpr hc
    have hmm : x * (x / (1 + x)) ≤ x * (1 - Real.exp (-x)) :=
      mul_le_mul_of_nonneg_left hle (le_of_lt hx0)
    have hx2 : x ^ 2 / (1 + x) = x * (x / (1 + x)) := by ring
    rw [hx2]
    change x * (x / (1 + x)) ≤ x * (1 - Real.exp (-x))
    exact hmm

/-- (E) d2y/dx2 = exp(-x) * (2 - x), exact HasDerivAt. -/
lemma exp_deriv2_ident (x : ℝ) :
    HasDerivAt (fun t : ℝ => 1 + (t - 1) * Real.exp (-t)) (Real.exp (-x) * (2 - x)) x := by
  have hE := exp_neg_deriv x
  have hT : HasDerivAt (fun t : ℝ => t - 1) (1 - 0) x :=
    (hasDerivAt_id x).sub (hasDerivAt_const (x := x) (1 : ℝ))
  have hP : HasDerivAt (fun t : ℝ => (t - 1) * Real.exp (-t))
      ((1 - 0) * Real.exp (-x) + (x - 1) * (-Real.exp (-x))) x := hT.mul hE
  have hG : HasDerivAt (fun t : ℝ => 1 + (t - 1) * Real.exp (-t))
      (0 + ((1 - 0) * Real.exp (-x) + (x - 1) * (-Real.exp (-x)))) x :=
    (hasDerivAt_const (x := x) (1 : ℝ)).add hP
  have hslope : 0 + ((1 - 0) * Real.exp (-x) + (x - 1) * (-Real.exp (-x))) = Real.exp (-x) * (2 - x) := by ring
  rw [hslope] at hG
  exact hG

/-- (F) slope strictly increasing on [0,2): d2y/dx2 > 0 for x < 2. -/
lemma exp_deriv2_sign_below {x : ℝ} (hx : x < 2) : 0 < Real.exp (-x) * (2 - x) := by
  exact mul_pos (Real.exp_pos _) (by linarith)

/-- (F) slope strictly decreasing on (2,inf): d2y/dx2 < 0 for x > 2. -/
lemma exp_deriv2_sign_above {x : ℝ} (hx : 2 < x) : Real.exp (-x) * (2 - x) < 0 := by
  exact mul_neg_of_pos_of_neg (Real.exp_pos _) (by linarith)

/-- max slope value at x = 2: dy/dx(2) = 1 + exp(-2). -/
lemma exp_slope_at_two : 1 + (2 - 1) * Real.exp (-2) = 1 + Real.exp (-2) := by ring

/- Axiom audit: every theorem below must print an axiom list subseteq
   {propext, Classical.choice, Quot.sound}. -/
#check yExp
#print axioms exp_mu_param
#print axioms exp_neg_deriv
#print axioms exp_deriv_ident
#print axioms exp_deriv_pos
#print axioms exp_forward_strict_mono
#print axioms exp_forward_lt
#print axioms exp_forward_injective_nonneg
#print axioms exp_forward_upper
#print axioms exp_forward_lower
#print axioms exp_deriv2_ident
#print axioms exp_deriv2_sign_below
#print axioms exp_deriv2_sign_above
#print axioms exp_slope_at_two
