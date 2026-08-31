#!/usr/bin/env python3
"""FC-FINAL -> Einstein-aether alpha_2: the Maxwell-point degeneracy. AeST's aether term -(K_B/2)F^2 is the
Maxwell EA point c1=-c3, c2=c4=0. The Foster-Jacobson (gr-qc/0509083) alpha_2 has c_123=c1+c2+c3 in the
denominator; at the Maxwell point c_123=0 => alpha_2 SINGULAR (numerator -c1^2 != 0), and alpha_1=-4c1=O(1).
=> the EA formulas are INAPPLICABLE at AeST's aether point; alpha_1,alpha_2 are entirely scalar-sector
(K_2,Q_0)-regularized => NOT-COMPUTED from EA. Do NOT paste EA coefficients."""
import sympy as sp
c1,c2,c3,c4=sp.symbols('c1 c2 c3 c4',real=True)
c123=c1+c2+c3; c14=c1+c4
alpha1=-8*(c3**2+c1*c4)/(2*c1-c1**2+c3**2)
alpha2=alpha1/2-(c1+2*c3-c4)*(2*c1+3*c2+c3+c4)/(c123*(2-c14))
sub={c3:-c1,c2:0,c4:0}
print("Maxwell point c1=-c3,c2=c4=0:")
print("  c_123 =",sp.simplify(c123.subs(sub)),"=> alpha_2 denominator = 0 => SINGULAR")
print("  alpha_2 numerator =",sp.simplify(((c1+2*c3-c4)*(2*c1+3*c2+c3+c4)).subs(sub)),"(!=0)")
print("  alpha_1 =",sp.simplify(alpha1.subs(sub)),"= -4 c1 = O(1) (bound 1e-4)")
print("=> EA formulas inapplicable at AeST's aether point; alpha_2 = NOT-COMPUTED (scalar-sector regularized).")
