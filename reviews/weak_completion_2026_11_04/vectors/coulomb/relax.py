"""Finite quantum conservative self-Coulomb relaxation of an actual cold packet."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'))
import numpy as np
from elastic_builder_v2 import grid,screening,event_arrays_chunked,make_events
from log_number import QuantumState,implicit_step

def main(out):
 start=time.monotonic();stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];ker=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/kernels.json').read_text());probe=json.loads((HERE.parent/'run_coulomb003/result.json').read_text());edges=np.array(stage['q_edges']);q,W,cells=grid(edges,1);f0=np.full(len(q),1e-45);f0[cells>=0]=2*np.array(stage['final_fS'])[cells[cells>=0]];T=old['history'][-1]['Tc_over_mu'];x=old['history'][-1]['x_minimum'];m=.003/2*math.sqrt(x*x+2/(31*.003));H=probe['cases'][1]['H_mu'];md=screening(q,W,f0,T,m);arr=event_arrays_chunked(q,W,T,m,md,incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.,diagnostic_f=f0);ev=make_events(arr);state=QuantumState(ev.measure,ev.eta,Z=ev.measure*f0,holes=np.zeros(len(q),bool));Y0=state.numbers();K=arr['kinetic_energy'];en=arr['full_energy'];initialN=float(sum(Y0));initialK=float(K@Y0);oldkernel=np.array(ker['K'][-1]);rows=[];ends=[];partial=True;reason='started';checks={};local={}
 def describe(st):
  f,a=st.arrays();Y=st.numbers();binY=np.bincount(cells[cells>=0],weights=Y[cells>=0],minlength=len(edges)-1);percharge=binY/2;loss=float(T**3*(percharge@oldkernel@percharge)/(H*sum(percharge)));pressure=float(T**3/3*np.sum(Y*(T*q)**2/en));force=float(T**3*.003**2*x/4*np.sum(Y/en));return dict(f=f.tolist(),Y=Y.tolist(),number=float(sum(Y)),kinetic_energy=float(K@Y),pressure=pressure,force=force,entropy=st.entropy(),annihilation_fractional_loss_over_H=loss,relative_L1_shape=float(sum(abs(Y-Y0))/initialN),number_relative_drift=float(sum(Y)/initialN-1),kinetic_energy_relative_drift=float(K@Y/initialK-1),max_f=float(f.max()))
 initial=describe(state)
 def save():Path(out).write_text(json.dumps(dict(claim_id='CC11_ACTUAL_COLD_SELF_COULOMB_RELAXATION',partial=partial,reason=reason,x=x,Tc=T,H_mu=H,q=q.tolist(),W=W.tolist(),cells=cells.tolist(),screening_masses_mu=np.sqrt(md).tolist(),events=len(ev.coefficient),initial=initial,local_controls=local,rows=rows,endpoints=ends,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualCC10memoryfinalscalarshape, fixedcoldpoleN and screen, quantumselfC-Cscreened directt kernel over0.1Hubbletime. Number andphysicalkineticenergyconserved; evolvingmassiveparticlesnotradiation. OldannihilationK isdiagnosticfunctionalonly, noannihilationsink applied. Finitegridandtimerefinecontrolsreported; nofullcoolingorviabilityclaim.'),indent=2)+'\n')
 save()
 try:
  feq=1/np.expm1(K/(T*T/m)*.1+2);r=ev.number_rhs(feq);gross=ev.number_gross(feq);rng=np.random.default_rng(19);h=rng.normal(size=len(q))*f0*ev.measure;ep=1e-5;num=(ev.number_rhs(f0+ep*h/ev.measure)-ev.number_rhs(f0-ep*h/ev.measure))/(2*ep);ana=ev.number_jacobian(f0)@h;local.update(DB_relative=float(sum(abs(r))/sum(gross)),Jacobian_relative=float(np.linalg.norm(num-ana)/np.linalg.norm(num)),entropy_rate=float(ev.entropy_production(f0)),number_rhs_relative=float(abs(sum(ev.number_rhs(f0)))/sum(abs(ev.number_rhs(f0)))),kinetic_rhs_relative=float(abs(K@ev.number_rhs(f0))/sum(abs(K*ev.number_rhs(f0)))));save()
  for steps in (4,8):
   st=state.copy();dt=.1/(steps*H);begin=time.monotonic()
   for step in range(steps):
    if time.monotonic()-start>210:reason='durable_wall_checkpoint';save();return
    oldst=st;st,info=implicit_step(ev,st,dt,tol=2e-8,number_floor=1e-14);r=describe(st);res=st.numbers()-oldst.numbers()-dt*st.rhs(ev);r.update(steps=steps,step=step+1,deltaN_equivalent=(step+1)*.1/steps,solver=info,number_balance_L1=float(sum(abs(res))));rows.append(r);save()
   r=describe(st);r.update(steps=steps,runtime_seconds=time.monotonic()-begin,annihilation_relative_change=r['annihilation_fractional_loss_over_H']/initial['annihilation_fractional_loss_over_H']-1);ends.append(r);print(steps,{k:v for k,v in r.items() if k not in ('f','Y')},flush=True);save()
  diff=float(sum(abs(np.array(ends[0]['Y'])-ends[1]['Y']))/initialN);checks=dict(DB=bool(local['DB_relative']<1e-11),Jacobian=bool(local['Jacobian_relative']<1e-5),energy=bool(max(abs(r['kinetic_energy_relative_drift']) for r in rows)<1e-6),number=bool(max(abs(r['number_relative_drift']) for r in rows)<1e-7),entropy=bool(all(r['entropy']>=initial['entropy'] for r in rows)),time_shape=bool(diff<.01),actual_hole_fill=bool(ends[-1]['relative_L1_shape']>1e-5));local['time_refinement_L1_relative']=diff;partial=False;reason='target_reached';save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
