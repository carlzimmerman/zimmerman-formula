/-
EMV1 MUTATE twin: false versions of five EMV1 statements, with the proofs that close the true ones. This file must FAIL to compile.
  homog_M        : (m - 1) / (m + 2) <= -1/2 on 0 <= m <= 1 (the insulating limit claimed for every m)
  alpha_inc_M    : alpha_inc = -1 / (2 + 6 x) (the x^2 term dropped)
  hasDerivAt_M   : de/dx = (3 x^2 + 6 x + 2) / (3 (1 + x)) (wrong power of 1 + x)
  alpha_order_M  : alpha_inc < alpha_tot (the order reversed)
  allowance_M    : the allowance is at most SWT1's q / (3/2 + q)
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EMV1M

noncomputable def eOf (x : ℝ) : ℝ := x * (3 * x + 2) / (3 * (1 + x))

theorem homog_M (m : ℝ) (h0 : 0 ≤ m) (h1 : m ≤ 1) : (m - 1) / (m + 2) ≤ -(1 / 2 : ℝ) := by
  have h : 0 < m + 2 := by linarith
  rw [div_le_iff₀ h]; linarith

theorem alpha_inc_M (x : ℝ) (hx : 0 < x) :
    1 - 1 / ((3 * x ^ 2 + 6 * x + 2) / (3 * (1 + x) ^ 2)) = -1 / (2 + 6 * x) := by
  have h1 : (3 * x ^ 2 + 6 * x + 2) ≠ 0 := by positivity
  have h2 : (1 + x) ≠ 0 := by positivity
  have h3 : (2 + 6 * x) ≠ 0 := by positivity
  field_simp
  ring

theorem hasDerivAt_M (x : ℝ) (hx : 0 < x) :
    HasDerivAt eOf ((3 * x ^ 2 + 6 * x + 2) / (3 * (1 + x))) x := by
  have hn : HasDerivAt (fun y : ℝ => y * (3 * y + 2)) (1 * (3 * x + 2) + x * (3 * 1)) x :=
    (hasDerivAt_id' x).mul (((hasDerivAt_id' x).const_mul 3).add_const 2)
  have hd : HasDerivAt (fun y : ℝ => 3 * (1 + y)) (3 * 1) x :=
    ((hasDerivAt_id' x).const_add 1).const_mul 3
  have hne : 3 * (1 + x) ≠ 0 := by positivity
  have key : ((1 * (3 * x + 2) + x * (3 * 1)) * (3 * (1 + x)) - x * (3 * x + 2) * (3 * 1)) / (3 * (1 + x)) ^ 2
      = (3 * x ^ 2 + 6 * x + 2) / (3 * (1 + x)) := by
    rw [div_eq_div_iff (by positivity) (by positivity)]; ring
  exact (hn.div hd hne).congr_deriv key

theorem alpha_order_M (x : ℝ) (hx : 0 < x) : -1 / (3 * x ^ 2 + 6 * x + 2) < -1 / (2 + 3 * x) := by
  have h1 : 0 < 2 + 3 * x := by linarith
  have h2 : 0 < 3 * x ^ 2 + 6 * x + 2 := by positivity
  rw [div_lt_div_iff₀ h2 h1]; nlinarith

theorem allowance_M (α q : ℝ) (hα1 : -(1 / 2) ≤ α) (hα0 : α < 0) (hq : 0 < q) :
    q / (-α * (3 + 2 * q)) ≤ q / (3 / 2 + q) := by
  have h0 : 0 < 3 / 2 + q := by linarith
  have h1 : 0 < -α * (3 + 2 * q) := by nlinarith
  rw [div_le_div_iff₀ h1 h0]
  nlinarith

end EMV1M

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
