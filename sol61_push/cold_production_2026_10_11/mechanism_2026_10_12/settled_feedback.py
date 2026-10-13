"""Forward spherical collisionless halo response to bracketed baryon cycles."""
import json, math, time
from pathlib import Path
import numpy as np
P=Path(__file__).parent
old=json.loads((P.parent/'halo_formation_probe_v2_run/results.json').read_text())
c=old['cell'];M=c['Mcat'];Mb=c['Mb'];a0=c['a'];eps=.01
rscore=np.array(old['score_radii']);target=np.array(old['target_enclosed_mass'])
def scale(t,mode,start):
 if mode=='static':return a0
 z=t-start
 if z<0 or z>=3.2:return a0
 phase=z%.8
 if phase>=.62:return a0
 up=.02 if mode=='rapid' else .31
 down=.62-up
 if phase<up:f=(1-math.cos(math.pi*phase/up))/2
 else:f=(1+math.cos(math.pi*(phase-up)/down))/2
 return a0*(1+7*f)
def force(pos,mp,a,fg):
 r=np.linalg.norm(pos,axis=1);order=np.argsort(r);rank=np.empty(len(r));rank[order]=np.arange(len(r))
 sg=mp*rank/(r*r+eps*eps)**1.5
 bg=Mb*((1-fg)/(r+a0)**2+fg/(r+a)**2)/np.maximum(r,1e-20)
 return -pos*(sg+bg)[:,None]
def bp(pos,a,fg,mp):
 r=np.linalg.norm(pos,axis=1)
 return -mp*Mb*np.sum((1-fg)/(r+a0)+fg/(r+a))
def energy(pos,vel,mp,a,fg):
 r=np.sort(np.linalg.norm(pos,axis=1))
 return .5*mp*np.sum(vel*vel)-mp*mp*np.sum(np.arange(len(r))/np.sqrt(r*r+eps*eps))+bp(pos,a,fg,mp)
def run(name,N,dt,mode,fg,start,plummer_scale):
 rng=np.random.default_rng(123);mp=M/N
 z=rng.normal(size=(N,3));z/=np.linalg.norm(z,axis=1)[:,None]
 # Deterministic radial quantiles of a Plummer density, random orbital planes.
 massfrac=(np.arange(N)+.5)/N
 radii=plummer_scale/np.sqrt(massfrac**(-2/3)-1)
 pos=z*radii[:,None]
 tangent=rng.normal(size=(N,3));tangent-=np.sum(tangent*z,axis=1)[:,None]*z
 tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 accel=force(pos,mp,a0,fg)
 speed=np.sqrt(radii*np.linalg.norm(accel,axis=1))
 vel=tangent*speed[:,None]
 L0=np.linalg.norm(np.cross(pos,vel),axis=1)
 initial_cdf=mp*np.searchsorted(radii,rscore,side='right')
 E0=energy(pos,vel,mp,a0,fg);work=0.;positive=0.;snaps=[];maxerr=0.;clock=time.monotonic()
 for i in range(round(8/dt)+1):
  t=i*dt;a=scale(t,mode,start)
  if i%round(.5/dt)==0:
   E=energy(pos,vel,mp,a,fg);err=abs(E-E0-work)/abs(E0);maxerr=max(maxerr,err)
   rad=np.sort(np.linalg.norm(pos,axis=1));cum=mp*np.searchsorted(rad,rscore,side='right')
   benc=Mb*rscore*rscore/(rscore+a0)**2
   snaps.append(dict(t=t,time_Gyr=t*c['tu_Gyr'],mass_fraction_inside=float(np.mean(rad<=1)),mass_error=float(np.max(abs(cum-target))/M),log_acceleration_rms=float(np.sqrt(np.mean(np.log10((benc+cum)/(benc+target))**2))),energy=float(E),work=float(work),work_balance_error=float(err),cumulative_mass=cum.tolist()))
  if i==round(8/dt):break
  am=scale(t+dt/2,mode,start);an=scale(t+dt,mode,start)
  dw=bp(pos,am,fg,mp)-bp(pos,a,fg,mp);work+=dw;positive+=max(dw,0)
  acc=force(pos,mp,am,fg);vel+=dt/2*acc;pos+=dt*vel;vel+=dt/2*force(pos,mp,am,fg)
  dw=bp(pos,an,fg,mp)-bp(pos,am,fg,mp);work+=dw;positive+=max(dw,0)
 return dict(plummer_scale=plummer_scale,initial_cumulative_mass=initial_cdf.tolist(),max_fractional_angular_momentum_error=float(np.max(abs(np.linalg.norm(np.cross(pos,vel),axis=1)/L0-1))),name=name,N=N,dt=dt,mode=mode,gas_fraction=fg,start=start,net_driver_work=float(work),positive_work_sum=float(positive),initial_energy=float(E0),max_sampled_work_balance_error=float(maxerr),seconds=time.monotonic()-clock,snapshots=snaps)
configs=[(f'{mode}_b{b}',1024,.001,mode,.5,1.,b) for b in [.15,.3] for mode in ['static','rapid','slow']]+[(f'{mode}_b{b}_refined',2048,.0005,mode,.5,1.,b) for b in [.15,.3] for mode in ['static','rapid']]
rows=[]
for conf in configs:
 r=run(*conf);rows.append(r);print(r['name'],r['max_sampled_work_balance_error'],r['snapshots'][-1]['mass_error'],flush=True)
 out=dict(rows=rows,cell=c,score_radii=rscore.tolist(),target=target.tolist(),scope='Initially circular shell equilibrium, Plummer radial mass quantiles, spherical collisionless gravity, prescribed gas redistribution; no target in forces')
 (P/'settled_feedback_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
out['checks']=[dict(name=r['name']+' work accounting',passed=r['max_sampled_work_balance_error']<.02) for r in rows];out['checks'] += [dict(name=r['name']+' angular momentum',passed=r['max_fractional_angular_momentum_error']<1e-9) for r in rows];out['all_pass']=all(z['passed'] for z in out['checks']);(P/'settled_feedback_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n');assert out['all_pass']
