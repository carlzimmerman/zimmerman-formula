import json,sys
from pathlib import Path
import sympy as s
r,M,Mbprime,Mcprime=s.symbols('r M Mbprime Mcprime',positive=True)
Mt=r*r*M/(r*r+M)
deriv=s.diff(Mt,r)+s.diff(Mt,M)*(Mbprime+Mcprime)
expected=(r**4*(Mbprime+Mcprime)+2*r*M*M)/(r*r+M)**2
checks=[]
def check(name,cond):
 checks.append(dict(name=name,passed=bool(cond)))
 if not cond:raise AssertionError(name)
check('total tether derivative',s.simplify(deriv-expected)==0)
freeprime=s.factor(Mcprime-deriv)
numerator=Mcprime*M*(2*r*r+M)-r**4*Mbprime-2*r*M*M
check('local positive free density inequality',s.simplify(freeprime-numerator/(r*r+M)**2)==0)
check('point baryon minimum cold density slope',s.simplify(s.solve(s.Eq(numerator.subs(Mbprime,0),0),Mcprime)[0]-2*r*M/(2*r*r+M))==0)
check('finite compact support outer negative free density',s.simplify(freeprime.subs({Mbprime:0,Mcprime:0})+2*r*M*M/(r*r+M)**2)==0)
# Exact rational counterexample: point baryon1, all cold2 enclosed by r1.
v={r:s.Integer(1),M:s.Integer(3),Mbprime:0,Mcprime:0}
massfree=2-Mt.subs(v)
negative=freeprime.subs(v)
check('positive enclosed free mass counterexample',massfree>0)
check('negative free density counterexample',negative<0)
rows=[]
for A in [s.Rational(1,2),s.Integer(1),s.Integer(2),s.Integer(5)]:
 for rv in [2,5,20,50]:
  mv=1+A*rv; tv=Mt.subs({r:rv,M:mv}); fv=A*rv-tv
  fp=freeprime.subs({r:rv,M:mv,Mbprime:0,Mcprime:A})
  check('supply decomposition A=%s r=%s'%(A,rv),s.simplify(tv+fv-A*rv)==0)
  rows.append(dict(A=float(A),r=rv,tether_mass=float(tv),free_mass=float(fv),
   free_mass_slope=float(fp),positive_mass_and_density=bool(fv>=0 and fp>=0)))
out=dict(checks=checks,annular_controls=rows,counterexample=dict(r=1,baryon_mass=1,cold_mass=2,
 tether_mass=str(Mt.subs(v)),free_mass=str(massfree),free_mass_slope=str(negative)),
 scope='Exact positive-density prerequisite; compact support control applies only if constitutive relation is imposed outside edge. Boundary/stiffness departures remain available.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'counterexample':out['counterexample']},indent=2))
