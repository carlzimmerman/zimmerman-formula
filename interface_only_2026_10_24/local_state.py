"""Spatially resolved phase with a free exterior; fixed-density gate only."""
import argparse,json,sys,time
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor,cho_solve,eigh
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from angular_gate import Field,h,hp,PROFILES,law

class Local(Field):
    def __init__(self,mass,b,n=128,length_kpc=30):
        super().__init__(mass,b,n,length_kpc,grid='uniform')
        self.tail_link=(length_kpc/self.rm)**2*self.r[-1]
        self.Ltail=np.zeros_like(self.Lmat);self.Ltail[-1,-1]=self.tail_link

    def energy_grad(self,x,beta,C):
        E,g=super().energy_grad(x,beta,C)
        E+=.5*self.tail_link*x[-1]**2;g[-1]+=self.tail_link*x[-1]
        return E,g

    def hessian(self,x,beta,C):
        return super().hessian(x,beta,C)+self.Ltail

    def run(self,f=.95,beta=20,duration=100):
        C=self.kinematics(f)['C'];Rin=min(5*self.b,.4*self.R);Rout=.8*self.R
        x0=np.where(self.r<=Rin,1.,np.where(self.r>=Rout,0.,
                      (1/self.r-1/Rout)/(1/Rin-1/Rout)))
        E0,_=self.energy_grad(x0,beta,C)
        M=np.diag(self.mobility_denom)+self.Lmat+self.Ltail
        fact=cho_factor(M)
        def rhs(t,y):
            _,g=self.energy_grad(y[:-1],beta,C);dx=-cho_solve(fact,g)
            return np.r_[dx,np.dot(g,-dx)/self.normalization]
        def jac(t,y):
            _,g=self.energy_grad(y[:-1],beta,C);H=self.hessian(y[:-1],beta,C)
            J=np.zeros((self.n+1,self.n+1));J[:-1,:-1]=-cho_solve(fact,H)
            J[-1,:-1]=2*cho_solve(fact,g)@H/self.normalization
            return J
        times=np.linspace(0,duration,51)
        sol=solve_ivp(rhs,(0,duration),np.r_[x0,0.],method='BDF',jac=jac,
            rtol=1e-8,atol=1e-10,t_eval=times)
        if not sol.success:raise RuntimeError(sol.message)
        inner=(self.r>=.5*self.b)&(self.r<=Rin);outer=self.r>=Rout
        if not np.any(inner):raise ValueError('no supply-admissible inner test region')
        history=[];balance=[]
        for j,t in enumerate(times):
            x=sol.y[:-1,j];q=h(x)
            mF=np.cumsum(self.m*(1-q))-(1-self.own)*self.m*(1-q)
            gf=mF/self.r**2
            corr=np.log10(law(self.baryon_g+gf)/self.g0)
            E,g=self.energy_grad(x,beta,C)
            balance.append(abs(E+sol.y[-1,j]*self.normalization-E0)/max(E0,1e-30))
            history.append(dict(t=float(t),q_inner=float(np.dot(self.m[inner],q[inner])/sum(self.m[inner])),
                q_outer=float(np.dot(self.m[outer],q[outer])/sum(self.m[outer])),
                correction_max_dex=float(max(abs(corr[inner]))),energy=float(E)))
        final=history[-1];x=sol.y[:-1,-1]
        ev=float(eigh(self.hessian(x,beta,C),M,subset_by_index=[0,0],eigvals_only=True)[0])
        _,g=self.energy_grad(x,beta,C);dx=-cho_solve(fact,g)
        return dict(status='completed',n=self.n,ell_kpc=self.length_kpc,Rin_kpc=Rin*self.rm,Rout_kpc=Rout*self.rm,
            initial_energy=E0,final=final,history=history,q=h(x).tolist(),x=x.tolist(),r_kpc=(self.r*self.rm).tolist(),
            max_energy_error=max(balance),endpoint_lowest_eigenvalue=ev,max_phase_speed=float(max(abs(dx))),
            preservation_pass=bool(final['q_inner']>=.95 and final['q_outer']<=.05 and final['correction_max_dex']<=.05))

def checks():
    m=Local(6e10,3,n=32,length_kpc=30);C=m.kinematics(.95)['C']
    x=.2+.5*np.linspace(1,0,m.n);E,g=m.energy_grad(x,20,C)
    v=np.cos(np.arange(m.n));eps=1e-6
    ep,gp=m.energy_grad(x+eps*v,20,C);em,gm=m.energy_grad(x-eps*v,20,C)
    grad=abs((ep-em)/(2*eps)-np.dot(g,v))/max(abs(np.dot(g,v)),1)
    H=m.hessian(x,20,C);hess=np.linalg.norm((gp-gm)/(2*eps)-H@v)/max(np.linalg.norm(H@v),1)
    assert grad<1e-6 and hess<1e-6
    return dict(gradient_directional_relative=grad,hessian_directional_relative=hess)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=128)
    ap.add_argument('--ells',default='.1,1,3,10,30');ap.add_argument('--profiles',default='1,2');args=ap.parse_args()
    out=dict(checks=checks(),runs=[]);path=Path(args.output)
    for i in map(int,args.profiles.split(',')):
        _,mass,b,_=PROFILES[i]
        for ell in map(float,args.ells.split(',')):
            start=time.monotonic();m=Local(mass,b,args.n,ell)
            row=m.run();row.update(profile=i,elapsed=time.monotonic()-start);out['runs'].append(row)
            path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
            print(json.dumps({k:v for k,v in row.items() if k not in ['history','q','x','r_kpc']}),flush=True)
