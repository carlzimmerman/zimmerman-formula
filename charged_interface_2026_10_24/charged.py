import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh,cho_factor,cho_solve
from surface import Surface,PROFILES,h
from angular_gate import hp,hpp
from recovery import tpotential

class Charged(Surface):
    def __init__(self,mass,b,n=128,k=1,delta=1e-5):
        super().__init__(mass,b,n,8,0)
        self.C=self.kinematics(.95)['C'];self.k=k;self.delta=delta;self.eta=0
        self.area=((self.r[:-1]+self.r[1:])/2)**2;self.reg=delta*np.diff(self.r)
    def charge(self,x,hessian=True):
        dq=self.Diff@h(x);root=np.sqrt(dq*dq+self.reg**2)
        I=float(np.dot(self.area,dq*dq/(root+self.reg)))
        if I<=1e-30:raise ValueError('nonzero charge requires an interface')
        a=self.Diff.T@(self.area*dq/root);Ix=hp(x)*a
        E=self.k/I;g=-self.k/I**2*Ix
        if not hessian:return E,g,I
        J=self.Diff*hp(x)[None,:]
        IH=J.T@((self.area*self.reg**2/root**3)[:,None]*J)+np.diag(hpp(x)*a)
        H=2*self.k/I**3*np.outer(Ix,Ix)-self.k/I**2*IH
        return E,g,H,I
    def energy_grad(self,x,beta=20,C=None):
        E,g=super().energy_grad(x,beta,C);e,d,_=self.charge(x,False);return E+e,g+d
    def hessian(self,x,beta=20,C=None):return super().hessian(x,beta,C)+self.charge(x)[2]
    def tpotential(self,x):return tpotential(self,x)
    def solve(self,start):
        sd=np.sqrt(self.mobility_denom);center=start*self.R
        x0=.5*(1-np.tanh((self.r-center)/(.05*self.R)))
        def fg(v):
            try: E,g=self.energy_grad(v/sd)
            except ValueError as exc:
                if "nonzero charge" not in str(exc): raise
                return np.inf,np.zeros_like(v)
            return E/self.normalization,g/sd/self.normalization
        opt=minimize(fg,x0*sd,jac=True,method='L-BFGS-B',bounds=list(zip(np.zeros(self.n),sd)),options=dict(maxiter=8000,ftol=1e-14,gtol=1e-10,maxls=50,maxcor=30))
        x=opt.x/sd;q=h(x);E,g=self.energy_grad(x);inner=(self.r>=.5*self.b)&(self.r<=min(5*self.b,.4*self.R));outer=self.r>=.8*self.R
        force=-np.gradient(self.tpotential(x),self.r,edge_order=2);res=(force-self.g0)/self.g0
        crossings=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0]
        return dict(start_fraction=start,n=self.n,k=self.k,delta=self.delta,success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),energy=float(E),charge_capacity=self.charge(x,False)[2],qinner=float(np.dot(self.m[inner],q[inner])/sum(self.m[inner])),qouter=float(np.dot(self.m[outer],q[outer])/sum(self.m[outer])),qinner_min=float(min(q[inner])),max_speed=float(max(abs(cho_solve(cho_factor(self.metric),g)))),eigenvalue=float(eigh(self.hessian(x),self.metric,subset_by_index=[0,0],eigvals_only=True)[0]),T_force_max_relative=float(max(abs(res[inner]))),T_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),crossings_kpc=(self.r[crossings]*self.rm).tolist(),x=x.tolist(),r=(self.r*self.rm).tolist(),force=force.tolist(),gravity=self.g0.tolist())

def checks():
    m=Charged(6e10,3,64,1);x=np.linspace(.8,.2,64);v=np.sin(np.arange(64)+.7);eps=1e-6;E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.cos(np.arange(64)+.2);mu=m.tpotential(x);es=[];eps=1e-6
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
        for k in [.1,1,10,100]:
            m=Charged(mass,b,128,k)
            for start in [.4,.7]:
                r=m.solve(start);r['profile']=i;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force','gravity']},flush=True)
