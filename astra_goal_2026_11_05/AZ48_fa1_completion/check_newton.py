#!/usr/bin/env python3
"""Bounded analytic Newton pilot; no physical Bullet classification."""
import json,platform
from pathlib import Path
import numpy as np
import grid3d as D
import newton3d as N
import bullet_source as B
import audit_inputs as A
checks=[];results=[]
def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
for n in [8,16]:
 g=D.Grid(n);x,y,z=g.coordinates()
 truth=.5*(1.2*x*x+1.7*y*y+2.3*z*z)+.13*x*y-.17*x*z+.21*y*z
 target_h=D.hessian(g,truth)
 for foot in B.A0:
  eps=B.normalization(foot)['epsilon'];source=D.operator(target_h,eps)
  initial=truth.copy();initial[1:-1,1:-1,1:-1]+=.002*np.prod(np.array(np.meshgrid(*[np.sin(np.pi*np.arange(1,n)/n)]*3,indexing='ij')),axis=0)
  solved,report=N.solve(g,source,eps,initial)
  check(f'{n}_{foot}_converged',report['status']=='converged',report['residual'])
  error=float(np.max(abs(solved-truth))/np.max(abs(truth)))
  check(f'{n}_{foot}_known_field',error<=1e-8,error)
  check(f'{n}_{foot}_ellipticity',all(s['principal_min']>0 for s in report['history']))
  check(f'{n}_{foot}_bounded',all(s.get('matvecs',0)<=400 for s in report['history']) and report['updates']<=60)
  results.append(dict(n=n,footing=foot,field_error=error,report=report))
  if n==8:
   saved={}
   def persist(field,history):saved.update(field=field.copy(),history=list(history))
   partial,paused=N.solve(g,source,eps,initial,accepted=persist,stop=lambda:bool(saved))
   check(foot+'_safe_step_interruption',paused['status']=='interrupted' and len(saved['history'])==2)
   resumed,resume_report=N.solve(g,source,eps,partial,history=saved['history'])
   check(foot+'_safe_step_resume_exact',np.array_equal(resumed,solved) and resume_report==report)
   bad=-truth
   _,rejected=N.solve(g,source,eps,bad)
   check(foot+'_nonelliptic_initial_rejected',rejected['status']=='nonelliptic_initial')
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),results=results,versions=dict(python=platform.python_version(),numpy=np.__version__),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(N.__file__).resolve(),Path(D.__file__).resolve(),Path(B.__file__).resolve(),A.HERE/'FROZEN_BULLET.md']},scope='N8/N16 quadratic Newton pilots only; not physical Bullet convergence. kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/'newton_checks.json',obj)
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
