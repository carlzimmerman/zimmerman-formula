"""New response-weighted local phase energy, including all mixed derivatives."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor,cho_solve,eigh
from scipy.integrate import solve_ivp
from local_state import Local,PROFILES,law
from angular_gate import Field,h,hp,hpp,F,Fp

class Response(Local):
    def __init__(self,mass,b,n=128,length_kpc=30,environment=2):
        super().__init__(mass,b,n,length_kpc)
        self.Amid=.5*(self.A[:-1]+self.A[1:])
        self.Diff=np.diff(np.eye(n),axis=0)
        self.tail_a=( (environment*self.R)**3-self.r[-1]**3)/3
        self.bt=environment*self.R-self.r[-1]
        self.ell2=(length_kpc/self.rm)**2
        self.environment=environment
        weights=self.links*F(self.Amid@np.ones(n))
        Mref=self.Diff.T@(weights[:,None]*self.Diff)
        Mref[-1,-1]+=self.ell2*self.gamma(sum(self.m))[0]
        self.metric=np.diag(self.mobility_denom)+Mref

    def gamma(self,M):
        d=self.tail_a-self.bt*M
        if d<=0:raise ValueError('tail outside saturation domain')
        return M*M/d,M*(2*self.tail_a-self.bt*M)/d**2,2*self.tail_a*self.tail_a/d**3

    def energy_grad(self,x,beta,C):
        E,g=Field.energy_grad(self,x,beta,C)
        diff=np.diff(x)
        E-=.5*np.dot(self.links,diff*diff);g-=self.Lmat@x
        u=self.Amid@h(x);gradF=Fp(u);weights=self.links*F(u)
        E+=.5*np.dot(weights,diff*diff)
        g+=hp(x)*(self.Amid.T@(.5*self.links*gradF*diff*diff))
        g+=self.Diff.T@(weights*diff)
        M=float(np.dot(self.m,h(x)));ga,gp,_=self.gamma(M)
        E+=.5*self.ell2*ga*x[-1]**2
        g+=.5*self.ell2*gp*x[-1]**2*self.m*hp(x)
        g[-1]+=self.ell2*ga*x[-1]
        return E,g

    def hessian(self,x,beta,C):
        H=Field.hessian(self,x,beta,C)-self.Lmat
        diff=np.diff(x);u=self.Amid@h(x);J=self.Amid*hp(x)[None,:]
        c=.5*self.links*Fp(u)*diff**2
        H+=J.T@((self.links*diff**2/(1-u)**3)[:,None]*J)
        H+=np.diag(hpp(x)*(self.Amid.T@c))
        cross=J.T@((self.links*Fp(u)*diff)[:,None]*self.Diff)
        H+=cross+cross.T+self.Diff.T@((self.links*F(u))[:,None]*self.Diff)
        M=float(np.dot(self.m,h(x)));ga,gp,gpp=self.gamma(M)
        mh=self.m*hp(x);end=np.zeros(self.n);end[-1]=1
        H+=.5*self.ell2*x[-1]**2*(gpp*np.outer(mh,mh)+gp*np.diag(self.m*hpp(x)))
        H+=self.ell2*gp*x[-1]*(np.outer(mh,end)+np.outer(end,mh))
        H[-1,-1]+=self.ell2*ga
        return H

    def evolve(self,duration=100):
        C=self.kinematics(.95)['C'];rin=min(5*self.b,.4*self.R);rout=.8*self.R
        x0=np.where(self.r<=rin,1,np.where(self.r>=rout,0,(1/self.r-1/rout)/(1/rin-1/rout)))
        E0,_=self.energy_grad(x0,20,C);factor=cho_factor(self.metric)
        def rhs(t,y):
            _,g=self.energy_grad(y[:-1],20,C);dx=-cho_solve(factor,g)
            return np.r_[dx,np.dot(g,-dx)/self.normalization]
        def jac(t,y):
            _,g=self.energy_grad(y[:-1],20,C);H=self.hessian(y[:-1],20,C)
            A=np.zeros((self.n+1,self.n+1));A[:-1,:-1]=-cho_solve(factor,H)
            A[-1,:-1]=2*cho_solve(factor,g)@H/self.normalization
            return A
        ts=np.linspace(0,duration,51);sol=solve_ivp(rhs,(0,duration),np.r_[x0,0],method='BDF',jac=jac,
            rtol=1e-8,atol=1e-10,t_eval=ts)
        if not sol.success:raise RuntimeError(sol.message)
        inner=(self.r>=.5*self.b)&(self.r<=rin);outer=self.r>=rout;hist=[];errors=[]
        for k,t in enumerate(ts):
            x=sol.y[:-1,k];q=h(x);mF=np.cumsum(self.m*(1-q))-(1-self.own)*self.m*(1-q)
            corr=np.log10(law(self.baryon_g+mF/self.r**2)/self.g0)
            E,g=self.energy_grad(x,20,C)
            errors.append(abs(E+sol.y[-1,k]*self.normalization-E0)/max(E0,1e-30))
            hist.append(dict(t=float(t),q_inner=float(np.dot(self.m[inner],q[inner])/sum(self.m[inner])),
                q_outer=float(np.dot(self.m[outer],q[outer])/sum(self.m[outer])),correction_max_dex=float(max(abs(corr[inner]))),energy=float(E)))
        x=sol.y[:-1,-1];_,g=self.energy_grad(x,20,C)
        return dict(n=self.n,environment=self.environment,ell_kpc=self.length_kpc,history=hist,final=hist[-1],
            initial_energy=E0,max_energy_error=max(errors),max_phase_speed=float(max(abs(cho_solve(factor,g)))),
            lowest_eigenvalue=float(eigh(self.hessian(x,20,C),self.metric,subset_by_index=[0,0],eigvals_only=True)[0]),
            q=h(x).tolist(),x=x.tolist(),r_kpc=(self.r*self.rm).tolist())

def checks():
    m=Response(6e10,3,n=32);C=m.kinematics(.95)['C'];x=.3+.5*np.linspace(1,0,m.n)
    E,g=m.energy_grad(x,20,C);v=np.sin(np.arange(m.n)+.7);eps=1e-6
    ep,gp=m.energy_grad(x+eps*v,20,C);em,gm=m.energy_grad(x-eps*v,20,C)
    dg=abs((ep-em)/(2*eps)-g@v)/max(abs(g@v),1)
    dh=np.linalg.norm((gp-gm)/(2*eps)-m.hessian(x,20,C)@v)/max(np.linalg.norm(m.hessian(x,20,C)@v),1)
    assert dg<1e-6 and dh<1e-6
    return dict(gradient_error=dg,hessian_error=dh)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=128)
    args=ap.parse_args();out=dict(checks=checks(),runs=[]);p=Path(args.output)
    for i in [1,2]:
        _,mass,b,_=PROFILES[i]
        for env in [2,4]:
            m=Response(mass,b,args.n,environment=env);r=m.evolve();r['profile']=i;out['runs'].append(r)
            p.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
            print({k:v for k,v in r.items() if k not in ['history','q','x','r_kpc']},flush=True)
