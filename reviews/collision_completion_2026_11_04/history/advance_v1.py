"""Conditional all25 action/number flow, centered covariance and independent work.

Angular integration is analytic within every finite momentum stencil segment.
The energy ledger integrates actual FRW work, not the reconstructed energy change.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from angular_fast import averaged_exact_events as averaged_events
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/integration'))
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/integration_solver'))
from consistent_background import ConsistentVertexBackground
from solver_floor import QuantumState,implicit_step
from generic_orbit import GenericOrbit,T0

def expansion_work(orb):return 3*float(orb['weights']@(orb['kin2']+orb['gas']['rho']+orb['gas']['pressure']))
def centered_covariance(ev,state):
 C=np.array([state.rhs(local) for local in ev.local_events]);avg=ev.phase_weights@C
 ee=np.array([local.energy for local in ev.local_events]);de=ee-ev.energy_average[None,:]
 return ev.t**3*float(np.sum(ev.phase_weights[:,None]*de*(C-avg))),avg

def main(output,prior_path,Nend='0.01',stepmax='0.00005',reference_path=None):
 start=time.monotonic();Nend=float(Nend);stepmax=float(stepmax);prior=json.loads(Path(prior_path).read_text());old=prior['state'];case=prior['case'];q=np.array(case['q']);W=np.array(case['W']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=old['J0'];model.last_x=old['xmid'];state=QuantumState(model.measure,model.eta,Z=old['Z'],holes=old['hole_flags']) if 'Z' in old else QuantumState(model.measure,model.eta,Y=np.array(old['Y']));N=old['N'];J=case['history'][-1]['action'];orb=model.orbit(N,state.numbers(),J=J);gas0=old['gas0'];reference=json.loads(Path(reference_path).read_text()) if reference_path else prior;E0=old.get('energy_reference_E',reference['state']['E']);work=old.get('independent_work',gas0*case['history'][-1].get('independent_energy_work_residual',0.)+E0-orb['E']);history=[];accepted=rejected=0;reasons={};step=stepmax;maxerr=0.;maxledger=0.;maxentropy=0.;initialY=np.array(old['initialY']);max_iterations=0;max_balance=0.;max_rounding=0.;start_N=N;solver_records=[]
 def record():
  d=model.summary(N,state.numbers(),orb);d.update(independent_energy_work_residual=(orb['E']+work-E0)/gas0,charged_fraction=float(state.numbers().reshape(model.ns,model.n).sum(axis=1)@model.charged/(initialY.reshape(model.ns,model.n).sum(axis=1)@model.charged)))
  history.append(d)
 record();reason='target reached'
 def save(partial):
  r=dict(claim_id='CC10_CORRECTED_HISTORY_WITH_NUMBER_FLOOR',partial=partial,checks=dict(target_reached=N>=Nend-1e-13,positive=bool(min(state.arrays()[0])>=0),fermion_bounds=bool(max(state.arrays()[0][model.eta<0])<=1),independent_energy_work=maxledger<.001,entropy=maxentropy<1e-9),case=dict(reason=reason,accepted=accepted,rejected=rejected,rejection_reasons=reasons,history=history,initial_N=start_N,number_floor=1e-13,max_Newton_iterations=max_iterations,max_number_balance_residual_L1=max_balance,max_roundoff_allowance_L1=max_rounding,q=q.tolist(),W=W.tolist(),phase_nodes=8,angles='analytic segment moments',maximum_predictor_corrector_logJ_error=maxerr,maximum_independent_energy_work_error=maxledger),state=dict(Y=state.numbers().tolist(),Z=state.Z.tolist(),hole_flags=state.holes.tolist(),N=N,J=J,E=orb['E'],J0=model.J0,initialY=initialY.tolist(),gas0=gas0,xmid=orb['xmid'],energy_reference_E=E0,independent_work=work,last_step=step,ancestry_checkpoint=str(prior_path),number_floor=1e-13),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Analytic-angular finite momentum projected25group tree inverse quantum network with commonmassgasforce and independent FRW work. Centered covariance removes cancellation atsmallamplitude. The angular integral is exact within its finite energy projection; radialmomentum/phase convergence is unresolved; no physical cosmologicalabundance or four-state memory included.')
  Path(output).write_text(json.dumps(r,indent=2)+'\n');return r
 save(True)
 while N<Nend-1e-13:
  step=min(step,stepmax,Nend-N)
  try:
   t=T0*math.exp(-N);H=model.hubble(N+step/2);ev=averaged_events(bg,orb['xs'],orb['weights'],t,q,W);cov,C=centered_covariance(ev,state);k0=-3+cov/(orb['omega']*J*model.hubble(N));nextstate,info=implicit_step(ev,state,step/H,tol=2e-8,number_floor=1e-13);max_iterations=max(max_iterations,info['iterations']);max_balance=max(max_balance,info['absolute_coordinate_residual_L1']);max_rounding=max(max_rounding,info['gross_roundoff_allowance_L1']);Yn=nextstate.numbers();expo=step*k0
   if not -400<expo<100:raise RuntimeError('action predictor exponent outside retained numericrange')
   Jp=J*math.exp(expo);pred=model.orbit(N+step,Yn,J=Jp);ep=averaged_events(bg,pred['xs'],pred['weights'],t*math.exp(-step),q,W);covp,Cp=centered_covariance(ep,nextstate);k1=-3+covp/(pred['omega']*Jp*model.hubble(N+step));err=abs(step*(k1-k0)/2)
   if err>.02:raise RuntimeError('action predictor-corrector error')
   if sum(abs(Yn-state.numbers()))/sum(state.numbers())>.04:raise RuntimeError('numberchange control')
   Jn=J*math.exp(step*(k0+k1)/2);neworb=model.orbit(N+step,Yn,J=Jn);dw=step*(expansion_work(orb)+expansion_work(neworb))/2;dS=nextstate.entropy()-state.entropy()
   if dS<-1e-9:raise RuntimeError('entropy decreased')
   ledger=abs((neworb['E']+work+dw-E0)/gas0)
   if ledger>.001:raise RuntimeError('independent energywork tolerance')
   N+=step;J=Jn;state=nextstate;orb=neworb;model.last_x=orb['xmid'];work+=dw;accepted+=1;maxerr=max(maxerr,err);maxledger=max(maxledger,ledger);maxentropy=max(maxentropy,-dS)
   if accepted==1 or N-history[-1]['N']>1e-4 or N>=Nend-1e-13:record()
   if accepted==1 or accepted%5==0:save(True)
   step=min(stepmax,step*min(1.5,max(.6,.9*math.sqrt(.02/max(err,1e-14)))))
  except RuntimeError as e:
   rejected+=1;reasons[str(e)]=reasons.get(str(e),0)+1;step*=.25
   if step<1e-12:reason=str(e);break
  if time.monotonic()-start>205:reason='bounded checkpoint';break
  if accepted>2000:reason='step count checkpoint';break
 if history[-1]['N']!=N:record()
 r=save(False);print(json.dumps(dict(checks=r['checks'],reason=reason,last=history[-1],accepted=accepted,rejected=rejected,runtime_seconds=r['runtime_seconds'])));assert all(r['checks'].values()),r['checks']
if __name__=='__main__':main(*sys.argv[1:])
