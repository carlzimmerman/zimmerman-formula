import Std
namespace AZ24
theorem negative_domain : (1:Rat) - (1-(-1/10))^2 = -21/100 := by decide +kernel
theorem vacuum_root : ((1:Rat)+1)*0^2+2*0+1-1=0 := by decide +kernel
end AZ24
#print axioms AZ24.negative_domain
#print axioms AZ24.vacuum_root
