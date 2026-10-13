import Mathlib

/-! Algebraic conservation identities for the stipulated homogeneous equations.
These statements do not certify the photon amplitude or the physical model. -/
namespace ConversionConservation

theorem charge_derivative (c z : ℝ) :
    (-4 * c * z) + 2 * (2 * c * z) = 0 := by ring

theorem energy_derivative (c delta k n z : ℝ) :
    delta * (3 * c * z) + c * (-2 * (delta - 4 * k * n) * z)
      + 2 * k * n * (-4 * c * z) = 0 := by ring

theorem neutral_bilinear (c delta k n nb Q D S : ℝ)
    (hc : c ≠ 0) (hQ : Q = n + 2 * nb)
    (hD : D = delta * nb + c * S + k * n ^ 2) :
    S = (D - delta * (Q - n) / 2 - k * n ^ 2) / c := by
  apply (eq_div_iff hc).mpr
  rw [hQ, hD]
  ring

end ConversionConservation
#print axioms ConversionConservation.charge_derivative
#print axioms ConversionConservation.energy_derivative
#print axioms ConversionConservation.neutral_bilinear
