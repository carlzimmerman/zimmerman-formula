import json,math,sys
from pathlib import Path
import sympy as s
D,D0,E,zeta,u,a=s.symbols('D D0 E zeta u a0',positive=True)
H=D0**2*(-D/D0-s.log(1-D/D0))
ee=s.factor(s.diff(H,D));Le=D0*E-D0**2*s.log(1+E/D0)
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 print(name,flush=True)
 if not c:raise AssertionError(name)
check('full tether electric map',s.simplify(ee-D/(1-D/D0))==0)
check('Legendre displacement',s.simplify(s.diff(Le,E)-E/(1+E/D0))==0)
# Logarithms are positive-domain real, with0<D<D0.
leg=ee*D-Le.subs(E,ee)
check('Legendre energy derivative match',s.simplify(s.diff(leg-H,D))==0)
check('Legendre vacuum constant match',s.simplify((leg-H).subs(D,0))==0)
check('charged carrier tether',s.simplify((zeta*ee).subs({D:u/zeta,D0:a/zeta})-u/(1-u/a))==0)
check('selfgravity cancellation residual',s.simplify(u/(1-u/a)-u-u*u/(a-u))==0)
dx=s.factor(s.diff(Le,E)/E);par=s.factor(s.diff(Le,E,2))
check('transverse electric susceptibility',s.simplify(dx-D0/(D0+E))==0)
check('longitudinal electric susceptibility',s.simplify(par-D0**2/(D0+E)**2)==0)
c2=s.factor(dx/par)
check('selected covariant gauge characteristic',s.simplify(c2-(1+E/D0))==0)
check('same characteristic from displacement',s.simplify((D/ee)*s.diff(ee,D)-c2.subs(E,ee))==0)
check('speed outside metric cone on displacement branch',s.simplify(c2.subs(E,ee)-1-D/(D0-D))==0)
dec=ee*D-2*H
check('transverse pressure exceeds energy derivative',s.simplify(s.diff(dec,D)-(D*s.diff(ee,D)-ee))==0)
check('DEC defect strictly increasing derivative',s.simplify(s.diff(dec,D)-D0*D*D/(D0-D)**2)==0)
check('DEC defect zero atvacuum',s.simplify(dec.subs(D,0))==0)
# Orthogonal quadratic expansion ofLorentzscalar X withbackgroundelectricE,
# wavepolarization deltaEz and magneticBy: Y identicallyzero, so Y^2 cannot fix.
lam,e,b=s.symbols('lambda e b',real=True)
rad=s.sqrt((E+lam*e)**2-lam**2*b*b)
second=s.simplify(s.diff(rad,lam,2).subs(lam,0))
first=s.simplify(s.diff(rad,lam).subs(lam,0))
check('invariant second variation selected mode',s.simplify(second+b*b/E)==0)
quadratic=s.simplify((par*first**2+s.diff(Le,E)*second)/2)
check('independent quadratic gauge block',s.simplify(quadratic-(par*e*e-dx*b*b)/2)==0)
rows=[]
for x in [.001,.01,.1,.5,.9]:
 electric=x/(1-x);h=-x-math.log1p(-x);l=electric-math.log1p(electric)
 epsT=1/(1+electric);epsL=1/(1+electric)**2
 check('positive electric coefficients x%g'%x,epsT>0 and epsL>0)
 check('supermetric speed x%g'%x,epsT/epsL>1)
 check('DEC pressure defect x%g'%x,l>h)
 rows.append(dict(D_over_D0=x,E_over_D0=electric,c_extra_over_metric=math.sqrt(epsT/epsL),
   H_over_D0_squared=h,transverse_pressure_over_D0_squared=l,DEC_defect=l-h))
out=dict(checks=checks,samples=rows,scope='Restricted local Lorentzinvariant algebraic gauge parent, purelyelectric background. NR force matches but selected characteristic is supermetric; not global inconsistency proof for all completions or a ghost verdict.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),samples=rows),indent=2))
