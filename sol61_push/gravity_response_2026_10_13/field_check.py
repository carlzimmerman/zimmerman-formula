#!/usr/bin/env python3
"""Nonlinear periodic Gross-Pitaevskii-Poisson response with a fixed baryon mode.
Dimensionless J=hbar=m=rho0=1. Source elimination/condensate are input hypotheses.
"""
import json,sys
from pathlib import Path
import numpy as np

def evolve(eps,B,N,dt,T=3.):
 x=2*np.pi*np.arange(N)/N;k=2*np.pi*np.fft.fftfreq(N,d=2*np.pi/N)
 inv=np.zeros(N);inv[k!=0]=-1/k[k!=0]**2
 psi=np.ones(N,dtype=complex);g=.75+eps;Phi_b=-B*np.cos(x)
 kin=np.exp(-.5j*k*k*dt);steps=round(T/dt)
 for _ in range(steps):
  rho=abs(psi)**2;Phi=np.fft.ifft(np.fft.fft(rho-1)*inv).real+Phi_b
  psi*=np.exp(-.5j*dt*(g*(rho-1)+Phi))
  psi=np.fft.ifft(np.fft.fft(psi)*kin)
  rho=abs(psi)**2;Phi=np.fft.ifft(np.fft.fft(rho-1)*inv).real+Phi_b
  psi*=np.exp(-.5j*dt*(g*(rho-1)+Phi))
 rho=abs(psi)**2
 amp=float(2*np.mean((rho-1)*np.cos(x)))
 deriv=np.fft.ifft(1j*k*np.fft.fft(psi))
 Phi_s=np.fft.ifft(np.fft.fft(rho-1)*inv).real
 energy=float(np.mean(abs(deriv)**2/2+g*(rho-1)**2/2+(rho-1)*Phi_s/2+Phi_b*rho))
 return dict(amplitude=amp,mass_mean=float(np.mean(rho)),minimum_density=float(min(rho)),
             energy_error_over_B2=energy/(B*B))
rows=[];checks=[]
for eps in [1e-4,.01,1.]:
 for B in [1e-4,1e-3]:
  fine=evolve(eps,B,128,.002);coarse=evolve(eps,B,64,.004)
  exact=B*2*np.sin(np.sqrt(eps)*3/2)**2/eps
  relative=abs(fine['amplitude']/exact-1)
  resolution=abs(fine['amplitude']-coarse['amplitude'])/B
  passed=(relative<3e-4 and resolution<3e-5 and abs(fine['mass_mean']-1)<1e-10
          and abs(fine['energy_error_over_B2'])<1e-4 and fine['minimum_density']>0)
  rows.append(dict(epsilon=eps,baryon_amplitude=B,static_total_gain=1+1/eps,
                   finite_time_total_gain=1+fine['amplitude']/B,linear_predicted_amplitude=float(exact),
                   relative_linear_error=float(relative),coarse_fine_amplitude_difference_over_B=float(resolution),
                   fine=fine,coarse=coarse))
  checks.append(dict(epsilon=eps,B=B,passed=bool(passed)))
r=dict(all_passed=all(c['passed'] for c in checks),checks=checks,cases=rows,
       scope='Six finite nonlinear periodic scalar-field cases. Condensate and source-eliminated contact are stipulated; no full two-field action, cosmology, light coupling, or metric modification.')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
sys.exit(0 if r['all_passed'] else 1)
