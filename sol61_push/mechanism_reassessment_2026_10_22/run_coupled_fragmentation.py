"""Finite-band classical-statistical continuation of a vacuum-built source.

This is a controlled EARLY-stage probe, not a full quantum relic calculation.
Long modes: 55 stochastic e-folds from zero, then 5 drift-only e-folds.
Resolved modes: constant-background de Sitter Hankel covariance at a=1.
Missing intermediate IR modes and UV vacuum modes are explicitly excluded.
"""
import json, sys, subprocess
from pathlib import Path
import numpy as np
from scipy.special import hankel1, h1vp

HERE=Path(__file__).parent
outdir=Path(sys.argv[1]); outdir.mkdir(exist_ok=True)
H=1.3445177278709404e10; lam=.00881292; m=.001
M=2*m*np.sqrt(1+.02**2); g=2.168e-6
rng=np.random.default_rng(2026102201)
fields=np.zeros((4096,4)); dt=.01

def drift(z):
 f1,f2,x1,x2=z.T; r=f1*f1+f2*f2; c=np.sqrt(2)*g/H
 return -np.array([(m/H)**2*f1+c*(x1*f1+x2*f2)+lam*r*f1,
  (m/H)**2*f2+c*(-x1*f2+x2*f1)+lam*r*f2,
  (M/H)**2*x1+g/(np.sqrt(2)*H)*(f1*f1-f2*f2),
  (M/H)**2*x2+c*f1*f2]).T/3

for j in range(6000):
 fields+=dt*drift(fields)
 if j<5500: fields+=np.sqrt(dt)/(2*np.pi)*rng.standard_normal(fields.shape)
phi2=np.sum(fields[:,:2]**2,axis=1); x2=np.sum(fields[:,2:]**2,axis=1)
index=int(np.argmin((np.log(phi2/np.median(phi2)))**2+(np.log(x2/np.median(x2)))**2))
background=fields[index].copy()
theta=np.arctan2(background[1],background[0])
ph=(background[0]+1j*background[1])*np.exp(-1j*theta)
xx=(background[2]+1j*background[3])*np.exp(-2j*theta)
background=np.array([ph.real,ph.imag,xx.real,xx.imag])
velocity=drift(background[None,:])[0]
radial=background[0]
A=(radial**4+2*(radial+velocity[0])**2/lam)**.25
omega_over_H=np.sqrt(lam)*A; b=1/omega_over_H
mp=m/(H*omega_over_H); mx=M/(H*omega_over_H)
c0=g/(np.sqrt(2)*lam*H*A)

def initial(n,L,seed,cutoff):
 # Common Fourier coefficients on 64^3: coarse and refined initial data
 # represent exactly the same retained Fourier realization.
 master=64; S=master**3
 rr=np.random.default_rng(seed)
 noise=np.fft.fftn(rr.standard_normal((8,master,master,master)),axes=(1,2,3))/np.sqrt(S)
 modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
 ix=modes%master
 noise=noise[:,ix,:,:][:,:,ix,:][:,:,:,ix]
 kk=2*np.pi*np.fft.fftfreq(n,d=L/n)
 k=np.sqrt(kk[:,None,None]**2+kk[None,:,None]**2+kk[None,None,:]**2)
 kh=k*omega_over_H
 selected=(kh>=np.exp(-5))&(kh<=cutoff)&(k>0)
 q=np.zeros((4,n,n,n)); v=q.copy(); covariances=[]
 mass2=[3*lam*radial**2+(m/H)**2,lam*radial**2+(m/H)**2,(M/H)**2,(M/H)**2]
 for s in range(4):
  nu=np.sqrt(2.25-mass2[s]); arg=kh[selected]
  u=np.sqrt(np.pi)/2*hankel1(nu,arg)
  up=-np.sqrt(np.pi)/2*(.5*hankel1(nu,arg)+arg*h1vp(nu,arg))/omega_over_H
  pref=omega_over_H**1.5/A
  P=np.zeros_like(k); cross=P.copy(); resid=P.copy()
  P[selected]=pref*np.abs(u)
  cross[selected]=pref*np.real(np.conj(u)*up)/np.abs(u)
  # Wronskian fixes the conditional variance without catastrophic
  # cancellation for squeezed long modes.
  resid[selected]=pref/(2*omega_over_H*np.abs(u))
  scale=n**3/L**1.5
  q[s]=np.fft.ifftn(scale*P*noise[2*s]).real+background[s]/A
  v[s]=np.fft.ifftn(scale*(cross*noise[2*s]+resid*noise[2*s+1])).real+(background[s]+velocity[s])/(omega_over_H*A)
  covariances.append(float(np.sum(P**2)/L**3))
 return q,v,dict(retained_modes=int(np.count_nonzero(selected)),
   covariance_variances=covariances,lowest_retained_k_over_H=float(np.min(kh[selected])),
   highest_retained_k_over_H=float(np.max(kh[selected])),nu=[float(np.sqrt(2.25-x)) for x in mass2])

