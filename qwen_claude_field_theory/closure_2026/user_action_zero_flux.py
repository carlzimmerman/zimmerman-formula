"""Construct zero conserved scalar flux with the calibrated curved equations.

Vacuum planar boundary data, not a sourced MOND or PPN certification.
"""
import json
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import user_action_calibrated_branch as m
rows=[]
for length in (.2,.1):
    seed=np.array([0.,0.,.02*(.2+np.exp(-.02))/2,.02,-.02,0.])
    def energy(slope):
        y=seed.copy();y[-1]=slope
        return float(m.ef(*m.arguments(y,0.,length)))
    root=brentq(energy,0.,10.,xtol=1e-13)
    for sign in (-1,1):
        initial=seed.copy();initial[-1]=sign*root
        def rhs(x,y):
            args=m.arguments(y,0.,length)
            return np.r_[y[3:],np.linalg.solve(m.hf(*args),np.asarray(m.ff(*args)).ravel())]
        sol=solve_ivp(rhs,(0.,.02),initial,rtol=1e-10,atol=1e-12,dense_output=True)
        samples=sol.sol(np.linspace(0,.02,101)) if sol.success else sol.y
        rows.append(dict(xi=length,initial_vprime=sign*root,initial_constraint=energy(sign*root),
            success=sol.success,max_constraint=float(max(abs(m.ef(*m.arguments(y,0.,length))) for y in samples.T)),
            max_logarithmic_slip=float(max(abs(samples[0]+samples[1]))),final_state=sol.y[:,-1].tolist()))
print(json.dumps(dict(full_theory='OPEN',scope=__doc__,scalar_flux=0,runs=rows),indent=2))
raise SystemExit(0 if all(r['success'] for r in rows) else 1)
