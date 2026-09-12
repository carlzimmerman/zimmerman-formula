import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/- Exact coefficient/sign implications only. The physical action-to-coefficient
   derivation is in audit_health.py and REPORT.md, not formalized here. -/
namespace ClosureFrontHealth

theorem canonical_coefficient_factor (U d ell : ℝ)
    (hU : U ≠ 0) (hell : ell ≠ 0) :
    d / ell - 4*d^2/U = d*(U-4*d*ell)/(U*ell) := by
  field_simp
  <;> ring

theorem canonical_coefficient_positive (U d ell : ℝ)
    (hU : 0 < U) (hd : 0 < d) (hell : 0 < ell)
    (h : 4*d*ell < U) : 0 < d / ell - 4*d^2/U := by
  rw [canonical_coefficient_factor U d ell (ne_of_gt hU) (ne_of_gt hell)]
  exact div_pos (mul_pos hd (sub_pos.mpr h)) (mul_pos hU hell)

theorem l205_purported_healthy_counterexample :
    (4*(1:ℝ)*1 > 1) ∧ ((1:ℝ)/1-4*1^2/1 < 0) := by
  norm_num

#print axioms canonical_coefficient_factor
#print axioms canonical_coefficient_positive
#print axioms l205_purported_healthy_counterexample
end ClosureFrontHealth
