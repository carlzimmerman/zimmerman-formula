import sys,time,resource,json,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np,mpmath as mp
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline
from thermal_core import *

def main(out):
 start=time.monotonic();checks={};controls=[]
 # Hand limits and adaptive quadrature are independent of fixed GL production.
 for y in (0.,1e-6,.001,.1,1,25,400):
  for fermion in (False,True):
   def fun(x):
    en=math.sqrt(x*x+y);q=math.exp(-en)
    return -x*x*math.log1p(q) if fermion else x*x*math.log1p(-q)
   ref=quad(fun,0,np.inf,epsabs=2e-12,epsrel=2e-12)[0]
   a=float(thermal_J([y],fermion,n=128)[0]);b=float(thermal_J([y],fermion,n=256)[0])
   controls.append(dict(y=y,fermion=fermion,adaptive=ref,GL128=a,GL256=b,abs_error128=abs(a-ref),abs_error256=abs(b-ref)))
 checks['GL128_absolute_error_below_5e_7']=max(r['abs_error128'] for r in controls)<5e-7
 checks['GL256_absolute_error_below_1e_8']=max(r['abs_error256'] for r in controls)<1e-8
 dcounts=[]
 for X in (0.,XOLD,10*XOLD):
  b,nb,f,nf=arrays(X);dcounts.append(dict(X=X,bosonic_dof=int(sum(nb)),fermionic_dof=int(sum(nf)),massless_fermionic_dof=int(sum(nf[f<1e-24])),min_scalar_m2=float(min(v for q in blocks(X) for v in q['scalar']))))
 checks['physical_dof']=all(r['bosonic_dof']==146 and r['fermionic_dof']==146 for r in dcounts)
 checks['extra_12_massless_Weyls_at_origin']=dcounts[0]['massless_fermionic_dof']-dcounts[1]['massless_fermionic_dof']==24
 sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
 from block_spectrum import sectors,cw_value
 err=[]
 for X in (0.,.1,XOLD,2*XOLD):
  ss=sectors(X,E,E,G)
  for mine,their in zip(blocks(X)[:3],ss[:3]):
   for key,old in [('scalar','scalars'),('weyl','Weyls'),('vector','vectors')]:
    a=sorted(map(float,mine[key]));b=sorted(map(float,their[old]))
    if key=='scalar' and mine['name']=='broken':b.pop(np.argmin(np.abs(b)))
    err.append(max([abs(v-w) for v,w in zip(a,b)]+[0.]))
 checks['block_eigenvalue_agreement']=max(err)<1e-12
 checks['CW_independent_match']=abs(float(cw_mp(mp.mpf(str(XOLD))))-float(cw_value(XOLD,E,E,G)))<1e-18
 forcecontrols=[]
 for X,T in [(XOLD,.003),(XOLD,.03),(.03,.001)]:
  direct=thermal_force(X,T,n=256);hh=1e-3*max(X,.01);numeric=fd(lambda xx:therm(xx,T,n=256),X,hh)[0]
  forcecontrols.append(dict(X=X,T=T,direct=direct,finite_difference=numeric,relative_error=abs(direct-numeric)/max(abs(direct),1e-80)))
 checks['force_derivative_control']=max(v['relative_error'] for v in forcecontrols)<2e-5
 print('controls',checks,flush=True)
 points=[];global_rows=[]
 for kind in ('canonical','protected'):
  vac=Vacuum(kind);mu=float(vac.mu);xv=float(vac.xv);vbase=vac.leading(0)
  # Leading action global curve and exact local finite action validation.
  Xgrid=np.unique(np.r_[0,np.geomspace(1e-7,1,61),np.linspace(1,2.1*XOLD,180),xv])
  vals=[float(vac.leading(mp.mpf(str(x)))-vbase) for x in Xgrid]
  spline=CubicSpline(Xgrid,vals,bc_type=((1,float(mp.diff(vac.leading,mp.mpf(0)))),(2,float(mp.diff(vac.leading,mp.mpf(str(Xgrid[-1])),2)))))
  k0=float(mp.diff(vac.leading,mp.mpf(0),2));f0=float(mp.diff(vac.leading,mp.mpf(0)))
  leading_min=brentq(spline.derivative(),.8*xv,1.2*xv);deltaV=-float(spline(leading_min))*mu**4
  # Finite preferred curvature from finite-action centered stencil.
  s0=mp.log(vac.xv/vac.xold);h=mp.mpf('.0005');z=[vac.finite(vac.xv*mp.exp(j*h)) for j in (-2,-1,0,1,2)]
  v1=(z[0]-8*z[1]+8*z[3]-z[4])/(12*h);v2=(-z[0]+16*z[1]-30*z[2]+16*z[3]-z[4])/(12*h*h)
  mf=math.sqrt(float(v2)*mu*mu/(62*xv*xv))
  local=[]
  for TT in np.geomspace(1e-5,.3,30):
   ff=xv*thermal_force(xv,TT,n=256)*mu**4
   cur=float(fd(lambda ss:therm(xv*math.exp(ss),TT,n=256),0,1e-3)[1])*mu**4
   local.append(dict(TD_GeV=float(TT*mu),TD_over_mu=float(TT),thermal_log_force_GeV4=float(ff),thermal_log_curvature_GeV4=float(cur),linear_log_displacement=-ff/(2*vac.R**2*vac.ms**2),H_rad_GeV=math.sqrt(math.pi**2*106.75/90)*(TT*mu/.02)**2/2.435e18))
  # Minima/maxima of global leading potential, with force evaluated directly;
  # dense log/linear X nodes resolve origin-shifted extrema.
  xx=np.unique(np.r_[0,np.geomspace(1e-9,1,140),np.linspace(1,2.1*XOLD,220)])
  Ts=np.geomspace(2e-6,.3,100);profiles=[]
  for TT in Ts:
   forces=np.array([float(spline(x,1))+thermal_force(x,TT,n=128) for x in xx])
   rr=[]
   for i in range(len(xx)-1):
    if forces[i]*forces[i+1]<0:
     rt=brentq(lambda x:float(spline(x,1))+thermal_force(x,TT,n=256),xx[i],xx[i+1],xtol=1e-11)
     hh=max(1e-6,rt*1e-4);cur=(float(spline(rt+hh,1))+thermal_force(rt+hh,TT,n=256)-float(spline(rt-hh,1))-thermal_force(rt-hh,TT,n=256))/(2*hh)
     rr.append(dict(X_over_mu=rt,X_over_Xvac=rt/xv,minimum=bool(cur>0),curvature_mu2=cur/62,relative_V_mu4=float(spline(rt))+therm_sub(rt,TT,n=256)))
   profiles.append(dict(TD_over_mu=float(TT),TD_GeV=float(TT*mu),extrema=rr))
  print(kind,'local done','mfinite',mf,'originK',k0,'deltaV',deltaV,flush=True)
  point=dict(kind=kind,mu_GeV=mu,Xvac_over_mu=xv,R_GeV=vac.R,finite_mass_reconstruction_GeV=mf,preferred_radial_mass_GeV=vac.ms,finite_log_slope_mu4=float(v1),finite_log_curvature_mu4=float(v2),origin_force_mu3=f0,origin_curvature_mu2=k0,leading_minimum_X_over_mu=leading_min,DeltaV_origin_to_leading_min_GeV4=deltaV,DeltaV_quarter_GeV=deltaV**.25,local=local,profiles=profiles)
  points.append(point)
 checks['local_finite_radial_mass_matches']=all(abs(p['finite_mass_reconstruction_GeV']/p['preferred_radial_mass_GeV']-1)<.01 for p in points)
 result=dict(claim_id='TH07A_THERMAL_VACUUM',checks={k:bool(v) for k,v in checks.items()},quadrature_controls=controls,dof_counts=dcounts,mass_block_max_difference=max(err),force_controls=forcecontrols,points=points,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Equilibrium ideal-gas one-loop thermal potential on physical rigid valley; exact tree SUGRA plus full rigid CW global profile; finite local T0 normal/two-loop action validation with protected tau held fixed. Unresummed global extrema are not a precision phase transition or reheating solution.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=result['checks'],runtime=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
