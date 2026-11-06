"""Exact checks for conditional transport tail and microscopic capture/heating."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(x):return s.simplify(x)==0
m,mN,M,g,y,lam,E=s.symbols('m mN M g y lam E',positive=True)
amp2=4*g*g*y*y*mN*mN/M**4
capcross=g*g*y*y*mN*mN/(4*s.pi*M**4*(m+mN)**2)
check('heavy mediator baryon cross section',zero(amp2/(16*s.pi*(m+mN)**2)-capcross))
beta=4*m*mN/(m+mN)**2
check('capture maximum transfer bounded',zero(1-beta-(m-mN)**2/(m+mN)**2))
vInf,vEsc=s.symbols('vInf vEsc',positive=True)
threshold=vInf**2/(vInf**2+vEsc**2)
check('capture energy threshold',zero((1-threshold)*(vInf**2+vEsc**2)-vEsc**2))
z=s.symbols('z',real=True)
Ep=E*(m+E+E*z)/(m+2*E)
delta=E**2/(m+2*E)
check('mean recoil energy',zero(s.integrate(E-Ep,(z,-1,1))/2-delta))
sig=lam**2/(16*s.pi*m*(m+2*E));Knat=lam**2/(64*s.pi*m*m)
sigE=sig*delta/E
ratio=4*m*E/(m+2*E)**2
check('coupling cancellation',zero(sigE/Knat-ratio))
check('ratio bound',zero(s.Rational(1,2)-ratio-(m-2*E)**2/(2*(m+2*E)**2)))
check('annihilation photon ratio',zero(ratio.subs(E,m)-s.Rational(4,9)))
p,q,t=s.symbols('p q t',real=True)
sol=s.solve([q-p+1,t-p+2,2*p+t-p-2],[p,q,t])
check('transport exponent selection',sol=={p:2,q:1,t:0})
r,A,K,kB,G=s.symbols('r A K kB G',positive=True)
n=A/r**2;u=K*A/r
continuity=s.diff(r*r*n*u,r)/r**2
check('annihilation continuity',zero(continuity+(-1 if args.mutate else 1)*K*n*n))
v2=4*s.pi*G*m*A
T0=m*v2/(2*kB);D=m*K*K*A*A/(4*kB)
T=T0-D/r**2
check('momentum with inertia',zero(u*s.diff(u,r)+(kB/m)*(s.diff(T,r)-2*T/r)+v2/r))
divu=s.diff(r*r*u,r)/r**2
H=n*s.Rational(3,2)*kB*u*s.diff(T,r)+n*kB*T*divu
check('energy finite-inertia correction',zero(H-K*A*A*kB*T0/r**4-2*kB*K*A*A*D/r**6))
L,Sig=s.symbols('L Sig',positive=True)
A2=Sig*L/(8*s.pi**2*G*m*m*K)
check('tail normalization',zero((v2*v2).subs(A*A,A2)-2*G*Sig*L/K))
R0=s.symbols('R0',positive=True)
check('particle flux pays outer annihilation',zero(4*s.pi*R0**2*(n*u).subs(r,R0)-s.integrate(4*s.pi*r*r*K*n*n,(r,R0,s.oo))))
check('no-heating adiabatic slope',zero((s.Rational(3,2)*r*(-s.Rational(2,3)/r)+1)))
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'exponents':{str(k):str(v) for k,v in sol.items()},'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
