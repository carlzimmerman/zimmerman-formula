import Mathlib

/-! Conditional sharp-edge power certificate; no physical bath is assumed.
The declared coefficient K represents a positive lower bound of C*D*T/2
when n=C*T*q^(-1/2). This file certifies the ideal mathematical integrand
only, not continuity/positivity of a physical D*T or stochastic dynamics. -/
noncomputable section
open MeasureTheory Set
namespace FrameworkEdgePower

def integrand (K q : ℝ) : ℝ := K / (q * Real.sqrt q)
def primitive (K q : ℝ) : ℝ := -2 * K / Real.sqrt q
def truncatedPower (K ε Q : ℝ) : ℝ := K * (2 / Real.sqrt ε - 2 / Real.sqrt Q)

theorem integrand_rpow (K q : ℝ) (hq : 0 < q) :
    integrand K q = K * q ^ (-3 / 2 : ℝ) := by
  have he : (-3 / 2 : ℝ) = -1 + -(1 / 2) := by norm_num
  rw [he, Real.rpow_add hq, Real.rpow_neg_one,
    Real.rpow_neg hq.le, ← Real.sqrt_eq_rpow]
  unfold integrand
  ring

theorem primitive_derivative (K q : ℝ) (hq : 0 < q) :
    HasDerivAt (primitive K) (integrand K q) q := by
  have hs : Real.sqrt q ≠ 0 := (Real.sqrt_pos.mpr hq).ne'
  have h := (hasDerivAt_const q (-2 * K)).div (Real.hasDerivAt_sqrt hq.ne') hs
  change HasDerivAt (primitive K) _ q at h
  apply h.congr_deriv
  dsimp [integrand]
  field_simp
  rw [Real.sq_sqrt hq.le]
  ring

theorem integral_exact (K ε Q : ℝ) (hε : 0 < ε) (hεQ : ε ≤ Q) :
    (∫ q in ε..Q, integrand K q) = truncatedPower K ε Q := by
  have hpos : ∀ q ∈ Set.uIcc ε Q, 0 < q := by
    rw [Set.uIcc_of_le hεQ]
    intro q hq
    exact lt_of_lt_of_le hε hq.1
  have hcont : ContinuousOn (integrand K) (Set.uIcc ε Q) := by
    apply continuousOn_const.div
      (continuousOn_id.mul Real.continuous_sqrt.continuousOn)
    intro q hq
    exact mul_ne_zero (hpos q hq).ne' (Real.sqrt_pos.mpr (hpos q hq)).ne'
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun q hq => primitive_derivative K q (hpos q hq)) hcont.intervalIntegrable
  rw [h]
  unfold primitive truncatedPower
  ring

/-- Every finite cap is exceeded by a genuine positive truncated interval integral. -/
theorem integral_unbounded (K Q cap : ℝ) (hK : 0 < K) (hQ : 0 < Q) :
    ∃ ε : ℝ, 0 < ε ∧ ε < Q ∧ cap < ∫ q in ε..Q, integrand K q := by
  let d : ℝ := max cap 0 + 2 * K / Real.sqrt Q + 1
  let s : ℝ := 2 * K / d
  have hsQ : 0 < Real.sqrt Q := Real.sqrt_pos.mpr hQ
  have hm : 0 ≤ max cap 0 := le_max_right cap 0
  have hd : 0 < d := by dsimp [d]; positivity
  have hs : 0 < s := by dsimp [s]; positivity
  have hsd : s * d = 2 * K := by dsimp [s]; field_simp
  have hlt : s < Real.sqrt Q := by
    apply (div_lt_iff₀ hd).mpr
    dsimp [d]
    have he : (2 * K / Real.sqrt Q) * Real.sqrt Q = 2 * K := by field_simp
    nlinarith
  have hsqQ : s ^ 2 < Q := by
    nlinarith [Real.sq_sqrt hQ.le]
  refine ⟨s ^ 2, pow_pos hs 2, hsqQ, ?_⟩
  rw [integral_exact K (s ^ 2) Q (pow_pos hs 2) hsqQ.le]
  unfold truncatedPower
  rw [Real.sqrt_sq hs.le]
  have he : K * (2 / s - 2 / Real.sqrt Q) = max cap 0 + 1 := by
    have hkd : 2 * K / s = d := by
      apply (div_eq_iff hs.ne').mpr
      nlinarith [hsd]
    calc
      K * (2 / s - 2 / Real.sqrt Q) = 2 * K / s - 2 * K / Real.sqrt Q := by ring
      _ = d - 2 * K / Real.sqrt Q := by rw [hkd]
      _ = max cap 0 + 1 := by dsimp [d]; ring
  rw [he]
  have := le_max_left cap 0
  linarith

/-- A supplied pointwise positive singular lower bound transfers the obstruction
 to any integrable power density. Neither lower bound nor integrability is derived
 from a bath here; both are explicit mathematical hypotheses. -/
theorem lower_bound_integral_unbounded (f : ℝ → ℝ) (K Q cap : ℝ)
    (hK : 0 < K) (hQ : 0 < Q)
    (hint : ∀ ε : ℝ, 0 < ε → ε < Q → IntervalIntegrable f volume ε Q)
    (hbound : ∀ q : ℝ, 0 < q → q ≤ Q → integrand K q ≤ f q) :
    ∃ ε : ℝ, 0 < ε ∧ ε < Q ∧ cap < ∫ q in ε..Q, f q := by
  obtain ⟨ε, hε, hεQ, hcap⟩ := integral_unbounded K Q cap hK hQ
  have hpos : ∀ q ∈ Set.uIcc ε Q, 0 < q := by
    rw [Set.uIcc_of_le hεQ.le]
    intro q hq
    exact lt_of_lt_of_le hε hq.1
  have hcont : ContinuousOn (integrand K) (Set.uIcc ε Q) := by
    apply continuousOn_const.div
      (continuousOn_id.mul Real.continuous_sqrt.continuousOn)
    intro q hq
    exact mul_ne_zero (hpos q hq).ne' (Real.sqrt_pos.mpr (hpos q hq)).ne'
  have hmono := intervalIntegral.integral_mono_on hεQ.le hcont.intervalIntegrable
    (hint ε hε hεQ) (fun q hq => hbound q (lt_of_lt_of_le hε hq.1) hq.2)
  exact ⟨ε, hε, hεQ, lt_of_lt_of_le hcap hmono⟩

end FrameworkEdgePower
#print axioms FrameworkEdgePower.integrand_rpow
#print axioms FrameworkEdgePower.primitive_derivative
#print axioms FrameworkEdgePower.integral_exact
#print axioms FrameworkEdgePower.integral_unbounded

#print axioms FrameworkEdgePower.lower_bound_integral_unbounded
