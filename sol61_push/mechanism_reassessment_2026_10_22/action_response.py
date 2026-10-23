import json,sys
from pathlib import Path
import numpy as np
from scipy.signal import find_peaks
p=Path(__file__).parent;grid=np.linspace(.75,.88,131);out=[];curves={}
for N in [32,64]:
 d=np.load(p/f'action_{N}.npz');S=d['S'];freq=d['omega'][:,None]*np.arange(1,17);C=d['coeff'].reshape(-1,8);a=(2*d['derivative_weights'][:,None]*freq**2).ravel();b=(freq**2).ravel();V=C*np.sqrt(a[:,None])
 for width in [.03,.01,.003]:
  values={k:[] for k in [4,8]}
  for w in grid:
   Pi=V.T@(V/(((w+1j*width)**2-b)[:,None]))
   for k in values:
    sk=S[:k,:k];pk=Pi[:k,:k];chi=(sk@np.linalg.solve(sk-pk,sk)-sk)[0,0];values[k].append(float(-chi.imag))
  for k,arr in values.items():
   arr=np.array(arr);peaks,_=find_peaks(arr,prominence=max(arr)*.03);rank=sorted(peaks,key=lambda i:arr[i],reverse=True)[:5]
   out.append(dict(quadrature_order=N,orbit_count=N*N,width=width,basis=k,maximum_frequency=float(grid[np.argmax(arr)]),maximum_absorptive=float(max(arr)),peaks=[dict(omega=float(grid[i]),height=float(arr[i])) for i in rank],minimum_absorptive=float(min(arr))))
   curves[f'{N}_{width}_{k}']=arr.tolist()
checks=dict(orbit_inputs=all(json.load(open(p/f'action_{N}.json'))['all_pass'] for N in [32,64]),passivity=all(r['minimum_absorptive']>=-1e-9 for r in out),finite=all(np.isfinite(r['maximum_absorptive']) for r in out))
result=dict(checks=checks,all_pass=all(checks.values()),rows=out,grid=grid.tolist(),curves=curves,scope='action-quadrature low-mode response; no continuum pole or fitted decay rate')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['grid','curves']},indent=2));sys.exit(0 if result["all_pass"] else 1)
