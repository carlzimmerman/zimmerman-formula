"""Shift the conversion threshold above the chosen halo's escape speed."""
import json,math
from pathlib import Path
from scipy.optimize import brentq
from scipy.integrate import quad
p=Path(__file__).parent
base=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
cosmo=json.loads((p/'portal_cosmology_run/results.json').read_text())['background']
halo=json.loads((p/'bound_halo_reactions_run/results.json').read_text())['halo']
c=299792458.;G=6.67430e-11;hb=1.054571817e-34;ev=1.602176634e-19;hbev=hb/ev;hc=hbev*c;Mpc=3.0856775814913673e22
u=.01;eps=base['epsilon'];rho=base['rho_source_eV4'];target=1.
def parameters(m):
 M=2*m*math.sqrt(1+u*u);A=math.sqrt(rho)/(math.sqrt(2)*M);g=eps*m*m/A
 lm=g*g/(4*m*m*u*u);sigma=10*lm*lm*hc*hc/(8*math.pi*m*m*(m*ev/c**2))
 return dict(m_eV=m,M_eV=M,source_amplitude_eV=A,cubic_g_eV=g,lambda_min=lm,lambda_rep=lm,lambda_=2*lm,u=u,epsilon=eps,z=base['z'],rho_source_eV4=rho,threshold_sigma_over_mass_cm2_g=sigma)
m=math.exp(brentq(lambda lm:math.log(parameters(math.exp(lm))['threshold_sigma_over_mass_cm2_g']/target),math.log(.1),math.log(1e4)))
q=parameters(m);pmax=halo['central_escape_speed_kms']*1000/c;xmax=(pmax/u)**2
ratio=lambda y:((1-2*y)/(1-y))**2 # amplitude lambda_eff/lambda_rep=1-y/(1-y)
width=q['cubic_g_eV']**2*(u/math.sqrt(1+u*u))/(8*math.pi*q['M_eV'])
ap=1/(1+q['z'])
def kernel(l):
 a=math.exp(l);r=u*ap/a;v=c*r/math.sqrt(1+r*r)
 H=math.sqrt(8*math.pi*G*(cosmo['rhom0_kg_m3']/a**3+cosmo['rhor0_kg_m3']/a**4+cosmo['rhoLambda_kg_m3'])/3)
 return v/(a*H*Mpc)
travel=quad(kernel,math.log(ap),0,epsabs=1e-10,epsrel=1e-10)[0]
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
check('threshold target',abs(q['threshold_sigma_over_mass_cm2_g']-1)<1e-12)
check('all initial bound pairs below on-shell threshold',u>pmax)
check('contact amplitude within ten percent for all bound-pair relative speeds',xmax<.1/1.1)
check('positive tree amplitude throughout bound interval',xmax<.5)
check('perturbative quartic example',q['lambda_']<1e-4)
check('ballistic quadrature refinement',abs(quad(kernel,math.log(ap),0,epsabs=1e-12,epsrel=1e-12)[0]-travel)<1e-9)
out=dict(all_pass=all(t['passed'] for t in checks),checks=checks,parameters=q,
 maximum_bound_pair_p_over_m=pmax,maximum_bound_pair_resonance_x=xmax,
 minimum_tree_cross_section_over_threshold=ratio(xmax)/(1+pmax*pmax),
 vacuum_source_lifetime_seconds=hbev/width,
 initial_free_daughter_pressure_over_energy=u*u/(3*(1+u*u)),
 initial_circular_source_eta=1-1/math.sqrt(1+u*u),
 today_unscattered_daughter_speed_m_s=c*u*ap/math.sqrt(1+(u*ap)**2),
 ballistic_comoving_distance_Mpc=travel,
 non_claims=['Initial chosen bound halo only; unbound fast populations can access resonance',
 'Ballistic distance is not a cosmological transfer function or observational constraint',
 'No new nonlinear production yield, abundance or halo-law derivation yet'])
(p/'detuned_carrier_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
