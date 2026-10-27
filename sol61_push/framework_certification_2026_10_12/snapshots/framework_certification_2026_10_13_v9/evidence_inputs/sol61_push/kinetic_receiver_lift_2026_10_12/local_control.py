"""Supplemental exact control closing a reviewer-identified omission test gap."""
from pathlib import Path
import json
import sympy as s

D,g,p,Pi,J,source=s.symbols('D g p Pi J scalar_source', real=True)
energy=Pi*source+D*J
momentum=g*source-p*J
full=s.expand(g*energy-Pi*momentum)
truncated=D*g*J
fixture={D:0,g:1,p:1,Pi:1,J:1}
assert s.simplify(full-(D*g+p*Pi)*J)==0
assert truncated.subs(fixture)==0 and full.subs(fixture)==1
result={'single_scalar_compatibility_recoil_omission_detected':True,
        'fixture':{'D':0,'g':1,'p':1,'Pi':1,'J':1},
        'truncated_residual':0,'full_residual':1,
        'scope':'Supplemental exact control only; no new PDE trajectory.'}
out=Path(__file__).resolve().parent/'local_control_run/results.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
