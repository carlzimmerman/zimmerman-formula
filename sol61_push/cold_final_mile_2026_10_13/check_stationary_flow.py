"""CE-FM-006: actual finite-annulus stationary IVP, frozen central source comparison."""
import json,sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

r=s.symbols('r',positive=True)
m0=(s.sqrt(1+4*r*r)-1)/2
mu=-(s.sqrt(1+4*r*r)-1)**2/(16*r*s.sqrt(1+4*r*r))
ic_m=s.lambdify(r,m0,'numpy');ic_p=s.lambdify(r,s.diff(m0,r),'numpy')
ic_mu=s.lambdify(r,mu,'numpy');ic_mup=s.lambdify(r,s.diff(mu,r),'numpy')
grid=np.geomspace(2,50,20001)
checks=[];rows=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)

for F in (.03,.1,.3):
    initial=[float(ic_m(2)+F*F*ic_mu(2)),float(F/(ic_p(2)+F*F*ic_mup(2))),0.]
    def rhs(radius,y):
        M,v,I=y;u=M/radius**2
        if v<=0 or not 0<u<1:raise ValueError('outside stationary flow domain')
        R=u*u/(1-u)
        return [F/v,(-1/radius**2+R)/v,R]
    solution=solve_ivp(rhs,(2,50),initial,method='DOP853',rtol=1e-11,atol=1e-13,dense_output=True)
    check(f'IVP completed F={F}',solution.success,solution.message)
    M,v,I=solution.sol(grid);u=M/grid**2
    check(f'admissible inward stream F={F}',np.all((v>0)&(u>0)&(u<1)),{'minimum_speed':float(np.min(v)),'maximum_u':float(np.max(u))})
    bernoulli=.5*v*v-1/grid-I
    drift=float(np.max(np.abs(bernoulli-bernoulli[0])))
    check(f'Bernoulli invariant F={F}',drift<1e-9,drift)
    formal=ic_m(grid)+F*F*ic_mu(grid)
    deviation=float(np.max(np.abs(M-formal)))
    # This tolerance tests a new finite IVP, not convergence of a universal expansion.
    check(f'formal branch correspondence F={F}',deviation<2*F**4,deviation)
    T=float(np.trapz(1/v,grid))
    mass_change=float(M[-1]-M[0]);replacement=mass_change/F
    err=abs(T/replacement-1)
    check(f'residence mass flux identity F={F}',err<1e-7,err)
    rows.append(dict(F=F,nfev=solution.nfev,mass_at_inner=float(M[0]),mass_at_outer=float(M[-1]),
                     maximum_absolute_formal_deviation=deviation,bernoulli_drift=drift,
                     residence_time=T,captured_mass_during_one_residence_if_retained=F*T,
                     central_mass_fraction_change_during_residence=F*T,
                     max_relative_law_mass_deviation=float(np.max(np.abs(M/ic_m(grid)-1)))))
result=dict(checks=checks,stationary_IVPs=rows,
            scope='Finite-annulus cold radial one-stream IVPs, fixed central mass; existence only on tested interval, no formation or physical receiver.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
