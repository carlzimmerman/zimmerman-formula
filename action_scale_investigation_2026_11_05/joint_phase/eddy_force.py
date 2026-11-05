"""Stress-correct weak gravity of canonical scalar vortices."""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp, quad

ap=argparse.ArgumentParser()
ap.add_argument('--out',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok)
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)

kr,ka,u=s.symbols('K_radial K_angular U',nonnegative=True)
rho=kr+ka+u
pr=kr-ka-u
pa=-kr+ka-u
pz=-kr-ka-u
active=s.expand(rho+pr+pa+pz)
used=rho if args.mutate else active
check('full stress active source',s.simplify(used+2*u)==0)
check('pure gradient active source cancels',s.simplify(used.subs(u,0))==0)
f,omega,lam,v,d=s.symbols('f omega lambda v deficit',positive=True)
finf2=v*v+omega*omega/lam
potential=lambda fsq:lam*(fsq-v*v)**2/4
delta_source=2*omega**2*(-d)-2*(potential(finf2-d)-potential(finf2))
check('rotating vortex excess active source',s.simplify(delta_source+omega**2*d+lam*d*d/2)==0)
x=s.symbols('x',positive=True)
F=s.Function('F')(x)
fp=s.diff(F,x)
B=x*x*fp*fp/2-F*F/2-x*x*(1-F*F)**2/4
ode=-fp/x+F/x**2+F*(F*F-1)
check('radial virial derivative',s.simplify(s.diff(B,x).subs(s.diff(F,x,2),ode)+x*(1-F*F)**2/2)==0)

profiles=[]
eps=1e-4
for radius in [20.,40.,80.]:
    solutions=[]
    for nodes,tol in [(400,1e-8),(800,1e-9)]:
        mesh=np.geomspace(eps,radius,nodes)
        guess=np.vstack([mesh/np.sqrt(1+mesh*mesh),(1+mesh*mesh)**(-1.5)])
        def rhs(xx,yy):
            return np.vstack([yy[1],-yy[1]/xx+yy[0]/xx**2+yy[0]*(yy[0]**2-1)])
        def bc(left,right):
            return np.array([left[1]-left[0]/eps,right[0]-(1-1/(2*radius**2))])
        sol=solve_bvp(rhs,bc,mesh,guess,tol=tol,max_nodes=20000)
        label=f'R={radius:g} nodes={nodes}'
        check(label+' solver converges',sol.success)
        if not sol.success:
            raise RuntimeError(sol.message)
        def integrand(xx):
            ff=float(sol.sol(xx)[0])
            return xx*(1-ff*ff)**2
        integral,qerr=quad(integrand,eps,radius,epsabs=1e-10,epsrel=1e-10,limit=300)
        def bval(xx):
            ff,ffp=sol.sol(xx)
            return xx*xx*ffp*ffp/2-ff*ff/2-xx*xx*(1-ff*ff)**2/4
        boundary=-2*(bval(radius)-bval(eps))
        residual=abs(integral-boundary)/max(abs(boundary),1e-15)
        check(label+' finite domain virial',residual<1e-6)
        # The excluded tiny core contributes eps^2/2 at leading order.
        corrected=integral+eps*eps/2+1/(2*radius**2)
        check(label+' far field force normalization',abs(corrected-1)<1e-4)
        sample=np.geomspace(eps,radius,1001)
        values=sol.sol(sample)[0]
        check(label+' sampled fundamental profile range',np.min(values)>=-1e-6 and np.max(values)<=1+1e-6)
        profiles.append({'R':radius,'initial_nodes':nodes,'tolerance':tol,'final_nodes':sol.x.size,
                         'integral':integral,'quad_error_estimate':qerr,'virial_boundary':float(boundary),
                         'virial_relative_residual':float(residual),'core_and_tail_corrected_integral':corrected,
                         'x':sample.tolist(),'F':values.tolist()})
        solutions.append(sol)
    sample=np.geomspace(eps,radius,1001)
    diff=float(np.max(np.abs(solutions[0].sol(sample)[0]-solutions[1].sol(sample)[0])))
    check(f'R={radius:g} independent resolution agreement',diff<1e-5)

result={'passed':all(checks.values()),'mode':'density_only_source' if args.mutate else 'main',
        'checks':checks,'profiles':profiles,
        'scope':'Leading weak-field canonical global vortex and analytic finite-charge contrast; '
                'not a finite galaxy or a fully backreacted rotating metric.',
        'results':{'active_static':'-2 U','active_rotating_excess':'-omega^2 deficit-lambda deficit^2/2',
                   'far_radial_acceleration':'outward 2 pi G n^2 v0^2 / r'}}
Path(args.out).parent.mkdir(parents=True,exist_ok=True)
Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['passed'] else 1)
