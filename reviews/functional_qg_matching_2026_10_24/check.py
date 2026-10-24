"""Conditional quadratic-plus-cubic force, not a quantum-gravity flow solve."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args()
Z,C,q,G,m,r,z,Sn,n=s.symbols('Z C q G m r z sphere_area n',positive=True)
checks=[]
def ck(name,e):
 v=s.factor(s.simplify(e));checks.append(dict(name=name,passed=v==0,residual=str(v)))
qe=2*q if a.mutate else q
source=qe*m/(Sn*r**(n-1))
y=(s.sqrt(Z*Z+4*C*source)-Z)/(2*C)
ck('general_spherical_flux',Sn*r**(n-1)*(Z*y+C*y*y)-q*m)
g=qe*y.subs({Sn:4*s.pi,n:3})
a0=q**3/(4*s.pi*G*C);gs=q*Z/C;gN=G*m/r**2
ck('physical_force_equation',g*g+gs*g-a0*gN)
ck('force_root',g-(s.sqrt(gs*gs+4*a0*gN)-gs)/2)
ck('quadratic_small_gradient_amplitude',s.limit(g/gN,r,s.oo)-q*q/(4*s.pi*G*Z))
ck('cubic_regime_amplitude',s.limit(r*g,r,0)-s.sqrt(a0*G*m))
ck('vanishing_quadratic_limit',s.limit(g,Z,0)-s.sqrt(a0*gN))
ck('field_rescaling_force',g.subs({q:q/z,Z:Z/z**2,C:C/z**3})-g)
ck('field_rescaling_gstar',gs.subs({q:q/z,Z:Z/z**2,C:C/z**3})-gs)
rb=2*s.sqrt(a0*G*m)/gs
ck('crossover_radius_definition',4*a0*gN.subs(r,rb)-gs*gs)
ck('crossover_mass_exponent',m*s.diff(rb,m)/rb-s.Rational(1,2))
ck('crossover_acceleration_mass_independent',s.diff(gN.subs(r,rb),m))
result=dict(mutated=a.mutate,passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,scope='exact static force for stated truncated action; no RG or physical infinity/zero-radius extrapolation')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
