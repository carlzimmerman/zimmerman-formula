/-
HIS1 MUTATE twin: false versions of the statements in HIS1.lean. This file must FAIL to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace HIS1_MUTATE

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

-- false: Newton above the law
theorem XL_neg (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a < 0 := by
  unfold XL
  have h4 : 0 < 4 * a / gb := by positivity
  have hlt : (1 : ℝ) < 1 + 4 * a / gb := by linarith
  have h := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) hlt
  rw [Real.sqrt_one] at h
  linarith

-- false: the reverse bound
theorem XL_ge (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : Real.sqrt (a / gb) < XL gb a := by
  unfold XL
  have ht : 0 ≤ a / gb := by positivity
  set u := Real.sqrt (a / gb) with hu
  have hu0 : 0 ≤ u := Real.sqrt_nonneg _
  have hu2 : u ^ 2 = a / gb := by rw [hu]; exact Real.sq_sqrt ht
  have h4 : 1 + 4 * a / gb = 1 + 4 * u ^ 2 := by rw [hu2]; ring
  have hs : Real.sqrt (1 + 4 * a / gb) ≤ 1 + 2 * u := by
    rw [h4, Real.sqrt_le_left (by positivity)]; nlinarith
  linarith

-- false: the order reversed
theorem between_false (X XLv : ℝ) (h0 : 0 ≤ X) (h1 : X < XLv) : Real.log (1 + XLv) ≤ Real.log (1 + X) := by
  exact Real.log_le_log (by linarith) (by linarith)

end HIS1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
