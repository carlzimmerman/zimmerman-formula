#!/usr/bin/env python3
"""Recompute a completed initial MW batch without checkpoint reuse."""
import json,os
from pathlib import Path
import engines as E
here=Path(__file__).resolve().parent
source=here/'main/mw/canonical_p056_r1.json'
saved=json.loads(source.read_text())
if not saved['complete']:raise RuntimeError('Wait for the completed resumed point')
K=E.mw();g,mu=K.make_grid(K.C.A0['canonical']);solver=K.Solver(g,mu,K.C.A0['canonical'])
ids=sorted(range(len(saved['grid_cells'])),key=lambda i:saved['width'][i])[:16]
checks=[]
for i in ids:
    fresh=solver.solve(saved['grid_cells'][i],saved['width'][i],lmax=2*(g.Nt-1))['corrected']
    old=saved['cells'][str(i)]
    err=max(abs(fresh[k]-old[k])/max(1,abs(old[k])) for k in ['vc','K0','cK','cO','h','D'])
    checks.append(dict(cell=i,relative_error=err,passed=err<=1e-10 and fresh['all_four']==old['all_four']))
obj=dict(scope='Initial16-cell uninterrupted fixture versus resumed full-point checkpoint',checks=checks,
         max_relative=max(c['relative_error'] for c in checks),passed=all(c['passed'] for c in checks))
path=here/'main/resume_check.json';tmp=path.with_suffix('.json.tmp')
with tmp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
os.replace(tmp,path);print(json.dumps(obj,indent=2));raise SystemExit(not obj['passed'])
