/-
  H045 -- THE NEGATIVE ENERGY DENSITY: Lean certificate.

  Companion to hy4_push/H045_negative_energy_verdict.py.

  H035 found that on the STATIC branch the scalar's energy density is

        rho = -Lambda^4 f(K),      f(0) = -1,   f'(K) = mu_2(sqrt K) > 0,

  which starts at +Lambda^4 (the vacuum) and FALLS, crossing zero somewhere
  near sqrt(K) = 1.4.  Four questions, and what is certified here:

  (a) WHERE?  f is STRICTLY INCREASING on (0,inf) (`fK_strictMono`), so
      rho = -f is strictly DECREASING and the crossing is UNIQUE
      (`crossing_unique`).  It lies in (7/6, 5/2) (`crossing_exists`,
      `no_zero_below`, `no_zero_above`).  The numeric value is a measurement,
      not a theorem: the Python lane gives u* = 1.22385628142208.

  (b) REACHABLE?  Yes, and this file proves the reason it cannot be dodged:
      the phantom map y(u) = u*mu_2(u) = g_N/(2 a_0) is a STRICTLY
      INCREASING, UNBOUNDED bijection of [0,inf) onto itself (`y_strictMono`,
      `y_ge_sub_quarter`, `no_domain_restriction`).  Every u >= 0 is realized
      by some radius of some spherical system.

  (c) FATAL?  `gradient_energy_wrong_sign`: rho(u) < rho(0) for EVERY u > 0 --
      the vacuum is a MAXIMUM along the gradient direction, not a minimum --
      and `rho_unbounded_below`: the static energy has no ground state.  The
      crossing u* is only where the sickness becomes NEGATIVE.

  (d) THE DOMAIN RESTRICTION DOES NOT EXIST (`no_domain_restriction`).

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

/-! ## The functions (u = sqrt K) -/

def fp (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2          -- f'(K) = mu_2(sqrt K)
def fK (u : ℝ) : ℝ := u^2 - 2 * Real.log (1 + u) - 2 / (1 + u) + 1
def rho_static (u : ℝ) : ℝ := - fK u                   -- rho/Lambda^4, static
def yph (u : ℝ) : ℝ := u * fp u                        -- = g_N/(2 a_0)

/-! ## 0. the vacuum -/

theorem fK_zero : fK 0 = -1 := by
  unfold fK; norm_num

theorem rho_static_zero : rho_static 0 = 1 := by
  unfold rho_static fK; norm_num

/-- f'(K) = mu_2 > 0 for K > 0 (H034 kept this: no ghost in the ELLIPTIC
    static problem).  The point of this file is that the same inequality is
    exactly what makes the HYPERBOLIC problem sick: P_X = -f' < 0. -/
theorem fp_pos (u : ℝ) (hu : 0 < u) : 0 < fp u := by
  unfold fp; positivity

/-! ## 1. the bracket: f(7/6) < 0 < f(5/2)
    Both from mathlib's own logarithm bounds, no numerics:
      Real.le_log_one_add_of_nonneg : 0 <= x -> 2x/(x+2) <= log (1+x)
      Real.log_le_sub_one_of_pos    : 0 < x  -> log x <= x - 1            -/

lemma fK_seven_sixths_neg : fK (7/6 : ℝ) < 0 := by
  have hlog : 2 * (7/6 : ℝ) / ((7/6 : ℝ) + 2) ≤ Real.log (1 + (7/6 : ℝ)) :=
    Real.le_log_one_add_of_nonneg (by norm_num)
  have hnum : (7/6 : ℝ)^2 - 2 * (2 * (7/6 : ℝ) / ((7/6 : ℝ) + 2))
                - 2 / (1 + (7/6 : ℝ)) + 1 = -(317/8892 : ℝ) := by norm_num
  unfold fK
  nlinarith

lemma fK_five_halves_pos : 0 < fK (5/2 : ℝ) := by
  have hlog : Real.log (1 + (5/2 : ℝ)) ≤ (1 + (5/2 : ℝ)) - 1 :=
    Real.log_le_sub_one_of_pos (by norm_num)
  have hnum : (5/2 : ℝ)^2 - 2 * ((1 + (5/2 : ℝ)) - 1)
                - 2 / (1 + (5/2 : ℝ)) + 1 = (47/28 : ℝ) := by norm_num
  unfold fK
  nlinarith

