"""Threshold contact scales, not a Bose-enhanced transport calculation."""
import json,math
from pathlib import Path
p=Path(__file__).parent
r=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=r['m_eV'];lam=r['lambda_rep'];c=299792458.;hb=1.054571817e-34;ev=1.602176634e-19;hc=hb*c/ev
masskg=m*ev/c**2;a=lam*hc/(8*math.pi*m);sigmam=8*math.pi*a*a/masskg
rho_si=1e-21;rho=rho_si*c*c/ev*hc**3
cs=c*math.sqrt(lam*rho/(2*m**4))
# Independent SI GP normalization: g=4pi hbar^2 a/mass.
gsi=4*math.pi*hb*hb*a/masskg
cs_si=math.sqrt(gsi*rho_si/(masskg*masskg))
checks=[dict(name='natural and SI contact speed',passed=math.isclose(cs,cs_si,rel_tol=1e-14)),dict(name='positive added quartic',passed=lam>0)]
out=dict(lambda_rep=lam,a_s_m=a,sigma_over_mass_m2_per_kg=sigmam,sigma_over_mass_cm2_per_g=10*sigmam,inherited_galaxy_density_kg_m3=rho_si,rho_eV4=rho,coherent_contact_speed_m_s=cs,COM_zero_p_over_m=r['u']/math.sqrt(2),COM_resonance_p_over_m=r['u'],checks=checks,all_pass=all(x['passed'] for x in checks),non_claims=['Threshold tree-level quantities only','No transport rate or empirical constraint'])
(p/'repulsive_scales_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
