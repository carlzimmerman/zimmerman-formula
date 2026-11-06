"""Conditional heating/cooling halo scaling and local thermal stability."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(x):return s.simplify(x)==0
n,T,kB,m,G,r,L,sig,Lam=s.symbols('n T kB m G r L sig Lam',positive=True)
q,p=s.symbols('q p',real=True)
H=n*sig*L/(4*s.pi*r*r);C=n*n*Lam*T**q
neq=sig*L/(4*s.pi*Lam*T**q*r*r)
check('heating cooling density',zero((H-C).subs(n,neq)))
A=sig*L/(4*s.pi*Lam*T**q)
v2=4*s.pi*G*m*A
check('flat speed normalization',zero(v2-G*m*sig*L/(Lam*T**q)))
pressure=A*kB*T/r**2
check('hydrostatic temperature',zero((s.diff(pressure,r)+m*A*v2/r**3).subs(v2,2*kB*T/m)))
# Verify hydrostatics independently with abstract v2 and A to avoid substitutions inside A.
a,v=s.symbols('a v',positive=True)
check('isothermal tail force balance',zero((s.diff(a*kB*T/r**2,r)+m*a*v*v/r**3).subs(T,m*v*v/(2*kB))))
check('mass exponent condition',zero((2*p/(q+1)).subs(p,(q+1)/2)-1))
ell,MB=s.symbols('ell MB',positive=True)
check('linear cooling BTFR normalization',zero((v*v-G*m*sig*L/(Lam*T)).subs(T,m*v*v/(2*kB))*v*v-(v**4-2*G*kB*sig*L/Lam)))
theta=s.symbols('theta',positive=True)
isobaric=1-theta**(q-1)
claimed=-q if args.mutate else 1-q
check('isobaric stability derivative',zero(s.diff(isobaric,theta).subs(theta,1)-claimed))
check('linear cooling isobaric marginality',zero(isobaric.subs(q,1)))
check('isochoric stability derivative',zero(s.diff(1-theta**q,theta).subs(theta,1)+q))
Pext=s.symbols('Pext',positive=True)
R=v*v/s.sqrt(8*s.pi*G*Pext)
check('outer pressure radius',zero((v*v/(4*s.pi*G*r*r)*kB*T/m).subs({r:R,T:m*v*v/(2*kB)})-Pext))
check('outer inventory',zero(v*v*R/G-v**4/(G*s.sqrt(8*s.pi*G*Pext))))
nQ,mu,massE=s.symbols('nQ mu massE',positive=True)
f=massE*n+kB*T*n*(s.log(n/nQ)-1)-mu*n
nstar=nQ*s.exp((mu-massE)/(kB*T))
check('reservoir stationary density',zero(s.diff(f,n).subs(n,nstar)))
check('nongravitating reservoir convexity',zero(s.diff(f,n,2)-kB*T/n))
runs=[]
for initial in [.1,10.]:
    sol=solve_ivp(lambda t,y:1-y,(0,12),[initial],method='DOP853',rtol=1e-10,atol=1e-12,dense_output=True)
    xs=np.linspace(0,12,121); vals=sol.sol(xs)[0];exact=1+(initial-1)*np.exp(-xs)
    check(f'{initial} q2 solves',sol.success)
    err=float(np.max(abs(vals-exact)))
    check(f'{initial} q2 exact solution',err<1e-8)
    check(f'{initial} q2 approaches equilibrium',abs(vals[-1]-1)<1e-4)
    runs.append({'initial':initial,'final':float(vals[-1]),'max_absolute_error':err})
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'runs':runs,'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
