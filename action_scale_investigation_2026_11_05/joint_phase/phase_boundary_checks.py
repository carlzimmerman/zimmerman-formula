"""Analytic thin phase wall, pressure response and leakage checks."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args()
checks={}
def eq(k,a,b):checks[k]=bool(s.simplify(a-b)==0)
phi,v,lam,D=s.symbols('phi v lam D',positive=True)
z=phi/v;V=lam*phi**2*(phi-v)**2/4+D*(3*z*z-2*z**3)
eq('phase stationary interior',s.diff(V,phi).subs(phi,0),0)
eq('phase stationary exterior',s.diff(V,phi).subs(phi,v),0)
eq('vacuum energy splitting',V.subs(phi,v)-V.subs(phi,0),D)
eq('exterior curvature',s.diff(V,phi,2).subs(phi,v),lam*v*v/2-6*D/v**2)
eq('degenerate tension integral',s.integrate(s.sqrt(lam/2)*phi*(v-phi),(phi,0,v)),s.sqrt(lam/2)*v**3/6)
R,W,S,I,P=s.symbols('R W S I P',positive=True)
acc=(P+D-2*S/R)/I-W*W/R
energy=S*R*R+I*R*R*W*W/2-D*R**3/3
eq('wall energy pressure work',s.diff(energy,R)*W+s.diff(energy,W)*acc,P*R*R*W)
a,C=s.symbols('a C',positive=True)
force=C/R**a+D-2*S/R
der=s.diff(force,R).subs(C,P*R**a).subs(S,R*(P+D)/2)
eq('homologous pressure stiffness',der,(D-(a-1)*P)/R)
m,T,B,y=s.symbols('m T B y',positive=True)
flux=s.sqrt(m/(2*s.pi*T))*s.integrate(y*s.exp(-m*y*y/(2*T)),(y,s.sqrt(2*B/m),s.oo))
eq('mass step leakage upper flux',flux,s.sqrt(T/(2*s.pi*m))*s.exp(-B/T))
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'scope':'Specified thin-wall potential and nonrelativistic normal-energy barrier; not microphysical matching of numerical phase parameters.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
