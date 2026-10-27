import json,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh,cho_factor,cho_solve
from response_stiffness import Response,PROFILES,h,checks

def run(i,n):
    _,mass,b,_=PROFILES[i];m=Response(mass,b,n,environment=2)
    C=m.kinematics(.95)['C'];sd=np.sqrt(m.mobility_denom)
    def fg(v):
        E,g=m.energy_grad(v/sd,20,C)
        return E/m.normalization,g/sd/m.normalization
    opt=minimize(fg,sd.copy(),jac=True,method='L-BFGS-B',bounds=list(zip(np.zeros(n),sd)),options=dict(maxiter=10000,ftol=1e-15,gtol=1e-10,maxls=40,maxcor=30))
    x=opt.x/sd;q=h(x);E,g=m.energy_grad(x,20,C)
    inner=(m.r>=.5*m.b)&(m.r<=min(5*m.b,.4*m.R));outer=m.r>=.8*m.R
    return dict(profile=i,n=n,q_inner=float(np.dot(m.m[inner],q[inner])/sum(m.m[inner])),q_outer=float(np.dot(m.m[outer],q[outer])/sum(m.m[outer])),energy=float(E),success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),max_speed=float(max(abs(cho_solve(cho_factor(m.metric),g)))),eigenvalue=float(eigh(m.hessian(x,20,C),m.metric,subset_by_index=[0,0],eigvals_only=True)[0]),x=x.tolist())
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for i in [1,2]:
        for n in [64,128,256]:
            r=run(i,n);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k!='x'},flush=True)
