"""Actual fresh-checkpoint fixed exact-angular step: independent log route."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
for folder in ('cascades','integration','integration_solver'):sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04'/folder))
from angular_fast import averaged_exact_events
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0
from log_number import QuantumState,implicit_step

def main(out):
 start=time.monotonic();prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_fresh_exact001/result.json').read_text());st=prior['state'];q=np.array(prior['case']['q']);W=np.array(prior['case']['W']);N=st['N'];Y=np.array(st['Y']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];state=QuantumState(model.measure,model.eta,Z=st['Z'],holes=st['hole_flags']);orb=model.orbit(N,Y,J=prior['case']['history'][-1]['action']);t=T0*math.exp(-N);ev=averaged_exact_events(bg,orb['xs'],orb['weights'],t,q,W);H=model.hubble(N);dN=5e-5;checks={};rows=[];result=dict(claim_id='CC10_INITIAL_LOG_NUMBER_CONTROL_V2',checks=checks,initial_N=N,dN=dN,q=q.tolist(),W=W.tolist(),rows=rows)
 def save():
  result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
 save()
 for name,steps in [('four_quarter',4),('eight_eighth',8)]:
  current=state.copy();history=[];case=dict(name=name,completed=False,history=history);rows.append(case);save();before=time.monotonic()
  for j in range(steps):
   old=current.copy();dt=dN/steps/H
   try:current,diag=implicit_step(ev,current,dt,tol=2e-8,number_floor=1e-14)
   except RuntimeError as exc:case['failure']=str(exc);save();raise
   f,a=current.arrays();rhs=current.rhs(ev);s=np.where(current.holes,-1.,1.);oldcoords=np.where(current.holes==old.holes,old.Z,old.measure-old.Z);res=current.Z-oldcoords-dt*s*rhs;energies=np.array([local.energy@current.rhs(local) for local in ev.local_events]);gross=current.gross(ev);den=max(float(max(ev.energy))*sum(gross),1e-300);num=current.numbers();counts=num.reshape(model.ns,model.n).sum(axis=1);u1=ev.by['F1_1'];sh=2*math.pi**2/45*106.75*(t/.02)**3;conversion=t**3/sh;history.append(dict(step=j+1,newton=diag,physical_balance_L1=float(sum(abs(res))),yield_equivalent_balance_L1=float(sum(abs(res))*conversion),phase_energy_relative=float(max(abs(energies))/den),entropy_gain=current.entropy()-state.entropy(),min_f=float(min(f)),max_fermion_f=float(max(f[ev.eta<0])),charged_number=float(counts@model.charged),U1_number=float(counts[u1]),U1_yield=float(counts[u1]*conversion),U1_mean_p_over_mu=float(num.reshape(model.ns,model.n)[u1]@(t*q)/counts[u1])));print(name,j+1,history[-1],flush=True);save()
  case.update(completed=True,runtime=time.monotonic()-before,final_numbers=current.numbers().tolist(),final_Z=current.Z.tolist(),hole_flags=current.holes.tolist());save()
 A=np.array(rows[0]['final_numbers']);B=np.array(rows[1]['final_numbers']);result['relative_L1_step_difference']=float(sum(abs(A-B))/sum(abs(B)));a=rows[0]['history'][-1];b=rows[1]['history'][-1];result['relative_observable_changes']={k:b[k]/a[k]-1 for k in ['charged_number','U1_number','U1_mean_p_over_mu']};checks.update(completed=all(r['completed'] for r in rows),bounds=all(h['min_f']>=0 and h['max_fermion_f']<=1 for r in rows for h in r['history']),entropy=all(h['entropy_gain']>=0 for r in rows for h in r['history']),local_energy=max(h['phase_energy_relative'] for r in rows for h in r['history'])<1e-12,physical_balance=max(h['physical_balance_L1'] for r in rows for h in r['history'])<1e-14,rare_budget=max(h['newton']['nonrounding_number_floor_budget_L1'] for r in rows for h in r['history'])<=1e-18,step_control=result['relative_L1_step_difference']<1e-3);save();assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
