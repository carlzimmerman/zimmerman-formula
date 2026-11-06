import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,A,g,V,c,d,L=s.symbols('r A gamma V c d L',positive=True)
H=r*r/2-V+(A*r-1-g*r*r)**2/(2*g);rh=r*s.diff(H,r);rho=rh-H
high=s.diag(*[s.simplify(s.limit(2*c*f/(g*r**4),r,s.oo))for f in [rho,H,H,H]])
rL=1/A;Hl=s.simplify(H.subs(r,rL));rhl=s.simplify(rh.subs(r,rL));mu=2*g*rL**4+d
eta=s.diag(-1,1,1,1);boost=s.zeros(4)
for sign in [-1,1]:
 cov=s.Matrix([-s.sqrt(1+L*L),sign*L,0,0]);T=Hl*eta+(rhl-mu)*cov*cov.T
 boost+=T.applyfunc(lambda z:s.simplify(s.limit(c*z/(2*d*L**2),L,s.oo)))
total=s.simplify(high+boost)
checks={'high_native_limit':high==s.diag(3*c,c,c,c),'off_enthalpy':s.simplify(rhl-mu+d)==0,'boost_native_limit':boost==s.diag(-c,-c,0,0),'multiplier_mass_vanishes':s.limit(c*mu/(d*L**2),L,s.oo)==0,'nonzero_tangent_total':total==s.diag(2*c,0,c,c),'normal_flux_zero':all(total[1,j]==0 for j in range(4))}
out=dict(checks=checks,all_pass=all(checks.values()),high=str(high),boost=str(boost),total=str(total),scope='Native constitutive tensor limits only. Not solutions of differential field equations, not same-data continuations, no nonuniqueness claim.')
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
