#!/usr/bin/env python3
"""Clock-specific endpoint eigenvalue sensitivity, separate from whole basis."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eig
from initial_data import FrozenBackground
from transfer_evolve import mode_system

parser=argparse.ArgumentParser()
parser.add_argument('--source',required=True,type=Path)
parser.add_argument('--result-file',required=True,type=Path)
args=parser.parse_args()
bg=FrozenBackground()
archive=json.loads(args.source.read_text())
rows=[]
for branch in archive['continuations']:
    p=branch['samples'][-1]
    v=bg.evaluate([p[x] for x in ('a','H','q','tau','baryon','radiation')],extended=True)[0]
    modes=[]
    for k in (3e6,3e7):
        operator,*_=mode_system(v,k)
        f=k/v['a']
        scales=np.array([1.,f,1.,f,1.,max(v['rho'],1.)*f])
        balanced=operator*scales[None,:]/scales[:,None]/f
        values,left,right=eig(balanced,left=True,right=True)
        speeds=-values**2
        clock=sorted(range(6),key=lambda i:abs(speeds[i]-p['clock_cs2']))[:2]
        data=[]
        for i in range(6):
            condition=np.linalg.norm(left[:,i])*np.linalg.norm(right[:,i])/abs(np.vdot(left[:,i],right[:,i]))
            data.append(dict(index=i,eigenvalue_real=float(values[i].real),eigenvalue_imag=float(values[i].imag),
                             cs2_real=float(speeds[i].real),eigenvalue_condition=float(condition),clock_pair=i in clock))
        modes.append(dict(k=k,whole_basis_condition=float(np.linalg.cond(right)),spectrum=data,
                          max_clock_eigenvalue_condition=max(data[i]['eigenvalue_condition'] for i in clock)))
    rows.append(dict(initial=branch['initial'],direction=branch['direction'],loga=p['loga'],modes=modes))
result=dict(rows=rows,convention='Per-eigenvalue kappa=norm(left)*norm(right)/abs(left.H right) for the same similarity-balanced numerical operator. This is coordinate dependent first-order sensitivity, not a rigorous backward/forward error certificate.',
            non_claim='Large whole-basis condition alone does not demonstrate large clock-specific eigenvalue sensitivity; no UV control follows from either condition.')
args.result_file.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([dict(direction=r['direction'],baryon=r['initial']['baryon'],q=r['initial']['q'],
                       max_clock_condition_at_kmax=r['modes'][-1]['max_clock_eigenvalue_condition']) for r in rows],indent=2))
