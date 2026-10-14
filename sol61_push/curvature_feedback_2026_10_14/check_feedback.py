import json,sys,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import simpson
from scipy.optimize import brentq
from background import evolve,detail,MI,GAMMA
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def eq(n,v):ck(n,s.simplify(v)==0)
# Exact signed exchange: the source reheating and scalar damping are internal transfers.
H,fp,fpp,v,w,r,acc,hd,up,gam,gamd=s.symbols('H Fprime Fsecond phi_dot chi_dot radiation phi_ddot H_dot Uprime Gamma_chi Gamma_phi')
scalar_acc=-(3*H+gamd)*v-up+24*fp*H**2*(H**2+hd)
source_dot=-3*H*w*w-4*H*r+gamd*v*v
canonical_phi_dot=v*scalar_acc+up*v
eq('reciprocal total component exchange',canonical_phi_dot+source_dot-(-3*H*(v*v+w*w)-4*H*r+24*fp*v*H**2*(H**2+hd)))
A=24*fp*H**2;B=24*H**3*fp-v;C=6*H+72*H**2*fp*v
b=-(3*H+gamd)*v-up+24*fp*H**4;d=up*v+source_dot-24*H**3*fpp*v*v
hh=(d-B*b)/(C+B*A);aa=b+A*hh
eq('scalar equation reduction',aa-24*fp*H**2*hh-b)
eq('differentiated Friedmann reduction',B*aa+C*hh-d)
eq('denominator and tensor kinetic relation',(C+B*A)/(6*H)-(1+8*H*fp*v+96*fp*fp*H**4))
# Cold diagnostics on aligned complete cycles, with GB energy separately screened.
def cold(sol,lam):
 ts=np.linspace(sol.t[-1]-1000,sol.t[-1],8001);pp=sol.sol(ts)[0]
 crossings=[]
 for i in range(len(ts)-1):
  if pp[i]<0 and pp[i+1]>=0:crossings.append(brentq(lambda t:sol.sol(t)[0],ts[i],ts[i+1]))
 ck('enough resolved late cycles lambda='+str(lam),len(crossings)>=11)
 z=np.array(crossings[-11:]);t=np.linspace(z[0],z[-1],5001);p,v,c,w,r,h,N=sol.sol(t)
 rho=.5*v*v+.005*p*p+lam*p**4/4;pr=.5*v*v-.005*p*p-lam*p**4/4
 wz=float(simpson(pr,x=t)/simpson(rho,x=t));a=sol.sol(z);com=np.exp(3*(a[6]-a[6,0]))*.5*a[1]**2
 drift=float(np.ptp(com)/np.mean(com))
 ck('late canonical pressure small lambda='+str(lam),abs(wz)<.001)
 ck('late dust redshifting lambda='+str(lam),drift<.001)
 return {'cycle_w':wz,'cycle_comoving_energy_relative_drift':drift,'interval':[float(z[0]),float(z[-1])]}
rows=[];saved=None
for lam in [1.,100.,10000.,.01]:
 sol,row=evolve(lam=lam,end=5000,rtol=2e-10,atol=1e-13)
 ck('feedback integrator lambda='+str(lam),row['success'])
 ck('Friedmann constraint lambda='+str(lam),row['max_Friedmann_relative_residual']<2e-5)
 if lam!=.01:
  ck('reaches end lambda='+str(lam),row['termination']=='end time')
  ck('tensor necessary screen lambda='+str(lam),min(row['min_QT'],row['min_FT'])>.9)
  row.update(cold(sol,lam))
  ck('late GB energy negligible lambda='+str(lam),abs(row['end_GB_fraction'])<1e-8)
 else:ck('strong case stops at explicit amplitude guard',row['termination']=='field amplitude guard100')
 rows.append(row)
sol,refined=evolve(lam=1.,end=5000,rtol=2e-12,atol=1e-15)
ck('refined feedback completes',refined['termination']=='end time')
ck('refined constraint',refined['max_Friedmann_relative_residual']<2e-7)
refined.update(cold(sol,1.))
ck('cold fraction refinement',abs(rows[0]['end_phi_canonical_fraction']/refined['end_phi_canonical_fraction']-1)<1e-4)
ck('expansion refinement',abs(rows[0]['N']-refined['N'])<1e-5)
eta0sol,eta0=evolve(lam=1.,eta=0,end=5000,rtol=2e-12,atol=1e-22)
zerosol,zero=evolve(lam=1.,phi=0,end=5000,rtol=2e-12,atol=1e-15)
ck('eta0 control completes',eta0['termination']=='end time')
ck('zero-seed control completes',zero['termination']=='end time')
ck('zero seed remains zero',zero['end_phi_canonical_fraction']==0 and zero['max_abs_phi']==0)
ck('curvature amplification survives feedback',refined['end_phi_canonical_fraction']>1e6*eta0['end_phi_canonical_fraction'])
ck('eta0 exact tensor GR limit',eta0['min_QT']==eta0['min_FT']==1)
# Durable sampled history of the refined full-feedback trajectory.
ts=np.unique(np.concatenate([np.linspace(0,150,3001),np.linspace(150,5000,9701)]));ys=sol.sol(ts);p,v,c,w,r,h,N=ys
vals=np.array([detail(y,1.,.1) for y in ys.T]);rho=.5*v*v+.005*p*p+p**4/4
history={'time':ts.tolist(),'phi':p.tolist(),'H':h.tolist(),'N':N.tolist(),'canonical_phi_rho':rho.tolist(),'radiation_rho':r.tolist(),'QT':vals[:,2].tolist(),'FT':vals[:,3].tolist()}
(out/'history.json').write_text(json.dumps(history)+'\n')
result={'passed':len(checks),'checks':checks,'rows':rows,'refined':refined,'eta0':eta0,'zero_seed':zero,'interpretation':'Full homogeneous metric/source feedback retains a cold remnant in three assigned quadratic-GB examples. Necessary tensor screen passes; no complete scalar perturbation or observational certificate. Strong case leaves amplitude guard. Reheating rate is phenomenological and seed supplied.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
