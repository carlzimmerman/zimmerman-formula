#!/usr/bin/env python3
"""Analytic full-3D operators and Jacobian checks on bounded pilot grids."""
import argparse,json,platform
from pathlib import Path
import numpy as np
import grid3d as D
import bullet_source as B
import audit_inputs as A
parser=argparse.ArgumentParser();parser.add_argument('--mutate',action='store_true');args=parser.parse_args()
checks=[]
def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
matrix=np.array([[1.2,.13,-.17],[.13,1.7,.21],[-.17,.21,2.3]])
results=[]
for n in [8,16]:
 g=D.Grid(n,half_width_kpc=4000.,alpha=3.,centre_kpc=[190.,90.,0.]);x,y,z=g.coordinates()
 phi=.5*(matrix[0,0]*x*x+matrix[1,1]*y*y+matrix[2,2]*z*z)+matrix[0,1]*x*y+matrix[0,2]*x*z+matrix[1,2]*y*z+2*x-3*y+z+7
 h=D.hessian(g,phi);expected=[matrix[0,0],matrix[1,1],matrix[2,2],matrix[0,1],matrix[0,2],matrix[1,2]]
 error=max(float(np.max(abs(value-target))) for value,target in zip(h,expected))/np.max(abs(matrix))
 check('quadratic_Hessian_'+str(n),error<=1e-10,error)
 for foot in B.A0:
  eps=B.normalization(foot)['epsilon'];truth=eps*np.trace(matrix)+np.trace(matrix)**2-np.sum(matrix*matrix)
  residual=D.operator(h,eps);error=float(np.max(abs(residual-truth))/abs(truth))
  check(foot+'_quadratic_operator_'+str(n),error<=1e-10,error)
  principal=eps*np.eye(3)+2*(np.trace(matrix)*np.eye(3)-matrix);minimum=float(np.linalg.eigvalsh(principal)[0])
  actual=D.principal_min(h,eps)
  check(foot+'_principal_matrix_'+str(n),abs(actual/minimum-1)<=1e-10)
  selector,_=D.selector(h,mutate=args.mutate);target=float(B.selector(matrix));check(foot+'_selector_'+str(n),np.max(abs(selector-target))<=1e-10)
  results.append(dict(n=n,footing=foot,max_operator_error=error,principal_minimum=actual))
 # Independent centred difference of the nonlinear operator, with full boundary variation.
 delta=np.sin(.7*x+.2*y)*np.cos(.3*z)+.2*x*y*z;dh=D.hessian(g,delta);epsilon=.017
 analytic=D.jacobian_product(h,dh,epsilon)
 for step in [1e-3,5e-4]:
  finite=(D.operator(D.hessian(g,phi+step*delta),epsilon)-D.operator(D.hessian(g,phi-step*delta),epsilon))/(2*step)
  error=float(np.max(abs(finite-analytic))/np.max(abs(analytic)))
  check('Jacobian_difference_'+str(n)+'_'+str(step),error<=1e-8,error)
check('expanded_box_central_spacing',abs(D.expanded_alpha(8000.)/np.sinh(D.expanded_alpha(8000.))*8000/(4000*3/np.sinh(3))-1)<=1e-12)
# Direct component tests expose a lost mixed derivative or ellipticity sign.
shape=(3,3,3);zero=np.zeros(shape);one=np.ones(shape)
h=[one,one,one,.2*one,.3*one,.4*one];dense=np.array([[1,.2,.3],[.2,1,.4],[.3,.4,1]])
check('mixed_selector_independent',np.max(abs(D.selector(h,mutate=args.mutate)[0]-B.selector(dense)))<=1e-12)
nonelliptic=[-3*one,one,one,zero,zero,zero]
check('nonelliptic_field_detected',D.principal_min(nonelliptic,.01)<0)
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),quadratic_results=results,
 versions=dict(python=platform.python_version(),numpy=np.__version__),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(D.__file__).resolve(),Path(B.__file__).resolve(),A.HERE/'FROZEN_BULLET.md']},
 scope='N8/N16 operator checks only; no nonlinear solve, field convergence or Bullet classification; kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/('mutate/grid3d_checks.json' if args.mutate else 'grid3d_checks.json'),obj);print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
