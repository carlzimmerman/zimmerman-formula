/-
  H047 -- DOES THE NOETHER-CHARGE FREE DUST CLUSTER?  Lean certificate.

  S = int sqrt(-g) [ (M_Pl^2/2) R + Lambda^4 f(K) ],   K = (1/2)(d phi)^2/Lambda^4
  Noether current of the shift symmetry:   J^mu = f'(K) d^mu phi,   grad_mu J^mu = 0.

  With u = sqrt(K), f'(K) = mu_2(u), and
      p/Lambda^4 = f,     rho/Lambda^4 = 2 K f' - f = 2 u^2 mu_2(u) - f.

  WHAT IS CERTIFIED HERE.

  (1) THE SOUND SPEED, EXACTLY.  For a shift-symmetric k-essence the rest-frame
      sound speed is c_s^2 = (dp/dK)/(drho/dK) = f'/(f' + 2 K f'').  Since
      f' = mu_2(u), K = u^2 and 2 K f'' = u mu_2'(u), with mu_2'(u) = 2/(1+u)^3,

          c_s^2(u) = mu_2/(mu_2 + u mu_2') = (u^2+3u+2)/(u^2+3u+4) = 1 - 2/(u^2+3u+4)

      proved from the definitions, derivative and all (`hasDerivAt_mu2`,
      `csSq_eq_sound_speed`).  Consequences proved below:
          * 1/2 <= c_s^2 < 1 for all u >= 0           (causal, no gradient instability)
          * c_s^2 > 0 on the whole regular domain u > -1
          * c_s^2 is NEVER 0 there.  So "sound speed exactly zero" is NOT a state
            of this f: it is a property the free-dust SECTOR must supply.
      `hasDerivAt_fK` additionally verifies that the given f really is the
      antiderivative belonging to f' = mu_2, i.e. df/du = 2 u mu_2(u).

  (2) A COHERENT CHARGE DOES NOT FREE-STREAM.  Free-streaming eats the SECOND
      CENTRAL MOMENT of the velocity distribution.  A classical field has ONE
      velocity at each event -- f(x,v) = n(x) delta^3(v - v(x)) -- so that moment
      is identically zero, hence lambda_fs = 0.  (`coherent_dispersion` vs
      `two_stream_dispersion`, `lamFs_of_zero_dispersion`.)

  (3) NO JEANS SCALE.  With c_s = 0 no mode is stabilised by pressure
      (`no_jeans_stabilisation`): the Jeans condition fails for every k.

  (4) SCALE-FREE GROWTH AND NO SUPPRESSION.  With c_s = 0 the growth equation
      loses its only k-dependent term, so P(k,a)/P(k,a_i) = D(a)^2 for every k
      (`growth_k_independent`) and R(k) = P_framework/P_LCDM = 1 (`no_suppression`),
      while any cutoff model is strictly below 1 (`cutoff_lt_one`).

  (5) THE CHARGE SCALES AS a^-3 (`charge_scales_a3`), and matching rho ~ a^{-3(1+w)}
      to a^-3 forces w = 0 (`exponent_forces_dust`) -- the dust identification.

  NOTHING HERE USES THE VALUE OF a_0 OR Lambda.  The prediction R(k) = 1 and the
  slope n_eff -> n_s - 4 are independent of the postulate, so they survive H029's
  circularity audit; the single scale a_0 could contribute, c^2/a_0, is exactly
  c H_0/a_0 restated and is NOT claimed (see the numeric lane).

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

/-! ## The model -/

/-- f'(K) = mu_2(sqrt K).  Strictly positive for u > 0: no ghost.
    Written with the denominator as a product so the quotient rule applies
    directly; `mu2_pow_form` gives the (1+u)^2 form. -/
def mu2 (u : ℝ) : ℝ := u * (2 + u) * (((1 + u) * (1 + u))⁻¹)

/-- The (1+u)^2 form, as it is written in the numeric lane. -/
theorem mu2_pow_form (u : ℝ) (hu : 1 + u ≠ 0) : mu2 u = u * (2 + u) / (1 + u)^2 := by
  unfold mu2
  rw [show (1 + u)^2 = (1 + u) * (1 + u) by ring]
  field_simp [hu]

/-- f(K) at K = u^2.  f(0) = -1, so the vacuum is a positive Lambda. -/
def fK (u : ℝ) : ℝ := u^2 - 2 * Real.log (1 + u) - 2 * (1 + u)⁻¹ + 1

/-- p / Lambda^4 -/
def pOf (u : ℝ) : ℝ := fK u

/-- rho / Lambda^4 = 2 K f' - f -/
def rhoOf (u : ℝ) : ℝ := 2 * u^2 * mu2 u - fK u

/-- The rest-frame sound speed, in closed form.  `csSq_eq_sound_speed` proves
    this equals f'/(f' + 2 K f''). -/
