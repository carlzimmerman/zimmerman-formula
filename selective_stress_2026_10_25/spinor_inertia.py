"""Gapped internal-state conversion inertia from the existing canonical action."""
import argparse,json,sys
from pathlib import Path
import numpy as np,sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from two_field import TwoField
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
J,sigma,w,M=s.symbols('J sigma w M',positive=True)
# In the instantaneous aligned internal basis the carrier rotation gives an
# off-diagonal inertial coupling sigma*pi*qdot/2. No phase-chart division.
H=s.Matrix([[0,-s.I*sigma*s.pi*w/2],[s.I*sigma*s.pi*w/2,J]])
lam=(J-s.sqrt(J*J+sigma*sigma*s.pi*s.pi*w*w))/2
assert s.simplify((H-lam*s.eye(2)).det())==0
Leff=-M*lam;I=s.simplify(s.diff(Leff,w,2).subs(w,0));assert s.simplify(I-M*sigma*sigma*s.pi*s.pi/(2*J))==0
Hkin=s.simplify(w*s.diff(Leff,w)-Leff);assert s.simplify(Hkin-M*J/2*(1-J/s.sqrt(J*J+sigma*sigma*s.pi*s.pi*w*w)))==0
m=TwoField(J=30);old=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());Mt=float(np.array(old['mass'])@old['q']);release=json.loads(Path('physical_completion_2026_10_25/run_free_finish/results.json').read_text())['released_energy_Eunit'];k=(m.material_length/m.rm)**2
kpc=3.085677581491367e19;Myr=365.25*86400*1e6;v=np.sqrt(9.3603e-11*m.rm*kpc);tdyn=m.rm*kpc/v/Myr;tcross=old['scaled_boundary_kpc']*kpc/299792458/Myr;Ireal=k*Mt*np.pi**2/(2*m.J)
cases=[]
for label,D in [('binding_only',m.eps*Mt),('whole_release_hypothesis',release)]:
 tau=tdyn*np.sqrt(k*Mt/(D*m.J));Enorm=D/.25;Itoy=Ireal/(Enorm*(tcross/tdyn)**2);fraction=D/(Mt*m.J);z=np.sqrt((1-2*fraction)**(-2)-1);vexact_ratio=z/(2*np.sqrt(fraction))
 cases.append({'case':label,'conversion_potential_Eunit':D,'conversion_potential_per_mass':D/Mt,'inverse_bare_conversion_frequency_Myr':tau,'R_over_c_Myr':tcross,'omega_R_over_c':tcross/tau,'prototype_material_inertia_at_D_point25':Itoy,'maximum_energy_over_collective_alignment_gap':fraction,'maximum_rotation_adiabatic_parameter':z/2,'exact_velocity_over_quadratic_velocity_at_maximum_energy':vexact_ratio})
out={'exact_algebra':{'rotating_basis_H':str(H),'lower_eigenvalue':str(lam),'effective_kinetic_Lagrangian':str(Leff),'small_velocity_inertia':str(I),'kinetic_Hamiltonian':str(Hkin)},'canonical_material_time_Myr':np.sqrt(k)*tdyn,'converted_mass_Mb':Mt,'alignment_J':m.J,'collective_inertia_in_old_dynamical_units':Ireal,'cases':cases,'non_claims':['Internal gapped-state elimination assumes near alignment and adiabatic spin following; finite rotation correction quantified','Collective density profile fixed; actual matter transport inertia can be much larger','Binding-only potential excludes the rest of the actual gravitational energy release','Whole-release potential is a separate reduced-path hypothesis, not derived from a mobile-density trajectory','No microscopic derivation of the canonical material action or outgoing coupling']}
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='exact_algebra'},indent=2),flush=True)
