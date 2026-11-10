/-
DCN1 MUTATE M4: false versions of DCN1.lean's statements, each with the true statement's proof. Every one must fail.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace DCN1M

-- the 1/(1+u) dropped from the Q term (M3's mutation)
theorem rate_identity_false (u L Q : ℝ) (hu : 0 < u) :
    -(L / (1 + u) - Q / (1 + u) ^ 2) * (u * (2 + u))
      = (2 + u) * (Q - (u / (1 + u) * L + Q / (1 + u) ^ 2)) := by
  have h1 : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

theorem slab_null_false (s : ℝ) : 2 * (s / 2 - s) = s := by ring

theorem sphere_null_false (s : ℝ) : 2 * (s / 6 - s) = -(4 / 3) * s := by ring

theorem slab_null_pos_false (s : ℝ) (hs : 0 < s) : 0 < 2 * (s / 2 - s) := by linarith

theorem sphere_null_pos_false (s : ℝ) (hs : 0 < s) : 0 < 2 * (s / 6 - s) := by linarith

theorem raw_switch_zero_false (γ sig : ℝ) (h : 0 ≤ sig) : -(γ / 2) * (max sig 0) ^ 2 = 0 := by
  rw [max_eq_right h]; ring

end DCN1M
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
