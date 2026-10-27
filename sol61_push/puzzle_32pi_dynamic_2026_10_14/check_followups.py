import sympy as s
import json
M,C,a,d=s.symbols('M C a d',positive=True)
V=2*C*M**2*a**2+d
f=-3*M**2/(16*C*a**2)
r=s.factor(s.diff(V,a)-s.Rational(8,3)*s.diff(f,a)*V**2/M**4)
assert s.simplify(r+d*(4*C*M**2*a**2+d)/(C*M**2*a**3))==0
U=s.Function('U')(a)
freedom=-3*M**4/(8*U)
assert s.simplify(s.diff(U,a)-s.Rational(8,3)*s.diff(freedom,a)*U**2/M**4)==0
print(json.dumps({'checks':2,'positive_vacuum_shift_residual':str(r),'continuum_designer_identity':'f=f0-3 M^4/(8 V) for arbitrary nonzero differentiable V','scope':'stationary homogeneous equations only'},indent=2))
