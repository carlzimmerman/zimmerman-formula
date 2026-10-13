"""Finite-stiffness sourced static profiles for the existing convex extension."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_bvp, simpson
P=Path(__file__).parent
checks={}; rows=[]; profiles={}
def run(eps,R,tol,inner):
    r=np.geomspace(inner,R,750)
    guess=r/(1+r*r)
    def fun(x,y):
        f=x/(1+x*x)**1.5
        return np.vstack((y[1],(y[0]*np.abs(y[0])-f)/eps-2*y[1]/x+2*y[0]/x**2))
    # Far boundary uses two asymptotic terms, not an exact infinite boundary.
    boundary=1/R-eps/R**2
    def bc(l,h):return np.array([l[1]-l[0]/inner,h[0]-boundary])
    sol=solve_bvp(fun,bc,r,np.vstack((guess,(1-r*r)/(1+r*r)**2)),tol=tol,max_nodes=30000)
    x=np.geomspace(inner,R,20001); p,dp=sol.sol(x); f=x/(1+x*x)**1.5
    lhs=simpson(eps*(x*x*dp*dp+2*p*p)+x*x*np.abs(p)**3,x=x)
    rhs=simpson(x*x*f*p,x=x)+eps*(x[-1]**2*p[-1]*dp[-1]-x[0]**2*p[0]*dp[0])
    key=f'{eps}_{R}_{tol}'
    checks[key+'_converged']=bool(sol.success)
    checks[key+'_positive']=bool(np.min(p)>0)
    checks[key+'_integrated_balance']=bool(abs(lhs-rhs)/abs(lhs)<2e-6)
    sample=np.array([.1,1.,10.,30.,100.])
    vals=sol.sol(sample)[0]; ideal=np.sqrt(sample/(1+sample*sample)**1.5)
    rows.append(dict(epsilon=eps,R=R,tolerance=tol,nodes=sol.x.size,
                     balance_relative_error=float(abs(lhs-rhs)/abs(lhs)),
                     radii=sample.tolist(),p_over_zero_stiffness=(vals/ideal).tolist()))
    return sol
for eps in [.001,.01,.1,1.,10.]:
    base=run(eps,200.,2e-8,1e-4)
    fine=run(eps,400.,2e-8,1e-5)
    grid=np.geomspace(.1,30.,300)
    discrepancy=float(np.max(np.abs(base.sol(grid)[0]/fine.sol(grid)[0]-1)))
    checks[f'{eps}_refinement']=discrepancy<2e-4
    profiles[str(eps)]=dict(r=grid.tolist(),p=fine.sol(grid)[0].tolist(),refinement_max_relative=discrepancy)
result=dict(checks=checks,all_pass=all(checks.values()),rows=rows,profiles=profiles,
            scope='Fixed Plummer baryon source, phenomenological convex action, finite radial domains; no carrier derivation, live baryons, vacuum normalization or observational fit.')
(P/'sourced_polarization_run_v3'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(checks=checks,rows=rows),indent=2));assert result['all_pass']
