import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,cumulative_trapezoid
S=5.364;rmin=1e-5;lam=(7-np.sqrt(73))/2
checks=[]
def check(name,c,detail=''):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name+': '+str(detail))
def components(r,q):
    qq=np.clip(q,0.,S);src=np.minimum(r**3,1)+qq
    root=2*src*r*r/(np.sqrt(src*src+4*src*r*r)+src)
    m=np.minimum(qq+root,S);u=(m-qq)/(r*r)
    return m,u,u/(1-u)
rows=[]
for B in [1.,1000.]:
    previous=None
    for factor in [200.,800.]:
        R=max(200.,factor*B);A=576*B**3
        x=np.unique(np.r_[np.geomspace(rmin,R,1000),1.])
        scale=(A/S)**(1/3);q=S*x**3/(scale**3+x**3)
        f=components(x,q)[2];integ=cumulative_trapezoid(f,x,initial=0)
        h=B*(3*(S-q[-1])/R**3)**(2/3)+integ[-1]-integ
        def rhs(x,y):return np.array([x*x*(np.maximum(y[1],0)/B)**1.5,-components(x,y[0])[2]])
        def bc(a,z):
            d=S-z[0]
            ntail=max((3*d-lam*(d-A/R**3))/R**3,0.)
            return np.array([a[0]-(max(a[1],0)/B)**1.5*rmin**3/3,z[1]-B*ntail**(2/3)])
        sol=solve_bvp(rhs,bc,x,np.array([q,h]),tol=1e-8,max_nodes=30000)
        check('asymptotic Robin solver B%g factor%g'%(B,factor),sol.success,sol.message)
        probe=np.geomspace(rmin,R,3000);qq,hh=sol.sol(probe)
        check('Robin physical domain B%g factor%g'%(B,factor),min(qq)>-1e-7 and max(qq)<S+1e-7 and min(hh)>-1e-8,(min(qq),max(qq),min(hh)))
        value=float((S-sol.sol(R)[0])*R**3/A)
        inner=float(sol.sol(4.)[0])
        rows.append(dict(B=B,outer_factor=factor,outer_radius=R,tail_amplitude_over_leading=value,reference_q_at_r4=inner,nodes=len(sol.x)))
        if previous is not None:
            check('inner Robin convergence B%g'%B,abs(inner-previous[1])<1e-5*S,abs(inner-previous[1]))
            # Slow-decaying asymptotic correction predicts convergence, not an exact finite-R amplitude.
            check('tail amplitude approaches leading B%g'%B,abs(value-1)<abs(previous[0]-1),[previous[0],value])
        previous=(value,inner)
out=dict(checks=checks,decaying_log_radius_exponent=lam,cases=rows,scope='Linearized asymptotic Robin comparison improves outer-tail interpretation; not proof of universal nonlinear asymptotics.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
