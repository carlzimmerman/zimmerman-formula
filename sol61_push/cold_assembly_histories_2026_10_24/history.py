"""Wave response to paid gas histories with paired massless stellar tracers."""
import argparse,json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.fft import fftn,ifftn,fftfreq
from scipy.ndimage import map_coordinates

p=argparse.ArgumentParser()
p.add_argument('--history',choices=['quiet','early','late','slow'],required=True)
p.add_argument('--tag',required=True);p.add_argument('--n',type=int,default=64)
p.add_argument('--L',type=float,default=32.)
a=p.parse_args();N=a.n;L=a.L;dx=L/N;dv=dx**3;eta=.7;dt=.06;T=60.;steps=round(T/dt)
x=(np.arange(N)-N/2)*dx;X,Y,Z=np.meshgrid(x,x,x,indexing='ij',sparse=True)
r2=X*X+Y*Y+Z*Z;r=np.sqrt(r2);inner=r<3
k=2*np.pi*fftfreq(N,d=dx);kx,ky,kz=np.meshgrid(k,k,k,indexing='ij',sparse=True)
k2=kx*kx+ky*ky+kz*kz;kernel=np.zeros_like(k2)
np.divide(-4*np.pi,k2,out=kernel,where=k2!=0)
kin=np.exp(-.5j*eta*k2*dt);damp=np.exp(-dt*.15*(np.maximum(r-12,0)/4)**4)
rc=np.exp(-((X/4)**2+(Y/2)**2+(Z/2)**2))/(math.pi**1.5*16)
re=np.exp(-r2/25)/(math.pi**1.5*125)
taper=np.where(r<=10,1.,np.where(r<12,np.cos(np.pi*(r-10)/4)**4,0.))
rho=(.8*rc+.2*re)*taper
phase=np.exp(-r2/50)*(-.03*r2/2+.03*X*Y)
psi=np.sqrt(rho)*np.exp(1j*phase/eta);psi/=math.sqrt(float(np.sum(abs(psi)**2)*dv))
order=np.argsort(r.ravel());sr=r.ravel()[order]
radial_grid=np.linspace(0,math.sqrt(3)*L/2,240)

def ag(t):
    if a.history=='quiet':return 1.
    start=25. if a.history=='late' else 5.
    if t<=start or t>=start+30:return 1.
    phase=(t-start)%10
    outward=5. if a.history=='slow' else 1.
    if phase<outward:return 1+2*(1-math.cos(math.pi*phase/outward))
    return 1+2*(1+math.cos(math.pi*(phase-outward)/(10-outward)))

def baryon_phi(t):return -.02/np.sqrt(r2+1)-.2/np.sqrt(r2+ag(t)**2)
def potential(w):return ifftn(kernel*fftn(abs(w)**2,workers=1),workers=1).real
def grad_phi(ph):
    pk=fftn(ph,workers=1)
    return [ifftn(1j*axis*pk,workers=1).real for axis in [kx,ky,kz]]

def q(w,ph,pb):
    den=abs(w)**2;wk=fftn(w,workers=1)
    K=float(.5*eta**2*np.sum(k2*abs(wk)**2)*dv/N**3)
    W=float(.5*np.sum(den*ph)*dv);B=float(np.sum(den*pb)*dv)
    wx=ifftn(1j*kx*wk,workers=1);wy=ifftn(1j*ky*wk,workers=1)
    jd=eta*np.imag(np.conj(w)*(X*wy-Y*wx))
    return {'M':float(den.sum()*dv),'E':K+W+B,'K':K,'Wself':W,'Wexternal':B,
            'J':float(jd.sum()*dv),'M_inner':float(den[inner].sum()*dv),
            'J_inner':float(jd[inner].sum()*dv)},den

def force(pos,gc,t):
    coords=(pos.T+L/2)/dx
    fc=np.column_stack([-map_coordinates(g,coords,order=1,mode='grid-wrap',prefilter=False) for g in gc])
    rr=np.linalg.norm(pos,axis=1);safe=np.maximum(rr,1e-12)
    gn=.02*rr/(rr*rr+1)**1.5+.2*rr/(rr*rr+ag(t)**2)**1.5
    extra=.5*(np.sqrt(gn*gn+4*.05*gn)-gn)
    return fc-(gn+extra)[:,None]*pos/safe[:,None]

rng=np.random.default_rng(7403)
u=rng.uniform(size=1024);rstar=1/np.sqrt(u**(-2/3)-1);rstar=rstar[rstar<6][:512]
assert len(rstar)==512
direction=rng.normal(size=(512,3));direction/=np.linalg.norm(direction,axis=1)[:,None]
pos=rstar[:,None]*direction
normal=rng.normal(size=(512,3));tangent=np.cross(direction,normal);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
den0=abs(psi)**2;massenc=np.cumsum(den0.ravel()[order])*dv
mc=np.interp(rstar,sr,massenc)
gn=.02*rstar/(rstar*rstar+1)**1.5+.2*rstar/(rstar*rstar+1)**1.5
extra=.5*(np.sqrt(gn*gn+4*.05*gn)-gn)
vel=tangent*np.sqrt(mc/rstar+(gn+extra)*rstar)[:,None]
fpos=pos.copy();fvel=vel.copy()
ph=potential(psi);gc=grad_phi(ph);frozen_gc=[g.copy() for g in gc]
removed={'M':0.,'E':0.,'J':0.};work=0.;pb=baryon_phi(0)

