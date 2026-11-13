import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! Exact order/positive-quadrature/algebraic mass-floor kernels.
No continuous deflection integral, FLRW model, observed mass prior, numerical
quadrature accuracy or full physical action is certified by this file. -/

namespace RedshiftBounds

noncomputable def force (a n : ℝ) : ℝ := (n + Real.sqrt (n^2+4*a*n))/2

theorem force_mono {a n m : ℝ} (ha : 0 ≤ a) (hn : 0 ≤ n) (h : n ≤ m) :
    force a n ≤ force a m := by
  have hm : 0 ≤ m := hn.trans h
  have hp : 0 ≤ (m-n)*(m+n+4*a) := by positivity
  have hr : n^2+4*a*n ≤ m^2+4*a*m := by nlinarith [hp]
  have hs := Real.sqrt_le_sqrt hr
  unfold force
  linarith

/-- A closed Newton-plus-deep upper envelope for the exact simple-mu root. -/
theorem force_upper {a n : ℝ} (ha : 0 ≤ a) (hn : 0 ≤ n) :
    force a n ≤ n + Real.sqrt (a*n) := by
  have hs : 0 ≤ Real.sqrt (a*n) := Real.sqrt_nonneg _
  have hs2 : (Real.sqrt (a*n))^2 = a*n := Real.sq_sqrt (mul_nonneg ha hn)
  have hp : 0 ≤ n*Real.sqrt (a*n) := mul_nonneg hn hs
  have harg : n^2+4*a*n ≤ (n+2*Real.sqrt (a*n))^2 := by nlinarith [hp,hs2]
  have hroot := Real.sqrt_le_sqrt harg
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by positivity)] at hroot
  unfold force
  linarith

/-- Enclosed-mass domination survives any fixed nonnegative quadrature weights.
    Radii are strictly positive, as for a ray with positive impact parameter. -/
theorem spherical_positive_weight_envelope
    {I : Type*} [Fintype I] (a G M : ℝ) (mass radius weight : I → ℝ)
    (ha : 0 ≤ a) (hG : 0 ≤ G) (_hM : 0 ≤ M)
    (hm : ∀ i, 0 ≤ mass i) (hbound : ∀ i, mass i ≤ M)
    (hr : ∀ i, 0 < radius i) (hw : ∀ i, 0 ≤ weight i) :
    (∑ i, weight i * force a (G*mass i/(radius i)^2)) ≤
      ∑ i, weight i * force a (G*M/(radius i)^2) := by
  apply Finset.sum_le_sum
  intro i hi
  have hd : 0 < (radius i)^2 := sq_pos_of_pos (hr i)
  have hn : 0 ≤ G*mass i/(radius i)^2 :=
    div_nonneg (mul_nonneg hG (hm i)) (le_of_lt hd)
  have hc : G*mass i/(radius i)^2 ≤ G*M/(radius i)^2 :=
    div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left (hbound i) hG) (le_of_lt hd)
  exact mul_le_mul_of_nonneg_left (force_mono ha hn hc) (hw i)

noncomputable def massRoot (A B target : ℝ) : ℝ :=
  (Real.sqrt (B^2+4*A*target)-B)/(2*A)

theorem massRoot_nonnegative {A B target : ℝ}
    (hA : 0 < A) (hB : 0 ≤ B) (ht : 0 ≤ target) :
    0 ≤ massRoot A B target := by
  have hr : B^2 ≤ B^2+4*A*target := by
    nlinarith [mul_nonneg (le_of_lt hA) ht]
  have hs := Real.sqrt_le_sqrt hr
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg hB] at hs
  unfold massRoot
  exact div_nonneg (sub_nonneg.mpr hs) (by positivity)

theorem massRoot_le_of_capacity {A B target t : ℝ}
    (hA : 0 < A) (hB : 0 ≤ B) (ht : 0 ≤ t)
    (h : target ≤ A*t^2+B*t) :
    massRoot A B target ≤ t := by
  have hc := mul_le_mul_of_nonneg_left h (show 0 ≤ 4*A by positivity)
  have hr : B^2+4*A*target ≤ (2*A*t+B)^2 := by nlinarith [hc]
  have hs := Real.sqrt_le_sqrt hr
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by positivity)] at hs
  unfold massRoot
  apply (div_le_iff₀ (show 0 < 2*A by positivity)).mpr
  nlinarith

/-- If geometry and the deflection capacity have the stated upper bounds,
    the closed algebraic necessary mass floor follows. The continuous
    deflection capacity is an explicit hypothesis, not a hidden Lean claim. -/
theorem source_independent_mass_floor {A B M theta beta betaMax alpha : ℝ}
    (hA : 0 < A) (hB : 0 ≤ B) (hM : 0 ≤ M) (htheta : 0 ≤ theta)
    (hmax : 0 < betaMax) (hbeta : beta ≤ betaMax) (halpha : 0 ≤ alpha)
    (hlens : theta ≤ beta*alpha)
    (hcapacity : alpha ≤ A*M+B*Real.sqrt M) :
    (massRoot A B (theta/betaMax))^2 ≤ M := by
  have hc : theta ≤ betaMax*(A*M+B*Real.sqrt M) := calc
    theta ≤ beta*alpha := hlens
    _ ≤ betaMax*alpha := mul_le_mul_of_nonneg_right hbeta halpha
    _ ≤ betaMax*(A*M+B*Real.sqrt M) :=
      mul_le_mul_of_nonneg_left hcapacity (le_of_lt hmax)
  have htarget : theta/betaMax ≤ A*M+B*Real.sqrt M := by
    apply (div_le_iff₀ hmax).mpr
    nlinarith [hc]
  have hs : 0 ≤ Real.sqrt M := Real.sqrt_nonneg M
  have hs2 : (Real.sqrt M)^2 = M := Real.sq_sqrt hM
  have hroot : massRoot A B (theta/betaMax) ≤ Real.sqrt M := by
    apply massRoot_le_of_capacity hA hB hs
    simpa only [hs2] using htarget
  have hroot0 : 0 ≤ massRoot A B (theta/betaMax) :=
    massRoot_nonnegative hA hB (div_nonneg htheta (le_of_lt hmax))
  have hp := mul_nonneg (sub_nonneg.mpr hroot) (add_nonneg hs hroot0)
  nlinarith [hp,hs2]

end RedshiftBounds

#print axioms RedshiftBounds.force_mono
#print axioms RedshiftBounds.force_upper
#print axioms RedshiftBounds.spherical_positive_weight_envelope
#print axioms RedshiftBounds.massRoot_nonnegative
#print axioms RedshiftBounds.massRoot_le_of_capacity
#print axioms RedshiftBounds.source_independent_mass_floor
