/-
FINAL-18 (KAPPA_B) MUTATE: the same statements with one sign, one factor or one root changed.
Every theorem below is FALSE and must be REJECTED by the elaborator: this file must exit 1.
The three mutations are the three ways the lane's conclusion could be manufactured:

  M-a  "the law force cancels the excess exactly"        -> drops the u^2/(a_0-u) remainder, which is
                                                            the only a_0-dependence of the fold.
  M-b  "the remainder is first order in the excess"      -> overstates the fold's a_0-sensitivity.
  M-c  "the share root is the negative branch"           -> flips the branch of the quadratic.
  M-d  "the share decreases with a_0"                    -> would make (M) a flat direction.
  M-e  "(M) inverts to x^2 = q^2"                        -> drops the (1+q), the shallow-regime term.
  M-f  "the matching condition has two solutions"        -> would leave kappa free.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace FINAL18M

/-- M-a: FALSE. The law force is not exactly u; the remainder u^2/(a_0-u) is what carries a_0. -/
theorem law_force_is_exactly_u (a0 u : ℝ) (hd : a0 - u ≠ 0) : a0 * u / (a0 - u) = u := by
  field_simp [hd]
  ring

/-- M-b: FALSE. The remainder is second order in the excess, not first. -/
theorem residual_is_linear (a0 u : ℝ) (hd : a0 - u ≠ 0) : a0 * u / (a0 - u) - u = u := by
  field_simp [hd]
  ring

/-- M-c: FALSE. The non-negative root is the positive branch. -/
theorem share_negative_root (X : ℝ) (hX : 0 ≤ X) :
    (-1 - Real.sqrt (1 + 4 * (X * (X + 1)))) / 2 = X := by
  have h : 1 + 4 * (X * (X + 1)) = (2 * X + 1) ^ 2 := by ring
  rw [h, Real.sqrt_sq (by linarith)]
  ring

/-- M-d: FALSE. The share rises with a_0; the opposite sign would make kappa a flat direction. -/
theorem share_antitone (k0 k1 : ℝ) (h0 : 0 ≤ k0) (h01 : k0 < k1) :
    (-1 + Real.sqrt (1 + 4 * k1)) / 2 < (-1 + Real.sqrt (1 + 4 * k0)) / 2 := by
  have hs : Real.sqrt (1 + 4 * k0) < Real.sqrt (1 + 4 * k1) := Real.sqrt_lt_sqrt (by linarith)
  linarith

/-- M-e: FALSE. (M) inverts to x^2 = q(1+q); the (1+q) is the shallow-regime term, not decoration. -/
theorem fold_match_solves_wrong (q x : ℝ) (h : (-1 + Real.sqrt (1 + 4 * x ^ 2)) / 2 = q) :
    x ^ 2 = q ^ 2 := by
  have h0 : 0 ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
  set s := Real.sqrt (1 + 4 * x ^ 2) with hs
  have hs2 : s ^ 2 = 1 + 4 * x ^ 2 := by
    rw [hs, Real.sq_sqrt h0]
  nlinarith

/-- M-f: FALSE. There is one solution, not two; the second "branch" is negative. -/
theorem fold_match_two_roots (q : ℝ) (hq : 0 ≤ q) :
    (-1 + Real.sqrt (1 + 4 * (q * (q + 1)))) / 2 = q + 1 := by
  have h : 1 + 4 * (q * (q + 1)) = (2 * q + 1) ^ 2 := by ring
  rw [h, Real.sqrt_sq (by linarith)]
  ring

end FINAL18M
