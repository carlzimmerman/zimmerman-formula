"""Posthoc mean-force approximation stress test; passive circular probes, not live DF."""
import pathlib,json,hashlib,time,numpy as np
from scipy.integrate import cumulative_trapezoid
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];tags=['draco_escape_long','sextans_escape_long'];mf=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json';models={m['name']:m for m in json.loads(mf.read_text())['models']};files=[pathlib.Path(__file__),mf]+[P/'runs'/f'{t}.json' for t in tags]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();rows=[];start=time.time()
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());name=q['parameters']['galaxy'];u=q['physical'];M=u['Munit_Msun'];R=u['Runit_pc'];V=u['Vunit_kms'];rgrid=np.array(q['radial_grid']);edges=np.r_[0,(rgrid+np.r_[rgrid[1:],q['parameters']['rmax']])/2];model=models[name];a0=9.3603e-11*3.085677581491367e10*R/V**2
 aa=[1.] if name=='Draco' else [434.24183347957097/R,794.1886040039351/R]
 def baryon(rad):
  gn=sum((model['stellar_mass']/M/len(aa))*rad/(rad*rad+ar*ar)**1.5 for ar in aa)
  return .5*(gn+np.sqrt(gn*gn+4*a0*gn))
 for birth in [60.,90.]:
  selected=[h for h in q['history'] if h['t']>=birth-1e-8];tt=np.array([h['t'] for h in selected]);cc=np.array([np.r_[0,h['cdf']] for h in selected]);mean=cc.mean(axis=0)
  def meanforce(rad):return baryon(rad)+np.interp(rad,edges,mean,left=0,right=mean[-1])/rad**2
  def dynamic(rad,t):
   j=min(max(int(np.searchsorted(tt,t,side='right')-1),0),len(tt)-2);f=np.clip((t-tt[j])/(tt[j+1]-tt[j]),0,1)
   cold=(1-f)*np.interp(rad,edges,cc[j],left=0,right=cc[j,-1])+f*np.interp(rad,edges,cc[j+1],left=0,right=cc[j+1,-1])
   return baryon(rad)+cold/rad**2
  pr=np.geomspace(1e-4,100.,16384);pp=np.r_[0,cumulative_trapezoid(meanforce(pr),pr)]
  def phi(rad):return np.interp(np.log(rad),np.log(pr),pp)
  for pop,ar in enumerate(aa):
   prob=(np.arange(256)+.5)/256*(6**3/(1+6**2)**1.5);r0=ar/np.sqrt(prob**(-2/3)-1);vc2=r0*meanforce(r0);L2=r0*r0*vc2;E0=.5*vc2+phi(r0)
   for dt in [.01,.005]:
    n=round((tt[-1]-birth)/dt)
    results={}
    for label,g in [('varying',dynamic),('static_mean',lambda r,t:meanforce(r))]:
     rr=r0.copy();vr=np.zeros_like(rr);late=[]
     for k in range(n):
      t=birth+k*dt;vr+=.5*dt*(L2/rr**3-g(rr,t));rr+=dt*vr
      assert min(rr)>0 and np.all(np.isfinite(rr))
      vr+=.5*dt*(L2/rr**3-g(rr,t+dt))
      if k>=.75*n and k%max(1,n//100)==0:late.append(rr.copy())
     dE=.5*(vr*vr+L2/rr**2)+phi(rr)-E0
     results[label]={'final_r50_over_initial':float(np.median(rr)/np.median(r0)),'late_mean_r50_over_initial':float(np.mean([np.median(z) for z in late])/np.median(r0)),'late_mean_starwise_r_over_initial_median':float(np.median(np.mean(late,axis=0)/r0)),'median_radial_excitation_over_initial_vc2':float(np.median(dE/vc2)),'median_final_radial_speed_kms':float(np.median(abs(vr))*V),'max_starwise_fractional_radius_change':float(np.max(abs(rr/r0-1)))}
    row={'tag':tag,'birth_t':birth,'duration_Myr':(tt[-1]-birth)*u['tunit_Myr'],'population':pop,'tracer_scale_pc':ar*R,'dt_code':dt,'results':results};rows.append(row);print(tag,birth,pop,dt,results['varying'],flush=True)
after=hashes();assert before==after
out={'scope':'POSTHOC passive circular-orbit cohorts in fixed stellar+baryonic-law background and saved cold MONOPOLE. Initial orbits circular in future-window sample-mean force; not observed stellar DF, not live self-gravity, no nonspherical force, no cold backreaction, no heating/survival certification. Excitation is measured relative to static mean potential and is not assumed irreversible.','inputs_before':before,'inputs_after':after,'runtime_s':time.time()-start,'results':rows}
(P/'stellar_probes.json').write_text(json.dumps(out,indent=2)+'\n')