def star_diag(z,v):
    centered=v-v.mean(axis=0)
    return {'sigma_trace':float(np.mean(np.sum(centered*centered,axis=1))/3),
            'rhalf':float(np.median(np.linalg.norm(z,axis=1))),'rmax':float(np.max(np.linalg.norm(z,axis=1)))}
def snap(t):
    total,den=q(psi,ph,pb);cdf=np.cumsum(den.ravel()[order])*dv
    return {'t':t,**total,'J_outer':total['J']-total['J_inner'],
        'M_outer':total['M']-total['M_inner'],'rhalf':float(sr[np.searchsorted(cdf,total['M']/2)]),
        'cdf_M':np.interp(radial_grid,sr,cdf,left=0,right=total['M']).tolist(),
        'gas_scale':ag(t),'work_external':work,'removed':dict(removed),
        'stars':star_diag(pos,vel),'stars_frozen':star_diag(fpos,fvel)}

start=time.time();initial=snap(0);hist=[initial]
for n in range(steps):
    t=n*dt;pm=baryon_phi(t+dt/2);pn=baryon_phi(t+dt)
    work+=float(np.sum(abs(psi)**2*(pm-pb))*dv)
    vel+=.5*dt*force(pos,gc,t);pos+=dt*vel
    fvel+=.5*dt*force(fpos,frozen_gc,0);fpos+=dt*fvel
    psi*=np.exp(-.5j*(ph+pm)*dt/eta)
    psi=ifftn(fftn(psi,workers=1)*kin,workers=1)
    ph=potential(psi);psi*=np.exp(-.5j*(ph+pm)*dt/eta)
    work+=float(np.sum(abs(psi)**2*(pn-pm))*dv);pb=pn
    before,_=q(psi,ph,pb);psi*=damp;ph=potential(psi);after,_=q(psi,ph,pb)
    for key in removed:removed[key]+=before[key]-after[key]
    gc=grad_phi(ph)
    vel+=.5*dt*force(pos,gc,t+dt);fvel+=.5*dt*force(fpos,frozen_gc,0)
    if (n+1)%25==0:hist.append(snap((n+1)*dt))
final=hist[-1];tail=[h for h in hist if h['t']>=45]
mr=final['M']+removed['M']-initial['M']
er=(final['E']+removed['E']-initial['E']-work)/abs(initial['E'])
jr=(final['J']+removed['J']-initial['J'])/abs(initial['J'])
mratio=final['M_inner']/initial['M_inner']
jratio=abs(final['J_inner']/final['M_inner'])/abs(initial['J_inner']/initial['M_inner'])
late=[h['M_inner'] for h in tail]
result={'parameters':{'N':N,'L':L,'dt':dt,'T':T,'eta':eta,'history':a.history,'gas_mass':.2,'stellar_source_mass':.02,'a0':.05},
 'initial':initial,'final':final,'history':hist,'radial_grid':radial_grid.tolist(),
 'M_residual':mr,'E_residual':er,'J_residual':jr,'external_work':work,
 'inner_mass_ratio':mratio,'inner_specific_spin_ratio':jratio,
 'late_star_sigma_over_frozen':float(np.mean([h['stars']['sigma_trace'] for h in tail])/np.mean([h['stars_frozen']['sigma_trace'] for h in tail])),
 'late_star_rhalf_over_frozen':float(np.mean([h['stars']['rhalf'] for h in tail])/np.mean([h['stars_frozen']['rhalf'] for h in tail])),
 'gates':{'M_ledger':abs(mr)<=1e-8,'E_work_ledger':abs(er)<=.01,'J_ledger':abs(jr)<=.02,
          'mass_retained_old_Sextans':removed['M']<=.01146,'central_mass_gain':mratio>=1.25,
          'specific_spin_reduced':jratio<=.5,'late_mass_stable':(max(late)-min(late))/np.mean(late)<=.1,
          'old_Sextans_central_fraction':final['M_inner']>=.9885403473237517},
 'elapsed_s':time.time()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'scope':'prescribed paid gas forcing; massless nonequilibrium tracer response; no empirical four-dwarf or covariant closure'}
def encode(v):
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)
out=Path(__file__).parent/'runs';out.mkdir(exist_ok=True)
(out/(a.tag+'.json')).write_text(json.dumps(result,indent=2,default=encode)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['initial','final','history','radial_grid']},indent=2,default=encode),flush=True)
