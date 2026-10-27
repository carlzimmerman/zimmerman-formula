import argparse,json
from pathlib import Path
import sympy as s
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--mutate',action='store_true');args=pa.parse_args()
K,k,A,gamma,C,d=s.symbols('K k A gamma C d',positive=True)
E=-K*C*C/(2*k*k)+K*d*d/(2*k*k)+(1 if not args.mutate else -1)*gamma*d*d/2+A*(C-d)**2/2
ds=s.solve(s.diff(E,d),d)[0]
S=s.factor(-k*k/K*s.diff(E.subs(d,ds),C,2))
z,t=s.symbols('z t',positive=True)
Sn=s.factor(S.subs({A:z*K/k**2,gamma:t*K/k**2}))
checks=[]
def ck(name,ok,value):
 checks.append(dict(name=name,passed=bool(ok),value=str(value)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))
ck('gradient_schur',s.simplify(Sn-(1-z*(1+t)/(1+t+z)))==0,Sn)
ck('gradient_difference',s.simplify(Sn-1/(1+z)+t*z*z/((1+z)*(1+t+z)))==0,s.factor(Sn-1/(1+z)))
ck('zero_gradient_limit',s.simplify(Sn.subs(t,0)-1/(1+z))==0,Sn.subs(t,0))
vals=[s.simplify((Sn-1/(1+z)).subs({z:zv,t:tv})) for zv in [s.Rational(1,10),1,10] for tv in [s.Rational(1,20),s.Rational(1,2),3]]
ck('gradient_sign_grid',all(v.is_nonpositive is True for v in vals),vals)
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',checks=checks),indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
