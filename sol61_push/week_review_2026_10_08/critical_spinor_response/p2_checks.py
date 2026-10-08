"""Unique local potential for exact P2 within the specified spinor parent."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
q,h,a0=s.symbols('q h a0',positive=True)
g=h*q
W=g*s.sqrt(a0*a0+4*g*g)/4+a0*a0*s.asinh(2*g/a0)/8-a0*g/2
if args.mutate: W+=a0*g/4
D=(s.sqrt(a0*a0+4*g*g)-a0)/2
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail),flush=True)
check('Potential derivative gives exact P2 flux',s.simplify(s.diff(W,q)-h*D)==0)
check('Exact quadrature residual',s.simplify(g*g-D*D-a0*D)==0)
check('Potential constant normalized',s.limit(W,q,0)==0)
check('No lower spinor operators',s.series(W,q,0,3).removeO()==0)
check('Critical sextic leading coefficient',s.expand(s.series(W,q,0,4).removeO()).coeff(q,3)==h**3/(3*a0))
check('Strict physical radial curvature',s.simplify(s.diff(W,q,2)-2*h**3*q/s.sqrt(a0*a0+4*h*h*q*q))==0)
check('Newtonian high field coefficient',s.limit(W/q**2,q,s.oo)==h*h/2)
Path(args.output).write_text(json.dumps(dict(checks=checks,potential=str(W),mutation=args.mutate),indent=2)+'\n')
print(str(sum(x['passed'] for x in checks))+'/'+str(len(checks))+' passed',flush=True)
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
