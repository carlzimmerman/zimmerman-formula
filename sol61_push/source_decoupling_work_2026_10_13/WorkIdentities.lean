import Mathlib

namespace DecouplingWork

-- The state is fixed across this instantaneous parameter change.
theorem quench_work (H0 C q0 q1 : ℝ) :
    (H0+q1*C)-(H0+q0*C)=(q1-q0)*C := by ring

theorem positive_quench_work (C q0 q1 : ℝ)
    (hc : C ≤ 0) (hq : q1 ≤ q0) : 0 ≤ (q1-q0)*C := by
  exact mul_nonneg_of_nonpos_of_nonpos (sub_nonpos.mpr hq) hc

-- The interaction energy remains present even after source conversion stops.
theorem retained_repulsive_energy (A K B k C : ℝ) :
    (A+K+k*B^2/2)-(A+K+k*B^2/2+C) = -C := by ring

end DecouplingWork

#print axioms DecouplingWork.quench_work
#print axioms DecouplingWork.positive_quench_work
#print axioms DecouplingWork.retained_repulsive_energy
