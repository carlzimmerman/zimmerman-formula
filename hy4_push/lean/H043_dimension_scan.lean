/-
  H043 -- DIMENSION SCAN: IS THE FRAMEWORK INCONSISTENT FOR D != 4?
         Lean certificate.

  Companion to hy4_push/H043_dimension_scan.py.  The question is whether the
  framework's laws, written in D spacetime dimensions, remain consistent
  with the galaxy data away from D = 4.  Three channels SELECT D = 4; two
  channels provably do NOT (they hold for every D and are certified here as
  honest negatives).

  WHAT IS CERTIFIED

  SELECTORS  (each one forces D = 4, over the integers):
    S1  amplitude-law exponent   M_ph/M_b = (R/r_M)^((D-2)/2)  --  the
        certified law (H021) has exponent 1  <=>  D = 4.
    S1' the same integer (D-2)/2 is the LENGTH dimension of the framework's
        r_M = sqrt(GM/a_0): [r_M] = L^((D-2)/2).  r/r_M is dimensionless
        (a ratio of masses sits on the left) only if that exponent is 1,
        i.e. only at D = 4.  This one is pure dimensional analysis -- no
        galaxy data enters.
    S2  rotation-curve slope     d ln v / d ln R = (4-D)/4  --  observed
        outer curves are flat, so the slope must vanish  <=>  D = 4.
    S3  BTFR exponent            M ∝ V^(2(D-2))  --  observed exponent 4
        <=>  D = 4.

  NON-SELECTORS  (certified to hold for EVERY D, hence no constraint):
    N1  the sound speed c_s^2(u) = (u^2+3u+2)/(u^2+3u+4) is strictly inside
        (0,1) -- and in fact in [1/2,1) -- for every u >= 0, and it carries
        no D at all: the D-slot of csSqD is provably vacuous.
    N2  the phantom surface density at the transition radius is the same for
        two galaxies of different mass, in every dimension:
        Sigma_ph(r_M) = a_0/(G A_(D-2)) has no r_M left in it.

  NOT CERTIFIED HERE
    * n = D(D-3)/2 = 2  <=>  D = 4.  That is H030/H017's already-established
      result; it is cited by the python lane as a premise, not re-derived.
    * a_0 = (1/2) c sqrt(G rho_Lambda) is not used: H029 showed it is
      algebraically identical to the postulate.

  Every excluded dimension is stated as a theorem: D >= 5 fails S1, S2, S3
  simultaneously; D = 3 fails them too (and has n = 0).  NO sorry.
  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

/-! ## The D-dependent exponents -/

/-- Exponent of the phantom amplitude law: M_ph/M_b = (R/r_M)^ampExp. -/
def ampExp (D : ℚ) : ℚ := (D - 2) / 2

/-- Logarithmic slope of the deep-MOND rotation curve: d ln v / d ln R. -/
def vSlope (D : ℚ) : ℚ := (4 - D) / 4

/-- Exponent of the mass--speed relation: M ∝ V^btfrExp. -/
def btfrExp (D : ℚ) : ℚ := 2 * (D - 2)

/-- The D = 4 values: the certified amplitude law, flat curves, BTFR slope 4. -/
theorem ampExp_four : ampExp 4 = 1 := by norm_num [ampExp]
theorem vSlope_four : vSlope 4 = 0 := by norm_num [vSlope]
theorem btfrExp_four : btfrExp 4 = 4 := by norm_num [btfrExp]

/-! ## S1: the amplitude-law exponent -/

/-- S1 (over the rationals): the exponent is 1 exactly at D = 4. -/
theorem ampExp_eq_one_iff (D : ℚ) : ampExp D = 1 ↔ D = 4 := by
  unfold ampExp
  constructor <;> intro h <;> linarith

/-- S1' (over the rationals): the length-dimension exponent of
    r_M = sqrt(GM/a_0) is 1 exactly at D = 4 -- the same algebra, stated
    separately because the two roles are different. -/
theorem rM_length_exponent_iff (D : ℚ) : (D - 2) / 2 = 1 ↔ D = 4 := by
  constructor <;> intro h <;> linarith

/-- S1 on integer dimensions: the physical D is an integer. -/
theorem ampExp_int_eq_one_iff (D : ℤ) : ampExp (D : ℚ) = 1 ↔ D = 4 := by
  constructor
  · intro h
    have hq : (D : ℚ) = 4 := (ampExp_eq_one_iff (D : ℚ)).mp h
    exact_mod_cast hq
  · intro h
    subst h
    norm_num [ampExp]

/-! ## S2: flat rotation curves -/

