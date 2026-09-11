import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
Conditional small-source obstruction for the exact exponential constitutive law.

The force bound 0 ≤ g ≤ C ε is an INPUT, not a PDE conclusion. There are no
assertions here about existence, smooth source dependence, domain uniformity,
nonlinear evolution, cosmological matching, or a measured Newton constant.
All statements concern the displayed real function at positive a0 and ε.
-/

namespace ConditionalSmallSource

noncomputable section

def mondForce (a0 g : ℝ) : ℝ := (1 - Real.exp (-(g / a0))) * g

/-- The standard exponential tangent bound, with no series approximation. -/
theorem exponential_upper (x : ℝ) : 1 - Real.exp (-x) ≤ x := by
  have h := Real.add_one_le_exp (-x)
  linarith

/-- Nonnegative force for the stated nonnegative acceleration branch. -/
theorem mondForce_nonneg (a0 g : ℝ) (ha : 0 < a0) (hg : 0 ≤ g) :
    0 ≤ mondForce a0 g := by
  have hquot : 0 ≤ g / a0 := div_nonneg hg ha.le
  have hexp : Real.exp (-(g / a0)) ≤ 1 :=
    Real.exp_le_one_iff.mpr (neg_nonpos.mpr hquot)
  exact mul_nonneg (sub_nonneg.mpr hexp) hg

/-- At any nonnegative g, the exact exponential force is at most quadratic. -/
theorem mondForce_le_quadratic (a0 g : ℝ) (hg : 0 ≤ g) :
    mondForce a0 g ≤ g^2 / a0 := by
  calc
    mondForce a0 g ≤ (g / a0) * g :=
      mul_le_mul_of_nonneg_right (exponential_upper (g / a0)) hg
    _ = g^2 / a0 := by ring

/-- The assumed linear source bound supplies the quadratic epsilon bound. -/
theorem conditional_quadratic_bound (a0 C ε g : ℝ)
    (ha : 0 < a0) (hg : 0 ≤ g) (hbound : g ≤ C * ε) :
    mondForce a0 g ≤ C^2 * ε^2 / a0 := by
  have hsq : g^2 ≤ (C * ε)^2 := by
    simpa only [pow_two] using mul_self_le_mul_self hg hbound
  calc
    mondForce a0 g ≤ g^2 / a0 := mondForce_le_quadratic a0 g hg
    _ ≤ (C * ε)^2 / a0 := div_le_div_of_nonneg_right hsq ha.le
    _ = C^2 * ε^2 / a0 := by ring

/-- A quantitative normalized estimate; this does not derive its PDE premise. -/
theorem conditional_normalized_bound (a0 n C ε g : ℝ)
    (ha : 0 < a0) (hn : 0 < n) (he : 0 < ε)
    (hg : 0 ≤ g) (hbound : g ≤ C * ε) :
    0 ≤ mondForce a0 g / (ε * n) ∧
      mondForce a0 g / (ε * n) ≤ C^2 * ε / (a0 * n) := by
  constructor
  · exact div_nonneg (mondForce_nonneg a0 g ha hg) (mul_pos he hn).le
  · calc
      mondForce a0 g / (ε * n) ≤ (C^2 * ε^2 / a0) / (ε * n) :=
        div_le_div_of_nonneg_right (conditional_quadratic_bound a0 C ε g ha hg hbound)
          (mul_pos he hn).le
      _ = C^2 * ε / (a0 * n) := by
        field_simp

/-- Below the explicit threshold, equality with the linear Newtonian source fails. -/
theorem conditional_force_lt_source (a0 n C ε g : ℝ)
    (ha : 0 < a0) (_hn : 0 < n) (hC : 0 < C) (he : 0 < ε)
    (hg : 0 ≤ g) (hbound : g ≤ C * ε)
    (hsmall : ε < a0 * n / C^2) :
    mondForce a0 g < ε * n := by
  have hc2 : 0 < C^2 := sq_pos_of_pos hC
  have hsmall' : ε * C^2 < a0 * n := (lt_div_iff₀ hc2).mp hsmall
  have hscaled := mul_lt_mul_of_pos_right hsmall' he
  have hquadratic : C^2 * ε^2 / a0 < ε * n := by
    apply (div_lt_iff₀ ha).2
    nlinarith only [hscaled]
  exact lt_of_le_of_lt (conditional_quadratic_bound a0 C ε g ha hg hbound) hquadratic

/-- A nonzero linear Newtonian source cannot obey the exact law in that range. -/
theorem conditional_not_exact_mond (a0 n C ε g : ℝ)
    (ha : 0 < a0) (hn : 0 < n) (hC : 0 < C) (he : 0 < ε)
    (hg : 0 ≤ g) (hbound : g ≤ C * ε)
    (hsmall : ε < a0 * n / C^2) :
    mondForce a0 g ≠ ε * n := by
  exact ne_of_lt (conditional_force_lt_source a0 n C ε g ha hn hC he hg hbound hsmall)

#print axioms exponential_upper
#print axioms mondForce_nonneg
#print axioms mondForce_le_quadratic
#print axioms conditional_quadratic_bound
#print axioms conditional_normalized_bound
#print axioms conditional_force_lt_source
#print axioms conditional_not_exact_mond

end

end ConditionalSmallSource
