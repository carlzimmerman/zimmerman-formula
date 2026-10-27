"""LD-3: continuation of the near-law mobile-density cell, scaled SLSQP."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from constrained import Constrained
from joint import Joint,RESERVOIR

class Warm(Constrained):
    def __init__(self,*args,**kwargs):Joint.__init__(self,*args,**kwargs)
    def solve_scaled(self,v):
        def fg(a):
            E,g=self.direct(a);return E/100,g/100
        constraints=[dict(type='eq',fun=lambda a:sum(a[:self.n])-RESERVOIR,jac=lambda a:np.r_[np.ones(self.n),np.zeros(self.n)]),dict(type='ineq',fun=self.cap,jac=self.capjac)]
        opt=minimize(fg,v,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*self.n+[(0,1)]*self.n,constraints=constraints,options=dict(maxiter=5000,ftol=1e-13))
        a=opt.x;r=self.report(np.r_[np.log(a[:self.n]),a[self.n:]]);E,g=self.direct(a);active=a[:self.n]>1e-7;lam=np.median(g[:self.n][active]);mr=g[:self.n]-lam;mr=np.where((~active)&(mr>0),0,mr)
        r.update(density_KKT_max=float(max(abs(mr))),mass_constraint_error=float(abs(sum(a[:self.n])-RESERVOIR)),cap_slack_min=float(min(self.cap(a))),optimizer=dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit)))
        return r

def transfer(m,old,shift=0):
    # Integrate old piecewise-constant cell mass into new cells; no law prior.
    ro=np.array(old['r'])/m.rm;edges=np.r_[0,(ro[:-1]+ro[1:])/2,old['R_kpc']/m.rm]
    new=np.linspace(0,m.R,m.n+1);cum=np.interp(new,edges,np.r_[0,np.cumsum(old['mass'])]);mass=np.maximum(np.diff(cum),1e-12);mass*=RESERVOIR/sum(mass)
    x=np.interp(m.r.numpy()*m.rm+shift,old['r'],old['v'][old['n']:]);return np.r_[mass,x]

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();base=json.loads(Path(__file__).with_name('run_joint').joinpath('results.json').read_text())['runs'][-1];out=dict(runs=[])
    for n,domain in [(96,2),(192,2),(192,4)]:
        m=Warm(n=n,domain=domain,beta=1000,k=120,tau=1,K=3);r=m.solve_scaled(transfer(m,base));out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
        if r['max_u']<.97 and r['mass_constraint_error']<1e-6:base=r
