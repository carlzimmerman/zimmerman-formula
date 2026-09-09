"""Leading static planar weak-field variation of Carl's submitted action.

Assumptions: normalized clock at rest, Q0=0, regular quadratic weak-field
expansion, ca=c1+c4 in the submitted normalization, b=2-K_B. Keep the
nonlinear scalar gradient function. This is not a full Dirac/PPN analysis.
"""
import json
import sympy as s
x=s.symbols('x',real=True)
G,b,ca,xi,j=s.symbols('G b ca xi j',nonzero=True,real=True)
P,Z,f=[s.Function(v)(x) for v in ('Phi','Psi','phi')]
rho=s.Function('rho')(x)
J=s.Function('J')
B=s.diff(f,x)**2+xi**2*s.diff(f,x,2)**2
L=(s.diff(Z,x)**2-2*s.diff(P,x)*s.diff(Z,x))/(8*s.pi*G)
L+=ca*s.diff(P,x)**2+2*b*s.diff(P,x)*s.diff(f,x)-b*J(B)-rho*P
def EL(density,field):
    return s.diff(density,field)-s.diff(s.diff(density,s.diff(field,x)),x)+s.diff(s.diff(density,s.diff(field,x,2)),x,2)
eq={str(v):s.simplify(EL(L,v)) for v in (P,Z,f)}
# Independently check the affine-J specialization and the GR limit.
linear=L.subs(J(B),j*B)
scalar=s.expand(EL(linear,f)/(2*b))
coefficient=s.diff(scalar,s.diff(f,x,4))
assert s.simplify(scalar-(-s.diff(P,x,2)+j*s.diff(f,x,2)-j*xi**2*s.diff(f,x,4)))==0
assert s.simplify(eq[str(P)].subs({ca:0,b:0})-(s.diff(Z,x,2)/(4*s.pi*G)-rho))==0
assert s.simplify(eq[str(Z)]-(s.diff(P,x,2)-s.diff(Z,x,2))/(4*s.pi*G))==0
print(json.dumps(dict(euler_lagrange={k:str(v) for k,v in eq.items()},
    affine_J_fourth_derivative_coefficient=str(coefficient),
    full_theory='OPEN',scope=__doc__),indent=2))
