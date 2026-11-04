"""Conditional oldlate scalar+neutral-cohort cooling with conservative elastic.

Every charged removal injects the actual neutral cascade. Signed scalar work,
finite-width/cell/boost energy residuals and independent massive FRW work are
kept separately. The recorded scalar orbit is a tested first-correction input,
not spliced to a new common warm history.
"""
import sys,json,time,resource,math,gc
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'))
import numpy as np
from scipy.sparse import csr_matrix,diags
from elastic_builder_v2 import grid,screening,event_arrays_chunked,make_events
from template import template_arrays
from log_number import QuantumState,implicit_step
MAXSTEP=.1

def lerp(x,grid,values):
 i=int(np.clip(np.searchsorted(grid,x)-1,0,len(grid)-2));a=(x-grid[i])/(grid[i+1]-grid[i]);return (1-a)*values[i]+a*values[i+1]

class Collision:
 def __init__(self,elastic,K,T,measure,eta):self.elastic=elastic;self.K=np.asarray(K);self.a=.5*T**3;self.measure=measure;self.eta=eta
 def number_rhs(self,f,a=None):
  Y=self.measure*f;v=-self.a*Y*(self.K@Y)
  return v if self.elastic is None else v+self.elastic.number_rhs(f,a)
 def number_gross(self,f,a=None):
  Y=self.measure*f;v=self.a*Y*(self.K@Y)
  return v if self.elastic is None else v+self.elastic.number_gross(f,a)
 def number_jacobian(self,f,a=None):
  Y=self.measure*f;j=-self.a*(diags(self.K@Y)+diags(Y)@csr_matrix(self.K))
  return j if self.elastic is None else j+self.elastic.number_jacobian(f,a)

