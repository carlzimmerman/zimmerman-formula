import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# GRW1 MUTATE twin: seven false versions of GRW1.lean's closed forms. Each must fail (one error per theorem).
κ = ½ FITTED; not theory closed. Adopts nothing.
-/

namespace GRW1M

/-- false: the coefficient FALLS as c rises (strictly) -/
theorem bad_mono (q2 c1 c2 : ℝ) (hq : 0 < q2) (h1 : 0 ≤ c1) (h12 : c1 < c2) :
    1 - q2 / (1 + c2 * q2) < 1 - q2 / (1 + c1 * q2) := by
  have hp1 : 0 < 1 + c1 * q2 := by positivity
  have hp2 : 0 < 1 + c2 * q2 := by nlinarith
  rw [sub_lt_sub_iff_left, div_lt_div_iff₀ hp1 hp2]
  nlinarith

/-- false: at c = 1 the coefficient is 2/(1 + q²) -/
theorem bad_one (q2 : ℝ) (hq : 0 ≤ q2) : 1 - q2 / (1 + 1 * q2) = 2 / (1 + q2) := by
  have : (1 + q2) ≠ 0 := by positivity
  field_simp
  ring

/-- false: the AQUAL response with the angle term's sign flipped -/
theorem bad_aqual (x m : ℝ) (hx : 0 ≤ x) :
    1 - (1 / (1 + x)) * (1 - x * m ^ 2 / (1 + x)) = (x / (1 + x)) * (1 - m ^ 2 / (1 + x)) := by
  have : (1 + x) ≠ 0 := by positivity
  field_simp
  ring

/-- false: the equilibrium total with + 1 in the denominator -/
theorem bad_equilibrium (c q2 r : ℝ) (hc : 0 ≤ c) (hq : 0 ≤ q2) (h : 1 < (1 - c) * q2) :
    r + r * (1 + c * q2) / ((1 - c) * q2 - 1) = r * q2 / ((1 - c) * q2 + 1) := by
  obtain ⟨D, hDdef, hDpos⟩ : ∃ D : ℝ, D = (1 - c) * q2 - 1 ∧ 0 < D := ⟨_, rfl, by linarith⟩
  have hDne : D ≠ 0 := hDpos.ne'
  have hE : (1 - c) * q2 + 1 ≠ 0 := by nlinarith
  rw [← hDdef]
  field_simp
  rw [hDdef]
  ring

/-- false: the baryon exponent's quadratic without the factor 1/2 on f -/
theorem bad_baryons (f : ℝ) (hf : 0 ≤ f) :
    ((-1 + Real.sqrt (1 + 24 * f)) / 4) ^ 2 + ((-1 + Real.sqrt (1 + 24 * f)) / 4) / 2 = 3 * f := by
  have hs : Real.sqrt (1 + 24 * f) ^ 2 = 1 + 24 * f := Real.sq_sqrt (by linarith)
  linear_combination (1 / 16) * hs

/-- false: the eigenvalue equation with + f λ -/
theorem bad_lam (f : ℝ) (hf0 : 0 ≤ f) (hf1 : f ≤ 1) :
    ((f + Real.sqrt (f ^ 2 + 4 * f * (1 - f))) / 2) ^ 2 + f * ((f + Real.sqrt (f ^ 2 + 4 * f * (1 - f))) / 2)
      - f * (1 - f) = 0 := by
  have hs : Real.sqrt (f ^ 2 + 4 * f * (1 - f)) ^ 2 = f ^ 2 + 4 * f * (1 - f) := Real.sq_sqrt (by nlinarith)
  linear_combination (1 / 4) * hs

/-- false: c can exceed 1 (claimed for every x and angle) -/
theorem bad_cfac (x m : ℝ) (hx : 0 ≤ x) (hm0 : 0 ≤ m) (hm1 : m ≤ 1) :
    1 < (1 / (1 + x)) * (1 - x * m ^ 2 / (1 + x)) := by
  have hp : 0 < 1 + x := by linarith
  rw [div_mul_eq_mul_div, one_mul, lt_div_iff₀ hp]
  have : 0 ≤ x * m ^ 2 / (1 + x) := by positivity
  nlinarith

end GRW1M
-- κ = ½ FITTED; not theory closed. Adopts nothing.
