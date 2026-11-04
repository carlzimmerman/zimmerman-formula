import Std
namespace AZ28
theorem longitudinal_control : (2:Rat)/(1+1)^2=1/2 := by decide +kernel
theorem transverse_control : (2:Rat)/(1+1)=1 := by decide +kernel
theorem k4_control : (16:Rat)/(2*(3*2-1)/(2-1))=8/5 := by decide +kernel
end AZ28
#print axioms AZ28.longitudinal_control
#print axioms AZ28.transverse_control
#print axioms AZ28.k4_control
