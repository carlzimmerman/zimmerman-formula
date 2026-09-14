/-
  K002 -- algebra of the f31 closed form that killed H004.

  Lean certifies mathematics, not physics.  The physical verdict is
  grok_push/K002_action_door_closed.out, reading hunt_2026/f31*.out.

  Certified here:
    drag_at_zero              : at XI2 = 0 the form reduces to the AeST lock
                                drag = -4(2-K_B)/(J_Y+1)
    drag_grows_linear         : the XI2 coefficient is 4(2-K_B) J_Y / (J_Y+1)^2
                                which is positive whenever 0 < K_B < 2 and J_Y > 0
                                -- so past XI2 ~ 1 the drag GROWS, it does not
                                suppress
    lock_is_ghost             : -(2-K_B)/(J_Y+1) < 0 for 0 < K_B < 2, J_Y > 0
                                -- the AeST lock value of c_14 is a spin-1 ghost
-/
import Mathlib

noncomputable section

/-- f31's fitted drag: 4(2-K_B)/(J_Y+1) * (J_Y XI2/(J_Y+1) - 1). -/
def drag (KB JY XI2 : ℝ) : ℝ :=
  (4 * (2 - KB) / (JY + 1)) * (JY * XI2 / (JY + 1) - 1)

/-- At XI2 = 0 the form is the AeST lock piece -4(2-K_B)/(J_Y+1). -/
theorem drag_at_zero (KB JY : ℝ) (hY : JY + 1 ≠ 0) :
    drag KB JY 0 = -4 * (2 - KB) / (JY + 1) := by
  unfold drag
  field_simp
  ring

/-- The coefficient of XI2 is 4(2-K_B) JY / (JY+1)^2.
    For 0 < K_B < 2 and JY > 0 this is strictly positive: the drag grows. -/
theorem drag_grows_linear (KB JY XI2 : ℝ)
    (hY : JY + 1 ≠ 0) :
    drag KB JY XI2 =
      (4 * (2 - KB) * JY / (JY + 1) ^ 2) * XI2
        - 4 * (2 - KB) / (JY + 1) := by
  unfold drag
  field_simp

/-- Sign of the slope: 0 < K_B < 2 and JY > 0 => the XI2 coefficient is > 0. -/
theorem drag_slope_pos (KB JY : ℝ)
    (_hKB0 : 0 < KB) (hKB2 : KB < 2) (hJY : 0 < JY) :
    0 < 4 * (2 - KB) * JY / (JY + 1) ^ 2 := by
  have hnum : 0 < 4 * (2 - KB) * JY := by nlinarith
  have hden : 0 < (JY + 1) ^ 2 := by nlinarith
  exact div_pos hnum hden

/-- Under 0 < K_B < 2 and JY > 0 the lock value of c_14 is strictly negative
    (spin-1 ghost). -/
theorem lock_is_ghost (KB JY : ℝ)
    (_hKB0 : 0 < KB) (hKB2 : KB < 2) (hJY : 0 < JY) :
    -((2 - KB) / (JY + 1)) < 0 := by
  have hden : 0 < JY + 1 := by linarith
  have hnum : 0 < 2 - KB := by linarith
  have : 0 < (2 - KB) / (JY + 1) := div_pos hnum hden
  linarith

end

#print axioms drag_at_zero
#print axioms drag_grows_linear
#print axioms drag_slope_pos
#print axioms lock_is_ghost
