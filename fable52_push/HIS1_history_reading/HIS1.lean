/-
HIS1 (criteria 152ecaf5c4): Lean statements for the closed forms the history tests use. They certify the algebra, not
the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  XL_pos        X_L(g_bar; a0) > 0: Newton (X = 0) lies strictly below the law at every g_bar
  newton_below  log(1) < log(1 + X_L): the Newtonian offset under the law is negative
  XL_le         X_L <= sqrt(a0 / g_bar)
  between       0 <= X <= X_L gives 0 <= log(1 + X) <= log(1 + X_L): a system between Newton and the law reads between them
-/
import Mathlib

namespace HIS1

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

theorem XL_pos (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : 0 < XL gb a := by
  unfold XL
  have h4 : 0 < 4 * a / gb := by positivity
  have hlt : (1 : ℝ) < 1 + 4 * a / gb := by linarith
  have h := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) hlt
  rw [Real.sqrt_one] at h
  linarith

theorem newton_below (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : Real.log 1 < Real.log (1 + XL gb a) := by
  have := XL_pos gb a hgb ha
  exact Real.log_lt_log (by norm_num) (by linarith)

theorem XL_le (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a ≤ Real.sqrt (a / gb) := by
  unfold XL
  have ht : 0 ≤ a / gb := by positivity
  set u := Real.sqrt (a / gb) with hu
  have hu0 : 0 ≤ u := Real.sqrt_nonneg _
  have hu2 : u ^ 2 = a / gb := by rw [hu]; exact Real.sq_sqrt ht
  have h4 : 1 + 4 * a / gb = 1 + 4 * u ^ 2 := by rw [hu2]; ring
  have hs : Real.sqrt (1 + 4 * a / gb) ≤ 1 + 2 * u := by
    rw [h4, Real.sqrt_le_left (by positivity)]; nlinarith
  linarith

theorem between (X XLv : ℝ) (h0 : 0 ≤ X) (h1 : X ≤ XLv) :
    0 ≤ Real.log (1 + X) ∧ Real.log (1 + X) ≤ Real.log (1 + XLv) := by
  constructor
  · exact Real.log_nonneg (by linarith)
  · exact Real.log_le_log (by linarith) (by linarith)

end HIS1

#print axioms HIS1.XL_pos
#print axioms HIS1.newton_below
#print axioms HIS1.XL_le
#print axioms HIS1.between

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
