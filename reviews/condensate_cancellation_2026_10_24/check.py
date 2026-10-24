"""Conditional fixed-metric P(X) condensate sourcing diagnostic."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args()
x,y,v,A,C,V,Delta,n=s.symbols('x y v A C V Delta n',positive=True)
x0=v*v/2
P=-V+A*(x-x0)**2/2
xs=x0+(1 if a.mutate else -1)*y*y/2
dxdy=s.diff(xs,y)
px=s.diff(P,x).subs(x,xs)
checks=[]
def ck(name,e):
 r=s.factor(s.simplify(e));checks.append(dict(name=name,passed=r==0,residual=str(r)))
ck('homogeneous_zero_stiffness',s.diff(P,x).subs(x,x0))
ck('homogeneous_positive_time_coefficient',(s.diff(P,x)+2*x*s.diff(P,x,2)).subs(x,x0)-A*v*v)
ck('smooth_static_current',px*y+A*y**3/2)
ck('smooth_static_lagrangian',P.subs(x,xs)+V-A*y**4/8)
ck('smooth_formal_radial_power',-(n-1)/3-((1-n)/3))
# To obtain attractive MOND current C y^2 on the chosen outward branch:
mond_px=C*y
mond_pxx=s.diff(mond_px,y)/dxdy
ck('mond_second_derivative',mond_pxx+C/y)
Kt=mond_px+v*v*mond_pxx
Kr=mond_px+2*xs*mond_pxx
ck('mond_matter_time_kinetic',Kt-C*(y*y-v*v)/y)
ck('mond_rest_time_kinetic',Kr-C*(2*y*y-v*v)/y)
ck('small_gradient_negative_rest_residue',s.limit(y*Kr,y,0)+C*v*v)
rho=2*x*s.diff(P,x)-P
ck('condensate_vacuum',rho.subs(x,x0)-V)
P2=P-Delta
ck('vacuum_shift_preserves_derivatives',s.diff(P2,x)-s.diff(P,x))
ck('vacuum_shift_changes_density',(2*x*s.diff(P2,x)-P2-rho)-Delta)
q,rhob,H=s.symbols('q rhob H',positive=True)
Jsteady=-q*rhob/(n*H)
ck('constant_source_steady_current',n*H*Jsteady+q*rhob)
r=dict(mutated=a.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,scope='fixed-metric P(X)-dominated local response; no full gravitational or supersymmetric halo solution')
Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
