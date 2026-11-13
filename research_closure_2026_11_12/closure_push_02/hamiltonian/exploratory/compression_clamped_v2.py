"""Does smooth compression enter a negative-compressibility region?

Finite periodic leading-Newtonian action; a compatibility background removes
the Poisson zero mode. Clamped flat S=exp[-max(Pi/Pic,0)^3], with the action's
one-sided stiffness gamma max(Pi,0)^2/2. Clamping is a distinct proposed gate
that addresses the literal flat gate's negative-Pi enhancement. Not adopted.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np


class Model:
    def __init__(self,N,k0=1e4,C=1e6,gamma=1e-8):
        self.N=N;self.k0=k0;self.C=C;self.gamma=gamma
        self.theta=2*np.pi*np.arange(N)/N
        modes=np.fft.fftfreq(N,1/N);modes[N//2]=0
        self.k=modes*k0
        self.D=np.fft.ifft(1j*self.k[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real
        self.P=np.zeros(N)
        self.max_constraint=0.

    def calc(self,n,P):
        Pi=self.D@P
        if np.max(np.abs(Pi))>5:raise RuntimeError('outside declared gate range |Pi|<=5')
        h=n-Pi;positive=np.maximum(Pi,0);gg=np.exp(positive**3)
        lp=3*positive**2; lpp=6*positive
        x=h*gg/(2*self.C)
        eP=gg/(4*self.C)*(-2*h+lp*h*h)+self.gamma*positive
        ePP=gg/(4*self.C)*(2-4*lp*h+(lpp+lp*lp)*h*h)+self.gamma*(Pi>0)
        denom=1-np.abs(P) # K=a0=Pi_c=1
        if np.min(denom)<=0:raise RuntimeError('outside W domain')
        WP=P/denom
        residual=-self.D@eP+WP
        jac=-self.D@(ePP[:,None]*self.D)+np.diag(1/denom**2)
        return Pi,x,residual,jac,ePP

    def constraint(self,n):
        P=self.P.copy()
        for iteration in range(30):
            Pi,x,res,jac,epp=self.calc(n,P)
            norm=np.max(np.abs(res))
            if norm<1e-10:
                self.P=P;self.max_constraint=max(self.max_constraint,norm)
                return P,Pi,x,epp
            step=np.linalg.solve(jac,-res)
            accepted=False
            for power in range(20):
                trial=P+step*2.**(-power)
                try:err=np.max(np.abs(self.calc(n,trial)[2]))
                except RuntimeError:continue
                if err<norm:
                    P=trial;accepted=True;break
            if not accepted:raise RuntimeError('polarization line search failed')
        raise RuntimeError('polarization constraint did not converge')

    def phi(self,n):
        f=np.fft.fft(n);result=np.zeros_like(f);mask=self.k!=0
        result[mask]=-f[mask]/self.k[mask]**2
        return np.fft.ifft(result).real

    def rhs(self,state):
        n,v=np.split(state,2)
        _,_,x,_=self.constraint(n)
        return np.concatenate((-self.D@(n*v),-self.D@(.5*v*v+self.phi(n)+x)))

    def inspect(self,state):
        n,v=np.split(state,2);P,Pi,x,epp=self.constraint(n)
        positive=np.maximum(Pi,0)
        S=np.exp(-positive**3);Sp=-3*positive**2*S;Spp=(9*positive**4-6*positive)*S
        aq=2*self.C*S;bq=2*self.C*x*Sp;D=self.C*x*x*Spp-self.gamma*(Pi>0)
        c=1+bq
        # Local high-k charge coefficient, before subleading Poisson term.
        heff=-D/(c*c-aq*D)
        unstable=(Pi>0)&(D>0)&(epp>0)&(heff<0)
        return {'min_n':float(n.min()),'max_n':float(n.max()),'min_Pi':float(Pi.min()),'max_Pi':float(Pi.max()),
                'max_x':float(np.max(abs(x))),'max_phi':float(np.max(abs(self.phi(n)))),
                'max_speed':float(np.max(abs(v))),'max_P_fraction_cap':float(np.max(abs(P))),
                'min_ePP':float(epp.min()),'max_D_positive_Pi':float(np.max(D[Pi>0])) if np.any(Pi>0) else None,
                'negative_highk_charge_coefficient_reached':bool(np.any(unstable)),
                'worst_highk_cs2':float(np.min(n[unstable]*heff[unstable])) if np.any(unstable) else None,
                'mean_charge':float(n.mean()),'nyquist_relative':float(abs(np.fft.fft(n)[self.N//2])/self.N/n.mean()),
                'highband_relative':float(np.linalg.norm(np.fft.fft(n)[np.abs(np.fft.fftfreq(self.N)*self.N)>=self.N/3])/np.linalg.norm(np.fft.fft(n)))}

    def near_transition(self):
        # Smooth asymmetric zero-mean divergence: a narrow positive peak,
        # broad shallow negative compensation, and a strictly positive charge.
        profile=np.exp(8*(np.cos(self.theta)-1))
        Pi=.86*(profile-profile.mean())/(1-profile.mean())
        inv=np.zeros(self.N,dtype=complex);mask=self.k!=0
        inv[mask]=1/(1j*self.k[mask])
        P=np.fft.ifft(inv*np.fft.fft(Pi)).real
        Pi=self.D@P
        WP=P/(1-np.abs(P))
        eP=np.fft.ifft(inv*np.fft.fft(WP)).real-.15/self.C
        pp=np.maximum(Pi,0);S=np.exp(-pp**3);lp=3*pp**2
        # Stable low root, evaluated without cancellation; lp=0 included.
        target=4*self.C*S*(eP-self.gamma*pp)
        disc=1+lp*target
        if disc.min()<=0:raise RuntimeError('initial algebraic root absent')
        h=-target/(1+np.sqrt(disc))
        n=Pi+h
        self.P=P
        return np.concatenate((n,-.001*np.sin(self.theta)))


def run(N,dt,tmax,output,initial_kind):
    start=time.perf_counter();m=Model(N)
    state=(m.near_transition() if initial_kind=='near_transition' else
           np.concatenate((1.7+.05*np.cos(m.theta),-.001*np.sin(m.theta))))
    initial=m.inspect(state);rows=[dict(t=0.,**initial)];event=None
    steps=int(np.ceil(tmax/dt));dt=tmax/steps
    for i in range(steps):
        a=m.rhs(state);b=m.rhs(state+dt*a/2);c=m.rhs(state+dt*b/2);d=m.rhs(state+dt*c)
        state+=dt*(a+2*b+2*c+d)/6
        row=m.inspect(state);rows.append(dict(t=(i+1)*dt,**row))
        if row['negative_highk_charge_coefficient_reached']:
            event='negative_highk_charge_coefficient';break
        if row['min_n']<=0 or row['highband_relative']>1e-3:
            event='numerical_control_failed';break
    if event is None:event='time_limit'
    result={'model':'clamped flat gate with one-sided stiffness; finite periodic NR model',
            'N':N,'dt':dt,'initial_kind':initial_kind,'event':event,'initial':initial,'last':rows[-1],
            'max_charge_mean_drift':float(max(abs(r['mean_charge']-initial['mean_charge']) for r in rows)),
            'constraint_max':m.max_constraint,'runtime_seconds':time.perf_counter()-start,'rows':rows}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--N',type=int,default=32)
    p.add_argument('--dt',type=float,default=2e-4);p.add_argument('--tmax',type=float,default=.05)
    p.add_argument('--initial',choices=['small_mode','near_transition'],default='near_transition')
    a=p.parse_args();run(a.N,a.dt,a.tmax,a.output,a.initial)
