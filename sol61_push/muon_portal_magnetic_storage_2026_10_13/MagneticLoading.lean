import Mathlib
namespace MagneticLoading
-- a=MR^2/2, b=(mu*y+g*F^2/4)/(2*a): generic completion of square.
theorem eliminate_identity (a b R : ℝ) :
 -a*R^2-2*a*b*R = -a*(R+b)^2+a*b^2 := by ring

-- Local independent-particle kinematics for a fixed source pole.
theorem fixed_pole_energy (delta U : ℝ) :
 (delta-2*U)/2+U=delta/2 := by ring

theorem above_free_threshold (delta U : ℝ) (hd : 0 < delta) :
 0 < (delta-2*U)/2+U := by
 rw [fixed_pole_energy]
 linarith

-- Attractive U=-V: classical necessary energy window for creation below
-- the free two-particle threshold. No rate or eigenstate claim.
theorem subthreshold_window (delta V : ℝ) :
 (0 < (delta+2*V)/2 ∧ delta/2 < 0) ↔
 (-2*V < delta ∧ delta < 0) := by constructor <;> intro h <;> constructor <;> linarith [h.1, h.2]
end MagneticLoading
#print axioms MagneticLoading.eliminate_identity
#print axioms MagneticLoading.fixed_pole_energy
#print axioms MagneticLoading.above_free_threshold
#print axioms MagneticLoading.subthreshold_window
