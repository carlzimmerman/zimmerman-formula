"""Exact dynamical-scale nonselection tests; c=1, no coefficient fit."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--out',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
a,K,p,f,z=s.symbols('a K p f z',positive=True)
W=a*a/K*(-p/a-s.log(1-p/a))
h=z+z/(1+z)-2*s.log(1+z)
checks={}
def check(name,value):
    checks[name]=bool(value)
    print(('PASS ' if value else 'FAIL ')+name,flush=True)
wa=s.diff(W,a).subs(p,a*z/(1+z))
check('fixed-p kernel derivative',s.simplify(wa+a*h/K)==0)
check('sign function vanishes at zero',h.subs(z,0)==0)
check('sign function has positive derivative',s.simplify(s.diff(h,z)-z*z/(1+z)**2)==0)
chi,chi0=s.symbols('chi chi0',real=True)
ar=s.symbols('a_ref',positive=True)
wchi=s.diff(W.subs(a,ar*s.exp(chi/f)),chi)
check('exponential scale chain rule',s.simplify(wchi-(s.diff(W,a)*a/f).subs(a,ar*s.exp(chi/f)))==0)
M,V,C,x,x0=s.symbols('M V C x x0',positive=True)
Q=s.symbols('Q',real=True)
alpha=s.sqrt(3*V)/M
d=s.sqrt(C/(2*V))
xdot=alpha*s.sqrt(x*x+d*d)
H=xdot/(3*x)
check('Friedmann with both kinetic energies',s.simplify(3*M*M*H*H-(V+C/(2*x*x)))==0)
primitive=-s.asinh(d/x)/d
check('late-time integral primitive',s.simplify(s.diff(primitive,x)-1/(x*s.sqrt(x*x+d*d)))==0)
check('primitive vanishes at infinity',s.limit(primitive,x,s.oo)==0)
delta=s.sqrt(s.Rational(2,3))*M*Q/s.sqrt(C)*s.asinh(d/x0)
check('late-time displacement normalization',s.simplify(delta-Q/(alpha*d)*s.asinh(d/x0))==0)
solution=chi0+Q/(alpha*d)*(s.asinh(d/x0)-s.asinh(d/x))
check('initial field value',s.simplify(solution.subs(x,x0)-chi0)==0)
velocity=s.simplify(s.diff(solution,x)*xdot)
check('conserved scalar momentum',s.simplify(x*velocity-Q)==0)
check('homogeneous scalar equation',s.simplify(s.diff(velocity,x)*xdot+3*H*velocity)==0)
late=(0 if args.mutate else chi0)+delta
check('initial offset survives',s.diff(late,chi0)==1)
check('operational scale retains offset',s.simplify(s.diff(s.log(ar*s.exp(late/f)),chi0)-1/f)==0)
out={'passed':all(checks.values()),'mode':'drop_initial_offset' if args.mutate else 'main',
     'checks':checks,'late_displacement':str(delta),
     'source_force':'-W_chi = a^2 h(s)/(K f) > 0 for p>0',
     'scope':'Canonical monotone scale promotion, homogeneous backreaction and static zero-flux obstruction only.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True)
Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
