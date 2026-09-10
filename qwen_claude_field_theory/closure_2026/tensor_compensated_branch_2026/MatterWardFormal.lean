import Mathlib.Data.Real.Basic

/-! Lean on-shell implication for the generated matter Ward identity. -/

namespace MatterWard

theorem conservation_on_matter_shell
    (divT0 divT1 E d0 d1 : ℝ)
    (h0 : divT0 = E * d0)
    (h1 : divT1 = E * d1)
    (hE : E = 0) :
    divT0 = 0 ∧ divT1 = 0 := by
  constructor
  · calc
      divT0 = E * d0 := h0
      _ = 0 := by rw [hE]; exact zero_mul d0
  · calc
      divT1 = E * d1 := h1
      _ = 0 := by rw [hE]; exact zero_mul d1

end MatterWard
