"""Finite prior contract: local quantum event invariants and equilibration."""
import sys,json,time,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from quantum import *

def run(out):
 start=time.monotonic();q,W=make_grid(18);cases=[]
 for x in [2.,5.,25.4000254000381]:
  ev=conversion_events(x,.004,q,W,angles=8)
  # Each active direction has its corresponding thermal chemical constraint.
  heavy=0 if ev.masses[0]>ev.masses[1] else 1
  chemical=np.array([-.002,-.003]+[.001]*3) if heavy==0 else np.array([-.003,-.002]+[.001]*3)
  eq=equilibrium(ev,.007,chemical);audit=ev.audit(eq)
  n=len(q);carrier=np.r_[np.ones(2*n),np.zeros(3*n)]
  invariant=np.r_[np.ones(n) if heavy==0 else np.zeros(n),np.ones(n) if heavy==1 else np.zeros(n),np.ones(3*n)]
  perturb=eq.copy();perturb[:n]*=1.05;perturb[n:2*n]*=.95
  direction=ev.rhs(perturb)
  bounds=np.r_[eq[direction<0]/(-direction[direction<0]),(1-eq[(direction>0)&(ev.eta<0)])/direction[(direction>0)&(ev.eta<0)]]
  amplitude=.2*float(min(bounds));initial=eq+amplitude*direction
  f=initial.copy();oldentropy=entropy(f,ev.measure,ev.eta);entropies=[oldentropy];accepted=0;rejected=0;z=0.;step=.001;ref=max(row for row in ev.row['widths_over_mu'].values()) if heavy==0 else max(ev.row['reverse_lightest_scalar_widths_over_mu'].values());ref=max(ref,1e-30)
  while z<30:
   step=min(step,30-z)
   try:new,diag=implicit_step(ev,f,step/ref)
   except RuntimeError:
    rejected+=1;step*=.25
    if step<1e-12:raise
    continue
   f=new;z+=step;accepted+=1;entropies.append(entropy(f,ev.measure,ev.eta));step=min(step*1.3,.5)
  delta=ev.measure*(f-initial);num0=float(ev.measure@initial)
  r=dict(x=x,heavy=NAMES[heavy],equilibrium_audit=audit,initial_audit=ev.audit(initial),final_audit=ev.audit(f),initial_observables=observables(ev,initial),final_observables=observables(ev,f),equilibrium_relative_L1=float(np.sum(ev.measure*abs(f-eq))/np.sum(ev.measure*eq)),energy_relative_drift=float(abs(ev.energy@delta)/(ev.energy@(ev.measure*initial))),carrier_relative_drift=float(abs(carrier@delta)/num0),additional_invariant_relative_drift=float(abs(invariant@delta)/num0),entropy_min_step=float(min(np.diff(entropies))),entropy_gain=float(entropies[-1]-entropies[0]),accepted=accepted,rejected=rejected,max_z=z,q=q.tolist(),initial_f=initial.tolist(),equilibrium_f=eq.tolist(),final_f=f.tolist(),cutoff_dropped_empty_measure_fraction=ev.dropped_vacuum_measure/max(ev.total_vacuum_measure,1e-300))
  cases.append(r);print(x,{k:r[k] for k in ['equilibrium_relative_L1','energy_relative_drift','carrier_relative_drift','additional_invariant_relative_drift','entropy_gain','accepted','rejected']},flush=True)
 checks=dict(event_energy=max(r['equilibrium_audit']['energy_residual'] for r in cases)<1e-13,equilibrium=max(r['equilibrium_audit']['detailed_balance_relative'] for r in cases)<1e-12,positive=min(r['final_observables']['min_f'] for r in cases)>=0,pauli=max(r['final_observables']['max_fermion_f'] for r in cases)<=1,energy=max(r['energy_relative_drift'] for r in cases)<1e-7,carriers=max(r['carrier_relative_drift'] for r in cases)<1e-7,extra_invariant=max(r['additional_invariant_relative_drift'] for r in cases)<1e-7,entropy=min(r['entropy_min_step'] for r in cases)>-1e-9,equilibration=max(r['equilibrium_relative_L1'] for r in cases)<.02)
 result=dict(claim_id='CC10_QUANTUM_CONVERSION_LOCAL_V1',checks=checks,cases=cases,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite entropic Galerkin quantum 1<->2 projected leading vertices; fixed backgrounds. No neutral cascade or field feedback.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(checks),flush=True)
 assert all(checks.values())
if __name__=='__main__':run(sys.argv[1])
