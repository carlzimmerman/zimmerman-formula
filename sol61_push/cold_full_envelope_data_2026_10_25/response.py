"""Prescribed mass-preserving halo breathing; passive stars, NOT a cold solver."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import argparse,hashlib,json,math,pathlib,resource,time
import numpy as np
from scipy.integrate import solve_ivp,cumulative_trapezoid
from physics import baryon_g,plummer_g,G
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]

def integrate_case(mc,b0,ms,aa,a,epsilon,period,n=128,tracer=None,tight=False):
 ar=a if tracer is None else tracer;u=(np.arange(n)+.5)/n*.98;r0=ar/np.sqrt(u**(-2/3)-1)
 def total_g(r,b):return baryon_g(r,ms,aa,'canonical')+plummer_g(r,mc,b)
 vc2=r0*total_g(r0,b0);ell2=r0*r0*vc2;tdyn=math.sqrt(a/float(total_g(a,b0)));Ptime=period*tdyn
 def scale(t):
  if t>=4*Ptime:return b0,0.
  om=2*math.pi/Ptime;return b0*(1+.5*epsilon*(1-math.cos(om*t))),b0*.5*epsilon*om*math.sin(om*t)
 def ode(t,y):
  r=y[:n];vr=y[n:2*n];b,bdot=scale(t)
  return np.r_[vr,ell2/r**3-total_g(r,b),G*mc*b*bdot/(r*r+b*b)**1.5]
 times=np.linspace(0,6*Ptime,601);sol=solve_ivp(ode,[0,6*Ptime],np.r_[r0,np.zeros(2*n)],method='DOP853',rtol=1e-10 if tight else 1e-8,atol=1e-12 if tight else 1e-10,t_eval=times)
 assert sol.success and np.min(sol.y[:n])>0
 r=sol.y[:n];vr=sol.y[n:2*n];work=sol.y[2*n:];v2=vr*vr+ell2[:,None]/r**2
 # Fixed baryonic potential with arbitrary constant; it cancels in E(t)-E(0).
 grid=np.geomspace(.0001,1e8,131072);phi=cumulative_trapezoid(baryon_g(grid,ms,aa,'canonical'),grid,initial=0.)
 from scipy.interpolate import CubicSpline
 ps=CubicSpline(np.log(grid),phi);bs=np.array([scale(t)[0] for t in times]);pot=ps(np.log(r))-G*mc/np.sqrt(r*r+bs[None,:]**2);pot0=ps(np.log(r0))-G*mc/np.sqrt(r0*r0+b0*b0)
 E=.5*v2+pot;E0=.5*vc2+pot0;escale=vc2+G*mc/b0;ledger=(E-E0[:,None]-work)/escale[:,None]
 late=times>=5*Ptime;median=np.median(r,axis=0);variance=np.mean(v2,axis=0)/3;sig0=math.sqrt(float(np.mean(vc2)/3));latevar=float(np.mean(variance[late]));lateR=float(np.mean(median[late]));minimum_enc=mc*a**3/(a*a+(b0*(1+epsilon))**2)**1.5;initial_enc=mc*a**3/(a*a+b0*b0)**1.5
 out=dict(epsilon=epsilon,period_over_tdyn=period,period_Myr=Ptime*.977792,tracer_scale_pc=ar,tracers=n,tight=tight,late_r50_ratio=lateR/float(np.median(r0)),late_variance_ratio=latevar/float(np.mean(vc2)/3),initial_orientation_sigma_kms=sig0,late_orientation_sigma_kms=math.sqrt(latevar),delta_sigma_kms=math.sqrt(latevar)-sig0,minimum_enclosed_cold_at_a_Msun=minimum_enc,minimum_enclosed_ratio=minimum_enc/initial_enc,work_ledger_max_relative=float(np.max(abs(ledger))),mean_final_work_kms2=float(np.mean(work[:,-1])),max_final_abs_work_kms2=float(np.max(abs(work[:,-1]))),mean_final_energy_change_kms2=float(np.mean(E[:,-1]-E0)),history=dict(t_Myr=(times*.977792).tolist(),r50_pc=median.tolist(),orientation_variance_kms2=variance.tolist(),mean_work_kms2=np.mean(work,axis=0).tolist()),solver_steps_saved=len(times),solver_evaluations=sol.nfev)
 assert out['work_ledger_max_relative']<1e-5,out['work_ledger_max_relative']
 if epsilon==0:assert max(abs(out['late_r50_ratio']-1),abs(out['late_variance_ratio']-1))<1e-7
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();dest=pathlib.Path(a.out);dest.mkdir(exist_ok=True,parents=True);assert not (dest/'result.json').exists();files=[P/'response.py',P/'physics.py',P/'RESPONSE_CONTRACT.md',P/'test_response.py',P/'fit_002/result.json'];hashes=lambda:{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files};before=hashes();fit=json.loads((P/'fit_002/result.json').read_text());rows=[];refine=[];start=time.time()
 for name,d in fit['datasets'].items():
  f=next(x for x in fit['rows'] if x['name']==name and x['footing']=='canonical' and x['beta']==0);model=f['fixed_supply_envelopes'][1];mc=model['cold_mass_Msun'];b=model['scale_pc'];ms=d['stellar_mass_Msun'];aa=d['tracer_scales_pc'];ar=d['observed_rhalf_pc']
  for tracer in aa:
   for ep,period in [(0.,6.)]+[(ep,period) for ep in [.03,.1,.3] for period in [2.,6.,20.]]:
    row=integrate_case(mc,b,ms,aa,ar,ep,period,tracer=tracer);row.update(name=name,delta_sigma_over_catalogue_error=abs(row['delta_sigma_kms'])/np.mean(d['observed_sigma_errors_kms']),delta_radius_over_catalogue_fractional_error=abs(row['late_r50_ratio']-1)/(np.mean(d['observed_rhalf_errors_pc'])/ar));rows.append(row)
    print(name,tracer,ep,period,'dSigma',round(row['delta_sigma_kms'],5),'r ratio',round(row['late_r50_ratio'],6),'workerr',row['work_ledger_max_relative'],flush=True)
    if ep==.1 and period==6:
     tight=integrate_case(mc,b,ms,aa,ar,ep,period,tracer=tracer,tight=True);check=dict(name=name,tracer_scale_pc=tracer,r50_relative=abs(tight['late_r50_ratio']/row['late_r50_ratio']-1),variance_relative=abs(tight['late_variance_ratio']/row['late_variance_ratio']-1),work_ledger_tight=tight['work_ledger_max_relative']);assert max(check['r50_relative'],check['variance_relative'])<1e-4;refine.append(check)
 result=dict(scope='conditional mass-preserving spherical envelope drive and passive circular stellar probes; not actual field stability, observed DF or retained material mass',rows=rows,refinement=refine,inputs_before=before,inputs_after=hashes(),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);assert before==result['inputs_after'];assert result['peak_RSS_bytes']<750_000_000;(dest/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('DONE',len(rows),result['seconds'],result['peak_RSS_bytes'],flush=True)
if __name__=='__main__':main()
