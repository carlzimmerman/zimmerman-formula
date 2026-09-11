#!/usr/bin/env python3
"""Hold evolved data fixed and separate adaptive projection error from grid error."""
import argparse
import json
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
import project
from evolve import Evolution,evolve


def run(points):
    start=time.monotonic()
    result=evolve(.02,.3,points=points,tend=.02,dt=.00025,outer=3.)
    state=result['state'];system=Evolution(.02,.3,points,3.,.021,1e-6)
    original=project.solve_ivp;rows=[]
    for label,rtol,atol,step in [('original',2e-10,2e-12,np.inf),
                                ('one_cell',2e-10,2e-12,system.dr),
                                ('half_cell',2e-10,2e-12,system.dr/2),
                                ('tighter',2e-12,2e-14,np.inf)]:
        before=time.monotonic()
        def integrate(*args,**kwargs):
            kwargs.update(rtol=rtol,atol=atol,max_step=step)
            return original(*args,**kwargs)
        project.solve_ivp=integrate
        try:
            f=system.fields(.02,state)
            mask=(system.r>2*system.dr)&(system.r<system.r[-1]-2*system.dr)
            row=dict(label=label,seconds=time.monotonic()-before,
                     constraint_max=np.max(abs(f['constraints'][mask]),axis=0).tolist(),
                     A_delta=float(max(abs(f['A']-state[0]))),h_delta=float(max(abs(f['h']-state[3]))))
            rows.append(row);print(json.dumps(dict(points=points,**row)),flush=True)
        finally:project.solve_ivp=original
    return dict(points=points,rows=rows,seconds=time.monotonic()-start)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--points',type=int,default=129);args=p.parse_args()
    run(args.points)
