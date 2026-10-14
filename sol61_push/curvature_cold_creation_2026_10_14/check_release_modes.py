"""Finite scalar-only release-mode checks on the same assigned FRW background."""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def bg(t):
 u=t-30.;lc=lambda v:np.logaddexp(v,-v)-np.log(2.)
 H=1/(1+t+lc(u)-lc(-30.));eps=1+np.tanh(u)
 return H,-eps*H*H,24*H**4*(1-eps)
def bgeq(t,y):
 p,v,N=y;H,Hp,G=bg(t)
 return [v,-3*H*v-(.01-.1*G)*p-p**3,H]
background=solve_ivp(bgeq,[0,5000],[1e-6,0,0],method='DOP853',rtol=2e-11,atol=1e-14,max_step=5,dense_output=True)
ck('background integration',background.success)
NT=background.sol(30)[2];HT=bg(30)[0]
rows=[]
for k in [0.,.01,.1,1.,10.]:
 def fun(t,y):
  H,Hp,G=bg(t);p,v,N=background.sol(t);kp=k*np.exp(NT-N)
  freq=.01+3*p*p-.1*G+kp*kp
  shifted=freq-2.25*H*H-1.5*Hp
  return [y[1],-3*H*y[1]-freq*y[0],y[3],-3*H*y[3]-freq*y[2],y[5],-shifted*y[4],y[7],-shifted*y[6]]
 init=[1e-6,0,0,1e-7,1e-6,1.5*HT*1e-6,0,1e-7]
 sol=solve_ivp(fun,[30,5000],init,method='DOP853',rtol=2e-10,atol=1e-16,max_step=3,dense_output=True)
 ck('mode integration k='+str(k),sol.success)
 N=background.sol(5000)[2];scale=np.exp(-1.5*(N-NT));y=sol.y[:,-1];H=bg(5000)[0]
 for n in [0,2]:
  chi=n+4;converted=np.array([scale*y[chi],scale*(y[chi+1]-1.5*H*y[chi])])
  error=np.linalg.norm((converted-y[n:n+2])*[1,10])/max(np.linalg.norm(y[n:n+2]*[1,10]),1e-30)
  ck('independent friction transformation k='+str((k,n)),error<2e-6)
 # Check transfer-map determinant from the Wronskian, independent of any growth interpretation.
 initial_det=1e-13;det=y[0]*y[3]-y[1]*y[2];expected=initial_det*np.exp(-3*(N-NT))
 ck('Wronskian expansion ledger k='+str(k),abs(det/expected-1)<3e-6)
 kp=k*np.exp(NT-N);freew=kp*kp/(3*(.01+kp*kp))
 final_rho=.5*background.y[1,-1]**2+.005*background.y[0,-1]**2+.25*background.y[0,-1]**4
 er=[.5*(y[n+1]**2+(.01+kp*kp)*y[n]**2)/final_rho for n in [0,2]]
 rows.append({'k_physical_at_transition_over_H_initial':k,'k_final_over_m':float(kp/.1),'late_free_isotropic_mode_w':float(freew),'final_scalar_mode_energy_proxy_over_background':er,'max_abs_delta_basis_1':float(max(abs(sol.y[0]))),'max_abs_delta_basis_2':float(max(abs(sol.y[2]))),'Wronskian_relative_error':float(abs(det/expected-1))})
ck('high momentum modes need not be cold',rows[-1]['late_free_isotropic_mode_w']>.1)
ck('long wavelength mode can remain cold',rows[1]['late_free_isotropic_mode_w']<1e-6)
ts=np.unique(np.concatenate([np.linspace(0,70,1401),np.linspace(70,5000,9861)]));p,v,N=background.sol(ts)
rho=.5*v*v+.005*p*p+.25*p**4
history={'time':ts.tolist(),'phi':p.tolist(),'N_relative_transition':(N-NT).tolist(),'canonical_rho':rho.tolist(),'GB':[float(bg(t)[2]) for t in ts]}
(out/'history.json').write_text(json.dumps(history)+'\n')
result={'passed':len(checks),'checks':checks,'rows':rows,'scope':'fixed FRW scalar perturbations, k specified at t=30, two supplied classical bases; not inflationary quantum spectrum, full metric stability, or a proof for all k','interpretation':'cold homogeneous energy does not establish an entirely cold inhomogeneous distribution; short wavelengths retain pressure'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
