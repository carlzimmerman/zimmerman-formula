module

public import Mathlib.Algebra.Order.Field.Basic
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Ring.Basic
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.NormNum

@[expose] public section

/-!
Conditional clock-tilt and static-response algebra.

The component action, auxiliary branch, PDE/source dictionary, clock mode
interpretation, and gravitating vacuum stress are not established here.
The displayed ratio uses conditional rigid coefficients of the specified
static branch; it is not a healthy gravitational normalization result.
-/

namespace Why4.ClockTilt

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def tiltLagrangian (a j H v u : K) : K :=
  (a + j) * u ^ 2 / 2 - j * H * v * u + j * H ^ 2 * v ^ 2 / 2

def tiltOmegaSquared (a j M H : K) : K :=
  -(H ^ 2 * j * a / ((a + j) * M))

def staticStiffness (t : K) : K := 1 + t / 3 - 2 * t ^ 2 / 3

theorem complete_square_identity
    (a j H v u : K) (hK : a + j ≠ 0) :
    tiltLagrangian a j H v u =
      (a + j) / 2 * (u - j * H * v / (a + j)) ^ 2 +
        H ^ 2 * j * a * v ^ 2 / (2 * (a + j)) := by
  unfold tiltLagrangian
  field_simp [hK]
  ring1

theorem tilt_frequency_negative
    (a j M H : K) (ha : 0 < a) (hj : 0 < j) (hM : 0 < M) (hH : H ≠ 0) :
    tiltOmegaSquared a j M H < 0 := by
  have hnum : 0 < H ^ 2 * j * a :=
    mul_pos (mul_pos (sq_pos_of_ne_zero hH) hj) ha
  have hden : 0 < (a + j) * M := mul_pos (add_pos ha hj) hM
  have hquot : 0 < H ^ 2 * j * a / ((a + j) * M) := div_pos hnum hden
  unfold tiltOmegaSquared
  linarith

theorem static_stiffness_factorization (t : K) :
    staticStiffness t = (t + 1) * (3 - 2 * t) / 3 := by
  unfold staticStiffness
  ring1

theorem static_stiffness_positive
    (t : K) (htlo : -(1 : K) < t) (hthi : t < 1 / 4) :
    0 < staticStiffness t := by
  rw [static_stiffness_factorization]
  exact div_pos (mul_pos (by linarith) (by linarith)) (by norm_num)

theorem conditional_rigid_static_ratio
    (g tau : K) (hg : g ≠ 0) (htau : tau ≠ 0) :
    (g ^ 2 / (12 * tau)) * (500 * g * tau / 81) / (25 * g / 48) ^ 3 =
      4096 / 1125 := by
  field_simp [hg, htau]
  ring1

theorem conditional_source_bridge (P : K) :
    (32 * P / 9) / (4096 / 1125) = 125 * P / 128 := by
  field_simp
  ring1

theorem conditional_source_bridge_gt_quarter
    (P : K) (hP : 3 ≤ P) : (1 / 4 : K) < (32 * P / 9) / (4096 / 1125) := by
  rw [conditional_source_bridge]
  linarith

#check @complete_square_identity
#check @tilt_frequency_negative
#check @static_stiffness_factorization
#check @static_stiffness_positive
#check @conditional_rigid_static_ratio
#check @conditional_source_bridge
#check @conditional_source_bridge_gt_quarter
#print axioms complete_square_identity
#print axioms tilt_frequency_negative
#print axioms static_stiffness_factorization
#print axioms static_stiffness_positive
#print axioms conditional_rigid_static_ratio
#print axioms conditional_source_bridge
#print axioms conditional_source_bridge_gt_quarter

end Why4.ClockTilt
