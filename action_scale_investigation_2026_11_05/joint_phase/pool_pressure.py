"""Pressure-confined pool mass extremum; no target coefficient as input."""
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
x=s.symbols('x',positive=True);p=s.Function('psi')(x);q=s.diff(p,x)
mu=x*x*q*s.exp(-p/2)/s.sqrt(4*s.pi)
exact=s.diff(mu,x).subs(s.diff(p,x,2),s.exp(-p)-2*q/x)
claimed=x*x*s.exp(-p/2)*(s.exp(-p)-(0 if args.mutate else q*q/2))/s.sqrt(4*s.pi)
check('mass derivative includes surface density change',s.simplify(exact-claimed)==0)

runs=[]
for tol,step in [(1e-9,.05),(1e-11,.025)]:
    eps=1e-5
    init=[eps**2/6-eps**4/120+eps**6/1890,eps/3-eps**3/30+eps**5/315]
    sol=solve_ivp(lambda xx,yy:[yy[1],np.exp(-yy[0])-2*yy[1]/xx],(eps,12),init,
                  method='DOP853',rtol=tol,atol=tol/100,max_step=step,dense_output=True)
    check(f'{tol:g} integration completes',sol.success)
    def crit(xx):
        pp,qq=sol.sol(xx);return 2*np.exp(-pp)-qq*qq
    xx=np.linspace(.01,12,2400)
    ids=np.where(np.array([crit(a)*crit(b)<0 for a,b in zip(xx[:-1],xx[1:])]))[0]
    check(f'{tol:g} first critical root exists',len(ids)>0)
    i=ids[0];root=brentq(crit,xx[i],xx[i+1],xtol=1e-12)
    pp,qq=sol.sol(root)
    mass=float(root**2*qq*np.exp(-pp/2)/np.sqrt(4*np.pi))
    beta=float(root*qq)
    check(f'{tol:g} critical point is first maximum',crit(root-1e-3)>0 and crit(root+1e-3)<0)
    check(f'{tol:g} exact edge acceleration identity',abs(beta**2/mass/np.sqrt(8*np.pi)-1)<1e-7)
    sample=np.linspace(.01,root,201); vals=sol.sol(sample)
    runs.append({'tolerance':tol,'max_step':step,'critical_radius':root,'critical_mass_mu':mass,
                 'surface_density_contrast':float(np.exp(pp)),'edge_speed_squared_over_cs_squared':beta,
                 'formal_flat_coefficient':4/mass,'edge_coefficient':beta**2/mass,
                 'x':sample.tolist(),'psi':vals[0].tolist(),'circular_speed_squared_over_cs_squared':(sample*vals[1]).tolist()})
for key in ['critical_radius','critical_mass_mu']:
    check(key+' independent integration agreement',abs(runs[0][key]/runs[1][key]-1)<1e-6)

mass_scale=s.symbols('mass_scale',positive=True)
# At fixed vacuum density, Newtonian similarity gives r~M_b^(1/3), cs^2~M_b^(2/3).
check('turnaround normalization retains mass dependence',s.simplify((mass_scale**s.Rational(2,3))**2/mass_scale-mass_scale**s.Rational(1,3))==0)
out={'passed':all(checks.values()),'mode':'omit_surface_density_derivative' if args.mutate else 'main',
     'checks':checks,'runs':runs,'scope':'Pressure-confined self-gravitating pool first mass maximum; '
     'not a derived confining mechanism, baryonic inventory, extended flat curve or cosmological attractor.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
