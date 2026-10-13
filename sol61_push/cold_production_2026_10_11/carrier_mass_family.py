"""Mass rescaling at fixed source energy, u, epsilon and lambda_rep/lambda_min."""
import json,math
from pathlib import Path
p=Path(__file__).parent
base=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
contact=json.loads((p/'repulsive_scales_run/results.json').read_text())
kin=json.loads((p/'resonant_kinetics_run/results.json').read_text())
halo=json.loads((p/'bound_halo_reactions_run/results.json').read_text())
m0=base['m_eV'];c=299792458.;hbar=6.582119569e-16;year=365.25*86400
ref=next(r for r in kin['rows'] if r['rho_kg_m3']==1e-21 and r['sigma_1d_kms']==200)
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def row(m):
 b=m/m0;A=base['source_amplitude_eV']/b;g=base['cubic_g_eV']*b**3
 delta=4*m*m*base['u']**2;lam=g*g/delta
 width=g*g*(base['u']/math.sqrt(1+base['u']**2))/(8*math.pi*base['M_eV']*b)
 sigma=c and 200000/c
 f=(2*math.pi)**1.5*contact['rho_eV4']/(m**4*sigma**3)*math.exp(-base['u']**2/(2*sigma*sigma))
 rate=width*(1+2*f)/hbar
 hc=hbar*c;masskg=m*1.602176634e-19/c**2
 sigmam=10*lam*lam*hc*hc/(8*math.pi*m*m*masskg)
 cs=c*math.sqrt(lam*contact['rho_eV4']/(2*m**4))
 check('fixed epsilon source scaling',abs((g*A/(m*m))/base['epsilon']-1)<2e-6)
 check('quartic m4 scaling',abs(lam/(base['lambda_rep']*b**4)-1)<1e-12)
 check('threshold sigma per mass m5 scaling',abs(sigmam/(contact['sigma_over_mass_cm2_per_g']*b**5)-1)<1e-8)
 check('occupation m inverse fourth scaling',abs(f/(ref['resonant_occupation']/b**4)-1)<1e-8)
 check('width m5 scaling',abs(width/(kin['vacuum_width_eV']*b**5)-1)<1e-12)
 check('contact pressure unchanged',abs(cs/contact['coherent_contact_speed_m_s']-1)<1e-8)
 birth=halo['runs'][-1]['initial_global_source_charge_rate_per_Gyr']*b
 return dict(m_eV=m,g_eV=g,lambda_rep=lam,threshold_sigma_per_mass_cm2_g=sigmam,
  contact_speed_m_s=cs,resonant_occupation=f,vacuum_lifetime_seconds=hbar/width,
  fixed_bath_source_mode_time_seconds=1/rate,
  initial_global_Plummer_conversion_time_seconds=year*1e9/birth,
  mode_rate_over_dephasing_energy=width*(1+2*f)/(m*sigma*sigma))
targetm=m0*(1/contact['sigma_over_mass_cm2_per_g'])**.2
rows=[row(m) for m in [1e-12,1e-6,.001,1.,10.,targetm,100.]]
check('illustrative threshold target hit',abs(rows[-2]['threshold_sigma_per_mass_cm2_g']-1)<1e-8)
out=dict(all_pass=all(q['passed'] for q in checks),checks=checks,rows=rows,
 mass_at_illustrative_1_cm2_g_eV=targetm,
 non_claims=['Fixed chosen production-parameter family only; not all masses/couplings excluded',
 'Threshold cross section is not the velocity-averaged halo transport cross section',
 'Source-mode and initial conversion times are not settling or conduction times',
 'Earlier nonlinear yields and cosmological history do not automatically rescale'])
(p/'carrier_mass_family_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks',len(checks));assert out['all_pass']
