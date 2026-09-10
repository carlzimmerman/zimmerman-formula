#!/usr/bin/env python3
"""Eliminate the actual reduced-action auxiliary; test the Lean formula bridge.

The prior fresh ADM expansion checks the reduced density used here. This
independent Hessian/completion-of-square calculation covers its next reduction.
It is not a nonlinear Dirac or observational certificate.
"""
import json
import sympy as s

B,A,Q,M,H,C,U,p=s.symbols('B A Q M2 H C U p',positive=True)
e=s.symbols('e',real=True)
u,ud,z=s.symbols('u ud z',real=True)
f=B*e+3*A
d=Q*A/(2*M*H)
D=U-Q*A+2*C*Q**2
L=B*(ud-d*u)**2/2-3*A**2*u**2/(4*M)+f*z*(ud-d*u)+e*f*z**2/2 \
  -C*p*u**2+p*(A-2*C*Q)*u*z/H-p*D*z**2/(2*H**2)
zstar=s.solve(s.diff(L,z),z)[0]
reduced=s.factor(L.subs(z,zstar))
actual=s.factor(s.diff(reduced,ud,2))
claimed=B-f**2/(e*f-p*D/H**2)
assert s.factor(actual-claimed)==0
# Independent Schur-complement check, including the cross-gradient terms.
hessian=s.hessian(L,(ud,z))
assert s.factor(actual-(hessian[0,0]-hessian[0,1]**2/hessian[1,1]))==0
assert s.factor(hessian[1,1]-(e*f-p*D/H**2))==0
# The r=0 clock profile fixes D, rather than assuming its sign abstractly.
m=s.symbols('m',positive=True)
assert s.factor(D.subs({U:m*Q*A,C:A/(2*Q*(1+m))})-Q*A*m**2/(1+m))==0
print(json.dumps(dict(auxiliary_solution=str(zstar),kinetic_hessian=str(actual),
                     action_to_Lean_formula_residual='0',independent_Schur_residual='0',
                     clock_profile_D='Q*A*m**2/(1+m)',
                     scope='Quadratic finite-k elimination, with formal p=0 limit; homogeneous action checked separately'),indent=2))
