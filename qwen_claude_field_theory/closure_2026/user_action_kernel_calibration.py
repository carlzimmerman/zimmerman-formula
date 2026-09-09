"""Construct J parametrically for the unscreened leading static reduction.

xi=0, zero scalar flux, positive aligned gradients, no-slip boundary data.
This is a conditional weak-field calibration, not full covariant closure.
"""
import json
import sympy as s
import numpy as np
from scipy.optimize import brentq
y=s.symbols('y',positive=True)
a,A,b,a0=s.symbols('a A b a0',positive=True)
mu=1-s.exp(-y);g=a0*y
scalar=(a*g-A*mu*g)/(2*b)
# J_s=2g follows from J'(s^2)*s=g; integrate using the actual scalar map.
integrand=2*g*s.diff(scalar,y)
primitive=s.integrate(integrand,y)
kernel=s.simplify(primitive-s.limit(primitive,y,0,dir='+'))
constitutive=s.simplify(s.diff(kernel,y)/s.diff(scalar**2,y))
assert s.simplify(constitutive*scalar-g)==0
assert s.simplify(a*g-2*b*scalar-A*mu*g)==0
D=s.simplify(s.diff(mu*y,y))
stationary=s.solve(s.diff(D,y),y)
peak=s.simplify(D.subs(y,stationary[0]))
sf=s.lambdify((y,a,A,b,a0),scalar,'numpy')
jf=s.lambdify((y,a,A,b,a0),constitutive,'numpy')
residual=[]
for target in np.geomspace(1e-5,50,61):
    sv=float(sf(target,1.2,1.,1.,1.))
    recovered=brentq(lambda z:sf(z,1.2,1.,1.,1.)-sv,1e-12,100.,xtol=1e-14)
    physical=float(jf(recovered,1.2,1.,1.,1.)*sv)
    residual.append(abs(physical-target)/target)
# A lower a/A is a counter-control: the map folds on a finite interval.
derivative=s.diff(scalar,y)
bad=float(derivative.subs({a:1.1,A:1,b:1,a0:1,y:stationary[0]}))
assert bad<0
assert max(residual)<1e-7
print(json.dumps(dict(scalar_gradient=str(scalar),parametric_J=str(kernel),
    J_derivative=str(constitutive),max_AQUAL_longitudinal_coefficient=str(peak),
    sufficient_monotone_condition='a/A > '+str(peak),
    inverse_check_max_relative_error=max(residual),fold_control_derivative=bad,
    full_theory='OPEN',scope=__doc__),indent=2))
