import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from free_formation import FreeVacuum
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=FreeVacuum();f=json.loads(Path('physical_completion_2026_10_25/run_free_finish/results.json').read_text());r=f['formed'];mass=np.array(r['mass']);q=np.array(r['q']);rad=np.array(r['r']);gd=m.A.numpy()@mass;gb=m.r.numpy()/(m.r.numpy()**2+m.b**2)**1.5;Phi=-m.A.numpy().T@(m.vol.numpy()*(gd+gb))-sum(mass)/m.R-1/np.sqrt(m.R*m.R+m.b*m.b);outside=rad>1.2*r['scaled_boundary_kpc'];capacity=float((-mass*(1-q)*Phi)[outside].sum());release=f['released_energy_Eunit'];threshold=1-capacity/release;out={'released_energy_Eunit':release,'outer_F_gravitational_escape_upper_bound_Eunit':capacity,'minimum_export_fraction_if_unexported_energy_heats_outer_F':threshold,'qualification':'The escape estimate omits existing thermal energy and is an upper bound on extra heat capacity. The mode experiment assumes oscillation energy has already been supplied; it does not derive pumping from galaxy collapse.'}
k=.5;gamma=.005
def rhs(t,z):
 s,p,x,px,Q=z;return [p,-(s-1)+px*px/s**3-s*k*k*x*x,px/s**2,-s*s*k*k*x-gamma*px,gamma*px*px/s**2]
def energy(z):
 s,p,x,px,Q=z;return .5*p*p+.5*(s-1)**2+.5*px*px/s**2+.5*s*s*k*k*x*x
z0=np.array([1.2,0.,1e-6,0.,0.]);tt=np.linspace(0,12000,60001);sol=solve_ivp(rhs,[0,12000],z0,t_eval=tt,method='DOP853',rtol=1e-10,atol=1e-13);assert sol.success;E=energy(sol.y);E0=energy(z0);balance=E+sol.y[4];frac=float(sol.y[4,-1]/E0);out.update(radiated_fraction=frac,passes_derived_heat_capacity_threshold=bool(frac>threshold),energy_balance_relative_error=float(max(abs(balance/E0-1))),duration_radial_frequency_units=12000,time=tt[::20].tolist(),radiated_history=(sol.y[4,::20]/E0).tolist(),residual_radial_history=((.5*sol.y[1,::20]**2+.5*(sol.y[0,::20]-1)**2)/E0).tolist());assert out['energy_balance_relative_error']<1e-6;dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if not isinstance(v,list)},flush=True)
