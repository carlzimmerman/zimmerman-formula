import Mathlib

namespace EquilibriumReview20260919

/-- Algebraic audit of the Euler force per unit background density.
`pressureForce` includes the derivative of rho=A/r^2; `backgroundForce`
is -delta_rho * Phi0' / rho.  Full PDE linearization is not formalized here. -/
theorem missing_background_force (s r x xp xpp : ℝ) (hr : r ≠ 0) :
    (s*xpp - 2*s/r*xp + 2*s/r^2*x) + 2*s/r*xp
      = s*xpp + 2*s/r^2*x := by ring

theorem old_linear_mode_not_zero (s r : ℝ) (hs : 0 < s) (hr : 0 < r) :
    s*0 + 2*s/r^2*r ≠ 0 := by positivity

theorem old_quadratic_mode_residual (s r : ℝ) (hr : r ≠ 0) :
    s*2 + 2*s/r^2*r^2 = 4*s := by field_simp; ring

/-- Conditional finite-annulus energy certificate: the displayed value is
computed independently from integral ((xi')^2 - 2 xi^2/r^2), xi=(r-1)(64-r)/r.
This theorem certifies negativity of that exact closed form, not spectral theory. -/
theorem trial_energy_negative : -(115605:ℝ)/64 + 1560*Real.log 2 < 0 := by
  have h : Real.log (2:ℝ) ≤ 1 := by
    have ht := Real.log_le_sub_one_of_pos (show (0:ℝ) < 2 by norm_num)
    norm_num at ht ⊢
    exact ht
  linarith

#print axioms missing_background_force
#print axioms old_linear_mode_not_zero
#print axioms old_quadratic_mode_residual
#print axioms trial_energy_negative
end EquilibriumReview20260919
