#!/usr/bin/env python3
"""Spatial two-field conversion with leading Newtonian gravity, periodic 1D.
Dimensionless kinetic masses 1 and 2; detuning is a separate slow energy.
No photons, external pump, source elimination, or new gravitational interaction.
"""
import json,sys
from pathlib import Path
import numpy as np

def evolve(c,alpha,N,dt,T=30.):
 x=2*np.pi*np.arange(N)/N;ks=np.fft.fftfreq(N,1/N);inv=np.zeros(N);inv[ks!=0]=-1/ks[ks!=0]**2
 p=.01*(1+.5*np.cos(x))+0j;b=np.sqrt((2-abs(p)**2)/2)+0j
 delta=1.;k=.35
 def potential(p,b):
  q=abs(p)**2+2*abs(b)**2
  return alpha*np.fft.ifft(np.fft.fft(q-q.mean())*inv).real
 def local(p,b,phi):
  return (-1j*(2*c*b*p.conjugate()+2*k*abs(p)**2*p+phi*p),
          -1j*(delta*b+c*p*p+2*phi*b))
 def diag(p,b):
  q=abs(p)**2+2*abs(b)**2;phi=potential(p,b)
  px=np.fft.ifft(1j*ks*np.fft.fft(p));bx=np.fft.ifft(1j*ks*np.fft.fft(b))
  kinetic=np.mean(abs(px)**2/2+abs(bx)**2/4)
  energy=kinetic+np.mean(delta*abs(b)**2+2*c*(b.conjugate()*p*p).real+k*abs(p)**4+q*phi/2)
  force=-np.fft.ifft(1j*ks*np.fft.fft(phi)).real
  current=(p.conjugate()*px+b.conjugate()*bx).imag
  return dict(charge=float(q.mean()),energy=float(energy),kinetic=float(kinetic),
    daughter_fraction=float(np.mean(abs(p)**2)/q.mean()),
    density_mode=float(2*abs(np.mean(q*np.exp(-1j*x)))),
    max_density_contrast=float(max(abs(q-2))),max_force=float(max(abs(force))),
    momentum=float(current.mean()),max_current=float(max(abs(current))))
 first=diag(p,b);series=[dict(time=0.,**first)]
 hp=np.exp(-.25j*ks**2*dt);hb=np.exp(-.125j*ks**2*dt)
 sample=max(1,round(.1/dt))
 for step in range(round(T/dt)):
  p=np.fft.ifft(hp*np.fft.fft(p));b=np.fft.ifft(hb*np.fft.fft(b))
  phi=potential(p,b)
  a1,b1=local(p,b,phi);a2,b2=local(p+dt*a1/2,b+dt*b1/2,phi)
  a3,b3=local(p+dt*a2/2,b+dt*b2/2,phi);a4,b4=local(p+dt*a3,b+dt*b3,phi)
  p+=dt*(a1+2*a2+2*a3+a4)/6;b+=dt*(b1+2*b2+2*b3+b4)/6
  p=np.fft.ifft(hp*np.fft.fft(p));b=np.fft.ifft(hb*np.fft.fft(b))
  if (step+1)%sample==0:series.append(dict(time=(step+1)*dt,**diag(p,b)))
 return dict(c=c,alpha=alpha,N=N,dt=dt,initial=first,final=series[-1],
  max_charge_error=max(abs(s['charge']-first['charge']) for s in series),
  max_energy_error=max(abs(s['energy']-first['energy']) for s in series),
  max_momentum_error=max(abs(s['momentum']-first['momentum']) for s in series),
  max_density_mode=max(s['density_mode'] for s in series),
  max_daughter_fraction=max(s['daughter_fraction'] for s in series),
  max_force=max(s['max_force'] for s in series),series=series)

G=6.67430e-11;hbar=1.054571817e-34;eV=1.602176634e-19;clight=299792458.
mass=1e6*eV/clight**2;gap=5*eV;t0=hbar/gap;x0=hbar/np.sqrt(mass*gap)
physical_alpha=4*np.pi*G*1000*t0*t0/2
cases=[];checks=[]
for c,alpha in [(0.,.02),(.3,0.),(.3,.02),(.5,.02),(.3,physical_alpha)]:
 runs=[evolve(c,alpha,64,.005),evolve(c,alpha,64,.0025),evolve(c,alpha,128,.0025)]
 a,b,d=runs
 temporal=max(abs(x['density_mode']-y['density_mode']) for x,y in zip(a['series'],b['series']))
 spatial=max(abs(x['density_mode']-y['density_mode']) for x,y in zip(b['series'],d['series']))
 check=dict(c=c,alpha=alpha,time_refinement_mode_error=temporal,space_refinement_mode_error=spatial,
  passed=bool(temporal<.002 and spatial<.002 and all(r['max_charge_error']<1e-7 and r['max_energy_error']<1e-4 and r['max_momentum_error']<1e-7 for r in runs)))
 checks.append(check);cases.append(dict(c=c,alpha=alpha,runs=runs));print(json.dumps(check),flush=True)
scale=dict(mass_eV=1e6,gap_eV=5,t0_seconds=t0,x0_meters=x0,period_meters=2*np.pi*x0,
 mean_density_for_alpha_point02=2*.02/(4*np.pi*G*t0*t0),
 alpha_for_mean_density_1000=physical_alpha,
 max_acceleration_m_s2_at_density_1000=cases[-1]['runs'][-1]['max_force']*x0/t0**2)
result=dict(all_passed=all(c['passed'] for c in checks),checks=checks,cases=cases,
 physical_scale=scale,
 scope='Five finite periodic planar two-field cases. Leading Newtonian gravity and prepared spatial seed assumed; no optical feedback, finite spherical apparatus, or new gravity law.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
sys.exit(0 if result['all_passed'] else 1)
