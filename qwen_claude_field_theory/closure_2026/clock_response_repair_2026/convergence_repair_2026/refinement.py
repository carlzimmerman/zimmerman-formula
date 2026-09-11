#!/usr/bin/env python3
"""Report spatial/time convergence and centered projection tangency, not forces."""
import json
import argparse
from pathlib import Path
import sys
import time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nonlinear_evolution_2026'))
from evolve import Evolution,evolve
from project import project_state


def run(state_cache=None):
    runs=[];rows=[];started=time.monotonic()
    for n,dt in ((65,.00025),(129,.00025),(257,.00025),(257,.000125)):
        result=evolve(.02,.3,points=n,tend=.02,dt=dt,outer=3.)
        last=result['snapshots'][-1]
        row=dict(points=n,dt=dt,seconds=result['seconds'],
                 constraints=[last['max_hamiltonian_constraint'],last['max_momentum_constraint'],last['max_clock_constraint']],
                 lapse_residual=last['max_lapse_fd_residual'],mass_error=last['mass_balance_relative_error'])
        rows.append(row);runs.append(result)
        if state_cache is not None:
            data={}
            for i,finished in enumerate(runs):
                data['state_'+str(i)]=finished['state'];data['r_'+str(i)]=finished['r']
            np.savez_compressed(state_cache,**data)
        print(json.dumps(dict(kind='run',**row)),flush=True)
    spatial=[]
    for a,b in zip(runs[:2],runs[1:3]):
        mask=a['r']<2.8
        spatial.append(np.max(abs(a['state'][:,mask]-b['state'][:,::2][:,mask]),axis=1).tolist())
    mask=runs[2]['r']<2.8
    temporal=np.max(abs(runs[2]['state'][:,mask]-runs[3]['state'][:,mask]),axis=1).tolist()
    tangent=[]
    for run in runs[1:3]:
        n=len(run['r']);system=Evolution(.02,.3,n,3.,.021,1e-6)
        state=project_state(.02,run['state'],system.r,system.model)
        rhs,_=system.rhs(.02,state)
        for step in (1e-4,5e-5,2.5e-5):
            plus=project_state(.02+step,state+step*rhs,system.r,system.model)
            minus=project_state(.02-step,state-step*rhs,system.r,system.model)
            error=(plus-minus)/(2*step)-rhs
            mask=system.r<2.8
            tangent.append(dict(points=n,step=step,
                                A=float(max(abs(error[0,mask]))),h=float(max(abs(error[3,mask]))),
                                k=float(max(abs(error[2,mask])))))
    checks=dict(unchanged_129_257_constraint_gate=bool(np.all(np.array(rows[2]['constraints'][:2])<.6*np.array(rows[1]['constraints'][:2]))),
                time_error_below_spatial_error=bool(np.all(np.array(temporal)<.2*np.array(spatial[1])+1e-10)),
                baryon_mass_balance=bool(max(abs(r['mass_error']) for r in rows)<1e-9))
    result=dict(rows=rows,spatial_state_errors=spatial,temporal_state_errors=temporal,
                centered_projection_tangency=tangent,checks=checks,seconds=time.monotonic()-started,
                state_order=['A','R/r','Kr','Ko','Q','chi_r','theta_r','D','shell_positions'],
                scope='t=.02, finite outer radius; no late-time physical or global convergence certificate')
    print(json.dumps(dict(kind='summary',**result)),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--state-cache',type=Path);args=parser.parse_args()
    answer=run(args.state_cache);sys.exit(0 if all(answer['checks'].values()) else 1)
