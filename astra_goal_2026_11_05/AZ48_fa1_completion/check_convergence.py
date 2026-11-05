#!/usr/bin/env python3
"""Synthetic full-ladder coverage and adversarial frozen-gate fixtures."""
import argparse,copy,json,platform
from pathlib import Path
import numpy as np
import scipy
import convergence as C
import sampling3d as S
import audit_inputs as A
parser=argparse.ArgumentParser();parser.add_argument('--mutate',action='store_true');args=parser.parse_args();checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
def fixture(foot):
 records=[]
 for source,n,width in C.REQUIRED:
  r=dict(field_identity=dict(arguments=dict(source=source,n=n,half_width=width,foot=foot,homotopy=False),source_hashes={'fixture':'not physical evidence'},versions={'fixture':True}),source_hashes={'fixture':'not physical evidence'},mutate=False,status='SINGLE GRID ONLY',finite=True,residual=1e-10,principal_min=.1,residual_eligible=True,max_hessian_norm=2.,inherited_threshold=S.inherited_threshold(foot))
  if source=='plummer':
   oracle=S.plummer_oracle(foot);r.update(oracle=oracle,plummer=dict(s=list(oracle['s']),norm=[1.]*70,tiny=[False]*70))
  else:
   r['points']={k:dict(position_kpc=v,s=.6,norm=1.,tiny=False) for k,v in S.POINTS.items()}
   r['discs']={k:[dict(nr=nr,ntheta=nt,mean_s=.6,on_fraction=1.,mean_on=True,min_hessian_norm=1.,tiny_samples=0) for nr,nt in [(32,64),(64,128)]] for k in S.POINTS}
  records.append(r)
 return records
for foot in ['canonical','alt']:
 base=fixture(foot)
 def grade(rows,prerequisites=True):return C.evaluate(rows,foot,prerequisites,mutate_grader=args.mutate)
 check(foot+'_complete_fixture_eligible',grade(base)['numerical_status']=='PASS')
 for i,role in enumerate(C.REQUIRED):
  reduced=copy.deepcopy(base);reduced.pop(i)
  check(foot+'_missing_'+str(role),grade(reduced)['numerical_status']=='UNDECIDED')
 check(foot+'_missing_known_answers',grade(base,False)['numerical_status']=='UNDECIDED')
 modifications=[
 ('bad_residual',lambda x:x[5].update(residual=1e-6)),
 ('nonelliptic',lambda x:x[5].update(principal_min=-.1)),
 ('pilot_instead_of_production',lambda x:x[5].update(status='PILOT ONLY')),
 ('point_resolution',lambda x:x[5]['points']['BCG1'].update(s=.63)),
 ('point_box',lambda x:x[6]['points']['GASM'].update(s=.63)),
 ('point_threshold_flip',lambda x:([r['points']['BCG1'].update(s=S.inherited_threshold(foot)+.001) for r in x[3:]],x[4]['points']['BCG1'].update(s=S.inherited_threshold(foot)-.001))),
 ('disc_resolution',lambda x:[d.update(mean_s=.64) for d in x[5]['discs']['BCG1']]),
 ('disc_box_fraction',lambda x:[d.update(on_fraction=.96) for d in x[6]['discs']['GASB']]),
 ('disc_threshold_flip',lambda x:([d.update(mean_s=S.inherited_threshold(foot)+.001) for r in x[3:] for d in r['discs']['BCG1']],[d.update(mean_s=S.inherited_threshold(foot)-.001) for d in x[4]['discs']['BCG1']])),
 ('disc_quadrature',lambda x:x[5]['discs']['GASM'][0].update(mean_s=.62)),
 ('tiny_point',lambda x:x[5]['points']['BCG1'].update(tiny=True)),
 ('tiny_disc',lambda x:x[5]['discs']['BCG1'][1].update(tiny_samples=1)),
 ('plummer_oracle_error',lambda x:[r['plummer']['s'].__setitem__(0,r['plummer']['s'][0]+.03) for r in x[:3]]),
 ('plummer_pair_error',lambda x:x[1]['plummer']['s'].__setitem__(0,x[1]['plummer']['s'][0]+.03)),
 ('plummer_missing_direction',lambda x:x[2]['plummer']['s'].pop()),
 ('changed_threshold',lambda x:x[5].update(inherited_threshold=.01)),
 ('wrong_footing',lambda x:x[5]['field_identity']['arguments'].update(foot='alt' if foot=='canonical' else 'canonical')),
 ('changed_engine',lambda x:x[5]['field_identity'].update(source_hashes={'changed':True})),
 ('nonfinite_sample',lambda x:x[5]['points']['BCG1'].update(s=float('nan'))),
 ]
 for name,change in modifications:
  rows=copy.deepcopy(base);change(rows)
  check(foot+'_'+name,grade(rows)['numerical_status']=='UNDECIDED')
 check(foot+'_duplicates_rejected',grade(base+[copy.deepcopy(base[0])])['numerical_status']=='UNDECIDED')
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(C.__file__).resolve(),Path(S.__file__).resolve(),Path(S.R.__file__).resolve(),Path(S.B.__file__).resolve(),S.THRESHOLDS,A.HERE/'FROZEN_BULLET.md',A.HERE/'SAMPLING_CONTRACT.md']},scope='Synthetic ladder fixtures only; no physical production field or convergence result. kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/('mutate/convergence_checks.json' if args.mutate else 'convergence_checks.json'),obj)
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c['name'] for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
