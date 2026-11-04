"""Positive ann-half / conservative elastic / ann-half oldcold comparison.

Ann log-ODE and all source quadratures are independent of the elastic BE
solver. Actual massive neutral cohorts and separately measured model energy
residuals are retained. The full raw energy residual is a precision diagnostic;
subtracting it is only accounting, not an independent physics certificate.
"""
import sys,json,time,resource,math,gc
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
import numpy as np
from scipy.integrate import solve_ivp
from elastic_builder_v2 import grid,screening,event_arrays_chunked
from template import template_arrays
from log_number import QuantumState,implicit_step
from binary_events_v2 import BinaryEvents
MAXSTEP=.05

def lerp(x,grid,values):
 i=int(np.clip(np.searchsorted(grid,x)-1,0,len(grid)-2));a=(x-grid[i])/(grid[i+1]-grid[i]);return (1-a)*values[i]+a*values[i+1]

def make_events(a):return BinaryEvents(a['index'],a['weights'],a['coefficient'],a['measure'],a['energy'],a['eta'],a['groups'])

def main(out):
 start=time.monotonic();OLD=ROOT/'reviews/collision_completion_2026_11_04';stage=json.loads((OLD/'memory/run_stage001/result.json').read_text());late=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];source=json.loads((HERE.parent/'run_late_kernels001/result.json').read_text());oldk=json.loads((OLD/'memory/run_stage001/kernels.json').read_text());edges=np.array(stage['q_edges']);q,W,cells=grid(edges,1);good=cells>=0;ci=cells[good];n=len(q);f0=np.full(n,1e-45);f0[good]=2*np.array(stage['initial_fS'])[ci];ff=f0.copy();ff[good]=2*np.array(stage['final_fS'])[ci];m=.003/2*math.sqrt(25.4000254000381**2+2/(31*.003));N0,Nend=late['history'][0]['N'],late['history'][-1]['N'];Tc0=late['history'][0]['Tc_over_mu'];omega=source['omega'];H0=late['history'][0]['H_over_oscillation']*omega;consts=2*math.pi**2/45*106.75/.02**3;cSM=1/consts;mass=np.array(source['terminal_mass_mu']);dm=np.array(source['terminal_dm_dx']);p0=np.array(source['terminal_p_mu']);terminal=np.array(source['terminal_transfer']);groups=np.array(source['terminal_group']);M=source['parent_mass'];ns=np.array(oldk['N']);Ks=np.array(oldk['K']);sn=np.array([c['N'] for c in source['cases']]);fields={key:np.array([c[key] for c in source['cases']]) for key in source['fields']};channels=np.array([c['channel_K'] for c in source['cases']]);Tref=1e-6;ref=event_arrays_chunked(q,W,Tref,m,screening(q,W,ff,Tref,m),incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.);ref['reference_screening_f']=ff;measure=ref['measure'];eta=ref['eta'];initial=QuantumState(measure,eta,Z=measure*f0,holes=np.zeros(n,bool));Yinit=initial.numbers();Jinit=source['initial_J'];s0=consts*Tc0**3;Efield0=omega*Jinit/s0;Einitial=cSM*float(np.sqrt(m*m+(Tc0*q)**2)@Yinit)+Efield0;histories={};endpoints={};states={};partial=True;reason='started';checks={};zgl,wgl=np.polynomial.legendre.leggauss(4)
 def therm(N):
  T=Tc0*math.exp(-(N-N0));return T,H0*math.exp(-2*(N-N0)),consts*T**3
 def neutral(cohorts,N):
  energy=pressure=force=rest=0.;counts=np.zeros(len(mass))
  for born,count in cohorts:
   p=p0*math.exp(born-N);E=np.sqrt(mass*mass+p*p);energy+=float(count@E);rest+=float(count@mass);pressure+=float(count@(p*p/(3*np.maximum(E,1e-300))));force+=float(count@(mass*dm/np.maximum(E,1e-300)));counts+=count
  return dict(energy=energy,rest=rest,pressure=pressure,force=force,counts=counts)
 def charged(N,Y):
  T,H,s=therm(N);E=np.sqrt(m*m+(T*q)**2);return dict(energy=cSM*float(E@Y),pressure=cSM/3*float(np.sum(Y*(T*q)**2/E)),force=T**3*.003**2*25.4000254000381/4*float(np.sum(Y/E)))
 def ann(a,b,st,cohorts,acc):
  Yold=st.numbers();before=neutral(cohorts,a)
  def rhs(N,y):
   T,H,s=therm(N);K=lerp(N,ns,Ks);Y=np.exp(y);yc=np.bincount(ci,weights=Y[good],minlength=len(edges)-1);v=np.zeros(n);v[good]=-.5*T**3/H*(K@yc)[ci];return v
  sol=solve_ivp(rhs,[a,b],np.log(Yold),rtol=2e-10,atol=2e-10,dense_output=True,max_step=.005,method='DOP853')
  if not sol.success:raise RuntimeError('annlogODE '+sol.message)
  Ynew=np.exp(sol.y[:,-1]);cuts=np.unique(np.r_[a,b,ns[(ns>a)&(ns<b)],sn[(sn>a)&(sn<b)]]);birth=[];integrals=dict(event=0.,P=0.,finite=0.,EC=0.,EN=0.,Egrid=0.,work=0.)
  for left,right in zip(cuts[:-1],cuts[1:]):
   for z,w in zip(zgl,wgl):
    N=(left+right)/2+(right-left)/2*z;wt=(right-left)/2*w;T,H,s=therm(N);Y=np.exp(sol.sol(N));yc=np.bincount(ci,weights=Y[good],minlength=len(edges)-1);pair=(T**3*yc/2)[:,None]*(T**3*yc/2)[None,:];K=lerp(N,ns,Ks);factor=K/np.maximum(lerp(N,sn,fields['K']),1e-300);rc=np.sum(lerp(N,sn,channels)*factor[None,:,:]*pair[None,:,:],axis=(1,2));e=rc*wt/(H*s);birth.append((N,e));integrals['event']+=float(sum(e));values={key:float(np.sum(pair*lerp(N,sn,val)*factor))*wt/(H*s) for key,val in fields.items()};integrals['P']+=values['scalar_field_power_pair'];integrals['finite']+=values['finite_width_energy_ledger_residual_pair'];integrals['EC']+=values['charged_mean_energy_rate_pair'];integrals['EN']+=values['neutral_exit_energy_rate_pair'];E=np.sqrt(m*m+(T*q)**2);loss=np.zeros(n);loss[good]=.5*T**3*Y[good]*(K@yc)[ci];integrals['Egrid']+=cSM*float(E@loss)*wt/H;integrals['work']+=3*charged(N,Y)['pressure']*wt
  exact_pair=cSM*float(sum(Yold-Ynew))/2;scale=exact_pair/max(integrals['event'],1e-300);acc['max_source_quadrature_renormalization']=max(acc['max_source_quadrature_renormalization'],abs(scale-1));acc['work']+=integrals['work'];inj=0
  for N,e in birth:
   count=(e*scale)@terminal;cohorts.append((N,count));inj+=M*float(sum(e))*scale
  after=neutral(cohorts,b);acc['work']+=before['energy']+inj-after['energy'];acc['pairyield']+=exact_pair;P=scale*integrals['P'];finite=scale*integrals['finite'];cell=scale*(integrals['EC']-integrals['Egrid']);boost=scale*(M*integrals['event']-integrals['EN']);raw=scale*(integrals['P']+M*integrals['event']-integrals['Egrid']);acc['field']+=P;acc['signed']+=P;acc['finite']+=finite;acc['cell']+=cell;acc['boost']+=boost;acc['residual']+=raw;acc['interpolation_closure']+=raw-finite-cell-boost
  return QuantumState(measure,eta,Z=Ynew,holes=np.zeros(n,bool))
 def save():Path(out).write_text(json.dumps(dict(claim_id='CC11_POSITIVE_SPLIT_COLD_COULOMB_CASCADE_STAGE',partial=partial,reason=reason,maxstep=MAXSTEP,N0=N0,Nend=Nend,q=q.tolist(),W=W.tolist(),initial_charged_yield=cSM*float(sum(Yinit)),initial_energy_over_entropy_mu=Einitial,initial_field_oscillation_over_entropy_mu=Efield0,histories=histories,endpoints=endpoints,states=states,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ConditionaloldlateTc1e-5→1e-6: accuratepositiveannlogODEhalfsteps+BEconservativequantumselfC-Celastic+actualmassivecohorts. Scalarsignedwork, rawfinitewidth/cell/boostresidualsandindependentpressure/redshiftworkretained. Correctedledgerisasourceaccountingcheck, rawunsubtractedmodelresidualmustbereported. Recordedscalarorbitfirst-correctioninput; nofreshwarmspliceorfullcandidate. Missingoldchargedspecies/bath/loop/inversemediumchannelsremainexplicit.'),separators=(',',':'))+'\n')
 save()
 try:
  for mode in ('no_elastic','elastic'):
   N=N0;st=initial.copy();cohorts=[];acc=dict(work=0.,field=Efield0,pairyield=0.,signed=0.,finite=0.,cell=0.,boost=0.,residual=0.,interpolation_closure=0.,max_source_quadrature_renormalization=0.);h=[];histories[mode]=h;max_e=max_raw=max_fb=max_nb=max_j=0;maxits=0
   while N<Nend-1e-12:
    if time.monotonic()-start>209:reason='durable_wall_checkpoint';states[mode]=dict(N=N,Y=st.numbers().tolist(),cohorts=[dict(N=b,count=c.tolist()) for b,c in cohorts],acc=acc);save();return
    dn=min(MAXSTEP,Nend-N);mid=N+dn/2;end=N+dn;st=ann(N,mid,st,cohorts,acc);info=dict(iterations=0)
    if mode=='elastic':
     T,H,s=therm(mid);f,a=st.arrays();ev=make_events(template_arrays(ref,T,f));oldst=st;st,info=implicit_step(ev,st,dn/H,tol=2e-8,number_floor=1e-14);nb=float(sum(abs(st.numbers()-oldst.numbers()-dn/H*st.rhs(ev))));max_nb=max(max_nb,nb);maxits=max(maxits,info['iterations']);del ev;gc.collect()
    st=ann(mid,end,st,cohorts,acc);N=end;Y=st.numbers();ch=charged(N,Y);ne=neutral(cohorts,N);T,H,s=therm(N);raw=(ch['energy']+ne['energy']+acc['field']+acc['work']-Einitial)/Einitial;corrected=raw-acc['residual']/Einitial;max_e=max(max_e,abs(corrected));max_raw=max(max_raw,abs(raw));jc=acc['field']/Efield0-1;max_j=max(max_j,abs(jc));forceN=s*ne['force'];recY=float(np.interp(N,[r['N'] for r in late['history']],[r['Y_charged'] for r in late['history']]));forceRef=s*recY*.003**2*25.4000254000381/(4*m);amp=float(np.interp(N,[r['N'] for r in late['history']],[(r['x_outer']-r['x_inner'])/2 for r in late['history']]));fr=abs(forceN+ch['force']-forceRef)/(62*omega*omega*amp);max_fb=max(max_fb,fr);r=dict(N=N,Tc=T,charged_yield=cSM*float(sum(Y)),charged_energy_over_entropy_mu=ch['energy'],charged_pressure_over_entropy_mu=ch['pressure'],neutral_energy_over_entropy_mu=ne['energy'],neutral_rest_over_entropy_mu=ne['rest'],neutral_pressure_over_entropy_mu=ne['pressure'],field_oscillation_over_entropy_mu=acc['field'],independent_FRW_work_over_entropy_mu=acc['work'],raw_energy_plus_work_minus_initial_relative=raw,full_model_residual_relative=acc['residual']/Einitial,accounted_model_ledger_relative=corrected,action_relative_correction=jc,combined_force_shift_over_recorded_amplitude=fr,elastic_implicit_iterations=info['iterations']);h.append(r);states[mode]=dict(N=N,Y=Y.tolist(),cohorts=[dict(N=b,count=c.tolist()) for b,c in cohorts],acc=acc);save()
   ne=neutral(cohorts,Nend);ch=charged(Nend,st.numbers());endpoints[mode]=dict(N=N,charged_yield=cSM*float(sum(st.numbers())),reference_continuous_memory_yield=stage['final_Y_charged'],charged_energy_over_entropy_mu=ch['energy'],charged_pressure_over_entropy_mu=ch['pressure'],neutral_energy_over_entropy_mu=ne['energy'],neutral_rest_over_entropy_mu=ne['rest'],neutral_pressure_over_entropy_mu=ne['pressure'],neutral_group_yields={gid:float(ne['counts'][groups==gid].sum()) for gid in set(groups)},neutral_force_mu3=therm(Nend)[2]*ne['force'],final_f=st.arrays()[0].tolist(),final_Y=st.numbers().tolist(),max_accounted_model_ledger_relative=max_e,max_raw_energy_plus_work_minus_initial_relative=max_raw,full_model_residual_over_entropy_mu=acc['residual'],full_model_residual_relative=acc['residual']/Einitial,finitewidth_residual_over_entropy_mu=acc['finite'],cell_residual_over_entropy_mu=acc['cell'],parentboost_residual_over_entropy_mu=acc['boost'],interpolation_energy_closure_over_entropy_mu=acc['interpolation_closure'],max_action_relative_correction=max_j,max_combined_force_shift_over_recorded_amplitude=max_fb,actual_pair_event_yield=acc['pairyield'],half_charged_yield_loss=(cSM*float(sum(Yinit))-cSM*float(sum(st.numbers())))/2,max_source_quadrature_renormalization=acc['max_source_quadrature_renormalization'],max_number_balance_L1=max_nb,max_implicit_iterations=maxits);print(mode,endpoints[mode]['charged_yield'],time.monotonic()-start,flush=True);save()
  partial=False;reason='target_reached';checks=dict(target=bool(all(abs(e['N']-Nend)<1e-12 for e in endpoints.values())),baseline_continuous=bool(abs(endpoints['no_elastic']['charged_yield']/stage['final_Y_charged']-1)<1e-6),accounting=bool(max(e['max_accounted_model_ledger_relative'] for e in endpoints.values())<1e-7),raw_residual_small=bool(max(e['max_raw_energy_plus_work_minus_initial_relative'] for e in endpoints.values())<1e-3),event_number=bool(max(abs(e['actual_pair_event_yield']/e['half_charged_yield_loss']-1) for e in endpoints.values())<1e-6),force_feedback=bool(max(e['max_combined_force_shift_over_recorded_amplitude'] for e in endpoints.values())<1e-3),action_feedback=bool(max(e['max_action_relative_correction'] for e in endpoints.values())<1e-3),source_quadrature=bool(max(e['max_source_quadrature_renormalization'] for e in endpoints.values())<1e-5));save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
