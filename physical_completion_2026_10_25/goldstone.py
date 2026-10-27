"""Canonical polar-field energy transfer; finite Fourier-mode radiation prototype."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[],'scope':'Homogeneous radial oscillator plus one angular Fourier mode; passive escape damping. Not a galaxy-formation calculation or a quantum emission-rate derivation.'}
for k,gamma in [(.5,0),(.5,.005),(1.5,.005)]:
 def rhs(t,z):
  s,p,x,px,Q=z;return [p,-(s-1)+px*px/s**3-s*k*k*x*x,px/s**2,-s*s*k*k*x-gamma*px,gamma*px*px/s**2]
 def energy(z):
  s,p,x,px,Q=z;return .5*p*p+.5*(s-1)**2+.5*px*px/s**2+.5*s*s*k*k*x*x
 z0=np.array([1.2,0.,1e-6,0.,0.]);t=np.linspace(0,2400,24001);sol=solve_ivp(rhs,[0,2400],z0,t_eval=t,method='DOP853',rtol=1e-10,atol=1e-13);assert sol.success;E=energy(sol.y);E0=energy(z0);balance=E+sol.y[4];frac=sol.y[4,-1]/E0;run={'wave_number_over_radial_frequency':k,'escape_damping_over_radial_frequency':gamma,'radiated_fraction_final':float(frac),'maximum_angular_mode_energy_fraction':float(max((.5*sol.y[3]**2/sol.y[0]**2+.5*sol.y[0]**2*k*k*sol.y[2]**2)/E0)),'energy_balance_relative_error':float(max(abs(balance/E0-1))),'minimum_radial_amplitude':float(min(sol.y[0])),'samples':len(t),'time':t[::20].tolist(),'radiated_fraction':(sol.y[4,::20]/E0).tolist(),'radial_energy_fraction':((.5*sol.y[1,::20]**2+.5*(sol.y[0,::20]-1)**2)/E0).tolist()};assert run['energy_balance_relative_error']<1e-6;out['runs'].append(run);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in run.items() if not isinstance(v,list)},flush=True)
