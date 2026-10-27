import json,sys
from pathlib import Path
import sympy as s
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
n,R,h,k,P,kap,gamma=s.symbols('n R h k P kappa_perp gamma',positive=True)
v1,v2,d1,d2=s.symbols('v1 v2 d1 d2',real=True)
v=s.Matrix([v1,v2]);d=s.Matrix([d1,d2]);C=s.Matrix([[n,-k*P],[k*P,n]])
Href=h+kap*P*P
check('current quadrature norm',s.simplify(C.T*C-(n*n+k*k*P*P)*s.eye(2))==s.zeros(2),C)
L=(C*v-d).dot(C*v-d)/(2*R)+Href*v.dot(v)/2
vs=s.solve([s.diff(L,v1),s.diff(L,v2)],(v1,v2),dict=True)[0]
red=s.simplify(L.subs(vs));I=Href/(R*Href+n*n+k*k*P*P)
check('medium reference-momentum reduction',s.simplify(red-I*d.dot(d)/2)==0,I)
Hessian=s.hessian(L,(v1,v2,d1,d2))
check('full four-velocity Hessian determinant',s.simplify(Hessian.det()-Href**2/R**2)==0,Href**2/R**2)
check('positive block Schur complement',s.simplify(Hessian[:2,:2]-(C.T*C/R+Href*s.eye(2)))==s.zeros(2),'Physical-current square andpositiveHref guarantee positivity')
omega=(kap+gamma*k*k)/I
check('nonzero-P quartic coefficient',s.simplify(s.limit(omega/k**4,k,s.oo)-gamma*P*P/Href)==0,omega)
check('no independent-clock needed for suppression',s.simplify(s.limit(I*k*k,k,s.oo)-Href/(P*P))==0,I)
check('zero-polarization fixed-frame comparison',s.simplify(I.subs(P,0)-h/(R*h+n*n))==0,I.subs(P,0))
check('bare no-stiffness comparison',s.simplify(s.limit(omega.subs(gamma,0)/k**2,k,s.oo)-kap*P*P/Href)==0,'Bare highk speed<1 sinceHref>kapP^2;gamma0 removesoriginal screening')
rows=[]
for kval in [s.Rational(1,10),s.Integer(1),s.Integer(10),s.Integer(100)]:
    vals={n:1,R:1,h:1,P:1,kap:1,gamma:s.Rational(1,10),k:kval}
    rows.append(dict(k=str(kval),Ieff=str(I.subs(vals)),frequency_squared=str(omega.subs(vals)),omega_squared_over_k_squared=str((omega/k**2).subs(vals))))
out=dict(checks=checks,inertia=str(I),frequency_squared=str(omega),controls=rows,scope='Reference-rest-frame alternative, one metric-frozen transverse principal block; not the independent-clock theory or full relativistic stability.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
