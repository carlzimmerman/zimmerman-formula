import Mathlib
namespace DemixingBounds
theorem positive_gap (r t : ℝ) (hr : 0 < r) (ht : 0 ≤ t) : 0 < r+t := by linarith
theorem unstable_mode (e n d : ℝ) (he : 0 < e) (hband : e < 2*n*d) :
    e*(e-2*n*d) < 0 := by
  exact mul_neg_of_pos_of_neg he (by linarith)
theorem maximum_gain (e n d : ℝ) :
    e*(2*n*d-e) ≤ (n*d)^2 := by
  nlinarith [sq_nonneg (e-n*d)]
end DemixingBounds
#print axioms DemixingBounds.positive_gap
#print axioms DemixingBounds.unstable_mode
#print axioms DemixingBounds.maximum_gain
