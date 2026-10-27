"""Checkpointed bounded joint minimization; never discard unfinished states."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from reservoir import Reservoir
from joint import RESERVOIR

class Checkpoint(Reservoir):
    def solve_checkpointed(self,v,path,maxiter=1000):
        path=Path(path);count=[0]
        def fg(a):
            E,g=self.direct(a);return E/100,g/100
        def report(a):
            r=self.report(np.r_[np.log(a[:self.n]),a[self.n:]]);E,g=self.direct(a);active=a[:self.n]>1e-7;lam=np.median(g[:self.n][active]);mr=g[:self.n]-lam;mr=np.where((~active)&(mr>0),0,mr)
            r.update(density_KKT_max=float(max(abs(mr))),mass_constraint_error=float(abs(sum(a[:self.n])-RESERVOIR)),cap_slack_min=float(min(self.cap(a))))
            return r
        def cb(a):
            count[0]+=1
            if count[0]%50==0:
                r=report(a);r.update(status='checkpoint_not_final',iterations=count[0]);path.write_text(json.dumps(r,indent=2)+'\n')
        cons=[dict(type='eq',fun=lambda a:sum(a[:self.n])-RESERVOIR,jac=lambda a:np.r_[np.ones(self.n),np.zeros(self.n)]),dict(type='ineq',fun=self.cap,jac=self.capjac)]
        opt=minimize(fg,v,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*self.n+[(0,1)]*self.n,constraints=cons,callback=cb,options=dict(maxiter=maxiter,ftol=1e-12))
        r=report(opt.x);r['optimizer']=dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit));path.write_text(json.dumps(r,indent=2)+'\n');return r
