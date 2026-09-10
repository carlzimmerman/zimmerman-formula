import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Conditional algebra for the action-derived principal symbol.
The action variation and Legendre transform are checked in SymPy, not assumed
to be formalized by these theorems. No theorem here proves a law of nature. -/
namespace TraceVariance

noncomputable def radialAlpha (y : ℝ) : ℝ := Real.exp (-y) * (1-y)
noncomputable def speedSquared (A alpha : ℝ) : ℝ := (1-alpha)/(A*alpha)

theorem radialAlpha_negative (y : ℝ) (hy : 1 < y) : radialAlpha y < 0 := by
  exact mul_neg_of_pos_of_neg (Real.exp_pos _) (by linarith)

theorem positive_kinetic_negative_radial_speed
    (A y : ℝ) (hA : 0 < A) (hy : 1 < y) :
    speedSquared A (radialAlpha y) < 0 := by
  have ha := radialAlpha_negative y hy
  exact div_neg_of_pos_of_neg (by linarith) (mul_neg_of_pos_of_neg hA ha)

theorem unstable_angular_cone
    (y costheta : ℝ) (hcone : 1 < y * costheta^2) :
    Real.exp (-y) * (1-y*costheta^2) < 0 := by
  exact mul_neg_of_pos_of_neg (Real.exp_pos _) (by linarith)

theorem frozen_and_actual_coefficients_have_opposite_signs
    (y : ℝ) (hy : 1 < y) :
    0 < Real.exp (-y) ∧ radialAlpha y < 0 := by
  exact ⟨Real.exp_pos _, radialAlpha_negative y hy⟩

#print axioms positive_kinetic_negative_radial_speed
#print axioms unstable_angular_cone
end TraceVariance
