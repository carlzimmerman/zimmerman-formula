"""Exact Rayleigh trial for the specified relaxed Coulomb fluctuation model."""
import argparse
import json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
r,g,v=s.symbols('r g v',positive=True)
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail),flush=True)
B=[]
for j in range(3):
    # Angular average of z^j |xi+g e_z|, substituting v=|xi+g e_z|.
    prim=s.integrate(s.expand(v**2*(v*v-r*r-g*g)**j),v)/(2**(j+1)*g**(j+1)*r)
    subtract=r**(j+1)/s.Integer(j+1) if j%2==0 else 0
    inner=s.factor(prim.subs(v,r+g)-prim.subs(v,g-r)-subtract)
    outer=s.factor(prim.subs(v,r+g)-prim.subs(v,r-g)-subtract)
    value=s.simplify(s.integrate(4*r*r*s.exp(-2*r)*inner,(r,0,g))+
                     s.integrate(4*r*r*s.exp(-2*r)*outer,(r,g,s.oo)))
    B.append(value)
    print('B'+str(j)+'='+str(value),flush=True)
expected=[g*g/3-g**4/15,g/2-g**3/15,g*g/10+2*g**4/105]
for j in range(3):
    check('Angular radial moment '+str(j),s.expand(s.series(B[j],g,0,5).removeO()-expected[j])==0)
norm=s.integrate(4*r**4*s.exp(-2*r)/3,(r,0,s.oo))
check('Ground state z second moment',norm==1,norm)
eta=s.Rational(4,3)
a=s.Rational(1,2) if args.mutate else eta/2
trial=(a*a*g*g+eta*(B[0]-2*a*g*B[1]+a*a*g*g*B[2]))/(1+a*a*g*g)
series=s.series(trial,g,0,5)
check('Candidate tuning cancels quadratic',s.expand(series.removeO()).coeff(g,2)==0,series)
check('No positive cubic in Rayleigh upper bound',s.expand(series.removeO()).coeff(g,3)==0,series)
check('Quartic Rayleigh coefficient',s.expand(series.removeO()).coeff(g,4)==s.Rational(4,45),series)
Path(args.output).write_text(json.dumps(dict(checks=checks,moments=[str(x) for x in B],
    trial=str(trial),series=str(series),mutation=args.mutate),indent=2)+'\n')
print(str(sum(x['passed'] for x in checks))+'/'+str(len(checks))+' passed',flush=True)
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
