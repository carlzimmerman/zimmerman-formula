import Mathlib
/-!
# AH8 MUTATE control -- deliberately FALSE statements closed with the same tactics; (1)-(3) must FAIL to compile; (4) is a true weaker statement and must compile.
Run: lake env lean AH8_alpha_identity_audit_MUTATE.lean   (expected: errors at (1), (2), (3); none at (4))
-/
open Real
noncomputable def ainv : ℝ := 137.035999177

-- (1) FALSE: the identity is exact (residual below 1e-9)
theorem mutate1 :
    (ainv + 1 / ainv - 12 * π * (1 / ainv) ^ 2) - (128 * π / 3 + 3) < 1e-9 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  norm_num; nlinarith [h1, h2]

-- (2) FALSE: the BARE claim 128 pi/3 + 3 is good to 1e-4 in absolute terms
theorem mutate2 : 128 * π / 3 + 3 - ainv < 0.0001 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  linarith

-- (3) FALSE: 12 pi is at least the exact coefficient 37.74
theorem mutate3 : 37.74 ≤ 12 * π := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  linarith

-- (4) POSITIVE CONTROL (true, weaker than bare_gap): compiles
theorem control_weaker : 0.005 < 128 * π / 3 + 3 - ainv := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  linarith
