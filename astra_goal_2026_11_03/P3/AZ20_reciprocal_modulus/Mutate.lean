import Std
/- Unequal weights falsely asserted to retain exchange symmetry. -/
example :
 ((1-(1:Rat)/(1+3*2*2)^2)/3+2*(1-1/(1+3/2*2)^2)/3) =
 ((1-(1:Rat)/(1+3/2*2)^2)/3+2*(1-1/(1+3*2*2)^2)/3) := by
 decide +kernel
