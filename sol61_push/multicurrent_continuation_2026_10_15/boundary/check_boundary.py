"""Exact normalization controls for the smooth charged-edge obstruction."""
import json
from pathlib import Path
import sys
import sympy as s

checks=[]
def exact(name, expr):
    value=s.simplify(expr)
    assert value==0,(name,value)
    checks.append(name)

a1,a2,w1,w2=s.symbols('a1 a2 w1 w2',positive=True)
exact('weighted Cauchy remainder',
 (a1+a2)*(w1**2/a1+w2**2/a2)-(w1+w2)**2-(a2*w1-a1*w2)**2/(a1*a2))
p,t,E,h,beta=s.symbols('p t E h beta',positive=True)
f=p-beta-E**2*(t-beta)**2/(h+E**2*(t-beta))
exact('Schur derivative',s.diff(f,beta)+h**2/(h+E**2*(t-beta))**2)
x,D0=s.symbols('x D0',positive=True)
f0=f.subs({beta:0,p:(1-x)**2,t:1-x,E:D0*x/(1-x)})
hc=D0**2*x**3/(1-x)**2
exact('threshold factorization',f0-(1-x)**2*(h-hc)/(h+D0**2*x**2/(1-x)))
delta,A,B=s.symbols('delta A B',positive=True)
power_h,power_x=s.symbols('power_h power_x',real=True)
ratio=A*delta**power_h/(D0**2*(B*delta**power_x)**3/(1-B*delta**power_x)**2)
exact('edge scaling identity',ratio-A/(D0**2*B**3)*delta**(power_h-3*power_x)*(1-B*delta**power_x)**2)
examples=[]
for ah,bx,expected in [(1,0,s.Integer(0)),(1,1,s.oo),(3,1,s.Integer(1)),(4,1,s.Integer(0))]:
    # B=1/2 keeps the nonscreened bx=0 case strictly below its constitutive pole.
    expression=ratio.subs({A:1,B:s.Rational(1,2),D0:1,power_h:ah,power_x:bx})
    limit=s.limit(expression,delta,0,dir='+')
    target=s.Integer(8) if ah==3 and bx==1 else expected
    assert limit==target,(ah,bx,limit,target)
    examples.append({'enthalpy_power':ah,'field_power':bx,'limit':str(limit)})
result={'claim_id':'MC-BOUNDARY-001','exact_identity_count':len(checks),'identities':checks,'limit_controls':examples,
 'non_claim':'No derived screening shell, alternative vacuum action or global halo dynamics.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities and {len(examples)} one-sided limit controls.')
