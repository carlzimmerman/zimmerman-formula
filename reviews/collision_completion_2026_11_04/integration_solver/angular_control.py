"""Actual warm exact-angular multistep, explicit Pauli availability control."""
from control_v1 import ROOT,ConsistentVertexBackground,GenericOrbit,T0
from protocol_holes import QuantumState,implicit_step
from protocol_average import AveragedNumberEvents
from angular_exact import exact_events
import sys,json,time,resource,math
from pathlib import Path
import numpy as np

def main(out):
 start=time.monotonic();prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_warm001/result.json').read_text());c=prior['case'];st=prior['state'];Y=np.array(st['Y']);q=np.array(c['q']);W=np.array(c['W']);N=st['N'];t=T0*math.exp(-N);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];orb=model.orbit(N,Y,E=st['E']);locals=[]
 for x in orb['xs']:
  d=bg.at(float(x));locals.append(exact_events(d,t,q,W,source=d['current_source']))
 ev=AveragedNumberEvents(locals,orb['weights'],orb['xs']);state=QuantumState(ev.measure,ev.eta,Y=Y);initial=state.copy();steps=[];checks={};H=model.hubble(N);n=len(q);u1=ev.by['F1_1'];sm=2*math.pi**2/45*106.75*(t/.02)**3
 def metrics(s):
  counts=s.numbers().reshape((-1,n));cs=counts.sum(axis=1);charged=np.array([g['charged'] for g in ev.groups]);return dict(charged_comoving=float(cs@charged),U1_comoving=float(cs[u1]),U1_yield=float(cs[u1]*t**3/sm),U1_mean_p_over_mu=float(counts[u1]@(t*q)/cs[u1]))
 result=dict(claim_id='CC10_EXACT_ANGULAR_WARM_MULTISTEP',checks=checks,initial_N=N,q=q.tolist(),W=W.tolist(),xs=ev.xs.tolist(),phase_weights=ev.phase_weights.tolist(),initial_metrics=metrics(state),steps=steps,scope='Two successive fixed actual8phase warmorbit collisionstepsdN1e-6 each, exactangular25groupFFS/SSS, explicitPauli holes. Notcoupledfieldorphaseconvergence.',runtime_seconds=0.,peak_rss_bytes=0)
 def save():
  result['runtime_seconds']=time.monotonic()-start;result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;Path(out).write_text(json.dumps(result,indent=2)+'\n')
 save()
 for j in range(2):
  before=state.copy();dN=1e-6;dt=dN/H;stepstart=time.monotonic()
  try:state,diag=implicit_step(ev,state,dt,tol=2e-8,maxiter=100)
  except RuntimeError as exc:result['failure']=str(exc);save();raise
  f,a=state.arrays();rhs=state.rhs(ev);oldcoord=np.where(state.holes==before.holes,before.Z,before.measure-before.Z);sign=np.where(state.holes,-1.,1.);res=state.Z-oldcoord-dt*sign*rhs;energy=ev.local_energy_rates(f,a);scales=np.array([np.dot(abs(op.energy),abs(op.number_rhs(f,a))) for op in locals]);relative_energy=float(max(abs(energy)/np.maximum(scales,1e-300)));steps.append(dict(step=j+1,dN=(j+1)*dN,newton=diag,runtime_seconds=time.monotonic()-stepstart,minimum_f=float(min(f)),maximum_fermion_f=float(max(f[ev.eta<0])),minimum_fermion_availability=float(min(a[ev.eta<0])),entropy_change=state.entropy()-initial.entropy(),coordinate_balance_L1=float(sum(abs(res))),coordinate_balance_relative=float(sum(abs(res))/sum(abs(state.numbers()))),local_energy_rates=energy.tolist(),max_local_relative_energy_rhs=relative_energy,forward_omission=ev.forward_omission(f),metrics=metrics(state),final_Z=state.Z.tolist(),hole_flags=state.holes.tolist()))
  print('step',j+1,{k:v for k,v in steps[-1].items() if k not in ('final_Z','hole_flags')},flush=True);save()
 checks.update(completed=len(steps)==2,physical_bounds=all(s['minimum_f']>=0 and s['maximum_fermion_f']<=1 and s['minimum_fermion_availability']>0 for s in steps),entropy=all(s['entropy_change']>=0 for s in steps),physical_number_balance=max(s['coordinate_balance_relative'] for s in steps)<1e-8,local_energy=max(s['max_local_relative_energy_rhs'] for s in steps)<1e-11);save();assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
