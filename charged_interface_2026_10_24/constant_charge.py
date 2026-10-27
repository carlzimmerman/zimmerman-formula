import argparse,json
from pathlib import Path
import numpy as np
from response_charge import ResponseCharge,h
from local_state import Local
from angular_gate import s,Fp

class ConstantCharge(ResponseCharge):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.metric=np.diag(self.mobility_denom)+self.Lmat+self.Ltail
    def energy_grad(self,x,beta=None,C=None):
        E,g=Local.energy_grad(self,x,self.beta,self.C);e,d,_=self.charge(x,False);return E+e,g+d
    def hessian(self,x,beta=None,C=None):return Local.hessian(self,x,self.beta,self.C)+self.charge(x)[2]
    def chemical(self,x):
        q=h(x);u=self.u(q);M=self.m@q;terms=self.a*(u/(1-u)+self.beta*self.C*s(x)*Fp(u))
        mu=np.cumsum(terms[::-1])[::-1]-(1-self.own)*terms+self.tail_mu(M)
        dq=self.Diff@q;root=np.sqrt(dq*dq+self.reg**2);soft=dq*dq/(root+self.reg)
        I=self.charge(x,False)[2];mu-=self.k/I**2*(self.Amid.T@(self.area*Fp(self.Amid@q)*soft))/self.m
        _,g=self.energy_grad(x);return q,mu,g

def checks():
    m=ConstantCharge(6e10,3,64,100,beta=100);x=np.linspace(.8,.2,64);v=np.sin(np.arange(64)+.7);eps=1e-6;E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.cos(np.arange(64)+.2);mu=m.tpotential(x);es=[];eps=1e-6
    for sign in [1,-1]:
        new=old+sign*eps*d;ratio=new/old;m.m=new;m.A=A*ratio;m.Amid=Am*ratio
        xn=2/np.pi*np.arcsin(np.sqrt((old*q+sign*eps*d)/new));es.append(m.energy_grad(xn)[0])
    dm=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1);assert max(dg,dh,dm)<1e-6
    return dict(gradient_error=dg,hessian_error=dh,T_mass_variation_error=dm)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for beta in [100,1000]:
        for k in [100,1000,10000]:
            m=ConstantCharge(6e10,3,128,k,beta=beta)
            for start in [.4,.7]:
                r=m.solve(start);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force','gravity']},flush=True)
