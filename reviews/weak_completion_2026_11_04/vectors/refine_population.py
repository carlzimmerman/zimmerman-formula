import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'))
import numpy as np
from common import CommonBackground,CommonOrbit
from transport_v3 import VectorFactory
from log_number import QuantumState,implicit_step

def main(out):
 start=time.monotonic();d=json.loads((HERE/'run_population002/result.json').read_text());q=np.array(d['q']);W=np.array(d['W']);x,N,t=d['x'],d['N'],d['Tc'];bg=CommonBackground();model=CommonOrbit(bg,q,W,8);fac=VectorFactory(HERE/'run_table003/result.json');rows=[];partial=True;reason='started';checks={};reference=d['endpoints']['full'];total=6*d['step_mu_inverse']
 def save():Path(out).write_text(json.dumps(dict(partial=partial,reason=reason,x=x,N=N,Tc=t,rows=rows,reference=dict(charged_number=reference['charged_number'],vector_number=reference['vector_number'],photino_number=reference['photino_number'],gas_force=reference['gas_force'],vector_force=reference['vector_force']),checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Same conditional fixed warm full30 transport; separate timestep, segmented angular quadrature, and empty-vector seed sensitivities. All quantities at three vector lifetimes; no coupled history claim.'),indent=2)+'\n')
 save()
 try:
  for name,steps,order,seed in [('halfdt',12,2,1e-35),('angle4',6,4,1e-35),('seed25',6,2,1e-25),('seed45',6,2,1e-45)]:
   ev=fac.full_events(bg.at(x),t,q,W,angle_order=order);Z=np.array(d['initial']['Z']);Z[25*len(q):]=ev.measure[25*len(q):]*seed;st=QuantumState(ev.measure,ev.eta,Z=Z,holes=d['initial']['hole_flags']);initial=st.copy();maxres=0;maxed=0;maxit=0;begin=time.monotonic();dt=total/steps
   for i in range(steps):
    if time.monotonic()-start>215:reason='durable_wall_checkpoint';save();return
    old=st;st,info=implicit_step(ev,st,dt,tol=2e-8,number_floor=1e-14);r=st.numbers()-old.numbers()-dt*st.rhs(ev);maxres=max(maxres,float(sum(abs(r))));maxed=max(maxed,float(abs(ev.energy@(st.numbers()-initial.numbers()))/(ev.energy@initial.numbers())));maxit=max(maxit,info['iterations'])
   Y=st.numbers();num=Y.reshape(30,len(q)).sum(axis=1);gas=model.gas(x,N,Y);f,a=st.arrays();row=dict(name=name,steps=steps,angle_order=order,seed=seed,charged_number=float(num@model.charged),vector_number=float(num[25:].sum()),photino_number=float(num[23]),gas_force=float(gas['force'][0]),vector_force=float(gas['force_by'][0,25:].sum()),max_number_balance_L1=maxres,max_relative_energy_drift=maxed,entropy_change=st.entropy()-initial.entropy(),max_fermion_f=float(f[ev.eta<0].max()),max_Newton_iterations=maxit,runtime_seconds=time.monotonic()-begin)
   row['relative_to_coarse']={k:row[k]/reference[k]-1 for k in ('charged_number','vector_number','photino_number','gas_force','vector_force')};rows.append(row);print(row,flush=True);save()
  partial=False;reason='target_reached';checks=dict(energy=bool(all(r['max_relative_energy_drift']<1e-10 for r in rows)),balance=bool(all(r['max_number_balance_L1']<1e-10 for r in rows)),entropy=bool(all(r['entropy_change']>=0 for r in rows)),bounds=bool(all(r['max_fermion_f']<=1 for r in rows)),angle4=bool(max(abs(v) for v in rows[1]['relative_to_coarse'].values())<1e-4),seed=bool(max(abs(v) for r in rows[2:] for v in r['relative_to_coarse'].values())<1e-5));save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
