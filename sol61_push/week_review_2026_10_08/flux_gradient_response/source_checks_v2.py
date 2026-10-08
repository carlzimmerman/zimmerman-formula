"""Finite-source matching checks; bounds, not an infinite-domain proof."""
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp
ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail),flush=True)
r=s.symbols('r',positive=True)
M=(35*r**3-42*r**5+15*r**7)/8
S=M/r**2
check('Enclosed mass normalized',M.subs(r,1)==1)
check('Density nonnegative interior square',s.expand(s.diff(M,r)/r**2-s.Rational(105,8)*(1-r**2)**2)==0)
check('Source field continuous',S.subs(r,1)==1)
check('Source derivative continuous',s.diff(S,r).subs(r,1)==-2)
lap=s.diff(S,r,2)+2*s.diff(S,r)/r-2*S/r**2
sgn=1 if args.mutate else -1
check('Density gradient forcing sign',s.simplify(lap-sgn*s.Rational(105,2)*r*(1-r*r))==0,lap)
F,c,kap,a0=s.symbols('F c kappa a0',positive=True)
d=2*(c-s.Rational(35,8))/(27*kap*s.sqrt(c/a0))
check('Central fractional expansion coefficient',s.simplify(s.Rational(27,4)*d-
 (c-s.Rational(35,8))/(2*kap*s.sqrt(c/a0)))==0)

def source(x):
    return np.where(x<=1,(35*x-42*x**3+15*x**5)/8,1/x**2)
numeric=[]
for kap in [.1,1.]:
    sols=[]
    for rmin,rmax in [(1e-4,10.),(1e-5,15.)]:
        grid=np.unique(np.r_[np.geomspace(rmin,1,250),np.linspace(1,rmax,450)])
        init=np.vstack([source(grid),np.where(grid<=1,(35-126*grid**2+75*grid**4)/8,-2/grid**3)])
        def ode(x,y):
            flux=np.maximum(y[0],1e-14)
            nu=2*np.sqrt(flux*flux+flux)/(2*flux+1)
            return np.vstack([y[1],2*flux/x**2-2*y[1]/x+(flux-source(x))/(kap*nu)])
        sol=solve_bvp(ode,lambda a,b:np.array([a[1]-a[0]/rmin,b[0]-1/rmax**2]),
            grid,init,tol=1e-8,max_nodes=20000)
        check('Source BVP converged '+str((kap,rmin,rmax)),sol.success,sol.message)
        x=np.geomspace(rmin,rmax,3001)
        flux=sol.sol(x)[0]
        check('Accepted source flux positive '+str((kap,rmin)),flux.min()>1e-8,flux.min())
        ratio=flux/source(x)
        check('Source comparison F at most S '+str((kap,rmin)),np.max(ratio)<1+1e-8,np.max(ratio))
        check('Strict source suppression inside r=3 '+str((kap,rmin)),np.max(ratio[x<3])<.9999)
        sols.append(sol)
    xx=np.geomspace(.01,8,1501)
    difference=np.max(np.abs(sols[0].sol(xx)[0]-sols[1].sol(xx)[0]))
    check('Moving both truncation boundaries '+str(kap),difference<2e-7,difference)
    sample=np.array([.1,.5,1.,2.,3.,5.])
    flux=sols[-1].sol(sample)[0]
    src=source(sample)
    accel_ratio=np.sqrt((flux*flux+flux)/(src*src+src))
    x=np.geomspace(.001,10,601)
    field=sols[-1].sol(x)[0]
    numeric.append(dict(kappa=kap,r=x.tolist(),flux_ratio=(field/source(x)).tolist(),
        acceleration_ratio=np.sqrt((field*field+field)/(source(x)**2+source(x))).tolist(),
        sample_r=sample.tolist(),sample_flux_ratio=(flux/src).tolist(),
        sample_acceleration_ratio=accel_ratio.tolist(),boundary_difference=float(difference)))
Path(args.output).write_text(json.dumps(dict(checks=checks,numeric=numeric,mutation=args.mutate),indent=2)+'\n')
print(str(sum(x['passed'] for x in checks))+'/'+str(len(checks))+' passed',flush=True)
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
