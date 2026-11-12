/-
SS1 (self-shielded late conversion): Lean statements for the reduced peeling reading.
FROZEN_CRITERIA.md b5adc7a90b section 8. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

The reduced peeling ODE dx/dtau = -x/(1+x^2) from x(0) = x0 has the exact first integral
  log f + x0^2 (f^2 - 1) / 2 = -tau,   f = x(tau)/x0 the retained fraction.
Everything below is stated about any f in (0, 1] satisfying that relation (the ODE itself is not formalised here).
  * peel_ge_bare      : f >= exp(-tau)                  (no system drains faster than the bare rate)
  * peel_le_frozen    : f <= exp(-tau / (1 + x0^2))      (the frozen-Damkohler formula over-states retention:
                                                          the column drops as the component drains)
  * thm2_corrected    : at x0 = 3.2, tau = 4.49:  1/2 < f < 0.615   (the outside text's ">= 0.615" is false;
                                                          the solution is 0.506)
  * thm4_corrected    : Gamma0 / Gamma_psi = (0.820 / Gyr) / (4.20 / Myr) = 1.952e-4 (not 0.032)
-/
import Mathlib

namespace SS1

open Real

/-- No system drains faster than the bare rate. -/
theorem peel_ge_bare (x0 τ f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1)
    (h : Real.log f + x0 ^ 2 * (f ^ 2 - 1) / 2 = -τ) : Real.exp (-τ) ≤ f := by
  have hsq : f ^ 2 ≤ 1 := by nlinarith
  have hlog : -τ ≤ Real.log f := by nlinarith [sq_nonneg x0]
  calc Real.exp (-τ) ≤ Real.exp (Real.log f) := Real.exp_le_exp.mpr hlog
    _ = f := Real.exp_log hf0

/-- Self-consistent peeling retains no more than the frozen-Damkohler formula. -/
theorem peel_le_frozen (x0 τ f : ℝ) (hf0 : 0 < f)
    (h : Real.log f + x0 ^ 2 * (f ^ 2 - 1) / 2 = -τ) : f ≤ Real.exp (-τ / (1 + x0 ^ 2)) := by
  have hl : Real.log f ≤ f - 1 := Real.log_le_sub_one_of_pos hf0
  have key : Real.log f ≤ (f ^ 2 - 1) / 2 := by nlinarith [sq_nonneg (1 - f)]
  have hpos : (0 : ℝ) < 1 + x0 ^ 2 := by positivity
  have hle : Real.log f ≤ -τ / (1 + x0 ^ 2) := by
    rw [le_div_iff₀ hpos]
    nlinarith [mul_nonneg (sq_nonneg x0) (sub_nonneg.2 key)]
  calc f = Real.exp (Real.log f) := (Real.exp_log hf0).symm
    _ ≤ Real.exp (-τ / (1 + x0 ^ 2)) := Real.exp_le_exp.mpr hle

/-- The outside text's Theorem 2 bound (retention >= 0.615 at x0 = 3.2) is false; the true value lies in (1/2, 0.615). -/
theorem thm2_corrected (f : ℝ) (hf0 : 0 < f)
    (h : Real.log f + (3.2 : ℝ) ^ 2 * (f ^ 2 - 1) / 2 = -4.49) : 1 / 2 < f ∧ f < 0.615 := by
  constructor
  · by_contra hc
    push_neg at hc
    have h2 : Real.log f ≤ Real.log (1 / 2) := Real.log_le_log hf0 hc
    have h3 : Real.log (1 / 2 : ℝ) = -Real.log 2 := by
      rw [one_div, Real.log_inv]
    have h4 := Real.log_two_gt_d9
    have hsq : f ^ 2 ≤ 1 / 4 := by nlinarith
    nlinarith
  · by_contra hc
    push_neg at hc
    have h1 : (0 : ℝ) < 0.615 := by norm_num
    have h2 : Real.log 0.615 ≤ Real.log f := Real.log_le_log h1 hc
    have h3 : 1 - (0.615 : ℝ)⁻¹ ≤ Real.log 0.615 := Real.one_sub_inv_le_log_of_pos h1
    have hsq : (0.615 : ℝ) ^ 2 ≤ f ^ 2 := by nlinarith
    norm_num at h3
    nlinarith

/-- Gamma0 / Gamma_psi in common units (per Myr): 0.820e-3 / 4.20 = 1.952e-4, not 0.032. -/
theorem thm4_corrected : |(0.820e-3 : ℝ) / 4.20 - 1.952e-4| < 1e-7 ∧ (0.820e-3 : ℝ) / 4.20 ≠ 0.032 := by
  constructor
  · rw [abs_lt]; constructor <;> norm_num
  · norm_num

end SS1

#print axioms SS1.peel_ge_bare
#print axioms SS1.peel_le_frozen
#print axioms SS1.thm2_corrected
#print axioms SS1.thm4_corrected