/-! ## 2. continuity and the intermediate value theorem -/

lemma fK_continuousOn {s : Set ℝ} (hs : ∀ x ∈ s, 0 < 1 + x) :
    ContinuousOn fK s := by
  intro x hx
  have hne : 1 + x ≠ 0 := by linarith [hs x hx]
  unfold fK
  continuity

/-- (a, part 1) THE CROSSING EXISTS: f is continuous and changes sign between
    7/6 and 5/2, so rho = -f vanishes at some u in that interval. -/
theorem crossing_exists : ∃ u ∈ Set.Icc (7/6 : ℝ) (5/2), fK u = 0 := by
  have hcont : ContinuousOn fK (Set.Icc (7/6 : ℝ) (5/2)) :=
    fK_continuousOn (by intro x hx; linarith [hx.1])
  have hmem : (0 : ℝ) ∈ Set.Icc (fK (7/6 : ℝ)) (fK (5/2 : ℝ)) :=
    ⟨le_of_lt fK_seven_sixths_neg, le_of_lt fK_five_halves_pos⟩
  rcases (intermediate_value_Icc (by norm_num : (7/6 : ℝ) ≤ 5/2) hcont hmem) with
    ⟨u, hu, hfu⟩
  exact ⟨u, hu, hfu⟩

/-! ## 3. f is strictly increasing (f'(u) = 2 u mu_2(u) = 2 y(u) > 0) -/

lemma hasDerivAt_fK (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt fK (2 * u - 2 * (1 + u)⁻¹ + 2 / (1 + u)^2) u := by
  have hA : HasDerivAt (fun x : ℝ => x ^ 2) (2 * u) u := by
    simpa using ((hasDerivAt_id u).pow 2)
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using ((hasDerivAt_id u).const_add 1)
  have hlog : HasDerivAt (fun x : ℝ => Real.log (1 + x)) ((1 + u)⁻¹) u := by
    simpa using (Real.hasDerivAt_log hu).comp u hlin
  have hB : HasDerivAt (fun x : ℝ => 2 * Real.log (1 + x)) (2 * (1 + u)⁻¹) u := by
    simpa using (hlog.const_mul (2 : ℝ))
  have hinv : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(1 : ℝ) / (1 + u)^2) u := by
    simpa using (hlin.inv hu)
  have hC : HasDerivAt (fun x : ℝ => 2 * (1 + x)⁻¹) (-2 / (1 + u)^2) u := by
    have h := hinv.const_mul (2 : ℝ)
    convert h using 1
    ring
  have hD : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 u := hasDerivAt_const u 1
  have h := (((hA.sub hB).sub hC).add hD)
  convert h using 1
  · ext x
    simp [fK, div_eq_mul_inv]
  · ring

lemma deriv_fK_eq (u : ℝ) (hu : 0 < u) : deriv fK u = 2 * u * fp u := by
  have hne : 1 + u ≠ 0 := by linarith
  rw [(hasDerivAt_fK u hne).deriv]
  unfold fp
  field_simp [hne]
  ring

/-- df/du = 2 u mu_2(u) > 0 for u > 0, so f is strictly increasing and
    rho = -f is strictly decreasing: THE CROSSING IS UNIQUE. -/
theorem fK_strictMono : StrictMonoOn fK (Set.Ici 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ici 0)
  · exact fK_continuousOn (by intro x hx; linarith [hx])
  · intro x hx
    rw [interior_Ici] at hx
    rw [deriv_fK_eq x hx]
    positivity

/-- (a, part 2) rho = -f is strictly DECREASING: the vacuum value 1 is a
    MAXIMUM along the gradient direction, and rho takes the value 0 once. -/
theorem rho_static_strictAnti : StrictAntiOn rho_static (Set.Ici 0) := by
  intro a ha b hb hab
  have h := fK_strictMono ha hb hab
  unfold rho_static
  linarith

theorem crossing_unique ⦃a : ℝ⦄ (ha : 0 ≤ a) ⦃b : ℝ⦄ (hb : 0 ≤ b)
    (hfa : fK a = 0) (hfb : fK b = 0) : a = b := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have := fK_strictMono ha hb hlt
    linarith
  · have := fK_strictMono hb ha hgt
    linarith

