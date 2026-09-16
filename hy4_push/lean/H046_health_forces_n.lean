/-
  H046 -- IS n = 2 FORCED BY THE HEALTH CONDITIONS?   (Agent J)

  QUESTION.  The programme's last free integer is n = 2, the deep slope
      n = lim_{u -> 0} mu(u)/u ,     mu = f' ,   L = Lambda^4 f(K),  K = u^2.
  H017/H030 derive it from the dimension: n = D(D-3)/2 = 2 at D = 4.  This
  file asks the sharper question: do the HEALTH conditions alone force it?

      (i)   0 <= c_s^2 <= 1 for all K      (subluminal, no gradient instability)
      (ii)  f' > 0                          (no ghost)
      (iii) stability
      (iv)  the deep slope is finite and non-zero

  ANSWER CERTIFIED HERE:  NO.

  The reason is a single identity.  Because K = u^2 and f'(K) = mu(u),

      2 K f''(K) = 2 u^2 * (mu'(u)/(2u)) = u mu'(u),

  so the k-essence sound speed is

      c_s^2 = mu / (mu + u mu') = 1 / (1 + dln mu / dln u).

  Therefore (i)+(ii)+(iii) hold  <=>  mu > 0 and mu' >= 0 on u > 0: the
  health conditions constrain the LOG-SLOPE of mu and are exactly blind to
  its AMPLITUDE, which is what n is.  Every n > 0 is realized by a healthy
  mu (certified for n = 1, 2, 3 below), so health cannot select n = 2.

  WHAT HEALTH DOES FORCE (genuine, n-independent):
    * (iv) says the deep log-slope is exactly 1, and then
          c_s^2 -> 1/(1+1) = 1/2  as K -> 0,   for EVERY value of n.
      The measured deep sound speed 1/2 is therefore a PREDICTION of health
      plus the existence of a linear MOND regime -- not a fit, and not a
      discriminator of n.
    * In the minimal Padé family mu = u(a+u)/(1+u)^2 (the family forced by
      mu(0)=0, mu(infinity)=1 and a double pole at u = -1) subluminality
      gives the SHARP bound a <= 2, and the observed a = 2 saturates it:
      a > 2 is superluminal for large u.  Scope: family-dependent.

  WHAT DOES FIX THE 2 (and it is not health):
    In f = K - c ln(1+sqrt K) - d/(1+sqrt K) + const,
      (alpha) finiteness of f'(0) forces d = c        (the 1/u pole cancels)
      (beta)  mu(0) = f'(0) = 0 (a MOND regime, no Newtonian floor) forces
              c = 2
      (gamma) then the deep slope equals c = 2.
    That is a derivation of the integer from REGULARITY + THE EXISTENCE OF A
    MOND REGIME.  It is not a health condition, and the family is put in by
    hand.  Reported as the honest positive result, not as a health theorem.

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

open Set Filter Topology

noncomputable section

namespace H046

/-! ## 0. The master identity for the sound speed -/

/-- The k-essence sound speed for L = Lambda^4 f(K) with K = u^2, f'(K) = mu(u).
    Since 2K f'' = u mu'(u),   c_s^2 = mu / (mu + u mu'). -/
def cs2 (mu mup u : ℝ) : ℝ := mu / (mu + u * mup)

/-- Log-slope form:  c_s^2 = 1 / (1 + dln(mu)/dln(u)).
    Health depends on the log-slope only; the amplitude n never appears. -/
theorem cs2_logslope (mu mup u : ℝ) (hmu : mu ≠ 0)
    (hden : mu + u * mup ≠ 0) :
    cs2 mu mup u = 1 / (1 + u * mup / mu) := by
  unfold cs2
  have hden2 : 1 + u * mup / mu ≠ 0 := by
    intro h0
    have hmul : (1 + u * mup / mu) * mu = 0 := by rw [h0]; ring
    field_simp [hmu] at hmul
    exact hden hmul
  field_simp [hmu, hden, hden2]

/-! ## 1. Health <=> positivity + monotonicity of mu -/

/-- (ii)+(iii): mu > 0 and mu' >= 0 give 0 <= c_s^2. -/
theorem cs2_nonneg (mu mup u : ℝ) (hmu : 0 ≤ mu) (hden : 0 < mu + u * mup) :
    0 ≤ cs2 mu mup u := by
  unfold cs2
  exact div_nonneg hmu (le_of_lt hden)

/-- (i): mu' >= 0 is exactly subluminality. -/
theorem cs2_le_one_of_mono (mu mup u : ℝ) (hu : 0 ≤ u) (hmup : 0 ≤ mup)
    (hden : 0 < mu + u * mup) :
    cs2 mu mup u ≤ 1 := by
  unfold cs2
  rw [div_le_one hden]
  nlinarith [mul_nonneg hu hmup]

/-- Converse: subluminality at a point with u > 0 forces mu' >= 0.
    Health is therefore EQUIVALENT to mu' >= 0 (plus mu > 0). -/
theorem mono_of_cs2_le_one (mu mup u : ℝ) (hu : 0 < u)
    (hden : 0 < mu + u * mup) (hle : cs2 mu mup u ≤ 1) :
    0 ≤ mup := by
  unfold cs2 at hle
  rw [div_le_one hden] at hle
  nlinarith

/-- HEALTH DICHOTOMY.  On u > 0 with a positive denominator,
    0 <= c_s^2 <= 1  <=>  mu > 0 and mu' >= 0.  The value of the deep slope
    n does not occur in either side. -/
theorem health_iff_mono (mu mup u : ℝ) (hu : 0 < u) (hden : 0 < mu + u * mup) :
    (0 ≤ cs2 mu mup u ∧ cs2 mu mup u ≤ 1) ↔ (0 ≤ mu ∧ 0 ≤ mup) := by
  constructor
  · intro h
    constructor
    · by_contra hm
      have hmneg : mu < 0 := by linarith
      have hnumneg : mu / (mu + u * mup) < 0 := div_neg_of_neg_of_pos hmneg hden
      unfold cs2 at h
      linarith
    · exact mono_of_cs2_le_one mu mup u hu hden h.2
  · intro h
    exact ⟨cs2_nonneg mu mup u h.1 hden,
           cs2_le_one_of_mono mu mup u (le_of_lt hu) h.2 hden⟩

/-! ## 2. The deep end: the universal sound speed 1/2 -/

/-- If the deep regime is mu = A u^q, the exact sound speed is 1/(1+q):
    A u^q / (A u^q + u * A q u^(q-1)) = 1/(1+q).  Certified for q = 1, 2, 3. -/
theorem deep_cs2_q1 (A u : ℝ) (hA : A ≠ 0) (hu : u ≠ 0) :
    (A * u) / (A * u + u * A) = (1 / 2 : ℝ) := by
  field_simp [hA, hu]
  ring

theorem deep_cs2_q2 (A u : ℝ) (hA : A ≠ 0) (hu : u ≠ 0) :
    (A * u ^ 2) / (A * u ^ 2 + u * (2 * A * u)) = (1 / 3 : ℝ) := by
  field_simp [hA, hu]
  ring

theorem deep_cs2_q3 (A u : ℝ) (hA : A ≠ 0) (hu : u ≠ 0) :
    (A * u ^ 3) / (A * u ^ 3 + u * (3 * A * u ^ 2)) = (1 / 4 : ℝ) := by
  field_simp [hA, hu]
  ring

/-- THE UNIVERSAL DEEP SOUND SPEED.  In the linear (MOND) regime mu = A u the
    sound speed is exactly 1/2 for EVERY amplitude A -- in particular for
    every value of n.  Condition (iv) (finite, non-zero deep slope, i.e.
    q = 1) therefore FORCES c_s^2(0) = 1/2 and simultaneously shows that
    c_s^2(0) cannot distinguish n. -/
theorem deep_cs2_universal_half (A u : ℝ) (hA : A ≠ 0) (hu : u ≠ 0) :
    cs2 (A * u) A u = (1 / 2 : ℝ) := by
  unfold cs2
  exact deep_cs2_q1 A u hA hu

/-! ## 3. A healthy family with ARBITRARY deep slope:  the falsification of
       "health forces n = 2". -/

/-- mu_n(u) = 1 - (1+u)^(-n) for n = 1, 2, 3.  Each has mu(0) = 0 (a MOND
    regime), mu(infinity) = 1 (Newtonian), and deep slope n. -/
def mu1 (u : ℝ) : ℝ := 1 - 1 / (1 + u)
def mu2 (u : ℝ) : ℝ := 1 - 1 / (1 + u) ^ 2
def mu3 (u : ℝ) : ℝ := 1 - 1 / (1 + u) ^ 3

/-- Their derivatives. -/
def dmu1 (u : ℝ) : ℝ := 1 / (1 + u) ^ 2
def dmu2 (u : ℝ) : ℝ := 2 / (1 + u) ^ 3
def dmu3 (u : ℝ) : ℝ := 3 / (1 + u) ^ 4

/-- The resulting sound speeds, closed form. -/
def cs2_1 (u : ℝ) : ℝ := (u + 1) / (u + 2)
def cs2_2 (u : ℝ) : ℝ := ((u + 1) * (u + 2)) / (u ^ 2 + 3 * u + 4)
def cs2_3 (u : ℝ) : ℝ := ((u + 1) * (u ^ 2 + 3 * u + 3)) / (u ^ 3 + 4 * u ^ 2 + 6 * u + 6)

/-- mu2 = u(2+u)/(1+u)^2 -- the programme's kernel. -/
theorem mu2_kernel (u : ℝ) (hv : 1 + u ≠ 0) :
    mu2 u = u * (2 + u) / (1 + u) ^ 2 := by
  unfold mu2
  field_simp [hv]
  ring_nf

/-- The slope mu2(u)/u, and its value at u = 0: the deep slope is 2. -/
theorem mu2_slope (u : ℝ) (hu : u ≠ 0) (hv : 1 + u ≠ 0) :
    mu2 u / u = (2 + u) / (1 + u) ^ 2 := by
  rw [mu2_kernel u hv]
  field_simp [hu]

/-- The slope mu1(u)/u, and its value at u = 0: the deep slope is 1. -/
theorem mu1_slope (u : ℝ) (hu : u ≠ 0) (hv : 1 + u ≠ 0) :
    mu1 u / u = 1 / (1 + u) := by
  unfold mu1
  field_simp [hu, hv]
  ring

/-- The slope mu3(u)/u, and its value at u = 0: the deep slope is 3. -/
theorem mu3_slope (u : ℝ) (hu : u ≠ 0) (hv : 1 + u ≠ 0) :
    mu3 u / u = (3 + 3 * u + u ^ 2) / (1 + u) ^ 3 := by
  unfold mu3
  field_simp [hu, hv]
  ring

/-- The three slopes are distinct integers: 1, 2, 3. -/
theorem slopes_are_1_2_3 :
    ((fun u : ℝ => (1 : ℝ) / (1 + u)) 0) = 1 ∧
    ((fun u : ℝ => (2 + u) / (1 + u) ^ 2) 0) = 2 ∧
    ((fun u : ℝ => (3 + 3 * u + u ^ 2) / (1 + u) ^ 3) 0) = 3 := by
  norm_num

/-- No ghost: mu > 0 for u > 0, for each of the three. -/
theorem mu1_pos (u : ℝ) (hu : 0 < u) : 0 < mu1 u := by
  unfold mu1
  have hv : 0 < 1 + u := by linarith
  have hlt : 1 / (1 + u) < 1 := by
    rw [div_lt_one hv]
    linarith
  linarith

theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < mu2 u := by
  rw [mu2_kernel u (by linarith : 1 + u ≠ 0)]
  positivity

theorem mu3_pos (u : ℝ) (hu : 0 < u) : 0 < mu3 u := by
  unfold mu3
  have hv : 1 < 1 + u := by linarith
  have hv0 : 0 < 1 + u := by linarith
  have hp : 1 < (1 + u) ^ 3 := by nlinarith [sq_pos_of_pos hv0]
  have hlt : 1 / (1 + u) ^ 3 < 1 := by
    rw [div_lt_one (by linarith : 0 < (1 + u) ^ 3)]
    exact hp
  linarith

/-- Monotone (equivalently: no superluminality): mu' > 0 for u > 0. -/
theorem dmu1_pos (u : ℝ) (hu : 0 < u) : 0 < dmu1 u := by
  unfold dmu1
  positivity

theorem dmu2_pos (u : ℝ) (hu : 0 < u) : 0 < dmu2 u := by
  unfold dmu2
  positivity

theorem dmu3_pos (u : ℝ) (hu : 0 < u) : 0 < dmu3 u := by
  unfold dmu3
  positivity

/-- The sound speeds of the three members, in [1/2, 1), for u >= 0.
    All three are healthy -- with three DIFFERENT deep slopes. -/
theorem cs2_1_bounds (u : ℝ) (hu : 0 ≤ u) :
    (1 / 2 : ℝ) ≤ cs2_1 u ∧ cs2_1 u < 1 := by
  unfold cs2_1
  have hden : 0 < u + 2 := by linarith
  constructor
  · rw [le_div_iff₀ hden]
    nlinarith
  · rw [div_lt_iff₀ hden]
    nlinarith

theorem cs2_2_bounds (u : ℝ) (hu : 0 ≤ u) :
    (1 / 2 : ℝ) ≤ cs2_2 u ∧ cs2_2 u < 1 := by
  unfold cs2_2
  have hden : 0 < u ^ 2 + 3 * u + 4 := by nlinarith [sq_nonneg u]
  constructor
  · rw [le_div_iff₀ hden]
    nlinarith [sq_nonneg u]
  · rw [div_lt_iff₀ hden]
    nlinarith

theorem cs2_3_bounds (u : ℝ) (hu : 0 ≤ u) :
    (1 / 2 : ℝ) ≤ cs2_3 u ∧ cs2_3 u < 1 := by
  unfold cs2_3
  have hden : 0 < u ^ 3 + 4 * u ^ 2 + 6 * u + 6 := by
    nlinarith [sq_nonneg u, mul_nonneg (sq_nonneg u) hu]
  constructor
  · rw [le_div_iff₀ hden]
    nlinarith [sq_nonneg u, mul_nonneg (sq_nonneg u) hu]
  · rw [div_lt_iff₀ hden]
    nlinarith [sq_nonneg u, mul_nonneg (sq_nonneg u) hu]

/-- The closed-form sound speeds ARE the sound speeds of these kernels:
    cs2 (mu_k u) (mu_k'(u)) u = cs2_k u.  (The identification of dmu_k with
    the derivative of mu_k is textbook calculus, checked symbolically in
    H046_is_n_two_forced_by_health.py; here it is the algebraic identity.) -/
theorem cs2_mu1_eq (u : ℝ) (hu : 0 < u) : cs2 (mu1 u) (dmu1 u) u = cs2_1 u := by
  unfold cs2 cs2_1
  have hd : mu1 u + u * dmu1 u ≠ 0 := by
    have hm : 0 < mu1 u := mu1_pos u hu
    have hdp : 0 < u * dmu1 u := by unfold dmu1; positivity
    linarith
  have h2 : u + 2 ≠ 0 := by linarith
  rw [div_eq_div_iff hd h2]
  unfold mu1 dmu1
  have h1 : 1 + u ≠ 0 := by linarith
  field_simp [h1]
  ring

theorem cs2_mu2_eq (u : ℝ) (hu : 0 < u) : cs2 (mu2 u) (dmu2 u) u = cs2_2 u := by
  unfold cs2 cs2_2
  have hd : mu2 u + u * dmu2 u ≠ 0 := by
    have hm : 0 < mu2 u := mu2_pos u hu
    have hdp : 0 < u * dmu2 u := by unfold dmu2; positivity
    linarith
  have h2 : u ^ 2 + 3 * u + 4 ≠ 0 := by nlinarith [sq_nonneg u]
  rw [div_eq_div_iff hd h2]
  unfold mu2 dmu2
  have h1 : 1 + u ≠ 0 := by linarith
  field_simp [h1]
  ring

theorem cs2_mu3_eq (u : ℝ) (hu : 0 < u) : cs2 (mu3 u) (dmu3 u) u = cs2_3 u := by
  unfold cs2 cs2_3
  have hd : mu3 u + u * dmu3 u ≠ 0 := by
    have hm : 0 < mu3 u := mu3_pos u hu
    have hdp : 0 < u * dmu3 u := by unfold dmu3; positivity
    linarith
  have h2 : u ^ 3 + 4 * u ^ 2 + 6 * u + 6 ≠ 0 := by
    have h3 : 0 ≤ u ^ 3 := by positivity
    nlinarith [sq_nonneg u, h3]
  rw [div_eq_div_iff hd h2]
  unfold mu3 dmu3
  have h1 : 1 + u ≠ 0 := by linarith
  field_simp [h1]
  ring

/-- Monotonicity (the health content: mu' >= 0), proved without calculus. -/
theorem mu2_mono (u v : ℝ) (hu : 0 ≤ u) (huv : u ≤ v) : mu2 u ≤ mu2 v := by
  unfold mu2
  have h1u : 0 < 1 + u := by linarith
  have h1v : 0 < 1 + v := by linarith
  have hs : (1 + u) ^ 2 ≤ (1 + v) ^ 2 := by
    exact pow_le_pow_left₀ (by linarith : 0 ≤ 1 + u) (by linarith : 1 + u ≤ 1 + v) 2
  have hp : 0 < (1 + u) ^ 2 := by positivity
  have hrec : (1 : ℝ) / (1 + v) ^ 2 ≤ 1 / (1 + u) ^ 2 :=
    one_div_le_one_div_of_le hp hs
  linarith

theorem mu3_mono (u v : ℝ) (hu : 0 ≤ u) (huv : u ≤ v) : mu3 u ≤ mu3 v := by
  unfold mu3
  have h1u : 0 < 1 + u := by linarith
  have hs : (1 + u) ^ 3 ≤ (1 + v) ^ 3 := by
    exact pow_le_pow_left₀ (by linarith : 0 ≤ 1 + u) (by linarith : 1 + u ≤ 1 + v) 3
  have hp : 0 < (1 + u) ^ 3 := by positivity
  have hrec : (1 : ℝ) / (1 + v) ^ 3 ≤ 1 / (1 + u) ^ 3 :=
    one_div_le_one_div_of_le hp hs
  linarith

/-- THE DEEP SLOPE AS A GENUINE LIMIT.  lim_{u -> 0+} mu_k(u)/u = k for
    k = 1, 2, 3: three different deep slopes, all from healthy kernels. -/
theorem deep_slope_mu1 :
    Tendsto (fun u : ℝ => mu1 u / u) (nhdsWithin (0 : ℝ) (Ioi 0)) (𝓝 (1 : ℝ)) := by
  have hEq : (fun u : ℝ => mu1 u / u) =ᶠ[nhdsWithin (0 : ℝ) (Ioi 0)]
      (fun u : ℝ => (1 : ℝ) / (1 + u)) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu_pos : 0 < u := hu
    exact mu1_slope u (ne_of_gt hu_pos) (by linarith : 1 + u ≠ 0)
  have hcont : ContinuousAt (fun u : ℝ => (1 : ℝ) / (1 + u)) 0 := by
    fun_prop (disch := norm_num)
  have hlim := (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm
  simpa using hlim

theorem deep_slope_mu2 :
    Tendsto (fun u : ℝ => mu2 u / u) (nhdsWithin (0 : ℝ) (Ioi 0)) (𝓝 (2 : ℝ)) := by
  have hEq : (fun u : ℝ => mu2 u / u) =ᶠ[nhdsWithin (0 : ℝ) (Ioi 0)]
      (fun u : ℝ => (2 + u) / (1 + u) ^ 2) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu_pos : 0 < u := hu
    exact mu2_slope u (ne_of_gt hu_pos) (by linarith : 1 + u ≠ 0)
  have hcont : ContinuousAt (fun u : ℝ => (2 + u) / (1 + u) ^ 2) 0 := by
    fun_prop (disch := norm_num)
  have hlim := (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm
  simpa using hlim

theorem deep_slope_mu3 :
    Tendsto (fun u : ℝ => mu3 u / u) (nhdsWithin (0 : ℝ) (Ioi 0)) (𝓝 (3 : ℝ)) := by
  have hEq : (fun u : ℝ => mu3 u / u) =ᶠ[nhdsWithin (0 : ℝ) (Ioi 0)]
      (fun u : ℝ => (3 + 3 * u + u ^ 2) / (1 + u) ^ 3) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu_pos : 0 < u := hu
    exact mu3_slope u (ne_of_gt hu_pos) (by linarith : 1 + u ≠ 0)
  have hcont : ContinuousAt (fun u : ℝ => (3 + 3 * u + u ^ 2) / (1 + u) ^ 3) 0 := by
    fun_prop (disch := norm_num)
  have hlim := (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm
  simpa using hlim

/-- The programme's own kernel has deep sound speed exactly 1/2 as a limit:
    the universal value, independent of n. -/
theorem deep_cs2_mu2_is_half :
    Tendsto (fun u : ℝ => cs2 (mu2 u) (dmu2 u) u)
      (nhdsWithin (0 : ℝ) (Ioi 0)) (𝓝 (cs2_2 0)) := by
  have hEq : (fun u : ℝ => cs2 (mu2 u) (dmu2 u) u) =ᶠ[nhdsWithin (0 : ℝ) (Ioi 0)]
      (fun u : ℝ => cs2_2 u) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu_pos : 0 < u := hu
    exact cs2_mu2_eq u hu_pos
  have hcont : ContinuousAt cs2_2 0 := by
    unfold cs2_2
    fun_prop (disch := norm_num)
  exact (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm

/-- The deep sound speed of the programme's own kernel is exactly 1/2. -/
theorem cs2_2_at_zero : cs2_2 0 = (1 : ℝ) / 2 := by
  norm_num [cs2_2]

/-- THE NEGATIVE RESULT.  n = 1, n = 2 and n = 3 are all realized by
    strictly positive, strictly monotone kernels whose sound speed lies in
    [1/2, 1) for every u >= 0.  Hence conditions (i)-(iv) are satisfied for
    at least three different values of n: health does NOT force n = 2. -/
theorem n_not_forced_by_health :
    (∀ u : ℝ, 0 < u → 0 < mu1 u ∧ 0 < dmu1 u) ∧
    (∀ u : ℝ, 0 < u → 0 < mu2 u ∧ 0 < dmu2 u) ∧
    (∀ u : ℝ, 0 < u → 0 < mu3 u ∧ 0 < dmu3 u) ∧
    (∀ u : ℝ, 0 ≤ u → (1 / 2 : ℝ) ≤ cs2_1 u ∧ cs2_1 u < 1) ∧
    (∀ u : ℝ, 0 ≤ u → (1 / 2 : ℝ) ≤ cs2_2 u ∧ cs2_2 u < 1) ∧
    (∀ u : ℝ, 0 ≤ u → (1 / 2 : ℝ) ≤ cs2_3 u ∧ cs2_3 u < 1) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro u hu; exact ⟨mu1_pos u hu, dmu1_pos u hu⟩
  · intro u hu; exact ⟨mu2_pos u hu, dmu2_pos u hu⟩
  · intro u hu; exact ⟨mu3_pos u hu, dmu3_pos u hu⟩
  · intro u hu; exact cs2_1_bounds u hu
  · intro u hu; exact cs2_2_bounds u hu
  · intro u hu; exact cs2_3_bounds u hu

/-- A SECOND degeneracy: even at FIXED n = 2 the functional form is not
    forced by health.  mu(u) = 2u/(1+2u) has the same deep slope 2, is
    strictly positive and monotone, and has sound speed (1+2u)/(2+2u) in
    [1/2,1) -- a DIFFERENT function from the programme's
    (u^2+3u+2)/(u^2+3u+4). -/
def alt2 (u : ℝ) : ℝ := 2 * u / (1 + 2 * u)
def cs2_alt2 (u : ℝ) : ℝ := (1 + 2 * u) / (2 + 2 * u)

theorem alt2_pos (u : ℝ) (hu : 0 < u) : 0 < alt2 u := by
  unfold alt2
  positivity

theorem cs2_alt2_bounds (u : ℝ) (hu : 0 ≤ u) :
    (1 / 2 : ℝ) ≤ cs2_alt2 u ∧ cs2_alt2 u < 1 := by
  unfold cs2_alt2
  have hden : 0 < 2 + 2 * u := by linarith
  constructor
  · rw [le_div_iff₀ hden]
    nlinarith
  · rw [div_lt_iff₀ hden]
    nlinarith

/-- The two n = 2 kernels differ: health fixes neither the slope nor the shape. -/
theorem two_healthy_n2_kernels_differ :
    mu2 1 ≠ alt2 1 := by
  unfold mu2 alt2
  norm_num

/-! ## 4. The sharp bound inside the minimal Padé family -/

/-- mu = u(a+u)/(1+u)^2 -- the family forced by mu(0)=0, mu(infinity)=1 and a
    minimal double pole at u = -1.  Its sound speed:
        c_s^2 = (u^2 + (a+1)u + a) / (u^2 + 3u + 2a). -/
def cs2a (a u : ℝ) : ℝ := (u ^ 2 + (a + 1) * u + a) / (u ^ 2 + 3 * u + 2 * a)

/-- 1 - c_s^2 = (a + 2u - a u)/(u^2+3u+2a):  the superluminality numerator. -/
theorem cs2a_subluminal_numerator (a u : ℝ) (hden : u ^ 2 + 3 * u + 2 * a ≠ 0) :
    1 - cs2a a u = (a + 2 * u - a * u) / (u ^ 2 + 3 * u + 2 * a) := by
  unfold cs2a
  apply mul_left_cancel₀ hden
  have hden3 : u * (u + 3) + 2 * a ≠ 0 := by
    intro h0
    apply hden
    nlinarith
  field_simp [hden, hden3]
  ring_nf

/-- SHARP BOUND.  If a member of this family is subluminal for every u >= 0,
    then its deep slope a satisfies a <= 2.  (Proof: for a > 2 the numerator
    a + 2u - a u is negative at u = 2a/(a-2) + 1.)
    SCOPE: this is a bound inside the family, not a derivation of a = 2; the
    observed a = 2 SATURATES it. -/
theorem subluminal_forces_slope_le_two (a : ℝ)
    (hsub : ∀ u : ℝ, 0 ≤ u → cs2a a u ≤ 1) : a ≤ 2 := by
  by_contra h
  have ha : 2 < a := by linarith
  have ha2pos : 0 < a - 2 := by linarith
  have hapos : 0 < a := by linarith
  let u : ℝ := 2 * a / (a - 2) + 1
  have hu : 0 ≤ u := by
    have hfrac : 0 < 2 * a / (a - 2) := by positivity
    unfold u
    linarith
  have hdenpos : 0 < u ^ 2 + 3 * u + 2 * a := by
    nlinarith [sq_nonneg u, hu, hapos]
  have hnumneg : a + 2 * u - a * u < 0 := by
    unfold u
    field_simp [ne_of_gt ha2pos]
    nlinarith
  have hneg : 1 - cs2a a u < 0 := by
    rw [cs2a_subluminal_numerator a u (ne_of_gt hdenpos)]
    exact div_neg_of_neg_of_pos hnumneg hdenpos
  have hgt : 1 < cs2a a u := by linarith
  have hle := hsub u hu
  linarith

/-- Positivity of c_s^2 in the same family forces a >= 0, so health confines
    the deep slope to 0 <= a <= 2. -/
theorem cs2a_nonneg_numerator (a u : ℝ) (ha : 0 ≤ a) (hu : 0 ≤ u) :
    0 ≤ u ^ 2 + (a + 1) * u + a := by
  nlinarith [sq_nonneg u, mul_nonneg hu (by linarith : 0 ≤ a + 1)]

/-! ## 5. What does fix the 2:  regularity + the existence of a MOND regime -/

/-- f'(K) for f = K - c ln(1+sqrt K) - d/(1+sqrt K), written in u = sqrt K. -/
def fp_cd (c d u : ℝ) : ℝ := 1 - c / (2 * u * (1 + u)) + d / (2 * u * (1 + u) ^ 2)

/-- THE RESIDUE IDENTITY.  u (f'(K) - 1) = (d - c - c u) / (2 (1+u)^2).
    As u -> 0 the left side vanishes whenever f' is finite at K = 0, so the
    right side must vanish too:  d = c.  Smoothness of f' at the vacuum
    forces the coefficient of the logarithm to equal the coefficient of
    1/(1+sqrt K). -/
theorem fp_cd_residue (c d u : ℝ) (hu : u ≠ 0) (hv : 1 + u ≠ 0) :
    u * (fp_cd c d u - 1) = (d - c - c * u) / (2 * (1 + u) ^ 2) := by
  unfold fp_cd
  field_simp [hu, hv]
  ring

/-- With d = c the pole cancels exactly:  f'(K) = 1 - c/(2(1+sqrt K)^2). -/
def fp_reg (c u : ℝ) : ℝ := 1 - c / (2 * (1 + u) ^ 2)

theorem fp_cd_of_equal_coeffs (c u : ℝ) (hu : u ≠ 0) (hv : 1 + u ≠ 0) :
    fp_cd c c u = fp_reg c u := by
  unfold fp_cd fp_reg
  field_simp [hu, hv]
  ring

/-- The pole form: the residue (d - c) sits on an explicit 1/u. -/
theorem fp_cd_pole (c d u : ℝ) (hu : u ≠ 0) (hv : 1 + u ≠ 0) :
    fp_cd c d u = fp_reg c u + (d - c) / (2 * u * (1 + u) ^ 2) := by
  unfold fp_cd fp_reg
  field_simp [hu, hv]
  ring

/-- At u = 0 the regularized f' is 1 - c/2. -/
theorem fp_reg_at_zero (c : ℝ) : fp_reg c 0 = 1 - c / 2 := by
  unfold fp_reg
  norm_num

/-- (beta) A MOND regime means no Newtonian floor: mu(0) = f'(0) = 0.
    With d = c this forces c = 2. -/
theorem no_newtonian_floor_forces_c_two (c : ℝ) (h : fp_reg c 0 = 0) : c = 2 := by
  rw [fp_reg_at_zero] at h
  linarith

/-- (gamma) At c = 2 the regularized kernel IS the programme's kernel mu2,
    whose deep slope is 2.  So the integer 2 follows from regularity plus the
    existence of a MOND regime -- not from health. -/
theorem c_two_gives_mu2 (u : ℝ) (hv : 1 + u ≠ 0) : fp_reg 2 u = mu2 u := by
  unfold fp_reg mu2
  field_simp [hv]

/-- For c /= 2 the kernel has a Newtonian floor mu(0) = 1 - c/2 /= 0, and the
    deep slope mu(u)/u diverges: the MOND regime is destroyed. -/
theorem floor_nonzero_if_c_ne_two (c : ℝ) (hc : c ≠ 2) : 1 - c / 2 ≠ 0 := by
  intro h
  apply hc
  linarith

/-! ## The spine -/

/-- THE SPINE.  (1) health is exactly mu > 0 and mu' >= 0 -- a condition on the
    LOG-SLOPE, blind to the amplitude n; (2) condition (iv) forces the deep
    sound speed to be exactly 1/2 for every n; (3) three kernels with deep
    slopes 1, 2 and 3 are all healthy, so n = 2 is NOT forced by
    (i)-(iv); (4) inside the minimal Padé family health gives the sharp bound
    n <= 2, saturated by the observed value; (5) what does force the 2 is
    regularity of f' at K = 0 (which makes the two coefficients equal) plus
    the absence of a Newtonian floor -- a phenomelogical, not a health,
    input. -/
theorem n_two_not_forced_spine :
    (∀ (mu mup u : ℝ), 0 < u → 0 < mu + u * mup →
      ((0 ≤ cs2 mu mup u ∧ cs2 mu mup u ≤ 1) ↔ (0 ≤ mu ∧ 0 ≤ mup))) ∧
    (∀ (A u : ℝ), A ≠ 0 → u ≠ 0 → cs2 (A * u) A u = (1 / 2 : ℝ)) ∧
    (∀ u : ℝ, 0 ≤ u → (1 / 2 : ℝ) ≤ cs2_1 u ∧ cs2_1 u < 1) ∧
    (∀ u : ℝ, 0 ≤ u → (1 / 2 : ℝ) ≤ cs2_2 u ∧ cs2_2 u < 1) ∧
    (∀ u : ℝ, 0 ≤ u → (1 / 2 : ℝ) ≤ cs2_3 u ∧ cs2_3 u < 1) ∧
    (∀ a : ℝ, (∀ u : ℝ, 0 ≤ u → cs2a a u ≤ 1) → a ≤ 2) ∧
    (∀ c : ℝ, fp_reg c 0 = 0 → c = 2) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro mu mup u hu hden; exact health_iff_mono mu mup u hu hden
  · intro A u hA hu; exact deep_cs2_universal_half A u hA hu
  · intro u hu; exact cs2_1_bounds u hu
  · intro u hu; exact cs2_2_bounds u hu
  · intro u hu; exact cs2_3_bounds u hu
  · intro a h; exact subluminal_forces_slope_le_two a h
  · intro c h; exact no_newtonian_floor_forces_c_two c h

#print axioms cs2_logslope
#print axioms health_iff_mono
#print axioms deep_cs2_universal_half
#print axioms n_not_forced_by_health
#print axioms subluminal_forces_slope_le_two
#print axioms fp_cd_residue
#print axioms fp_cd_pole
#print axioms no_newtonian_floor_forces_c_two
#print axioms n_two_not_forced_spine

end H046

end
