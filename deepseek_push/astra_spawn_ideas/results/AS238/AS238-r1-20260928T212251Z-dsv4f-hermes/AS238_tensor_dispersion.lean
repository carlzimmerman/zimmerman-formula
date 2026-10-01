import Mathlib

/-!
AS238 — tensor dispersion on homogeneous occupied FLRW.
Certified algebraic identities (CA5-GNC-R branch, kappa = 1/2 adopted):

1. mass_cancel: the quadratic (mass) coefficient of the TT mode vanishes exactly
   under the occupied Friedmann pair  3 M H^2 = M*Lambda + T + V + V0,  M*Hdot = -T
   (occupies branch: Lambda = 0, gate inactive; this is the pre-Friedmann residual
   -(3 M H^2 + 2 M Hdot - M Lambda + T - V - V0)/4 -> 0).

2. kinetic_coeff: the canonical kinetic coefficient after the integration-by-parts
   identity <qdd q> = -<qd^2> (window boundaries at q = qd = 0): raw coefficient
   -(3/4) A - C  with C = -A  equals  (1/4) A  = (M/8)/(M/2) kinetic share.

3. shear_disp: with the diagnostic shear-squared operator kappa, the dispersion is
   (M + kappa) w^2 = M k^2/a^2, i.e. w^2 = (M/(M+kappa)) (k^2/a^2): the negative
   control must detect coefficient M/(M+kappa), not k^2/a^2.

4. onshell_substitution: q = cos(k z - w t) solves the k/a-damped-free EOM
   qdd + (k^2/a^2) q = 0 at H = 0 iff w^2 = k^2/a^2 (algebraic residual only).
-/

theorem mass_cancel (M H Hdot Lam T V V0 : ℝ)
    (h1 : 3*M*H^2 = M*Lam + T + V + V0)
    (h2 : M*Hdot = -T) :
    -(3*M*H^2 + 2*M*Hdot - M*Lam + T - V - V0)/4 = 0 := by
  nlinarith

theorem kinetic_coeff (A C : ℝ) (hC : C = -A) :
    -(3/4:ℝ)*A - C = (1/4:ℝ)*A := by
  nlinarith

theorem shear_disp (M kap k2 w2 : ℝ) (hM : M + kap ≠ 0)
    (h : (M+kap)*w2 = M*k2) :
    w2 = (M/(M+kap))*k2 := by
  calc
    w2 = (M*k2)/(M+kap) := by
      rw [← h]
      field_simp [hM]
    _ = (M/(M+kap))*k2 := by
      ring

theorem onshell_substitution (omega k2 : ℝ) (h : omega^2 = k2) :
    -omega^2 + k2 = 0 := by
  nlinarith

/- Axiom census (unfiltered): must be a subset of {propext, Classical.choice, Quot.sound}. -/
#print axioms mass_cancel
#print axioms kinetic_coeff
#print axioms shear_disp
#print axioms onshell_substitution