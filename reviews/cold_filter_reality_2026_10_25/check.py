import argparse,importlib.util,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,solve_ivp
from scipy.optimize import brentq
from astropy.io import fits
import sympy as S
spec=importlib.util.spec_from_file_location('interface','reviews/cold_filter_interface_2026_10_25/check.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
VQ=S.lambdify((a.q,a.d),S.diff(a.V,a.q),'numpy')
PC=3.085677581491367e16;MSUN=1.98847e30;G=6.67430e-11
NAMES=['A1795','A2029','A2142','A2319','A644','A85','ZW1215']
X=np.array([.1,.2,.3,.5,.7,1.])

def clusters(mutate):
 rows=[]
 for name in NAMES:
  with fits.open(f'real_research/data/xcop/{name}/{name}_fgas_profile.fits') as h:
   t=h[1].data.copy();r500=float(h[1].header['R500'])
  mass=np.exp(np.interp(np.log(X),np.log(t['RADIUS']),np.log(t['MGAS'])))
  errlo=np.interp(np.log(X),np.log(t['RADIUS']),t['MGAS_LO'])
  errhi=np.interp(np.log(X),np.log(t['RADIUS']),t['MGAS_HI'])
  r=X*r500*(1 if mutate else 1000)*PC
  volume=4*np.pi/3*np.diff(r**3)
  rho=np.diff(mass)*MSUN/volume
  independent=np.diff(mass)/(4*np.pi/3*np.diff((X*r500*1000)**3))*MSUN/PC**3
  assert np.allclose(rho,independent,rtol=1e-12,atol=0),'radius units mismatch'
  low=(mass[1:]-errlo[1:]-mass[:-1]-errhi[:-1])*MSUN/volume
  assert np.all(rho>0)
  for H in [1e-18,1.8e-18,3e-18]:
   Dmass=3*H*H/(8*np.pi*G)*.75
   for i in range(5):
    dd=float(rho[i]/Dmass);lb=float(low[i]/Dmass)
    rows.append(dict(name=name,HJ=H,inner_X=float(X[i]),outer_X=float(X[i+1]),gas_density_kg_m3=float(rho[i]),d=dd,endpoint_box1_d_lower=lb,
        above_slow_threshold=dd>31.04,box1_lower_above_threshold=lb>31.04))
 return rows

def smooth(w):
 L=max(20.,16*w)
 density=lambda z:10*(1-np.tanh(np.asarray(z)/w))
 z=np.unique(np.round(np.r_[np.linspace(-L,L,1601),np.linspace(-min(L,20),min(L,20),801)],12))
 assert np.min(np.diff(z))>1e-9
 def eqy(dd):
  if dd>=8:return 0.
  return brentq(lambda y:(8-12*y)/(1-y/4)**1.5-dd,0,2/3)
 y=np.array([eqy(dd) for dd in density(z)])
 q=2*np.arcsin(np.sqrt(y/4))
 guess=np.vstack([q,np.gradient(q,z)])
 sol=solve_bvp(lambda z,u:np.vstack([u[1],VQ(u[0],density(z))]),
      lambda l,r:np.array([l[0],r[0]-a.QOUT]),z,guess,tol=1e-6,max_nodes=30000)
 assert sol.success,sol.message
 zz=np.linspace(-L,L,5001);qq=sol.sol(zz)[0]
 assert np.min(qq)>-1e-6 and np.max(qq)<a.QOUT+1e-6
 def pot(z):return float(a.HESS(float(sol.sol(z)[0]),float(density(z))))
 def wave(pm,rtol=1e-9):
  k=2.4*pm;om=5.76*(1+pm*pm);kin=math.sqrt(om-3.)
  z=solve_ivp(lambda z,u:[u[1],(pot(z)-om)*u[0]],[-L,L],np.array([1+0j,-1j*kin]),
       method='DOP853',rtol=rtol,atol=rtol*.01)
  assert z.success
  u,du=z.y[:,-1];inc=(u+1j*du/k)/2;ref=(u-1j*du/k)/2
  R=float(abs(ref/inc)**2);T=float(kin/k/abs(inc)**2)
  assert abs(R+T-1)<1e-6,'wave flux'
  return dict(pm=pm,R=R,T=T,flux_error=abs(R+T-1))
 waves=[wave(pm) for pm in [.001,.003,.01]];tight=wave(.001,2e-10)
 assert abs(tight['R']-waves[0]['R'])<1e-5
 return dict(width=w,L=L,nodes=len(sol.x),max_BVP_residual=float(max(sol.rms_residuals)),waves=waves,tight_R=tight['R'])

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');arg=p.parse_args()
 out=Path(arg.output);out.mkdir(parents=True,exist_ok=True)
 rows=clusters(arg.mutate);profiles=[smooth(w) for w in [.1,1.,10.,100.]]
 summary={}
 for H in [1e-18,1.8e-18,3e-18]:
  rr=[x for x in rows if x['HJ']==H]
  summary[str(H)]=dict(count=len(rr),min_d=min(x['d'] for x in rr),max_d=max(x['d'] for x in rr),
    above=sum(x['above_slow_threshold'] for x in rr),box1_lower_above=sum(x['box1_lower_above_threshold'] for x in rr))
 result=dict(scope='fixed illustrative point; smooth source controls and cluster shell-average diagnostic',cluster_rows=rows,cluster_summary=summary,smooth_profiles=profiles)
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(cluster_summary=summary,smooth_profiles=profiles),indent=2))
if __name__=='__main__':main()
