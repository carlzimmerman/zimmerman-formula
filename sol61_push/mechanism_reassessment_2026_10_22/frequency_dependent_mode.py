import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eig
p=Path(__file__).parent;pv=json.load(open(p/'pv_h32_probe.json'));S=np.load(p/'actionh32_64.npz')['S'];names=['resonant_h32_low.json','resonant_h32_probe.json','resonant_h32_high.json'];ws=np.array([.822,.8228,.8236]);out=[]
for k in [8,12,16]:
 vals=[];gaps=[]
 for w,name in zip(ws,names):
  P=np.array(next(r for r in pv['rows'] if r['quadrature']==32 and r['omega']==w)['matrix'])[:k,:k];B=np.array(json.load(open(p/name))['rows'][0]['matrix'])[:k,:k];v,_=eig(S[:k,:k]-P+1j*B,S[:k,:k]);ix=np.argsort(abs(v));vals.append(v[ix[0]]);gaps.append(float(abs(v[ix[1]])))
 vals=np.array(vals);derivative=(vals[2]-vals[0])/.0016;linear=.8228-vals[1]/derivative;poly=np.polyfit(ws-.8228,vals,2);roots=np.roots(poly);quadratic=.8228+roots[np.argmin(abs(roots))]
 out.append(dict(basis=k,boundary_eigenvalues=[[float(x.real),float(x.imag)] for x in vals],complex_slope=[float(derivative.real),float(derivative.imag)],linear_estimate=[float(linear.real),float(linear.imag)],quadratic_estimate=[float(quadratic.real),float(quadratic.imag)],relative_imaginary_change=float(abs(linear.imag/quadratic.imag-1)),minimum_other_eigenvalue_magnitude=min(gaps),conditional_periods_per_efold=float(quadratic.real/(2*np.pi*(-quadratic.imag)))))
result=dict(rows=out,scope='local Taylor continuation of boundary-response eigenvalue; conditional weak-damping estimate, not direct continued-dispersion root')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
