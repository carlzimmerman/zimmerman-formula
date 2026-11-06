"""Decay/annihilation source with explicit particle and energy moments."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(x):return s.simplify(x)==0
M,m,g,lam,beta=s.symbols('M m g lam beta',positive=True)
check('identical-daughter decay factor',zero(g*g/(2*M)*beta/(8*s.pi)/2-g*g*beta/(32*s.pi*M)))
check('identical-radiation annihilation factor',zero(lam*lam/(4*m*m)/(8*s.pi)/2-lam*lam/(64*s.pi*m*m)))
n,T,J,K,cv,ei,E0=s.symbols('n T J K cv ei E0',positive=True)
ndot=J-K*n*n
Tdot=J*(ei-(0 if args.mutate else cv*T))/(cv*n)
energy=n*(E0+cv*T)
out=(E0+ei)*J-(E0+cv*T)*K*n*n
check('number and energy moment conservation',zero(s.diff(energy,n)*ndot+s.diff(energy,T)*Tdot-out))
check('positive number equilibrium',zero(ndot.subs(n,s.sqrt(J/K))))
check('thermal equilibrium',zero(Tdot.subs(T,ei/cv)))
# Proper conserved equation supplies physical stability independently of mutation.
physical=s.Matrix([ndot,J*(ei-cv*T)/(cv*n)])
jac=physical.jacobian([n,T]).subs({n:s.sqrt(J/K),T:ei/cv})
check('number relaxation eigenvalue',zero(jac[0,0]+2*s.sqrt(J*K)))
check('thermal relaxation eigenvalue',zero(jac[1,1]+s.sqrt(J*K)))
r,l,dotN,vS,ES,C,G=s.symbols('r l dotN vS ES C G',positive=True)
ns=dotN*s.exp(-r/l)/(4*s.pi*r*r*vS)
check('mediator transport equation',zero(s.diff(r*r*vS*ns,r)/r**2+vS/l*ns))
source=dotN*s.exp(-r/l)/(2*s.pi*l*r*r)
profile=s.sqrt(dotN/(2*s.pi*l*K))*s.exp(-r/(2*l))/r
check('pair production reaction balance',zero(source-K*profile**2))
check('energy injection total',zero(s.integrate(source*ES/2*4*s.pi*r*r,(r,0,s.oo))-dotN*ES))
mass=16*s.pi*m*C*l*l*(1-(1+r/(2*l))*s.exp(-r/(2*l)))
check('profile enclosed mass',zero(s.diff(mass,r)-4*s.pi*m*C*r*s.exp(-r/(2*l))))
check('central enclosed mass',zero(mass.subs(r,0)))
x=s.symbols('x',positive=True)
f=(1-(1+x)*s.exp(-x))/x
check('peak derivative',zero(s.diff(f,x)-((x*x+x+1)*s.exp(-x)-1)/x**2))
check('small radius rising speed',s.limit(f/x,x,0)==s.Rational(1,2))
check('large radius Kepler speed',s.limit(x*f,x,s.oo)==1)
check('required hydrostatic acceleration',zero(-s.diff(s.log(C*s.exp(-r/(2*l))/r),r)-(1/r+1/(2*l))))
root=brentq(lambda xx:(xx*xx+xx+1)*np.exp(-xx)-1,1,3,xtol=1e-13)
peak=float(f.subs(x,root))
check('nonzero peak found',abs((root*root+root+1)*np.exp(-root)-1)<1e-12)
runs=[]
for initial in [[.2,.5],[2.,.5],[.5,2.],[3.,4.]]:
    def rhs(t,z):
        nn,tt=z
        return [2-.5*nn*nn,2*(3-tt)/nn]
    sol=solve_ivp(rhs,(0,40),initial,method='DOP853',rtol=1e-10,atol=1e-12,max_step=.1,dense_output=True)
    ys=sol.sol(np.linspace(0,40,401))
    check(str(initial)+' positive complete solution',sol.success and np.all(ys>0))
    check(str(initial)+' common physical equilibrium',np.max(abs(ys[:,-1]-[2,3]))<1e-7)
    runs.append({'initial':initial,'final':ys[:,-1].tolist()})
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'peak_x':root,'peak_shape_factor':peak,'runs':runs,'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
