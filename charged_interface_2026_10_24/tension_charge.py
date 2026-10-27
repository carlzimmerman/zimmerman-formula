"""CI-6: independent positive area tension plus response-localized charge."""
import argparse,json
from pathlib import Path
import numpy as np
from response_charge import ResponseCharge,h
from angular_gate import hp,hpp

class TensionCharge(ResponseCharge):
    def __init__(self,*args,tau=1,**kwargs):
        super().__init__(*args,**kwargs);self.tau=tau
    def tension(self,x):
        dq=self.Diff@h(x);root=np.sqrt(dq*dq+self.reg**2)
        J=float(self.area@(dq*dq/(root+self.reg)))
        v=self.Diff.T@(self.area*dq/root);D=self.Diff*hp(x)[None,:]
        H=D.T@((self.area*self.reg**2/root**3)[:,None]*D)+np.diag(hpp(x)*v)
        return self.tau*J,self.tau*hp(x)*v,self.tau*H
    def energy_grad(self,x,beta=None,C=None):
        E,g=super().energy_grad(x,beta,C);e,d,_=self.tension(x);return E+e,g+d
    def hessian(self,x,beta=None,C=None):return super().hessian(x,beta,C)+self.tension(x)[2]
    def solve(self,start):
        r=super().solve(start);r['tau']=self.tau;return r

def checks():
    m=TensionCharge(6e10,3,64,100,beta=100,tau=10);x=np.linspace(.8,.2,64);v=np.sin(np.arange(64)+.7);eps=1e-6
    E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.cos(np.arange(64)+.2);errors={}
    for species,mu in [('T',m.tpotential(x)),('F',m.fpotential(x))]:
        es=[]
        for sign in [1,-1]:
            new=old+sign*eps*d;ratio=new/old;m.m=new;m.A=A*ratio;m.Amid=Am*ratio
            xn=2/np.pi*np.arcsin(np.sqrt((old*q+(sign*eps*d if species=='T' else 0))/new));es.append(m.energy_grad(xn)[0])
        m.m=old;m.A=A;m.Amid=Am
        errors[species+'_mass_variation_error']=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1)
    assert max(dg,dh,*errors.values())<1e-6
    return dict(gradient_error=dg,hessian_error=dh,**errors)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for beta in [20,1000]:
        for k in [10,100,1000]:
            for tau in [.1,1,10]:
                m=TensionCharge(6e10,3,128,k,beta=beta,tau=tau)
                r=m.solve(.5);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
                print({k:v for k,v in r.items() if k not in ['x','r','force','gravity']},flush=True)
