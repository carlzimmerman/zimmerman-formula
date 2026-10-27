"""Infinite-collision limit, not invented finite scattering amplitudes."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.special import logsumexp,expit
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.sparse import bmat,csc_matrix,diags
from photons import Radiation,escape,environment,PROFILES

class FastChemistry:
    def __init__(self,rad,n):self.rad=rad;self.n=n
    def state(self,T):
        D=self.rad.D;g=self.rad.deg[1:];lz=logsumexp(np.log(g)+D/T)
        probs=np.exp(np.log(g)+D/T-lz);meanD=float(probs@D)
        lq=np.log(self.n)-1.5*np.log(T/(2*np.pi))+.5/T
        lr=np.log(self.n)-1.5*np.log((100*101/201)*T/(2*np.pi))+lz
        lc2=lq+np.logaddexp(0,lr);lc3=lq+lr
        lo=-max(1,lc2/2,lc3/3)-10
        def poly(z):return np.expm1(z)+np.exp(np.clip(lc2+2*z,-745,700))+np.exp(np.clip(lc3+3*z,-745,700))
        lx=brentq(poly,lo,0.,xtol=1e-300,rtol=1e-14)
        x=np.exp(lx);rem=-np.expm1(lx);lh=lr+lx;den=np.logaddexp(0,np.log(2)+lh)
        a=rem*np.exp(-den);t=rem*np.exp(lh-den);tb=t*probs;c=x+t
        # Exact derivative with respect to log T, implicit cubic + partition function.
        qp=-1.5-.5/T;rp=-1.5-meanD/T
        t2=np.exp(lc2+2*lx);t3=np.exp(lc3+3*lx)
        xp=-(t2*(qp+expit(lr)*rp)+t3*(qp+rp))/(x+2*t2+3*t3)
        remp=-x*xp/max(rem,1e-300);hp=rp+xp
        ap=a*(remp-expit(np.log(2)+lh)*hp)
        tp=t*(remp+expit(-np.log(2)-lh)*hp)
        tbp=probs*tp+tb*(meanD-D)/T
        K=1.5*T*(1+x);U=K-.5*a-(.5+D)@tb
        capacity=K+1.5*T*x*xp-.5*ap-(.5+D)@tbp
        assert capacity>0
        return dict(x=x,c=c,a=a,t=t,tb=tb,U=U,capacity=capacity,targets=np.r_[a,tb],target_prime=np.r_[ap,tbp])

    def run(self,alpha,mass,Mb,b,rtol=1e-9):
        rad=self.rad;n,Ti,L,age=environment(alpha,mass,Mb,b);assert abs(n-self.n)/n<1e-12
        T0=brentq(lambda T:self.state(T)['U']-3*Ti,1e-9,2*Ti+1,xtol=1e-14)
        nq=rad.nq
        def evaluate(y,jac=False):
            T=brentq(lambda tt:self.state(tt)['U']-y[0],1e-10,max(1.,y[0]+1),xtol=2e-14);s=self.state(T);phot=y[1:nq+1];op=s['targets']@rad.sig
            ex=np.exp(-rad.omega/T);A=age*op*alpha**3*rad.G*ex;B=-age*op*n*(-np.expm1(-rad.omega/T))
            events=A+B*phot;tau=alpha*n*L*op;ff,fp=escape(tau);esc=age/(alpha*L)*ff
            flow=esc*phot;du=-np.dot(rad.omega,events)
            out=np.r_[du,events-flow,np.dot(rad.omega,flow)]
            if not jac:return out
            opp=s['target_prime']@rad.sig
            dr=age*(opp*(alpha**3*rad.G*ex-n*phot*(1-ex))+op*(alpha**3*rad.G+n*phot)*ex*rad.omega/T)
            des=age*n*fp*opp
            dr/=s['capacity'];des/=s['capacity']
            jtt=-np.dot(rad.omega,dr)
            return bmat([[csc_matrix([[jtt]]),csc_matrix((-rad.omega*B)[None,:]),None],[csc_matrix((dr-des*phot)[:,None]),diags(B-esc),None],[csc_matrix([[np.dot(rad.omega,des*phot)]]),csc_matrix((rad.omega*esc)[None,:]),csc_matrix((1,1))]],format='csc')
        y0=np.zeros(nq+2);y0[0]=3*Ti
        sol=solve_ivp(lambda t,y:evaluate(y),(0,1),y0,method='BDF',jac=lambda t,y:evaluate(y,True),rtol=rtol,atol=2e-13,t_eval=np.r_[0,np.geomspace(1e-12,1,121)])
        assert sol.success,sol.message
        Ts=np.array([brentq(lambda tt:self.state(tt)['U']-u,1e-10,max(1.,u+1),xtol=2e-14) for u in sol.y[0]]);states=[self.state(T) for T in Ts];U=sol.y[0];radE=rad.omega@sol.y[1:nq+1];energy=U+radE+sol.y[-1]
        sf=states[-1];f=201/101*sf['t'];deg=max(float(s0*self.n*(2*np.pi/(m*T))**1.5) for T,s in zip(Ts,states) for s0,m in zip([s['x'],s['c'],s['a'],s['t']],[100,1,101,201]))
        plasma=max(float((4*np.pi*(s['x']+s['c']+s['t'])*n/3)**(1/3)/T) for T,s in zip(Ts,states))
        gates=dict(classical=deg<.1,weak_plasma=plasma<.1,dilute=n<.001,low_temperature=max(Ts)<=.05,nonrelativistic=max(Ts)*alpha**2<.01)
        out=dict(alpha=alpha,mass_eV=mass,Mb=Mb,b=b,initial_ionized_T=Ti,post_relaxation_T=T0,final_T=float(Ts[-1]),molecular_mass_fraction=float(f),atomic_fraction=float(sf['a']),free_X=float(sf['x']),countercharge_C=float(sf['c']),energy_error=float(max(abs(energy-3*Ti))),charge_error=float(max(abs(s['x']+s['t']-s['c']) for s in states)),radiation_energy=float(radE[-1]),escaped_energy=float(sol.y[-1,-1]),temperature_range=[float(min(Ts)),float(max(Ts))],groups=nq,gates={k:bool(v) for k,v in gates.items()},applicable=bool(all(gates.values())),nfev=sol.nfev)
        assert out['energy_error']<1e-8 and out['charge_error']<1e-12
        return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();rad=Radiation(3);rows=[]
    for al in [.15,.2]:
        for mass in [1e6,1e7,10**8.5]:
            states=[]
            for Mb,b in PROFILES:
                n,*_=environment(al,mass,Mb,b);s=FastChemistry(rad,n).run(al,mass,Mb,b);states.append(s);print(al,mass,Mb,s['molecular_mass_fraction'],s['energy_error'],flush=True)
            f=[s['molecular_mass_fraction'] for s in states];rows.append(dict(alpha=al,mass=mass,states=states,applicable=all(s['applicable'] for s in states),target=f[2]>=.8 and max(f[0],f[1],f[3])<=.2))
    Path(a.output).write_text(json.dumps(dict(rows=rows),indent=2)+'\n')
if __name__=='__main__':main()
