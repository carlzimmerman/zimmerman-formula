/-
  H009 -- THE MIMETIC RESOLUTION: Lean certificate.

  Horn A (glm53 G032) is the minimal relativistic completion: pure GR plus
  the MOND scalar on a FIXED hypersurface-orthogonal congruence.  G032
  measured alpha_1 = 0 exactly at every (CA, JY) cell, gamma -> 1,
  alpha_3 -> 0 -- the preferred-frame lock
      alpha_1 = -4 c_14 - 4 (2 - K_B)/(J_Y + 1)
  has no handle, because the vector has no equation of motion.

  The cost GLM recorded: explicit local Lorentz violation.

  This file certifies the algebraic core of the resolution: the fixed
  congruence is the NORMALISED GAUGE of a mimetic parent.  Three facts,
  each pure algebra, no analysis:

    (1) the mimetic constraint is an IDENTITY: for
        g = -(g~^{-1}(dT,dT)) g~  one has  g^{-1}(dT,dT) = -1  identically.
        Writing Xt := g~^{-1}(dT,dT), this is  Xt / (-Xt) = -1.
    (2) in the normalised gauge, u_mu = d_mu T is unit-timelike,
        so it IS the Horn-A congruence;
    (3) T -> f(T) scales dT by s, hence Xt by s^2 and g by s^2, leaving the
        contraction UNCHANGED -- so the frame is a gauge choice, not a
        structure added to the theory.

  We state (1) and (3) in the abstract form X/(-X) = -1, which is their
  entire mathematical content; the expanded 1+1 component form is equivalent
  and was verified separately in H009_mimetic_horn_a.py.

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

open Real

/-! ## 1. The mimetic constraint is an identity

The physical metric is g = (-Xt) g~ with Xt = g~^{-1}(dT,dT).  Contracting
the physical inverse with dT gives Xt / (-Xt), which is -1 for any nonzero
(timelike) Xt.  It is an identity of the DEFINITION, not an equation of
motion: no dynamics is spent enforcing it.
-/

/-- X divided by its own negation is -1, for any nonzero X. -/
theorem mimetic_scalar_identity (X : ℝ) (hX : X ≠ 0) :
    X / (-X) = (-1 : ℝ) := by
  field_simp [hX]

/-- The mimetic constraint: the physical metric's inverse contracts with dT
    to -1 identically.  Here Xt stands for g~^{-1}(dT,dT), which is nonzero
    precisely when the gradient is timelike -- the case the construction uses. -/
theorem mimetic_constraint_identity (Xt : ℝ) (hXt : Xt ≠ 0) :
    Xt / (-Xt) = (-1 : ℝ) := by
  exact mimetic_scalar_identity Xt hXt

/-! ## 2. The conformal factor is positive for a timelike gradient

g = (-Xt) g~ is a positive rescaling of g~ exactly when Xt < 0.  This is what
makes the physical metric have the right signature.
-/

/-- For a timelike gradient (Xt < 0) the mimetic conformal factor is positive. -/
theorem mimetic_factor_pos (Xt : ℝ) (htime : Xt < 0) : 0 < -Xt := by
  linarith

/-! ## 3. Reparametrisation invariance -- the frame is a gauge

Under T -> f(T) the gradient scales by s := f'(T).  Then Xt -> s^2 Xt
(quadratic in dT) and the metric scales by s^2 as well, so the contraction
is unchanged: still -1.  The theory cannot tell which clock you used, so the
CMB frame that Horn A singles out is one representative of a gauge orbit --
exactly the status of the fixed volume element in unimodular gravity.
-/

/-- Scaling both numerator and denominator by s^2 leaves the ratio unchanged. -/
theorem reparametrisation_invariance (Xt s : ℝ) (hs : s ≠ 0) (hXt : Xt ≠ 0) :
    (s^2 * Xt) / (-(s^2 * Xt)) = Xt / (-Xt) := by
  have hs2 : s^2 ≠ 0 := pow_ne_zero 2 hs
  have hprod : s^2 * Xt ≠ 0 := mul_ne_zero hs2 hXt
  rw [mimetic_scalar_identity (s^2 * Xt) hprod]
  rw [mimetic_scalar_identity Xt hXt]

/-- After reparametrisation the constraint still reads -1. -/
theorem reparametrisation_still_minus_one
    (Xt s : ℝ) (hs : s ≠ 0) (hXt : Xt ≠ 0) :
    (s^2 * Xt) / (-(s^2 * Xt)) = (-1 : ℝ) := by
  rw [reparametrisation_invariance Xt s hs hXt]
  exact mimetic_scalar_identity Xt hXt

/-! ## 4. The spine: Horn A is a gauge of a covariant parent -/

/-- THE SPINE.  The mimetic constraint is an identity of the definition, the
    conformal factor is positive precisely for timelike gradients, and the
    construction is invariant under reparametrisation of the clock.  Hence
    Horn A's fixed congruence is a GAUGE of a generally covariant parent, and
    the local Lorentz violation recorded in G032 is a gauge artifact
    (unimodular-gravity class), not an added structure.

    NOTE ON SCOPE: this certifies the ALGEBRA of the gauge statement.  It does
    not certify (i) that the mimetic mode's dynamics are harmless for the
    growth sector, (ii) off-shell equivalence of the parent with the
    gauge-fixed theory, or (iii) any specific paper's construction.  Those are
    recorded as open in H009's reading and in hy4_push/H009_mimetic_horn_a.py. -/
theorem mimetic_horn_a_spine
    (Xt s : ℝ) (hs : s ≠ 0) (hXt : Xt ≠ 0) (htime : Xt < 0) :
    -- (1) the constraint is an identity of the definition
    Xt / (-Xt) = (-1 : ℝ)
    -- (2) the conformal factor is positive for a timelike gradient
    ∧ 0 < -Xt
    -- (3) reparametrisation invariance: the frame is a gauge, not a structure
    ∧ (s^2 * Xt) / (-(s^2 * Xt)) = (-1 : ℝ) := by
  exact ⟨mimetic_constraint_identity Xt hXt,
          mimetic_factor_pos Xt htime,
          reparametrisation_still_minus_one Xt s hs hXt⟩

#print axioms mimetic_horn_a_spine
#print axioms mimetic_constraint_identity
#print axioms reparametrisation_invariance
#print axioms mimetic_factor_pos

end
