"""Fresh or exact-prefix continuation of the matched-energy 25-group benchmark.

Each segment is bounded and saves its full state after accepted steps. A
global fresh claim requires ancestry back to the N=0 input with work=0.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
for folder in ('cascades','integration'):sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04'/folder))
sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/vectors'))
from transport_v3 import VectorFactory
VECTOR_FACTORY=VectorFactory(ROOT/'reviews/weak_completion_2026_11_04/vectors/run_table003/result.json')
def averaged_exact_events(bg,xs,weights,t,q,W):return VECTOR_FACTORY.averaged_events(bg,xs,weights,t,q,W,angle_order=2)
from common import CommonBackground as ConsistentVertexBackground
sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/energy'))
from precise_common import PreciseCommonOrbit as GenericOrbit
from common import T0
from split_energy_v7 import QuantumState,step

def main(output,prior_path,target='0.0021690179772784167',stepmax='.0002',phase='8'):
 start=time.monotonic();target=float(target);stepmax=float(stepmax);prior=json.loads(Path(prior_path).read_text());old=prior['state'];case=prior['case'];q=np.array(case['q']);W=np.array(case['W']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,int(phase));model.J0=old['J0'];model.last_x=old['xmid'];state=QuantumState(model.measure,model.eta,Z=old['Z'],holes=old['hole_flags']);N=float(old['N']);J=float(old.get('J',old['J0']));orb=model.orbit(N,state.numbers(),J=J);E0=float(old.get('matched_initial_energy',orb['E']));work=float(old.get('matched_independent_work',0.));startN=N;initialY=np.array(old['initialY']);gas0=float(old['gas0']);history=[];accepted=rejected=0;reasons={};h=float(old.get('matched_last_step',stepmax));reason='requested target reached';maximum_energy_ratio=float(case.get('max_energy_error_over_excitation',0.));max_outer=0;max_balance=0.;max_phase_energy=0.;max_population_iterations=0;minimum_f=0.;maximum_fermion=0.;minimum_entropy=0.;maximum_guess=0.
 if N!=0 and 'matched_initial_energy' not in old:raise RuntimeError('Nonfresh ancestor without matched independent ledger is forbidden')
 def record():
  row=model.summary(N,state.numbers(),orb);exc=float(orb['E']-orb['minimum']);residual=float(orb['E']+work-E0);row.update(orbital_excitation=exc,independent_work=work,energy_work_residual_mu4=residual,energy_work_residual_over_gas0=residual/gas0,energy_work_residual_over_excitation=residual/max(exc,1e-300));history.append(row)
 def save():
  result=dict(claim_id='CC11_FRESH_JOINT_VECTOR_ENERGY_HISTORY',partial=N<target-1e-13,checks=dict(target_reached=N>=target-1e-13,positive=minimum_f>=0,Pauli=maximum_fermion<=1,entropy=minimum_entropy>=-1e-9,independent_energy_work=maximum_energy_ratio<.01),case=dict(reason=reason,accepted=accepted,rejected=rejected,rejection_reasons=reasons,history=history,q=q.tolist(),W=W.tolist(),stepmax=stepmax,phase_nodes=int(phase),initial_N=startN,target_N=target,max_energy_error_over_excitation=maximum_energy_ratio,max_outer_iterations=max_outer,max_population_iterations=max_population_iterations,max_number_balance_L1=max_balance,max_phase_collision_energy_relative=max_phase_energy),state=dict(Y=state.numbers().tolist(),Z=state.Z.tolist(),hole_flags=state.holes.tolist(),N=N,J=J,E=orb['E'],J0=model.J0,initialY=initialY.tolist(),gas0=gas0,xmid=orb['xmid'],matched_initial_energy=E0,matched_independent_work=work,matched_last_step=h,ancestry_checkpoint=str(prior_path)),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Fresh30groupvector+scalar+fermion1<->2historywithpolarizedvectors, matchedmidACTIONendpointenergyconservationandindependentSimpsonFRWwork. NoelasticCoulomborloopdecaysinthisearlywarmrun; finitephase/momentum/tableaccuracy, notcoldcosmologicalverdict.')
  Path(output).write_text(json.dumps(result,indent=2)+'\n');return result
 record();save()
 while N<target-1e-13:
  if time.monotonic()-start>145:reason='bounded checkpoint before new nonlinear step';break
  h=min(h,stepmax,target-N);before=time.monotonic()
  try:
   ns,Jn,on,dw,info=step(model,bg,averaged_exact_events,N,state,J,h,geometry='midpoint',max_outer=8,outer_tol=2e-5)
   delta=float(sum(abs(ns.numbers()-state.numbers()))/max(sum(abs(state.numbers())),1e-300))
   if delta>.1:raise RuntimeError('population change exceeds .1')
   if abs(math.log(Jn/J))>.7:raise RuntimeError('action logarithmic change exceeds .7')
   exc=float(on['E']-on['minimum']);residual=float(on['E']+work+dw-E0);ratio=abs(residual)/max(exc,1e-300)
   if ratio>.01:raise RuntimeError('independent work error exceeds .01 excitation')
   col=info['collision']
   if col['entropy_change']<-1e-9:raise RuntimeError('entropy decreased')
   minimum_f=min(minimum_f,col['min_f']);maximum_fermion=max(maximum_fermion,col['max_fermion_f']);minimum_entropy=min(minimum_entropy,col['entropy_change']);maximum_energy_ratio=max(maximum_energy_ratio,ratio);max_outer=max(max_outer,len(col['outer_iterations']));max_balance=max(max_balance,col['physical_number_balance_L1']);max_phase_energy=max(max_phase_energy,col['local_energy_relative']);max_population_iterations=max(max_population_iterations,max(a['population_newton']['iterations'] for a in col['outer_iterations']));N+=h;J=Jn;state=ns;orb=on;model.last_x=orb['xmid'];work+=dw;accepted+=1;record();save();print('accepted',N,'h',h,'J',J,'exc',exc,'energy_ratio',ratio,'outer',len(col['outer_iterations']),'stepsec',time.monotonic()-before,flush=True);h=min(stepmax,h*1.4)
  except RuntimeError as err:
   rejected+=1;reasons[str(err)]=reasons.get(str(err),0)+1;h*=.25;print('rejected',str(err),'newh',h,flush=True);save()
   if h<1e-11:reason=str(err);break
  if time.monotonic()-start>205:reason='bounded checkpoint';break
 result=save();print(json.dumps(dict(checks=result['checks'],reason=reason,N=N,accepted=accepted,rejected=rejected,runtime_seconds=result['runtime_seconds'])),flush=True)
 if N>=target-1e-13:assert all(result['checks'].values())
if __name__=='__main__':main(*sys.argv[1:])
