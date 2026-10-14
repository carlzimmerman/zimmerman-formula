import Mathlib

namespace ColdPrimakoff

-- k.q=x, k.P_target=Mw, epsilon.J=epsilon.q=e for a stationary target.
theorem target_current_reduction (x Mw e : ℝ) :
    x*e-(2*Mw+x)*e = -2*Mw*e := by ring

-- Photon polarization replaced by its momentum in the vertex contraction.
theorem photon_ward_identity (kq kJ : ℝ) :
    kq*kJ-kJ*kq=0 := by ring

end ColdPrimakoff

#print axioms ColdPrimakoff.target_current_reduction
#print axioms ColdPrimakoff.photon_ward_identity
