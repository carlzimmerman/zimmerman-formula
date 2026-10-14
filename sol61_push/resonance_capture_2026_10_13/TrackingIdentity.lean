import Mathlib
namespace ResonanceCapture
 theorem residual_identity (x y R err : ℝ) :
  (1+err)*(x^2+(y-R)^2)-R^2 =
  x^2+y^2-2*R*y+err*(x^2+(y-R)^2) := by ring
 theorem tracking_real (x y R err C sigma : ℝ) :
  -x/2+(sigma+C*((1+err)*(x^2+(y-R)^2)-R^2))*(y-R)+sigma*R =
  -x/2+sigma*y+C*(x^2+y^2-2*R*y+err*(x^2+(y-R)^2))*(y-R) := by ring
 theorem tracking_imag (x y R Rp err C sigma : ℝ) :
  -(y-R)/2-(sigma+C*((1+err)*(x^2+(y-R)^2)-R^2))*x-(Rp+R/2)+Rp =
  -y/2-sigma*x-C*(x^2+y^2-2*R*y+err*(x^2+(y-R)^2))*x := by ring
end ResonanceCapture
#print axioms ResonanceCapture.residual_identity
#print axioms ResonanceCapture.tracking_real
#print axioms ResonanceCapture.tracking_imag
