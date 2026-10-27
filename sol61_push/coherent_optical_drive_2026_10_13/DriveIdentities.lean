import Mathlib
namespace OpticalDrive
 theorem counterpropagating_invariant (E a b : ℝ) :
  2*((E*a-E*b)^2-(E*a+E*b)^2) = -8*E^2*a*b := by ring
 theorem driven_energy_balance (r i gamma detuning drive : ℝ) :
  2*r*(-gamma*r/2+detuning*i)+2*i*(-gamma*i/2-detuning*r-drive)
  = -gamma*(r^2+i^2)-2*drive*i := by ring
end OpticalDrive
#print axioms OpticalDrive.counterpropagating_invariant
#print axioms OpticalDrive.driven_energy_balance
