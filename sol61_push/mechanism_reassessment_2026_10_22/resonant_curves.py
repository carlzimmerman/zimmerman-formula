import json,sys
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
from scipy.interpolate import PchipInterpolator
from scipy.linalg import eigh
p=Path(__file__).parent;omega=.8228;F=15*10000/(2**4.5*np.pi)
# Fixed approximate mode direction from finest finite-broadening response, S normalized.
d=np.load(p/'action_128.npz');S=d['S'];freq=d['omega'][:,None]*np.arange(1,17);a=(2*d['derivative_weights'][:,None]*freq**2).ravel();b=(freq**2).ravel();V=d['coeff'].reshape(-1,8)*np.sqrt(a[:,None]);Pi=V.T@(V/(((omega+.003j)**2-b)[:,None]));ev,U=eigh((S-Pi).real,S);mode=U[:,np.argmin(abs(ev))]
rows=[]
for order in [64,128]:
 data=np.load(p/f'action_{order}.npz');meta=json.load(open(p/f'action_{order}.json'));gx,gw=roots_legendre(order);u=(gx+1)*meta['max_L2']/2;uw=gw*meta['max_L2']/2
 Os=data['omega'].reshape(order,order);Qs=data['Q'].reshape(order,order);Cs=data['coeff'].reshape(order,order,16,8)
 matrices=np.zeros((16,8,8));counts=np.zeros(16,dtype=int);derivatives=[];near_ends=0;nonmonotonic=0
 for j in range(order):
  E=-Qs[j]-u[j]/2;O=Os[j];interp=PchipInterpolator(E,O,extrapolate=False);deriv=interp.derivative()
  nonmonotonic+=int(np.any(np.diff(O)>0) and np.any(np.diff(O)<0))
  for n in range(1,17):
   roots=interp.solve(omega/n,extrapolate=False);roots=roots[np.isfinite(roots)&(roots>E[0])&(roots<E[-1])]
   cinterp=PchipInterpolator(E,Cs[j,:,n-1,:],axis=0,extrapolate=False)
   for root in roots:
    slope=abs(float(deriv(root)))
    if slope<1e-9:raise RuntimeError('near tangent resonance needs special treatment')
    C=cinterp(root);matrices[n-1]+=2*np.pi**3*F*uw[j]*np.outer(C,C)/slope;counts[n-1]+=1;derivatives.append(slope)
    near_ends+=int((root-E[0])/(E[-1]-E[0])<.01 or (E[-1]-root)/(E[-1]-E[0])<.01)
 B=matrices.sum(axis=0)
 rows.append(dict(order=order,matrix=B.tolist(),mode_projected_absorption=float(mode@B@mode),dilation_absorption=float(B[0,0]),harmonic_mode_absorption=[float(mode@B@mode) for B in matrices],roots_per_harmonic=counts.tolist(),minimum_abs_energy_derivative=min(derivatives),near_end_roots=near_ends,nonmonotonic_rows=nonmonotonic,min_matrix_eigenvalue=float(min(np.linalg.eigvalsh(B)))))
B0=np.array(rows[0]['matrix']);B1=np.array(rows[1]['matrix']);checks=dict(positive_matrices=all(x['min_matrix_eigenvalue']>-1e-10 for x in rows),finite=all(np.isfinite(x['mode_projected_absorption']) for x in rows))
out=dict(checks=checks,all_pass=all(checks.values()),frequency=omega,mode=mode.tolist(),mode_reference_generalized_eigenvalue=float(ev[np.argmin(abs(ev))]),rows=rows,matrix_relative_change=float(np.linalg.norm(B1-B0)/np.linalg.norm(B1)),mode_relative_change=abs(rows[1]['mode_projected_absorption']/rows[0]['mode_projected_absorption']-1),scope='interpolated roots inside sampled energy range; endpoint slivers omitted, not a certified full continuum damping result')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{k:v for k,v in x.items() if k!='matrix'} for x in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
