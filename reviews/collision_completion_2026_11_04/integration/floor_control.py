"""Physical number-floor sensitivity at the actual fresh exact checkpoint."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from angular_fast import averaged_exact_events
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0
from protocol_floor import QuantumState,implicit_step

def main(output):
 start=time.monotonic();prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_fresh_exact001/result.json').read_text());old=prior['state'];q=np.array(prior['case']['q']);W=np.array(prior['case']['W']);N=old['N'];bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=old['J0'];model.last_x=old['xmid'];Y=np.array(old['Y']);state=QuantumState(model.measure,model.eta,Z=old['Z'],holes=old['hole_flags']);orb=model.orbit(N,Y,J=prior['case']['history'][-1]['action']);ev=averaged_exact_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W);dt=5e-5/model.hubble(N);rows=[];final=[]
 for floor in (1e-14,1e-13,1e-12):
  before=time.monotonic();nextstate,info=implicit_step(ev,state,dt,tol=2e-8,number_floor=floor);num=nextstate.numbers();f,a=nextstate.arrays();res=num-Y-dt*nextstate.rhs(ev);rates=np.array([local.energy@nextstate.rhs(local) for local in ev.local_events]);gross=nextstate.gross(ev);den=max(float(max(ev.energy))*sum(gross),1e-300);rows.append(dict(number_floor=floor,newton=info,runtime=time.monotonic()-before,physical_balance_L1=float(sum(abs(res))),phase_energy_relative=float(max(abs(rates))/den),entropy_change=nextstate.entropy()-state.entropy(),min_f=float(min(f)),max_fermion_f=float(max(f[ev.eta<0])),total_number=float(sum(num)),charged_number=float(num.reshape(model.ns,model.n).sum(axis=1)@model.charged)));final.append(num)
 diff=[float(sum(abs(num-final[0]))/sum(abs(final[0]))) for num in final];checks=dict(all_steps=len(rows)==3,bounds=all(x['min_f']>=0 and x['max_fermion_f']<=1 for x in rows),entropy=all(x['entropy_change']>=-1e-10 for x in rows),phase_energy=all(x['phase_energy_relative']<1e-12 for x in rows),physical_balance=all(x['physical_balance_L1']<1e-10 for x in rows),floor_sensitivity=max(diff)<1e-8)
 out=dict(claim_id='CC10_EMPTY_NUMBER_FLOOR_CONTROL',checks={k:bool(v) for k,v in checks.items()},initial_N=N,dN=5e-5,rows=rows,relative_L1_floor_differences=diff,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual fixedoperator freshcheckpoint step and empty-number residual floor sensitivity. Hole coordinates remain explicit; no state clipping. This is numerical error control, not continuum convergence or physical common history.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
