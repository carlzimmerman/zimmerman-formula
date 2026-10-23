import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
p=Path(__file__).parent
# Reuse only the already-audited continuum background and trial-potential construction.
source=(p/'kinetic_weight.py').read_text().split(' grid=np.linspace')[0]
namespace={'__file__':str(p/'kinetic_weight.py'),'__name__':'background_only'}
exec(source,namespace)
r=namespace['rr'];rho=namespace['rho'];drho=namespace['drho'];phi=namespace['potential'];norm=namespace['potential_norm'];q=namespace['q']
dr=-(3*rho+r*drho)/norm
S=float(np.trapz(r*r*dr*phi,r))
s=r**3*rho/norm
S2=float(np.trapz(q*(2-q)/(1-q)**2*s*s/r**2+.01*r*r*dr*dr,r))
rows=[];curves={};time=np.linspace(0,120,1201)
for N in [1024,4096]:
 data=json.load(open(p/f'kinetic_weight_{N}.json'));row=data['rows'][0];o=np.array(row['omega_samples']);Q=np.array(row['Q_samples']);C=np.array(row['couplings']);freq=o[:,None]*np.arange(1,17)
 a=(row['mass']/N*2*freq**2*C*C/Q[:,None]).ravel();b=(freq**2).ravel();keep=a>0;a=a[keep];b=b[keep]
 for bins in [512,1024]:
  # Uniform frequency bins; preserve total strength and its b-weighted moment.
  index=np.minimum((np.sqrt(b)/np.sqrt(b.max())*bins).astype(int),bins-1)
  aa=np.bincount(index,weights=a,minlength=bins);bb=np.bincount(index,weights=a*b,minlength=bins);mask=aa>0;bb=bb[mask]/aa[mask];aa=aa[mask]
  v=np.sqrt(aa);matrix=np.diag(bb)+np.outer(v,v)/S
  lam,U=eigh(matrix,driver='evr');weights=(U.T@v)**2/a.sum();response=weights@np.cos(np.sqrt(lam)[:,None]*time)
  checks=[]
  for z in [.4+.03j,.828+.01j,1.3+.03j]:
   pi=np.sum(aa/(z*z-bb));resolvent=np.sum((U.T@v)**2/(z*z-lam));expected=pi/(1-pi/S);checks.append(abs(resolvent-expected)/max(abs(expected),1e-12))
  imax=np.argmax(weights);windows={}
  for lo,hi in [(0,10),(30,40),(110,120)]:
   y=response[(time>=lo)&(time<=hi)];windows[f'{lo}-{hi}']=float(np.sqrt(np.mean(y*y)))
  rows.append(dict(samples=N,bins=bins,occupied_bins=len(aa),S=S,min_eigenvalue=float(lam.min()),largest_weight=float(weights[imax]),largest_weight_frequency=float(np.sqrt(lam[imax])),weight_sum=float(weights.sum()),resolvent_error=max(checks),strength_error=float(abs(aa.sum()/a.sum()-1)),windows=windows))
  curves[f'{N}_{bins}']=response.tolist()
checks=dict(positive_stiffness=S>0,stiffness_identity=abs(S/S2-1)<1e-6,positive_spectra=all(x['min_eigenvalue']>0 for x in rows),spectral_identity=all(x['resolvent_error']<1e-7 for x in rows),weights=all(abs(x['weight_sum']-1)<1e-8 for x in rows))
comparison={}
for N in [1024,4096]:
 d=np.array(curves[f'{N}_512'])-curves[f'{N}_1024'];comparison[str(N)]=dict(max=float(max(abs(d))),rms=float(np.sqrt(np.mean(d*d))))
out=dict(checks=checks,all_pass=all(checks.values()),stiffness=S,stiffness_second_variation=S2,rows=rows,bin_comparison=comparison,times=time.tolist(),curves=curves,scope='one-shape finite sampled feedback; normalized collective-vector autocorrelation, not actual initial dilation evolution or damping rate')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['times','curves']},indent=2));sys.exit(0 if out['all_pass'] else 1)
