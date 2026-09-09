"""Curved branch using the calibrated implicit J, finite xi, vacuum planar data.

This tests the same chosen kernel in the full static equations. It does not
test a sourced galactic boundary problem or infer PPN gamma.
"""
import json
import numpy as np
import sympy as s
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
P,B,v,pp,bp,vp,pf,xi=s.symbols('P B v pp bp vp pf xi',real=True)
u,j0,j1,j2=s.symbols('u j0 j1 j2',real=True)
q=s.Matrix([P,B,v]);vel=s.Matrix([pp,bp,vp])
U=v*v+xi*xi*(vp*vp+2*bp*bp*v*v)
jt=j0+j1*(U-u)+j2*(U-u)**2/2
# a=4g-2ca=1.2, A=1, b=1, a0=1 in the calibration.
R=s.exp(P+2*B)*(s.Rational(35,100)*(2*bp*bp+4*pp*bp)+s.Rational(1,10)*pp*pp+2*pp*v-s.Rational(1,100)-jt)-pf*v
H=s.hessian(R,vel).subs(u,U)
F=(s.Matrix([s.diff(R,z) for z in q])-s.Matrix([s.diff(R,w) for w in vel]).jacobian(q)*vel).subs(u,U)
E=(vel.dot(s.Matrix([s.diff(R,w) for w in vel]))-R).subs(u,U)
args=(P,B,v,pp,bp,vp,pf,xi,j0,j1,j2)
hf=s.lambdify(args,H,'numpy',cse=True);ff=s.lambdify(args,F,'numpy',cse=True);ef=s.lambdify(args,E,'numpy',cse=True)
def kernel(U):
    gradient=np.sqrt(U)
    y=brentq(lambda y:y*(.2+np.exp(-y))/2-gradient,0.,max(1.,10*gradient),xtol=1e-14)
    den=.2+np.exp(-y);ds=(den-y*np.exp(-y))/2
    J=.1*y*y+(y*y+y+1)*np.exp(-y)-1
    first=2/den
    second=(2*np.exp(-y)/den**2)/(2*gradient*ds)
    return J,first,second
def arguments(state,flux,length):
    P,B,v,pp,bp,vp=state
    return (*state,flux,length,*kernel(v*v+length**2*(vp*vp+2*bp*bp*v*v)))
rows=[]
for length in (.2,.1):
    initial=np.array([0.,0.,.02*(.2+np.exp(-.02))/2,.02,-.02,0.])
    zero=float(ef(*arguments(initial,0.,length)))
    flux=-zero/(float(ef(*arguments(initial,1.,length)))-zero)
    def rhs(x,state):
        arg=arguments(state,flux,length)
        return np.r_[state[3:],np.linalg.solve(hf(*arg),np.asarray(ff(*arg)).ravel())]
    for tol in (1e-8,1e-10):
        sol=solve_ivp(rhs,(0.,.02),initial,rtol=tol,atol=tol*1e-2,dense_output=True)
        values=sol.sol(np.linspace(0,.02,101)) if sol.success else sol.y
        energy=[abs(float(ef(*arguments(z,flux,length)))) for z in values.T]
        # In the unscreened zero-flux approximation this difference vanishes.
        mismatch=[float(arguments(z,flux,length)[-2]*z[2]-z[3]) for z in values.T]
        rows.append(dict(xi=length,rtol=tol,success=sol.success,scalar_flux=flux,
            constraint_max=max(energy),logarithmic_slip_max=float(max(abs(values[0]+values[1]))),
            scalar_relation_mismatch_max=max(abs(z) for z in mismatch),final_state=sol.y[:,-1].tolist()))
print(json.dumps(dict(full_theory='OPEN',scope=__doc__,runs=rows,
    caution='Nonzero conserved scalar flux and finite curved vacuum data differ from calibration assumptions; mismatch is not isolated to xi.'),indent=2))
raise SystemExit(0 if all(r['success'] for r in rows) else 1)
