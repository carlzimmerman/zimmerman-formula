import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/- Conditional algebraic consequences of the independently varied equations
in derive.py. Covariant variation, gauges and PDE existence are not formalized
here. Perfect-fluid scalar sources only: free-streaming shear is excluded. -/
namespace CosmologicalBridge
noncomputable section

theorem shear_equation_implies_equal_potentials
    (M2 a k phi psi : ℝ) (hM : M2 ≠ 0) (ha : a ≠ 0) (hk : k ≠ 0)
    (equation : -M2*a*k^2*(phi-psi)=0) : phi=psi := by
  have hc : -M2*a*k^2 ≠ 0 := mul_ne_zero (mul_ne_zero (neg_ne_zero.mpr hM) ha)
    (pow_ne_zero 2 hk)
  exact sub_eq_zero.mp ((mul_eq_zero.mp equation).resolve_left hc)

/-- Matter/clock energy Ward identity needs BOTH clock equations. -/
theorem on_shell_energy_conserved
    (energy q deltaJ deltaQ backgroundJ clockRate deltaClock alpha backgroundClock : ℝ)
    (ward : energy=q*deltaJ+deltaQ*backgroundJ-clockRate*deltaClock
                       +clockRate*alpha*backgroundClock)
    (hj : deltaJ=0) (hjb : backgroundJ=0)
    (hc : deltaClock=0) (hcb : backgroundClock=0) : energy=0 := by
  simpa [hj,hjb,hc,hcb] using ward

#print axioms shear_equation_implies_equal_potentials
#print axioms on_shell_energy_conserved
end
end CosmologicalBridge
