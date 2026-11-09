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

namespace SS1M
/-- MUTATE: the outside text's Theorem 2 bound as written. Must NOT compile. -/
theorem thm2_as_written (f : ℝ) (hf0 : 0 < f)
    (h : Real.log f + (3.2 : ℝ) ^ 2 * (f ^ 2 - 1) / 2 = -4.49) : (0.615 : ℝ) ≤ f := by
  nlinarith [Real.log_le_sub_one_of_pos hf0]
end SS1M
