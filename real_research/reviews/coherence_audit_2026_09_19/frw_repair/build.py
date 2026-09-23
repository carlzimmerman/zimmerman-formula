from pathlib import Path
import time,json,sympy as sp
from action_build import build_frw_perturbation_odes_shift
start=time.time()
print('Building corrected flat-FRW quadratic equations from the action.',flush=True)
ODE,S=build_frw_perturbation_odes_shift()
p=Path(__file__).resolve().parent/'run_build'/'equations.json'
p.write_text(json.dumps({'ODE':[sp.srepr(o) for o in ODE], 'S':{key:([sp.srepr(x) for x in val] if key=='amps' else sp.srepr(val)) for key,val in S.items()}},indent=1))
print('Built',len(ODE),'equations in',time.time()-start,'seconds',flush=True)
for i,e in enumerate(ODE): print('row',i,'ops',sp.count_ops(e),flush=True)
