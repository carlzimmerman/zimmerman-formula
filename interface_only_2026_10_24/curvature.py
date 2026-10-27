import argparse,json
from pathlib import Path
import numpy as np
from surface import Surface,PROFILES,h
from angular_gate import hp,hpp
from recovery import tpotential

class Curvature(Surface):
    def __init__(self,mass,b,n=128,ell4=6,delta=1e-6):
        super().__init__(mass,b,n,8,0)
        self.C=self.kinematics(.95)['C'];self.ell4=ell4;self.delta=delta
        self.cw=16*(ell4/self.rm)**5/((self.r[:-1]+self.r[1:])/2)**2
        self.reg=delta*np.diff(self.r)
    def curv(self,x):
        dq=self.Diff@h(x);root=np.sqrt(dq*dq+self.reg**2)
        a=self.Diff.T@(self.cw*dq/root);J=self.Diff*hp(x)[None,:]
        E=float(np.dot(self.cw,dq*dq/(root+self.reg)))
        return E,hp(x)*a,J.T@((self.cw*self.reg**2/root**3)[:,None]*J)+np.diag(hpp(x)*a)
    def energy_grad(self,x,beta=20,C=None):
        E,g=super().energy_grad(x,beta,C);e,d,_=self.curv(x);return E+e,g+d
    def hessian(self,x,beta=20,C=None):return super().hessian(x,beta,C)+self.curv(x)[2]
    def solve(self,start):
        row=super().solve(start);row.update(ell4=self.ell4,delta=self.delta);return row

def checks():
    m=Curvature(6e10,3,64,6);x=np.linspace(.8,.2,64);v=np.sin(np.arange(64)+.7);eps=1e-7;E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.cos(np.arange(64)+.2);mu=tpotential(m,x);es=[];eps=1e-6
    for sign in [1,-1]:
        new=old+sign*eps*d;ratio=new/old;m.m=new;m.A=A*ratio;m.Amid=Am*ratio
        xn=2/np.pi*np.arcsin(np.sqrt((old*q+sign*eps*d)/new));es.append(m.energy_grad(xn)[0])
    dm=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1)
    assert max(dg,dh,dm)<1e-5
    return dict(gradient_error=dg,hessian_error=dh,T_mass_variation_error=dm)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for i in [1,2]:
        _,mass,b,_=PROFILES[i]
        for ell4 in [3,6,10]:
            m=Curvature(mass,b,128,ell4)
            for start in ['front','all']:
                r=m.solve(start);r['profile']=i;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force','gravity','kappa']},flush=True)
