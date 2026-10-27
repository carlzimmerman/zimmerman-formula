import Mathlib

namespace ColdSourceKinematics

-- P is the magnitude of the produced mediator momentum. Its positive-energy
-- mass shell and a target-rest-frame minus-momentum constraint imply this bound.
theorem momentum_bound (ER P M T : ℝ)
    (hT : 0 < T) (hP : 0 ≤ P) (hER : 0 ≤ ER)
    (shell : ER^2 = M^2+P^2) (lightcone : ER-P < T) :
    M^2-T^2 < 2*T*P := by
  have hp : 0 < (T+P-ER)*(T+P+ER) :=
    mul_pos (by linarith) (by linarith)
  nlinarith

-- r is the strictly positive minus momentum of the outgoing massive target.
theorem from_conserved_minus_momentum (ER P Pz M T r : ℝ)
    (hT : 0 < T) (hP : 0 ≤ P) (hER : 0 ≤ ER)
    (shell : ER^2 = M^2+P^2) (hr : 0 < r)
    (hz : Pz ≤ P) (conservation : ER-Pz+r=T) :
    M^2-T^2 < 2*T*P := by
  apply momentum_bound ER P M T hT hP hER shell
  linarith

end ColdSourceKinematics

#print axioms ColdSourceKinematics.momentum_bound
#print axioms ColdSourceKinematics.from_conserved_minus_momentum
