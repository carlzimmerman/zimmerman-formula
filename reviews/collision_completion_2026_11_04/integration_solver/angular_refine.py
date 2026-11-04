"""Exact-angular warm continuation and collision-time step control."""
from angular_control import *

def main_refine(out):
 start=time.monotonic();prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_warm001/result.json').read_text());c=prior['case'];st=prior['state'];Y=np.array(st['Y']);q=np.array(c['q']);W=np.array(c['W']);N=st['N'];t=T0*math.exp(-N);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];orb=model.orbit(N,Y,E=st['E']);ops=[]
 for x in orb['xs']:
  d=bg.at(float(x));ops.append(exact_events(d,t,q,W,source=d['current_source']))
 ev=AveragedNumberEvents(ops,orb['weights'],orb['xs']);initial=QuantumState(ev.measure,ev.eta,Y=Y);H=model.hubble(N);n=len(q);u1=ev.by['F1_1'];charged=np.array([g['charged'] for g in ev.groups]);cases=[];checks={};result=dict(claim_id='CC10_EXACT_ANGULAR_WARM_TIME_CONTROL',checks=checks,initial_N=N,xs=ev.xs.tolist(),phase_weights=ev.phase_weights.tolist(),q=q.tolist(),W=W.tolist(),cases=cases)
 def save():
  result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
 save()
 for dN in [1e-5,5e-6]:
  state=initial.copy();history=[];case=dict(step_dN=dN,total_dN=3e-5,history=history,completed=False);cases.append(case);save()
  for j in range(round(3e-5/dN)):
   before=state.copy();dt=dN/H
   try:state,diag=implicit_step(ev,state,dt,tol=2e-8,maxiter=100)
   except RuntimeError as exc:case['failure']=str(exc);save();raise
   f,a=state.arrays();rhs=state.rhs(ev);oldcoord=np.where(state.holes==before.holes,before.Z,before.measure-before.Z);res=state.Z-oldcoord-dt*np.where(state.holes,-1.,1.)*rhs;counts=state.numbers().reshape((-1,n));cs=counts.sum(axis=1);localenergy=ev.local_energy_rates(f,a);scale=np.array([op.energy@abs(op.number_rhs(f,a)) for op in ops]);history.append(dict(step=j+1,dN=(j+1)*dN,newton=diag,min_f=float(min(f)),max_fermion_f=float(max(f[ev.eta<0])),min_fermion_availability=float(min(a[ev.eta<0])),entropy_gain=state.entropy()-initial.entropy(),coordinate_balance_relative=float(sum(abs(res))/sum(abs(state.numbers()))),local_energy_relative=float(max(abs(localenergy)/np.maximum(scale,1e-300))),charged_comoving=float(cs@charged),U1_comoving=float(cs[u1]),U1_mean_p_over_mu=float(counts[u1]@(t*q)/cs[u1])))
   print('progress',dN,j+1,history[-1],flush=True);save()
  case.update(completed=True,final_Z=state.Z.tolist(),hole_flags=state.holes.tolist(),final_number=state.numbers().tolist());save()
 coarse=np.array(cases[0]['final_number']);fine=np.array(cases[1]['final_number']);result['relative_number_L1']=float(sum(abs(coarse-fine))/sum(abs(fine)));A=cases[0]['history'][-1];B=cases[1]['history'][-1];result['relative_observable_changes']={k:B[k]/A[k]-1 for k in ['charged_comoving','U1_comoving','U1_mean_p_over_mu']};checks.update(completed=all(c['completed'] for c in cases),bounds=all(h['min_f']>=0 and h['max_fermion_f']<=1 and h['min_fermion_availability']>0 for c in cases for h in c['history']),entropy=all(h['entropy_gain']>=0 for c in cases for h in c['history']),physical_number_balance=max(h['coordinate_balance_relative'] for c in cases for h in c['history'])<1e-8,local_energy=max(h['local_energy_relative'] for c in cases for h in c['history'])<1e-11,step_control=result['relative_number_L1']<1e-4);save();assert all(checks.values())
if __name__=='__main__':main_refine(sys.argv[1])
