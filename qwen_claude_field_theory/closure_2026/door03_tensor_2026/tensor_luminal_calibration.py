"""Check whether constant c13 can make the submitted tensor speed luminal.

The local frozen-background principal symbol is derived independently in
door01_joint_2026/tensor_principal.py. Here the calibrated exponential J is
used to test whether the required c13 is constant along acceleration y.
"""
import json
import numpy as np
import sympy as s
y,a,A,b,a0=s.symbols('y a A b a0',positive=True)
xi,F=s.symbols('xi F',positive=True)
mu=1-s.exp(-y)
scalar=a0*y*(a-A+A*s.exp(-y))/(2*b)
Jprime=s.simplify(2*b*s.exp(y)/(a-A+A*s.exp(-y)))
needed=s.simplify(-b*xi**2*Jprime*scalar**2)
variation=s.simplify(s.diff(needed,y))
assert s.simplify(needed + b*xi**2*Jprime*scalar**2)==0
assert s.simplify(variation.subs({a:2*A,y:1}))!=0
nf=s.lambdify((y,a,A,b,a0,xi),needed,'numpy')
samples=np.geomspace(1e-4,50,100)
values=nf(samples,1.2,1.,1.,1.,.2)
print(json.dumps(dict(full_theory='OPEN',required_c13=str(needed),
    derivative_required_c13=str(variation),
    calibrated_s_samples=[float(values[i]) for i in (0,25,50,75,99)],
    calibrated_range=[float(values.min()),float(values.max())],
    condition='With F-c13>0, c_T^2=(F+b J_prime*v^2*xi^2)/(F-c13). Exact c_T=c requires c13=-b J_prime*v^2*xi^2.',
    conclusion='For nonzero b, xi and calibrated varying acceleration, a constant c13 cannot keep c_T=c on an extended branch. If c13=0, positive b*J_prime gives c_T^2>1.',
    scope=__doc__),indent=2))