def main(out):
 start=time.monotonic();OLD=ROOT/'reviews/collision_completion_2026_11_04';stage=json.loads((OLD/'memory/run_stage001/result.json').read_text());old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];source=json.loads((HERE.parent/'run_late_kernels001/result.json').read_text());oldk=json.loads((OLD/'memory/run_stage001/kernels.json').read_text());edges=np.array(stage['q_edges']);q,W,cells=grid(edges,1);good=cells>=0;n=len(q);f0=np.full(n,1e-45);f0[good]=2*np.array(stage['initial_fS'])[cells[good]];ff=f0.copy();ff[good]=2*np.array(stage['final_fS'])[cells[good]];m=.003/2*math.sqrt(25.4000254000381**2+2/(31*.003));Tc0=old['history'][0]['Tc_over_mu'];N0=old['history'][0]['N'];Nend=old['history'][-1]['N'];omega=source['omega'];H0=old['history'][0]['H_over_oscillation']*omega;consts=2*math.pi**2/45*106.75/.02**3;cSM=1/consts;mass=np.array(source['terminal_mass_mu']);dm=np.array(source['terminal_dm_dx']);p0=np.array(source['terminal_p_mu']);terminal=np.array(source['terminal_transfer']);groups=np.array(source['terminal_group']);M=source['parent_mass'];ns=np.array(oldk['N']);Ks=np.array(oldk['K']);sn=np.array([c['N'] for c in source['cases']]);fields={key:np.array([c[key] for c in source['cases']]) for key in source['fields']};channels=np.array([c['channel_K'] for c in source['cases']]);Tref=1e-6;ref=event_arrays_chunked(q,W,Tref,m,screening(q,W,ff,Tref,m),incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.);ref['reference_screening_f']=ff;measure=ref['measure'];eta=ref['eta'];initial=QuantumState(measure,eta,Z=measure*f0,holes=np.zeros(n,bool));Yinit=initial.numbers();en0=np.sqrt(m*m+(Tc0*q)**2);Echarge0=cSM*float(en0@Yinit);Jinit=source['initial_J'];s0=consts*Tc0**3;Efield0=omega*Jinit/s0;Einitial=Echarge0+Efield0;histories={};endpoints={};states={};partial=True;reason='started';checks={}
 def therm(N):
  T=Tc0*math.exp(-(N-N0));return T,H0*math.exp(-2*(N-N0)),consts*T**3
 def neutral(cohorts,N):
  energy=pressure=force=rest=0.;counts=np.zeros(len(mass))
  for born,count in cohorts:
   p=p0*math.exp(born-N);e=np.sqrt(mass*mass+p*p);energy+=float(count@e);rest+=float(count@mass);pressure+=float(count@(p*p/(3*np.maximum(e,1e-300))));force+=float(count@(mass*dm/np.maximum(e,1e-300)));counts+=count
  return dict(energy=energy,rest=rest,pressure=pressure,force=force,counts=counts)
 def save():Path(out).write_text(json.dumps(dict(claim_id='CC11_CONDITIONAL_COLD_COULOMB_CASCADE_STAGE',partial=partial,reason=reason,maxstep=MAXSTEP,N0=N0,Nend=Nend,q=q.tolist(),W=W.tolist(),histories=histories,endpoints=endpoints,states=states,initial_charged_yield=cSM*float(sum(Yinit)),initial_energy_over_entropy_mu=Einitial,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='SeparateconditionaloldCT09latecoolingTc1e-5→1e-6: actualchargedscalar37cellshape pluspositivequantumselfC-Celastictemplate, old4Pmemorychemicalkernel, actualtreecascadecohortswithmass,p,redshift,force. Signedscalarwork/actionfirstcorrection, finitewidth/cell/parentboostenergyresidualsexplicit. Recordedvacuumorbithistoryretainedandfeedbackbounded. Oldearlygauginobathunknown; noFDinvented. Loopneutralexits/inverseoccupiedneutralselfenergiesnotcompletedhere. Nojointfreshwarm/coldspliceorviabilityclaim.'),separators=(',',':'))+'\n')
 save()
 try:
  for mode in ('no_elastic','elastic'):
   N=N0;st=initial.copy();J=Jinit;cohorts=[];work=0.;residual=0.;pairyield=0.;signed=finite=cell=boost=0.;h=[];max_energy=0.;max_jcorr=0.;max_force_ratio=0.;max_number_balance=0.;maxits=0;maxpowers=0
   histories[mode]=h
   while N<Nend-1e-12:
    if time.monotonic()-start>207:reason='durable_wall_checkpoint';states[mode]=dict(N=N,Y=st.numbers().tolist(),Z=st.Z.tolist(),hole_flags=st.holes.tolist(),J=J,cohorts=[dict(N=b,count=c.tolist()) for b,c in cohorts],work=work,residual=residual);save();return
    dn=min(MAXSTEP,Nend-N);Nm=N+dn/2;Nnew=N+dn;T,H,s=therm(Nm);Told,_,sold=therm(N);Tnew,_,snew=therm(Nnew);Yold=st.numbers();eold=np.sqrt(m*m+(Told*q)**2);emid=np.sqrt(m*m+(T*q)**2);enew=np.sqrt(m*m+(Tnew*q)**2);before=neutral(cohorts,N);work+=cSM*float((eold-emid)@Yold);K=lerp(Nm,ns,Ks);Km=np.zeros((n,n));ci=cells[good];Km[np.ix_(good,good)]=K[np.ix_(ci,ci)];f,a=st.arrays();ee=None
    if mode=='elastic':ee=make_events(template_arrays(ref,T,f))
    op=Collision(ee,Km,T,measure,eta);oldst=st;st,info=implicit_step(op,st,dn/H,tol=2e-8,number_floor=1e-14);Y=st.numbers();nr=Y-Yold-dn/H*st.rhs(op);max_number_balance=max(max_number_balance,float(sum(abs(nr))));maxits=max(maxits,info['iterations']);Ycell=np.bincount(ci,weights=Y[good],minlength=len(edges)-1);percharge=T**3*Ycell/2;pair=percharge[:,None]*percharge[None,:];kt=lerp(Nm,sn,fields['K']);factor=K/np.maximum(kt,1e-300);kc=lerp(Nm,sn,channels)*factor[None,:,:];rc=np.sum(kc*pair[None,:,:],axis=(1,2));event=float(sum(rc));birth=rc*dn/(H*s);count=birth@terminal;cohorts.append((Nm,count));pairyield+=float(sum(birth));kern={key:lerp(Nm,sn,val)*factor for key,val in fields.items()};P=float(np.sum(pair*kern['scalar_field_power_pair']));EF=float(np.sum(pair*kern['finite_width_energy_ledger_residual_pair']));EC=float(np.sum(pair*kern['charged_mean_energy_rate_pair']));EN=float(np.sum(pair*kern['neutral_exit_energy_rate_pair']));Eremoved=cSM*float(emid@(Yold-Y));dfield=P*dn/(H*s);dboost=(M*event-EN)*dn/(H*s);dcell=EC*dn/(H*s)-Eremoved;dfinite=EF*dn/(H*s);# Their sum is the measured model energy residual, with interpolation closure separate.
    dres=dfield+M*float(sum(birth))-Eremoved;residual+=dres;signed+=dfield;finite+=dfinite;cell+=dcell;boost+=dboost;Jmid=J*math.exp(-1.5*dn);Jmid+=P*dn/(H*omega);J=Jmid*math.exp(-1.5*dn);Jbase=Jinit*math.exp(-3*(Nnew-N0));max_jcorr=max(max_jcorr,abs(J/Jbase-1));maxpowers=max(maxpowers,float(np.sum(pair*kern['absolute_scalar_field_power_bound_pair']))/(H*max(Jmid,1e-300)*omega));work+=cSM*float((emid-enew)@Y);after=neutral(cohorts,Nnew);work+=before['energy']+M*float(sum(birth))-after['energy'];charged=cSM*float(enew@Y);field=omega*J/snew;ledger=(charged+after['energy']+field+work-Einitial-residual)/Einitial;max_energy=max(max_energy,abs(ledger));forceC=Tnew**3*.003**2*25.4000254000381/4*float(np.sum(Y/enew));forceN=snew*after['force'];xamp=float(np.interp(Nnew,[r['N'] for r in old['history']],[(r['x_outer']-r['x_inner'])/2 for r in old['history']]));curvature=62*omega*omega;force_ratio=abs(forceN)/(curvature*xamp);max_force_ratio=max(max_force_ratio,force_ratio);r=dict(N=Nnew,Tc=Tnew,charged_yield=cSM*float(sum(Y)),charged_energy_over_entropy_mu=charged,neutral_energy_over_entropy_mu=after['energy'],neutral_rest_over_entropy_mu=after['rest'],neutral_pressure_over_entropy_mu=after['pressure'],field_energy_over_entropy_mu=field,FRW_work_over_entropy_mu=work,energy_ledger_relative=ledger,finitewidth_residual_integrated=dfinite,cell_residual_integrated=dcell,parentboost_residual_integrated=dboost,interpolation_energy_closure=dres-dfinite-dcell-dboost,scalar_work_integrated=dfield,neutral_force_mu3=forceN,charged_force_mu3=forceC,neutral_force_shift_over_orbit_amplitude=force_ratio,J=J,J_over_recorded_action=J/Jbase,elastic_entropy_rate=0 if ee is None else float(ee.entropy_production(st.arrays()[0])),implicit_iterations=info['iterations']);h.append(r);N=Nnew
    if ee is not None:del ee
    del op;gc.collect();states[mode]=dict(N=N,Y=Y.tolist(),J=J);save()
   final=neutral(cohorts,Nend);groupy={gid:float(final['counts'][groups==gid].sum()) for gid in set(groups)};endpoints[mode]=dict(N=N,charged_yield=cSM*float(sum(st.numbers())),actual_pair_event_yield=pairyield,half_charged_yield_loss=(cSM*float(sum(Yinit))-cSM*float(sum(st.numbers())))/2,neutral_group_yields=groupy,neutral_energy_over_entropy_mu=final['energy'],neutral_rest_over_entropy_mu=final['rest'],neutral_force_mu3=therm(Nend)[2]*final['force'],charged_energy_over_entropy_mu=cSM*float(enew@st.numbers()),final_f=st.arrays()[0].tolist(),final_Y=st.numbers().tolist(),max_energy_ledger_relative=max_energy,scalar_signed_work_over_entropy_mu=signed,finitewidth_residual_over_entropy_mu=finite,cell_residual_over_entropy_mu=cell,parentboost_residual_over_entropy_mu=boost,full_model_residual_over_entropy_mu=residual,max_action_relative_correction=max_jcorr,max_neutral_force_shift_over_amplitude=max_force_ratio,max_number_balance_L1=max_number_balance,max_Newton_iterations=maxits,max_absolute_scalar_collision_dlogJ_bound=maxpowers,J=J);print(mode,endpoints[mode]['charged_yield'],time.monotonic()-start,flush=True);save()
  partial=False;reason='target_reached';checks=dict(target=bool(all(abs(r['N']-Nend)<1e-12 for r in endpoints.values())),energy=bool(max(r['max_energy_ledger_relative'] for r in endpoints.values())<1e-8),number_to_neutral=bool(max(abs(r['actual_pair_event_yield']/r['half_charged_yield_loss']-1) for r in endpoints.values())<1e-7),feedback_small=bool(max(r['max_neutral_force_shift_over_amplitude'] for r in endpoints.values())<1e-3),action_correction=bool(max(r['max_action_relative_correction'] for r in endpoints.values())<1e-3),massive_neutral_storage=bool(all(r['neutral_rest_over_entropy_mu']>0 for r in endpoints.values())),positive_action=bool(all(r['J']>0 for r in endpoints.values())));save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
