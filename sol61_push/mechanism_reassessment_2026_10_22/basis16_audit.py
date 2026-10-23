import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent;checks={};metrics={}
for order in [64,128]:
 a=np.load(p/f'action16_{order}.npz');b=np.load(p/f'action_{order}.npz');checks[f'prefix_{order}']=bool(np.max(abs(a['coeff'][:,:,:8]-b['coeff']))<1e-12 and np.max(abs(a['S'][:8,:8]-b['S']))<1e-12);checks[f'action_{order}']=json.load(open(p/f'action16_{order}.json'))['all_pass'];metrics[str(order)]={'stiffness_condition':float(np.linalg.cond(a['S'])),'moment_errors':{str(k):float(np.linalg.norm((a['measured_moment']-a['moment'])[:k,:k])/np.linalg.norm(a['moment'][:k,:k])) for k in [8,12,16]}}
b=json.load(open(p/'resonant16_probe.json'));pv=json.load(open(p/'pv16_probe.json'));c=json.load(open(p/'complex16_probe.json'));checks['resonance']=b['all_pass'];checks['principal_value']=pv['all_pass'];checks['dissipative_identity']=all(abs(q['imag']-q['projected_absorption'])<1e-9 for r in c['rows'] for q in r['points'])
indicators=[r['decay_indicator'] for r in c['rows'] if r['order']==128];metrics['basis_indicator_relative_span']=(max(indicators)-min(indicators))/np.mean(indicators)
out=dict(checks=checks,all_pass=all(checks.values()),metrics=metrics,diagnostics=c['rows'],scope='audit of direct enlarged-basis calculations; real-axis indicator, not a solved pole or physical lifetime')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(dict(checks=checks,metrics=metrics),indent=2));sys.exit(0 if out['all_pass'] else 1)
