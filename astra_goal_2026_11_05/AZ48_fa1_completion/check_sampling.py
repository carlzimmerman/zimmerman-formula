#!/usr/bin/env python3
"""Analytic sampling/disc/oracle fixtures and separate selector-sign mutation."""
import argparse,json
from pathlib import Path
import numpy as np
import sampling3d as S
import grid3d as D
import bullet_source as B
import audit_inputs as A
p=argparse.ArgumentParser();p.add_argument('--mutate',action='store_true');args=p.parse_args();checks=[]
def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
g=D.Grid(16);x,y,z=g.coordinates();points=np.array([[0.,0.,0.],[190.,90.,0.],[820.,220.,0.],[-550.,400.,100.]])
matrices={'isotropic':np.eye(3),'rotated':np.array([[1.2,.13,-.17],[.13,1.7,.21],[-.17,.21,2.3]]),'planar':np.diag([1.,1.,0.])}
for name,H in matrices.items():
 phi=.5*(H[0,0]*x*x+H[1,1]*y*y+H[2,2]*z*z)+H[0,1]*x*y+H[0,2]*x*z+H[1,2]*y*z
 sampler=S.Sampler(g,D.hessian(g,phi),mutate=args.mutate);values=sampler(points)
 target=float(B.selector(H));error=float(np.max(abs(values['s']-target)))
 check(name+'_sample_invariant',error<=1e-10,error)
 check(name+'_sample_norm',np.max(abs(values['norm']-np.linalg.norm(H)))<=1e-10)
 check(name+'_not_tiny',not np.any(values['tiny']))
 for nr,nt in [(32,64),(64,128)]:
  positions,weights=S.disc_nodes([190.,90.,0.],nr,nt)
  r2=np.sum((positions[:,:2]-[190.,90.])**2,axis=1)
  check(name+f'_area_{nr}',abs(np.sum(weights)-1)<1e-12)
  check(name+f'_radius_squared_{nr}',abs(np.dot(weights,r2)/5000-1)<1e-12)
  result=S.disc(sampler,[190.,90.,0.],.24,nr,nt)
  check(name+f'_disc_invariant_{nr}',abs(result['mean_s']-target)<=1e-10)
  check(name+f'_disc_fraction_{nr}',result['on_fraction']==float(target>=.24))
try:sampler([[5000.,0.,0.]])
except ValueError:rejected=True
else:rejected=False
check('outside_domain_rejected',rejected)
zero=S.Sampler(g,[np.zeros(g.interior) for _ in range(6)])([[0.,0.,0.]])
check('zero_field_flagged',bool(zero['tiny'][0]) and zero['norm'][0]==0)
for foot in B.A0:
 oracle=S.plummer_oracle(foot)
 check(foot+'_70_oracle_samples',len(oracle['s'])==70 and len(set(oracle['r_over_a']))==5)
 check(foot+'_angular_invariance',all(np.ptp(np.asarray(oracle['s'])[np.asarray(oracle['r_over_a'])==r])==0 for r in [.3,.5,1.,2.,5.]))
points_s=dict(BCG1=.1,BCG3=.3,GASM=.4,GASB=.2)
r=S.threshold_reading(points_s,.24)
check('wrong_sign_known',r['conditional_reading']=='WRONG SIGN' and r['wrong_sign_intervals']['main']==dict(lower_open=.1,upper_closed=.4))
check('all_galaxies_allowed',S.threshold_reading(points_s,.05)['conditional_reading']=='WEIGHT ALLOWED AT GALAXIES')
check('no_sign_known',S.threshold_reading(points_s,.5)['conditional_reading']=='NO SIGN')
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(S.__file__).resolve(),Path(D.__file__).resolve(),Path(B.__file__).resolve(),Path(S.R.__file__).resolve(),S.THRESHOLDS,A.HERE/'SAMPLING_CONTRACT.md']},scope='Sampling implementation fixtures only; no physical field convergence. kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/('mutate/sampling_checks.json' if args.mutate else 'sampling_checks.json'),obj)
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
