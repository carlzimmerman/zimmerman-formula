#!/usr/bin/env python3
"""Evaluate the proved residual coefficients, not a BVP solution/error bound."""
import csv
import json
import math
from pathlib import Path
import sys

out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
G=6.674e-11; Msun=1.98892e30; pc=3.0856775814913673e16
rows=[]
for footing,a0 in [('canonical',9.3603e-11),('alternative',1.1312e-10)]:
    rM=math.sqrt(G*1e10*Msun/a0)
    for n,c in [(1,17/27),(2,5/(6*math.sqrt(3)))]:
        for L in [5.75,24.,1000.]:
            eps=c*(L*pc/rM)**2
            rows.append(dict(footing=footing,n=n,Lstar_pc=L,rM_kpc=rM/pc/1000,
                             trial_force_residual=eps,trial_force_residual_percent=100*eps))
assert len(rows)==12
for start in [0,3,6,9]:
    a,b,c=rows[start:start+3]
    assert math.isclose(b['trial_force_residual']/a['trial_force_residual'],(24/5.75)**2,rel_tol=1e-14)
    assert math.isclose(c['trial_force_residual']/b['trial_force_residual'],(1000/24)**2,rel_tol=1e-14)
result={'status':'completed','assertion_tested':'12 arithmetic evaluations of analytic trial-profile force residual at x=sqrt(2), with 8 quadratic-scaling checks. Not a numerical solution or solution-error bound.','rows':rows}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
with (out/'residuals.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(result,indent=2))
