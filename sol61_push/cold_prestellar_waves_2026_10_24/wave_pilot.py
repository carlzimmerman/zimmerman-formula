"""Isolated angular-Galerkin Schrodinger-Poisson collapse; CCT-007."""
import argparse,hashlib,json,math,resource,time,subprocess
from pathlib import Path
import numpy as np
from scipy.special import sph_harm
from scipy.linalg.lapack import zgttrf,zgttrs
from numpy.polynomial.legendre import leggauss

p=argparse.ArgumentParser();p.add_argument('--galaxy',required=True,choices=['Draco','Sextans','Fornax','Leo I'])
p.add_argument('--tag',required=True);p.add_argument('--nr',type=int,default=256);p.add_argument('--lmax',type=int,default=2)
p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=60)
p.add_argument('--rmax',type=float,default=40.);p.add_argument('--absorb',type=float,default=24.)
a=p.parse_args();HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
source=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json'
old=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json'
pins=[Path(__file__),HERE/'CONTRACT.md',source,old]
hashes=lambda:{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}
before=hashes();gal=next(g for g in json.loads(source.read_text())['models'] if g['name']==a.galaxy)
obs=json.loads(old.read_text())['galaxies'][a.galaxy]['observations']
G=.00430091;Munit=5.364*200*gal['formed_mass'];Runit=float(obs['rhalf_sph_physical'])
Vunit=math.sqrt(G*Munit/Runit);tunit=.977792*Runit/Vunit;eta=3000/(Runit*Vunit)
nr=a.nr;L=a.lmax;dt=a.dt
r=np.geomspace(1e-4,a.rmax,nr+1)[:-1]
hl=np.diff(np.r_[0.,r]);hr=np.diff(np.r_[r,a.rmax]);w=(hl+hr)/2
diag=(1/hl+1/hr)/w*.5*eta*eta
off=-.5*eta*eta/(hr[:-1]*np.sqrt(w[:-1]*w[1:]))
lm=[(l,m) for l in range(L+1) for m in range(-l,l+1)];nm=len(lm);ms=np.array([m for l,m in lm])
lrho=[(l,m) for l in range(2*L+1) for m in range(-l,l+1)]
cost,wt=leggauss(2*L+2);ph=np.arange(4*L+2)*2*math.pi/(4*L+2)
theta=np.repeat(np.arccos(cost),len(ph));phi=np.tile(ph,len(cost));wa=np.repeat(wt,len(ph))*2*math.pi/len(ph)
Y=np.array([sph_harm(m,l,phi,theta) for l,m in lm]).T
Yrho=np.array([sph_harm(m,l,phi,theta) for l,m in lrho]).T
gram=Y.conj().T@(wa[:,None]*Y);assert np.max(abs(gram-np.eye(nm)))<1e-12
to_rho=wa[:,None]*Yrho.conj()
to_matrix=(wa[:,None,None]*Y.conj()[:,:,None]*Y[:,None,:]).reshape(len(wa),nm*nm)
groups=[]
for l in range(L+1):
    inds=np.array([i for i,(ll,m) in enumerate(lm) if ll==l])
    td=diag+.5*eta*eta*l*(l+1)/r**2
    ds=dt/2;fac=1j*ds/(2*eta)
    fact=zgttrf(np.array(fac*off),np.array(1+fac*td),np.array(fac*off))
    assert fact[-1]==0
    groups.append((inds,td,fact))

def kinetic(v):
    out=np.empty_like(v)
    for inds,td,fact in groups:
        z=v[:,inds];tz=td[:,None]*z
        tz[1:]+=off[:,None]*z[:-1];tz[:-1]+=off[:,None]*z[1:]
        rhs=np.asfortranarray(z-1j*(dt/2)/(2*eta)*tz)
        val,info=zgttrs(*fact[:-1],rhs)
        assert info==0;out[:,inds]=val
    return out
def energy_K(v):
    total=0.
    for inds,td,fact in groups:
        z=v[:,inds]
        total+=float(np.sum(td[:,None]*abs(z)**2)+2*np.real(np.sum(off[:,None]*z[:-1].conj()*z[1:])))
    return total

