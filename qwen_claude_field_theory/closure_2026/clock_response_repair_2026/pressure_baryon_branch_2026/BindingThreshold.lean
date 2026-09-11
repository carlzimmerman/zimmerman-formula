import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-! Conditional algebra at the minimum lapse of a pressure-balanced initial
configuration. The maximum-principle/PDE and fluid chemical-frequency premises
are stated hypotheses. No complete static galaxy or gravity theory is claimed.
-/
namespace BindingThreshold
noncomputable section

theorem necessary_binding (l0 lb R N mb h : ℝ)
    (h0 : 0 < l0) (hb : 0 < lb) (hR : 0 ≤ R)
    (hm : 0 < mb) (hh : 0 < h)
    (hlapse : l0 ≤ N*(l0+lb*R))
    (hfluid : N*(mb+h) ≤ mb) : l0*h ≤ mb*lb*R := by
  have a := mul_le_mul_of_nonneg_right hlapse (add_pos hm hh).le
  have hp : 0 ≤ l0+lb*R := add_nonneg h0.le (mul_nonneg hb.le hR)
  have b := mul_le_mul_of_nonneg_right hfluid hp
  nlinarith only [a,b]

theorem polytrope_threshold (l0 lb mb lam r : ℝ) (hr : 0 < r)
    (h : l0*r^2 ≤ mb*lb*(lam/2*r^3*(9*r^2+5*mb))) :
    2*l0 ≤ mb*lb*lam*r*(9*r^2+5*mb) := by
  have hh : (2*l0)*r^2 ≤ (mb*lb*lam*r*(9*r^2+5*mb))*r^2 := by
    nlinarith only [h]
  exact le_of_mul_le_mul_right hh (sq_pos_of_pos hr)

theorem subcritical_exclusion (l0 lb R N mb h : ℝ)
    (h0 : 0 < l0) (hb : 0 < lb) (hR : 0 ≤ R)
    (hm : 0 < mb) (hh : 0 < h)
    (hlapse : l0 ≤ N*(l0+lb*R))
    (hfluid : N*(mb+h) ≤ mb)
    (hsmall : mb*lb*R < l0*h) : False := by
  exact (not_lt_of_ge (necessary_binding l0 lb R N mb h h0 hb hR hm hh hlapse hfluid)) hsmall

#print axioms necessary_binding
#print axioms polytrope_threshold
#print axioms subcritical_exclusion
end
end BindingThreshold
