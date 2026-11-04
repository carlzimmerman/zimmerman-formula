import sys,time,json,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
from thermal_core_v2 import *
from scipy.interpolate import CubicSpline
from scipy.optimize import root,brentq

def main(out):
 start=time.monotonic();rows=[];checks={};directcontrols=[]
 for kind in ('canonical','protected'):
  vac=Vacuum(kind);mu=float(vac.mu);xv=float(vac.xv);base=vac.leading(0)
  # Shape interpolation for robust seed finding, subsequently checked by direct mp forces.
  xx=np.unique(np.r_[0,np.geomspace(1e-7,1,100),np.linspace(1,70,400),xv])
  yy=[float(vac.leading(mp.mpf(str(x)))-base) for x in xx]
  sp=CubicSpline(xx,yy,bc_type=((1,float(mp.diff(vac.leading,0))),(2,float(mp.diff(vac.leading,mp.mpf(70),2)))))
  def f(x,t,n=256):return float(sp(x,1))+thermal_force(x,t,n=n)
  def df(x,t,n=256):
   hh=max(1e-5,abs(x)*1e-4)
   return float(sp(x,2))+(thermal_force(x+hh,t,n=n)-thermal_force(x-hh,t,n=n))/(2*hh)
  spins=[]
  for name,seed in [('origin',(.2,.0048)),('vacuum',((1.1*xv),(.0007 if kind=='canonical' else .00105)))]:
   def eq(zz):
    x,t=zz
    if t<=0:return [1e4,1e4]
    return [f(x,t)*1e12,df(x,t)*1e12]
   sol=root(eq,seed,tol=1e-8)
   x,t=sol.x
   # Recover direct T0 force/curvature and 128/256 quadrature controls.
   d0=float(mp.diff(vac.leading,mp.mpf(str(x))));d20=float(mp.diff(vac.leading,mp.mpf(str(x)),2))
   th=thermal_force(x,t,n=256);hh=max(1e-5,abs(x)*1e-4);th2=(thermal_force(x+hh,t,n=256)-thermal_force(x-hh,t,n=256))/(2*hh)
   rhoSM=math.pi**2/30*106.75*(t*mu/.02)**4
   gap=float(vac.leading(mp.mpf(str(x)))-vac.leading(vac.xv))*mu**4
   spins.append(dict(name=name,root_success=bool(sol.success),X_over_mu=float(x),X_over_Xvac=float(x/xv),TD_over_mu=float(t),TD_GeV=float(t*mu),residual_scaled=list(map(float,sol.fun)),T0_force_direct=d0,T0_force_spline=float(sp(x,1)),force_direct_total=d0+th,T0_curvature_direct=d20,total_curvature_direct=d20+th2,force_GL128=thermal_force(x,t,n=128),force_GL256=th,zero_T_excess_GeV4=gap,rho_SM_GeV4=rhoSM,zero_T_excess_over_rhoSM=gap/rhoSM,Hrad_GeV=math.sqrt(rhoSM/3)/2.435e18,radial_curvature_scale_GeV=math.sqrt(abs(d20)*mu*mu/62)))
  # Wide subPlanck probe, including direct high-precision T0 derivatives; no fit extrapolation.
  wide=[]
  for t in (.0005,.0015,.004,.005,.008,.03):
   vals=[]
   for x in np.geomspace(1.5*xv,1e5*XOLD,60):
    d0=float(mp.diff(vac.leading,mp.mpf(str(x))))
    ft=thermal_force(x,t,n=256)
    vals.append(dict(X_over_mu=float(x),X_over_Xvac=float(x/xv),T0_force_mu3=d0,thermal_force_mu3=ft,total_force_mu3=d0+ft))
   wide.append(dict(TD_over_mu=t,TD_GeV=t*mu,positive_force_count=sum(v['total_force_mu3']>0 for v in vals),negative_force_count=sum(v['total_force_mu3']<0 for v in vals),rows=vals))
  # Isolated origin branch minima/maxima just above spin, thermal energy/entropy.
  os=spins[0];details=[]
  for factor in (1.001,1.01,1.05,1.2):
   t=os['TD_over_mu']*factor;xs=np.geomspace(1e-8,20,300);fr=[f(x,t) for x in xs];roots=[]
   for i in range(len(xs)-1):
    if fr[i]*fr[i+1]<0:
     rt=brentq(lambda x:f(x,t),xs[i],xs[i+1]);
     F=therm(rt,t,n=256);dT=fd(lambda tt:therm(rt,tt,n=256),t,t*1e-3)[0];rho=F-t*dT;entropy=-dT
     roots.append(dict(X_over_mu=rt,minimum=df(rt,t)>0,F_thermal_mu4=F,rho_thermal_mu4=rho,entropy_thermal_mu3=entropy))
   details.append(dict(TD_GeV=t*mu,TD_over_mu=t,roots=roots))
  rows.append(dict(kind=kind,mu_GeV=mu,spins=spins,wide=wide,origin_branch=details))
 checks['all_spinodal_roots_solved']=all(z['root_success'] for r in rows for z in r['spins'])
 checks['spinodal_force_direct_small']=all(abs(z['force_direct_total'])<2e-15 for r in rows for z in r['spins'])
 checks['origin_release_not_visible_dominant']=all(r['spins'][0]['zero_T_excess_over_rhoSM']<1e-6 for r in rows)
 checks['wide_stays_subPlanck']=all(1e5*XOLD*r['mu_GeV']/2.435e18<1e-3 for r in rows)
 result=dict(claim_id='TH07B_STATIC_REFINED',checks=checks,points=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Direct exact-tree+full-rigid-CW derivative checks, unresummed static thermal extrema and finite wide-X force probes. No real-time evolution, chemical-equilibrium theorem, or ring-resummed critical prediction. Light field force spline and finite grid limits explicit.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,runtime=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'],spins=[dict(kind=r['kind'],spins=r['spins']) for r in rows])));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
