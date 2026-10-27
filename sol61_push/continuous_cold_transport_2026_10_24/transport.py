"""Exploratory isolated wave candidate in a periodic cube with ledgered absorber."""
import argparse
import json
import math
import resource
import time
from pathlib import Path
import numpy as np
from scipy.fft import fftn, ifftn, fftfreq

parser=argparse.ArgumentParser()
parser.add_argument('--n',type=int,required=True)
parser.add_argument('--dt',type=float,default=.06)
parser.add_argument('--beta',type=float,default=.03)
parser.add_argument('--tag',required=True)
parser.add_argument('--L',type=float,default=24.)
args=parser.parse_args()
N=args.n; L=args.L; eta=.7; dx=L/N; dv=dx**3; T=30.
steps=round(T/args.dt); dt=T/steps
x=(np.arange(N)-N/2)*dx
X,Y,Z=np.meshgrid(x,x,x,indexing='ij',sparse=True)
r2=X*X+Y*Y+Z*Z; r=np.sqrt(r2)
k=2*np.pi*fftfreq(N,d=dx)
KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij',sparse=True)
k2=KX*KX+KY*KY+KZ*KZ
kernel=np.zeros_like(k2); np.divide(-4*np.pi,k2,out=kernel,where=k2!=0)
kinetic_phase=np.exp(-.5j*eta*k2*dt)
damping=np.exp(-dt*.15*(np.maximum(r-9,0)/3)**4)
phase=-.03*r2/2+args.beta*X*Y
psi=np.exp(-.5*((X/4)**2+(Y/2)**2+(Z/2)**2))*np.exp(1j*phase/eta)
psi/=math.sqrt(float(np.sum(abs(psi)**2)*dv))
order=np.argsort(r.ravel()); sorted_r=r.ravel()[order]

def potential(p):
    return ifftn(kernel*fftn(abs(p)**2,workers=1),workers=1).real

def quantities(p,ph=None):
    rho=abs(p)**2; ph=potential(p) if ph is None else ph
    pk=fftn(p,workers=1)
    mass=float(rho.sum()*dv)
    Ekin=float(.5*eta**2*np.sum(k2*abs(pk)**2)*dv/N**3)
    Egrav=float(.5*np.sum(rho*ph)*dv)
    px=ifftn(1j*KX*pk,workers=1); py=ifftn(1j*KY*pk,workers=1)
    J=float(eta*np.sum(np.imag(np.conj(p)*(X*py-Y*px)))*dv)
    enclosed=np.cumsum(rho.ravel()[order])*dv
    rh=float(sorted_r[np.searchsorted(enclosed,.5*mass)])
    return {'mass':mass,'E':Ekin+Egrav,'K':Ekin,'W':Egrav,'Jz':J,'rhalf':rh}

start=time.time(); initial=quantities(psi); history=[]
removed={'mass':0.,'E':0.,'Jz':0.}
ph=potential(psi)
for step in range(steps):
    psi*=np.exp(-.5j*ph*dt/eta)
    psi=ifftn(fftn(psi,workers=1)*kinetic_phase,workers=1)
    ph=potential(psi)
    psi*=np.exp(-.5j*ph*dt/eta)
    before=quantities(psi,ph)
    psi*=damping
    ph=potential(psi)
    after=quantities(psi,ph)
    for key in removed:removed[key]+=before[key]-after[key]
    if step%25==0 or step==steps-1:
        history.append({'t':(step+1)*dt,**after,'removed':dict(removed)})
final=history[-1]
Eres=(final['E']+removed['E']-initial['E'])/abs(initial['E'])
Jres=(final['Jz']+removed['Jz']-initial['Jz'])/max(abs(initial['Jz']),1e-12)
tail=[h['rhalf'] for h in history if h['t']>=.75*T]
result={'parameters':{'N':N,'L':L,'dt':dt,'T':T,'eta':eta,'beta':args.beta},
        'initial':initial,'final':{k:final[k] for k in initial},'removed':removed,
        'energy_ledger_relative':Eres,'spin_ledger_relative':Jres,
        'export_spin_fraction':removed['Jz']/initial['Jz'] if abs(initial['Jz'])>1e-10 else None,
        'export_mass_fraction':removed['mass']/initial['mass'],
        'export_energy_over_initial_binding':removed['E']/abs(initial['E']),
        'contraction':initial['rhalf']/final['rhalf'],
        'late_radius_range_fraction':(max(tail)-min(tail))/np.mean(tail),
        'gates':{'energy_ledger':abs(Eres)<=.01,
                 'spin_ledger':abs(Jres)<=.02 if abs(initial['Jz'])>1e-10 else abs(final['Jz'])<1e-9,
                 'positive_net_boundary_energy':removed['E']>0,
                 'half_spin_export':removed['Jz']/initial['Jz']>=.5 if abs(initial['Jz'])>1e-10 else None,
                 'contraction_1p5':initial['rhalf']/final['rhalf']>=1.5,
                 'late_radius_stable':(max(tail)-min(tail))/np.mean(tail)<=.1},
        'history':history,'elapsed_s':time.time()-start,
        'peak_rss_native_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'periodic-cube candidate, absorber bookkeeping, not certified physical escape or four-dwarf closure'}
out=Path(__file__).parent/'transport_runs';out.mkdir(exist_ok=True)
def encode_numpy(value):
    if isinstance(value,np.generic):
        return value.item()
    raise TypeError(type(value).__name__)
(out/(args.tag+'.json')).write_text(json.dumps(result,indent=2,default=encode_numpy)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2,default=encode_numpy),flush=True)
