import json,sys
from pathlib import Path
import numpy as np
from scipy.signal import find_peaks
p=Path(__file__).parent;grid=np.linspace(.4,1.7,261);out=[];curves={}
for N in [1024,4096]:
 d=np.load(p/f'multishape_{N}.npz');S=d['S'];freq=d['omega'][:,None]*np.arange(1,17);C=d['coeff'].reshape(-1,8);a=(2*float(d['mass'])/N*freq**2/d['Q'][:,None]).ravel();b=(freq**2).ravel();V=C*np.sqrt(a[:,None])
 for width in [.03,.01]:
  values={k:[] for k in [1,2,4,8]}
  for w in grid:
   Pi=V.T@(V/(((w+1j*width)**2-b)[:,None]))
   for k in values:
    sk=S[:k,:k];pk=Pi[:k,:k];chi=(sk@np.linalg.solve(sk-pk,sk)-sk)[0,0];values[k].append(float(-chi.imag))
  for k,arr in values.items():
   arr=np.array(arr);peaks,_=find_peaks(arr,prominence=max(arr)*.03);rank=sorted(peaks,key=lambda i:arr[i],reverse=True)[:5]
   out.append(dict(samples=N,width=width,basis=k,maximum_frequency=float(grid[np.argmax(arr)]),maximum_absorptive=float(max(arr)),peaks=[dict(omega=float(grid[i]),height=float(arr[i])) for i in rank],minimum_absorptive=float(min(arr))))
   curves[f'{N}_{width}_{k}']=arr.tolist()
checks=dict(orbit_inputs=all(json.load(open(p/f'multishape_{N}.json'))['all_pass'] for N in [1024,4096]),passivity=all(r['minimum_absorptive']>=-1e-9 for r in out),finite=all(np.isfinite(r['maximum_absorptive']) for r in out))
result=dict(checks=checks,all_pass=all(checks.values()),rows=out,grid=grid.tolist(),curves=curves,scope='finite-broadening multi-shape response to external dilation potential; no continuum pole or fitted decay rate')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['grid','curves']},indent=2));import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(2,1,figsize=(8,6),sharex=True,layout='constrained')
for k in [1,2,4,8]:axes[0].plot(grid,curves[f'4096_0.01_{k}'],label=f'{k} field shapes')
for N in [1024,4096]:
 for width in [.03,.01]:axes[1].plot(grid,curves[f'{N}_{width}_8'],label=f'{N} orbits, epsilon={width}')
for ax in axes:
 ax.axvline(.827760,color='gray',ls=':',label='Cold-fluid fundamental');ax.set_ylabel('Absorptive response');ax.legend(fontsize=7);ax.set_xlim(.6,1.65)
axes[1].set_xlabel('Dimensionless angular frequency');fig.suptitle('Kinetic field feedback: finite numerical broadening
Peak widths are not physical damping rates',fontsize=11)
fig.savefig(p/'multishape_response.png',dpi=160)
sys.exit(0 if result['all_pass'] else 1)
