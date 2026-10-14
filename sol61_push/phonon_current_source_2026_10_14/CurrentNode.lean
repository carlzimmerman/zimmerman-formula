import Mathlib

namespace PhononCurrent

-- The polarization-summed transverse numerator at zero outgoing momentum.
-- Physical reduction to this expression is an independent modeling obligation.
theorem transverse_numerator_at_rest (energy qt t qsq : ℝ) (hqt : qt = 0) :
    energy^2 - qt * t / (2 * qsq) = energy^2 := by
  simp [hqt]

theorem transverse_numerator_positive (energy qt t qsq : ℝ)
    (he : energy ≠ 0) (hqt : qt = 0) :
    0 < energy^2 - qt * t / (2 * qsq) := by
  rw [transverse_numerator_at_rest energy qt t qsq hqt]
  exact sq_pos_of_ne_zero he

-- Energy supplied by a photon includes the internal excitation energy.
theorem excitation_energy_accounted (photon daughter omega n : ℝ)
    (h : photon = daughter + (n + 1) * omega) :
    photon - daughter = (n + 1) * omega := by linarith

end PhononCurrent
#print axioms PhononCurrent.transverse_numerator_at_rest
#print axioms PhononCurrent.transverse_numerator_positive
#print axioms PhononCurrent.excitation_energy_accounted
