"""Positive-mass rotating baryon perturbation: torque, work, and profile memory."""
from pathlib import Path
import json,time,math
import numpy as np
P=Path(__file__).parent
old=json.loads((P.parent/'halo_formation_probe_v2_run/results.json').read_text());c=old['cell']
M=c['Mcat'];Mb=c['Mb'];ab=c['a'];eps=.01;fg=.5;soft=ab/2
rs=np.array(old['score_radii']);target=np.array(old['target_enclosed_mass'])
def centres(t,d,omega):
 ramp=0 if t<=1 else (1 if t>=1.5 else (1-math.cos(2*math.pi*(t-1)))/2)
 z=d*ramp*np.array([math.cos(omega*t),math.sin(omega*t),0.])
 return z
def pot(pos,t,d,omega):
 r=np.linalg.norm(pos,axis=1);z=centres(t,d,omega)
 return -Mb*(1-fg)/(r+ab)-Mb*fg/2*(1/np.sqrt(np.sum((pos-z)**2,axis=1)+soft**2)+1/np.sqrt(np.sum((pos+z)**2,axis=1)+soft**2))
def force(pos,mp,t,d,omega):
 r=np.linalg.norm(pos,axis=1);order=np.argsort(r);rank=np.empty(len(r));rank[order]=np.arange(len(r))
 acc=-pos*(mp*rank/(r*r+eps*eps)**1.5+Mb*(1-fg)/(np.maximum(r,1e-20)*(r+ab)**2))[:,None]
 z=centres(t,d,omega)
 for centre in [z,-z]:
  delta=pos-centre;acc-=Mb*fg/2*delta/(np.sum(delta*delta,axis=1)+soft**2)[:,None]**1.5
 return acc
def energy(pos,vel,mp,t,d,omega):
 r=np.sort(np.linalg.norm(pos,axis=1))
 return .5*mp*np.sum(vel*vel)-mp*mp*np.sum(np.arange(len(r))/np.sqrt(r*r+eps*eps))+mp*np.sum(pot(pos,t,d,omega))
def run(name,b,d,N,dt,omega=40.):
 rng=np.random.default_rng(123);mp=M/N
 unit=rng.normal(size=(N,3));unit/=np.linalg.norm(unit,axis=1)[:,None]
 rad=b/np.sqrt(((np.arange(N)+.5)/N)**(-2/3)-1);pos=unit*rad[:,None]
 tangent=rng.normal(size=(N,3));tangent-=np.sum(tangent*unit,axis=1)[:,None]*unit;tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 vel=tangent*np.sqrt(rad*np.linalg.norm(force(pos,mp,0,d,omega),axis=1))[:,None]
 L0=np.linalg.norm(np.cross(pos,vel),axis=1);E0=energy(pos,vel,mp,0,d,omega);work=0.;snaps=[];maxerr=0.;Jref=None;maxj=0.;Lref=None
 for it in range(round(8/dt)+1):
  t=it*dt
  if it%round(.5/dt)==0:
   E=energy(pos,vel,mp,t,d,omega);Lz=mp*np.cross(pos,vel)[:,2].sum();J=E-omega*Lz
   if t==1.5:Jref=J;Lref=Lz
   if Jref is not None:maxj=max(maxj,abs(J-Jref)/abs(E0))
   err=abs(E-E0-work)/abs(E0);maxerr=max(maxerr,err)
   radii=np.sort(np.linalg.norm(pos,axis=1));cum=mp*np.searchsorted(radii,rs,side='right')
   snaps.append(dict(t=t,E=float(E),work=float(work),Lz=float(Lz),jacobi=float(J),mass_error=float(np.max(abs(cum-target))/M),mass_inside=float(np.mean(radii<=1)),cumulative_mass=cum.tolist()))
  if it==round(8/dt):break
  tm=t+dt/2;tn=t+dt
  work+=mp*np.sum(pot(pos,tm,d,omega)-pot(pos,t,d,omega))
  vel+=dt/2*force(pos,mp,tm,d,omega);pos+=dt*vel;vel+=dt/2*force(pos,mp,tm,d,omega)
  work+=mp*np.sum(pot(pos,tn,d,omega)-pot(pos,tm,d,omega))
 L=np.linalg.norm(np.cross(pos,vel),axis=1);barL=fg*Mb*d*d*omega
 return dict(name=name,b=b,d=d,N=N,dt=dt,omega=omega,work_error=float(maxerr),jacobi_error_after_growth=float(maxj),median_absolute_fractional_L_change=float(np.median(abs(L/L0-1))),p90_absolute_fractional_L_change=float(np.quantile(abs(L/L0-1),.9)),steady_delta_Lz=float(snaps[-1]['Lz']-Lref),nominal_bar_Lz=float(barL),angular_momentum_demand_fraction=None if d==0 else float((snaps[-1]['Lz']-Lref)/barL),snapshots=snaps)
rows=[]
configs=[(f'{label}_b{b}',b,d,1024,.001) for b in [.15,.3] for label,d in [('static',0),('bar',.01),('widebar',.04)]]+[(f'widebar_b{b}_refined',b,.04,2048,.0005) for b in [.15,.3]]
for conf in configs:
 r=run(*conf);rows.append(r);print(r['name'],r['work_error'],r['jacobi_error_after_growth'],r['snapshots'][-1]['mass_error'],flush=True)
 out=dict(rows=rows,scope='Spherical self gravity plus positive-mass prescribed rotating baryon pair; no target force; no live bar backreaction',score_radii=rs.tolist(),target=target.tolist(),cell=c)
 (P/'torque_halo_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
out['checks']=[dict(name=r['name']+' work',passed=r['work_error']<.02) for r in rows]+[dict(name=r['name']+' Jacobi',passed=r['jacobi_error_after_growth']<.02) for r in rows];out['all_pass']=all(x['passed'] for x in out['checks']);(P/'torque_halo_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n');assert out['all_pass']
