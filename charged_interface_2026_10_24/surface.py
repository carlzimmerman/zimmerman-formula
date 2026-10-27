import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh,cho_factor,cho_solve
from response_stiffness import Response,PROFILES,h
from pinning import moments
from forces import potential
from recovery import tpotential

class Surface(Response):
    def __init__(self,mass,b,n=128,Rjb=8,strength=100):
        super().__init__(mass,b,n,30,2)
        self.Rjb=Rjb;self.strength=strength;self.C=moments(self,Rjb*self.b)
        self.epsilon=0.;self.B=np.zeros(n);self.c=0.
        r=self.r;grad=-5*r/(r*r+self.b*self.b);Hr=-5*(self.b*self.b-r*r)/(r*r+self.b*self.b)**2;Ht=-5/(r*r+self.b*self.b)
        invL2=grad**2+np.sqrt(Hr**2+2*Ht**2)
        # Face gradient and density length: both converge under refinement.
        self.v2=np.diff(self.C)**2/np.diff(r)**2/(.5*(invL2[:-1]+invL2[1:]))
        self.kappa=1/(1+strength*self.v2)
        self.links*=self.kappa
        self.Lmat=self.Diff.T@(self.links[:,None]*self.Diff)
        weights=self.links*(self.Amid@np.ones(n))**2/(1-self.Amid@np.ones(n))
        self.metric=np.diag(self.mobility_denom)+self.Diff.T@(weights[:,None]*self.Diff)
        self.metric[-1,-1]+=self.ell2*self.gamma(sum(self.m))[0]
    def energy_grad(self,x,beta=20,C=None):return super().energy_grad(x,beta,self.C)
    def hessian(self,x,beta=20,C=None):return super().hessian(x,beta,self.C)
    def solve(self,start):
        sd=np.sqrt(self.mobility_denom)
        x0=np.ones(self.n) if start=='all' else .5*(1-np.tanh((self.r-self.Rjb*self.b)/(.1*self.Rjb*self.b)))
        def fg(v):
            E,g=self.energy_grad(v/sd);return E/self.normalization,g/sd/self.normalization
        opt=minimize(fg,x0*sd,jac=True,method='L-BFGS-B',bounds=list(zip(np.zeros(self.n),sd)),options=dict(maxiter=6000,ftol=1e-14,gtol=1e-10,maxls=40,maxcor=30))
        x=opt.x/sd;q=h(x);E,g=self.energy_grad(x);inner=(self.r>=.5*self.b)&(self.r<=min(5*self.b,.4*self.R));outer=self.r>=.8*self.R
        a=-np.gradient(tpotential(self,x),self.r,edge_order=2);res=(a-self.g0)/self.g0
        return dict(start=start,n=self.n,Rjb=self.Rjb,strength=self.strength,success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),energy=float(E),qinner=float(np.dot(self.m[inner],q[inner])/sum(self.m[inner])),qouter=float(np.dot(self.m[outer],q[outer])/sum(self.m[outer])),qinner_min=float(min(q[inner])),max_speed=float(max(abs(cho_solve(cho_factor(self.metric),g)))),eigenvalue=float(eigh(self.hessian(x),self.metric,subset_by_index=[0,0],eigvals_only=True)[0]),T_force_max_relative=float(max(abs(res[inner]))),T_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),x=x.tolist(),r=(self.r*self.rm).tolist(),force=a.tolist(),gravity=self.g0.tolist(),kappa=self.kappa.tolist())

def checks():
    m=Surface(6e10,3,n=64,strength=100);x=np.linspace(.8,.2,64);v=np.sin(np.arange(64)+.7);eps=1e-6;E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.cos(np.arange(64)+.2);mu=tpotential(m,x);es=[];eps=1e-5
    for sign in [1,-1]:
        new=old+sign*eps*d;ratio=new/old;m.m=new;m.A=A*ratio;m.Amid=Am*ratio
        xn=2/np.pi*np.arcsin(np.sqrt((old*q+sign*eps*d)/new));es.append(m.energy_grad(xn)[0])
    dm=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1)
    assert max(dg,dh,dm)<1e-6
    return dict(gradient_error=dg,hessian_error=dh,T_mass_variation_error=dm)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for i in [1,2]:
        _,mass,b,_=PROFILES[i]
        for rj in [1,5,8]:
            for strength in [0,100,10000]:
                m=Surface(mass,b,128,rj,strength)
                for start in ['front','all']:
                    r=m.solve(start);r['profile']=i;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force','gravity','kappa']},flush=True)
