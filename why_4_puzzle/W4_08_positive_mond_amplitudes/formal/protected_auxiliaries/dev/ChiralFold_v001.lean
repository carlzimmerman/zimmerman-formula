module

public import Mathlib.Algebra.Order.Field.Basic
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Ring.Basic
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.NormNum

@[expose] public section

/-!
Exact algebra for the normalized chiral auxiliary cubic.

The cubic equation and kinetic coefficient are explicit inputs. These results
do not establish a component-action dictionary, a physical background, a
microscopic state, or an operational MOND amplitude. The optional ratio is
only a ratio of local Taylor coefficients and is named accordingly.
-/

namespace Why4.ChiralFold

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def cubic (x y : K) : K := y ^ 3 - 3 * (1 + x) * y + 2

def chiTimeCoefficient (g x y : K) : K := g * (1 + x - y ^ 2 / 3)

theorem zero_gradient_factorization (y : K) :
    cubic 0 y = (y - 1) ^ 2 * (y + 2) := by
  unfold cubic
  ring1

theorem exact_fold_expansion (x t : K) :
    cubic x (1 + t) = t ^ 2 * (3 + t) - 3 * x * (1 + t) := by
  unfold cubic
  ring1

theorem timelike_root_square_gt_three
    (x y : K) (hxlo : -(1 / 4 : K) < x) (hxhi : x < 0)
    (hroot : cubic x y = 0) : 3 < y ^ 2 := by
  have hfactor : cubic x y = (y - 1) ^ 2 * (y + 2) - 3 * x * y := by
    unfold cubic
    ring1
  by_cases hy : 0 ≤ y
  · have hprod : 0 ≤ (y - 1) ^ 2 * (y + 2) :=
      mul_nonneg (sq_nonneg (y - 1)) (by linarith)
    have hpos : 0 < (y - 1) ^ 2 * (y + 2) - 3 * x * y := by
      by_cases hyzero : y = 0
      · subst y
        norm_num
      · have hyp : 0 < y := lt_of_le_of_ne hy (Ne.symm hyzero)
        have hxy : x * y < 0 := mul_neg_of_neg_of_pos hxhi hyp
        nlinarith
    rw [← hfactor, hroot] at hpos
    exact False.elim ((lt_irrefl (0 : K)) hpos)
  · have hyneg : y < 0 := lt_of_not_ge hy
    by_contra hsquare
    have hsq : y ^ 2 ≤ 3 := le_of_not_gt hsquare
    have hym2 : -(2 : K) ≤ y := by
      nlinarith [sq_nonneg (y + 2)]
    have hcube : 3 * y ≤ y ^ 3 := by
      have hprod : 0 ≤ (3 - y ^ 2) * (-y) :=
        mul_nonneg (by linarith) (le_of_lt (neg_pos.mpr hyneg))
      nlinarith
    have hxy : x * y ≤ -y / 4 := by
      have hprod : 0 ≤ (x + 1 / 4) * (-y) :=
        mul_nonneg (by linarith) (le_of_lt (neg_pos.mpr hyneg))
      nlinarith
    have hbound : (1 / 2 : K) ≤ cubic x y := by
      unfold cubic
      nlinarith
    rw [hroot] at hbound
    norm_num at hbound

theorem timelike_chi_coefficient_negative
    (g x y : K) (hg : 0 < g)
    (hxlo : -(1 / 4 : K) < x) (hxhi : x < 0)
    (hroot : cubic x y = 0) : chiTimeCoefficient g x y < 0 := by
  have hsq : 3 < y ^ 2 := timelike_root_square_gt_three x y hxlo hxhi hroot
  unfold chiTimeCoefficient
  exact mul_neg_of_pos_of_neg hg (by nlinarith)

theorem timelike_base_coefficient_negative
    (g x y : K) (hg : 0 < g)
    (hxlo : -(1 / 4 : K) < x) (hxhi : x < 0)
    (hroot : cubic x y = 0) : g * (1 - y ^ 2 / 3) < 0 := by
  have hsq : 3 < y ^ 2 := timelike_root_square_gt_three x y hxlo hxhi hroot
  exact mul_neg_of_pos_of_neg hg (by nlinarith)

theorem nominal_local_taylor_ratio
    (g tau : K) (hg : g ≠ 0) (htau : tau ≠ 0) :
    (g ^ 2 / (12 * tau)) * (4 * tau * g / 81) / (g / 3) ^ 3 = 1 / 9 := by
  field_simp [hg, htau]
  ring1

#check @zero_gradient_factorization
#check @exact_fold_expansion
#check @timelike_root_square_gt_three
#check @timelike_chi_coefficient_negative
#check @timelike_base_coefficient_negative
#check @nominal_local_taylor_ratio
#print axioms zero_gradient_factorization
#print axioms exact_fold_expansion
#print axioms timelike_root_square_gt_three
#print axioms timelike_chi_coefficient_negative
#print axioms timelike_base_coefficient_negative
#print axioms nominal_local_taylor_ratio

end Why4.ChiralFold
