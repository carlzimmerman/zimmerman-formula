"""Finite sensitivity of conservative number-Newton dynamics to empty-cell seed."""
import sys,json,time,resource
from pathlib import Path
import numpy as np
from network import ROOT,table
from reaction import full_events,serial_moments
from averaged import grid
from coupled_v4 import collision_step

def main(out):
 start=time.monotonic();q,W=grid(8);d=table(3.);ev=full_events(d,.004,q,W,angles=4);n=len(q);cases=[]
 for seed in (0.,1e-25,1e-35,1e-45):
  f=np.full(len(ev.measure),seed);i=ev.by['Fc_0'];f[i*n:(i+1)*n]=1/(np.exp(q)+1);Y=ev.measure*f;E0=float(Y@ev.energy);accepted=0;failed=None;dt=1e7
  for k in range(100):
   try:Y,it=collision_step(ev,Y,dt);accepted+=1
   except RuntimeError as exc:failed=str(exc);break
  m=serial_moments(ev,Y/ev.measure);m.update(seed=seed,accepted=accepted,time_mu=accepted*dt,failed=failed,energy_error=float((Y@ev.energy)/E0-1));cases.append(m);print(seed,accepted,failed,m['charged_number'],m['neutral_force'],flush=True)
 completed=[c for c in cases if c['failed'] is None];reference=next(c for c in completed if c['seed']==1e-35) if any(c['seed']==1e-35 for c in completed) else (completed[0] if completed else None)
 if reference:
  for c in cases:
   if c['failed'] is None:
    c['charged_relative_to_reference']=c['charged_number']/reference['charged_number']-1;c['neutral_force_relative_to_reference']=c['neutral_force']/reference['neutral_force']-1
 checks=dict(all_seeded_completed=all(c['failed'] is None for c in cases if c['seed']>0),energy_conserved=max((abs(c['energy_error']) for c in completed),default=1)<1e-8)
 result=dict(claim_id='CC10_EMPTY_SEED_SENSITIVITY',cases=cases,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Fixedx3 Tc.004 physical F-only FD;100 conservative number-Newton steps to1e9μ^-1. Finite seed sensitivity, not a proof of unique boundary continuum dynamics or complete cosmology.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
