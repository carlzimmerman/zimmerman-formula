import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
namespace MediumEmission

-- These are conditional nonrelativistic energy-accounting lemmas, not field dynamics.
theorem energy_partition (d cs w gain : ℝ)
    (balance : d = gain + cs*w) : gain = d-cs*w := by linarith

theorem no_release_is_drag (cs w gain : ℝ) (hcs : 0 < cs) (hw : 0 < w)
    (balance : 0 = gain + cs*w) : gain < 0 := by
  nlinarith [mul_pos hcs hw]

theorem zero_release_threshold (cs w v μ : ℝ)
    (hw : 0 < w) (hv : 0 ≤ v) (hμ : μ ≤ 1)
    (balance : cs*w + w^2/2 = v*w*μ) : cs < v := by
  have upper : v*w*μ ≤ v*w := mul_le_of_le_one_right (mul_nonneg hv (le_of_lt hw)) hμ
  have hw2 : 0 < w^2 := sq_pos_of_pos hw
  nlinarith

theorem cold_nonzero_recoil_requires_release (d cs w : ℝ)
    (hcs : 0 < cs) (hw : 0 < w)
    (balance : d = cs*w+w^2/2) : 0 < d := by
  nlinarith [mul_pos hcs hw, sq_nonneg w]

theorem fixed_recoil_cannot_allow_opposite_directions (d cs w v : ℝ)
    (hw : 0 < w) (hv : 0 < v)
    (forward : d = cs*w-v*w+w^2/2)
    (backward : d = cs*w+v*w+w^2/2) : False := by
  nlinarith [mul_pos hv hw]

theorem internal_reservoir_identity (U U' K K' radiation d : ℝ)
    (reservoir : U' = U-d) (transfer : K'-K = d-radiation) :
    U'+K'+radiation = U+K := by linarith

#print axioms energy_partition
#print axioms no_release_is_drag
#print axioms zero_release_threshold
#print axioms cold_nonzero_recoil_requires_release
#print axioms fixed_recoil_cannot_allow_opposite_directions
#print axioms internal_reservoir_identity
end MediumEmission