theorem no_zero_below ⦃u : ℝ⦄ (hu0 : 0 ≤ u) (hu : u ≤ 7/6) : fK u ≠ 0 := by
  intro h
  have hle : fK u ≤ fK (7/6 : ℝ) :=
    fK_strictMono.monotoneOn hu0 (by norm_num) hu
  linarith [fK_seven_sixths_neg]

theorem no_zero_above ⦃u : ℝ⦄ (hu : 5/2 ≤ u) : fK u ≠ 0 := by
  intro h
  have hle : fK (5/2 : ℝ) ≤ fK u :=
    fK_strictMono.monotoneOn (by norm_num) (by linarith) hu
  linarith [fK_five_halves_pos]

/-! ## 4. (c) THE GRADIENT ENERGY HAS THE WRONG SIGN -/

/-- THE CENTRAL INSTABILITY.  For EVERY u > 0 the static energy density is
    BELOW the vacuum: rho(u) < rho(0) = 1.  So the vacuum K = 0 is not a
    minimum of the static energy but a maximum, and the theory lowers its
    energy by growing a spatial gradient.  (In k-essence variables
    X = -(1/2)(dphi)^2/Lambda^4 this is P_X = -f' = -mu_2 < 0: the wrong-sign
    gradient term.  The crossing u* is where rho turns NEGATIVE -- the
    sickness itself starts at u = 0+.) -/
theorem gradient_energy_wrong_sign (u : ℝ) (hu : 0 < u) :
    rho_static u < rho_static 0 := by
  have h := fK_strictMono (le_of_lt hu) (le_refl 0) (le_of_lt hu)
  unfold rho_static at *
  linarith

/-- No ground state: rho/Lambda^4 -> -inf, so the static energy functional is
    unbounded below.  (f(u) >= u^2 - 2u - 1 because log(1+u) <= u and
    2/(1+u) <= 2.) -/
theorem rho_unbounded_below : ∀ B : ℝ, ∃ u ≥ 0, rho_static u < B := by
  intro B
  let u : ℝ := 2 * |B| + 6
  have hu_nonneg : 0 ≤ u := by dsimp [u]; positivity
  have hu6 : 6 ≤ u := by dsimp [u]; nlinarith [abs_nonneg B]
  have hlog : Real.log (1 + u) ≤ u := by
    have hpos : 0 < 1 + u := by linarith
    have := Real.log_le_sub_one_of_pos hpos
    linarith
  have hinv : 0 < 1 + u := by linarith
  have hfrac : 2 / (1 + u) ≤ 2 := by
    rw [div_le_iff₀ hinv]
    nlinarith
  have hf_lower : u^2 - 2 * u - 1 ≤ fK u := by
    unfold fK
    nlinarith
  have hquad : B < -(u^2 - 2 * u - 1) := by
    dsimp [u] at *
    nlinarith [abs_nonneg B, le_abs_self B, neg_le_abs B]
  refine ⟨u, hu_nonneg, ?_⟩
  unfold rho_static
  linarith

/-! ## 5. (b)(d) THE PHANTOM MAP: strictly increasing and UNBOUNDED -/

/-- y(u) = u*mu_2(u) = u - u/(1+u)^2. -/
lemma yph_eq (u : ℝ) (hu : 1 + u ≠ 0) : yph u = u - u / (1 + u)^2 := by
  unfold yph fp
  field_simp [hu]
  ring

theorem yph_zero : yph 0 = 0 := by
  unfold yph fp; norm_num

/-- THE KEY ALGEBRAIC IDENTITY.  For 0 <= a < b,
      y(b) - y(a) = (b-a) * [((1+a)(1+b))^2 + ab - 1] / ((1+a)^2 (1+b)^2)
    and the bracket equals (a+b+ab)(2+a+b+ab) + ab > 0.  No calculus. -/
lemma yph_sub_identity (a b : ℝ) (ha : 1 + a ≠ 0) (hb : 1 + b ≠ 0) :
    yph b - yph a =
      (b - a) * (((1 + a) * (1 + b))^2 + a * b - 1) / ((1 + a)^2 * (1 + b)^2) := by
  rw [yph_eq b hb, yph_eq a ha]
  field_simp [ha, hb]
  ring

