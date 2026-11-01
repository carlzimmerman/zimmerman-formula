import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-! Scoped adapters for the positive isolated S law. These do not replace any
existing B-law certificate and make no empirical or field-equation claim. -/
namespace TP01LawDictionary

theorem simple_balance_iff {g gN a : ℝ} (hg : 0 < g) (ha : 0 < a) :
    gN = g ^ 2 / (g + a) ↔ g ^ 2 = gN * (g + a) := by
  have h : g + a ≠ 0 := by positivity
  rw [eq_div_iff h]
  constructor <;> intro heq <;> linarith

theorem simple_newton_excess {g gN a : ℝ} (hg : 0 < g) (ha : 0 < a)
    (law : g ^ 2 = gN * (g + a)) : 0 < g - gN ∧ g - gN < a := by
  have hsum : 0 < g + a := by positivity
  constructor
  · apply (mul_lt_mul_iff_right₀ hsum).mp
    nlinarith [mul_pos hg ha]
  · apply (mul_lt_mul_iff_right₀ hsum).mp
    nlinarith [sq_pos_of_pos ha]

theorem simple_scalar_efe_iff {x b e : ℝ} (hx : 0 < x) (he : 0 ≤ e) :
    x * ((x + e) / (1 + x + e)) = b ↔
      x ^ 2 + (e - b) * x - b * (1 + e) = 0 := by
  have hden : 1 + x + e ≠ 0 := by positivity
  rw [← mul_div_assoc, div_eq_iff hden]
  constructor <;> intro h <;> nlinarith

theorem distinct_exact_witness :
    (1 / 2 : ℝ) = 1 ^ 2 / (1 + 1) ∧
      (1 : ℝ) ^ 2 ≠ (1 / 2) ^ 2 + 1 * (1 / 2) := by norm_num

theorem ratio_square_bound (x : ℝ) :
    3 * (1 + x) ^ 2 ≤ 4 * (x ^ 2 + x + 1) := by
  nlinarith [sq_nonneg (x - 1)]

end TP01LawDictionary

#print axioms TP01LawDictionary.simple_balance_iff
#print axioms TP01LawDictionary.simple_newton_excess
#print axioms TP01LawDictionary.simple_scalar_efe_iff
#print axioms TP01LawDictionary.distinct_exact_witness
#print axioms TP01LawDictionary.ratio_square_bound
