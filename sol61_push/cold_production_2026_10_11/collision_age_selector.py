"""Conditional collision-age radius in a scale-free isothermal halo family."""
import json,math
from pathlib import Path
from scipy.integrate import quad
p=Path(__file__).parent
par=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
cos=json.loads((p/'portal_cosmology_run/results.json').read_text())['background']
G=6.67430e-11;c=299792458.;rhoL=cos['rhoLambda_kg_m3'];u=par['u'];s0=par['threshold_sigma_over_mass_cm2_g']/10
age=1/math.sqrt(8*math.pi*G*rhoL/3);a0=.5*c*math.sqrt(G*rhoL)
pdf=lambda y:math.sqrt(2/math.pi)*y*y*math.exp(-y*y/2)
normal=quad(pdf,0,6,epsabs=1e-13)[0]
mean=quad(lambda y:y*pdf(y),0,6,epsabs=1e-13)[0]/normal
checks=[]
def check(n,e,t):checks.append(dict(name=n,error=float(e),passed=bool(abs(e)<t)))
rows=[]
for vk in [20,50,100,150,200,250,300]:
 V=vk*1000
 def rate_integrand(y):
  pm=V*y/(2*c);x=(pm/u)**2
  ratio=((1-2*x)/(1-x))**2/(1+pm*pm)
  return pdf(y)*s0*V*y*ratio/normal
 K=quad(rate_integrand,0,6,epsabs=1e-9,epsrel=1e-11)[0]
 rad=math.sqrt(V*V*K*age/(4*math.pi*G));acc=V*V/rad
 inferred=math.sqrt(4*math.pi*G*V*V/(K*age))
 check('radius acceleration '+str(vk),acc/inferred-1,1e-12)
 check('collision age '+str(vk),V*V/(4*math.pi*G*rad*rad)*K*age-1,1e-12)
 rows.append(dict(V_km_s=vk,effective_sigma_over_mass_cm2_g=10*K/(mean*V),radius_kpc=rad/3.0856775814913673e19,cold_acceleration_m_s2=acc,acceleration_over_target=acc/a0,required_constant_cross_section_at_this_V_cm2_g=10*4*math.pi*G*V/(mean*age*a0*a0),maximum_pair_resonance_x=(3*V/(c*u))**2))
out=dict(parameters=par,assumptions=dict(density='V^2/(4 pi G r^2)',relative_speed_pdf='truncated Maxwell in y=w/V, 0<=y<=6',age_seconds=age,target_acceleration_m_s2=a0,mean_relative_speed_over_V=mean),rows=rows,acceleration_dynamic_range=rows[-1]['cold_acceleration_m_s2']/rows[0]['cold_acceleration_m_s2'],checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Declared cold-self-gravitating isothermal family, not formed halos or a baryonic solution','Truncated relative-speed PDF is a rate surrogate, not a proven distribution function','Collision-age condition is diagnostic, not a dynamical attractor','No baryonic equality-radius condition is derived'])
(p/'collision_age_selector_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
