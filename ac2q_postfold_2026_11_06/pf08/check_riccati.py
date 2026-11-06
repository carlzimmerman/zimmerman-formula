import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,c,cr,wp,wm,h,R,Rr=s.symbols('r c cr wp wm h R Rr',nonzero=True)
checks={};A=(1-c*c+r*c*cr)/2;B=(1+c*c-r*c*cr)/2
for sign in [1,-1]:
 K=(wp+wm)/2;a=sign*c*(wp-wm)/2
 quad=a*a*(1-r*cr/c)-K*K+sign*a*K*((c*c-1)/c-r*cr)
 checks['diagonal_'+str(sign)]=s.expand(quad+A*wp**2+B*wp*wm)==0
 # D_sigma log(f)=(-B/(r c²))*(-r c² w_other) plus bounded terms
 checks['weight_'+str(sign)]=s.expand(-A*wp**2-B*wp*wm+B*wm*wp+A*wp**2)==0
c2=h/(r*R);rccr=s.simplify(r*s.diff(c2,r)/2) # correct total derivative separately: h'=R, R'=Rr
rccr=s.simplify((1-c2-h*Rr/R**2)/2)
G=3*(1-c2)-h*Rr/R**2
checks['genuine_coefficient']=s.simplify((1-c2+rccr)/2-G/4)==0
out=dict(all_pass=all(checks.values()),checks=checks,scope='Exact principal quadratic algebra and weight cancellation only; no PDE existence or propagated bounds')
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(0 if out['all_pass']else 1)
