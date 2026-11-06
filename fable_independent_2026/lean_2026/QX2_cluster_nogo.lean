import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# QX2 (2026-11-06): the algebra of the cluster no-go for v3s / AC2q statics

Lane closure_2026_11_06/QX2_clusters (criteria 2f84fed672). The numbers (X-COP, SPARC) come from qx2.py and are
not certified here. Certified: the logical steps that turn those numbers into the door label.

1. `law_mono`: the spherical law g(gN) = gN/2 + √(gN²/4 + a0 gN) is monotone in gN, so adding any non-negative
   source (clock, dust) to the baryons can only raise the model mass. The generous bounds in iterations 3 and 5 are
   upper bounds.
2. `universal_nu_gap`: for any single-valued ν, if log ν(y) lies within s of SPARC's binned value A, and X-COP needs
   B ≥ A + E at the same y, then the X-COP miss is at least E − s. With E = 0.30, s = 0.054 this is ≥ 0.246 > 0.05.
3. `stiffness_shift`: a relative change ε ≥ 0 of the phantom mass moves log M by at most ε (natural log), since
   log(1 + ε) ≤ ε.
4. `sum_le_of_pointwise`: a deeper potential gives more K(Q) dust in every Riemann sum (iteration 5's bound is
   generous).
5. `door_fail`: if the plain law misses by D ≥ 0.43 and the static terms move the mean by at most t1 + t2 + t3 with
   each ≤ 0.01, the remaining miss is > 0.05: the gate fails.
-/

namespace QX2

/-- The spherical AQUAL law, simple μ: g as a function of the Newtonian gN. -/
noncomputable def law (a0 gN : ℝ) : ℝ := gN / 2 + Real.sqrt (gN ^ 2 / 4 + a0 * gN)

theorem law_mono {a0 x y : ℝ} (ha : 0 ≤ a0) (hx : 0 ≤ x) (hxy : x ≤ y) : law a0 x ≤ law a0 y := by
  unfold law
  have h1 : x ^ 2 / 4 + a0 * x ≤ y ^ 2 / 4 + a0 * y := by nlinarith
  have h2 := Real.sqrt_le_sqrt h1
  linarith

theorem universal_nu_gap (L A B s E : ℝ) (hs : |L - A| ≤ s) (hB : A + E ≤ B) : E - s ≤ B - L := by
  have := (abs_le.mp hs).2
  linarith

theorem universal_nu_record (L A B : ℝ) (hs : |L - A| ≤ 0.054) (hB : A + 0.30 ≤ B) : 0.05 < B - L := by
  have := universal_nu_gap L A B 0.054 0.30 hs hB
  linarith

theorem stiffness_shift (ε : ℝ) (hε : 0 ≤ ε) : Real.log (1 + ε) ≤ ε := by
  have h := Real.log_le_sub_one_of_pos (by linarith : (0 : ℝ) < 1 + ε)
  linarith

theorem sum_le_of_pointwise {n : ℕ} (p q w : Fin n → ℝ) (hw : ∀ i, 0 ≤ w i) (hpq : ∀ i, p i ≤ q i) :
    ∑ i, p i * w i ≤ ∑ i, q i * w i :=
  Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_right (hpq i) (hw i)

/-- K(Q) dust mass scales as μ_K²: monotone in μ_K for a fixed non-negative integral. -/
theorem dust_mono_mu {I m1 m2 : ℝ} (hI : 0 ≤ I) (h0 : 0 ≤ m1) (h : m1 ≤ m2) : m1 ^ 2 * I ≤ m2 ^ 2 * I := by
  have : m1 ^ 2 ≤ m2 ^ 2 := by nlinarith
  exact mul_le_mul_of_nonneg_right this hI

theorem door_fail (D t1 t2 t3 : ℝ) (hD : 0.43 ≤ D) (h1 : t1 ≤ 0.01) (h2 : t2 ≤ 0.01) (h3 : t3 ≤ 0.01) :
    0.05 < D - (t1 + t2 + t3) := by
  linarith

end QX2

#print axioms QX2.law_mono
#print axioms QX2.universal_nu_gap
#print axioms QX2.universal_nu_record
#print axioms QX2.stiffness_shift
#print axioms QX2.sum_le_of_pointwise
#print axioms QX2.dust_mono_mu
#print axioms QX2.door_fail
