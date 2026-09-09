"""Exact static planar EL equations and radial diffeomorphism identity.

Arbitrary differentiable J, normalized static clock; no time/shift variations.
This identity is spatial gauge consistency, not the full matter Ward identity.
"""
import json
import sympy as s
x=s.symbols('x',real=True)
P,A,B,f=[s.Function(n)(x) for n in ('P','A','B','phi')]
G,ca,b,xi,C=s.symbols('G ca b xi C',real=True)
J=s.Function('J')
fp=s.diff(f,x);Pp=s.diff(P,x);Ap=s.diff(A,x);Bp=s.diff(B,x)
U=s.exp(-2*A)*fp**2+xi**2*s.exp(-4*A)*((s.diff(f,x,2)-Ap*fp)**2+2*Bp**2*fp**2)
L=s.exp(P-A+2*B)*((2*Bp**2+4*Pp*Bp)/(16*s.pi*G)+ca*Pp**2+2*b*Pp*fp)
L-=s.exp(P+A+2*B)*(C+b*J(U))
def EL(field):
    return s.diff(L,field)-s.diff(s.diff(L,s.diff(field,x)),x)+s.diff(s.diff(L,s.diff(field,x,2)),x,2)
equations=[EL(v) for v in (P,A,B,f)]
# delta A=epsilon*A'+epsilon'; other fields transform as scalars under x.
identity=sum(E*s.diff(v,x) for E,v in zip(equations,(P,A,B,f)))-s.diff(equations[1],x)
residual=s.simplify(s.expand(identity))
assert residual==0
# A selected derivative coefficient block, not the full principal symbol:
# mixed equations can also contain B''' and must be reduced together.
gauge={A:0,s.diff(A,x):0,s.diff(A,x,2):0,s.diff(A,x,3):0}
physical=[equations[i].subs(gauge).doit() for i in (0,2,3)]
highest=(s.diff(P,x,2),s.diff(B,x,2),s.diff(f,x,4))
matrix=s.Matrix(physical).jacobian(highest)
orders={name:{str(field):int(max([0]+[derivative.derivative_count for derivative in expr.atoms(s.Derivative) if derivative.expr==field])) for field in (P,B,f)} for name,expr in zip(('lapse','transverse','scalar'),physical)}
print(json.dumps(dict(radial_noether_identity=str(residual),
    exact_density=str(L),constraint=str(equations[1].subs(gauge).doit()),
    selected_derivative_coefficient_block=str(matrix),derivative_orders=orders,
    full_theory='OPEN',scope=__doc__),indent=2))
