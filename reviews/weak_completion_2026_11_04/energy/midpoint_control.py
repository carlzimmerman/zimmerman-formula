"""Bounded conditional-positive midpoint control, separate from fresh BE runs."""
from one_step import *
from split_energy_v7 import step as midpoint_step,MidpointNumberOperator,implicit_step
from scipy.sparse import csr_matrix

class LinearDecay:
 def __init__(self):self.measure=np.ones(2);self.eta=np.ones(2);self.energy=np.ones(2)
 def number_rhs(self,f,availability=None):return np.array([-f[0],f[0]])
 def number_jacobian(self,f,availability=None):return csr_matrix([[-1.,0.],[1.,0.]])
 def number_gross(self,f,availability=None):return np.full(2,f[0])

def main_mid(out):
 start=time.monotonic();toy=[];ev=LinearDecay();old=QuantumState(ev.measure,ev.eta,Y=np.array([1.,0.]))
 for z in [1.,4.]:
  wrapped=MidpointNumberOperator(ev,old)
  try:
   ns,info=implicit_step(wrapped,old,z,tol=2e-8,maxiter=30,number_floor=1e-14);toy.append(dict(z=z,completed=True,new_numbers=ns.numbers().tolist(),expected_parent=(1-z/2)/(1+z/2),newton=info))
  except RuntimeError as exc:toy.append(dict(z=z,completed=False,expected_parent=(1-z/2)/(1+z/2),rejection=str(exc)))
 d,bg,model,state,N,J,orb=load(ROOT/'reviews/weak_completion_2026_11_04/energy/run_fresh_fine007/result.json');rows=[];checks={};total=5e-5;result=dict(claim_id='CC11_CONDITIONAL_POSITIVE_MIDPOINT_CONTROL',initial_N=N,total_dN=total,linear_stiff_sign=toy,rows=rows,checks=checks)
 def save():
  result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
 save()
 for count in [1,2,4]:
  current=state.copy();currentN=N;currentJ=J;currentorbit=orb;work=0.;history=[];row=dict(substeps=count,completed=False,history=history);rows.append(row);save()
  for k in range(count):
   try:ns,Jn,on,dw,info=midpoint_step(model,bg,averaged_exact_events,currentN,current,currentJ,total/count,geometry='midpoint',population='midpoint',max_outer=10,outer_tol=1e-7)
   except RuntimeError as exc:row['failure']=str(exc);save();break
   col=info['collision'];history.append(dict(step=k+1,min_f=col['min_f'],max_fermion_f=col['max_fermion_f'],entropy_gain=col['entropy_change'],physical_number_balance_L1=col['physical_number_balance_L1'],local_energy_relative=col['local_energy_relative'],outer_iterations=len(col['outer_iterations']),Newtons=[i['population_newton']['iterations'] for i in col['outer_iterations']]));current=ns;currentJ=Jn;currentorbit=on;currentN+=total/count;work+=dw;print('midpoint',count,k+1,currentJ,history[-1],flush=True);save()
  else:
   row.update(completed=True,final_J=currentJ,final_numbers=current.numbers().tolist(),independent_work=work,independent_energy_work_error=(currentorbit['E']-orb['E']+work)/(orb['E']-orb['minimum']));save()
 all_done=all(r['completed'] for r in rows);checks.update(stiff_positive_sign=toy[0]['completed'] and abs(toy[0]['new_numbers'][0]-toy[0]['expected_parent'])<1e-7,stiff_overshoot_rejected=not toy[1]['completed'],actual_steps_completed=all_done)
 if all_done:
  A,B,C=[np.array(r['final_numbers']) for r in rows];d1=float(sum(abs(A-B)));d2=float(sum(abs(B-C)));j1=abs(rows[0]['final_J']-rows[1]['final_J']);j2=abs(rows[1]['final_J']-rows[2]['final_J']);result['order']=dict(number_difference_h_h2=d1,number_difference_h2_h4=d2,number_observed_order=math.log(d1/d2,2) if d1*d2>0 else None,action_difference_h_h2=j1,action_difference_h2_h4=j2,action_observed_order=math.log(j1/j2,2) if j1*j2>0 else None);checks.update(actual_quantum_bounds=all(h['min_f']>=0 and h['max_fermion_f']<=1 for r in rows for h in r['history']),actual_entropy=all(h['entropy_gain']>=-1e-10 for r in rows for h in r['history']),actual_balance=max(h['physical_number_balance_L1'] for r in rows for h in r['history'])<1e-12,independent_energy=max(abs(r['independent_energy_work_error']) for r in rows)<.01,second_order_signal=result['order']['number_observed_order']>1.5 and result['order']['action_observed_order']>1.5)
 result['scope']='LocalcontrolatNEWcompletedfinewarmstate. MidpointisnotLstableorunconditionallypositive; meaningfulovershootmustberejected. Nochangedfreshhistoryorcontinuum/coldcandidateclaim.';save();print(json.dumps(dict(checks=checks,order=result.get('order'),runtime=result['runtime_seconds'])),flush=True);assert all(checks.values())
if __name__=='__main__':main_mid(sys.argv[1])
