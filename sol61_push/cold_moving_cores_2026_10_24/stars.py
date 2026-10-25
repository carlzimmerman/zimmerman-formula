"""Passive inertial star cohorts: evolving nonspherical cold field versus frozen control."""
import pathlib,json,hashlib,resource,time,sys,numpy as np
from tracking import Potential
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];tag=sys.argv[1];run=P/'runs'/f'{tag}.json';track=P/'runs'/f'{tag}_tracking.json';npz=P/'runs'/f'{tag}_tracking.npz';source=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json';pins=[pathlib.Path(__file__),P/'tracking.py',run,track,npz,source,P/'CONTRACT.md'];before={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins};q=json.loads(run.read_text());tr=json.loads(track.read_text());z=np.load(npz);ts=z['times'];co=z['potential_coefficients'];r=z['r'];lm=z['lm'];phys=q['physical'];M=phys['Munit_Msun'];R=phys['Runit_pc'];V=phys['Vunit_kms'];name=q['parameters']['galaxy'];g=next(g for g in json.loads(source.read_text())['models'] if g['name']==name);Ms=g['stellar_mass']/M;A0=9.3603e-11*3.085677581491367e10*R/(V*V);rng=np.random.default_rng(1010);N=128
# Paired directions cancel initial position/velocity sampling dipoles.
u=rng.normal(size=(N//2,3));u/=np.linalg.norm(u,axis=1)[:,None];u=np.r_[u,-u];vv=rng.normal(size=(N//2,3));vv=np.r_[vv,-vv];tan=vv-u*np.sum(vv*u,axis=1)[:,None];tan/=np.linalg.norm(tan,axis=1)[:,None];quant=(np.arange(N//2)+.5)/(N//2);Fmax=3**3/(1+3**2)**1.5;f=quant*Fmax;rr=(f**(-2/3)-1)**(-.5);rr=np.r_[rr,rr]
scales=[1.] if name!='Sextans' else [434.24183348/R,794.188604/R];rad=rr*np.resize(scales,N);c=np.array(tr['history'][0]['aperture_COM_code']);bulk=np.array(tr['history'][0]['aperture_velocity_code']);x0=c+rad[:,None]*u

def baryon_acc(x):
 center=x.mean(axis=0);d=x-center;s=np.maximum(np.linalg.norm(d,axis=1),1e-10);gn=sum(Ms/len(scales)*s/(s*s+a*a)**1.5 for a in scales);gb=.5*(gn+np.sqrt(gn*gn+4*A0*gn));return -gb[:,None]*d/s[:,None]
def field(t,static=False):
 if static:return Potential(r,co[0],lm)
 j=np.clip(np.searchsorted(ts,t)-1,0,len(ts)-2);f=np.clip((t-ts[j])/(ts[j+1]-ts[j]),0,1);return Potential(r,(1-f)*co[j]+f*co[j+1],lm)
a0=-field(ts[0]).evaluate(x0,True)+baryon_acc(x0);inward=np.maximum(-np.sum(a0*u,axis=1),0);v0=bulk+np.sqrt(rad*inward)[:,None]*tan

def stats(x,v):
 cc=x.mean(axis=0);vel=v-v.mean(axis=0);d=x-cc;rr=np.linalg.norm(d,axis=1);return dict(COM_pc=(cc*R).tolist(),bulk_velocity_kms=(v.mean(axis=0)*V).tolist(),r50_pc=float(np.median(rr)*R),r90_pc=float(np.quantile(rr,.9)*R),sigma_1d_kms=float(np.sqrt(np.mean(vel*vel))*V),vr_rms_kms=float(np.sqrt(np.mean((np.sum(vel*d,axis=1)/np.maximum(rr,1e-10))**2))*V))
rows=[];initial=stats(x0,v0);start=time.time()
for dt in [.02,.01]:
 for static in [False,True]:
  x=x0.copy();v=v0.copy();out=[];n=round((ts[-1]-ts[0])/dt)
  for k in range(n):
   t=ts[0]+k*dt;a=-field(t,static).evaluate(x,True)+baryon_acc(x);v+=dt*a/2;x+=dt*v;a=-field(t+dt,static).evaluate(x,True)+baryon_acc(x);v+=dt*a/2
   if (k+1)%round(.5/dt)==0:out.append(dict(t=t+dt,**stats(x,v)))
  last=out[-1];cold_c=np.array(tr['history'][-1]['aperture_COM_code'])*R;last['star_cold_COM_separation_pc']=float(np.linalg.norm(np.array(last['COM_pc'])-cold_c));last['fraction_within_Rstar_of_tracked_cold_COM']=float(np.mean(np.linalg.norm(x*R-cold_c,axis=1)<R));rows.append(dict(dt=dt,static_cold=static,history=out));print(tag,dt,static,last,flush=True)
after={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins};assert before==after
(P/'runs'/f'{tag}_stars.json').write_text(json.dumps(dict(scope='paired passive circular cohorts in full nonspherical cold potential; moving rigid baryonic self/Xi background, absent cold backreaction/host/live DF; comparison to frozen same field, not an observational fit or irreversible heating measurement',parameters=dict(N=N,seed=1010,initial_radius_truncation_Rstar=3,initial_velocity='local radial circular speed plus aperture wave-current bulk velocity',stellar_mass=g['stellar_mass'],elapsed_Myr=(ts[-1]-ts[0])*phys['tunit_Myr']),initial=initial,initial_outward_force_fraction=float(np.mean(inward==0)),results=rows,inputs_before=before,inputs_after=after,seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
