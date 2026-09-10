import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/- Conditional real-algebra certificates. SymPy separately derives the ADM
quadratic action. These theorems do not formalize the action variation or prove
empirical viability, nonlinear health, PPN, or complete gravity. -/
namespace ClockResponseRepair

noncomputable def eps (m r : ℝ) : ℝ := (1 + r * (m - 1)) / (1 + m - r)

theorem denominator_positive (m r : ℝ) (hm : 0 < m) (hr : r ≤ 1) :
    0 < 1 + m - r := by linarith

theorem repaired_gradient (m r : ℝ) (hm : 0 < m) (hr : r ≤ 1) :
    (m - 1 + eps m r) * (1 + m - r) = m^2 := by
  have hn : 1 + m - r ≠ 0 := ne_of_gt (denominator_positive m r hm hr)
  unfold eps
  field_simp
  ring

theorem clock_gradient_positive (m r : ℝ) (hm : 0 < m) (hr : r ≤ 1) :
    0 < m - 1 + eps m r := by
  have hd := denominator_positive m r hm hr
  have hi := repaired_gradient m r hm hr
  have hs : 0 < m^2 := sq_pos_of_pos hm
  nlinarith

theorem exact_response (m r : ℝ) (hm : 0 < m) (hr : r ≤ 1) :
    (eps m r * (m + 1) - 1) / (m - 1 + eps m r) = r := by
  have hd : 1 + m - r ≠ 0 := ne_of_gt (denominator_positive m r hm hr)
  have hg : m - 1 + eps m r ≠ 0 := ne_of_gt (clock_gradient_positive m r hm hr)
  apply (div_eq_iff hg).2
  unfold eps
  field_simp
  ring

theorem kinetic_positive (B f e k D H : ℝ)
    (hB : 0 < B) (hf : 0 < f) (he : e < 0)
    (hk : 0 ≤ k) (hD : 0 < D) (hH : H ≠ 0) :
    0 < B - f^2 / (e*f - k*D/H^2) := by
  have hh : 0 < H^2 := sq_pos_of_ne_zero hH
  have hx : 0 ≤ k*D/H^2 := div_nonneg (mul_nonneg hk (le_of_lt hD)) (le_of_lt hh)
  have hn : e*f - k*D/H^2 < 0 := by nlinarith
  have hf2 : 0 < f^2 := sq_pos_of_pos hf
  have hquot : f^2 / (e*f - k*D/H^2) < 0 := div_neg_of_pos_of_neg hf2 hn
  linarith

#print axioms denominator_positive
#print axioms repaired_gradient
#print axioms clock_gradient_positive
#print axioms exact_response
#print axioms kinetic_positive
end ClockResponseRepair
