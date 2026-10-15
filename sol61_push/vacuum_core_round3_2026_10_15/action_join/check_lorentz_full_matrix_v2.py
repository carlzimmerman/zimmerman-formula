#!/usr/bin/env python3
"""Orthogonal full-Hessian and Maxwell-constraint check for the scoped no-go."""
import hashlib
import json
import sys
from pathlib import Path
import sympy as s

E,D0,LS,LSS,LPP,lam=s.symbols('E D0 LS LSS LPP lam',real=True)
e=s.Matrix(s.symbols('ex ey ez',real=True)); b=s.Matrix(s.symbols('bx by bz',real=True))
variables=list(e)+list(b)
dS=lam*E*e[2]+lam**2*(e.dot(e)-b.dot(b))/2
dP=lam*E*b[2]+lam**2*e.dot(b)
jet=LS*dS+LSS*dS*dS/2+LPP*dP*dP/2
L2=s.expand(jet).coeff(lam,2)
t=D0/(D0+E); p=D0**2/(D0+E)**2
L2=s.expand(L2.subs({LS:t,LSS:(p-t)/E**2}))
H=s.hessian(L2,variables)
expected=s.diag(t,t,p,-t,-t,-t+E**2*LPP)
checks=[]
def exact(name,expr):
    residual=s.simplify(expr)
    if isinstance(residual,s.MatrixBase):
        ok=all(v==0 for v in residual)
    else:
        ok=residual==0
    assert ok,(name,residual)
    checks.append(name)
exact('full 6x6 constitutive Hessian',H-expected)
coords=s.symbols('time X Y Z',real=True); time,X,Y,Z=coords
a=s.Function('a')(time,X)
subs=dict(zip(variables,[0,0,-s.diff(a,time),0,-s.diff(a,X),0]))
DD=s.Matrix([s.diff(L2,v) for v in e]).subs(subs)
HH=-s.Matrix([s.diff(L2,v) for v in b]).subs(subs)
EE=e.subs(subs); BB=b.subs(subs)
def curl(V):
    return s.Matrix([s.diff(V[2],Y)-s.diff(V[1],Z),s.diff(V[0],Z)-s.diff(V[2],X),s.diff(V[1],X)-s.diff(V[0],Y)])
def div(V):
    return s.diff(V[0],X)+s.diff(V[1],Y)+s.diff(V[2],Z)
exact('electric Gauss constraint',div(DD))
exact('magnetic divergence constraint',div(BB))
exact('all three Faraday components',BB.diff(time)+curl(EE))
ampere=DD.diff(time)-curl(HH)
exact('all three Ampere components',ampere-s.Matrix([0,0,-p*s.diff(a,time,2)+t*s.diff(a,X,2)]))
exact('free LPP absent from mode equation',s.diff(ampere[2],LPP))
exact('exact speed excess',t/p-1-E/D0)
exact('invariant curvature derivative',(s.diff(t,E)/E)+D0/(E*(D0+E)**2))
DE=s.Function('D')(E)
exact('general response slope identity',s.diff(DE/E,E)-(E*s.diff(DE,E)-DE)/E**2)
root=Path(__file__).resolve().parents[3]
proof=root/'sol61_push/vacuum_core_round3_2026_10_15/lorentz/PROOF.md'
assert hashlib.sha256(proof.read_bytes()).hexdigest()=='a40e10dfff284d97704dc88132dea6a879fe0410b8d272005ff42f33c22ec289'
checks.append('audited proof byte hash unchanged')
Path(sys.argv[1]).write_text(json.dumps({'exact_checks':checks,'exact_check_count':len(checks),'scope':'parity-even derivative-free L(S,P), unchanged Le, nonzero pure-electric background','proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest()},indent=2)+'\n')
print(str(len(checks))+' full-matrix, constraint, derivative and proof-hash checks passed.')
