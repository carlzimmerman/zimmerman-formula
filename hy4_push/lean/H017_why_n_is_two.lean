/-
  H017 -- WHY n = 2: Lean certificate.

  The programme's last measured input is the integer n = 2, which appears
  TWICE: as the deep slope of the interpolating function mu_2 (the SHAPE of
  the acceleration relation) and as the coefficient in the seesaw
  a_0 = Lambda^2/(n M_Pl) (its SIZE).

  This file certifies the derivation of that integer from the dimensionality
  of spacetime:

      n = D(D-3)/2   (transverse polarizations of a massless spin-2 field
                      in D spacetime dimensions)

      n(4) = 2       -- the measured value
      n(D) = 2  <=>  D = 4  or  D = -1   (D = -1 unphysical)  -- unique
      n(3) = 0       -- 2+1 gravity has no propagating modes  -- boundary

  and the JOINT RELATION that follows if the counted modes are the
  gravitational field's:

      a_0 * M_Pl * n = Lambda^2

  which locks a shape observable (the slope) to a scale observable
  (a_0 M_Pl) through one integer.  Measured ratio 0.999980
  (H017_why_n_is_two.py).

  SCOPE: the polarization FORMULA n = D(D-3)/2 is standard kinematics taken
  here as the counting rule; what is certified is (i) its value at D = 4,
  (ii) the UNIQUENESS of that value, (iii) the boundary consistency at D = 3,
  and (iv) the algebraic form of the joint relation.  The step that would
  promote this from "derived by dimension" to "derived from the action" --
  showing the scalar's response sums over exactly the graviton's two
  transverse modes -- is NOT certified here and remains open.  Also stated:
  at D = 4 massless spin-1 has D-2 = 2 polarizations, so the COUNT alone is
  degenerate between spin-1 and spin-2; spin-0 (which gives 1) is excluded.

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

/-! ## The counting rule and its value -/

/-- The transverse-polarization count of a massless spin-2 field in D
    spacetime dimensions:  n(D) = D(D-3)/2. -/
def n_pol (D : ℤ) : ℤ := D * (D - 3) / 2

/-- (i) At D = 4 the count is 2 -- the SPARC mode count. -/
theorem n_at_four : n_pol 4 = 2 := by
  unfold n_pol
  norm_num

/-- (iii) At D = 3 the count is 0: no propagating gravitational degrees of
    freedom in 2+1 dimensions. The formula reproduces this without being
    told. -/
theorem n_at_three : n_pol 3 = 0 := by
  unfold n_pol
  norm_num

/-! ## Uniqueness -/

/-- (ii) n(D) = 2 forces D = 4 or D = -1.  Certified on the polynomial form
    D(D-3) = 4 (i.e. D^2 - 3D - 4 = 0, whose roots are 4 and -1).  The
    integer division in n_pol is avoided here because omega cannot see
    through it; the polynomial statement is the mathematical content. -/
theorem n_eq_two_roots (D : ℤ) (h : D * (D - 3) = 4) :
    D = 4 ∨ D = -1 := by
  have hfac : (D - 4) * (D + 1) = 0 := by nlinarith
  have hz := Int.eq_zero_or_eq_zero_of_mul_eq_zero hfac
  cases hz with
  | inl hD => left; omega
  | inr hD => right; omega

/-- The converse: both roots do give 2. -/
theorem n_of_root_neg_one : n_pol (-1) = 2 := by
  unfold n_pol
  norm_num

/-- D = -1 is unphysical, so among physical dimensions (D >= 3) the value
    n = 2 selects D = 4 uniquely. -/
theorem n_two_selects_four (D : ℤ) (hD : 3 ≤ D) (h : D * (D - 3) = 4) :
    D = 4 := by
  rcases n_eq_two_roots D h with h4 | hneg
  · exact h4
  · omega

/-! ## The spin degeneracy (stated, not resolved) -/

/-- Massless spin-1 in D dimensions has D - 2 polarizations; at D = 4 that
    is 2, degenerate with the spin-2 count. -/
def n_vec (D : ℤ) : ℤ := D - 2

theorem n_vec_at_four : n_vec 4 = 2 := by
  unfold n_vec
  norm_num

/-- Spin-0 has 1 polarization, so the measured n = 2 excludes a purely
    scalar counting. -/
theorem scalar_excluded : (1 : ℤ) ≠ 2 := by norm_num

/-! ## The joint relation -/

/-- (iv) If the counted modes are the gravitational field's, the same integer
    must appear in the deep slope and in the seesaw, giving
        a_0 * M_Pl * n = Lambda^2.
    Certified here as the algebraic statement with n = 2. -/
theorem joint_relation (a0 MPl Lambda : ℝ)
    (h : a0 * MPl * 2 = Lambda^2) :
    a0 * MPl * n_pol 4 = Lambda^2 := by
  norm_num [n_pol]
  exact h

/-- Equivalently: the seesaw with n = the polarization count. -/
theorem seesaw_from_polarizations (a0 MPl Lambda : ℝ)
    (h : a0 * MPl * 2 = Lambda^2) :
    a0 * 2 * MPl = Lambda^2 := by
  nlinarith

/-! ## The spine -/

/-- THE SPINE.  The mode count is the transverse-polarization count of a
    massless spin-2 field in four dimensions: n = D(D-3)/2 = 2 at D = 4,
    uniquely (the only other root is D = -1), and boundary-consistent
    (D = 3 gives 0, matching the absence of propagating 2+1 gravity).  The
    same integer governs the deep slope of mu_2 and the seesaw coefficient,
    locking a shape observable to a scale observable through
    a_0 M_Pl n = Lambda^2.

    SCOPE: the counting RULE is taken as standard kinematics.  What is open
    -- and stated -- is the action-level step: showing the scalar's response
    sums over exactly these two modes.  Until that is done, n = 2 is
    DERIVED BY DIMENSION, not derived from the action. -/
theorem n_two_spine :
    n_pol 4 = 2 ∧ n_pol 3 = 0 ∧ n_pol (-1) = 2
    ∧ (∀ D : ℤ, 3 ≤ D → D * (D - 3) = 4 → D = 4) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact n_at_four
  · exact n_at_three
  · exact n_of_root_neg_one
  · intro D hD h
    exact n_two_selects_four D hD h

#print axioms n_two_spine
#print axioms n_eq_two_roots
#print axioms n_two_selects_four
#print axioms joint_relation
#print axioms seesaw_from_polarizations

end