/-- (b) THE PHANTOM MAP IS STRICTLY INCREASING: more baryonic acceleration
    means a bigger gradient, with no upper bound and no turning back. -/
theorem y_strictMono : StrictMonoOn yph (Set.Ici 0) := by
  intro a ha b hb hab
  have h1a : 1 + a ≠ 0 := by linarith [ha]
  have h1b : 1 + b ≠ 0 := by linarith [hb]
  have hden : 0 < (1 + a)^2 * (1 + b)^2 := by positivity
  rw [yph_sub_identity a b h1a h1b]
  apply div_pos
  · apply mul_pos (sub_pos.mpr hab)
    have hs : 0 < a + b + a * b := by
      nlinarith [ha, hb, hab, mul_nonneg ha hb]
    have habn : 0 ≤ a * b := mul_nonneg ha hb
    have hnum : ((1 + a) * (1 + b))^2 + a * b - 1 =
        (a + b + a * b) * (2 + (a + b + a * b)) + a * b := by ring
    rw [hnum]
    nlinarith
  · exact hden

/-- The ceiling that would be needed to save the theory does not exist:
    y(u) >= u - 1/4, because 4u <= (1+u)^2 (i.e. 0 <= (1-u)^2). -/
lemma y_ge_sub_quarter (u : ℝ) (hu : 0 ≤ u) : u - 1/4 ≤ yph u := by
  have h1 : 0 < 1 + u := by linarith
  have hsq : 4 * u ≤ (1 + u)^2 := by
    nlinarith [sq_nonneg (1 - u)]
  have hle : u / (1 + u)^2 ≤ (1 : ℝ) / 4 := by
    rw [div_le_div_iff₀ (by positivity : 0 < (1 + u)^2) (by norm_num : (0 : ℝ) < 4)]
    nlinarith
  rw [yph_eq u h1.ne']
  linarith

/-- (d) NO DOMAIN RESTRICTION.  For every bound B there is a NONNEGATIVE u
    with y(u) > B.  Since y(u) = g_N/(2 a_0) and g_N = GM/r^2 can be made
    arbitrarily large by going to small enough r (or large enough M), every
    u -- in particular every u ABOVE the crossing u* -- is realized by some
    spherical static configuration.  THERE IS NO CONSISTENCY CONDITION THAT
    KEEPS u BELOW u*, AND HENCE NO ESCAPE FROM (c). -/
theorem no_domain_restriction : ∀ B : ℝ, ∃ u ≥ 0, B < yph u := by
  intro B
  by_cases hB : B + 1 ≤ 0
  · refine ⟨0, le_refl 0, ?_⟩
    rw [yph_zero]
    linarith
  · let u : ℝ := B + 1
    have hu : 0 ≤ u := by dsimp [u]; linarith
    have hge := y_ge_sub_quarter u hu
    refine ⟨u, hu, ?_⟩
    dsimp [u] at hge ⊢
    linarith

/-! ## 6. the spine -/

/-- THE VERDICT, certified: the vacuum is +1; the static energy density is
    strictly below it for every gradient; the crossing exists and is unique;
    and no domain restriction excludes the region beyond it. -/
theorem negative_energy_spine :
    rho_static 0 = 1 ∧
    (∀ u, 0 < u → rho_static u < rho_static 0) ∧
    (∃ u ∈ Set.Icc (7/6 : ℝ) (5/2), fK u = 0) ∧
    (∀ B : ℝ, ∃ u ≥ 0, B < yph u) ∧
    (∀ B : ℝ, ∃ u ≥ 0, rho_static u < B) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · exact rho_static_zero
  · exact gradient_energy_wrong_sign
  · exact crossing_exists
  · exact no_domain_restriction
  · exact rho_unbounded_below

#print axioms negative_energy_spine
#print axioms fK_strictMono
#print axioms crossing_exists
#print axioms crossing_unique
#print axioms y_strictMono
#print axioms no_domain_restriction
#print axioms rho_unbounded_below
#print axioms gradient_energy_wrong_sign

end
