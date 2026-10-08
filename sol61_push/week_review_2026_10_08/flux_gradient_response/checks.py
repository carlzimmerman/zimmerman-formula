"""Exact identities and bounded shell tests for the proposed flux stiffness."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_bvp
ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail),flush=True)
r,B,a0,g,kappa,h,Z,F=s.symbols('r B a0 g kappa h Z F',positive=True)
constit=(s.sqrt(a0*a0+4*g*g)-a0)/2
inverse=s.sqrt(F*F+a0*F)
nu=2*inverse/(2*F+a0)
check('P2 inverse',s.simplify(inverse**2-F**2-a0*F)==0)
check('Inverse differential Jacobian',s.simplify(nu*s.diff(inverse,F)-1)==0)
check('Radial monotonicity identity',s.simplify(F*s.diff(nu,F)/nu-a0*a0/(2*(F+a0)*(2*F+a0)))==0)
check('Radial monotonicity upper bound',s.factor(2*(F+a0)*(2*F+a0)-2*a0*a0)>0)

def radial_lap(expr):
    return s.diff(expr,r,2)+2*s.diff(expr,r)/r-2*expr/r**2
f0=B/r**2
check('Inverse square vector harmonic',s.simplify(radial_lap(f0))==0)
wrong_f=B/r
check('Deep acceleration is not harmonic flux',s.simplify(radial_lap(wrong_f)+2*B/r**3)==0)

# Direct Euler variation of the spherical radial energy with generic F(g).
rr=s.symbols('rr',positive=True)
v=s.Function('v')(rr)
fun=s.Function('f')
pot=s.Function('W')
fv=fun(v)
density=rr**2*(pot(v)+kappa*(s.diff(fv,rr)**2+2*fv**2/rr**2)/2)
variation=s.diff(density,v)-s.diff(s.diff(density,s.diff(v,rr)),rr)
target=rr**2*(s.diff(pot(v),v)-kappa*s.diff(fun(v),v)*
    (s.diff(fv,rr,2)+2*s.diff(fv,rr)/rr-2*fv/rr**2))
check('Independent radial energy variation',s.simplify(variation-target)==0)

# Local positive principal symbol around a constant nonzero background.
kp,kt,mu,n=s.symbols('kparallel ktransverse mu nu',positive=True)
k2=kp*kp+kt*kt
T=Z*k2/(4*h*g)
sign=-1 if args.mutate else 1
S=(mu*kt*kt+n*kp*kp+sign*kappa*k2*(mu*mu*kt*kt+n*n*kp*kp))/2
expected=2*h*g/Z*((mu*kt*kt+n*kp*kp)/k2+kappa*(mu*mu*kt*kt+n*n*kp*kp))
check('All-direction local dispersion',s.simplify(S/T-expected)==0)
check('Parallel high wavenumber stiffness',s.expand(S).coeff(kp,4)>0)
check('Transverse high wavenumber stiffness',s.expand(S).coeff(kt,4)>0)

# Deep linearization: C=2 sqrt(B/a0), ell^3=kappa C.
C=s.symbols('C',positive=True)
arg=2*r**s.Rational(3,2)/(3*s.sqrt(kappa*C))
tail=r**s.Rational(-1,2)*s.besselk(1,arg)
res=radial_lap(tail)-r*tail/(kappa*C)
check('Exact deep linear Bessel mode',s.simplify(s.expand_func(res))==0)
ell=(kappa*C)**s.Rational(1,3)
check('Stretched exponential argument',s.simplify(arg-s.Rational(2,3)*(r/ell)**s.Rational(3,2))==0)
check('Bessel algebraic prefactor',s.simplify(r**s.Rational(-1,2)/s.sqrt(arg)/
      (s.sqrt(s.Rational(3,2))*(kappa*C)**s.Rational(1,4)*r**s.Rational(-5,4)))==1)

# Known Newtonian limiting counterexample to automatic exterior matching.
ellN=s.symbols('ellN',positive=True)
newton=B/r**2*(1-(1+r/ellN)*s.exp(-r/ellN))
check('Newtonian screened exterior solution',s.simplify(newton-ellN**2*radial_lap(newton)-B/r**2)==0)
check('Newtonian exterior need not be exact inverse square',s.simplify(newton-B/r**2)!=0)

numeric=[]
for kap in [.1,1.]:
    for ratio in [.8,1.2]:
        sols=[]
        for nodes in [180,360]:
            grid=np.linspace(1,10,nodes)
            # The floor only protects intermediate Newton iterates, never the accepted solution.
            def ode(rr,yy):
                field=np.maximum(yy[0],1e-12)
                derivative=2*np.sqrt(field*field+field)/(2*field+1)
                return np.vstack([yy[1],2*field/rr**2-2*yy[1]/rr+(field-1/rr**2)/(kap*derivative)])
            sol=solve_bvp(ode,lambda left,right:np.array([left[0]-ratio,right[0]-.01]),
                grid,np.vstack([1/grid**2,-2/grid**3]),tol=1e-8,max_nodes=10000)
            check('BVP convergence '+str((kap,ratio,nodes)),sol.success,sol.message)
            sols.append(sol)
        x=np.linspace(1,10,2001)
        vals=sols[-1].sol(x)
        field=vals[0]
        check('Accepted flux stays positive '+str((kap,ratio)),field.min()>1e-3,field.min())
        disagreement=np.max(np.abs(sols[0].sol(x)[0]-field))
        check('Independent mesh agreement '+str((kap,ratio)),disagreement<2e-8,disagreement)
        scaled=field*x*x
        lo=min(1,ratio); hi=max(1,ratio)
        check('Maximum principle bounds '+str((kap,ratio)),scaled.min()>lo-2e-8 and scaled.max()<hi+2e-8)
        delta=field-1/x**2
        check('Boundary correction has no interior sign reversal '+str((kap,ratio)),
            np.min(np.sign(ratio-1)*delta)>-2e-10)
        # Cubic collocation derivative evaluated between mesh nodes, independent of ode output.
        dv=sols[-1].sol(x,1)[1]
        vnu=2*np.sqrt(field*field+field)/(2*field+1)
        current=field-kap*vnu*(dv+2*vals[1]/x-2*field/x**2)
        err=np.max(np.abs(current-1/x**2))
        check('Gauss current residual '+str((kap,ratio)),err<2e-7,err)
        sample=sols[-1].sol(np.array([1.,2.,3.,5.,10.]))[0]*np.array([1.,2.,3.,5.,10.])**2
        numeric.append(dict(kappa=kap,inner_ratio=ratio,r=x[::10].tolist(),
            flux_ratio=scaled[::10].tolist(),samples=sample.tolist(),
            max_current_error=float(err),mesh_disagreement=float(disagreement)))
Path(args.output).write_text(json.dumps(dict(checks=checks,numeric=numeric,mutation=args.mutate),indent=2)+'\n')
print(str(sum(x['passed'] for x in checks))+'/'+str(len(checks))+' passed',flush=True)
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