/-- S2 (over the rationals): the rotation curve is flat exactly at D = 4. -/
theorem vSlope_eq_zero_iff (D : ℚ) : vSlope D = 0 ↔ D = 4 := by
  unfold vSlope
  constructor <;> intro h <;> linarith

/-- S2 on integer dimensions. -/
theorem vSlope_int_eq_zero_iff (D : ℤ) : vSlope (D : ℚ) = 0 ↔ D = 4 := by
  constructor
  · intro h
    have hq : (D : ℚ) = 4 := (vSlope_eq_zero_iff (D : ℚ)).mp h
    exact_mod_cast hq
  · intro h
    subst h
    norm_num [vSlope]

/-! ## S3: the BTFR exponent -/

/-- S3 (over the rationals): M ∝ V^4 exactly at D = 4. -/
theorem btfrExp_eq_four_iff (D : ℚ) : btfrExp D = 4 ↔ D = 4 := by
  unfold btfrExp
  constructor <;> intro h <;> linarith

/-- S3 on integer dimensions. -/
theorem btfrExp_int_eq_four_iff (D : ℤ) : btfrExp (D : ℚ) = 4 ↔ D = 4 := by
  constructor
  · intro h
    have hq : (D : ℚ) = 4 := (btfrExp_eq_four_iff (D : ℚ)).mp h
    exact_mod_cast hq
  · intro h
    subst h
    norm_num [btfrExp]

/-! ## Any one selector is enough; all of them together are consistent only at 4 -/

/-- Each selector alone forces D = 4 -- the three exclusions are independent. -/
theorem one_selector_suffices (D : ℤ)
    (h : ampExp (D : ℚ) = 1 ∨ vSlope (D : ℚ) = 0 ∨ btfrExp (D : ℚ) = 4) :
    D = 4 := by
  rcases h with h | h | h
  · exact (ampExp_int_eq_one_iff D).mp h
  · exact (vSlope_int_eq_zero_iff D).mp h
  · exact (btfrExp_int_eq_four_iff D).mp h

/-- At D = 4 all three hold simultaneously (the certified framework). -/
theorem four_satisfies_all_selectors :
    ampExp 4 = 1 ∧ vSlope 4 = 0 ∧ btfrExp 4 = 4 := by
  exact ⟨ampExp_four, vSlope_four, btfrExp_four⟩

/-! ## The excluded dimensions -/

/-- Every D >= 5 fails S1: the amplitude law is not linear. -/
theorem dim_ge_five_ampExp_ne_one (D : ℤ) (hD : 5 ≤ D) : ampExp (D : ℚ) ≠ 1 := by
  intro h
  have h4 : D = 4 := (ampExp_int_eq_one_iff D).mp h
  omega

/-- Every D >= 5 fails S2: the deep-MOND rotation curve is not flat
    (at D = 5, v ∝ R^(-1/4) -- a 44% decline over a decade in radius). -/
theorem dim_ge_five_vSlope_ne_zero (D : ℤ) (hD : 5 ≤ D) : vSlope (D : ℚ) ≠ 0 := by
  intro h
  have h4 : D = 4 := (vSlope_int_eq_zero_iff D).mp h
  omega

/-- Every D >= 5 fails S3: the mass--speed relation is not M ∝ V^4. -/
theorem dim_ge_five_btfrExp_ne_four (D : ℤ) (hD : 5 ≤ D) : btfrExp (D : ℚ) ≠ 4 := by
  intro h
  have h4 : D = 4 := (btfrExp_int_eq_four_iff D).mp h
  omega

/-- D = 3 fails S2 (curves rise as R^(+1/4)) -- and has n = 0 (H017). -/
theorem dim_three_vSlope_ne_zero : vSlope 3 ≠ 0 := by norm_num [vSlope]

/-- D = 3 fails S1 (amplitude exponent 1/2, not 1). -/
theorem dim_three_ampExp_ne_one : ampExp 3 ≠ 1 := by norm_num [ampExp]

/-- The excluded set is every integer dimension except 4: D ≠ 4 implies all
    three selectors fail simultaneously.  (No lower bound on D is needed --
    the algebra excludes D <= 2 as well; D >= 3 is the physical range.) -/
theorem only_four_is_consistent (D : ℤ) (hne : D ≠ 4) :
    ampExp (D : ℚ) ≠ 1 ∧ vSlope (D : ℚ) ≠ 0 ∧ btfrExp (D : ℚ) ≠ 4 := by
  constructor
  · intro h
    exact hne ((ampExp_int_eq_one_iff D).mp h)
  constructor
  · intro h
    exact hne ((vSlope_int_eq_zero_iff D).mp h)
  · intro h
    exact hne ((btfrExp_int_eq_four_iff D).mp h)