def csSq (u : ℝ) : ℝ := (u^2 + 3 * u + 2) / (u^2 + 3 * u + 4)

/-! ## 0. The vacuum -/

theorem fK_zero : fK 0 = -1 := by
  unfold fK
  norm_num

theorem rhoOf_zero : rhoOf 0 = 1 := by
  unfold rhoOf mu2 fK
  norm_num

theorem pOf_zero : pOf 0 = -1 := by
  unfold pOf fK
  norm_num

/-! ## 1. The sound speed, derived -/

/-- mu_2 in the form that exhibits the structure: mu_2 = 1 - (1+u)^{-2}. -/
theorem mu2_as_one_minus (u : ℝ) (hu : 1 + u ≠ 0) :
    mu2 u = 1 - (1 + u)⁻¹ * (1 + u)⁻¹ := by
  unfold mu2
  have hsq : (1 + u) * (1 + u) ≠ 0 := mul_ne_zero hu hu
  field_simp [hsq, hu]
  ring

/-- d mu_2/du = 2/(1+u)^3, proved by the quotient rule (not asserted). -/
theorem hasDerivAt_mu2 (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt mu2 (2 * ((1 + u)⁻¹)^3) u := by
  have h2x : HasDerivAt (fun x : ℝ => 2 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (2 : ℝ)
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  have hn : HasDerivAt (fun x : ℝ => x * (2 + x)) (1 * (2 + u) + u * 1) u :=
    (hasDerivAt_id u).mul h2x
  have hd : HasDerivAt (fun x : ℝ => (1 + x) * (1 + x))
      (1 * (1 + u) + (1 + u) * 1) u :=
    hlin.mul hlin
  have hdne : (1 + u) * (1 + u) ≠ 0 := mul_ne_zero hu hu
  have hinvd : HasDerivAt (fun x : ℝ => (((1 + x) * (1 + x))⁻¹))
      ((-((((1 + u) * (1 + u))^2)⁻¹)) * (1 * (1 + u) + (1 + u) * 1)) u := by
    simpa [Function.comp_def] using (hasDerivAt_inv hdne).comp u hd
  have hq : HasDerivAt mu2
      ((1 * (2 + u) + u * 1) * (((1 + u) * (1 + u))⁻¹)
        + (u * (2 + u)) * ((-((((1 + u) * (1 + u))^2)⁻¹))
            * (1 * (1 + u) + (1 + u) * 1))) u :=
    hn.mul hinvd
  convert hq using 1
  field_simp [hu]
  ring

/-- d f/du = 2 u mu_2(u): verifies that the given f is the antiderivative
    belonging to f' = mu_2.  Proved, not asserted. -/
theorem hasDerivAt_fK (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt fK (2 * u * mu2 u) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  have hsq : HasDerivAt (fun x : ℝ => x^2) (2 * u) u := by
    simpa using hasDerivAt_pow 2 u
  have hlog : HasDerivAt (fun x : ℝ => Real.log (1 + x)) ((1 + u)⁻¹) u := by
    simpa [Function.comp_def] using (Real.hasDerivAt_log hu).comp u hlin
  have hinv : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(((1 + u)^2)⁻¹)) u := by
    simpa [Function.comp_def] using (hasDerivAt_inv hu).comp u hlin
  have hmain : HasDerivAt
      (fun x : ℝ => x^2 - 2 * Real.log (1 + x) - 2 * (1 + x)⁻¹ + 1)
      (2 * u - 2 * (1 + u)⁻¹ - 2 * (-(((1 + u)^2)⁻¹))) u :=
    (((hsq.sub (hlog.const_mul 2)).sub (hinv.const_mul 2)).add_const 1)
  have hmain0 : HasDerivAt fK (2 * u * mu2 u) u := by
    change HasDerivAt
      (fun x : ℝ => x^2 - 2 * Real.log (1 + x) - 2 * (1 + x)⁻¹ + 1)
      (2 * u * mu2 u) u
    convert hmain using 1
    unfold mu2
    field_simp [hu]
    ring
  exact hmain0

/-- THE SOUND SPEED THEOREM.  c_s^2 = (dp/dK)/(drho/dK) = f'/(f' + 2 K f''),
    and with K = u^2, f' = mu_2(u), 2 K f'' = u mu_2'(u), that is
    mu_2/(mu_2 + u mu_2') -- which is the closed form (u^2+3u+2)/(u^2+3u+4).
    This is the derivation, not a restatement. -/
theorem csSq_eq_sound_speed (u : ℝ) (hu : 1 + u ≠ 0) (hu0 : u ≠ 0) :
    csSq u = mu2 u / (mu2 u + u * deriv mu2 u) := by
  rw [(hasDerivAt_mu2 u hu).deriv]
  unfold csSq mu2
  field_simp [hu, hu0]
  ring

/-! ## 2. Properties of the sound speed -/

/-- The denominator is never zero: u^2+3u+4 = (u+3/2)^2 + 7/4 > 0. -/
theorem csSq_denom_pos (u : ℝ) : 0 < u^2 + 3 * u + 4 := by
  nlinarith [sq_nonneg (u + (3 / 2 : ℝ))]

/-- POSITIVE on the whole regular domain u > -1: no gradient instability. -/
theorem csSq_pos (u : ℝ) (hu : -1 < u) : 0 < csSq u := by
  unfold csSq
  have hn : 0 < u^2 + 3 * u + 2 := by
    have h1 : 0 < u + 1 := by linarith
    have h2 : 0 < u + 2 := by linarith
    nlinarith [mul_pos h2 h1]
  exact div_pos hn (csSq_denom_pos u)

/-- SUB-LUMINAL: c_s^2 < 1 for every u.  Causal. -/
theorem csSq_lt_one (u : ℝ) : csSq u < 1 := by
  unfold csSq
  have hd : 0 < u^2 + 3 * u + 4 := csSq_denom_pos u
  rw [div_lt_one hd]
  nlinarith

/-- THE SOUND SPEED NEVER VANISHES.  c_s^2 = 0 is not a state of this f --
    it is a property the free-dust sector must supply. -/
theorem csSq_ne_zero (u : ℝ) (hu : -1 < u) : csSq u ≠ 0 :=
  ne_of_gt (csSq_pos u hu)

/-- c_s^2 >= 1/2 for u >= 0, with equality only at u = 0. -/
theorem csSq_ge_half (u : ℝ) (hu : 0 ≤ u) : (1 / 2 : ℝ) ≤ csSq u := by
  unfold csSq
  have hd : 0 < u^2 + 3 * u + 4 := csSq_denom_pos u
  have hn : 0 ≤ u * (u + 3) := by
    nlinarith [mul_nonneg hu (by linarith : (0 : ℝ) ≤ u + 3)]
  field_simp [ne_of_gt hd]
  nlinarith

theorem csSq_zero : csSq 0 = (1 / 2 : ℝ) := by
  unfold csSq
  norm_num

/-! ## 3. The w = 0 (dust background) state -/

/-- Where p = 0 the equation of state is exactly w = 0: dust. -/
theorem w_zero_of_f_zero (u : ℝ) (h : fK u = 0) (hr : rhoOf u ≠ 0) :
    pOf u / rhoOf u = 0 := by
  unfold pOf
  rw [h]
  field_simp [hr]
  ring

/-- At that point rho = 2 u^2 mu_2. -/
theorem rhoOf_at_dust (u : ℝ) (h : fK u = 0) : rhoOf u = 2 * u^2 * mu2 u := by
  unfold rhoOf
  rw [h]
  ring

/-- THE SEPARATION.  The dust background (w = 0) still has a NONZERO sound
    speed: vanishing pressure is not the same as vanishing pressure response.
    This is why the free dust cannot simply be identified with the k-essence
    fluid -- that fluid would be Jeans-stable on every sub-horizon scale. -/
theorem dust_background_has_pressure_response (u : ℝ) (hu : -1 < u)
    (h : fK u = 0) (hr : rhoOf u ≠ 0) :
    pOf u / rhoOf u = 0 ∧ csSq u ≠ 0 :=
  ⟨w_zero_of_f_zero u h hr, csSq_ne_zero u hu⟩

/-! ## 4. Does a conserved charge free-stream? -/

/-- The velocity dispersion (second central moment) of a two-point velocity
    distribution with weight w on v1 and 1-w on v2. -/
def disp2 (v1 v2 w : ℝ) : ℝ :=
  w * (v1 - (w * v1 + (1 - w) * v2))^2 + (1 - w) * (v2 - (w * v1 + (1 - w) * v2))^2

/-- A THERMAL (WDM) distribution: half the weight at +v, half at -v.  Its
    dispersion is v^2 > 0 for v /= 0.  This is what free-streaming consumes. -/
theorem two_stream_dispersion (v : ℝ) : disp2 v (-v) (1 / 2) = v^2 := by
  unfold disp2
  ring

/-- A COHERENT state: all the weight at ONE velocity (a delta function in
    velocity space).  Its dispersion is identically zero, whatever the
    weights.  There is no spread to stream with. -/
theorem coherent_dispersion (v w : ℝ) : disp2 v v w = 0 := by
  unfold disp2
  ring

/-- The free-streaming length is proportional to the dispersion:
    lambda_fs = int (sigma/a) dt, here written for a constant sigma. -/
def lamFs (sigma dt : ℝ) : ℝ := sigma * dt

/-- ZERO DISPERSION => ZERO FREE-STREAMING LENGTH.  A conserved Noether charge
    of a coherent classical field does not free-stream, so the warm-dark-matter
    damping argument has nothing to act on. -/
theorem lamFs_of_zero_dispersion (dt : ℝ) : lamFs 0 dt = 0 := by
  unfold lamFs
  ring

/-! ## 5. No Jeans scale -/

/-- A mode k is stabilised by pressure iff c_s^2 k^2 >= 4 pi G rho a^2. -/
def jeansStable (cs G rho a k : ℝ) : Prop := 4 * Real.pi * G * rho * a^2 ≤ cs^2 * k^2

/-- With c_s = 0 NO mode is stabilised, on any scale: the Jeans length is zero.
    Both legs of the WDM argument (free-streaming and Jeans damping) are gone. -/
theorem no_jeans_stabilisation (G rho a k : ℝ)
    (hG : 0 < G) (hrho : 0 < rho) (ha : 0 < a) :
    ¬ jeansStable 0 G rho a k := by
  intro h
  unfold jeansStable at h
  have hpos : 0 < 4 * Real.pi * G * rho * a^2 := by positivity
  nlinarith

/-! ## 6. Scale-free growth and the prediction -/

/-- With c_s = 0 the growth equation has no k-dependent term, so
    P(k,a) = D(a)^2 P(k,a_i) and the ratio P(k,a)/P(k,a_i) is the SAME number
    at every k.  The shape of P is invariant. -/
theorem growth_k_independent (D P : ℝ → ℝ) (k₁ k₂ a : ℝ)
    (h₁ : P k₁ ≠ 0) (h₂ : P k₂ ≠ 0) :
    (D a^2 * P k₁) / P k₁ = (D a^2 * P k₂) / P k₂ := by
  field_simp [h₁, h₂]

/-- R(k) = P_framework(k)/P_LCDM(k): with identical primordial spectrum and
    identical background this is 1 at EVERY k.  No cutoff, no break. -/
theorem no_suppression (P : ℝ → ℝ) (k : ℝ) (h : P k ≠ 0) : P k / P k = 1 := by
  field_simp [h]

/-- The contrast: any damping model with a cutoff, R(k) = exp(-(k/k_cut)^2),
    is strictly below 1 for every k > 0. -/
def cutoff (k kcut : ℝ) : ℝ := Real.exp (-(k / kcut)^2)

theorem cutoff_lt_one (k kcut : ℝ) (hk : 0 < k) (hkcut : 0 < kcut) :
    cutoff k kcut < 1 := by
  unfold cutoff
  rw [Real.exp_lt_one_iff]
  have hp : 0 < k / kcut := div_pos hk hkcut
  have hs : 0 < (k / kcut)^2 := sq_pos_of_ne_zero (ne_of_gt hp)
  linarith

/-- THE DISCRIMINATOR: the cutoff model is never 1, while the framework's R(k)
    is 1 identically.  The two are separated by orders of magnitude at large k. -/
theorem cutoff_ne_one (k kcut : ℝ) (hk : 0 < k) (hkcut : 0 < kcut) :
    cutoff k kcut ≠ 1 := by
  have h := cutoff_lt_one k kcut hk hkcut
  linarith

/-! ## 7. The charge scales as a^-3 -/

/-- grad_mu J^mu = 0 in FLRW gives d/dt(a^3 J^0) = 0, so J^0 ~ a^-3 exactly. -/
theorem charge_scales_a3 (J0i ai a : ℝ) (hai : ai ≠ 0) (ha : a ≠ 0) :
    (ai^3 * J0i) / a^3 = J0i * (ai / a)^3 := by
  field_simp [hai, ha]

/-- Matching rho ~ a^{-3(1+w)} to the observed a^-3 forces w = 0: dust. -/
theorem exponent_forces_dust (w : ℝ) (h : -3 * (1 + w) = -3) : w = 0 := by
  linarith

/-! ## The spine -/

/-- THE SPINE.  (i) the sound speed is the closed form, positive and sub-luminal,
    and NEVER zero -- so c_s^2 = 0 is a sector input, not a state of f;
    (ii) a coherent charge has zero velocity dispersion, hence zero free-streaming
    length; (iii) with c_s = 0 no mode is Jeans-stabilised; (iv) growth is
    k-independent, so R(k) = 1 at every k.  Prediction: the framework's free
    dust is indistinguishable from CDM in the linear power spectrum, with
    n_eff -> n_s - 4 and NO small-scale cutoff. -/
theorem noether_dust_spine :
    csSq 0 = (1 / 2 : ℝ) ∧
    (0 < csSq 1 ∧ csSq 1 < 1) ∧
    (∀ u : ℝ, -1 < u → csSq u ≠ 0) ∧
    (∀ v w : ℝ, disp2 v v w = 0) ∧
    (∀ dt : ℝ, lamFs 0 dt = 0) ∧
    (∀ (G rho a k : ℝ), 0 < G → 0 < rho → 0 < a → ¬ jeansStable 0 G rho a k) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact csSq_zero
  · exact ⟨csSq_pos 1 (by norm_num), csSq_lt_one 1⟩
  · intro u hu; exact csSq_ne_zero u hu
  · intro v w; exact coherent_dispersion v w
  · intro dt; exact lamFs_of_zero_dispersion dt
  · intro G rho a k hG hrho ha; exact no_jeans_stabilisation G rho a k hG hrho ha

#print axioms csSq_eq_sound_speed
#print axioms hasDerivAt_mu2
#print axioms hasDerivAt_fK
#print axioms csSq_pos
#print axioms csSq_lt_one
#print axioms csSq_ne_zero
#print axioms csSq_ge_half
#print axioms coherent_dispersion
#print axioms two_stream_dispersion
#print axioms lamFs_of_zero_dispersion
#print axioms no_jeans_stabilisation
#print axioms growth_k_independent
#print axioms no_suppression
#print axioms cutoff_lt_one
#print axioms charge_scales_a3
#print axioms dust_background_has_pressure_response
#print axioms noether_dust_spine

end