def self_potential(v,matrix=False):
    vang=v@Y.T
    rho=abs(vang)**2/(w*r*r)[:,None]
    crho=rho@to_rho
    coeff=np.empty_like(crho)
    for j,(l,m) in enumerate(lrho):
        shell=w*r*r*crho[:,j]
        inner=np.cumsum(shell*r**l)/r**(l+1)
        term=shell/r**(l+1)
        outer=(np.cumsum(term[::-1])[::-1]-term)*r**l
        coeff[:,j]=-4*math.pi/(2*l+1)*(inner+outer)
    pang=coeff@Yrho.T
    assert np.max(abs(pang.imag))<1e-8*max(1.,float(np.max(abs(pang.real))))
    pang=pang.real
    W=.5*float(np.sum(abs(vang)**2*pang*wa))
    if not matrix:return coeff,W
    mat=(pang@to_matrix).reshape(nr,nm,nm)
    mat=(mat+mat.swapaxes(1,2).conj())/2
    return mat,coeff,W
def gas(t):
    if t<=4:ag=5.
    elif t<10:ag=3+2*math.cos(math.pi*(t-4)/6)
    else:ag=1.
    frac=1. if t<=16 else (.5*(1+math.cos(math.pi*(t-16)/8)) if t<24 else 0.)
    return -frac/5.364/np.sqrt(r*r+ag*ag)
def apply(v,mat,duration):
    ev,U=np.linalg.eigh(mat)
    z=np.einsum('rij,ri->rj',U.conj(),v)
    return np.einsum('rij,rj->ri',U,z*np.exp(-1j*duration/eta*ev))
def potential_step(v,pg):
    mat,_,_=self_potential(v,True);mat+=pg[:,None,None]*np.eye(nm)
    mid=apply(v,mat,dt/2)
    mat,_,_=self_potential(mid,True);mat+=pg[:,None,None]*np.eye(nm)
    return apply(v,mat,dt)

v=np.zeros((nr,nm),complex)
base=r*np.exp(-r*r/32)*np.exp(-1j*(10/Vunit)/eta*np.sqrt(r*r+.04))
taper=np.where(r<=18,1.,np.where(r<22,np.cos(math.pi*(r-18)/8)**4,0.))
base*=taper
v[:,lm.index((0,0))]=base
for m,amp in [(2,.5),(-2,.15*np.exp(1j*math.pi/3)),(0,.2)]:v[:,lm.index((2,m))]=amp*(r/4)**2*base
v*=np.sqrt(w)[:,None];v/=np.sqrt(np.sum(abs(v)**2))
initial_field=v.copy();removed={'M':0.,'E':0.,'J':0.};work=0.;epos=eneg=0.
damp=np.exp(-dt*.3*(np.maximum(r-a.absorb,0)/(a.rmax-a.absorb))**4)
history=[];start=time.time();finished=True

def diag_state(t,v,pg,coeff=None,W=None):
    if coeff is None:coeff,W=self_potential(v)
    shell=np.sum(abs(v)**2,axis=1);cdf=np.cumsum(shell);mass=float(cdf[-1]);K=energy_K(v)
    Jrad=eta*np.sum(ms[None,:]*abs(v)**2,axis=1);J=float(Jrad.sum())
    B=float(np.sum(shell*pg));u=v/np.sqrt(w)[:,None]
    flux=eta*np.imag(np.sum(u.conj()*np.gradient(u,r,axis=0),axis=1))
    jflux=eta*eta*np.imag(np.sum(ms[None,:]*u.conj()*np.gradient(u,r,axis=0),axis=1))
    ix=np.argmin(abs(r-.85*a.absorb))
    # Spherical-tracer virial diagnostic, using actual monopole cold shell masses.
    aa_phys=[Runit] if a.galaxy!='Sextans' else [434.24183347957097,794.1886040039351]
    cold_sigma2=[float(G*Munit/(3*ar)*np.sum(shell*(1+(r*Runit/ar)**2)**(-1.5))) for ar in aa_phys]
    core=r<1.
    return dict(t=t,M=mass,E=K+W+B,K=K,Wself=W,Wgas=B,J=J,
        M_inner=float(shell[core].sum()),J_inner=float(Jrad[core].sum()),
        rhalf=float(np.interp(mass/2,cdf,r)),r90=float(np.interp(.9*mass,cdf,r)),
        flux_radius=float(r[ix]),outward_mass_flux=float(flux[ix]),outward_J_flux=float(jflux[ix]),
        cold_sigma2_kms2=cold_sigma2,source_work=work,removed=dict(removed),
        absorber_energy_positive=epos,absorber_energy_negative=eneg,
        cdf=cdf.tolist(),mode_mass=[float(x) for x in np.sum(abs(v)**2,axis=0)])

