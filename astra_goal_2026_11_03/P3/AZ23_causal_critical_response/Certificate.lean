import Std
namespace AZ23
-- Finite witnesses for L[f]=(y^2+3) f''-2y f'+2f at y=1.
theorem homogeneous_y : ((1:Rat)^2+3)*0-2*1*1+2*1=0 := by decide +kernel
theorem particular_y_cubed : ((1:Rat)^2+3)*6-2*1*3+2*1=20 := by decide +kernel
end AZ23
#print axioms AZ23.homogeneous_y
#print axioms AZ23.particular_y_cubed
