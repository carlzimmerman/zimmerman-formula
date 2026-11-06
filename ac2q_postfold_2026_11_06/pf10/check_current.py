import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,A,g,mu,C,V,W=s.symbols('r A gamma mu C V W',positive=True)
H=r*r/2-V-W+(A*r-1-g*r*r)**2/(2*g);h=s.diff(H,r);Deff=(A*r-1)/g-r*r;D=Deff-mu;Q=A*r
contraction=s.expand(r*h-mu*Q-Q*D);expected=r*r*(3-2*A*r+2*g*r*r)
k=r*h-mu*Q;T00=-H+k*C*C;J0=(h-mu*A)*C
checks={'native_contraction':s.simplify(contraction-expected)==0,'multiplier_cancels':s.diff(contraction,mu)==0,'stress_current_quotient':s.simplify(J0-(T00+H)/(r*C))==0,'divergence_square':s.simplify(D+(r-A/(2*g))**2-A*A/(4*g*g)+1/g+mu)==0,'quartic_limit':s.limit(contraction/r**4,r,s.oo)==2*g,'H_quartic_limit':s.limit(H/r**4,r,s.oo)==g/2}
out=dict(checks=checks,all_pass=all(checks.values()),scope='Exact current and constitutive algebra only; measure compactness, trace passage and native realizability require analytic proof')
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
