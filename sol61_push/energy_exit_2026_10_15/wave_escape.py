"""Spherical isolated Newtonian wave field. No friction, absorber or target profile."""
import json
from pathlib import Path
import numpy as np
from scipy.fft import dst,idst

def evolve(N,Rbox,dt,G=1.,end=200.):
    dr=Rbox/(N+1);r=dr*np.arange(1,N+1);kk=np.pi*np.arange(1,N+1)/Rbox
    R0=5.; chirp=.03
    u=(r*np.exp(-r*r/(2*R0*R0))*np.exp(-.5j*chirp*r*r)).astype(complex)
    u/=np.sqrt(4*np.pi*dr*np.sum(np.abs(u)**2))
    kinetic=np.exp(-.25j*kk*kk*dt)
    cut=int(round(20/dr))-1
    def potential(v):
        d=np.abs(v)**2
        return -4*np.pi*G*dr*(np.cumsum(d)/r+np.cumsum((d/r)[::-1])[::-1]-d/r)
    def derivative(v):
        ext=np.r_[0.,v,0.,-v[::-1]]
        w=2*np.pi*np.fft.fftfreq(len(ext),d=dr)
        return np.fft.ifft(1j*w*np.fft.fft(ext))[1:N+1]
    def measure(t):
        d=np.abs(u)**2;phi=potential(u);der=derivative(u)
        K=.5*4*np.pi*dr*np.sum(kk*kk*np.abs(dst(u,type=1,norm='ortho'))**2)
        W=.5*4*np.pi*dr*np.sum(d*phi)
        mass=4*np.pi*dr*np.sum(d)
        inside=4*np.pi*dr*(np.sum(d[:cut])+.5*d[cut])
        physicalgrad=der-u/r
        outerK=.5*4*np.pi*dr*np.sum(np.abs(physicalgrad[cut:])**2)
        flux=4*np.pi*float(np.imag(np.conj(u[cut])*der[cut]))
        return dict(t=float(t),mass=float(mass),energy=float(K+W),kinetic=float(K),gravity=float(W),
          mass_inside20=float(inside),outer_kinetic=float(outerK),outward_flux20=flux,
          mass_beyond80pctbox=float(4*np.pi*dr*np.sum(d[r>.8*Rbox])),
          rho_center_extrapolation=float(abs(u[0]/r[0])**2),
          second_moment=float(4*np.pi*dr*np.sum(r*r*d)))
    hist=[measure(0.)]
    stride=round(.2/dt)
    for j in range(round(end/dt)):
        u=idst(dst(u,type=1,norm='ortho')*kinetic,type=1,norm='ortho')
        u*=np.exp(-1j*dt*potential(u))
        u=idst(dst(u,type=1,norm='ortho')*kinetic,type=1,norm='ortho')
        if (j+1)%stride==0:hist.append(measure((j+1)*dt))
    E0=hist[0]['energy'];M0=hist[0]['mass']
    times=np.array([h['t'] for h in hist]);flux=np.array([h['outward_flux20'] for h in hist])
    integ=np.trapz(flux,times)
    finalrho=np.abs(u/r)**2
    return dict(N=N,Rbox=Rbox,dr=dr,dt=dt,G=G,end=end,cut_radius=float(r[cut]),
      initial_radius=R0,initial_chirp=chirp,
      mass_error=max(abs(h['mass']-M0) for h in hist),
      relative_energy_error=max(abs(h['energy']-E0)/abs(E0) for h in hist),
      net_mass_flux20=float(integ),measured_mass_change20=hist[0]['mass_inside20']-hist[-1]['mass_inside20'],
      boundary_guard=max(h['mass_beyond80pctbox'] for h in hist),
      final_outside20_mass=M0-hist[-1]['mass_inside20'],
      max_center_density=max(h['rho_center_extrapolation'] for h in hist),
      initial_center_density=hist[0]['rho_center_extrapolation'],
      history=hist,final_profile=dict(r=r[::8].tolist(),rho=finalrho[::8].tolist()))

rows=[evolve(2047,200.,.02),evolve(4095,200.,.01),evolve(4095,400.,.02),evolve(4095,400.,.02,G=0.)]
checks={}
for i,row in enumerate(rows):
    checks[f'mass_{i}']=row['mass_error']<1e-8
    checks[f'energy_{i}']=row['relative_energy_error']<.002
    checks[f'boundary_{i}']=row['boundary_guard']<1e-6
    checks[f'flux_{i}']=abs(row['net_mass_flux20']-row['measured_mass_change20'])<.002
checks['core_concentration']=rows[1]['max_center_density']>5*rows[1]['initial_center_density']
checks['outward_mass']=rows[1]['final_outside20_mass']>.001
checks['box_agreement']=abs(rows[0]['final_outside20_mass']-rows[2]['final_outside20_mass'])<.002
checks['resolution_agreement']=abs(rows[0]['final_outside20_mass']-rows[1]['final_outside20_mass'])<.003
result=dict(checks={k:bool(v) for k,v in checks.items()},runs=rows,
 nonclaims=['Finite-time wave redistribution, not asymptotic settling','No MOND law or galaxy fit',
 'No charged dark medium in this comparison','No production or vacuum selection',
 'Canonical scalar dilute Newtonian limit; cosmological vacuum gravity neglected'])
Path(__file__).with_name('wave_run_v1').joinpath('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['checks'],indent=2))
print(json.dumps([{k:v for k,v in row.items() if k not in ('history','final_profile')} for row in rows],indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
