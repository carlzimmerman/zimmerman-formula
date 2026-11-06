"""Exact checks of a specified wall and single-scatter capture model."""
import argparse, json
import sympy as s
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--out',required=True); p.add_argument('--mutate',action='store_true'); args=p.parse_args()
R,v,a,S,D,t,Rb=s.symbols('R v a Sigma Delta t Rb', positive=True)
gamma=1/s.sqrt(1-v*v)
L=-S*R**2/gamma+D*R**3/3
mom=s.diff(L,v)
el=s.diff(mom,R)*v+s.diff(mom,v)*a-s.diff(L,R)
checks={}
def eq(name,x,y): checks[name]=bool(s.simplify(x-y)==0)
eq('wall Euler Lagrange',el/R**2,S*gamma**3*a+2*S*gamma/R-D)
energy=v*mom-L
eq('wall conserved energy',energy,S*R**2*gamma-D*R**3/3)
P=s.symbols('P',positive=True)
acc=(D-P-2*S*gamma/R)/(S*gamma**3)
Edot=s.diff(energy,R)*v+s.diff(energy,v)*acc
eq('drag energy loss',Edot,-R**2*P*v)
trajectory=s.sqrt(Rb**2+t**2)
vel=s.diff(trajectory,t); acceleration=s.diff(vel,t)
eq('hyperbolic gamma',gamma.subs(v,vel),trajectory/Rb)
eq('empty wall trajectory', (S*gamma**3*a+2*S*gamma/R-D).subs({v:vel,a:acceleration,R:trajectory,D:3*S/Rb}),0)
eq('empty wall zero total energy',energy.subs({v:vel,R:trajectory,D:3*S/Rb}),0)
# Divide physical powers by 4*pi. An empty classical wall has no radiation.
wall_dot=s.simplify(s.diff(S*R**2*gamma,R)*v+s.diff(S*R**2*gamma,v)*acc.subs(P,0))
rad=D*R**2*v if args.mutate else 0
eq('latent power budget',wall_dot+rad,D*R**2*v)
w,rho,sd=s.symbols('w rho sd',positive=True)
drag=2*rho*((sd**2+w**2)*s.erf(w/(s.sqrt(2)*sd))+s.sqrt(2/s.pi)*sd*w*s.exp(-w*w/(2*sd*sd)))
eq('Maxwell linear drag',s.diff(drag,w).subs(w,0),4*rho*s.sqrt(2/s.pi)*sd)
eq('critical radius unstable pressure slope',s.diff(D-2*S/R,R).subs(R,2*S/D),D**2/(2*S))
k,q=s.symbols('k q',positive=True)
ref=(k-q)**2/(k+q)**2; trans=4*k*q/(k+q)**2
eq('mass step flux conservation',ref+trans,1)
A,b,z,H=s.symbols('A b z H',positive=True)
primitive=A*s.atan(z/b)/b
eq('column primitive',s.diff(primitive,z),A/(b*b+z*z))
x=s.symbols('x',positive=True)
mean_column=s.integrate(4*s.pi*A*H*s.acos(x),(x,0,1))
eq('column area equals particle count',mean_column,4*s.pi*A*H)
m,E,lam,escape=s.symbols('m E lam escape',positive=True)
sigma=lam**2/(16*s.pi*m*(m+2*E)); Tmax=2*E**2/(m+2*E)
recoil=s.symbols('recoil',nonnegative=True)
eq('mean uniform recoil',s.integrate(recoil/Tmax,(recoil,0,Tmax)),E**2/(m+2*E))
cap=s.symbols('cap',positive=True)
retained=s.integrate(recoil/Tmax,(recoil,0,cap))
eq('retained heating fraction',retained/(Tmax/2),(cap/Tmax)**2)
eq('hard photon bound fraction',((m*escape**2/2)/Tmax).subs(E,m),3*escape**2/4)
sigmaE=sigma*E/(m+2*E)
eq('energy transfer cross section',sigma*Tmax/(2*E),sigmaE)
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'mutation':args.mutate,'scope':'Exact identities only; no halo equilibrium or stability simulation.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True); Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2)); raise SystemExit(0 if all(checks.values()) else 1)
