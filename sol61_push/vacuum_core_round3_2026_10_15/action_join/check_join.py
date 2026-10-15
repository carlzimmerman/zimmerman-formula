#!/usr/bin/env python3
"""Exact, independent local identities for the restricted S2/current-action join."""
import json
import sys
from pathlib import Path
import sympy as s

checks=[]
def zero(name, expr):
    value=s.simplify(expr)
    if value != 0:
        raise AssertionError((name, value))
    checks.append({'name':name,'passed':True})
def yes(name, cond):
    if not bool(cond):
        raise AssertionError(name)
    checks.append({'name':name,'passed':True})

u,a,zeta,E,D,r,gamma=s.symbols('u a zeta E D r gamma',positive=True)
k=zeta**2; D0=a/zeta
Le=D0*E-D0**2*s.log(1+E/D0)
D_E=E/(1+E/D0); E_D=D/(1-D/D0)
H=D0**2*(-D/D0-s.log(1-D/D0))
W=a*a/k*(-s.log(1-u/a)-u/a-u*u/(2*a*a))
zero('Le derivative gives D',s.diff(Le,E)-D_E)
zero('constitutive inverse',D_E.subs(E,E_D)-D)
zero('H is electric Legendre transform',H-(D*E_D-Le.subs(E,E_D)))
zero('H derivative gives E',s.diff(H,D)-E_D)
zero('W equals H minus Maxwell displacement energy',W-(H.subs(D,u/zeta)-u*u/(2*k)))
zero('frozen W derivative',k*s.diff(W,u)-u*u/(a-u))
zero('W derivative equals electric force minus displacement',k*s.diff(W,u)-zeta*(E_D.subs(D,u/zeta)-u/zeta))
# Signed radial jets on the positive branch, derived directly from expanded static reduction.
phi,phip,phipp,p,pp,ppp,rhob=s.symbols('phi phip phipp p pp ppp rhob',real=True)
A=phip-k*p
L=r*r*(-phip*phip/(2*k)-rhob*phi+phip*p-H.subs(D,zeta*p))-gamma*(r*r*pp*pp+2*p*p)/2
jets=((phi,phip),(phip,phipp),(p,pp),(pp,ppp))
def dr(expr):
    return s.diff(expr,r)+sum(s.diff(expr,q)*dq for q,dq in jets)
elphi=s.diff(L,phi)-dr(s.diff(L,phip))
elp=s.diff(L,p)-dr(s.diff(L,pp))
zero('Phi EL equals positive total-source constraint',elphi-(2*r*A+r*r*(phipp-k*pp))/k+rhob*r*r)
zero('P EL contains radial vector Laplacian',elp-r*r*(A-(k*p)**2/(a-k*p)+gamma*(ppp+2*pp/r-2*p/r**2)))
# Algebraic branch, independently reduced polynomial.
gb=s.symbols('gb',positive=True)
zero('canonical residual is rest polynomial',(gb+u)**2-gb*(gb+u+a)-(u*u+gb*u-a*gb))
zero('positive-root identity',((s.sqrt(gb*gb+4*a*gb)-gb)/2)**2+gb*(s.sqrt(gb*gb+4*a*gb)-gb)/2-a*gb)
zero('rest map derivative positivity formula',s.diff(u*u/(a-u),u)-u*(2*a-u)/(a-u)**2)
# Kinetic and positivity obstructions are direct consequences of definitions.
pdot,rho=s.symbols('pdot rho',positive=True)
zero('static velocity Hessian vanishes',s.diff(L,pdot,2))
zero('dust velocity Hessian is inverse density',s.diff(pdot*pdot/(2*rho),pdot,2)-1/rho)
alpha=s.symbols('alpha',positive=True)
coords=s.symbols('X Y Z',real=True)
zero('admissible local polarization can have negative divergence',sum(s.diff(-alpha*q,q) for q in coords)+3*alpha)
Ls=s.symbols('Lstar',positive=True)
zero('stiffness dictionary',(gamma/(2*k)).subs(gamma,k*Ls*Ls/2)-Ls*Ls/4)
# Exact stiffness ratio: the positive profile has a negative vector Laplacian.
y,ell,ss=s.symbols('y ell ss',positive=True)
f=2/(1+s.sqrt(1+4*y*y))
lap=s.diff(f,y,2)+2*s.diff(f,y)/y-2*f/y**2
ratio=-ell*ell*lap*(1-f)/(2*f*f)
target=ell*ell*(2/s.sqrt(1+4*y*y)-1/(1+4*y*y)**s.Rational(3,2))
zero('exact stiffness residual ratio',ratio-target)
zero('small-radius ratio limit',s.limit(target,y,0,dir='+')-ell*ell)
zero('large-radius ratio leading coefficient',s.limit(y*target,y,s.oo)-ell*ell)
rs=ell*ell*(2/ss-1/ss**3)
zero('ratio monotonicity derivative',s.diff(rs,ss)-ell*ell*(3-2*ss*ss)/ss**4)
zero('exact ratio maximum',rs.subs(ss,s.sqrt(s.Rational(3,2)))-4*s.sqrt(6)*ell*ell/9)
zero('radius of maximum',s.sqrt((s.Rational(3,2)-1)/4)-1/(2*s.sqrt(2)))
R1=target.subs(ell,1)
yes('outer 1pct crossing above 99.99',R1.subs(y,s.Rational(9999,100))>s.Rational(1,100))
yes('outer 1pct crossing below 100',R1.subs(y,100)<s.Rational(1,100))
yes('ratio at 10 exceeds 9pct',R1.subs(y,10)>s.Rational(9,100))
inputs=Path(__file__).parent/'inputs'
old=json.loads((inputs/'ag4_derive_results.json').read_text())
yes('original G4 failure retained',old['gates']['G4'] is False and old['gate_pass'] is False)
corner=[q for q in old['G4_rows'] if q['Ldim']==1][0]
yes('raw ell1 corner contradicts <=1.09pct headline',corner['max_ratio_ge10rs']>0.09)
yes('ell1 crossing not found in original grid',str(corner['r_1pct_in_rM'])=='nan')
result={
 'claim':'Restricted static S2/current-action bridge and dynamic/stiffness limitations',
 'checks':checks,'exact_check_count':len(checks),
 'stiffness':{'ratio_at_10_ell1':str(s.N(R1.subs(y,10),22)),
              'global_factor':str(s.N(4*s.sqrt(6)/9,22)),
              'ell1_outer_1pct_crossing_bracket_rM':['99.99','100'],
              'original_raw_ell1_sampled_max':corner['max_ratio_ge10rs']},
 'limitations':['Static Newtonian restricted sector only','No dynamical lift certified','No finite-gamma solution bound','Original G4 failure unchanged']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(str(len(checks))+' exact or direct raw-artifact checks passed; static bridge restricted, original G4 failed retained.')
