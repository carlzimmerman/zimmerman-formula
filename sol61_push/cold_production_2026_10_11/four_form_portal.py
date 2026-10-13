"""Fixed-flux four-form reduction and positive charged-potential matching."""
from fractions import Fraction as F
from pathlib import Path
import json,math
p=Path(__file__).parent
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
for q in [F(0),F(1),F(3,2)]:
 for s in [F(0),F(1,7),F(10)]:
  Z=1/(1+s);electric=q/Z
  L=Z*electric*electric/2;H=q*electric-L;Routh=L-q*electric
  check('fixed-flux Hamiltonian positive',H==q*q/(2*Z) and H>=0)
  check('Routhian sign',Routh==-H)
  check('affine invariant coupling',H==q*q/2*(1+s))
# Squared magnitudes phi and chi, alpha/mu^2 = h; the interaction square is unchanged.
for phi2,chi2 in [(F(0),F(0)),(F(1,3),F(2)),(F(7),F(1,8))]:
 for eps in [F(1,10),F(2)]:
  bare=F(3,4);h=F(2,5);eff=bare+h*eps
  original_mass=bare*(phi2+4*chi2)
  portal=eps*(1+h*(phi2+4*chi2))
  check('vacuum-subtracted effective mass identity',original_mass+portal-eps==eff*(phi2+4*chi2))
  delta=F(1,1000);source_mass2=4*eff+delta
  check('mass-squared threshold gap unchanged',source_mass2-4*eff==delta)
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
c=299792458.;ev=1.602176634e-19;hbev=6.582119569e-16
rhoL=6e-27;eps=rhoL*c*c/ev*(hbev*c)**3
m=params['m_eV'];fraction=.5;mu=math.sqrt(eps/(fraction*m*m))
check('illustrative matched mass',abs(((1-fraction)*m*m+eps/mu**2)/(m*m)-1)<1e-14)
out=dict(all_pass=all(x['passed'] for x in checks),checks=checks,
 illustrative_vacuum_energy_eV4=eps,alpha=1.,fraction_of_mass_squared_from_flux=fraction,
 matched_portal_scale_eV=mu,non_claims=['Tree-level fixed-flux sector only',
 'No flux selection, membrane transitions, radiative stability or UV completion',
 'At matched parameters the local scalar theory is unchanged; no halo selector derived'])
(p/'four_form_portal_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
