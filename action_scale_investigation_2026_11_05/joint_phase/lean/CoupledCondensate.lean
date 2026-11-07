import Std
namespace CoupledCondensate
open Std Lean.Grind
variable {F : Type} [Field F]

-- Thermodynamic pressure of a repulsive, nonrelativistic condensate.
theorem interaction_pressure (m n g mu e : F)
    (hm : mu=m+g*n) (he : 2*e=2*m*n+g*n^2) :
    2*(n*mu-e)=g*n^2 := by grind

-- Relaxing a massive phase fluctuation induces an attractive correction.
theorem relaxed_phase_energy (k h n g z e : F)
    (stationary : k*z+h*n=0)
    (energy : 2*e=g*n^2+k*z^2+2*h*n*z) :
    2*k*e=(k*g-h^2)*n^2 := by grind

-- The induced interaction stays fixed under a field-width deformation.
theorem induced_coupling_invariant (s k kp h hp g ge gep : F)
    (hs : s ≠ 0) (hk : k ≠ 0)
    (curvature : kp*s^2=k) (coupling : hp*s=h)
    (old : k*ge=k*g-h^2) (new : kp*gep=kp*g-hp^2) :
    gep=ge := by grind

-- Neutral exterior charge does not delete the interior electric force.
theorem charge_force (p G m n mb q qb : F) :
    -(4*p*G*m*(m*n+mb))-q*(qb-q*n) =
    -(4*p*G*m^2-q^2)*n-(4*p*G*m*mb+q*qb) := by grind

-- Fixed-shape homologous energy E=A/R^3-D/R+C*R^3+S*R^2.
-- force and curvature are supplied after differentiation; calculus is external.
theorem homologous_curvature (a d c s r curvature : F)
    (stationary : -3*a+d*r^2+3*c*r^6+2*s*r^5=0)
    (second : curvature*r^5=12*a-2*d*r^2+6*c*r^6+2*s*r^5) :
    curvature*r^5=6*a+12*c*r^6+6*s*r^5 := by grind

section Ordered
variable [LE F] [LT F] [LawfulOrderLT F] [IsLinearOrder F] [OrderedRing F]

-- L=d log N/d log R; t is the surface fraction, j the concentration slope.
-- Their physical bounds are proved in the accompanying analytic note.
theorem inventory_slope (L t j : F) (ht : t ≤ 1) (hj : 0 ≤ j)
    (profile : 2*L=6-t+2*j) : 5 ≤ 2*L := by grind

-- b=d log(v_edge^4)/d log N, for fixed particle mass and N proportional to Mb.
theorem speed_exponent (L b : F) (hL : 0 < L) (hl : 5 ≤ 2*L)
    (speed : b*L=2*L-2) : 6 ≤ 5*b := by
  have heq : (5*b)*L=10*L-10 := by grind
  have hprod : 6*L ≤ (5*b)*L := by grind
  exact (Field.IsOrdered.mul_le_mul_iff_of_pos_right hL).mp hprod

theorem no_linear_mass_scaling (b : F) (bound : 6 ≤ 5*b) : b ≠ 1 := by grind
end Ordered

#print axioms interaction_pressure
#print axioms relaxed_phase_energy
#print axioms induced_coupling_invariant
#print axioms charge_force
#print axioms homologous_curvature
#print axioms inventory_slope
#print axioms speed_exponent
#print axioms no_linear_mass_scaling
end CoupledCondensate
