"""Symmetry-protected Lambda-medium shape freedom, no MOND identification."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
Y,t1,t2,t3,n=s.symbols('Y tau1 tau2 tau3 n',positive=True)
r=t2/t1**2-1/n
J=Y*t1**(n/2)
def ward(f):return Y*s.diff(f,Y)-2/n*(t1*s.diff(f,t1)+2*t2*s.diff(f,t2)+3*t3*s.diff(f,t3))
checks=[]
def ck(name,expr):
 v=s.simplify(expr);checks.append({'name':name,'residual':str(v),'passed':v==0})
ck('volume_invariant_ward',ward(J));ck('shape_invariant_ward',ward(r));ck('squared_shape_ward',ward(r*r))
u=s.symbols('strain',real=True)
# Positive strain eigenvalues near zero, exact isotropic trace at every strain.
lam=[1+u,1-u,s.Integer(1)]
strain_r=s.simplify(sum(x*x for x in lam)/sum(lam)**2-s.Rational(1,3))
ck('trace_preserving_shear',strain_r-2*u*u/9)
ck('unchanged_background',strain_r.subs(u,0));ck('unchanged_background_stress',s.diff(strain_r,u).subs(u,0))
ck('changed_quadratic_response',s.diff(strain_r,u,2)-s.Rational(4,9))
ck('squared_shape_preserves_quadratic',s.diff(strain_r**2,u,2).subs(u,0))
ck('changed_fourth_response',s.diff(strain_r**2,u,4)-s.Rational(32,27))
result={'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'exact internal scaling Ward identities and local strain deformation; no assertion of microscopic health or acceleration response'}
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