initial=diag_state(0,v,gas(0));history.append(initial)
steps=round(a.T/dt);pg=gas(0.)
for it in range(steps):
    t=it*dt;pm=gas(t+dt/2);pn=gas(t+dt)
    work+=float(np.sum(np.sum(abs(v)**2,axis=1)*(pm-pg)))
    v=kinetic(v);v=potential_step(v,pm);v=kinetic(v)
    work+=float(np.sum(np.sum(abs(v)**2,axis=1)*(pn-pm)));pg=pn
    # Exact finite-Hamiltonian change caused by the artificial sink is ledgered.
    c0,W0=self_potential(v);K0=energy_K(v);m0=float(np.sum(abs(v)**2));J0=float(eta*np.sum(ms[None,:]*abs(v)**2))
    E0=K0+W0+float(np.sum(np.sum(abs(v)**2,axis=1)*pg))
    v*=damp[:,None]
    c1,W1=self_potential(v);K1=energy_K(v);m1=float(np.sum(abs(v)**2));J1=float(eta*np.sum(ms[None,:]*abs(v)**2))
    E1=K1+W1+float(np.sum(np.sum(abs(v)**2,axis=1)*pg))
    removed['M']+=m0-m1;removed['E']+=E0-E1;removed['J']+=J0-J1
    epos+=max(0.,E0-E1);eneg+=min(0.,E0-E1)
    if (it+1)%25==0 or it==steps-1:
        h=diag_state(t+dt,v,pg,c1,W1)
        h['mass_residual']=h['M']+removed['M']-initial['M']
        h['energy_residual']=(h['E']+removed['E']-work-initial['E'])/max(abs(initial['E']),1e-12)
        h['J_residual']=(h['J']+removed['J']-initial['J'])/max(abs(initial['J']),1e-12)
        history.append(h)
        if abs(h['energy_residual'])>.05 or abs(h['J_residual'])>.05:
            finished=False;break
        if (it+1)%250==0:print(a.tag,round(t+dt,3),'M',round(m1,6),'Eres',round(h['energy_residual'],6),'Jres',round(h['J_residual'],6),flush=True)

tail=[h for h in history if h['t']>=max(24.,.75*history[-1]['t'])]
out=dict(parameters=vars(a),physical=dict(eta_pc_kms=3000.,Munit_Msun=Munit,Runit_pc=Runit,Vunit_kms=Vunit,tunit_Myr=tunit,eta_code=eta),
    angular_modes=lm,radial_grid=r.tolist(),radial_weights=w.tolist(),initial=initial,history=history,
    status='finished' if finished else 'stopped numerical ledger gate >5percent',
    stationarity=None if len(tail)<3 else dict(rhalf_range_over_mean=float(np.ptp([h['rhalf'] for h in tail])/np.mean([h['rhalf'] for h in tail])),
       core_mass_range_over_mean=float(np.ptp([h['M_inner'] for h in tail])/max(1e-14,np.mean([h['M_inner'] for h in tail])))),
    seconds=time.time()-start,peak_RSS_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    source_hashes_before=before,source_hashes_after=hashes(),revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
assert before==out['source_hashes_after']
(HERE/'runs').mkdir(exist_ok=True)
(HERE/'runs'/f'{a.tag}.json').write_text(json.dumps(out,indent=2)+'\n')
np.savez_compressed(HERE/'runs'/f'{a.tag}_fields.npz',r=r,w=w,initial=initial_field,final=v,lm=np.array(lm))
print(json.dumps({k:out[k] for k in ['status','seconds','peak_RSS_bytes_macos','stationarity']}),flush=True)
