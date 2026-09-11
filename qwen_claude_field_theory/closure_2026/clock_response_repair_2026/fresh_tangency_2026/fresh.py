#!/usr/bin/env python3
"""Re-evolve after the center repair; never substitute the historical cache."""
import argparse
import json
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'nonlinear_evolution_2026'))
sys.path.insert(0,str(BASE/'origin_tangency_2026'))
from evolve import evolve, Evolution
from project import project_state
from tangent_linear import tangent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path,required=True)
    parser.add_argument('--points',type=int,nargs='+',default=[65,129,257])
    parser.add_argument('--dt',type=float,default=.00025)
    args=parser.parse_args()
    rows=[]
    for n in args.points:
        started=time.monotonic()
        run=evolve(.02,.3,tend=.02,dt=args.dt,points=n,outer=3.,gamma=1e-6)
        statefile=args.result_file.parent/f'state_{n}.npz'
        np.savez_compressed(statefile,r=run['r'],state=run['state'])
        system=Evolution(.02,.3,n,3.,.022,1e-6)
        state=project_state(.02,run['state'],run['r'],system.model)
        diagnostics=[tangent(system,state,.02,step) for step in (1e-4,1e-5)]
        row=dict(configuration=run['configuration'],snapshots=run['snapshots'],
                 tangent=diagnostics,state_file=str(statefile),
                 seconds=time.monotonic()-started)
        rows.append(row)
        result=dict(scope='Fresh evolved states; bounded diagnostics, not a continuum proof',
                    full_theory_status='OPEN',cases=rows)
        args.result_file.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
