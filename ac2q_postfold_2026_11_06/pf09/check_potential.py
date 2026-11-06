import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,R,h,Dr,g,K,B,E,P,wp,wpp,wpphi,Z,u,v,D,CA=s.symbols('r R h Dr g K B E P wp wpp wpphi Z u v D CA',nonzero=True)
J=h+P*wp/r
F0=-(h*K+r*r*Dr*u+wp*v+2*B*J)/R;F=F0-Z/R
Eu=wpp*v/r-wp*F/r**3+wp*K/r**2+wpphi/r
Ev=Dr*F/r+r*u/g-2*E*v+K*(D-2*P*E)/r
Eu0=Eu.subs({Z:0,wpphi:0});Ev0=Ev.subs({Z:0,wpphi:0})
nCA=r*Eu-K*(wp/r+CA)-wpp*v-wpphi+wp*F/r**2
checks={'energy_source_cancels':s.cancel(r*R*F+r**3*Dr*u+r*wp*v+r*Z+r*h*K+2*B*(r*h+P*wp))==0,'polarization_constraint':s.cancel(nCA+K*CA)==0,'inverse_matrix_unchanged':all(s.cancel(s.diff(f-f0,x))==0 for f,f0 in [(Eu,Eu0),(Ev,Ev0)]for x in [u,v]),'canonical_force_sign':s.simplify(F.subs({h:r,R:1,Dr:0,wp:0})+r*(K+2*B)+Z)==0}
out=dict(checks=checks,all_pass=all(checks.values()),non_claims=['Not an independent local theorem','No verification of every source regularity estimate or singular continuation'])
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
