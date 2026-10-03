import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt

namespace MOND_Equivalence

variable (Lambda a_0 : ℝ)

-- Node 1: Target MOND Acceleration Relation
def F1 : Prop := a_0 ^ 2 = Lambda / (32 * Real.pi)

-- Node 2: Horizon Area Action Match (A * Lambda = 32π²)
def F2 : Prop := (Real.pi / a_0 ^ 2) * Lambda = 32 * Real.pi ^ 2

-- Node 3: Euclidean Volume Partition Ratio (Vol_prod / Vol_S4 = 16π)
def F3 : Prop := Lambda / (2 * a_0 ^ 2) = 16 * Real.pi

/-- Equivalence Theorem 1 ↔ 2 -/
theorem f1_iff_f2 (hL : 0 < Lambda) (ha : 0 < a_0) : F1 Lambda a_0 ↔ F2 Lambda a_0 := by
  have ha_sq : a_0 ^ 2 ≠ 0 := ne_of_gt (sq_pos_of_ne_zero (ne_of_gt ha))
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  constructor
  · intro h1
    unfold F1 at h1
    unfold F2
    rw [h1]
    have h_div : (Real.pi / (Lambda / (32 * Real.pi))) * Lambda = 32 * Real.pi ^ 2 := by
      calc (Real.pi / (Lambda / (32 * Real.pi))) * Lambda
        _ = (Real.pi * (32 * Real.pi) / Lambda) * Lambda := by rw [div_div_eq_mul_div]
        _ = Real.pi * (32 * Real.pi)                    := mul_div_cancel₀ _ (ne_of_gt hL)
        _ = 32 * Real.pi ^ 2                            := by ring
    exact h_div
  · intro h2
    unfold F2 at h2
    unfold F1
    have h_alg : a_0 ^ 2 = Lambda / (32 * Real.pi) := by
      have h_mul : Real.pi * Lambda = 32 * Real.pi ^ 2 * a_0 ^ 2 := by
        calc Real.pi * Lambda
          _ = (Real.pi / a_0 ^ 2 * Lambda) * a_0 ^ 2 := by rw [div_mul_cancel₀ _ ha_sq]
          _ = 32 * Real.pi ^ 2 * a_0 ^ 2             := by rw [h2]
      have h_div : a_0 ^ 2 = (Real.pi * Lambda) / (32 * Real.pi ^ 2) := by
        have h32 : 32 * Real.pi ^ 2 ≠ 0 := by positivity
        exact (eq_div_of_mul_eq h32 h_mul).symm
      rw [h_div]
      have h_ring : 32 * Real.pi ^ 2 = Real.pi * (32 * Real.pi) := by ring
      rw [h_ring, mul_div_mul_left Lambda (32 * Real.pi) hpi]
    exact h_alg

/-- Equivalence Theorem 1 ↔ 3 -/
theorem f1_iff_f3 (hL : 0 < Lambda) (ha : 0 < a_0) : F1 Lambda a_0 ↔ F3 Lambda a_0 := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  constructor
  · intro h1
    unfold F1 at h1
    unfold F3
    rw [h1]
    calc Lambda / (2 * (Lambda / (32 * Real.pi)))
      _ = Lambda / (Lambda / (16 * Real.pi)) := by
        have : 2 * (Lambda / (32 * Real.pi)) = Lambda / (16 * Real.pi) := by ring
        rw [this]
      _ = 16 * Real.pi := div_div_cancel₀ _ (ne_of_gt hL)
  · intro h3
    unfold F3 at h3
    unfold F1
    have h_alg : a_0 ^ 2 = Lambda / (32 * Real.pi) := by
      have h_mul : Lambda = 16 * Real.pi * (2 * a_0 ^ 2) := by
        exact (div_eq_iff (by positivity)).mp h3
      have h_ring : Lambda = 32 * Real.pi * a_0 ^ 2 := by
        calc Lambda
          _ = 16 * Real.pi * (2 * a_0 ^ 2) := h_mul
          _ = 32 * Real.pi * a_0 ^ 2      := by ring
      have h_div : a_0 ^ 2 = Lambda / (32 * Real.pi) := by
        have h32 : 32 * Real.pi ≠ 0 := by positivity
        exact (eq_div_of_mul_eq h32 h_ring).symm
      exact h_div
    exact h_alg

end MOND_Equivalence
