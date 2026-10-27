"""Exact checks and finite-frequency audit for reciprocal conversion radiation."""
import argparse,json
from pathlib import Path
import numpy as np,sympy as sy
from scipy.integrate import quad
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
d,R=sy.symbols('d R',positive=True);p=3*d**2/R**3*(1-3*d/(4*R)+d**3/(16*R**3))
norm=sy.integrate(p,(d,0,2*R));A0=sy.integrate(p/(4*sy.pi*d),(d,0,2*R));assert sy.simplify(norm-1)==0;assert sy.simplify(A0-3/(10*sy.pi*R))==0
eta=sy.symbols('eta',positive=True);assert sy.simplify(sy.Rational(1,4)-eta/(1+eta)**2-(eta-1)**2/(4*(eta+1)**2))==0
rows=[]
for z in [1e-5,1e-4,.001,.01,.03,.1,.3,1.,3.,10.]:
 fun=lambda x:3*x*(1-3*x/4+x**3/16)/(4*np.pi)
 re=quad(lambda x:fun(x)*np.cos(z*x),0,2,epsabs=1e-13)[0];im=quad(lambda x:fun(x)*np.sin(z*x),0,2,epsabs=1e-13)[0]
 F=1-z*z/10+z**4/280-z**6/15120 if z<.01 else 3*(np.sin(z)-z*np.cos(z))/z**3
 identity_error=abs(im-z*F*F/(4*np.pi));assert identity_error<2e-13
 rows.append({'omega_R_over_c':z,'real_self_kernel_R':re,'imag_self_kernel_R':im,'uniform_sphere_form_factor':F,'retarded_identity_absolute_error':identity_error,'real_kernel_relative_to_static':re/(3/(10*np.pi))})
# Physical units: inverse angular frequency tau=1/omega, NOT the oscillation period.
c=299792458.;kpc=3.085677581491367e19;Myr=365.25*86400*1e6;radius=56.36*kpc;tau=100*Myr
gamma_bound=(radius/c)/tau**2;uniform_bound=5/6*gamma_bound
export=.977191;required=np.log(1/(1-export))
out={'exact_checks':{'distance_probability_normalization':str(norm),'static_self_kernel':str(A0),'optimized_coupling_identity':'1/4-eta/(1+eta)^2=(eta-1)^2/[4(eta+1)^2]'},'finite_frequency_kernel_checks':rows,'physical_example':{'source_radius_kpc':56.36,'inverse_angular_frequency_Myr':100.,'light_crossing_Myr':radius/c/Myr,'omega_R_over_c':radius/(c*tau),'general_compact_source_minimum_energy_efold_Gyr':1/gamma_bound/Myr/1000,'uniform_sphere_minimum_energy_efold_Gyr':1/uniform_bound/Myr/1000,'uniform_sphere_minimum_time_for_export_fraction_Gyr':required/uniform_bound/Myr/1000,'required_export_fraction':export,'fixed_bare_frequency_optimized_coupling_minimum_efold_Gyr':4/uniform_bound/Myr/1000},'non_claims':['Low-frequency linear harmonic conversion coordinate with compact normalized spherical source','No exclusion of rapid bursts, nonspherical channels, slow sound modes, alternate interactions or a different field theory','The 100 Myr inverse angular frequency is a stated example, not a measured formation timescale','Not a full galaxy formation simulation']}
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['physical_example'],indent=2),flush=True)
