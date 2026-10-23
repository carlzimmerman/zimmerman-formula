"""Independent adaptive integration of the new linear quantum mode evolution."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import hankel1,h1vp
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
s=json.loads((P/'coupled_fragmentation_96_run/results.json').read_text())['source'];w=s['omega_over_H'];A=s['conformal_scale_over_H'];lam=.00881292;phi=s['background_over_H'][0]
raw=np.fromfile(P/'coupled_fragmentation_96_run/fine96_initial.bin',dtype='<f8');n=int(raw[0]);raw=raw[9:].reshape(2,4,n,n,n);q0=float(raw[0,0].mean());v0=float(raw[1,0].mean())
base=np.load(P/'linear_quantum_correlations_run/base32_final.npz');k=base['k'];ids=np.unique(np.linspace(0,len(k)-1,31).astype(int));k=k[ids];nu=np.sqrt(2.25-np.array([3,1])*lam*phi**2);kh=k*w;pref=w**1.5/A
u0=np.array([pref*np.sqrt(np.pi)/2*hankel1(x,kh) for x in nu]);vinit=np.array([-pref*np.sqrt(np.pi)/(2*w)*(.5*hankel1(x,kh)+kh*h1vp(x,kh)) for x in nu]);cnt=u0.size
y0=np.concatenate(([q0,v0],u0.ravel(),vinit.ravel())).astype(complex)
def rhs(t,y):
 q,v=y[:2];u=y[2:2+cnt].reshape(2,-1);uv=y[2+cnt:].reshape(2,-1);acc=-(k[None,:]**2+np.array([3,1])[:,None]*q*q)*u
 return np.concatenate(([v,-q**3],uv.ravel(),acc.ravel()))
sol=solve_ivp(rhs,(0,float(base['z'])),y0,method='DOP853',rtol=1e-12,atol=1e-14)
assert sol.success
U=sol.y[2:2+cnt,-1].reshape(2,-1);V=sol.y[2+cnt:,-1].reshape(2,-1)
errs={}
for name in ['base32','time32']:
 d=np.load(P/'linear_quantum_correlations_run'/(name+'_final.npz'));du=d['U'][:,ids]-U;dv=d['V'][:,ids]-V
 errs[name]=dict(mode_error=float(np.linalg.norm(np.concatenate([du.ravel(),dv.ravel()]))/np.linalg.norm(np.concatenate([U.ravel(),V.ravel()]))),mean_error=float(abs(d['q']-sol.y[0,-1])))
checks=dict(adaptive_solve=sol.success,mode_error_reduces_quadratically=3.5<errs['base32']['mode_error']/errs['time32']['mode_error']<4.5,mean_error_reduces_quadratically=3.5<errs['base32']['mean_error']/errs['time32']['mean_error']<4.5,fine_mode_error=errs['time32']['mode_error']<.002)
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),errors=errs,modes_tested=len(ids),scope='Independent DOP853 check of the declared linear equations only; not validation of missing nonlinear quantum evolution.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
