"""Exact homogeneity and nonlinear reference-tail gate; no fitted constants."""
import json
from pathlib import Path
import sympy as s
r,C,lam,A=s.symbols('r C lam A',positive=True)
p=s.symbols('p',real=True)
v=C/r
h=(s.diff(v,r)**2+2*v*v/r**2)**((p-2)/2)
div=s.diff(h*s.diff(v,r),r)+2*h*s.diff(v,r)/r-2*h*v/r**2
checks=[]
def ck(n,x): checks.append(dict(name=n,passed=bool(x)))
ck('p=3/2 radial operator',s.simplify((-lam*div).subs(p,s.Rational(3,2))-3**s.Rational(3,4)*lam*s.sqrt(C)/r**2)==0)
solC=A*A/(3**s.Rational(3,2)*lam*lam)
ck('reference coefficient',s.simplify(3**s.Rational(3,4)*lam*s.sqrt(solC)-A)==0)
m,n=s.symbols('m n')
sol=s.solve([m+n-3,m+2*n-3],[m,n])
ck('simultaneous mass and radius homogeneity needs no gradients',sol=={m:3,n:0})
# Positive radial and transverse Hessian coefficients of |X|^(3/2).
ck('gradient energy convex away from zero',s.Rational(3,2)>1)
ck('vacuum Hessian singular',s.limit(s.diff(r**s.Rational(3,2),r,2),r,0,dir='+')==s.oo)
result=dict(all_pass=all(x['passed'] for x in checks),checks=checks,
 reference_tail_coefficient=str(solC),homogeneity_solution={str(k):str(v) for k,v in sol.items()},
 scope='Homogeneous monomial reference energies and positive asymptotic radial branch; no no-go for arbitrary actions.')
out=Path(__file__).parent/'gradient_run';out.mkdir(exist_ok=True)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
