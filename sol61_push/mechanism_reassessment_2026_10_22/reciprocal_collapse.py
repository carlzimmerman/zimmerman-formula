"""Closed conservative cold-shell + homologous uniform gas sphere prototype."""
import json,sys
from pathlib import Path
import numpy as np
rows=[]
for N,h in [(32,.0005),(64,.00025)]:
 dm=1/N;m=np.arange(1,N+1)*dm;w=np.full(N,dm);w[-1]=dm/2;r=6*m**(1/3);v=np.zeros(N);B=3.;V=0.;kappa=.3;inertia=.6
 def forces(r,B):
  volume=np.diff(np.r_[0,r**3])/3
  if min(volume)<=0 or min(r*r-m)<=0 or B<=0:raise ValueError('domain guard')
  pressure=.005*(dm/volume)**2
  gb=np.where(r<B,r/B**3,1/r**2)
  cold=r*r*(pressure-np.r_[pressure[1:],0])/w+(m/r**2)**2/(1-m/r**2)-gb
  derivative=np.where(r<B,1.5*(B*B-r*r)/B**4,0)
  baryon=(2*kappa/B**3-.6/B**2-np.sum(w*derivative)-.5*dm*1.5/B**2)/inertia
  return cold,baryon
 def energy(r,v,B,V):
  volume=np.diff(np.r_[0,r**3])/3
  potential=np.where(r<B,-(3*B*B-r*r)/(2*B**3),-1/r)
  return float(.5*np.sum(w*v*v)+.3*V*V+.005*np.sum(dm*dm/volume)+np.sum(w*(np.sqrt(m)*np.arctanh(np.sqrt(m)/r)-m/r))+kappa/B**2-.6/B+np.sum(w*potential)-.5*dm*1.5/B)
 E0=energy(r,v,B,V);a,aB=forces(r,B);samples=[];failure=None
 for i in range(int(100/h)):
  v+=h*a/2;V+=h*aB/2;r+=h*v;B+=h*V
  try:a,aB=forces(r,B)
  except ValueError as e:failure=dict(time=(i+1)*h,reason=str(e));break
  v+=h*a/2;V+=h*aB/2
  if (i+1)%round(1/h)==0:samples.append(dict(t=(i+1)*h,B=float(B),cold_half_mass_radius=float(np.interp(.5,m,r)),cold_edge=float(r[-1]),energy=energy(r,v,B,V)))
 rows.append(dict(N=N,dt=h,initial_energy=E0,initial_baryon_radius=3.,initial_cold_half_mass_radius=6*.5**(1/3),failure=failure,samples=samples,max_energy_error=max([abs(s['energy']-E0) for s in samples],default=None)))
checks=dict(completed=all(r['failure'] is None for r in rows),energy=all(r['max_energy_error'] is not None and r['max_energy_error']<1e-5 for r in rows))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='closed two-component collapse from chosen cold/subvirial initial conditions; gas entropy fixed; no primordial production, cooling or cosmological setup')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{**r,'samples':r['samples'][-3:]} for r in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