/-! ## N1: the sound speed -- stable in every dimension, so no constraint -/

/-- The k-essence sound speed (H008) as a function of the MOND variable u. -/
def csSq (u : ℝ) : ℝ := (u^2 + 3*u + 2) / (u^2 + 3*u + 4)

/-- The same expression with a dimension slot.  The slot is VACUOUS: this is
    the formal statement that the sound speed carries no D-dependence. -/
def csSqD (_D : ℕ) (u : ℝ) : ℝ := (u^2 + 3*u + 2) / (u^2 + 3*u + 4)

/-- N1a: the D-slot is provably unused. -/
theorem csSqD_is_csSq (D : ℕ) (u : ℝ) : csSqD D u = csSq u := rfl

/-- The denominator is strictly positive for every u (complete the square). -/
theorem denom_pos (u : ℝ) : 0 < u^2 + 3*u + 4 := by
  have hsq : 0 ≤ (u + 3/2)^2 := sq_nonneg (u + 3/2)
  nlinarith

/-- The numerator is strictly positive for u >= 0. -/
theorem num_pos (u : ℝ) (hu : 0 ≤ u) : 0 < u^2 + 3*u + 2 := by
  have hsq : 0 ≤ u^2 := sq_nonneg u
  nlinarith

/-- N1b: stable -- c_s^2 > 0 (no gradient instability). -/
theorem csSq_pos (u : ℝ) (hu : 0 ≤ u) : 0 < csSq u := by
  unfold csSq
  exact div_pos (num_pos u hu) (denom_pos u)

/-- N1c: causal -- c_s^2 < 1 (subluminal).  Proved from the exact identity
    1 - c_s^2 = 2/(u^2+3u+4). -/
theorem csSq_lt_one (u : ℝ) : csSq u < 1 := by
  unfold csSq
  have hd : 0 < u^2 + 3*u + 4 := denom_pos u
  have hnum : u^2 + 3*u + 2 < u^2 + 3*u + 4 := by norm_num
  have h : (u^2 + 3*u + 2) / (u^2 + 3*u + 4) <
           (u^2 + 3*u + 4) / (u^2 + 3*u + 4) :=
    div_lt_div_of_pos_right hnum hd
  simpa [ne_of_gt hd] using h

/-- N1d: the lower bound -- c_s^2 >= 1/2, attained at u = 0. -/
theorem csSq_ge_half (u : ℝ) (hu : 0 ≤ u) : (1/2 : ℝ) ≤ csSq u := by
  have hd : 0 < u^2 + 3*u + 4 := denom_pos u
  have hid : csSq u - (1/2 : ℝ) = (u^2 + 3*u) / (2 * (u^2 + 3*u + 4)) := by
    unfold csSq
    field_simp [ne_of_gt hd]
    ring_nf
  have hn : 0 ≤ u^2 + 3*u := by
    have hsq : 0 ≤ u^2 := sq_nonneg u
    nlinarith
  have hfrac : 0 ≤ (u^2 + 3*u) / (2 * (u^2 + 3*u + 4)) := by
    exact div_nonneg hn (by nlinarith [hd])
  linarith

/-- The zero-field value: c_s^2(0) = 1/2. -/
theorem csSq_zero : csSq 0 = (1/2 : ℝ) := by norm_num [csSq]

/-- N1: fluid stable and subluminal for every u >= 0 -- and, because the
    D-slot is vacuous, for every dimension.  Stability imposes NO constraint
    on D. -/
theorem fluid_stable_all_D (D : ℕ) (u : ℝ) (hu : 0 ≤ u) :
    0 < csSqD D u ∧ csSqD D u < 1 := by
  constructor
  · simpa [csSqD, csSq] using csSq_pos u hu
  · simpa [csSqD, csSq] using csSq_lt_one u

/-! ## N2: the universal surface density -- survives in every dimension -/

/-- The phantom surface density at the transition radius, in D dimensions:
    Sigma_ph(r_M) = (a_0/G) (r_M/r_M)^((D-2)/2) / A_(D-2), where A_(D-2) is
    the volume of the unit (D-2)-ball (A = pi at D = 4). -/
def SigmaAtRM (D a0 G A rM : ℝ) : ℝ := (a0 / G) * ((rM / rM) ^ ((D - 2) / 2)) / A

/-- N2: two galaxies with different transition radii (hence different masses)
    give the SAME surface density at their own r_M -- in every dimension.
    The mass cancels because r_M absorbs it; no D is selected. -/
