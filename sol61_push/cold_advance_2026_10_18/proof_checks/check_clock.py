"""Exact checks of the proposed clock action; derivation is in the research note."""
import json
import sys
from pathlib import Path
import sympy as s

checks=[]
def ck(name,expr):
    if s.simplify(expr)!=0:
        raise AssertionError((name,expr))
    checks.append(name)

e=s.symbols('e',real=True)
w,y,g,Z,k,D=s.symbols('omega y gamma Z0 kappa Delta',positive=True)
pt,px,py,pz,ft,fx,fy,fz=s.symbols('pt px py pz ft fx fy fz',real=True)
X=(w+e*pt)**2-e**2*(px**2+py**2+pz**2)
U=((w+e*pt)*e*ft-e*px*(y+e*fx)-e**2*(py*fy+pz*fz))/s.sqrt(X)
Y2=(y+e*fx)**2+e**2*(fy**2+fz**2-ft**2)+U**2
Lag=k*X/2+D*(X-w*w)**2/(8*w*w)+(Z+2*g*s.sqrt(Y2))*U**2/2-g*Y2**s.Rational(3,2)/3
quadratic=s.diff(Lag,e,2).subs(e,0)/2
A=Z+2*g*y;q=Z+g*y;r=q*y*y/(w*w);d=q*y/w
expected=A*ft*ft/2+(k+D)*pt*pt/2-g*y*fx*fx-g*y*(fy*fy+fz*fz)/2-k*(px*px+py*py+pz*pz)/2+r*px*px/2-d*ft*px
ck('direct covariant quadratic expansion',quadratic-expected)
t,v=s.symbols('t v',real=True)
C=g*y*(1+t);E=k-r*t;B=k+D
f=s.expand((A-C)*(B-E)-d*d*t)
ck('angular determinant',f-(D*(q-g*y*t)-g*y*r*t*t))
ck('radial determinant',f.subs(t,1)-(Z*D-g*y*r))
ck('canonical-clock obstruction',f.subs({t:1,D:0})+g*y*r)
ck('worst-direction derivative',s.diff(f,t)+g*y*D+2*g*y*r*t)
M=s.Matrix([[A*v*v-C,d*s.sqrt(t)*v],[d*s.sqrt(t)*v,B*v*v-E]])
ck('dispersion polynomial',M.det()-(A*B*v**4-(A*E+B*C+d*d*t)*v*v+C*E))
polynomial=s.expand(M.det().subs({g:1,Z:1,w:1,k:3,D:3,y:1,t:1}))
ck('rational witness polynomial',polynomial-(18*v**4-19*v*v+2))
for sign in [-1,1]:
    z=(19+sign*s.sqrt(217))/36
    ck('rational witness root '+str(sign),polynomial.subs(v*v,z))
assert 217<225 and s.Rational(34,36)<1
checks.append('exact witness speed upper bound')
# General response angular identity; extends the algebra without identifying fields.
J,cp,AA,XX=s.symbols('J Cperp A X0',positive=True)
qq=AA-cp;rr=qq*y*y/XX
general=(AA-cp-J*t)*(D+rr*t)-qq*rr*t
ck('general response angular identity',general-(D*(qq-J*t)-J*rr*t*t))
# Rational full-W constitutive function; no frozen field-action identification.
a0=s.symbols('a0',positive=True)
R=y*y/(a0-y)
cpR=R/y;Jexpr=s.diff(R,y)-cpR
ck('rational constitutive radial/transverse gap',Jexpr-a0*y/(a0-y)**2)
ck('rational constitutive finite-band threshold',general.subs({AA:Z+s.diff(R,y),cp:cpR,J:Jexpr,t:1})-(Z*D-Jexpr*(Z+Jexpr)*y*y/XX))
out=dict(n_checks=len(checks),checks=checks,outcome='Exact finite symbolic identities verified; all-angle theorem requires the accompanying proof and stated positive-energy hypotheses',non_claims=['No microscopic generation of clock operator','No metric, finite inventory, ultraviolet or nonlinear global causality proof'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
