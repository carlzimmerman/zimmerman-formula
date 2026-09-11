#!/usr/bin/env python3
"""Projection tangency with independent radial error budgets and saved states."""
import json
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
import project
from evolve import Evolution


def run():
    saved=np.load(HERE/'run_002/states.npz');original=project.solve_ivp;rows=[]
    for index in (1,2):
        raw=saved['state_'+str(index)];r=saved['r_'+str(index)];n=len(r)
        system=Evolution(.02,.3,n,3.,.022,1e-6)
        for label,rtol,atol in [('evolution_budget',2e-10,2e-12),('diagnostic_budget',2e-12,2e-14)]:
            def integrate(*args,**kw):
                kw.update(rtol=rtol,atol=atol);return original(*args,**kw)
            project.solve_ivp=integrate
            try:
                state=project.project_state(.02,raw,r,system.model)
                rate,_=system.rhs(.02,state)
                for step in (1e-3,5e-4,2.5e-4,1e-4):
                    start=time.monotonic()
                    plus=project.project_state(.02+step,state+step*rate,r,system.model)
                    minus=project.project_state(.02-step,state-step*rate,r,system.model)
                    error=(plus-minus)/(2*step)-rate
                    cuts={}
                    for cutoff in (0.,.1,.3):
                        mask=(r>=cutoff)&(r<2.8);indices=np.flatnonzero(mask)
                        cuts[str(cutoff)]={name:dict(error=float(np.max(abs(error[j,mask]))),
                            radius=float(r[indices[np.argmax(abs(error[j,mask]))]])) for name,j in [('A',0),('h',3),('k',2)]}
                    row=dict(points=n,budget=label,step=step,seconds=time.monotonic()-start,cuts=cuts)
                    rows.append(row);print(json.dumps(row),flush=True)
            finally:project.solve_ivp=original
    return rows


if __name__=='__main__':run()
