/-
CSD1 MUTATE twin: the statements of CSD1.lean with a sign or a term changed. Every theorem is false and must fail
(expected: exit 1, one error per theorem). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace CSD1_MUTATE

theorem balance_is_law_flip (a0 y gN : ℝ) (hb : a0 * y = (gN + y) * (a0 - y)) :
    (gN + y) ^ 2 = gN * (a0 - (gN + y)) := by
  nlinarith [hb]

theorem self_push_flip (a0 y : ℝ) (h : a0 - y ≠ 0) : a0 * y / (a0 - y) - y = -(y ^ 2) / (a0 - y) := by
  rw [div_sub' h, div_left_inj' h]
  ring

theorem advective_junction_flip (Nin Nout vout Rd : ℝ) (h : Nout * (vout - Rd) = Nin * (0 - Rd)) :
    Nout * vout = Rd * (Nout + Nin) := by
  nlinarith [h]

theorem outflow_needed_flip (Nin Nout vout Rd : ℝ) (hN : 0 < Nout) (hR : 0 < Rd) (hlt : Nin < Nout)
    (h : Nout * vout = Rd * (Nout - Nin)) : vout < 0 := by
  by_contra hneg
  push_neg at hneg
  nlinarith [mul_pos hR (sub_pos.mpr hlt), mul_nonneg hN.le hneg]

end CSD1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
