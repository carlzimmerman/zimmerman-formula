"""Evaluate the conditional Gaussian variance bound; no full-field evolution."""
import json, math
from pathlib import Path
p=Path(__file__).parent
r=json.loads((p/'envelope_run_v2/results.json').read_text())
a=r['parameters']; M=a['M_eV'];m=a['m_eV'];eps=a['epsilon'];f=a['f_eV'];lam=a['lambda_'];rho=a['rho_source_eV4']
W=max(x['weight_sum'] for x in r['rows']); ns=rho/M
sigma=ns/m*(4+W)
R=M/m
checks=[]
def check(n,b): checks.append(dict(name=n,passed=bool(b)))
check('input finite computation passed',r['all_pass'])
check('variance direct and simplified',math.isclose(sigma/f**2,2*R*eps**2*(1+W/4),rel_tol=1e-14))
check('mass direct and simplified',math.isclose(3*lam*sigma/m**2,3*R**3*eps**2*(1+W/4),rel_tol=1e-14))
# Exact inequality follows from (n+1/2)^2 - n(n+1)=1/4.
for n in [0.,1e-6,.1,1.,10.,1e6]:
 check('covariance bound n='+str(n),math.sqrt(n*(n+1))<=n+.5)
out=dict(weight_sum_bound=W,variance_over_f_squared_bound=sigma/f**2,
 hartree_mass_squared_over_m_squared_bound=3*lam*sigma/m**2,
 detuning_bound=3*lam*sigma/(m**2*eps),
 phase_bound_up_to_x200=200*3*lam*sigma/(m**2*eps),
 checks=checks,all_pass=all(c['passed'] for c in checks),
 non_claims=['Conditional retained Gaussian modes only','No UV renormalization','No nonlinear error bound or scattering bound'])
(p/'hartree_bound_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
