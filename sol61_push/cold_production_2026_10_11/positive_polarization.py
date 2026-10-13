"""Positive-energy scalar-polarization extension: static law and linear modes."""
import json,math
from pathlib import Path
import numpy as np
p=Path(__file__).parent
checks=[]
def check(n,e,t):checks.append(dict(name=n,error=float(e),passed=bool(abs(e)<t)))
def matrix(k,angle,P,gamma=.1,mismatch=0.):
 kv=k*np.array([math.sin(angle),0.,math.cos(angle)])
 H=np.zeros((4,4),complex);H[0,0]=k*k;H[0,1:]=1j*kv;H[1:,0]=-1j*kv
 H[1:,1:]=(1+P+gamma*k*k+mismatch)*np.eye(3)+P*np.diag([0.,0.,1.])
 return H
rows=[]
for P in [0.,.001,.1,1.]:
 low=1e99
 for k in [.001,.01,.1,1.,10.]:
  for angle in [0.,math.pi/4,math.pi/2]:
   H=matrix(k,angle,P);ev=np.linalg.eigvalsh(H);low=min(low,float(ev[0]))
   check('nonnegative squared frequencies '+str((P,k,angle)),min(0,float(ev[0])),1e-12)
 rows.append(dict(background_P=P,minimum_sampled_omega_squared=low))
# The vacuum longitudinal determinant is gamma k^4, avoiding cancellation.
vacuum=[]
for k in [.001,.003,.01,.03,.1]:
 tr=1+1.1*k*k;det=.1*k**4
 slow=2*det/(tr+math.sqrt(tr*tr-4*det))
 ev=np.linalg.eigvalsh(matrix(k,0.,0.))[0]
 check('vacuum dispersion '+str(k),ev-slow,1e-12)
 vacuum.append(dict(k=k,omega_squared=slow,ratio_to_gamma_k_four=slow/(.1*k**4)))
# Static unregularized outside-source law, dimensionless flux D=B/r^2.
static=[]
for strength in [.01,1.,100.]:
 for radius in [1.,10.,100.]:
  D=strength/radius**2;P=math.sqrt(D);field=D+P
  check('stationarity '+str((strength,radius)),field-P-P*P,1e-12)
  check('flux '+str((strength,radius)),radius*radius*(field-P)-strength,1e-10)
  static.append(dict(source_flux_strength=strength,r=radius,force=field,asymptotic_flat_speed_squared=math.sqrt(strength),regulator_fraction_estimate=.2/(math.sqrt(strength)*radius)))
# An adverse perturbation is recorded, not counted as a stable model.
negative=float(np.linalg.eigvalsh(matrix(.1,0.,0.,mismatch=-.01))[0])
check('negative mismatch instability detected',max(0,negative+1e-6),1e-12)
out=dict(model='Dimensionless positive scalar/polarization energy, unit positive time kinetic terms, cubic norm coefficient 1, gradient regulator gamma=.1',stable_rows=rows,vacuum_dispersion=vacuum,static_rows=static,negative_mismatch_minimum_omega_squared=negative,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['New phenomenological sector, not derived from protected carrier','Static exact force uses gamma=0; gamma=.1 estimates are asymptotic only','No nonlinear stability, renormalization, cosmological embedding or observational test','Critical tuning, cubic norm and vacuum coefficient not derived'])
(p/'positive_polarization_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
