"""Local rate-law obstruction and phenomenological global attractor."""
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
def zero(e):return s.simplify(e)==0
A,B,d=s.symbols('A B d',positive=True);h,eta=s.symbols('h eta',real=True)
J=s.Matrix([[-d*B,h*B],[-A+eta*d*B,-A-eta*h*B]])
claimed=A*B*(d if args.mutate else d+h)
check('general determinant',zero(J.det()-claimed))
check('scaling-compatible neutral mode',zero(claimed.subs(h,-d)))
x,y,a,b=s.symbols('x y a b',positive=True)
local=s.Matrix([x*(1-x*y),1-x*y])
check('local invariant',zero(s.diff(s.log(x)-y,x)*local[0]+s.diff(s.log(x)-y,y)*local[1]))
field=s.Matrix([a*(y-x),b*(1-x*y)])
V=b*(x-1)**2/(2*a)+(y-1)**2/2
check('global Lyapunov identity',zero(s.diff(V,x)*field[0]+s.diff(V,y)*field[1]+b*((x-1)**2+x*(y-1)**2)))
JC=field.jacobian([x,y]).subs({x:1,y:1})
check('global trace',zero(s.trace(JC)+a+b))
check('global determinant',zero(JC.det()-2*a*b))
runs=[]
for model in ['A','B','C']:
    for initial in [[.2,.5],[2.,.5],[.5,2.],[3.,2.]]:
        def rhs(t,z):
            n,T=z
            if model=='A':return [1-n,1-n*T]
            if model=='B':return [n*(1-n*T),1-n*T]
            return [T-n,1-n*T]
        sol=solve_ivp(rhs,(0,60),initial,method='DOP853',rtol=1e-10,atol=1e-12,max_step=.1,dense_output=True)
        grid=np.linspace(0,60,601);ys=sol.sol(grid);last=ys[:,-1]
        name=f'{model} {initial}'
        check(name+' positive complete trajectory',sol.success and np.all(ys>0))
        if model in ['A','C']:
            check(name+' common equilibrium',np.max(abs(last-1))<1e-7)
        else:
            inv=np.log(ys[0])-ys[1];inv0=np.log(initial[0])-initial[1]
            check(name+' invariant',np.max(abs(inv-inv0))<1e-7)
            check(name+' thermal equilibrium',abs(last[0]*last[1]-1)<1e-7)
            nr=brentq(lambda n:np.log(n)-1/n-inv0,1e-5,100)
            check(name+' history-dependent analytic state',np.max(abs(last-[nr,1/nr]))<1e-7)
        if model=='C':
            energy=((ys[0]-1)**2+(ys[1]-1)**2)/2
            check(name+' Lyapunov decreases',np.max(np.diff(energy))<1e-10)
        runs.append({'model':model,'initial':initial,'final':last.tolist()})
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'runs':runs,'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
