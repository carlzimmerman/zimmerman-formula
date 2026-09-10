import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace CubicStaticGate

/- These are conditional algebraic consequences of the explicitly reduced
radial action. They do not formalize the weak-field reduction of a GR action. -/
theorem fixed_acceleration_two_radius_obstruction
    (r1 r2 gamma u fy b g : ℝ)
    (h1r : r1 ≠ 0) (h2r : r2 ≠ 0) (hg : gamma ≠ 0) (hu : u ≠ 0)
    (h1 : fy*u + 2*gamma*u^2/r1 = b*g/2)
    (h2 : fy*u + 2*gamma*u^2/r2 = b*g/2) : r1 = r2 := by
  have he : 2*gamma*u^2/r1 = 2*gamma*u^2/r2 := by linarith
  have hn : (2:ℝ)*gamma*u^2 ≠ 0 :=
    mul_ne_zero (mul_ne_zero (by norm_num) hg) (pow_ne_zero 2 hu)
  have hh := (div_eq_div_iff h1r h2r).mp he
  exact (mul_left_cancel₀ hn hh).symm

/-- E can be exp(-g/a0), but that function is a target INPUT, not derived here. -/
theorem metric_flux_fixes_scalar_gradient
    (M b u g E : ℝ) (hM : M ≠ 0) (hb : b ≠ 0)
    (h : g-b*u/(2*M) = g*(1-E)) : u = 2*M*g*E/b := by
  apply (eq_div_iff hb).2
  field_simp at h
  nlinarith [h]

#print axioms fixed_acceleration_two_radius_obstruction
#print axioms metric_flux_fixes_scalar_gradient
end CubicStaticGate
