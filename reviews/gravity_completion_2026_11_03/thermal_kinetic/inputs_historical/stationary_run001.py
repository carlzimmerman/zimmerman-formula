"""TK08: fixed occupation of the actual charged fermion light eigenbranch."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
import mpmath as mp
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'thermal'))
from thermal_core import Vacuum,thermal_force,E,G,A0,cw_mp

DG=np.array([[E/2,0,0],[0,0,5*G],[0,5*G,0.]])
def light(x):
 M=np.array([[E*x/2,-E*A0/2,5*G*A0],[-E*A0/2,0,5*G*x],[5*G*A0,5*G*x,0.]])
 w,u=np.linalg.eigh(M);v=u[:,1];mass=w[1];dm=float(v@DG@v)
 return float(mass),dm

def nodes(n):
 z,w=leggauss(n);p=25*(z+1);return p,25*w*p*p/(np.exp(p)+1)
Q={n:nodes(n) for n in (128,256)}
def frozen(x,t,n=128):
 m,dm=light(x);p,w=Q[n];en=np.sqrt(p*p+(m/t)**2);pref=24/(2*math.pi**2)
 rho=pref*t**4*float(w@en)
 force=pref*t*t*m*dm*float(w@(1/en))
 pressure=pref*t**4/3*float(w@(p*p/en))
 return rho,force,pressure
def eq_light_force(x,t,n=128):
 m,dm=light(x);p,w=Q[n];en=np.sqrt(p*p+(m/t)**2)
 # Undo the frozen FD weight and insert FD of the actual energy.
 ratio=(np.exp(p)+1)/(np.exp(np.minimum(en,745))+1)
 return 24/(2*math.pi**2)*t*t*m*dm*float(w@(ratio/en))

def main(out):
 start=time.monotonic();checks={};controls=[]
 for r in (0,1e-4,.1,1,10,100):
  z,w=Q[256];got=float(w@(1/np.sqrt(z*z+r*r)))
  ref=quad(lambda p:p*p/(math.exp(p)+1)/math.sqrt(p*p+r*r),0,80,epsabs=1e-12)[0]
  controls.append(dict(m_over_t=r,force_integral=got,adaptive=ref,absolute_error=abs(got-ref)))
 checks['FD_force_quadrature']=max(v['absolute_error'] for v in controls)<2e-10
 checks['FD_massless_energy']=abs(frozen(0,1,256)[0]/(24*7*math.pi**2/240)-1)<1e-12
 m0,d0=light(0)
 # Exact zero-mode projection: q=-e a/2, A=5 g a.
 exact_d0=(5*G)*2*(5*G*A0)*(E*A0/2)/((5*G*A0)**2+(E*A0/2)**2)
 checks['origin_eigen_slope']=abs(d0/exact_d0-1)<1e-13
 checks['origin_mass_zero']=abs(m0)<1e-17
 ms=[light(x) for x in np.linspace(0,200,401)]
 checks['light_mass_positive_monotone_grid']=min(m for m,d in ms)>-1e-17 and min(d for m,d in ms)>0
 derivatives=[]
 for x,t in ((.01,.004),(1,.004),(25,.001),(100,.0001)):
  h=max(1e-5,x*1e-4);numer=(frozen(x+h,t,256)[0]-frozen(x-h,t,256)[0])/(2*h);f=frozen(x,t,256)[1]
  derivatives.append(dict(x=x,t=t,numeric=numer,direct=f,relative_error=abs(numer/f-1)))
 checks['energy_force_derivative']=max(v['relative_error'] for v in derivatives)<1e-6
 # Expansion identity at fixed x, Tc proportional a^-1.
 expansion=[]
 for x,t in ((0,.004),(1,.004),(25,.001)):
  h=1e-4;rp=frozen(x,t*math.exp(-h),256)[0];rm=frozen(x,t*math.exp(h),256)[0]
  rho,force,p=frozen(x,t,256);err=abs((rp-rm)/(2*h)+3*(rho+p))/rho
  expansion.append(dict(x=x,t=t,relative_identity_error=err))
 checks['expansion_energy_identity']=max(v['relative_identity_error'] for v in expansion)<2e-7
 rows=[]
 grid=np.unique(np.r_[0,np.geomspace(1e-8,1,90),np.linspace(1,60,240),np.linspace(60,200,60)])
 tgrid=np.unique(np.r_[np.geomspace(.0001,.01,65),.0048,.004,.003,.002,.001,.0007,.00064])
 rootsgrid=np.unique(np.r_[0,np.geomspace(1e-10,1,100),np.linspace(1,200,450)])
 for kind in ('canonical','protected'):
  vac=Vacuum(kind);vbase=vac.leading(mp.mpf(0));vals=np.array([float(vac.leading(mp.mpf(str(x)))-vbase) for x in grid]);f0=float(mp.diff(vac.leading,mp.mpf(0)));k0=float(mp.diff(vac.leading,mp.mpf(0),2))
  spline=CubicSpline(grid,vals,bc_type=((1,f0),(2,float(mp.diff(vac.leading,mp.mpf(200),2)))))
  branches=[]
  for mode in ('frozen_only','frozen_plus_other_equilibrium'):
   for t in tgrid:
    def force(x):
     value=float(spline(x,1))+frozen(x,t)[1]
     if mode=='frozen_plus_other_equilibrium':value+=thermal_force(x,t)-eq_light_force(x,t)
     return value
    fs=[force(x) for x in rootsgrid];rr=[]
    for left,right,fl,fr in zip(rootsgrid[:-1],rootsgrid[1:],fs[:-1],fs[1:]):
     if fl*fr<0:
      rt=brentq(force,left,right,xtol=1e-11);h=max(1e-6,rt*1e-4);cur=(force(rt+h)-force(rt-h))/(2*h)
      rho,ff,pp=frozen(rt,t,256);mu=float(vac.mu)
      rr.append(dict(x=rt,x_over_vac=rt/float(vac.xv),minimum=bool(cur>0),mass_GeV=light(rt)[0]*mu,radial_m2_GeV2=cur*mu*mu/62,rho_frozen_mu4=rho,pressure_frozen_mu4=pp,force_frozen_mu3=ff))
    branches.append(dict(mode=mode,t=t,TD_GeV=t*float(vac.mu),extrema=rr))
  rows.append(dict(kind=kind,mu_GeV=float(vac.mu),xvac=float(vac.xv),origin_force=f0,origin_curvature=k0,light_origin_slope=d0,light_only_instability_T_over_mu=math.sqrt(-k0/(d0*d0)),branches=branches,grid=grid.tolist(),T0_potential_mu4=vals.tolist(),T0_origin_reference_mu4=float(vbase)))
  print(kind,'done',flush=True)
 result=dict(claim_id='TK08_FROZEN_STATIONARY',checks={k:bool(v) for k,v in checks.items()},quadrature_controls=controls,derivative_controls=derivatives,expansion_controls=expansion,light_origin_slope=d0,zero_mode_gaugino_fraction=(E*A0/2)**2/((5*G*A0)**2+(E*A0/2)**2),mass_slope_grid=[dict(x=x,mass=light(x)[0],slope=light(x)[1]) for x in (0,.1,1,5,10,25,50,100,200)],points=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Frozen assumed FD occupation of 12 charged Weyls; leading global tree SUGRA+rigid CW. Hybrid other-species equilibrium is a stationary limiting diagnostic, no photino abundance or consistent collision operator.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
