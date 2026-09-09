"""Construct a local curved static branch via a spatial Routh reduction.

Illustrative dimensionless parameters; exponential primitive used as J.
This does NOT derive the physical-metric MOND kernel or dynamical stability.
"""
import json
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

P,B,v,A,pp,bp,vp,flux=s.symbols('P B v A Pp Bp vp flux',real=True)
g,ca,b,xi,C=s.symbols('g ca b xi C',real=True)
q=s.Matrix([P,B,v]);vel=s.Matrix([pp,bp,vp])
U=v*v+xi*xi*s.exp(-2*A)*(vp*vp+2*bp*bp*v*v)
# a0=1, J(U)=G(sqrt(U)); a chosen constitutive input, not a fitted result.
J=U+2*(1+s.sqrt(U))*s.exp(-s.sqrt(U))-2
L=s.exp(P-A+2*B)*(g*(2*bp*bp+4*pp*bp)+ca*pp*pp+2*b*pp*s.exp(A)*v)
L-=s.exp(P+A+2*B)*(C+b*J)+flux*s.exp(A)*v
# Last term is Routh subtraction after conserving momentum of phi.
constraint=s.diff(L,A).subs(A,0)
R=L.subs(A,0)
energy=(vel.dot(s.Matrix([s.diff(R,w) for w in vel]))-R)
assert s.simplify(constraint+energy)==0
H=s.hessian(R,vel)
forcing=s.Matrix([s.diff(R,z) for z in q])-s.Matrix([s.diff(R,w) for w in vel]).jacobian(q)*vel
params={g:1,ca:s.Rational(1,10),b:1,xi:s.Rational(1,5),C:s.Rational(1,100)}
args=(P,B,v,pp,bp,vp,flux)
hfun=s.lambdify(args,H.subs(params),'numpy',cse=True)
ffun=s.lambdify(args,forcing.subs(params),'numpy',cse=True)
efun=s.lambdify(args,energy.subs(params),'numpy',cse=True)
initial=np.array([0.,0.,.5,.02,0.,0.])
flux_value=float(s.solve(energy.subs(params).subs(dict(zip(tuple(q)+tuple(vel),initial))),flux)[0])
def rhs(x,y):
    acceleration=np.linalg.solve(hfun(*y,flux_value),np.asarray(ffun(*y,flux_value)).ravel())
    return np.r_[y[3:],acceleration]
if __name__=='__main__':
    rows=[]
    for tolerance in (1e-8,1e-10):
        solution=solve_ivp(rhs,(0.,.1),initial,rtol=tolerance,atol=tolerance*1e-2,dense_output=True)
        values=solution.sol(np.linspace(0,.1,101)) if solution.success else solution.y
        residual=[abs(float(efun(*y,flux_value))) for y in values.T]
        singular=[np.linalg.svd(hfun(*y,flux_value),compute_uv=False)[-1] for y in values.T]
        rows.append(dict(success=solution.success,message=solution.message,rtol=tolerance,
            energy_constraint_max=max(residual),minimum_sampled_spatial_hessian_singular_value=float(min(singular)),
            final_state=solution.y[:,-1].tolist(),function_evaluations=solution.nfev))
    print(json.dumps(dict(full_theory='OPEN',scope=__doc__,parameters={str(k):str(w) for k,w in params.items()},
        scalar_flux=flux_value,spatial_metric_constraint_plus_energy='0 (symbolically verified)',runs=rows),indent=2))
    raise SystemExit(0 if all(r['success'] for r in rows) else 1)
