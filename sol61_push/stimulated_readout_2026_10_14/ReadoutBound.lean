import Mathlib

-- A conditional algebraic bound, not a derivation of the physical rate model.
theorem readout_denominator_gap (γ κ η : ℝ) :
    (γ + κ) * (γ * κ + 4 * η ^ 2) - κ * (γ + 2 * η) ^ 2 =
      γ * (κ - 2 * η) ^ 2 := by ring

theorem readout_efficiency_bound (γ κ η : ℝ)
    (hγ : 0 < γ) (hκ : 0 < κ) (hη : 0 ≤ η) :
    4 * η ^ 2 * κ / ((γ + κ) * (γ * κ + 4 * η ^ 2)) ≤
      4 * η ^ 2 / (γ + 2 * η) ^ 2 := by
  have hd : 0 < (γ + κ) * (γ * κ + 4 * η ^ 2) := by positivity
  have he : 0 < (γ + 2 * η) ^ 2 := by positivity
  apply (div_le_div_iff₀ hd he).2
  have hprod : 0 ≤ 4 * η ^ 2 * γ * (κ - 2 * η) ^ 2 := by positivity
  nlinarith [readout_denominator_gap γ κ η]
