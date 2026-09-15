/-
  H019 -- THE ZIMMERMAN FORMULA IS THE SEESAW: Lean certificate.

  THE CLOSURE.  Two formulae that the field has treated as separate
  "coincidences" are one equation:

      a_0 = (1/2) c sqrt(G rho_Lambda)          [Zimmerman]
      a_0 = Lambda^2 / (2 M_Pl)                 [the MOND seesaw]

  In natural units (hbar = c = 1), where rho_Lambda = Lambda^4 and
  M_Pl = 1/sqrt(G):

      (1/2) sqrt(G rho_Lambda) = (1/2) sqrt(G) Lambda^2
                               = (1/2) Lambda^2 / M_Pl
                               = Lambda^2 / (2 M_Pl)

  So the factor 1/2 in the Zimmerman formula is 1/n with n = 2, the
  transverse polarization count of the graviton -- derived in H017
  (n = D(D-3)/2 = 2 at D = 4) and H018 (from the action's static response:
  one monopole, two degenerate helicities).

  We certify the ALGEBRAIC identity, holding the physical relations as
  hypotheses (Lean has no unit system here; the numerical agreement
  1.000000000000000 is H019's measurement):

    (1) the seesaw identity:  (1/2) sqrt(G) * Lambda^2 = Lambda^2/(2 M_Pl)
        given sqrt(G) * M_Pl = 1;
    (2) with rho = Lambda^4: (1/2) sqrt(G rho) = Lambda^2/(2 M_Pl);
    (3) Lambda is fixed by a_0 and M_Pl:  Lambda^2 = 2 M_Pl a_0;
    (4) dark energy: f(0) = -1 gives w = -1 with rho > 0;
    (5) the conjunction.

  SCOPE: D = 4 (hence n = 2) remains an input, used once in the transverse-
  traceless projector (H018).  Deriving D = 4 from the action is not claimed.

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Sqrt

noncomputable section

open Real

/-! ## The seesaw identity -/

/-- (1) If sqrt(G) * M_Pl = 1 (i.e. M_Pl = 1/sqrt(G), the natural-units Planck
    mass), then (1/2) sqrt(G) Lambda^2 = Lambda^2/(2 M_Pl).  Certified with
    G and M_Pl positive so the divisions are well behaved. -/
theorem seesaw_identity (G MPl Lambda : ℝ)
    (hG : 0 < G) (hM : 0 < MPl) (hPl : Real.sqrt G * MPl = 1) :
    (1/2 : ℝ) * Real.sqrt G * Lambda^2 = Lambda^2 / (2 * MPl) := by
  have hsq : Real.sqrt G = 1 / MPl := by
    exact eq_div_of_mul_eq (ne_of_gt hM) hPl
  rw [hsq]
  ring

/-- (2) With rho_Lambda = Lambda^4, the Zimmerman form (1/2) sqrt(G rho) is
    the seesaw.  Uses sqrt(G * Lambda^4) = sqrt(G) * Lambda^2. -/
theorem zimmerman_is_seesaw (G MPl Lambda : ℝ)
    (hG : 0 < G) (hM : 0 < MPl) (hL : 0 ≤ Lambda)
    (hPl : Real.sqrt G * MPl = 1) :
    (1/2 : ℝ) * Real.sqrt (G * Lambda^4) = Lambda^2 / (2 * MPl) := by
  have hL2 : 0 ≤ Lambda^2 := sq_nonneg Lambda
  have hsqrt : Real.sqrt (G * Lambda^4) = Real.sqrt G * Lambda^2 := by
    -- Lambda^4 = (Lambda^2)^2 with Lambda^2 >= 0
    have h4 : Lambda^4 = (Lambda^2)^2 := by ring
    rw [h4]
    rw [Real.sqrt_mul (le_of_lt hG), Real.sqrt_sq_eq_abs, abs_of_nonneg hL2]
  rw [hsqrt]
  simpa [mul_assoc] using seesaw_identity G MPl Lambda hG hM hPl

/-! ## Lambda is fixed, not fitted -/

/-- (3) Lambda^2 = 2 M_Pl a_0: fixing a_0 and M_Pl fixes the dark-energy
    scale.  No reference to the observed rho_Lambda is needed. -/
theorem lambda_fixed_by_a0 (MPl a0 Lambda : ℝ)
    (h : a0 = Lambda^2 / (2 * MPl)) (hM : MPl ≠ 0) :
    Lambda^2 = 2 * MPl * a0 := by
  rw [h]
  field_simp [hM]

/-- Lambda is positive: Lambda = sqrt(2 M_Pl a_0) for positive M_Pl, a_0. -/
theorem lambda_sqrt_form (MPl a0 : ℝ) (hM : 0 < MPl) (ha : 0 < a0) :
    0 < Real.sqrt (2 * MPl * a0) := by
  apply Real.sqrt_pos.2
  nlinarith

/-! ## Dark energy -/

/-- The free function at zero gradient.  f(0) = -1 is the statement that dark
    energy is the value of the MOND function at the vacuum. -/
def f_zero : ℝ := -1

theorem f_zero_value : f_zero = -1 := by rfl

/-- (4) w = -1 with positive energy density: p = f(0) = -1,
    rho = 2*0*f' - f(0) = +1. -/
theorem dark_energy_w : f_zero / (2 * (0:ℝ) * (0:ℝ) - f_zero) = (-1 : ℝ) := by
  unfold f_zero
  norm_num

theorem dark_energy_rho_pos : 0 < (2 * (0:ℝ) * (0:ℝ) - f_zero) := by
  unfold f_zero
  norm_num

/-! ## The spine -/

/-- THE SPINE.  The Zimmerman formula and the MOND seesaw are one equation;
    the 1/2 is 1/n with n = 2 the graviton's polarization count (H017/H018);
    Lambda is fixed by a_0 and M_Pl rather than fitted; and dark energy is the
    zero-mode of the MOND scalar, f(0) = -1 giving w = -1 with rho > 0.

    One field, one function, one scale.  SCOPE: D = 4 remains input. -/
theorem zimmerman_seesaw_spine (G MPl Lambda a0 : ℝ)
    (hG : 0 < G) (hM : 0 < MPl) (hL : 0 ≤ Lambda)
    (hPl : Real.sqrt G * MPl = 1)
    (ha0 : a0 = Lambda^2 / (2 * MPl)) :
    -- the Zimmerman form IS the seesaw
    (1/2 : ℝ) * Real.sqrt (G * Lambda^4) = Lambda^2 / (2 * MPl)
    -- Lambda is fixed by a_0 and M_Pl
    ∧ Lambda^2 = 2 * MPl * a0
    -- dark energy: w = -1
    ∧ f_zero / (2 * (0:ℝ) * (0:ℝ) - f_zero) = (-1 : ℝ)
    -- positive energy density
    ∧ 0 < (2 * (0:ℝ) * (0:ℝ) - f_zero) := by
  have hMne : MPl ≠ 0 := ne_of_gt hM
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact zimmerman_is_seesaw G MPl Lambda hG hM hL hPl
  · exact lambda_fixed_by_a0 MPl a0 Lambda ha0 hMne
  · exact dark_energy_w
  · exact dark_energy_rho_pos

#print axioms zimmerman_seesaw_spine
#print axioms seesaw_identity
#print axioms zimmerman_is_seesaw
#print axioms lambda_fixed_by_a0
#print axioms dark_energy_w

end
