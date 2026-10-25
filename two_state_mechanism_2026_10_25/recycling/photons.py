"""Conservative frequency-resolved photons and 23 bound molecular states."""
import argparse,json,sys,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import bmat,csc_matrix,diags
from numpy.polynomial.legendre import leggauss
PREV=Path(__file__).resolve().parent.parent/'nonequilibrium'
sys.path.insert(0,str(PREV))
from kinetics_v3 import atomic_shape,CTH,environment,PROFILES


def escape(tau):
    """Gamma_escape=(c/L) f(tau), and analytic df/dtau."""
    tau=np.maximum(np.asarray(tau),0.);f=np.empty_like(tau);df=np.empty_like(tau)
    tiny=tau<1e-5;f[tiny]=4/3-13/45*tau[tiny];df[tiny]=-13/45
    mid=(tau>=1e-5)&(tau<.2);t=tau[mid];D=np.zeros_like(t);Dp=np.zeros_like(t)
    for n in range(1,13):
        moment=3*2.**n/((n+1)*(n+3));coef=(-1)**(n+1)*moment/math.factorial(n)
        D+=coef*t**n;Dp+=n*coef*t**(n-1)
    f[mid]=t/D-t;df[mid]=(D-t*Dp)/D**2-1
    big=tau>=.2;t=tau[big];ex=np.exp(-2*t)
    beta=.75/t*(1-.5/t**2+(1/t+.5/t**2)*ex)
    bp=.75*(-1/t**2+1.5/t**4+ex*(-2/t**2-3/t**3-1.5/t**4))
    f[big]=t*beta/(1-beta);df[big]=beta/(1-beta)+t*bp/(1-beta)**2
    return f,df

