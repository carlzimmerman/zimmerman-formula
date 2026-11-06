/- QX12 MUTATE twin: three false claims that must fail. kappa = 1/2 FITTED; not theory closed. -/
import Mathlib

namespace QX12M

/-- FALSE: the inverse without the + a0 in the denominator. -/
theorem law_inverse_bad {g a0 : ℝ} (hg : 0 < g) (ha : 0 < a0) :
    g ^ 2 / g / 2 + Real.sqrt ((g ^ 2 / g) ^ 2 / 4 + a0 * (g ^ 2 / g)) = g := by
  sorry

/-- FALSE: a deeper point holds less (order reversed). -/
theorem baro_order_bad {h : ℝ → ℝ} (hh : StrictMono h) {ρ₁ ρ₂ c D₁ D₂ : ℝ}
    (e1 : h ρ₁ = c + D₁) (e2 : h ρ₂ = c + D₂) (hD : D₁ ≤ D₂) : ρ₂ ≤ ρ₁ := by
  by_contra hc
  push_neg at hc
  linarith

/-- FALSE: larger sound speed holds more. -/
theorem iso_ratio_bad {c₁ c₂ D : ℝ} (h1 : 0 < c₁) (h12 : c₁ ≤ c₂) (hD : 0 ≤ D) :
    Real.exp (D / c₁) ≤ Real.exp (D / c₂) := by
  apply Real.exp_le_exp.mpr
  exact div_le_div_of_nonneg_left hD h1 h12

end QX12M

#print axioms QX12M.law_inverse_bad
#print axioms QX12M.baro_order_bad
#print axioms QX12M.iso_ratio_bad
