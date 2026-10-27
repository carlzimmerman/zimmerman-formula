import json,sys
from pathlib import Path
import sympy as s
n,nu,eps,b,R,V,Q,nu_max=s.symbols('n nu epsilon b R V Q nu_max',positive=True)
checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=str(detail)))
    if not cond:raise AssertionError(name)
energy=eps*n+b*n*n/2
ep=s.diff(energy,n);h=n*ep
I=s.factor((h/(n*n+R*h)).subs(n,nu/b))
src=s.factor((n+energy).subs(n,nu/b))
check('source becomes small',s.limit(src,b,s.oo)==0,src)
check('local actual carrier inertia survives limit',s.limit(I,b,s.oo)==1/R,I)
check('reference inertia itself vanishes',s.limit(h.subs(n,nu/b),b,s.oo)==0,h.subs(n,nu/b))
check('relative inertia deficit',s.simplify(1-R*I-nu/(nu+b*R*(eps+nu)))==0,1-R*I)
# General static source-neutrality condition differentiates n+E(n), not E alone.
E=s.Function('E')
check('exact constant source requires negative enthalpy',s.solve(s.Eq(s.diff(n+E(n),n),0),s.diff(E(n),n))==[-1],'Eprime=-1 => h=-n; determinant h/R<0')
check('negative reference direction at neutral derivative',s.simplify((n*s.diff(E(n),n)/R).subs(s.diff(E(n),n),-1)+n/R)==0,'det Hessian=-n/R')
supply=V*nu_max/b
check('fixed-catchment supply vanishes',s.limit(supply,b,s.oo)==0,supply)
check('fixed nonzero supply enforces finite b ceiling',s.solve(s.Eq(supply,Q),b)==[V*nu_max/Q],V*nu_max/Q)
rows=[]
for bv in [10,100,1000]:
    vals={nu:s.Rational(1,10),eps:s.Rational(1,10),R:1,b:bv,V:1,nu_max:s.Rational(1,10)}
    rows.append(dict(b=bv,source=str(src.subs(vals)),inertia=str(I.subs(vals)),maximum_isolated_supply=str(supply.subs(vals))))
out=dict(checks=checks,controls=rows,scope='Singular EOS scaling in a local static branch; integrated mass identity under isolated no-flux boundary and fixed finite catchment. Other scalings/boundaries not excluded.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
