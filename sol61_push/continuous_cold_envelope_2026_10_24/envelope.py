"""Live same-field envelope experiment; scalar outputs only, no galaxy fit."""
import argparse,json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.fft import fftn,ifftn,fftfreq

p=argparse.ArgumentParser()
p.add_argument('--fraction',type=float,required=True)
p.add_argument('--tag',required=True)
p.add_argument('--n',type=int,default=64)
p.add_argument('--L',type=float,default=32.)
a=p.parse_args()
N=a.n;L=a.L;dx=L/N;dv=dx**3;eta=.7;dt=.06;T=60.;steps=round(T/dt)
x=(np.arange(N)-N/2)*dx
X,Y,Z=np.meshgrid(x,x,x,indexing='ij',sparse=True)
r2=X*X+Y*Y+Z*Z;r=np.sqrt(r2);inner=r<3
k=2*np.pi*fftfreq(N,d=dx)
kx,ky,kz=np.meshgrid(k,k,k,indexing='ij',sparse=True)
k2=kx*kx+ky*ky+kz*kz
kernel=np.zeros_like(k2);np.divide(-4*np.pi,k2,out=kernel,where=k2!=0)
kin=np.exp(-.5j*eta*k2*dt)
damp=np.exp(-dt*.15*(np.maximum(r-12,0)/4)**4)
rc=np.exp(-((X/4)**2+(Y/2)**2+(Z/2)**2))/(math.pi**1.5*4*2*2)
re=np.exp(-r2/25)/(math.pi**1.5*5**3)
taper=np.where(r<=10,1.,np.where(r<12,np.cos(np.pi*(r-10)/4)**4,0.))
rho=((1-a.fraction)*rc+a.fraction*re)*taper
phase=np.exp(-r2/50)*(-.03*r2/2+.03*X*Y)
psi=np.sqrt(rho)*np.exp(1j*phase/eta);psi/=math.sqrt(float(np.sum(abs(psi)**2)*dv))
order=np.argsort(r.ravel());sr=r.ravel()[order]
virial_weights={str(scale):1/(3*scale*(1+(r/scale)**2)**1.5) for scale in [.5,1,2,4]}

def potential(w):return ifftn(kernel*fftn(abs(w)**2,workers=1),workers=1).real

def totals(w,ph):
    den=abs(w)**2;wk=fftn(w,workers=1)
    K=float(.5*eta**2*np.sum(k2*abs(wk)**2)*dv/N**3)
    W=float(.5*np.sum(den*ph)*dv)
    wx=ifftn(1j*kx*wk,workers=1);wy=ifftn(1j*ky*wk,workers=1)
    jd=eta*np.imag(np.conj(w)*(X*wy-Y*wx))
    M=float(den.sum()*dv);J=float(jd.sum()*dv)
    return {'M':M,'E':K+W,'K':K,'W':W,'J':J},den,jd

def snapshot(w,ph,t,removed):
    total,den,jd=totals(w,ph)
    mi=float(den[inner].sum()*dv);ji=float(jd[inner].sum()*dv)
    enc=np.cumsum(den.ravel()[order])*dv
    rh=float(sr[np.searchsorted(enc,total['M']/2)])
    prof={str(R):float(den[r<R].sum()*dv) for R in [1,2,3,4,6,8,10,12]}
    return {'t':t,**total,'M_inner':mi,'J_inner':ji,'M_outer':total['M']-mi,
            'J_outer':total['J']-ji,'rhalf':rh,'profile':prof,
            'stellar_virial_moment':{s:float(np.sum(den*weight)*dv) for s,weight in virial_weights.items()},
            'removed':dict(removed)}

start=time.time();ph=potential(psi);removed={'M':0.,'E':0.,'J':0.}
initial=snapshot(psi,ph,0.,removed);history=[initial]
for n in range(steps):
    psi*=np.exp(-.5j*ph*dt/eta)
    psi=ifftn(fftn(psi,workers=1)*kin,workers=1)
    ph=potential(psi);psi*=np.exp(-.5j*ph*dt/eta)
    bef,_,_=totals(psi,ph)
    psi*=damp;ph=potential(psi)
    aft,_,_=totals(psi,ph)
    for key in removed:removed[key]+=bef[key]-aft[key]
    if (n+1)%25==0 or n==steps-1:
        history.append(snapshot(psi,ph,(n+1)*dt,removed))
final=history[-1];mid=min(history,key=lambda h:abs(h['t']-30))
mr=final['M']+removed['M']-initial['M']
er=(final['E']+removed['E']-initial['E'])/abs(initial['E'])
jr=(final['J']+removed['J']-initial['J'])/abs(initial['J'])
sgn=1 if initial['J_inner']>=0 else -1
jref=abs(initial['J_inner'])
inner_loss=sgn*(initial['J_inner']-mid['J_inner'])/jref
outer_gain=sgn*(mid['J_outer']-initial['J_outer'])/jref
specific_ratio=abs(final['J_inner']/final['M_inner'])/abs(initial['J_inner']/initial['M_inner'])
tail=[h['M_inner'] for h in history if h['t']>=45]
gates={'initial_bound':initial['E']<0,'mass_ledger':abs(mr)<=1e-8,
       'energy_ledger':abs(er)<=.01,'angular_ledger':abs(jr)<=.02,
       'storage_inner_spin_loss':inner_loss>=.5,'storage_outer_spin_gain':outer_gain>=.5,
       'storage_mass_retained':mid['removed']['M']<=.01146,
       'formation_inner_mass_gain':final['M_inner']>=1.25*initial['M_inner'],
       'formation_inner_specific_spin_reduced':specific_ratio<=.5,
       'formation_mass_retained':removed['M']<=.01146,
       'formation_late_mass_stable':(max(tail)-min(tail))/np.mean(tail)<=.1}
result={'parameters':{'N':N,'L':L,'dt':dt,'T':T,'eta':eta,'envelope_fraction':a.fraction},
        'initial':initial,'mid':mid,'final':final,'history':history,'gates':gates,
        'M_ledger_absolute':mr,'E_ledger_relative':er,'J_ledger_relative':jr,
        'mid_inner_spin_loss_fraction':inner_loss,'mid_outer_spin_gain_fraction':outer_gain,
        'final_inner_mass_ratio':final['M_inner']/initial['M_inner'],
        'final_inner_specific_spin_ratio':specific_ratio,
        'final_virial_moment_ratios':{s:final['stellar_virial_moment'][s]/initial['stellar_virial_moment'][s] for s in virial_weights},
        'elapsed_s':time.time()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'retention and aperture exchange in a periodic-box candidate; not certified bound-envelope capture, physical infinity-energy escape, stellar heating or four-dwarf closure'}
def encode(v):
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)
out=Path(__file__).parent/'runs';out.mkdir(exist_ok=True)
(out/(a.tag+'.json')).write_text(json.dumps(result,indent=2,default=encode)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['initial','mid','final','history']},indent=2,default=encode),flush=True)