cases=[('base',32,32.,.04,2026102202,.35,1.),
       ('time',32,32.,.02,2026102202,.35,1.),
       ('space',64,32.,.02,2026102202,.35,1.),
       ('uncoupled',32,32.,.04,2026102202,.35,0.)]
rows=[]
for name,n,L,step,seed,cutoff,coupling in cases:
 q,v,ic=initial(n,L,seed,cutoff)
 path=outdir/(name+'_initial.bin')
 with path.open('wb') as f:
  np.array([n,L,step,200.,b,mp,mx,c0*coupling,1.],dtype='<f8').tofile(f)
  q.astype('<f8').tofile(f); v.astype('<f8').tofile(f)
 subprocess.run([str(HERE/'coupled_field_lattice'),str(path),str(outdir/(name+'.csv')),str(outdir/(name+'_final.bin'))],check=True)
 table=np.genfromtxt(outdir/(name+'.csv'),delimiter=',',names=True)
 final=np.fromfile(outdir/(name+'_final.bin'),dtype='<f8').reshape(2,4,n,n,n)
 transform=np.fft.fftn(final[0,:2],axes=(1,2,3))/n**3
 kk=2*np.pi*np.fft.fftfreq(n,d=L/n)
 kfd2=4/(L/n)**2*(np.sin(kk[:,None,None]*(L/n)/2)**2+np.sin(kk[None,:,None]*(L/n)/2)**2+np.sin(kk[None,None,:]*(L/n)/2)**2)
 k2=kk[:,None,None]**2+kk[None,:,None]**2+kk[None,None,:]**2
 power=np.sum(np.abs(transform)**2,axis=0)
 gradient=.5*kfd2*power
 uv=k2>(.6*np.pi/(L/n))**2
 late=table['z']>=150
 E0=table['Econf'][0]
 frac=table['phi_variance']/(table['phi_variance']+table['phi_mean_squared'])
 rolling=np.convolve(table['phi_variance'],np.ones(10),'valid')/np.convolve(table['phi_variance']+table['phi_mean_squared'],np.ones(10),'valid')
 crossing=np.flatnonzero(rolling>.5)
 ratio_x=table['X_mean_physical_squared'][-1]/table['X_mean_physical_squared'][0]
 denom=table['phi_kinetic_physical']+table['phi_gradient']+table['phi_potential']
 pressure=table['phi_kinetic_physical']-table['phi_gradient']/3-table['phi_potential']
 row=dict(name=name,n=n,L=L,dt=step,initial_covariance=ic,
   energy_work_residual=float(np.max(np.abs(table['Econf']-table['work']-E0))/abs(E0)),
   charge_absolute_drift=float(np.max(np.abs(table['charge']-table['charge'][0]))),
   first_sample_variance_fraction_above_half=float(table['z'][crossing[0]+9]) if len(crossing) else None,
   late_variance_fraction=float(np.sum(table['phi_variance'][late])/np.sum((table['phi_variance']+table['phi_mean_squared'])[late])),
   late_gradient_fraction=float(np.mean(table['phi_gradient'][late]/denom[late])),
   late_pressure_over_energy=float(np.sum(pressure[late])/np.sum(denom[late])),
   final_uv_gradient_fraction=float(np.sum(gradient[uv])/np.sum(gradient)),
   final_X_mean_physical_squared_ratio=float(ratio_x),
   final_H_over_M=float(H/(1+b*200)**2/M),
   minimum_nonzero_p_over_m=float(H*omega_over_H*2*np.pi/L/(1+b*200)/m))
 rows.append(row); print(json.dumps(row),flush=True)
 # Keep final states and diagnostics; initial files are retained as evidence.

base,time,space,uncoupled=rows
checks=dict(energy_balance=all(r['energy_work_residual']<.002 for r in rows),
 charge_conservation=all(r['charge_absolute_drift']<1e-9 for r in rows),
 timestep_observable=abs(time['late_variance_fraction']-base['late_variance_fraction'])<.05,
 spatial_observable=abs(space['late_variance_fraction']-time['late_variance_fraction'])<.1,
 resolved_cascade=all(r['final_uv_gradient_fraction']<.05 for r in rows))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,
 source=dict(H_GeV=H,stochastic_seed=2026102201,patch_index=index,
   background_over_H=background.tolist(),conformal_scale_over_H=float(A),
   omega_over_H=float(omega_over_H),cubic_coefficient=float(c0),
   coarse_stochastic_efolds=55,drift_only_efolds=5),
 scope='Conditional finite-band classical-statistical early fragmentation, with all original vertices. Constant-background Hankel matching, a representative coarse patch, and omitted intermediate IR/UV modes limit quantum interpretation. No late cold relic or dilute quantum collision kinetics.')
(outdir/'results.json').write_text(json.dumps(out,indent=2))
sys.exit(0 if out['all_pass'] else 1)
