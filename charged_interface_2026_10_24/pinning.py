import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize
from scipy.linalg import eigh,cho_factor,cho_solve
from response_stiffness import Response,PROFILES,h,hp,hpp,law
from model import mb,A0

def moments(m,Rj):
    def vel(r):
        y=mb(r,m.b)/r**2;g=law(y);core=.1*m.b
        f=.95/np.sqrt(1+(r/Rj)**8)
        return f*np.sqrt(r*g)*r/np.sqrt(r*r+core*core)
    r=m.r;v=vel(r);eps=1e-5
    dv=(vel(r*(1+eps))-vel(r*(1-eps)))/(2*eps*r)
    omega=v/r+dv
    radial=np.geomspace(r[0]*.5,max(m.R,m.b)*1e5,12000)
    rho=(1+(radial/m.b)**2)**-2.5
    integrand=rho*(law(mb(radial,m.b)/radial**2)-vel(radial)**2/radial)
    pressure=-cumulative_trapezoid(integrand[::-1],radial[::-1],initial=0)[::-1]
    sig=np.interp(r,radial,pressure/rho)
    grad=-5*r/(r*r+m.b*m.b);Hr=-5*(m.b*m.b-r*r)/(r*r+m.b*m.b)**2;Ht=-5/(r*r+m.b*m.b)
    C=omega**2/(omega**2+sig*(grad**2+np.sqrt(Hr**2+2*Ht**2)))
    assert np.all(sig>0) and np.all((C>=0)&(C<=1))
    return C

class Pin(Response):
    def __init__(self,mass,b,n=128,Rjb=5,epsilon=0,c=.1):
        super().__init__(mass,b,n,30,2)
        self.C=moments(self,Rjb*self.b);self.B=self.C**2/(self.C**2+c*c)
        self.epsilon=epsilon/(A0*self.rm);self.physical_epsilon=epsilon;self.c=c;self.Rjb=Rjb
    def energy_grad(self,x,beta=20,C=None):
        E,g=super().energy_grad(x,beta,self.C)
        return E-self.epsilon*np.dot(self.m*self.B,h(x)),g-self.epsilon*self.m*self.B*hp(x)
    def hessian(self,x,beta=20,C=None):
        return super().hessian(x,beta,self.C)-np.diag(self.epsilon*self.m*self.B*hpp(x))
    def solve(self,start):
        sd=np.sqrt(self.mobility_denom)
        rin=min(5*self.b,.4*self.R);rout=.8*self.R
        x0=np.ones(self.n) if start=='all' else np.where(self.r<=rin,1,np.where(self.r>=rout,0,(1/self.r-1/rout)/(1/rin-1/rout)))
        def fg(v):
            E,g=self.energy_grad(v/sd);return E/self.normalization,g/sd/self.normalization
        opt=minimize(fg,x0*sd,jac=True,method='L-BFGS-B',bounds=list(zip(np.zeros(self.n),sd)),options=dict(maxiter=6000,ftol=1e-14,gtol=1e-10,maxls=40,maxcor=30))
        x=opt.x/sd;q=h(x);E,g=self.energy_grad(x)
        inner=(self.r>=.5*self.b)&(self.r<=rin);outer=self.r>=rout
        gf=(np.cumsum(self.m*(1-q))-(1-self.own)*self.m*(1-q))/self.r**2
        dB=np.gradient(self.B,self.r,edge_order=2)
        source=self.baryon_g+gf-self.epsilon*dB
        valid=bool(np.all(source[inner]>0))
        correction=float(max(abs(np.log10(law(source[inner])/self.g0[inner])))) if valid else None
        return dict(start=start,n=self.n,Rjb=self.Rjb,epsilon=self.physical_epsilon,c=self.c,success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),energy=float(E),qinner=float(np.dot(self.m[inner],q[inner])/sum(self.m[inner])),qouter=float(np.dot(self.m[outer],q[outer])/sum(self.m[outer])),max_speed=float(max(abs(cho_solve(cho_factor(self.metric),g)))),eigenvalue=float(eigh(self.hessian(x),self.metric,subset_by_index=[0,0],eigvals_only=True)[0]),binding_source_positive=valid,binding_only_correction_dex=correction,x=x.tolist(),r=(self.r*self.rm).tolist(),C=self.C.tolist())

def checks():
    m=Pin(6e10,3,n=32,epsilon=1e5);x=np.linspace(.8,.3,32);v=np.sin(np.arange(32)+.7);eps=1e-6
    E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    assert dg<1e-6 and dh<1e-6
    return dict(gradient_error=dg,hessian_error=dh)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=128);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for i in [1,2]:
        _,mass,b,_=PROFILES[i]
        for rj in [2,5]:
            for epsilon,c in [(0,.1),(1e5,.01),(1e5,.1)]:
                m=Pin(mass,b,a.n,rj,epsilon,c)
                for start in ['local','all']:
                    r=m.solve(start);r['profile']=i;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','C']},flush=True)
