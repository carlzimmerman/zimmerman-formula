/-
CSD1: Lean statements for the exact items of the lane (its Part 1). They certify the algebra, not the physics, and no
number or label of the lane. Written by the lead after the lane landed. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

  shell_push_cross    : U(y) = a0 y / (a0 - y) equals g exactly when a0 y = g (a0 - y) (a0 - y nonzero).
  balance_is_law      : the static balance of the shell equation, U(y) = g_N + y, gives the law for g = g_N + y:
                        g^2 = g_N (a0 + g).
  self_push           : the clock's own excess pushes outward at second order: U(y) - y = y^2 / (a0 - y).
  self_push_pos       : that push is positive for 0 < y < a0.
  advective_junction  : N_out (v_out - Rdot) = N_in (0 - Rdot) is N_out v_out = Rdot (N_out - N_in).
  outflow_needed      : with a growing front and N_in < N_out the outer flow must move outward.
  inflow_allowed      : with a growing front and N_in > N_out the outer flow moves inward.
-/
import Mathlib

namespace CSD1

theorem shell_push_cross (a0 y g : ℝ) (h : a0 - y ≠ 0) : a0 * y / (a0 - y) = g ↔ a0 * y = g * (a0 - y) :=
  div_eq_iff h

theorem balance_is_law (a0 y gN : ℝ) (hb : a0 * y = (gN + y) * (a0 - y)) :
    (gN + y) ^ 2 = gN * (a0 + (gN + y)) := by
  nlinarith [hb]

theorem self_push (a0 y : ℝ) (h : a0 - y ≠ 0) : a0 * y / (a0 - y) - y = y ^ 2 / (a0 - y) := by
  rw [div_sub' h, div_left_inj' h]
  ring

theorem self_push_pos (a0 y : ℝ) (hy : 0 < y) (hya : y < a0) : 0 < y ^ 2 / (a0 - y) := by
  apply div_pos
  · positivity
  · linarith

theorem advective_junction (Nin Nout vout Rd : ℝ) (h : Nout * (vout - Rd) = Nin * (0 - Rd)) :
    Nout * vout = Rd * (Nout - Nin) := by
  nlinarith [h]

theorem outflow_needed (Nin Nout vout Rd : ℝ) (hN : 0 < Nout) (hR : 0 < Rd) (hlt : Nin < Nout)
    (h : Nout * vout = Rd * (Nout - Nin)) : 0 < vout := by
  by_contra hneg
  push_neg at hneg
  nlinarith [mul_pos hR (sub_pos.mpr hlt), mul_nonneg hN.le (neg_nonneg.mpr hneg)]

theorem inflow_allowed (Nin Nout vout Rd : ℝ) (hN : 0 < Nout) (hR : 0 < Rd) (hgt : Nout < Nin)
    (h : Nout * vout = Rd * (Nout - Nin)) : vout < 0 := by
  by_contra hneg
  push_neg at hneg
  nlinarith [mul_pos hR (sub_pos.mpr hgt), mul_nonneg hN.le hneg]

end CSD1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
