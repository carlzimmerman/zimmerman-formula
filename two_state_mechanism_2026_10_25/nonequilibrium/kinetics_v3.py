"""Finite-age, optically thin radiative subnetwork with explicit energy ledger."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.interpolate import PchipInterpolator
from scipy.special import lambertw
BASE=Path(__file__).resolve().parent
G=6.67430e-11;MSUN=1.98847e30;KPC=3.085677581491367e19
C=299792458.;HBAR=1.054571817e-34;EVMASS=1.7826619216279e-36
PROFILES=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]
M=100.;ETA=5.364;MUAX=M*(M+1)/(2*M+1);AGE=10e9*365.25*86400
CTH=512*np.pi**2/(3*np.e**4)

def atomic_shape(excess):
    v=np.asarray(excess);z=np.sqrt(np.maximum(v,1e-30))
    return np.exp(4-4*np.arctan(z)/z)/(-np.expm1(-2*np.pi/z))/(1+v)**4

def atomic(T):
    def f(u):return (1+2*T*u)**2*float(atomic_shape(2*T*u))*np.exp(-u)
    v=quad(f,0,100,epsabs=1e-11,epsrel=1e-9)[0]
    w=quad(lambda u:u*f(u),0,100,epsabs=1e-11,epsrel=1e-9)[0]
    return 2*np.sqrt(2/np.pi)*.25*CTH/np.sqrt(T)*v,T*w/v

class Rates:
    def __init__(self,path):
        self.data=json.loads(Path(path).read_text());d=self.data
        self.en=np.array(d['energies']);self.S=np.array(d['strength']);self.D=np.array([r['D'] for r in d['levels']]);self.deg=np.array([r['weight'] for r in d['levels']])
        self.Ts=np.geomspace(1e-8,.3,400)
        ks=[];es=[]
        for T in self.Ts:
            q=(self.en[None,:]+self.D[:,None])**3*self.S*np.exp(-self.en[None,:]/T)
            integ=np.trapz(q,self.en,axis=1)
            kval=4/3*self.deg*(2*np.pi/MUAX)**1.5*T**-1.5*integ
            mean=np.trapz(q*self.en,self.en,axis=1)/np.maximum(integ,1e-300)
            ka,ea=atomic(T);ks.append(np.r_[ka,kval]);es.append(np.r_[ea,mean])
        self.ks=np.array(ks);self.es=np.array(es)
        self.lk=PchipInterpolator(np.log(self.Ts),np.log(np.maximum(self.ks,1e-290)),axis=0,extrapolate=False)
        self.ee=PchipInterpolator(np.log(self.Ts),self.es,axis=0,extrapolate=False)
        self.rmax=float(np.max(self.ks[:,1:].sum(axis=1)/self.ks[:,0]))
        self.count_bound=float(self.rmax*lambertw(1/self.rmax).real)
        # Opacity sampled at all individual molecular threshold-offset grids and atomic edge.
        self.photons=np.unique(np.concatenate([.5*(1+np.geomspace(1e-10,4,400))]+[self.en+D for D in self.D]))
        self.sigA=np.where(self.photons>=.5,CTH*atomic_shape(np.maximum(2*self.photons-1,0)),0.)
        self.sigB=np.array([4*np.pi**2/3*self.photons*np.interp(self.photons-D,self.en,s,left=0.,right=0.) for D,s in zip(self.D,self.S)])
    def at(self,T):
        # Extrapolation deliberately forbidden; failed temperature coverage is not data.
        if not self.Ts[0]<=T<=self.Ts[-1]:raise ValueError('temperature outside rate table: '+str(T))
        return np.exp(self.lk(np.log(T))),self.ee(np.log(T))
    def reciprocity(self):
        out=[]
        for T in [.001,.01,.05]:
            omega=self.en[None,:]+self.D[:,None]
            planck=1/np.expm1(np.minimum(omega/T,700))
            gamma=4/3*np.trapz(omega**3*self.S*planck,self.en,axis=1)
            k=4/3*self.deg*(2*np.pi/MUAX)**1.5*T**-1.5*np.trapz(omega**3*self.S*np.exp(-self.en[None,:]/T)*(1+planck),self.en,axis=1)
            ratio=k/gamma*(MUAX*T/(2*np.pi))**1.5*np.exp(-self.D/T)/self.deg
            out.append(dict(T=T,max_relative_error=float(max(abs(ratio-1)))))
        return out

def environment(alpha,mass,Mb,b):
    aD=HBAR/(mass*EVMASS*C*alpha);EH=mass*EVMASS*C*C*alpha*alpha
    n=3*ETA*Mb*MSUN/(4*np.pi*(b*KPC)**3*(M+1)*mass*EVMASS)
    sigma2=G*(1+ETA)*Mb*MSUN/(6*b*KPC)
    return n*aD**3,(M+1)*sigma2/(2*C*C*alpha*alpha),b*KPC/aD,AGE*EH/HBAR

def parcel(rates,alpha,mass,Mb,b,tol=2e-8):
    n,Ti,L,age=environment(alpha,mass,Mb,b);nb=len(rates.D)
    # State a,t_b,K,Q; algebraic stoichiometry tracks BOTH constituent species.
    y0=np.zeros(nb+3);y0[-2]=3*Ti
    pref=n*alpha**3*age
    def rhs(t,y):
        a=y[0];ts=y[1:nb+1];x=1-a-2*sum(ts);c=1-a-sum(ts)
        T=y[-2]/(1.5*(1+x));ks,es=rates.at(T)
        ra=pref*ks[0]*max(x,0)*max(c,0)
        rb=pref*ks[1:]*max(a,0)*max(x,0)
        return np.r_[ra-sum(rb),rb,-es[0]*ra-np.dot(es[1:],rb),(.5+es[0])*ra+np.dot(rates.D+es[1:],rb)]
    sol=solve_ivp(rhs,(0,1),y0,method='BDF',rtol=tol,atol=tol*1e-4,t_eval=np.r_[0,np.geomspace(1e-12,1,160)])
    assert sol.success,sol.message
    a=sol.y[0];ts=sol.y[1:nb+1];t=ts.sum(axis=0);x=1-a-2*t;c=1-a-t
    T=sol.y[-2]/(1.5*(1+x));energy=sol.y[-2]-.5*a-(.5+rates.D)@ts+sol.y[-1]
    errors=dict(energy_absolute=float(max(abs(energy-3*Ti))),charge=float(max(abs(x+t-c))),heavy=float(max(abs(x+a+2*t-1))),light=float(max(abs(c+a+t-1))))
    assert min(np.r_[x,c,a,t])>-1e-7
    assert errors['energy_absolute']<1e-8 and max(errors[k] for k in ['charge','heavy','light'])<1e-12
    deg=max(float(np.max(f*n*(2*np.pi/(m*T))**1.5)) for f,m in zip([x,c,a,t],[M,1,M+1,2*M+1]))
    plasma=float(np.max((4*np.pi*(x+c+t)*n/3)**(1/3)/T))
    dilute=float(max(n,max(t)*n*2.**3))
    # Matrix computes opacity over every recorded state, not only endpoint.
    tau=alpha*n*L*(a[:,None]*rates.sigA[None,:]+ts.T@rates.sigB)
    opacity=float(max(tau.ravel()))
    # Upper estimate electron-impact geometric encounter rate, NOT a physical dissociation rate.
    gates=dict(classical=deg<.1,weak_plasma=plasma<.1,dilute=dilute<.01,low_temperature=max(T)<=.05,nonrelativistic=max(T)*alpha**2<.01,optically_thin=opacity<.1)
    gates={k:bool(v) for k,v in gates.items()}
    return dict(initial_T=Ti,density=n,final_T=float(T[-1]),atomic_fraction=float(a[-1]),free_X=float(x[-1]),countercharge_C=float(c[-1]),molecular_count=float(t[-1]),molecular_mass_fraction=float((2*M+1)/(M+1)*t[-1]),level_populations=ts[:,-1].tolist(),escaped_energy=float(sol.y[-1,-1]),errors=errors,degeneracy=deg,plasma_coupling=plasma,dilution=dilute,max_optical_depth=opacity,gates=gates,applicable=bool(all(gates.values())),nfev=sol.nfev,temperature_range=[float(min(T)),float(max(T))])

def main():
    p=argparse.ArgumentParser();p.add_argument('--spectrum',required=True);p.add_argument('--output',required=True);p.add_argument('--check',action='store_true');a=p.parse_args();rates=Rates(a.spectrum)
    rows=[]
    pairs=[(.2,100.),(.15,100.),(.2,1000.)] if a.check else [(al,float(m)) for al in [.1,.15,.2] for m in np.geomspace(1,1e6,13)]
    for alpha,mass in pairs:
        states=[parcel(rates,alpha,mass,Mb,b,tol=2e-10 if a.check else 2e-8) for Mb,b in PROFILES]
        f=[s['molecular_mass_fraction'] for s in states]
        rows.append(dict(alpha=alpha,mass_eV=mass,states=states,applicable=all(s['applicable'] for s in states),target=f[2]>=.8 and max(f[0],f[1],f[3])<=.2))
    eligible=[r for r in rows if r['applicable']]
    best=max(rows,key=lambda r:r['states'][2]['molecular_mass_fraction'])
    beste=max(eligible,key=lambda r:r['states'][2]['molecular_mass_fraction']) if eligible else None
    summary=dict(points=len(rows),profile_runs=4*len(rows),eligible_points=len(eligible),targets=sum(r['target'] for r in rows),eligible_targets=sum(r['target'] for r in eligible),max_disk=best['states'][2]['molecular_mass_fraction'],best_parameters=[best['alpha'],best['mass_eV']],fractions_at_best=[s['molecular_mass_fraction'] for s in best['states']],max_eligible_disk=beste['states'][2]['molecular_mass_fraction'] if beste else None,best_eligible_parameters=[beste['alpha'],beste['mass_eV']] if beste else None,eligible_fractions_at_best=[s['molecular_mass_fraction'] for s in beste['states']] if beste else None,max_rate_ratio=rates.rmax,conditional_molecular_mass_cap=(2*M+1)/(M+1)*rates.count_bound,max_energy_error=max(s['errors']['energy_absolute'] for r in rows for s in r['states']),reciprocity=rates.reciprocity())
    Path(a.output).write_text(json.dumps(dict(summary=summary,rows=rows),indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
