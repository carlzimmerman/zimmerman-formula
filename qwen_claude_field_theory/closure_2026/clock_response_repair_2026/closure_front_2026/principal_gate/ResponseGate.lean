import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

/- Exact real-algebra gates. The map from the covariant action to these
coefficients is derived separately in Python; it is NOT assumed proved here. -/
namespace ClosureResponseGate

theorem exponential_mu_upper (y : ℝ) :
    1 - Real.exp (-y) ≤ y := by
  have h := Real.add_one_le_exp (-y)
  linarith

theorem mond_acceleration_lower_bound (a0 g gN : ℝ)
    (ha : 0 < a0) (hg : 0 ≤ g)
    (hmond : g * (1 - Real.exp (-(g/a0))) = gN) :
    a0*gN ≤ g^2 := by
  calc
    a0*gN = a0*(g*(1-Real.exp (-(g/a0)))) := by rw [hmond]
    _ ≤ a0*(g*(g/a0)) :=
      mul_le_mul_of_nonneg_left
        (mul_le_mul_of_nonneg_left (exponential_mu_upper (g/a0)) hg) ha.le
    _ = g^2 := by field_simp

theorem finite_response_obstruction (a0 C g gN : ℝ)
    (ha : 0 < a0) (hC : 0 < C) (hn : 0 < gN) (hg : 0 ≤ g)
    (hresponse : g ≤ C*gN) (hsmall : C^2*gN < a0)
    (hmond : g * (1 - Real.exp (-(g/a0))) = gN) : False := by
  have hbound := mond_acceleration_lower_bound a0 g gN ha hg hmond
  have hprod := mul_nonneg (sub_nonneg.mpr hresponse)
    (add_nonneg (mul_nonneg hC.le hn.le) hg)
  have hstrict := mul_lt_mul_of_pos_right hsmall hn
  nlinarith

theorem regular_clock_bracket_nondegenerate (k C : ℝ)
    (hk : k ≠ 0) (hC : C ≠ 0) : 0 < (k^2*C)^2 := by
  exact sq_pos_of_ne_zero (mul_ne_zero (pow_ne_zero 2 hk) hC)

theorem braiding_sound_response_identity (G B K : ℝ)
    (hG : G ≠ 0) (hK : K ≠ 0) :
    (1+B/G)*(G/K) = (G+B)/K := by
  field_simp

theorem healthy_braiding_enhances (G B : ℝ)
    (hG : 0 < G) (hB : 0 < B) : 1 < 1+B/G := by
  have h := div_pos hB hG
  linarith

/-- The critical linear static field equations cannot support a nonzero
source with nonzero braiding. Nonlinear regularization is not excluded. -/
theorem critical_static_source_compatibility (M G0 b u v rho : ℝ)
    (hb : b ≠ 0)
    (hEinstein : 2*M*u = rho+2*b*v)
    (hScalar : G0*v = 2*b*u)
    (hCritical : M*G0 = 2*b^2) : rho = 0 := by
  have hprod : b*rho = 0 := by
    linear_combination -b*hEinstein-M*hScalar+v*hCritical
  exact (mul_eq_zero.mp hprod).resolve_left hb

#print axioms exponential_mu_upper
#print axioms mond_acceleration_lower_bound
#print axioms finite_response_obstruction
#print axioms regular_clock_bracket_nondegenerate
#print axioms braiding_sound_response_identity
#print axioms healthy_braiding_enhances
#print axioms critical_static_source_compatibility
end ClosureResponseGate
