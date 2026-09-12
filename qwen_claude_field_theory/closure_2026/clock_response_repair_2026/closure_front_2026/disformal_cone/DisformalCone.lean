import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

/- Conditional algebra only: neither the action variation nor a physical
interpretation of these real variables is formalized in this file. -/
namespace DisformalCone

theorem equal_cones_force_zero_disformal (C D : ℝ) (hC : C ≠ 0)
    (h : (C-D)/C = 1) : D = 0 := by
  have hmul := (div_eq_iff hC).mp h
  linarith

theorem no_slip_common_cone_has_no_linear_scalar_shift (c d : ℝ)
    (hslip : c-d = -c) (hcone : -2*d = 0) : c = 0 ∧ d = 0 := by
  constructor <;> linarith

theorem nonzero_null_ray_has_nonzero_time (t x y z : ℝ)
    (hnull : t^2 = x^2+y^2+z^2)
    (hnonzero : 0 < t^2+x^2+y^2+z^2) : t^2 ≠ 0 := by
  intro h
  nlinarith

theorem disformal_null_ray_obstruction (D t x y z : ℝ) (hD : D ≠ 0)
    (hnull : t^2 = x^2+y^2+z^2)
    (hnonzero : 0 < t^2+x^2+y^2+z^2) : D*t^2 ≠ 0 := by
  exact mul_ne_zero hD (nonzero_null_ray_has_nonzero_time t x y z hnull hnonzero)

theorem exponential_comparison_equal_cones (phi : ℝ)
    (h : Real.exp (4*phi) = 1) : phi = 0 := by
  have he : Real.exp (4*phi) = Real.exp 0 := by simpa using h
  have hinj := Real.exp_injective he
  linarith

#print axioms equal_cones_force_zero_disformal
#print axioms no_slip_common_cone_has_no_linear_scalar_shift
#print axioms nonzero_null_ray_has_nonzero_time
#print axioms disformal_null_ray_obstruction
#print axioms exponential_comparison_equal_cones
end DisformalCone
