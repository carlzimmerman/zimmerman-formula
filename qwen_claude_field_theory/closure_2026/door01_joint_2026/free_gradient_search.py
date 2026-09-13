"""Search no-slip initial gradients after eliminating the zero-flux constraint.

For each fixed scalar gradient v and xi, unknowns are P' and v'; B'=-P'
enforces initial no-slip. Residuals are the spatial constraint and P''+B''.
This is a bounded search, not an exclusion proof.
"""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import least_squares
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import user_action_calibrated_branch as m

def residual(x, v, xi):
    pp,vp=x; y=np.array([0.,0.,v,pp,-pp,vp])
    args=m.arguments(y,0.,xi)
    acceleration=np.linalg.solve(m.hf(*args),np.asarray(m.ff(*args)).ravel())
    return np.array([float(m.ef(*args)),float(acceleration[0]+acceleration[1])])

def run():
    rows=[]
    for xi in (.2,.1):
        for v in (.001,.01,.02,.05,.1):
            best=None
            guesses=np.array(np.meshgrid(np.geomspace(1e-5,1,6),np.linspace(-10,10,7))).reshape(2,-1).T
            for magnitude,slope in guesses:
                for sign in (-1,1):
                    solution=least_squares(lambda x:residual(x,v,xi),
                        [sign*magnitude,slope],bounds=([-10.,-100.],[10.,100.]),
                        xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=500)
                    norm=float(max(abs(residual(solution.x,v,xi))))
                    if best is None or norm<best['residual_max']:
                        best=dict(xi=xi,v=v,pp=float(solution.x[0]),
                                  vp=float(solution.x[1]),residual_max=norm,
                                  success=bool(solution.success),nfev=solution.nfev)
            rows.append(best)
    return dict(base='3e52670d0',full_theory='OPEN',scope=__doc__,runs=rows,
        fixed_conditions='P=B=0, P\'=-B\', scalar flux=0, calibrated kernel, dimensionless illustrative parameters',
        non_claims=['Finite optimizer search does not exclude roots outside bounds or tangencies'])

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
