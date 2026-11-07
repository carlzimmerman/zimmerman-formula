"""Radial redistribution and required conductive energy transport."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
checks={}
def eq(k,a,b):checks[k]=bool(s.simplify(a-b)==0)
r,r0,R,l,A,K,j,U,m,T,ein,ui=s.symbols('r r0 R l A K j U m T ein ui',positive=True)
n=A/r**2;J=j*s.exp(-r/l)/r**2
u=U-j*l/A*s.exp(-r/l)+K*A/r
q=J/n
cv=s.Rational(3,2);cp=cv+1
eq('exact sourced continuity',s.diff(r*r*n*u,r)/r**2,J-K*n*n)
e_rel=ein-m*u*ui+m*u*u/2
momentum_source=0 if args.mutate else m*J*(ui-u)
# Conservative bulk kinetic source includes half u^2 times number source.
combined=J*(e_rel-cv*T)+J*cv*T+u*momentum_source+m*u*u*J/2
eq('injection lab energy reconstructed',combined,J*ein)
Q=s.simplify(J*(ein-cv*T)-n*T*s.diff(r*r*u,r)/r**2)
Qexpected=J*(ein-cp*T)+K*n*n*T-2*n*T*u/r
eq('leading required heat divergence',Q,Qexpected)
primitive=-j*l*(ein-cp*T)*s.exp(-r/l)+2*j*l*T*s.Ei(-r/l)-2*A*T*U*s.log(r)+K*A*A*T/r
eq('heat luminosity primitive',s.diff(primitive,r),r*r*Q)
fluxbalance=j*l*(s.exp(-r0/l)-s.exp(-R/l))-K*A*A*(1/r0-1/R)
eq('finite number budget',A*(u.subs(r,R)-u.subs(r,r0)),fluxbalance)
# Long-decay source limit: j is held finite as a local source amplitude.
jstar=K*A*A/(r0*R)
us=K*A*(r-r0)*(r-R)/(r*r0*R)
eq('long decay balanced flow',s.diff(us,r),jstar/A-K*A/r**2)
eq('inner impermeable matching',us.subs(r,r0),0)
eq('outer impermeable matching',us.subs(r,R),0)
Qs=jstar/r**2*(ein-cp*T)+K*A*A*T/r**4-2*A*T*us/r**3
I=s.integrate(s.expand(r*r*Qs),(r,r0,R))
D=1/r0-1/R
expected=K*A*A*(D*(ein-s.Rational(11,2)*T)+2*T*(1/r0+1/R)*s.log(R/r0))
eq('long decay heat budget',s.expand_log(I,force=True),s.expand_log(expected,force=True))
ezero=T*(s.Rational(11,2)-2*(R+r0)/(R-r0)*s.log(R/r0))
eq('insulated shell required injection energy',expected.subs(ein,ezero),0)
z=s.symbols('z',positive=True)
eq('thin shell energy limit',s.limit((ezero/T).subs(R,z*r0),z,1),cv)
# Short mean free path kinetic conduction diagnostic, independent of exact coefficient.
C,sig,L=s.symbols('C sig L',positive=True)
vth=s.sqrt(T/m);kap=C*vth/sig;tau=A*sig/r
epsilon=L/(4*s.pi*r*kap*T)
eq('conduction opacity tradeoff',epsilon,L*tau/(4*s.pi*C*A*T*vth))
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'mutation':args.mutate,'scope':'Exact continuity and heat identities for trial flat tail; subsonic thermal closure; no global halo stability.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
