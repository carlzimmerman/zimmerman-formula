import Mathlib
import Mathlib.Tactic
noncomputable section
open Real

-- AS081 API probe: derivative-of-log/laplacian certificates, mathlib v4.34.0-rc2
#check Real.hasDerivAt_log
#check Real.deriv_log
#check HasDerivAt.deriv
#check HasDerivAt.const_mul
#check HasDerivAt.congr_of_eventuallyEq
#check HasDerivAt.inv
#check deriv_inv
#check deriv_add
#check div_eq_mul_inv
#check mul_assoc
#check sq_eq_sq_iff_eq_or_eq_neg
#check isOpen_Ioi.mem_nhds
#check IsOpen.mem_nhds

-- small lemma: derivative of x ↦ x⁻¹ for x ≠ 0, HasDerivAt form
example (r : ℝ) (hr : r ≠ 0) : HasDerivAt (fun x : ℝ => x⁻¹) (-(r⁻¹) ^ 2) r := by
  exact hasDerivAt_inv r hr