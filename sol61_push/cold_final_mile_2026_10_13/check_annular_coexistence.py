import json,sys
from pathlib import Path
import sympy as s
r,A,l=s.symbols('r A l',positive=True)
M=1+A*r;T=r*r*M/(r*r+M);F=A*r-T;u=T/r**2
g=M/r**2;R=u*u/(1-u)
checks=[]
def check(name,cond):
 checks.append(dict(name=name,passed=bool(cond)))
 if not cond:raise AssertionError(name)
check('tether full-force balance',s.simplify(R-(1+F)/r**2)==0)
check('ordinary mass counted once',s.simplify(g-(1+T+F)/r**2)==0)
check('positive free mass numerator for A at least sqrt2',
       s.simplify(F-r*((A*A-1)*r+A)/(r*r+A*r+1))==0)
check('free density sign factor',s.simplify(s.diff(F,r)-(1+A*r)*((A*A-2)*r+A)/(r*r+A*r+1)**2)==0)
check('tether density positive formula',s.simplify(s.diff(T,r)-(r**4*A+2*r*M*M)/(r*r+M)**2)==0)
check('strict wall distance',s.simplify(1-u-r*r/(r*r+M))==0)
check('finite asymptotic free mass',s.limit(F,r,s.oo)==A*A-1)
check('deep total acceleration coefficient',s.limit(r*g,r,s.oo)==A)
check('deep external source carries matching amplitude',s.simplify(1+s.limit(F,r,s.oo)-A*A)==0)
L2=r+A*r*r
acc=-g+l/r**3
check('circular orbit balance',s.simplify(acc.subs(l,L2))==0)
omega2=-s.diff(acc,r).subs(l,L2)
check('radial frequency in frozen total potential',s.simplify(omega2-(1+2*A*r)/r**3)==0)
rows=[]
for av in [s.sqrt(2),s.Integer(2),s.Integer(5)]:
 for rv in [s.Rational(1,2),s.Integer(2),s.Integer(20),s.Integer(50)]:
  v={A:av,r:rv};vals=[T.subs(v),F.subs(v),s.diff(T,r).subs(v),s.diff(F,r).subs(v),omega2.subs(v)]
  check('positive masses slopes frequency A=%s r=%s'%(av,rv),all(x>0 for x in vals))
  rows.append(dict(A=float(av),r=float(rv),tether_mass=float(vals[0]),free_mass=float(vals[1]),
                  tether_slope=float(vals[2]),free_slope=float(vals[3]),omega_r_squared=float(vals[4])))
out=dict(checks=checks,controls=rows,scope='Conditional spherical measure-valued annular equilibrium with prescribed matched core; frozen-potential orbital radial stability only. No collective, nonspherical or smooth-DF stability, formation or finite interface established.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_passed':all(x['passed'] for x in checks)},indent=2))
