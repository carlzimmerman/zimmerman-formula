#!/usr/bin/env python3
"""Exact local differential identities supporting REPORT.md.
Does not certify endpoint limits, existence of operators, or spectrum.
"""
import json
from pathlib import Path
import sys
import sympy as s
r=s.symbols('r',positive=True)
P=s.Function('P')(r); g=s.Function('Gamma')(r); e=s.Function('eta')(r)
K=3*g-4
old=g*P*r**4*s.diff(e,r)**2-r**3*s.diff(K*P,r)*e**2
new=P*(s.Rational(4,3)*r**4*s.diff(e,r)**2+(g-s.Rational(4,3))*r**2*(r*s.diff(e,r)+3*e)**2)
checks={}
checks['Newtonian completion of squares and exact boundary derivative']=s.simplify(new-old-s.diff(r**3*K*P*e**2,r))==0
Pi=s.Function('Pi')(r); V=s.Function('V')(r)
u=s.Function('u')(r);z=s.Function('z')(r)
L_u=-s.diff(Pi*s.diff(u,r),r)+V*u
left=Pi*s.diff(z,r)**2+V*z**2-L_u*z**2/u-Pi*u**2*s.diff(z/u,r)**2
checks['ground state identity with exact boundary derivative']=s.simplify(left-s.diff(Pi*s.diff(u,r)*z**2/u,r))==0
p,pp,rho,c2,gamma,ap,bp,A,eta,etap=s.symbols('p pp rho c2 gamma ap bp A eta etap')
k=3*gamma-4
raw=A*(gamma*p*r*r*((3-r*ap)*eta+r*etap)**2+(4*pp*r**3+2*p*r**3*(ap+bp)-(p+rho*c2)*r**4*ap**2)*eta**2)
stable=A*(gamma*p*r**4*etap**2+2*p*r**3*(k-gamma*r*ap)*eta*etap+(3*k*p*r*r-(6*gamma+2)*p*r**3*ap-2*p*r**3*bp+((gamma-1)*p-rho*c2)*r**4*ap**2)*eta**2)
boundary_derivative=4*A*(((ap+bp)*p*r**3+pp*r**3+3*p*r*r)*eta**2+2*p*r**3*eta*etap)
checks['GR stabilized work differs by exact total derivative']=s.expand(raw-stable-boundary_derivative)==0
t,G,m,d,a1,b1=s.symbols('t G m d a1 b1')
gpn=s.Rational(4,3)+t*d
apn=t*G*m/r**2
bpn=t*G*(4*s.pi*r*rho-m/r**2)
num=(1+t*(a1+b1))*(3*(3*gpn-4)*p*r*r-(6*gpn+2)*p*r**3*apn-2*p*r**3*bpn+(gpn-1)*p*r**4*apn**2-rho*r**4*t*(G*m/r**2)**2)
first=s.expand(num).coeff(t,1)
H=8*G*p*m*r+8*s.pi*G*p*rho*r**4+G**2*rho*m**2
checks['leading PN work equals 9 delta P r2 minus H']=s.simplify(first-(9*d*p*r*r-H))==0
result={'arithmetic':'exact symbolic rational-function and differential algebra','sympy':s.__version__,'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL','non_claims':['Endpoint boundary terms have to be checked separately','No spectral existence or min-max theorem formalization','No numerical or PN remainder certification']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
