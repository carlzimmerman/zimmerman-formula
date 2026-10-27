import argparse,json
from pathlib import Path
import numpy as np
from surface import Surface,PROFILES,h
from angular_gate import Field,hp,hpp,s,F,Fp

class Align(Surface):
    def __init__(self,mass,b,n=128,Rjb=8,eta=3):
        super().__init__(mass,b,n,Rjb,0)
        self.eta=eta;self.Avg=.5*(np.eye(n)[:-1]+np.eye(n)[1:]);self.dc=np.diff(self.C)
    def residual(self,x):
        mid=self.Avg@x
        return self.Diff@x-self.eta*hp(mid)*self.dc,self.Diff-(self.eta*self.dc*hpp(mid))[:,None]*self.Avg
    def energy_grad(self,x,beta=20,C=None):
        E,g=Field.energy_grad(self,x,beta,self.C);diff=np.diff(x);E-=.5*np.dot(self.links,diff**2);g-=self.Lmat@x
        d,J=self.residual(x);u=self.Amid@h(x);weight=self.links*F(u)
        E+=.5*np.dot(weight,d*d);g+=J.T@(weight*d)+hp(x)*(self.Amid.T@(.5*self.links*Fp(u)*d*d))
        M=self.m@h(x);ga,gp,_=self.gamma(M);E+=.5*self.ell2*ga*x[-1]**2
        g+=.5*self.ell2*gp*x[-1]**2*self.m*hp(x);g[-1]+=self.ell2*ga*x[-1]
        return E,g
    def hessian(self,x,beta=20,C=None):
        H=Field.hessian(self,x,beta,self.C)-self.Lmat;d,J=self.residual(x);u=self.Amid@h(x);Ju=self.Amid*hp(x)[None,:]
        H+=Ju.T@((self.links*d*d/(1-u)**3)[:,None]*Ju)
        H+=np.diag(hpp(x)*(self.Amid.T@(.5*self.links*Fp(u)*d*d)))
        cross=Ju.T@((self.links*Fp(u)*d)[:,None]*J);H+=cross+cross.T+J.T@((self.links*F(u))[:,None]*J)
        # h'''=-pi² h'.
        H+=self.Avg.T@((self.eta*self.dc*np.pi**2*hp(self.Avg@x)*self.links*F(u)*d)[:,None]*self.Avg)
        M=self.m@h(x);ga,gp,gpp=self.gamma(M);mh=self.m*hp(x);end=np.zeros(self.n);end[-1]=1
        H+=.5*self.ell2*x[-1]**2*(gpp*np.outer(mh,mh)+gp*np.diag(self.m*hpp(x)))
        H+=self.ell2*gp*x[-1]*(np.outer(mh,end)+np.outer(end,mh));H[-1,-1]+=self.ell2*ga
        return H
    def tpotential(self,x):
        q=h(x);u=self.u(q);M=self.m@q;terms=self.a*(u/(1-u)+20*self.C*s(x)*Fp(u))
        mu=np.cumsum(terms[::-1])[::-1]-(1-self.own)*terms+self.tail_mu(M)
        d,_=self.residual(x);mu+=self.Amid.T@(.5*self.links*Fp(self.Amid@q)*d*d)/self.m
        mu+=.5*self.ell2*self.gamma(M)[1]*x[-1]**2
        _,g=self.energy_grad(x);ratio=np.divide(np.cos(np.pi*x/2),np.pi*np.sin(np.pi*x/2),out=np.zeros_like(x),where=abs(np.sin(np.pi*x/2))>1e-10)
        return q*mu+ratio*g/self.m
    def solve(self,start):
        row=super().solve(start);x=np.array(row['x']);a=-np.gradient(self.tpotential(x),self.r,edge_order=2);res=(a-self.g0)/self.g0;inner=(self.r>=.5*self.b)&(self.r<=min(5*self.b,.4*self.R))
        row.update(eta=self.eta,T_force_max_relative=float(max(abs(res[inner]))),T_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),force=a.tolist());return row

def checks():
    m=Align(6e10,3,64,5,3);x=np.linspace(.8,.2,64);v=np.sin(np.arange(64)+.7);eps=1e-6;E,g=m.energy_grad(x);ep,gp=m.energy_grad(x+eps*v);em,gm=m.energy_grad(x-eps*v);H=m.hessian(x)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1);dh=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.cos(np.arange(64)+.2);mu=m.tpotential(x);es=[];eps=1e-5
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
            for eta in [1,3,10]:
                m=Align(mass,b,128,rj,eta)
                for start in ['front','all']:
                    r=m.solve(start);r['profile']=i;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force','gravity','kappa']},flush=True)
