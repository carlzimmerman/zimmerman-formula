import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace ExactExponentialScaleLock

/-! The calculus step (the unit slope of 1-exp(-u)) is certified by SymPy.
    These lemmas certify the exact algebraic consequence: once slope matching
    fixes a0=aLambda, the dimensionless coefficient is one; kappa=1/2 would
    require a slope ratio two. -/

theorem scale_matching_forces_equal {a0 aL : ℝ}
    (ha0 : 0 < a0) (haL : 0 < aL)
    (hslope : 1 / a0 = 1 / aL) : a0 = aL := by
  field_simp at hslope
  linarith

theorem scale_free_exponential_kappa_one {a0 aL κ : ℝ}
    (ha0 : 0 < a0) (haL : 0 < aL)
    (hscale : a0 = κ * aL)
    (hslope : 1 / a0 = 1 / aL) : κ = 1 := by
  have heq : a0 = aL := scale_matching_forces_equal ha0 haL hslope
  have hL : aL ≠ 0 := ne_of_gt haL
  rw [heq] at hscale
  apply (mul_left_cancel₀ hL)
  calc
    aL * κ = κ * aL := by ring
    _ = aL := hscale.symm
    _ = aL * 1 := by ring

theorem half_requires_slope_ratio_two {a0 aL : ℝ}
    (ha0 : 0 < a0) (haL : 0 < aL)
    (hk : a0 = (1 / 2 : ℝ) * aL) :
    (1 / a0) / (1 / aL) = 2 := by
  field_simp
  nlinarith

end ExactExponentialScaleLock
