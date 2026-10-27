"""Audit bare carrier inertia and fixed-background mean-field detuning."""
import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from two_field import TwoField
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
m=TwoField(J=30);r=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());marg=json.loads(Path('selective_stress_2026_10_25/run_reservoir_halo_margin/results.json').read_text());n=m.n;mass=np.array(r['mass']);rho=mass/m.vol.numpy();q=np.array(r['q']);x=np.array(r['v'][n:2*n]);u=m.A.numpy()@(mass*q);F=u*u/(1-u);A=m.volume_cost+m.J*rho+m.beta*.95*F/(np.pi**2/4)
a0=np.array(marg['outer_margin'])+m.J*m.J*rho/A;delta=a0-m.J;gap=np.sqrt(m.J*m.J+delta*delta+2*m.J*delta*np.cos(np.pi*x));theta_x=np.pi/2*m.J*(m.J+delta*np.cos(np.pi*x))/(gap*gap)
k=(m.material_length/m.rm)**2;Icorr=float(np.sum(2*k*mass*theta_x**2*x*x/gap));Mt=float(mass@q);Ilead=k*Mt*np.pi**2/(2*m.J)
kpc=3.085677581491367e19;vunit=np.sqrt(9.3603e-11*m.rm*kpc);cbar=299792458/vunit;Z=(m.vacuum_length/m.rm)**2+m.ell2*F;Ibare=float(m.vol.numpy()@(Z*x*x)/cbar**2);core=(q>.99)&(np.array(r['r'])<.9*r['scaled_boundary_kpc'])
out={'scope':'Local onsite diagonal detuning on the already computed static background, with its global response derivative frozen; not the full nonlocal dynamical Hessian or a formation path.','minimum_internal_gap_in_core':float(min(gap[core])),'maximum_absolute_core_detuning_over_J':float(max(abs(delta[core]))/m.J),'alignment_only_collective_inertia':Ilead,'frozen_detuning_corrected_inertia':Icorr,'corrected_over_leading':Icorr/Ilead,'bare_Lorentz_carrier_inertia':Ibare,'bare_carrier_over_leading_material':Ibare/Ilead,'formula':'gap²=J²+Delta²+2JDelta cos(pi x); theta_ground_x=(pi/2)J(J+Delta cos(pi x))/gap²; I=integral2kappa rho(theta_ground_x)² x_mode²/gap; x_mode=x_static.','non_claims':['No exact transport inertia or full nonlinear spinor mode derived','Background densities and response derivative fixed; this is a correction-size audit','No gap along the entire all-F-to-galaxy path certified']}
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
