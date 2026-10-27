import Mathlib
noncomputable section
namespace SpatialRegulator
theorem vacuum_frequency_positive (k K S : ℝ)
    (hk : 0<k) (hK : 0<K) (hS : 0<S) : 0<k^4/(K*S^2) := by positivity

theorem radial_speed_control (kap v scale K bound : ℝ)
    (hscale : 0 < scale) (hK : 0 < K)
    (h : 4*kap*v ≤ bound*K*scale^2) :
    4*kap*v/(K*scale^2) ≤ bound := by
  apply (div_le_iff₀ (by positivity : 0 < K*scale^2)).2
  nlinarith [h]

theorem quartic_gradient_energy_nonnegative (lap S : ℝ) (hS : 0<S) :
    0 ≤ lap^2/(2*S^2) := by positivity

#print axioms vacuum_frequency_positive
#print axioms radial_speed_control
#print axioms quartic_gradient_energy_nonnegative
end SpatialRegulator
