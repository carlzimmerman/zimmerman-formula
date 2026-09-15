/-
  H020 -- THE SEVEN: Lean certificate.

    a_0 = (1/2) c sqrt(G rho_Lambda)                     [Zimmerman]
    rho_Lambda = Omega_L rho_c,   rho_c = 3 H_0^2/(8 pi G)

  Substituting, G CANCELS:

    a_0 = (1/2) c H_0 sqrt( 3 Omega_L / (8 pi) )

  hence

    c H_0 / a_0 = sqrt( 32 pi / (3 Omega_L) ) = 6.994

  This DERIVES the programme's registered boundary "c H_0 = 7 a_0"
  (G016/G050's Hubble-kernel boundary): the 7 was the rounding of 6.994.

  Because G cancels, the MOND/Hubble ratio is pure cosmology -- it does not
  know the strength of gravity.  a_0/(cH_0) depends on Omega_Lambda ALONE,
  which answers the oldest puzzle in MOND ("why is a_0 of order cH_0?").

  CONSEQUENCE: the kernel growth raise at z = 0 is
      (a_0/(cH_0))^2 = 3 Omega_L/(32 pi),
  a pure number.  The S_8 tension is therefore a PREDICTION, not a knob.

  Certified: (1) the G-cancellation; (2) the Seven ratio;
  (3) the growth-raise square; (4) the conjunction.  Physical constants enter
  as hypotheses (Lean has no unit system here); the numerical agreement
  (1.000000000000) is H020's measurement.

  SCOPE: Omega_Lambda = 0.685 is a measured input.  What is derived is the
  RELATION, not the value of Omega_Lambda.  D = 4 (H018) also remains input.

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Sqrt

noncomputable section

open Real

/-! ## Definitions -/

def rho_crit (H0 G : ℝ) : ℝ := 3 * H0^2 / (8 * Real.pi * G)
def rho_Lam  (OmL H0 G : ℝ) : ℝ := OmL * rho_crit H0 G
def a0_of_rhoL (c G rhoL : ℝ) : ℝ := (1/2 : ℝ) * c * Real.sqrt (G * rhoL)

/-! ## (1) The G-cancellation -/

theorem G_cancellation (c G H0 OmL : ℝ)
    (hG : G ≠ 0) (hpi : Real.pi ≠ 0) :
    a0_of_rhoL c G (rho_Lam OmL H0 G)
      = (1/2 : ℝ) * c * Real.sqrt (3 * OmL * H0^2 / (8 * Real.pi)) := by
  unfold a0_of_rhoL rho_Lam rho_crit
  have hden : (8 * Real.pi * G : ℝ) ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (by norm_num) hpi) hG
  have harg : G * (OmL * (3 * H0^2 / (8 * Real.pi * G)))
                = 3 * OmL * H0^2 / (8 * Real.pi) := by
    field_simp [hden]
  rw [harg]

/-- H_0 factors out of the square root (for H_0 >= 0). -/
theorem H0_out_of_sqrt (H0 OmL : ℝ) (hH : 0 ≤ H0) (hO : 0 ≤ OmL) :
    Real.sqrt (3 * OmL * H0^2 / (8 * Real.pi))
      = H0 * Real.sqrt (3 * OmL / (8 * Real.pi)) := by
  have hsq : 3 * OmL * H0^2 / (8 * Real.pi) = H0^2 * (3 * OmL / (8 * Real.pi)) := by ring
  rw [hsq]
  rw [Real.sqrt_mul (sq_nonneg H0)]
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg hH]

/-- The full G-cancelled form of a_0. -/
theorem a0_omega_form (c G H0 OmL : ℝ)
    (hG : G ≠ 0) (hpi : Real.pi ≠ 0) (hH : 0 ≤ H0) (hO : 0 ≤ OmL) :
    a0_of_rhoL c G (rho_Lam OmL H0 G)
      = (1/2 : ℝ) * c * H0 * Real.sqrt (3 * OmL / (8 * Real.pi)) := by
  rw [G_cancellation c G H0 OmL hG hpi]
  rw [H0_out_of_sqrt H0 OmL hH hO]
  ring

/-! ## (2) The Seven -/

theorem seven_identity (c H0 OmL : ℝ) (hO : 0 < OmL) :
    ((1/2 : ℝ) * c * H0 * Real.sqrt (3 * OmL / (8 * Real.pi)))
      * Real.sqrt (32 * Real.pi / (3 * OmL)) = c * H0 := by
  have hApos : 0 < 3 * OmL / (8 * Real.pi) := by positivity
  have hprod : (3 * OmL / (8 * Real.pi)) * (32 * Real.pi / (3 * OmL)) = 4 := by
    field_simp
    ring
  have hmul : Real.sqrt (3 * OmL / (8 * Real.pi))
                * Real.sqrt (32 * Real.pi / (3 * OmL)) = 2 := by
    rw [← Real.sqrt_mul (le_of_lt hApos), hprod]
    norm_num
  rw [mul_assoc, hmul]
  ring

/-! ## (3) The growth raise -/

theorem raise_square (OmL : ℝ) (hO : 0 ≤ OmL) :
    (Real.sqrt (3 * OmL / (32 * Real.pi)))^2 = 3 * OmL / (32 * Real.pi) := by
  rw [Real.sq_sqrt]
  positivity

theorem raise_bounded (OmL : ℝ) (hO0 : 0 < OmL) (hO1 : OmL < 1) :
    0 < 3 * OmL / (32 * Real.pi) ∧ 3 * OmL / (32 * Real.pi) < 1 := by
  constructor
  · positivity
  · have hpipos : 0 < Real.pi := Real.pi_pos
    have h3lt : (3 : ℝ) < 32 * Real.pi := by nlinarith [Real.pi_gt_three]
    have hpos : 0 < 32 * Real.pi := by positivity
    have hlt3 : 3 * OmL < 3 := by nlinarith
    have : 3 * OmL < 32 * Real.pi := by linarith
    exact (div_lt_one hpos).2 this

/-! ## (4) The spine -/

theorem seven_spine (c G H0 OmL : ℝ)
    (hG : G ≠ 0) (hpi : Real.pi ≠ 0) (hH : 0 ≤ H0) (hO : 0 < OmL) :
    a0_of_rhoL c G (rho_Lam OmL H0 G)
      = (1/2 : ℝ) * c * H0 * Real.sqrt (3 * OmL / (8 * Real.pi))
    ∧ ((1/2 : ℝ) * c * H0 * Real.sqrt (3 * OmL / (8 * Real.pi)))
        * Real.sqrt (32 * Real.pi / (3 * OmL)) = c * H0
    ∧ (Real.sqrt (3 * OmL / (32 * Real.pi)))^2 = 3 * OmL / (32 * Real.pi) := by
  refine ⟨?_, ?_, ?_⟩
  · exact a0_omega_form c G H0 OmL hG hpi hH (le_of_lt hO)
  · exact seven_identity c H0 OmL hO
  · exact raise_square OmL (le_of_lt hO)

#print axioms seven_spine
#print axioms G_cancellation
#print axioms a0_omega_form
#print axioms seven_identity
#print axioms raise_square

end
