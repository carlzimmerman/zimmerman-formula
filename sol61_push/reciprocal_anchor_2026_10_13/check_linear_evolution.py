import json,math,sys
from pathlib import Path
import sympy as s
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
C0,C1,K0,gamma,k=s.symbols('C0 C1 K0 gamma k',positive=True)
C=C0+C1*k*k;K=K0+gamma*k*k
M=s.Matrix([[0,C],[-K,0]]);E=s.diag(K,C);S=s.diag(s.sqrt(K),s.sqrt(C))
check('energy-skew generator',s.simplify(M.T*E+E*M)==s.zeros(2),M)
check('weighted Fourier rotation',s.simplify(S*M*S.inv()-s.sqrt(C*K)*s.Matrix([[0,1],[-1,0]]))==s.zeros(2),s.sqrt(C*K))
theta=s.symbols('theta',real=True)
U=s.Matrix([[s.cos(theta),s.sqrt(C/K)*s.sin(theta)],[-s.sqrt(K/C)*s.sin(theta),s.cos(theta)]])
check('exact finite Fourier energy preservation',s.simplify(U.T*E*U-E)==s.zeros(2),U)
check('canonical symplectic propagator',s.trigsimp(U.det())==1,U.det())
check('positive quartic dispersion coefficient',s.simplify(s.limit(C*K/k**4,k,s.oo)-C1*gamma)==0,C*K)
rows=[]
for kv in [.1,1.,10.,100.]:
    cc=2+kv*kv;kk=1+.1*kv*kv;om=math.sqrt(cc*kk)
    p=.3;mom=-.2;t=1.23
    pt=p*math.cos(om*t)+math.sqrt(cc/kk)*mom*math.sin(om*t)
    mt=-math.sqrt(kk/cc)*p*math.sin(om*t)+mom*math.cos(om*t)
    initial=kk*p*p+cc*mom*mom;final=kk*pt*pt+cc*mt*mt
    error=abs(final/initial-1)
    check('deterministic finite Fourier invariant k'+str(kv),error<1e-12,error)
    rows.append(dict(k=kv,omega=om,energy_relative_error=error))
out=dict(checks=checks,frequency_squared=str(C*K),controls=rows,scope='Constant-coefficient reduced positive-energy branch; no metric-cone or complete parent health claim.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
