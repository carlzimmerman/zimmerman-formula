"""Autonomous conversion potential, adiabatic modulus, passive phase escape.

Initial energy is conversion potential, not a supplied radial oscillation.
This is a reduced Hamiltonian test, not spatial galaxy formation.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
out={'runs':[],'non_claims':['No spatial density, gravitational collapse or boundary in this reduced model','The cold conversion potential and angular inertia are stipulated, not microscopically derived','Leaky Fourier mode is an approximation to outgoing transport; not a continuum spectral-density calculation']}
for k,gamma,duration in [(.15,.005,12000),(.25,.005,12000),(.5,.005,12000),(1.5,.005,12000),(.25,500.,600),(500.,500.,600)]:
 def rhs(t,z):
  q,P,x,p,Q=z;S=1+np.sin(np.pi*q/2)**2;Sp=np.pi/2*np.sin(np.pi*q);Vq=-np.pi/8*np.sin(np.pi*q)
  return [P,-Vq+Sp*(p*p/S**3-S*k*k*x*x),p/S**2,-S*S*k*k*x-gamma*p,gamma*p*p/S**2]
 def energy(z):
  q,P,x,p,Q=z;S=1+np.sin(np.pi*q/2)**2
  return .5*P*P+.25*np.cos(np.pi*q/2)**2+.5*p*p/S**2+.5*S*S*k*k*x*x
 z0=np.array([1e-4,0.,1e-6,0.,0.]);tt=np.linspace(0,duration,12001)
 sol=solve_ivp(rhs,[0,duration],z0,t_eval=tt,method='Radau' if gamma>1 else 'DOP853',rtol=2e-10,atol=2e-13);assert sol.success
 E=energy(sol.y);E0=energy(z0);q=sol.y[0];conversion=.5*sol.y[1]**2+.25*np.cos(np.pi*q/2)**2
 run={'k_over_conversion_frequency':k,'escape_over_conversion_frequency':gamma,'duration':duration,'radiated_fraction':float(sol.y[4,-1]/E0),'energy_ledger_relative_error':float(max(abs((E+sol.y[4])/E0-1))),'initial_conversion_potential_fraction':float(.25*np.cos(np.pi*z0[0]/2)**2/E0),'initial_angular_energy_fraction':float((E0-.25*np.cos(np.pi*z0[0]/2)**2)/E0),'final_conversion_energy_fraction':float(conversion[-1]/E0),'final_conversion_order':float(np.sin(np.pi*q[-1]/2)**2),'time':tt[::20].tolist(),'radiated_history':(sol.y[4,::20]/E0).tolist(),'conversion_energy_history':(conversion[::20]/E0).tolist()}
 assert run['energy_ledger_relative_error']<2e-5;out['runs'].append(run);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in run.items() if not isinstance(v,list)},flush=True)
