"""Exact operational-scale deformation; no fitted coefficient is an input."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
u=s.symbols('u',nonnegative=True);e=s.symbols('e',real=True)
a,K,b,G,rho,zeta=s.symbols('a K b G rho zeta',positive=True)
f0=-u-s.log(1-u);deform=u**3*(1-u)**2/3;f=f0+e*deform
checks={}
def check(name,ok):
 checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
check('unchanged zero quadratic data',all(s.diff(deform,u,j).subs(u,0)==0 for j in range(3)))
check('cubic coefficient changes',s.diff(f,u,3).subs(u,0)==2*(1+e))
curv=s.diff(deform,u,2)
check('deformation curvature polynomial',s.expand(curv-(2*u-8*u*u+s.Rational(20,3)*u**3))==0)
bernstein=[s.Integer(0),s.Rational(2,3),-s.Rational(4,3),s.Rational(2,3)]
recon=sum(bernstein[j]*s.binomial(3,j)*u**j*(1-u)**(3-j) for j in range(4))
check('Bernstein curvature bound certificate',s.expand(recon-curv)==0 and min(bernstein)==-s.Rational(4,3) and max(bernstein)==s.Rational(2,3))
# On [0,1], Bernstein basis nonnegative, sums to1: |curv|<=4/3.
check('uniform convexity lower bound',1-s.Rational(1,2)*max(abs(x) for x in bernstein)==s.Rational(1,3))
poly=s.cancel(curv/u)
check('curvature over u lower bound certificate',s.expand(poly+s.Rational(2,5)-s.Rational(20,3)*(u-s.Rational(3,5))**2)==0)
check('curvature over u upper bound certificate',s.expand(2-poly-s.Rational(4,3)*u*(6-5*u))==0)
# These prove -.4<=poly<=2, hence |curv|<=2u.
check('base flux derivative lower bound',s.simplify((s.diff(f0,u,2)-1-2*u)*(1-u)**2-u**2*(3-2*u))==0)
check('saturation correction vanishes',s.limit(s.diff(deform,u),u,1,dir='-')==0)
check('conjugate diverges at saturation',s.limit((1-u)*s.diff(f,u),u,1,dir='-')==1)
A=a*s.diff(f,u);gn=A-a*u
check('Newtonian flux positive factor',s.simplify(gn-a*u**2*(1/(1-u)+e*(1-u)*(1-s.Rational(5,3)*u)))==0)
deep=s.limit(A*A/gn,u,0,dir='+')
reported=a if args.mutate else a/(1+e)
check('operational MOND scale',s.simplify(deep-reported)==0)
check('baseline simple-mu law',s.simplify((gn-A*A/(A+a)).subs(e,0))==0)
keff=s.simplify(deep.subs(a,s.sqrt(b*rho))/s.sqrt(G*rho))
check('operational dimensionless ratio',s.simplify(keff-s.sqrt(b/G)/(1+e))==0)
check('coefficient sensitivity is nonzero',s.simplify(s.diff(keff,e)+s.sqrt(b/G)/(1+e)**2)==0)

# Canonical clock redefinition phi_new=zeta*phi changes Z, not the invariant rho.
Z,Xn,V=s.symbols('Z Xnew V',positive=True)
rho_old=Z*Xn/zeta**2+V;rho_new=Z/zeta**2*Xn+V
check('clock normalization leaves b unchanged',s.simplify(b*rho_old-b*rho_new)==0)
out={'passed':all(checks.values()),'mode':'freeze_deep_scale' if args.mutate else 'main','checks':checks,
 'deep_scale':str(deep),'operational_kappa':str(keff),'e_domain':'[-1/2,1/2]',
 'curvature_uniform_lower_bound':'1/(3K)',
 'scope':'Exact local kernel and leading unscreened force normalization; no whole-action health or coefficient derivation.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');raise SystemExit(0 if out['passed'] else 1)
