"""Track the old protected branch as the exterior capacitance is restored."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh,cho_factor,cho_solve
from local_state import Local,h,PROFILES
from angular_gate import F

def follow(index,n=128):
    _,mass,b,_=PROFILES[index];m=Local(mass,b,n,30);C=m.kinematics(.95)['C']
    sqrtD=np.sqrt(m.mobility_denom);norm=m.normalization;full=m.tail_link
    Rin=min(5*m.b,.4*m.R);outer=m.r>=.8*m.R;inner=(m.r>=.5*m.b)&(m.r<=Rin)
    v=sqrtD.copy();rows=[]
    for tau in np.r_[0.,np.geomspace(1e-6,1,61)]:
        m.tail_link=full*tau;m.Ltail[-1,-1]=m.tail_link
        def fg(v):
            E,g=m.energy_grad(v/sqrtD,20,C)
            return E/norm,g/sqrtD/norm
        opt=minimize(fg,v,jac=True,method='L-BFGS-B',bounds=list(zip(np.zeros(n),sqrtD)),
            options={'maxiter':4000,'ftol':1e-14,'gtol':1e-9,'maxls':40,'maxcor':30})
        v=opt.x;x=v/sqrtD;q=h(x);E,g=m.energy_grad(x,20,C)
        metric=np.diag(m.mobility_denom)+m.Lmat+m.Ltail
        dx=cho_solve(cho_factor(metric),g)
        ev=float(eigh(m.hessian(x,20,C),metric,subset_by_index=[0,0],eigvals_only=True)[0])
        rows.append(dict(tau=float(tau),optimizer_success=bool(opt.success),message=str(opt.message),
            q_inner=float(np.dot(m.m[inner],q[inner])/sum(m.m[inner])),
            q_outer=float(np.dot(m.m[outer],q[outer])/sum(m.m[outer])),
            energy=float(E),max_phase_speed=float(max(abs(dx))),eigenvalue=ev,iterations=int(opt.nit)))
    return dict(profile=index,n=n,ell_kpc=30,rows=rows)

def exclusion(index,n):
    _,mass,b,_=PROFILES[index];m=Local(mass,b,n,30);C=m.kinematics(.95)['C']
    M=np.diag(m.mobility_denom)
    H=m.Lmat+m.Ltail-np.diag(40*C*F(m.u0)*m.vol)
    ev=float(eigh(H,M,subset_by_index=[0,0],eigvals_only=True)[0])
    return dict(profile=index,n=n,lower_bound_eigenvalue=ev,nonzero_stationary_excluded=bool(ev>0))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=128)
    args=ap.parse_args();out=dict(exclusion=[exclusion(i,n) for i in [1,2] for n in [64,128,256]],runs=[])
    p=Path(args.output)
    for i in [1,2]:
        out['runs'].append(follow(i,args.n));p.write_text(json.dumps(out,indent=2)+'\n')
        print(i,out['runs'][-1]['rows'][-1],flush=True)
