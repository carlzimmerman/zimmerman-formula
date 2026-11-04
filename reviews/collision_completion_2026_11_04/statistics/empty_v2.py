"""Bounded physical empty-bath run; partial progress is saved after each case."""
import sys,json,time,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from quantum_v2 import *

def run(out):
 start=time.monotonic();q,W=make_grid(20);cases=[];checks={}
 def save():
  result=dict(claim_id='CC10_PHYSICAL_EMPTY_CONVERSION_V2',checks=checks,cases=cases,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,solver='symmetric event-local implicit scalar extent; full quantum RHS, finite splitting error')
  Path(out).write_text(json.dumps(result,indent=2)+'\n')
 for x,step in [(5.,.1),(25.4000254000381,.1),(25.4000254000381,.05)]:
  ev=conversion_events(x,.004,q,W,angles=6);n=len(q);f=np.r_[1/(np.exp(q)+1),np.zeros(4*n)];initial=f.copy();ref=max(ev.row['widths_over_mu'].values());history=[];z=0.;accepted=0
  initial_rate=ev.rhs(initial);rate_max=float(max(initial_rate[2*n:]));H=math.sqrt(math.pi**2*106.75/90)*2e6*.004**2/(2.435e18*.02**2)
  while z<1-1e-12:
   dz=min(step,1-z);f,diag=symmetric_sweep(ev,f,dz/ref);z+=dz;accepted+=1
   history.append(dict(z=z,N_equivalent=z*H/ref,observables=observables(ev,f)))
   print('progress',x,step,z,history[-1]['observables']['number_comoving'],flush=True)
  delta=ev.measure*(f-initial);n0=float(sum(ev.measure*initial));ob=observables(ev,f)
  cases.append(dict(x=x,Tc=.004,step_z=step,q=q.tolist(),initial_f=initial.tolist(),final_f=f.tolist(),initial_observables=observables(ev,initial),final_observables=ob,history=history,accepted=accepted,energy_relative_drift=float(abs(ev.energy@delta)/(ev.energy@(ev.measure*initial))),carrier_relative_drift=float(abs(sum(delta[:2*n]))/n0),extra_invariant_relative_drift=float(abs(sum(delta[:n])+sum(delta[2*n:]))/n0),entropy_gain=entropy(f,ev.measure,ev.eta)-entropy(initial,ev.measure,ev.eta),final_audit=ev.audit(f),max_initial_gaugino_df_dtau=rate_max,shortest_initial_fill_time_tau=1/rate_max,initial_quantum_filling_over_H=rate_max/H))
  save()
 checks.update(positive=min(c['final_observables']['min_f'] for c in cases)>-1e-13,pauli=max(c['final_observables']['max_fermion_f'] for c in cases)<=1+1e-13,energy=max(c['energy_relative_drift'] for c in cases)<1e-7,carriers=max(c['carrier_relative_drift'] for c in cases)<1e-7,entropy=min(c['entropy_gain'] for c in cases)>=0)
 coarse=np.array(cases[1]['final_f']);fine=np.array(cases[2]['final_f']);cases[2]['step_comparison_relative_number_L1']=float(np.sum(ev.measure*abs(fine-coarse))/np.sum(ev.measure*fine));checks['step_comparison']=cases[2]['step_comparison_relative_number_L1']<.15
 save();print(json.dumps(checks),flush=True);assert all(checks.values())
if __name__=='__main__':run(sys.argv[1])
