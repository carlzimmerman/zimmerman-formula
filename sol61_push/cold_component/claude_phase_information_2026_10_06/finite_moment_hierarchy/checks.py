#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--result',required=True);ap.add_argument('--control',choices=['wrong_degree','erase_flux']);args=ap.parse_args()
mu,x,y,z,r=s.symbols('mu x y z r',real=True);checks=[]
def check(name,ok):
 checks.append({'name':name,'passed':bool(ok)});print(('PASS ' if ok else 'FAIL ')+name)
def eq(a,b):return s.simplify(a-b)==0
R2=x*x+y*y+z*z
# Uniform sphere monomial average: independent Gaussian radial/angular factorization.
def sphere(a,b,c):
 if any(i%2 for i in (a,b,c)):return s.Integer(0)
 return s.simplify(s.gamma(s.Rational(a+1,2))*s.gamma(s.Rational(b+1,2))*s.gamma(s.Rational(c+1,2))/(2*s.pi*s.gamma(s.Rational(a+b+c+3,2))))
def avg(poly):return s.simplify(sum(coef*sphere(*powers) for powers,coef in s.Poly(s.expand(poly),x,y,z).terms()))
counts=[]
for N in range(0,9):
 ell=N+1;degree=ell if args.control!='wrong_degree' else max(0,ell-1)
 P=s.legendre(degree,mu)
 H=s.expand(sum(coef*z**powers[0]*R2**((degree-powers[0])//2) for powers,coef in s.Poly(P,mu).terms()))
 # Rodrigues expression itself supplies orthogonality proof, not sampled angular points.
 check('Rodrigues N'+str(N),eq(s.legendre(ell,mu),s.diff((mu*mu-1)**ell,mu,ell)/(2**ell*s.factorial(ell))))
 check('solid harmonic N'+str(N),eq(sum(s.diff(H,c,2) for c in (x,y,z)),0))
 retained=[]
 for a in range(N+1):
  for b in range(N+1-a):
   for c in range(N+1-a-b):retained.append(avg(x**a*y**b*z**c*H))
 counts.append(len(retained));check('all Cartesian retained moments N'+str(N),all(v==0 for v in retained))
 clell=2**ell*s.factorial(ell)**2/s.factorial(2*ell+1)
 check('first nonzero angular moment N'+str(N),eq(avg(z**ell*H),clell) and clell>0)
 B=lambda a,b:s.gamma(a)*s.gamma(b)/s.gamma(a+b)
 radial=s.simplify(B(ell+s.Rational(3,2),s.Rational(9,2))/B(s.Rational(3,2),s.Rational(9,2)))
 D=s.Rational(3,4)/s.pi*2**s.Rational(ell,2)*clell*radial*(1+r*r)**(-s.Rational(10+ell,4))
 if args.control=='erase_flux':D=s.Integer(0)
 check('strict positive flux coefficient N'+str(N),D.subs(r,1)>0)
 check('nonzero retained evolution N'+str(N),eq((-s.diff(D,r)).subs(r,1),s.Rational(10+ell,4)*D.subs(r,1)) and (-s.diff(D,r)).subs(r,1)>0)
 # Legendre boundedness representation, expanded cosine even moments.
 integral_poly=s.expand(sum(s.binomial(ell,2*k)*mu**(ell-2*k)*(-1)**k*(1-mu*mu)**k*s.binomial(2*k,k)/4**k for k in range(ell//2+1)))
 check('boundedness integral polynomial N'+str(N),eq(integral_poly,s.legendre(ell,mu)))
check('isotropic sphere average normalized',eq(sphere(0,0,0),1))
out={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'control':args.control,'bounds':{'N_min':0,'N_max':8,'Cartesian_monomial_counts':counts},'proof_scope':'universal N argument is in REPORT, finite exact implementation check only'}
Path(args.result).write_text(json.dumps(out,indent=2)+'\n');raise SystemExit(bool(out['failed']))
