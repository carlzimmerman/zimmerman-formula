import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt

namespace MOND_dS

/--
  Theorem: If the local 2D Rindler horizon area (π / a_0²) multiplied by the
  cosmological vacuum measure Λ equals the 4D Chern-Gauss-Bonnet topological
  normalization constant (32π²), then a_0 is uniquely determined as √(Λ / 32π).
-/
theorem mond_relation (Lambda a_0 : ℝ) (hL : 0 < Lambda) (ha : 0 < a_0)
    (h_match : (Real.pi / a_0 ^ 2) * Lambda = 32 * Real.pi ^ 2) :
    a_0 = Real.sqrt (Lambda / (32 * Real.pi)) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hpi_ne : Real.pi ≠ 0 := ne_of_gt hpi
  have ha_sq_pos : 0 < a_0 ^ 2 := sq_pos_of_ne_zero (ne_of_gt ha)
  have ha_sq_ne : a_0 ^ 2 ≠ 0 := ne_of_gt ha_sq_pos

  -- Step 1: Isolate a_0^2 algebraically from the topological match
  have h_sq : a_0 ^ 2 = Lambda / (32 * Real.pi) := by
    have h1 : Real.pi * Lambda = (32 * Real.pi ^ 2) * a_0 ^ 2 := by
      calc Real.pi * Lambda
        _ = ((Real.pi / a_0 ^ 2) * Lambda) * a_0 ^ 2 := by rw [div_mul_cancel₀ _ ha_sq_ne]
        _ = (32 * Real.pi ^ 2) * a_0 ^ 2             := by rw [h_match]
    have h2 : a_0 ^ 2 = (Real.pi * Lambda) / (32 * Real.pi ^ 2) := by
      have h32_pi2_ne : 32 * Real.pi ^ 2 ≠ 0 := by positivity
      exact (eq_div_of_mul_eq h32_pi2_ne h1).symm
    rw [h2]
    have h_factor : 32 * Real.pi ^ 2 = Real.pi * (32 * Real.pi) := by ring
    rw [h_factor, mul_div_mul_left Lambda (32 * Real.pi) hpi_ne]

  -- Step 2: Apply square root to both sides
  rw [h_sq]
  exact (Real.sqrt_sq (le_of_lt ha)).symm

end MOND_dS
