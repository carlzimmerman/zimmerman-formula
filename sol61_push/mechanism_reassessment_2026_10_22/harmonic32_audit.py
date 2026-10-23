import json,sys,subprocess
from pathlib import Path
import numpy as np
p=Path(__file__).parent;result=Path(sys.argv[1]);target=result.parent/'frequency_mode.json'
subprocess.run([sys.executable,str(p/'frequency_dependent_mode.py'),str(target)],check=True,stdout=subprocess.DEVNULL)
a=np.load(p/'actionh32_64.npz');b=np.load(p/'action16_64.npz');checks={'action':json.load(open(p/'actionh32_64.json'))['all_pass'],'nested_coefficients':bool(np.max(abs(a['coeff'][:,:16,:]-b['coeff']))<1e-12),'principal_value':json.load(open(p/'pv_h32_probe.json'))['all_pass']}
for name in ['resonant_h32_low.json','resonant_h32_probe.json','resonant_h32_high.json']:
 d=json.load(open(p/name));checks[name]=d['all_pass'];checks[name+'_no_new_roots']=all(sum(r['roots_per_harmonic'][16:])==0 for r in d['rows'])
f=json.load(open(target));out=dict(checks=checks,all_pass=all(checks.values()),frequency_diagnostic=f,moment_error=json.load(open(p/'actionh32_64.json'))['matrix_sum_rule_error'],scope='audit of direct harmonic refinement and recomputed local Taylor diagnostic; no direct continued root or formation claim')
result.write_text(json.dumps(out,indent=2));print(json.dumps({'checks':checks,'frequency_diagnostic':f},indent=2));sys.exit(0 if out['all_pass'] else 1)
