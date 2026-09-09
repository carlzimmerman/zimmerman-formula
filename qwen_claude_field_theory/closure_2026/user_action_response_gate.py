"""Physical static response of the submitted action, regular planar background.

Use the preceding static reduction, zero slip boundary conditions, constant
background scalar gradient s0 and J differentiable twice there. Compare its
Fourier response with the scale-independent symbol of local AQUAL.
"""
import json
import sympy as s
a,b,d,j1,xi,k,rho=s.symbols('a b d j1 xi k rho',nonzero=True,real=True)
P,f=s.symbols('delta_Phi delta_phi',real=True)
# a=1/(4*pi*G)-2*(c1+c4); d=J'(s0^2)+2*s0^2*J''(s0^2).
# Quadratic Fourier energy, after independently obtained no-slip relation.
L=-a*k**2*P**2/2+2*b*k**2*P*f-b*(d*k**2+j1*xi**2*k**4)*f**2-rho*P
H=s.hessian(L,(P,f))
solution=s.solve([s.diff(L,v) for v in (P,f)],(P,f),dict=True)[0]
inverse_response=s.factor(-rho/(k**2*solution[P]))
scale_derivative=s.factor(s.diff(inverse_response,k))
assert s.simplify(H*s.Matrix([solution[P],solution[f]])-s.Matrix([rho,0]))==s.zeros(2,1)
assert s.simplify(s.diff(inverse_response.subs(xi,0),k))==0
assert s.simplify(scale_derivative-4*b*j1*xi**2*k/(d+j1*xi**2*k**2)**2)==0
rows=[dict(k=float(v),inverse_response=float(inverse_response.subs({a:4,b:1,d:1,j1:1,xi:1,k:v}))) for v in (s.Rational(1,10),1,10)]
print(json.dumps(dict(hessian=str(H),determinant=str(s.factor(H.det())),
    physical_potential=str(solution[P]),inverse_response=str(inverse_response),
    scale_derivative=str(scale_derivative),illustrative_dimensionless_samples=rows,
    scope=__doc__,full_theory='OPEN',
    result='Regular nonzero b,j1,xi gives scale-dependent static response; incompatible with exact local AQUAL for arbitrary wavelengths in this reduction.'),indent=2))
