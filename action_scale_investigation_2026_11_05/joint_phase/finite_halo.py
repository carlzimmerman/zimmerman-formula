"""Finite-wall energy obstruction and vacuum-reservoir accounting."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(e):return s.simplify(e)==0
r,R,A,K,m,kB,G,TR,nR=s.symbols('r R A K m kB G TR nR',positive=True)
n=A/r**2;u=K*A*(1/r-1/R)
check('finite wall continuity',zero(s.diff(r*r*n*u,r)/r**2+K*n*n))
check('finite wall no flux',zero(u.subs(r,R)))
P=nR*kB*TR
required=-K*nR*P
claimed=0 if args.mutate else -K*nR*nR*kB*TR
check('boundary compression energy',zero(required-claimed))
v2=4*s.pi*G*m*A
D=m*K*K*A*A/kB
C=s.symbols('C',real=True)
T=m*v2/(2*kB)-D/(4*r*r)+D/(3*R*r)+C*r*r
check('finite tail momentum',zero(u*s.diff(u,r)+(kB/m)*(s.diff(T,r)-2*T/r)+v2/r))
H=n*s.Rational(3,2)*kB*u*s.diff(T,r)+n*kB*T*s.diff(r*r*u,r)/r**2
check('profile agrees with boundary obstruction',zero(H.subs(r,R)+K*(A/R**2)**2*kB*T.subs(r,R)))
ls,la,v,c,E=s.symbols('ls la v c E',positive=True)
sigma_self=ls**2/(128*s.pi*m*m)
Kann=la**2/(64*s.pi*m*m)
check('elastic versus annihilation rates',zero(sigma_self*(v/c)/Kann-ls**2*v/(2*la**2*c)))
sigma_rad=la**2/(16*s.pi*m*(m+2*E))
check('material versus radiation opacity ratio',zero(sigma_self/sigma_rad-ls**2*(1+2*E/m)/(8*la**2)))
DVac,L,gamma,zeta,MB,rho=s.symbols('DVac L gamma zeta MB rho',positive=True)
vol=4*s.pi*R**3/3
check('moving phase power',zero(s.diff(DVac*vol,R)-4*s.pi*DVac*R*R))
Lreq=MB*c*c*s.sqrt(G*rho)/(4*zeta)
check('required luminosity conversion',zero((2*zeta*Lreq/(c*MB))/(c*s.sqrt(G*rho))-s.Rational(1,2)))
check('finite reservoir lifetime',zero((DVac*vol/Lreq)-16*s.pi*zeta*DVac*R**3/(3*MB*c*c*s.sqrt(G*rho))))
t=s.symbols('t',real=True);V=s.Function('V')(t)
check('constant vacuum has no local decay power',s.diff(s.Symbol('V0'),t)==0)
check('decaying vacuum source',zero(-s.diff(s.exp(-gamma*t),t)-gamma*s.exp(-gamma*t)))
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
