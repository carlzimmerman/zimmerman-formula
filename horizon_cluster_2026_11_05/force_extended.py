"""HC011 empirical force-law comparisons, explicit models and validation.
python horizon_cluster_2026_11_05/force_models.py OUTPUT
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares, minimize_scalar
import sympy as sp
B=Path(__file__).resolve().parent;O=Path(sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
a=np.loadtxt(B.parent/'real_research/data/sparc_data/NGC7331_rotmod.dat');a=a[a[:,0]>=a[:,0].max()/2];r,v,ev,vg,vd,vb=a[:,:6].T;x=r/25
G=6.67430e-11;MS=1.98847e30;KPC=3.085677581491367e19;C=299792458.;LAM=1.09e-52
al=C*C*np.sqrt(LAM/(32*np.pi));qmax=1.6e8*14.7/12.23;bnl=np.sqrt(G*MS*qmax*al)/1e6;bh2=G*MS*qmax/(r*KPC)/1e6
checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
ck('17 outer radii',len(r)==17)
def estimate(kind,ud,ub,train):
 free=kind=='power';nuisance=ud is None
 def unpack(p):
  bb=np.exp(p[0]);s=p[1] if free else (-1 if kind=='central' else (1 if kind=='constant_g' else 0))
  d,u=p[-2:] if nuisance else (ud,ub)
  return bb,s,d,u
 def model(p):
  bb,s,d,u=unpack(p);v2=vg*np.abs(vg)+d*vd**2+u*vb**2+bb*x**s
  return np.sqrt(np.maximum(v2,1e-10))
 def fun(p):return ((model(p)-v)/ev)[train]
 starts=[]
 for slope in ([-1,0,1] if free else [0]):
  p=[np.log(2e4)]+([slope] if free else [])+([.5,.7] if nuisance else [])
  low=[-12]+([-3] if free else [])+([.1,.1] if nuisance else [])
  high=[np.log(1e6)]+([3] if free else [])+([1.2,1.4] if nuisance else [])
  z=least_squares(fun,p,bounds=(low,high),xtol=1e-12,ftol=1e-12,gtol=1e-10,max_nfev=4000)
  starts.append(z)
 best=min(starts,key=lambda z:np.sum(z.fun**2));ck('converged '+kind,best.success)
 bb,s,d,u=unpack(best.x);pred=model(best.x)
 ck('positive model speed',np.all(pred>0) and np.isfinite(pred).all())
 return {'B_km2_s2':float(bb),'s_velocity_squared':float(s),'force_exponent_alpha':float(1-s),'disk_ML':float(d),'bulge_ML':float(u),'chi2_train':float(np.sum(best.fun**2)),'parameters':len(best.x),'predicted_v':pred.tolist(),'bound_hit':bool(np.any(np.isclose(best.x,low,atol=1e-5)) or np.any(np.isclose(best.x,high,atol=1e-5)))}
rows=[];allmask=np.ones(len(r),bool)
for ud,ub in [(d,u) for d in [.3,.5,.7] for u in [.5,.7,.9]]+[(None,None)]:
 result={'stellar_setting':'free_bounded' if ud is None else [ud,ub],'models':{}}
 for kind in ['central','inverse_r','constant_g','power']:
  fit=estimate(kind,ud,ub,allmask);pred=np.zeros(len(v))
  for parity in [0,1]:
   train=np.arange(len(v))%2==parity;z=estimate(kind,ud,ub,train);pred[~train]=np.array(z['predicted_v'])[~train]
  fit['held_out_RMSE_km_s']=float(np.sqrt(np.mean((pred-v)**2)));fit['held_out_normalized_RMSE']=float(np.sqrt(np.mean(((pred-v)/ev)**2)));result['models'][kind]=fit
 if ud is not None:
  model=np.sqrt(vg*np.abs(vg)+ud*vd**2+ub*vb**2+bh2+bnl)
  result['BH_only_fixed_scalar_chi2']=float(np.sum(((model-v)/ev)**2))
  result['needed_charge_over_BH_upper_limit']=(result['models']['inverse_r']['B_km2_s2']/bnl)**2
  result['constant_g_over_aLambda']=result['models']['constant_g']['B_km2_s2']*1e6/(25*KPC)/al
 rows.append(result)
# Independent one-parameter minimization checks nominal inverse-r fit.
nom=next(z for z in rows if z['stellar_setting']==[.5,.7]);vb2=vg*np.abs(vg)+.5*vd**2+.7*vb**2
for kind,slope in [('central',-1),('inverse_r',0)]:
 z=minimize_scalar(lambda bb:np.sum(((np.sqrt(vb2+bb*x**slope)-v)/ev)**2),bounds=(0,1e6),method='bounded',options={'xatol':1e-6})
 ck('independent optimizer '+kind,np.isclose(z.x,nom['models'][kind]['B_km2_s2'],rtol=1e-6))
# Symbolic checks: no empirical inputs.
z,ell,A=sp.symbols('z ell A',positive=True)
ck('Yukawa enclosed mass derivative',sp.simplify(sp.diff((1+z/ell)*sp.exp(-z/ell),z)+z/ell**2*sp.exp(-z/ell))==0)
ck('SdS dimensionless mass relation',sp.simplify(1-2*(z/2*(1-z*z/3))/z-z*z/3)==0)
target=sp.sqrt(8*sp.pi);m=target/2*(1-target**2/3)
k=1/sp.sqrt(32*sp.pi);xb=sp.sqrt(1+k*k)-k
ck('SdS surface gravity',sp.simplify((1-xb**2)/(2*xb)-k)==0)
ck('target needs negative SdS mass',float(m)<0)
q0,a0,r0=sp.symbols('q0 a0 r0',positive=True)
field=sp.sqrt(q0*a0)/r0
ck('nonlinear exterior flux',sp.simplify(r0**2*field**2/a0-q0)==0)
res={'aLambda_m_s2':al,'BH_33degree_upper_limit_Msun':qmax,'BH_scalar_B_km2_s2':float(bnl),'r_kpc':r.tolist(),'vobs':v.tolist(),'errV':ev.tolist(),'models':rows,'exact':{'area_target':float(32*sp.pi**2),'SdS_any_horizon_area_bound':float(12*sp.pi),'SdS_BH_area_bound':float(4*sp.pi),'target_dimensionless_mass':float(m),'same_kappa_BH_radius_sqrtLambda':float(xb),'same_kappa_BH_A_Lambda':float(4*sp.pi*xb**2)},'checks':checks,'limitations':['one galaxy','inclination distance fixed','correlated systematics not fitted','stellar gradients and molecular gas missing','alternating-radius holdouts are not independent galaxies','33deg limit is orientation-dependent','phenomenological fits do not define lensing or a relativistic theory']}
(O/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'nominal':nom,'free_stellar':rows[-1],'exact':res['exact'],'aLambda':al,'BH_scalar_B':bnl,'checks':len(checks)},indent=2))
