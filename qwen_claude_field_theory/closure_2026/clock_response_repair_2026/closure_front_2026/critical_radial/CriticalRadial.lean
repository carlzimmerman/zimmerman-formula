import Mathlib.Data.Real.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-! Algebra of the explicitly retained radial action. These theorems do not
derive the covariant equations, validate the omitted-term hierarchy, or identify
a scalar charge with baryonic mass. The source appears through the metric row.+-/
namespace CriticalRadial
noncomputable section

/-- Source compatibility after elimination without division by the critical G.
The radial scalar row is multiplied by r to avoid a hidden r=0 division. -/
theorem metric_induced_radial_source (M b G0 gamma r p g gN : ℝ)
    (hmetric : M*g = M*gN+b*p)
    (hscalar : G0*r*p-2*b*r*g+4*gamma*p^2 = 0) :
    (M*G0-2*b^2)*r*p+4*M*gamma*p^2 = 2*M*b*r*gN := by
  linear_combination M*hscalar+2*b*r*hmetric

/-- At the critical coefficient, the retained nonlinearity balances the
minimally induced source. No inverse critical coefficient is introduced. -/
theorem critical_nonlinear_balance (M b G0 gamma r p g gN : ℝ)
    (hmetric : M*g = M*gN+b*p)
    (hscalar : G0*r*p-2*b*r*g+4*gamma*p^2 = 0)
    (hcritical : M*G0 = 2*b^2) :
    4*M*gamma*p^2 = 2*M*b*r*gN := by
  have h := metric_induced_radial_source M b G0 gamma r p g gN hmetric hscalar
  rw [hcritical] at h
  simpa using h

/-- The additional r^3*p^3 metric terms cancel on the critical null direction.
The remaining pi*p^2 coefficient is the one in the symbolic action jet. -/
theorem critical_metric_cubic_cancellation (M alpha G0 H1 r p pi : ℝ)
    (hcritical : G0 = 2*M*alpha^2) :
    M*alpha^3*(r^2*pi*p^2+r^3*p^3)
      -2*M*alpha^3*(r^3*p^3+2*r^2*pi*p^2)
      +(G0*alpha*r*p-H1*alpha*pi)*r^2*p^2/2
    = -(alpha*(H1+3*G0)/2)*r^2*pi*p^2 := by
  rw [hcritical]
  ring

/-- A nonzero omitted linear coefficient cannot stay below a quadratic
amplitude remainder for every arbitrarily small positive amplitude. -/
theorem nonzero_linear_term_breaks_uniform_quadratic_bound (linear cap : ℝ)
    (hlinear : 0 < linear) (hcap : 0 < cap) :
    ¬ ∀ amplitude : ℝ, 0 < amplitude → linear ≤ cap*amplitude := by
  intro h
  have hamp : 0 < linear/(2*cap) := by positivity
  have hbound := h (linear/(2*cap)) hamp
  have heq : cap*(linear/(2*cap)) = linear/2 := by
    field_simp
  rw [heq] at hbound
  linarith

#print axioms metric_induced_radial_source
#print axioms critical_nonlinear_balance
#print axioms critical_metric_cubic_cancellation
#print axioms nonzero_linear_term_breaks_uniform_quadratic_bound
end
end CriticalRadial