theorem Sigma_universal_in_every_D (D a0 G A rM₁ rM₂ : ℝ)
    (h₁ : rM₁ ≠ 0) (h₂ : rM₂ ≠ 0) :
    SigmaAtRM D a0 G A rM₁ = SigmaAtRM D a0 G A rM₂ := by
  unfold SigmaAtRM
  rw [div_self h₁, div_self h₂]

/-- The value it takes: a_0/(G A), with no r_M (hence no M) left. -/
theorem Sigma_at_rM_value (D a0 G A rM : ℝ) (hrM : rM ≠ 0) (hG : G ≠ 0) (hA : A ≠ 0) :
    SigmaAtRM D a0 G A rM = a0 / (G * A) := by
  unfold SigmaAtRM
  rw [div_self hrM]
  have hone : ((1 : ℝ) ^ ((D - 2) / 2)) = 1 := by simp
  rw [hone, mul_one]
  field_simp [hG, hA]

/-- At D = 4 the geometric factor is A = pi, giving the framework's
    Sigma_ph = a_0/(pi G) (H033). -/
theorem Sigma_four_is_a0_over_piG (a0 G rM : ℝ) (hrM : rM ≠ 0) (hG : G ≠ 0) :
    SigmaAtRM 4 a0 G Real.pi rM = a0 / (G * Real.pi) := by
  exact Sigma_at_rM_value 4 a0 G Real.pi rM hrM hG Real.pi_ne_zero

/-! ## The amplitude law itself -/

/-- The general-D amplitude law, as a real-power expression. -/
def ampRatio (D R rM : ℝ) : ℝ := (R / rM) ^ ((D - 2) / 2)

/-- At R = r_M the phantom mass equals the baryon mass -- in every dimension
    (the unit coefficient of H021 is D-independent). -/
theorem ampRatio_at_rM (D rM : ℝ) (hrM : rM ≠ 0) : ampRatio D rM rM = 1 := by
  unfold ampRatio
  rw [div_self hrM]
  simp

/-- At D = 4 the exponent is 1, so the law is the certified M_ph/M_b = r/r_M. -/
theorem ampRatio_four (R rM : ℝ) : ampRatio 4 R rM = R / rM := by
  unfold ampRatio
  norm_num

/-! ## The spine -/

/-- THE SPINE.  (i) At D = 4 the amplitude exponent is 1, the rotation-curve
    slope is 0 and the BTFR exponent is 4 -- the certified framework.
    (ii) Any ONE of those three numbers forces D = 4 over the integers, so
    every D >= 5 (and D = 3) is excluded three times over.
    (iii) Two further properties hold in EVERY dimension and therefore do
    not select D: the sound speed stays in (0,1) for all u >= 0 with no D
    in it, and the phantom surface density at r_M is the same for any two
    masses.  The framework is consistent only at D = 4. -/
theorem dimension_scan_spine :
    (ampExp 4 = 1 ∧ vSlope 4 = 0 ∧ btfrExp 4 = 4)
    ∧ (∀ D : ℤ, ampExp (D : ℚ) = 1 → D = 4)
    ∧ (∀ D : ℤ, vSlope (D : ℚ) = 0 → D = 4)
    ∧ (∀ D : ℤ, btfrExp (D : ℚ) = 4 → D = 4)
    ∧ (∀ D : ℤ, 5 ≤ D → ampExp (D : ℚ) ≠ 1)
    ∧ (∀ D : ℕ, ∀ u : ℝ, 0 ≤ u → 0 < csSqD D u ∧ csSqD D u < 1)
    ∧ (∀ D a0 G A rM₁ rM₂ : ℝ, rM₁ ≠ 0 → rM₂ ≠ 0 →
         SigmaAtRM D a0 G A rM₁ = SigmaAtRM D a0 G A rM₂) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact four_satisfies_all_selectors
  · intro D h; exact (ampExp_int_eq_one_iff D).mp h
  · intro D h; exact (vSlope_int_eq_zero_iff D).mp h
  · intro D h; exact (btfrExp_int_eq_four_iff D).mp h
  · intro D hD; exact dim_ge_five_ampExp_ne_one D hD
  · intro D u hu; exact fluid_stable_all_D D u hu
  · intro D a0 G A rM₁ rM₂ h₁ h₂
    exact Sigma_universal_in_every_D D a0 G A rM₁ rM₂ h₁ h₂

#print axioms dimension_scan_spine
#print axioms ampExp_int_eq_one_iff
#print axioms vSlope_int_eq_zero_iff
#print axioms btfrExp_int_eq_four_iff
#print axioms only_four_is_consistent
#print axioms fluid_stable_all_D
#print axioms csSq_lt_one
#print axioms Sigma_universal_in_every_D

end
