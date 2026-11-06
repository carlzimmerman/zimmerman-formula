import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,A,g=s.symbols('r A gamma',positive=True);u=s.symbols('u',positive=True)
H=r*r/2+(A*r-1-g*r*r)**2/(2*g);h=s.diff(H,r);R=s.diff(h,r)
mid=A/(2*g);A0sq=g*(1+u)**2/u
checks={'R_polynomial':s.expand(R-(3+A*A/g-6*A*r+6*g*r*r))==0,'middle_h':s.simplify(h.subs(r,mid)-mid)==0,'middle_R':s.simplify(R.subs(r,mid)-(3-A*A/(2*g)))==0,'threshold_factor':s.factor(A0sq/g-6)==(u*u-4*u+1)/u,'half_u_R_min':s.simplify((3-A0sq/(2*g)).subs(u,s.Rational(1,2)))==s.Rational(3,4),'on_at_crossing':s.simplify(A*mid-A*A/(2*g))==0}
out=dict(checks=checks,all_pass=all(checks.values()),scope='Exact constitutive barrier identities, including counterexample to universal u<1 claim; not mixed-type nonexistence or singular selection')
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
