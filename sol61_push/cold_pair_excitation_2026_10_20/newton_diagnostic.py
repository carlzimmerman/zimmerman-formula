"""Trace unchanged15-step discrete Newton on a preserved failed input."""
from pathlib import Path
import inspect,json,sys,resource
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'sol61_push/cold_fragment_modes_2026_10_20'))
import radial_tools as rt

source=inspect.getsource(rt.background)
old="history.append({'iteration':it,'field_residual_scaled':float(field_res),'charge_residual_relative':float(F[-1])})"
new="history.append({'iteration':it,'field_residual_scaled':float(field_res),'charge_residual_relative':float(F[-1]),'omega':float(xx[-1]),'full_residual_norm':float(np.linalg.norm(F))})"
assert source.count(old)==1
source=source.replace(old,new)
old='dx=spsolve(J,-F);base=np.linalg.norm(F)'
new="dx=spsolve(J,-F);base=np.linalg.norm(F);history[-1].update(newton_omega_step=float(dx[-1]),newton_step_norm=float(np.linalg.norm(dx)))"
assert source.count(old)==1
source=source.replace(old,new)
assert source.count('xx=trial;break')==1
source=source.replace('xx=trial;break',"history[-1]['accepted_line_step']=float(step);xx=trial;break")
for failure in ['discrete stationary line search failed','discrete stationary Newton limit']:
    old="raise RuntimeError('"+failure+"')"
    assert source.count(old)==1
    source=source.replace(old,"raise RuntimeError(json.dumps({'failure':'"+failure+"','history':history}))")
env=dict(rt.__dict__);exec(source,env)
seed,out=map(Path,sys.argv[1:3])
try:
    result=env['background'](seed,136000,60.,1199)
    record={'stationary_converged':True,'record':result[-1]}
except RuntimeError as error:
    record={'stationary_converged':False,**json.loads(str(error))}
record.update(scope='Diagnostic only: original15-step cap, source equations/tolerances/line-search unchanged; expected stationary failure is not a passed reference.',peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(out/'results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
