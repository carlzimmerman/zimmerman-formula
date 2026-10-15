"""Exact local Lorentz-vacuum characteristic controls; proof carries quantifiers."""
import json
from pathlib import Path
import sys
import sympy as s
E,D0,u,v,lam,Ls,Lss,Lpp=s.symbols('E D0 u v lam Ls Lss Lpp',positive=True)
checks=[]
def exact(name,expr):
 z=s.factor(expr)
 assert z==0,(name,z)
 checks.append(name)
Le=D0*E-D0**2*s.log(1+E/D0)
D=s.diff(Le,E); t=D/E; p=s.diff(D,E)
exact('electric response',D-E/(1+E/D0))
exact('longitudinal dielectric',p-(1+E/D0)**-2)
exact('transverse dielectric',t-(1+E/D0)**-1)
exact('invariant electric curvature',(p-t)/E**2+D0/(E*(D0+E)**2))
# For e_z=u, b_y=v, deltaS=E u lambda+(u²-v²)lambda²/2, P=0.
dS=E*u*lam+(u*u-v*v)*lam**2/2
jet=Ls*dS+Lss*dS*dS/2
quadratic=s.expand(jet).coeff(lam,2)
exact('full invariant quadratic Az jet',quadratic-((Ls+E**2*Lss)*u*u-Ls*v*v)/2)
exact('restricted quadratic dielectric',quadratic.subs({Ls:t,Lss:(p-t)/E**2})-(p*u*u-t*v*v)/2)
exact('phase speed',t/p-1-E/D0)
exact('cone excess positive coefficient',t-p-D0*E/(D0+E)**2)
exact('general response slope',s.diff(t,E)+D0/(D0+E)**2)
exact('positive longitudinal coefficient',p-D0**2/(D0+E)**2)
# Three exact parameter controls; they do not establish the universal inequality.
controls=[]
for ratio in [s.Rational(1,1000),s.Rational(1,10),s.Integer(1)]:
 speed=s.factor((t/p).subs(E,ratio*D0))
 assert speed>1
 controls.append({'E_over_D0':str(ratio),'speed_squared':str(speed)})
Path(sys.argv[1]).write_text(json.dumps({'claim_id':'VC3-L-001','exact_identity_count':len(checks),'identities':checks,'parameter_controls':controls,'scope':'Parity-even derivative-free Lorentz vacuum with unchanged Le; no statement against a different Maxwell phase or extra fields.'},indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities and {len(controls)} exact controls.')
