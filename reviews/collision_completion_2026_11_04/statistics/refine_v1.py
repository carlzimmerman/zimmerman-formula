"""Discriminate soft momentum projection error and event time splitting."""
import sys,json,time,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from quantum_v2 import *

def grid(soft):
 q=np.unique(np.r_[0.,np.geomspace(1e-6,.02,9),np.linspace(.025,1.,soft),np.linspace(1.25,20.,40),30.,50.,80.])
 edges=np.r_[0.,(q[:-1]+q[1:])/2,q[-1]+(q[-1]-q[-2])/2]
 return q,(edges[1:]**3-edges[:-1]**3)/3

def run(out):
 start=time.monotonic();cases=[];row=background(25.4000254000381);checks={}
 def save():
  result=dict(claim_id='CC10_QUANTUM_SOFT_REFINEMENT_V1',checks=checks,cases=cases,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
  Path(out).write_text(json.dumps(result,indent=2)+'\n')
 for soft,dz in [(16,.025),(32,.025),(64,.025),(64,.0125)]:
  q,W=grid(soft);ev=conversion_events(row['x'],.004,q,W,angles=6,row=row);n=len(q);f=np.r_[1/(np.exp(q)+1),np.zeros(4*n)];initial=f.copy();ref=max(row['widths_over_mu'].values());ent0=entropy(f,ev.measure,ev.eta);rate=ev.rhs(f);z=0.;steps=0
  while z<1-1e-12:
   step=min(dz,1-z);f,_=symmetric_sweep(ev,f,step/ref);z+=step;steps+=1
   if steps%20==0:print('progress',soft,dz,z,flush=True)
  dn=ev.measure*(f-initial);nr0=sum(ev.measure*initial);obs=observables(ev,f)
  cases.append(dict(soft_bins=soft,step_z=dz,q=q.tolist(),final_f=f.tolist(),initial_f=initial.tolist(),final_observables=obs,initial_observables=observables(ev,initial),energy_relative_drift=float(abs(ev.energy@dn)/(ev.energy@(ev.measure*initial))),carrier_relative_drift=float(abs(sum(dn[:2*n]))/nr0),entropy_gain=entropy(f,ev.measure,ev.eta)-ent0,max_initial_gaugino_df_dtau=float(max(rate[2*n:])),shortest_initial_fill_time_tau=float(1/max(rate[2*n:]))))
  if len(cases)>1:
   prev=cases[-2]['final_observables'];cases[-1]['relative_changes_from_previous']=dict(U1_yield=obs['yields'][2]/prev['yields'][2]-1,U1_mean_p=obs['mean_p_over_mu'][2]/prev['mean_p_over_mu'][2]-1,total_gaugino_number=sum(obs['number_comoving'][2:])/sum(prev['number_comoving'][2:])-1)
  print('case',soft,dz,obs['number_comoving'],cases[-1].get('relative_changes_from_previous'),flush=True);save()
 checks.update(positive=min(c['final_observables']['min_f'] for c in cases)>-1e-13,pauli=max(c['final_observables']['max_fermion_f'] for c in cases)<=1+1e-13,energy=max(c['energy_relative_drift'] for c in cases)<1e-7,carriers=max(c['carrier_relative_drift'] for c in cases)<1e-7,entropy=min(c['entropy_gain'] for c in cases)>=0,soft_grid_change=abs(cases[2]['relative_changes_from_previous']['U1_yield'])<.1,time_step_change=abs(cases[3]['relative_changes_from_previous']['U1_yield'])<.1)
 save();print(json.dumps(checks),flush=True);assert all(checks.values())
if __name__=='__main__':run(sys.argv[1])
