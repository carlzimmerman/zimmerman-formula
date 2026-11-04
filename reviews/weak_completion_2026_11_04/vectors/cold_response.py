"""Hard-tail-resolved vector-channel impulse response on the late pole background."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'))
import numpy as np
from common import CommonBackground,CommonOrbit,T0
from transport_v3 import VectorFactory
from log_number import QuantumState,implicit_step

def main(out):
 start=time.monotonic();z,w=np.polynomial.legendre.leggauss(6);qq=[];ww=[]
 for a,b in zip([0,.1,1,5,20,80,800,8000,80000],[.1,1,5,20,80,800,8000,80000,800000]):
  u=a+(b-a)*(z+1)/2;qq.extend(u);ww.extend(w*(b-a)/2*u*u)
 q=np.array(qq);W=np.array(ww);x=25.4000254000381;t=1e-6;N=math.log(T0/t);bg=CommonBackground();model=CommonOrbit(bg,q,W,8);ev=VectorFactory(HERE/'run_table003/result.json').full_events(bg.at(x),t,q,W,angle_order=4);v=ev.vector_operator;g=ev.by['F8_2'];m=v.measure;eta=v.eta;Z=m*1e-45;soft=np.exp(-q*q/2)*W;soft/=soft.sum();Z[g*len(q):(g+1)*len(q)]+=1e-9*soft;st=QuantumState(m,eta,Z=Z);initial=st.copy();width=sum(c['width'] for c in ev.channels if c['parent']=='Vc_L');dt=.5/width;rows=[];partial=True;reason='started';checks={};E0=float(v.energy@st.numbers());seed=float(m.sum()*1e-45)
 def save():Path(out).write_text(json.dumps(dict(partial=partial,reason=reason,x=x,N=N,Tc=t,q=q.tolist(),W=W.tolist(),groups=[g['id'] for g in ev.groups],initial_parent='F8_2',initial_comoving_number=1e-9,initial_seed_number=seed,vector_lifetime=1/width,rows=rows,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Conditional dilute heavy-parent vector-channel impulse at actual late pole; every open VSS/VFF/SVV channel, full massive V momentum/L/T/force and inverses retained. S/F-only reactions disabled to isolate vector response. Initial heavy packet is a Green response, not an asserted cosmological production abundance. qmax~8e5 resolves hard daughters; no warm/cold endpoint splice or relic claim.'),indent=2)+'\n')
 save()
 try:
  for i in range(1,7):
   old=st;st,info=implicit_step(v,st,dt,tol=2e-8,number_floor=1e-18);Y=st.numbers();f,a=st.arrays();num=Y.reshape(30,len(q)).sum(axis=1);gas=model.gas(x,N,Y);F,R,*_=v._logs(f,a);parent=v.index[:,0]//len(q);mask=(parent==25)|(parent==26);dcharged=model.charged[v.index[:,1:]//len(q)];mult=np.sum(v.a[:,1:]*dcharged,axis=1);ret=float(np.sum((v.coefficient*F[0])[mask]*mult[mask]));rev=float(np.sum((v.coefficient*R[0])[mask]*mult[mask]));rhs=st.rhs(v);res=Y-old.numbers()-dt*rhs;forward=float(np.sum(v.coefficient*F[0]));row=dict(step=i,tau=i*dt,info=info,number_by_group=num.tolist(),charged_number=float(num@model.charged),vector_number=float(num[25:].sum()),heavy_parent_number=float(num[g]),vector_force=float(gas['force_by'][0,25:].sum()),gas_force=float(gas['force'][0]),vector_energy=float(t**3*np.sum(Y.reshape(30,len(q))[25:]*v.energies[25:])),relative_total_energy_drift=float((v.energy@Y-E0)/E0),number_balance_L1=float(sum(abs(res))),forward_charged_return_rate=ret,inverse_charged_consumption_rate=rev,entropy_change=st.entropy()-initial.entropy(),occupied_forward_omission_fraction=float(ev.omitted_by_parent@f/max(forward,1e-300)),max_fermion_f=float(f[eta<0].max()),Y=Y.tolist());rows.append(row);print(i,row['vector_number'],row['charged_number'],row['relative_total_energy_drift'],flush=True);save()
  # The actual on-shell coherent P mass lies below every vector-emission threshold.
  P=ev.by['S1_1'];direct_P=sum(c['width'] for c in ev.channels if c['p']==P);checks=dict(energy=bool(max(abs(r['relative_total_energy_drift']) for r in rows)<1e-8),balance=bool(max(r['number_balance_L1'] for r in rows)<1e-20),entropy=bool(all(r['entropy_change']>=0 for r in rows)),bounds=bool(all(r['max_fermion_f']<=1 for r in rows)),charged_returns=bool(rows[-1]['forward_charged_return_rate']>0),massive_vector_force=bool(rows[-1]['vector_force']>0),P_direct_closed=bool(direct_P==0));partial=False;reason='target_reached';save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
