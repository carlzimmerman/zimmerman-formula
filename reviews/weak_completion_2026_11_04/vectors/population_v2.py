"""Finite actual warm-state transport, vectors retained as massive L/T particles."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'))
import numpy as np
from common import CommonBackground,CommonOrbit,T0
from transport_v3 import VectorFactory
from log_number import QuantumState,implicit_step

def main(out):
 start=time.monotonic();prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/history/run_refine002/result.json').read_text());q=np.array(prior['case']['q']);W=np.array(prior['case']['W']);s=prior['state'];N=s['N'];t=T0*math.exp(-N);x=3.8632233;bg=CommonBackground();model=CommonOrbit(bg,q,W,8);factory=VectorFactory(HERE/'run_table003/result.json');ev=factory.full_events(bg.at(x),t,q,W,angle_order=2);m=ev.measure;eta=ev.eta;oldZ=np.array(s['Z']);oldH=np.array(s['hole_flags']);Z=m*1e-35;Z[:len(oldZ)]=oldZ;holes=np.zeros(len(m),bool);holes[:len(oldH)]=oldH;initial=QuantumState(m,eta,Z=Z,holes=holes);Y0=initial.numbers();charged=np.array([g['charged'] for g in ev.groups]);width=sum(c['width'] for c in ev.channels if c['parent']=='Vc_L');lifetime=1/width;dt=lifetime*.5;rows=[];endpoints={};checks={};partial=True;reason='not_started'
 def describe(st):
  Y=st.numbers();f,a=st.arrays();num=Y.reshape(30,len(q)).sum(axis=1);gas=model.gas(x,N,Y);v=ev.vector_operator;F,R,*_=v._logs(f,a);flux=v.coefficient*(F[0]-R[0]);pg=v.index[:,0]//len(q);isdaughtercharged=charged[v.index[:,1:]//len(q)];chargedreturn=np.sum(v.a[:,1:]*isdaughtercharged,axis=1);mask=(pg==25)|(pg==26);ret=float(np.sum(flux[mask]*chargedreturn[mask]));forward=float(np.sum((v.coefficient*F[0])[mask]*chargedreturn[mask]));reverse=float(np.sum((v.coefficient*R[0])[mask]*chargedreturn[mask]));return dict(Y=Y.tolist(),Z=st.Z.tolist(),hole_flags=st.holes.tolist(),number_by_group=num.tolist(),charged_number=float(num@charged),vector_number=float(num[25:].sum()),photino_number=float(num[23]),energy_comoving=float(ev.energy@Y),gas_force=float(gas['force'][0]),vector_force=float(gas['force_by'][0,25:].sum()),neutral_force=float(gas['force_by'][0,~charged].sum()),net_vector_decay_charged_return_rate=ret,forward_vector_decay_charged_return_rate=forward,inverse_vector_birth_charged_consumption_rate=reverse,entropy=st.entropy(),min_f=float(f.min()),max_fermion_f=float(f[eta<0].max()),occupied_forward_omission=float(ev.omitted_by_parent@f))
 initialrow=describe(initial)
 def save():
  r=dict(claim_id='CC11_FINITE_POLARIZED_VECTOR_TRANSPORT',partial=partial,reason=reason,x=x,N=N,Tc=t,q=q.tolist(),W=W.tolist(),groups=[g['id'] for g in ev.groups],vector_lifetime_mu_inverse=lifetime,step_mu_inverse=dt,initial=initialrow,rows=rows,endpoints=endpoints,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Conditional fixed warm background restart of corrected CC10 diagonal state. Full30 quantum 1↔2 with L/T boost weights and inverses; baseline same state/operators with vector channels off. No expansion or scalar-field advance in this control. Seed1e-35 declared; source-old coherence/energy limitations inherited.');Path(out).write_text(json.dumps(r,indent=2)+'\n')
 save()
 try:
  for name,op in [('full',ev),('no_vector_channels',ev.scalar_fermion_operator)]:
   st=initial.copy();ret=0
   for step in range(1,7):
    if time.monotonic()-start>210:reason='durable_wall_checkpoint';save();return
    old=st;st,info=implicit_step(op,st,dt,tol=2e-8,number_floor=1e-14);r=describe(st);ret+=dt*r['net_vector_decay_charged_return_rate'] if name=='full' else 0;res=st.numbers()-old.numbers()-dt*st.rhs(op);r.update(mode=name,step=step,tau=step*dt,info=info,number_balance_L1=float(sum(abs(res))),relative_energy_drift=float((r['energy_comoving']-initialrow['energy_comoving'])/initialrow['energy_comoving']),integrated_net_charged_return=ret);rows.append(r);print(name,step,r['vector_number'],r['charged_number'],r['vector_force'],flush=True);save()
   endpoints[name]=describe(st);endpoints[name]['integrated_net_charged_return']=ret
  partial=False;reason='target_reached';checks.update(bounds=bool(all(r['min_f']>=0 and r['max_fermion_f']<=1 for r in rows)),energy=bool(max(abs(r['relative_energy_drift']) for r in rows)<1e-10),entropy=bool(all(r['entropy']>=initialrow['entropy']-1e-10 for r in rows)),balance=bool(max(r['number_balance_L1'] for r in rows)<1e-10),actual_vector_population=bool(endpoints['full']['vector_number']>1e-15),charged_return=bool(endpoints['full']['forward_vector_decay_charged_return_rate']>0),inverse_present=bool(endpoints['full']['inverse_vector_birth_charged_consumption_rate']>0));save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
