import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eig
p=Path(__file__).parent;pv=json.load(open(sys.argv[2] if len(sys.argv)>2 else p/'pv_probe.json'));br=json.load(open(p/'resonant_h32_probe.json'));rows=[]
for order in [64]:
 S=np.load(p/f'actionh32_{order}.npz')['S'];B=np.array(next(r for r in br['rows'] if r['order']==order)['matrix'])
 for k in [8,12,16]:
  points=[]
  for w in [.822,.8228,.8236]:
   P=np.array(next(r for r in pv['rows'] if r['order']==order and r['quadrature']==32 and r['omega']==w)['matrix']);vals,vec=eig(S[:k,:k]-P[:k,:k]+1j*B[:k,:k],S[:k,:k]);i=np.argmin(abs(vals));x=vec[:,i];x/=np.sqrt(np.vdot(x,S[:k,:k]@x).real)
   points.append(dict(omega=w,real=float(vals[i].real),imag=float(vals[i].imag),projected_absorption=float(np.vdot(x,B[:k,:k]@x).real)))
  slope=(points[-1]['real']-points[0]['real'])/.0016;root=.8228-points[1]['real']/slope;indicator=points[1]['imag']/slope
  rows.append(dict(order=order,basis=k,points=points,linearized_crossing=root,real_slope=slope,decay_indicator=indicator,scope='B held fixed at .8228; real-axis linearized indicator, not a solved continued pole'))
out=dict(rows=rows,scope='basis-sensitive diagnostic only; no physical lifetime claim')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
