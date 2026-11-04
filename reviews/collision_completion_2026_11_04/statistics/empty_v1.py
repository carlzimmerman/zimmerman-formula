"""Physical frozen FD F, exactly empty C and all gauginos: quantum bath."""
import sys,json,time,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from quantum import *

def run(out):
 start=time.monotonic();q,W=make_grid(20);cases=[]
 for x in [5.,25.4000254000381]:
  ev=conversion_events(x,.004,q,W,angles=8);n=len(q)
  f=np.r_[1/(np.exp(q)+1),np.zeros(4*n)];initial=f.copy()
  H=math.sqrt(math.pi**2*106.75/90)*2e6*.004**2/(2.435e18*.02**2)
  ref=max(ev.row['widths_over_mu'].values());z=0.;step=1e-5;accepted=0;rejected=0;history=[]
  while z<10:
   step=min(step,10-z)
   try:new,diag=implicit_step(ev,f,step/ref)
   except RuntimeError as exc:
    rejected+=1;step*=.25
    if step<1e-15:raise RuntimeError(str(exc)+' z='+str(z)+' step='+str(step))
    continue
   f=new;z+=step;accepted+=1
   if accepted==1 or len(history)==0 or z-history[-1]['z']>.2 or z>=10:
    history.append(dict(z=z,N_equivalent=z*H/ref,observables=observables(ev,f)))
   step=min(step*1.4,.15)
  delta=ev.measure*(f-initial);n0=float(sum(ev.measure*initial));ob=observables(ev,f)
  cases.append(dict(x=x,Tc=.004,q=q.tolist(),initial_f=initial.tolist(),final_f=f.tolist(),initial_observables=observables(ev,initial),final_observables=ob,history=history,accepted=accepted,rejected=rejected,energy_relative_drift=float(abs(ev.energy@delta)/(ev.energy@(ev.measure*initial))),carrier_relative_drift=float(abs(sum(delta[:2*n]))/n0),extra_invariant_relative_drift=float(abs(sum(delta[:n])+sum(delta[2*n:]))/n0),entropy_gain=entropy(f,ev.measure,ev.eta)-entropy(initial,ev.measure,ev.eta),final_audit=ev.audit(f)))
  print(x,{k:cases[-1][k] for k in ['accepted','rejected','energy_relative_drift','carrier_relative_drift','extra_invariant_relative_drift','entropy_gain']},flush=True)
 checks=dict(positive=min(c['final_observables']['min_f'] for c in cases)>=0,pauli=max(c['final_observables']['max_fermion_f'] for c in cases)<=1,energy=max(c['energy_relative_drift'] for c in cases)<1e-7,carriers=max(c['carrier_relative_drift'] for c in cases)<1e-7)
 result=dict(claim_id='CC10_PHYSICAL_EMPTY_CONVERSION_V1',checks=checks,cases=cases,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(checks),flush=True);assert all(checks.values())
if __name__=='__main__':run(sys.argv[1])
