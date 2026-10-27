"""LD-2: exact saturation inequality and direct density simplex."""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from scipy.optimize import minimize
from joint import Joint,T,RESERVOIR,outer

class Constrained(Joint):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Quadratic radial mesh resolves core independently of outer extent.
        edges=self.R*np.linspace(0,1,self.n+1)**2;r=(edges[1:]+edges[:-1])/2
        self.r=T(r);self.vol=T(np.diff(edges**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2)
        self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
    def direct(self,v):
        a=T(v).requires_grad_(True);E=self.energy(torch.log(a[:self.n]),a[self.n:]);g=torch.autograd.grad(E,a)[0]
        return float(E.detach()),g.detach().numpy()
    def cap(self,v):
        m=v[:self.n];x=v[self.n:];q=np.sin(np.pi*x/2)**2
        return .97-self.A.numpy()@(m*q)
    def capjac(self,v):
        m=v[:self.n];x=v[self.n:];q=np.sin(np.pi*x/2)**2;hp=np.pi/2*np.sin(np.pi*x)
        return -np.c_[self.A.numpy()*q,self.A.numpy()*(m*hp)]
    def start(self,scale=4,front=.4):
        v=self.initial(scale,front);m=np.exp(v[:self.n]-max(v[:self.n]));m*=RESERVOIR/sum(m)
        return np.r_[m,v[self.n:]]
    def solve_direct(self,v):
        cons=[dict(type='eq',fun=lambda a:sum(a[:self.n])-RESERVOIR,jac=lambda a:np.r_[np.ones(self.n),np.zeros(self.n)]),dict(type='ineq',fun=self.cap,jac=self.capjac)]
        opt=minimize(self.direct,v,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*self.n+[(0,1)]*self.n,constraints=cons,options=dict(maxiter=2500,ftol=1e-10))
        val=opt.x;r=self.report(np.r_[np.log(val[:self.n]),val[self.n:]])
        E,g=self.direct(val);active=val[:self.n]>1e-7;lam=float(np.median(g[:self.n][active]));mr=g[:self.n]-lam;mr=np.where((~active)&(mr>0),0,mr)
        r.update(density_KKT_max=float(max(abs(mr))),mass_constraint_error=float(abs(sum(val[:self.n])-RESERVOIR)),cap_slack_min=float(min(self.cap(val))),optimizer=dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit)))
        return r

def checks():
    m=Constrained(n=32);v=m.start();v[m.n:]=np.linspace(.8,.1,m.n);v[:m.n]*=.5;v[:m.n]+=RESERVOIR/(2*m.n)
    d=np.cos(np.arange(2*m.n)+.5);d[:m.n]*=1e-5;eps=1e-6;E,g=m.direct(v)
    fd=(m.direct(v+eps*d)[0]-m.direct(v-eps*d)[0])/(2*eps)
    er=abs(fd-g@d)/max(abs(fd),1);ce=np.max(abs((m.cap(v+eps*d)-m.cap(v-eps*d))/(2*eps)-m.capjac(v)@d));assert er<1e-6 and ce<1e-6
    return dict(direct_gradient_error=er,cap_jacobian_error=float(ce))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for beta,k,tau,K in [(20,120,1,.3),(20,120,1,3),(1000,100,.1,3),(1000,120,1,3)]:
        m=Constrained(n=64,beta=beta,k=k,tau=tau,K=K);r=m.solve_direct(m.start());out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