class Radiation:
    def __init__(self,order=3,decades=1):
        d=json.loads((PREV/'run_refine/results.json').read_text())
        self.D=np.array([r['D'] for r in d['levels']]);self.deg=np.r_[1,[r['weight'] for r in d['levels']]]
        self.B=np.r_[.5,self.D];self.mu=np.r_[1,np.full(len(self.D),100*101/201)]
        self.nb=len(self.D);self.nm=self.nb+2
        offsets=np.geomspace(1e-10,2.,int(11*decades)+1)
        edges=np.unique(np.r_[0.,self.B,np.concatenate([b+offsets for b in self.B]),2.6])
        edges=edges[edges<=2.6];g,w=leggauss(order)
        self.omega=((edges[:-1,None]+edges[1:,None])/2+(edges[1:,None]-edges[:-1,None])*g/2).ravel()
        self.weights=((edges[1:,None]-edges[:-1,None])*w/2).ravel()
        self.G=self.omega**2/np.pi**2*self.weights;self.nq=len(self.G)
        sigA=np.where(self.omega>=.5,CTH*atomic_shape(np.maximum(2*self.omega-1,0)),0.)
        self.sig=np.vstack([sigA]+[4*np.pi**2/3*self.omega*np.interp(self.omega-D,d['energies'],s,left=0,right=0) for D,s in zip(self.D,d['strength'])])
        self.E=np.maximum(self.omega[None,:]-self.B[:,None],0.)
        self.St=np.zeros((self.nb+1,self.nb+1));self.St[0,0]=1;self.St[0,1:]=-1;self.St[1:,1:]=np.eye(self.nb)
    def coefficients(self,T):
        return self.sig*self.G[None,:]*(self.deg*(2*np.pi/(self.mu*T))**1.5)[:,None]*np.exp(-self.E/T)
    def system(self,alpha,mass,Mb,b,closed=False):
        n,Ti,L,age=environment(alpha,mass,Mb,b)
        nm=self.nm;nq=self.nq;nb=self.nb
        def evaluate(y,jac=False):
            a=y[0];ts=y[1:nb+1];x=1-a-2*sum(ts);c=1-a-sum(ts)
            T=max(y[nm-1]/(1.5*(1+x)),1e-12)
            targets=np.r_[a,ts];prod=np.r_[x*c,np.full(nb,a*x)]
            photons=y[nm:nm+nq];F=n*photons/(alpha**3*self.G)
            H=age*n*alpha**3*self.coefficients(T)
            A=H*prod[:,None];BB=A*n/(alpha**3*self.G)[None,:]-age*n*targets[:,None]*self.sig
            events=A+BB*photons[None,:]
            tau=alpha*n*L*(targets@self.sig);ff,fp=escape(tau)
            esc=np.zeros(nq) if closed else age/(alpha*L)*ff
            flux=esc*photons
            out=np.r_[self.St@events.sum(axis=1),-np.sum(self.E*events),events.sum(axis=0)-flux,np.dot(self.omega,flux)]
            if not jac:return out
            Jmm=np.zeros((nm,nm));Jpm=np.zeros((nq,nm));Jqm=np.zeros((1,nm))
            temp=H*prod[:,None]*(1+F)[None,:]*(-1.5/T+self.E/T**2)
            for j in range(nm):
                if j==0:
                    dp=np.r_[-x-c,np.full(nb,x-a)];dT=T/(1+x)
                elif j<nm-1:
                    dp=np.r_[-2*c-x,np.full(nb,-2*a)];dT=2*T/(1+x)
                else:dp=np.zeros(nb+1);dT=1/(1.5*(1+x))
                dr=temp*dT+H*dp[:,None]*(1+F)[None,:]
                des=np.zeros(nq)
                if j<nm-1:
                    dr[j]-=age*n*self.sig[j]*photons
                    if not closed:des=age*n*fp*self.sig[j]
                Jmm[:-1,j]=self.St@dr.sum(axis=1);Jmm[-1,j]=-np.sum(self.E*dr)
                Jpm[:,j]=dr.sum(axis=0)-des*photons
                Jqm[0,j]=np.dot(self.omega,des*photons)
            Jmp=np.vstack([self.St@BB,-np.sum(self.E*BB,axis=0)])
            return bmat([[csc_matrix(Jmm),csc_matrix(Jmp),None],[csc_matrix(Jpm),diags(BB.sum(axis=0)-esc),None],[csc_matrix(Jqm),csc_matrix((self.omega*esc)[None,:]),csc_matrix((1,1))]],format='csc')
        return evaluate,(n,Ti,L,age)
    def run(self,alpha,mass,Mb,b,rtol=2e-7,closed=False,end=1.):
        fun,(n,Ti,L,age)=self.system(alpha,mass,Mb,b,closed)
        nm=self.nm;nb=self.nb;nq=self.nq;y0=np.zeros(nm+nq+1);y0[nm-1]=3*Ti
        atol=np.full(len(y0),2e-13);atol[nm-1]=max(1e-18,3*Ti*2e-10)
        sol=solve_ivp(lambda t,y:fun(y),(0,end),y0,method='BDF',jac=lambda t,y:fun(y,True),rtol=rtol,atol=atol,t_eval=np.r_[0,np.geomspace(1e-12*end,end,121)])
        if not sol.success:raise RuntimeError(sol.message)
        a=sol.y[0];ts=sol.y[1:nb+1];t=ts.sum(axis=0);x=1-a-2*t;c=1-a-t
        T=sol.y[nm-1]/(1.5*(1+x));rad=self.omega@sol.y[nm:nm+nq]
        E=sol.y[nm-1]-.5*a-(.5+self.D)@ts+rad+sol.y[-1]
        deg=max(float(max(f*n*(2*np.pi/(m*T))**1.5)) for f,m in zip([x,c,a,t],[100,1,101,201]))
        plasma=float(max((4*np.pi*(x+c+t)*n/3)**(1/3)/T))
        gates=dict(classical=deg<.1,weak_plasma=plasma<.1,dilute=max(n,float(max(t))*n*8)<.01,low_temperature=max(T)<=.05,nonrelativistic=max(T)*alpha**2<.01)
        tau=alpha*n*L*(np.vstack([a,ts]).T@self.sig)
        result=dict(alpha=alpha,mass_eV=mass,Mb=Mb,b=b,groups=nq,closed=closed,end_age_fraction=end,initial_T=Ti,final_T=float(T[-1]),molecular_mass_fraction=float(201/101*t[-1]),atomic_fraction=float(a[-1]),free_X=float(x[-1]),countercharge_C=float(c[-1]),photon_number=float(sum(sol.y[nm:nm+nq,-1])),radiation_energy=float(rad[-1]),escaped_energy=float(sol.y[-1,-1]),max_optical_depth=float(max(tau.ravel())),energy_error=float(max(abs(E-3*Ti))),charge_error=float(max(abs(x+t-c))),minimum_species=float(min(np.r_[a,t,x,c])),temperature_range=[float(min(T)),float(max(T))],gates={k:bool(v) for k,v in gates.items()},applicable=bool(all(gates.values())),nfev=sol.nfev,njev=sol.njev)
        assert result['energy_error']<1e-7 and result['charge_error']<1e-12 and result['minimum_species']>-1e-7
        return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--order',type=int,default=3);p.add_argument('--decades',type=int,default=1);p.add_argument('--single',action='store_true');a=p.parse_args();rad=Radiation(a.order,a.decades)
    rows=[]
    pairs=[(.15,1e7)] if a.single else [(al,m) for al in [.15,.2] for m in [1e6,1e7,10**8.5]]
    for al,m in pairs:
        states=[]
        for Mb,b in PROFILES:
            state=rad.run(al,m,Mb,b);states.append(state);print(al,m,Mb,state['molecular_mass_fraction'],state['max_optical_depth'],state['nfev'],flush=True)
        f=[s['molecular_mass_fraction'] for s in states]
        rows.append(dict(alpha=al,mass=m,states=states,applicable=all(s['applicable'] for s in states),target=f[2]>=.8 and max(f[0],f[1],f[3])<=.2))
    Path(a.output).write_text(json.dumps(dict(rows=rows),indent=2)+'\n')
if __name__=='__main__':main()
