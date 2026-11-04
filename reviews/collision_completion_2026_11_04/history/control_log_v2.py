"""Independent solver equivalence at the actual corrected fresh002 state."""
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,time,math,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parent))
for path in ('cascades','integration','integration_solver','initial_solver'):
 sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04'/path))
from angular_fast import averaged_exact_events
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0
from log_number import QuantumState,implicit_step as log_step
from solver_floor import implicit_step as floor_step

def main(out):
 start=time.monotonic();prior=ROOT/'reviews/collision_completion_2026_11_04/integration/run_fresh_exact002/result.json';d=json.loads(prior.read_text());s=d['state'];q=np.array(d['case']['q']);W=np.array(d['case']['W']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=s['J0'];model.last_x=s['xmid'];state=QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);orb=model.orbit(s['N'],state.numbers(),J=d['case']['history'][-1]['action']);ev=averaged_exact_events(bg,orb['xs'],orb['weights'],T0*math.exp(-s['N']),q,W);dt=5e-5/model.hubble(s['N']);rows=[];states=[]
 for name,method,floor in [('floor',floor_step,1e-13),('log',log_step,1e-14)]:
  begin=time.monotonic();new,info=method(ev,state,dt,tol=2e-8,number_floor=floor);Y=new.numbers();rhs=new.rhs(ev);res=Y-state.numbers()-dt*rhs;f,av=new.arrays();number=Y.reshape(model.ns,model.n).sum(axis=1);local_E=[float(local.energy@new.rhs(local)) for local in ev.local_events];row=dict(solver=name,number_floor=floor,runtime_seconds=time.monotonic()-begin,info=info,physical_number_residual_L1=float(sum(abs(res))),entropy_change=new.entropy()-state.entropy(),max_local_energy_residual=float(max(abs(v) for v in local_E)),min_f=float(f.min()),max_fermion_f=float(f[ev.eta<0].max()),charged_comoving=float(number@model.charged),U1_comoving=float(number[model.by['F1_1']]),Y=Y.tolist(),Z=new.Z.tolist(),hole_flags=new.holes.tolist());rows.append(row);states.append(new);print({k:v for k,v in row.items() if k not in ('Y','Z','hole_flags')},flush=True)
 diff=float(sum(abs(states[1].numbers()-states[0].numbers()))/sum(abs(states[0].numbers())));checks=dict(bulk_equivalence=diff<1e-12,positive=all(r['min_f']>=0 for r in rows),fermion_bounds=all(r['max_fermion_f']<=1 for r in rows),physical_balance=all(r['physical_number_residual_L1']<1e-12 for r in rows),entropy=all(r['entropy_change']>=-1e-10 for r in rows),local_energy=all(r['max_local_energy_residual']<1e-20 for r in rows))
 result=dict(claim_id='CC10_HISTORY_LOG_SOLVER_EQUIVALENCE',initial_N=s['N'],dN=5e-5,rows=rows,relative_L1_difference=diff,checks={k:bool(v) for k,v in checks.items()},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual corrected fresh002 frozen-operator step. Comparison of two nonlinear solvers for the same conservative BE equation; no coupled advance or time-step convergence claim.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(result['checks'].values()),result['checks']
if __name__=='__main__':main(sys.argv[1])
