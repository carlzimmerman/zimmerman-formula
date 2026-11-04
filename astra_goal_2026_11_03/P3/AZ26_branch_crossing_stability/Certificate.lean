import Std
namespace AZ26
theorem unstable_control : ((2:Rat)-1)*(2-4)/(4*(3*2-1)) = -1/10 := by decide +kernel
theorem stable_control : ((2:Rat)-1)*(2-1)/(1*(3*2-1)) = 1/5 := by decide +kernel
end AZ26
#print axioms AZ26.unstable_control
#print axioms AZ26.stable_control
