"""Eliminate the spatial constraint before searching no-slip compatibility.

At fixed calibrated action parameters, P=B=0, P'=-B'=.02, flux=0,
solve E_A=0 for w=xi*v' on both signs, then compute P''+B''.
Finite samples cannot exclude unsampled roots or other boundary data.
"""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import user_action_calibrated_branch as m

def run():
    rows=[]
    for length in (.2,.1):
        for v in np.geomspace(1e-5,10.,121):
            def state(w):return np.array([0.,0.,v,.02,-.02,w/length])
            def energy(w):return float(m.ef(*m.arguments(state(w),0.,length)))
            upper=max(1.,20*v)
            left,right=energy(0.),energy(upper)
            assert left*right<0, 'Declared bracket does not enclose a root'
            w=brentq(energy,0.,upper,xtol=1e-13)
            for sign in (-1,1):
                y=state(sign*w);args=m.arguments(y,0.,length)
                matrix=m.hf(*args);forcing=np.asarray(m.ff(*args)).ravel()
                acceleration=np.linalg.solve(matrix,forcing)
                scale=1+abs(float(m.ef(*m.arguments(y,1.,length))))
                residual=energy(sign*w)
                assert abs(residual)/scale<1e-8, 'Constraint root inaccurate'
                rows.append(dict(xi=length,v=float(v),vprime=float(y[-1]),
                    constraint=float(residual),slip_curvature=float(acceleration[0]+acceleration[1]),
                    hessian_condition=float(np.linalg.cond(matrix)),
                    relative_linear_solve_residual=float(np.linalg.norm(matrix@acceleration-forcing)/(1+np.linalg.norm(forcing)))))
    summary=[dict(xi=length,
                  minimum=min(r['slip_curvature'] for r in rows if r['xi']==length),
                  maximum=max(r['slip_curvature'] for r in rows if r['xi']==length)) for length in (.2,.1)]
    return dict(base='3e52670d0',full_theory='OPEN',scope=__doc__,rows=rows,summary=summary,
                normalization='Inherited dimensionless g=.35, ca=.1, b=1, C=.01, a0=1; no parameter fitting')

if __name__=='__main__':print(json.dumps(run(),indent=2))
