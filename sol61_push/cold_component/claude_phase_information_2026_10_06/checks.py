#!/usr/bin/env python3
import argparse,itertools,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--result',required=True);ap.add_argument('--control',choices=['erase_skew','equate_fourth']);args=ap.parse_args()
checks=[]
def check(name,expr):
 ok=bool(expr);checks.append({'name':name,'passed':ok});print(('PASS ' if ok else 'FAIL ')+name)
def eq(a,b):return s.simplify(a-b)==0
sig=s.symbols('sigma',positive=True)
q=s.Rational
pairs=[(s.sqrt(2)*sig,q(1,3)),(-sig/s.sqrt(2),q(2,3))]
if args.control=='erase_skew':pairs=[(sig,q(1,2)),(-sig,q(1,2))]
streams=[([c[0] for c in cs],s.prod(c[1] for c in cs)) for cs in itertools.product(pairs,repeat=3)]
def mom(exponents,vs=streams):return s.simplify(sum(w*s.prod(v[i]**exponents[i] for i in range(3)) for v,w in vs))
check('eight positive stream weights normalized',eq(mom((0,0,0)),1) and all(w>0 for v,w in streams))
check('zero mean all axes',all(eq(mom(tuple(int(i==j) for i in range(3))),0) for j in range(3)))
check('full second moment isotropic',all(eq(mom(tuple(int(k==i)+int(k==j) for k in range(3))),sig**2 if i==j else 0) for i in range(3) for j in range(3)))
check('nonzero diagonal third moment',all(eq(mom(tuple(3*int(i==j) for i in range(3))),sig**3/s.sqrt(2)) for j in range(3)))
check('third mixed components vanish',eq(mom((1,2,0)),0) and eq(mom((1,1,1)),0))
check('all stream speeds below escape',all(s.simplify(sum(t*t for t in v)/(12*sig**2))<1 for v,w in streams))
# beta integrals derived by v=sqrt(2 psi)*sqrt(u), radial isotropic integration
psi=s.symbols('psi',positive=True)
B=lambda a,b:s.gamma(a)*s.gamma(b)/s.gamma(a+b)
radv=lambda k:s.simplify((2*psi)**k*B(k+q(3,2),q(9,2))/B(q(3,2),q(9,2)))
check('equilibrium second moment',eq(radv(1)/3,psi/6))
check('equilibrium fourth isotropic components',eq(radv(2)/5,psi**2/14) and eq(radv(2)/15,psi**2/42))
A=24*s.sqrt(2)/(7*s.pi**3)
check('DF normalization equals Plummer density',eq(2*s.pi*A*(2*psi)**q(3,2)*psi**q(7,2)*B(q(3,2),q(9,2)),3*psi**5/(4*s.pi)))
r=s.symbols('r',positive=True);Phi=-1/s.sqrt(1+r*r);rho=3/(4*s.pi)*(1+r*r)**(-q(5,2));sigma2=-Phi/6
check('self consistent Poisson',eq(s.diff(r*r*s.diff(Phi,r),r)/r**2,4*s.pi*rho))
check('exact isotropic Jeans balance',eq(s.diff(rho*sigma2,r)+rho*s.diff(Phi,r),0))
K=rho*sigma2**q(3,2)/s.sqrt(2)
check('eight stream stress time derivative nonzero at r1',eq((-s.diff(K,r)).subs(r,1),q(13,4)*K.subs(r,1)))
# parity-even six-axis stream control, all odd moments zero
six=[]
for i in range(3):
 for sign in [-1,1]:six.append(([sign*s.sqrt(3)*sig if j==i else 0 for j in range(3)],q(1,6)))
check('six stream second moments identical',eq(mom((2,0,0),six),sig**2) and eq(mom((1,1,0),six),0))
check('six stream third moment hidden',eq(mom((3,0,0),six),0) and eq(mom((1,2,0),six),0))
Rxxxx=s.simplify(mom((4,0,0),six).subs(sig,s.sqrt(psi/6)))
if args.control=='equate_fourth':Rxxxx=psi**2/14
check('six stream fourth differs',eq(Rxxxx-psi**2/14,psi**2/84))
check('six stream fourth mixed differs',eq(mom((2,2,0),six),0) and psi**2/42>0)
Delta=rho*(-Phi)**2/84
check('six stream third time derivative nonzero',eq((-s.diff(Delta,r)).subs(r,1),q(7,2)*Delta.subs(r,1)))
# integration-by-parts force sign in all raw moment equations
v=s.symbols('v');n=s.symbols('n',integer=True,positive=True)
check('Vlasov force moment coefficient',eq(s.diff(v**n,v),n*v**(n-1)))
result={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'control':args.control,'domain':'exact SymPy with positive symbolic sigma/psi and rational weights'}
Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(bool(result['failed']))
