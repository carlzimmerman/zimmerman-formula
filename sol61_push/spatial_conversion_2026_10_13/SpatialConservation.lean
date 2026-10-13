import Mathlib

/-! Pointwise real-component algebra; PDE existence and continuum numerics
are not formalized. A,B are daughter components, C,D source components. -/
namespace SpatialConservation

theorem local_charge_flow (A B C D AX BX CX DX c V W : ℝ) :
    2*A*(-BX/2 + 2*c*(D*A-C*B)+V*B)
    + 2*B*(AX/2 - 2*c*(C*A+D*B)-V*A)
    + 4*C*(-DX/4 + 2*c*A*B+W*D)
    + 4*D*(CX/4 - c*(A^2-B^2)-W*C)
    = -(A*BX-B*AX+C*DX-D*CX) := by ring

theorem weighted_current_bound (a b u v : ℝ) :
    (a*u+b*v)^2 ≤ (a^2+2*b^2)*(u^2+v^2/2) := by
  nlinarith [sq_nonneg (a*v-2*b*u)]

end SpatialConservation
#print axioms SpatialConservation.local_charge_flow
#print axioms SpatialConservation.weighted_current_bound
