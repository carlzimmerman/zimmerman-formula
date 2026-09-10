import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

namespace ClockEllipticity

/- r = sqrt(1+Y/ell), Q^2 = X+Y. These are the two eigenvalues
of the spatial principal tensor, expressed using r. The bridge to that
tensor is symbolic differentiation in ellipticity.py, not a Lean GR library. -/
theorem transverse_identity (U d ell X r : ℝ) (hr : r ≠ 0) :
    U-2*d*ell+2*d*ell*r-2*d*(X+ell*(r^2-1))/r =
    (U-2*d*ell)*(1-1/r)+(U-2*d*X)/r := by
  field_simp
  <;> ring

theorem longitudinal_identity (U d ell X r : ℝ) (hr : r ≠ 0) :
    U-2*d*ell+2*d*ell/r-2*d*(X+ell*(r^2-1))/r^3 =
    (U-2*d*ell)*(1-1/r^3)+(U-2*d*X)/r^3 := by
  field_simp
  <;> ring

theorem eigenvalue_positive (W0 D t : ℝ)
    (hW : 0 ≤ W0) (hD : 0 < D) (ht : 1 ≤ t) :
    0 < W0*(1-1/t)+D/t := by
  have ht0 : 0 < t := by linarith
  have hi : 1/t ≤ (1:ℝ) := (div_le_iff₀ ht0).2 (by linarith)
  have hp : 0 ≤ W0*(1-1/t) := mul_nonneg hW (by linarith)
  exact add_pos_of_nonneg_of_pos hp (div_pos hD ht0)

theorem both_eigenvalues_positive (U d ell X r : ℝ)
    (hW : 0 ≤ U-2*d*ell) (hD : 0 < U-2*d*X) (hr : 1 ≤ r) :
    0 < U-2*d*ell+2*d*ell*r-2*d*(X+ell*(r^2-1))/r ∧
    0 < U-2*d*ell+2*d*ell/r-2*d*(X+ell*(r^2-1))/r^3 := by
  have hr0 : r ≠ 0 := ne_of_gt (by linarith : 0 < r)
  have hr3 : 1 ≤ r^3 := by nlinarith [sq_nonneg (r-1)]
  rw [transverse_identity U d ell X r hr0,
      longitudinal_identity U d ell X r hr0]
  exact ⟨eigenvalue_positive _ _ _ hW hD hr,
         eigenvalue_positive _ _ _ hW hD hr3⟩

/-- The stationary action's coefficients satisfy the needed W0 condition. -/
theorem stationary_margin (A q m : ℝ) (hA : 0 < A) (hq : 0 < q) (hm : 0 < m) :
    0 < m*q*A - 2*(A*(m*q*A)/(2*q*(q*A+m*q*A)))*(q^2*m/2) := by
  have hqA : q*A+m*q*A ≠ 0 := ne_of_gt (by positivity)
  have hq0 : q ≠ 0 := ne_of_gt hq
  have hm1 : 1+m ≠ 0 := ne_of_gt (by positivity)
  have ident : m*q*A - 2*(A*(m*q*A)/(2*q*(q*A+m*q*A)))*(q^2*m/2)
      = m*q*A*(2+m)/(2*(1+m)) := by
    field_simp
    <;> ring
  rw [ident]
  positivity

#print axioms both_eigenvalues_positive
#print axioms stationary_margin
end ClockEllipticity
