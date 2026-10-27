import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
r,S,Q=s.symbols('r S Q',positive=True)
Re=s.sqrt(S+S*S/Q);R=S*S/(r*r*(r*r-S))
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
primitive=-Q/r+S/r+s.sqrt(S)/2*s.log((r-s.sqrt(S))/(r+s.sqrt(S)))
# Integrand for escape work is Q/r^2-R; explicit primitive sign independent.
workprimitive=-(Q+S)/r-s.sqrt(S)/2*s.log((r-s.sqrt(S))/(r+s.sqrt(S)))
check('escape force primitive',s.simplify(s.diff(workprimitive,r)-(Q/r**2-R))==0)
bar=(Q+S)/Re-s.sqrt(S)/2*s.log((Re+s.sqrt(S))/(Re-s.sqrt(S)))
check('exact barrier from primitive',s.simplify(s.expand_log(-workprimitive.subs(r,Re)-bar,force=True))==0)
check('integrand vanishes atedge',s.simplify((Q/r**2-R).subs(r,Re))==0)
check('deep large supply barrier',s.limit(S*bar.subs(Q,1),S,s.oo)==s.Rational(2,3))
def barrier(ss,q=1.):
 rr=math.sqrt(ss+ss*ss/q)
 return (q+ss)/rr-math.sqrt(ss)*math.atanh(math.sqrt(ss)/rr)
def numeric(ss,q=1.):
 rr=math.sqrt(ss+ss*ss/q)
 # qcoordinate=1/r integrates endpoint exactly without an infinite tail.
 fun=lambda z:q-ss*ss*z*z/(1-ss*z*z)
 return quad(fun,0,1/rr,epsabs=1e-12,epsrel=1e-12)[0]
rows=[]
for ss in [.2,1.,2.,5.,10.,100.]:
 bv=barrier(ss);num=numeric(ss)
 check('positive escape work S%g'%ss,bv>0,bv)
 check('quadrature escape work S%g'%ss,abs(bv-num)<1e-11,abs(bv-num))
 for frac in [.01,.1,.5]:
  # Core.05 ensures every stated remaining supply stays admissible.
  remain=ss*(1-frac);cost=quad(barrier,remain,ss,epsabs=1e-12,epsrel=1e-12)[0]
  check('ground energy increase positive S%g frac%g'%(ss,frac),cost>0,cost)
  # Barrier decreases with supply; removing a finite packet costs at least
  # its original infinitesimal binding, and at most its final one.
  check('packet binding bounds S%g frac%g'%(ss,frac),
        ss*frac*bv*(1-1e-12)<=cost<=ss*frac*barrier(remain)*(1+1e-12))
  rows.append(dict(S=ss,escaped_fraction=frac,edge=math.sqrt(ss+ss*ss),barrier=bv,
                   escape_speed_over_Vf=math.sqrt(2*bv),minimum_ground_energy_increase=cost))
out=dict(checks=checks,controls=rows,scope='Zero-stiffness fixed external source test-shell barrier and ground-state removal bookkeeping; no ejection dynamics or radiation/export rate.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),S5=[x for x in rows if x['S']==5]),indent=2))
