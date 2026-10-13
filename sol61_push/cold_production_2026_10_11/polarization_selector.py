"""Constitutive tuning required for a polarization acceleration selector."""
import json,math
from pathlib import Path
p=Path(__file__).parent
checks=[]
def check(n,e,t):checks.append(dict(name=n,error=float(e),passed=bool(abs(e)<t)))
rows=[]
for mismatch in [0.,1e-4,.01,.1]:
 samples=[]
 for y in [1e-10,1e-8,1e-6,1e-4,.01]:
  pol=2*y/(math.sqrt(mismatch*mismatch+4*y)+mismatch)
  force=(1+mismatch)*pol+pol*pol
  slope=(1+mismatch+2*pol)/(mismatch+2*pol)*y/force
  check('constitutive equation '+str((mismatch,y)),(mismatch*pol+pol*pol)/y-1,1e-12)
  if mismatch==0:check('critical force '+str(y),force/(y+math.sqrt(y))-1,1e-12)
  samples.append(dict(gN_over_a0=y,g_over_a0=force,logarithmic_force_slope=slope))
 rows.append(dict(quadratic_fractional_mismatch=mismatch,samples=samples))
out=dict(rows=rows,vacuum_shift_test=[dict(vacuum_multiplier=f,a0_multiplier=1,kappa_if_initial_half=.5/math.sqrt(f)) for f in [.25,1,4]],required_vacuum_coefficient_GW0_over_a0_squared=4.,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Phenomenological constitutive law, not microscopic polarization or dynamical stability','No production match between dipolar medium and protected scalar carrier','No derived critical quadratic coefficient, cubic coefficient or vacuum normalization'])
(p/'polarization_selector_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
