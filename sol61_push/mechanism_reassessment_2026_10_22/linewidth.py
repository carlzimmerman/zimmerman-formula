import sys,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar,brentq
p=Path(__file__).parent;orders=[int(x) for x in sys.argv[2:]] or [64,128];rows=[]
for order in orders:
 data=np.load(p/f'action_{order}.npz');S=data['S'];freq=data['omega'][:,None]*np.arange(1,17);a=(2*data['derivative_weights'][:,None]*freq**2).ravel();b=(freq**2).ravel();V=data['coeff'].reshape(-1,8)*np.sqrt(a[:,None])
 for eps in [.003,.001,.0003,.0001]:
  def absorb(w):
   Pi=V.T@(V/(((w+1j*eps)**2-b)[:,None]));chi=(S@np.linalg.solve(S-Pi,S)-S)[0,0];return float(-chi.imag)
  opt=minimize_scalar(lambda w:-absorb(w),bounds=(.818,.828),method='bounded',options={'xatol':1e-10});w=opt.x;height=-opt.fun
  left=brentq(lambda x:absorb(x)-height/2,.79,w,xtol=1e-10);right=brentq(lambda x:absorb(x)-height/2,w,.85,xtol=1e-10);hwhm=(right-left)/2
  rows.append(dict(order=order,epsilon=eps,peak=float(w),height=float(height),hwhm=float(hwhm),excess_over_epsilon=float(hwhm-eps),asymmetry=float((right-w)-(w-left)),optimizer_success=bool(opt.success)))
checks=dict(optimizers=all(r['optimizer_success'] for r in rows),positive=all(r['height']>0 and r['hwhm']>0 for r in rows))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='finite-broadening width diagnostic; excess width is not a claimed damping rate')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
