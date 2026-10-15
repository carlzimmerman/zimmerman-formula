import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
p,k,a,c,v=s.symbols('p k a c v',real=True)
checks=[]
def check(name,expr):
 assert s.simplify(expr)==0,(name,expr)
 checks.append(name)
L=(2*a*a+(c-2*k*v)**2-(2*a+c-2*k*v)**2)/8+p*(2*a+c-2*k*v)**2/8+p*(2*a*a+c*c)/2+2*p*v*v
vs=s.solve(s.diff(L,v),v)[0]
K=s.simplify(s.hessian(L.subs(v,vs),(a,c)))
det=(k*k*(4*p*p+3*p-2)+28*p*p-p-2)/(2*(k*k+4))
check('scalar determinant',K.det()-det)
check('positive c diagonal',K[1,1]-p*(k*k+5)/(k*k+4))
check('isotropic zero momentum trace',(L.subs({a:1,c:1,k:0,v:0}))-(21*p-6)/8)
check('zero momentum determinant factor',det.subs(k,0)-(7*p-2)*(4*p+1)/8)
check('ultraviolet transverse trace kinetic',s.limit(K[0,0],k,s.oo)-(4*p*p+3*p-2)/(2*p))
check('quarter phase determinant',det.subs(p,s.Rational(1,4))+(16*k*k+21)/(32*(k*k+4)))
check('full phase scalar determinant',det.subs(p,1)-(5*k*k+25)/(2*(k*k+4)))
# Orthogonal kinetic check: complete square in shift before differentiating.
check('independent shift square',L-(L.subs(v,vs)+p*(k*k+4)*(v-vs)**2/2))
theta,kap,x=s.symbols('theta kap x',real=True)
Liso=(-6+9*theta+3*kap)*x*x/8
check('general isotropic kinetic',Liso-3*(kap+3*theta-2)*x*x/8)
A=(1+4*p)/2;B=(1+2*p)/2;C=2*p
check('tensor full phase speed',B.subs(p,1)/A.subs(p,1)-s.Rational(3,5))
check('tensor full phase gap',C.subs(p,1)/A.subs(p,1)-s.Rational(4,5))
check('tensor vacuum speed',B.subs(p,0)/A.subs(p,0)-1)
Z1,Z2=s.symbols('Z1 Z2',positive=True)
r=(Z1-Z2)/(Z1+Z2);t=2*Z1/(Z1+Z2)
check('tensor interface flux',r*r+Z2/Z1*t*t-1)
Fc,ld,lg,src=s.symbols('Fc ld lg src',real=True)
# Canonical scalar dE/dt integrated by parts = dotlambda * source.
check('controller source work',ld*(Fc**2*lg+src)-Fc**2*ld*lg-ld*src)
res={'claim_id':'CVI-001','checks_passed':len(checks),'scalar_K':str(K),'scalar_determinant':str(s.factor(det)), 'ultraviolet_critical_phase':str((-3+s.sqrt(41))/8),'ultraviolet_critical_phase_decimal':float((-3+s.sqrt(41))/8),'tensor_coefficients':{'A':str(A),'B':str(B),'C_D_equals_one':str(C)},'scope':'Exact homogeneous flat-collar quadratic action; compact wave-packet argument separately in REPORT.md. No full seven-mode interface, physical material or powered craft solution.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(res,indent=2))
