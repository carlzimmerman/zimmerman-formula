"""One further declared refinement; prior failed evidence remains immutable."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
source=(p/'spherical_long.py').read_text().split('rows=[run(')[0]
env={'__file__':str(p/'spherical_long.py')};exec(compile(source,str(p/'spherical_long.py'),'exec'),env)
r=env['run'](512,8192,.01)
r['formation']=all(s['force_rms_fractional_error']<=.1 and s['min_force']>=0 for s in r['samples'] if s['time']>=560)
old=json.loads((p/'spherical_long_run/results.json').read_text())['rows'][1]
np=env['np'];target=np.array(old['target'])
diff=np.linalg.norm(np.interp(old['r'],r['r'],r['force'])-np.array(old['force']))/np.linalg.norm(target)
env['check']('further refinement force',diff,.03)
out=dict(row=r,checks=env['checks'],all_checks_pass=all(c['passed'] for c in env['checks']))
(p/'spherical_fine_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=out['checks'],formation=r['formation'],late=[s for s in r['samples'] if s['time']>=560]),indent=2))
assert out['all_checks_pass']
