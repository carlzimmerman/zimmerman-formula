"""Explicit hybrid: NWAearlyhistory then staticfiniteBWlatecontinuation."""
import sys
sys.dont_write_bytecode=True
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from finite_bw import Finite
from accurate import LocalPotential
from two_species import ROOT,HERE

def run(model,N,y,Nend,out):
 n=model.n;step=.001;accepted=0;rejected=0;history=[model.rate(N,y,True)];reason='target cooling reached';startN=N
 def snapshot(reason):
  return dict(reason=reason,initial_N=startN,final_N=N,accepted=accepted,rejected=rejected,history=history,state=y.tolist(),q_edges=model.edges.tolist(),q_centers=model.q.tolist(),initial_f_F=model.f0.tolist(),final_f_F=(y[:n]*model.norm/model.W).tolist(),final_f_S_number_normalization=(y[n:2*n]*model.norm/model.W).tolist(),max_local_rate_over_oscillation=model.maxlocal,max_phase_nodes=model.max_phase_nodes,max_period_relative_change=model.max_period_relative_change)
 while N<Nend-1e-12:
  step=min(step,.01,Nend-N)
  try:
   A,a=model.rate(N,y);yp=np.r_[expm(step*A)@y[:2*n],y[2*n:]+step*a];B,b=model.rate(N+step,yp);yn=np.r_[expm(step*(A+B)/2)@y[:2*n],y[2*n:]+step*(a+b)/2];err=max(float(sum(abs(yn[:2*n]-yp[:2*n])))/max(float(sum(yn[:2*n])),1e-4),abs(float(yn[2*n]-yp[2*n]))*.1,abs(float(yn[2*n+1]-yp[2*n+1]))*.05)
   if err>.001:rejected+=1;step*=max(.15,.8*math.sqrt(.001/err));continue
   N+=step;y=yn;accepted+=1;last=model.rate(N,y,True)
   if accepted==1 or N-history[-1]['N']>.02 or N>=Nend-1e-12:history.append(last)
   if accepted%20==0:Path(out).write_text(json.dumps({'claim_id':'CT09_HYBRID_FINITE_BW_CONTINUATION','partial':True,'case':snapshot('in progress')},indent=2)+'\n')
   if model.maxlocal>.1:reason='local collision averaging hierarchy failed';break
   if abs(last['energy_ledger_error'])>.02:reason='energy ledger tolerance failed';break
   step*=min(2,max(.5,.9*math.sqrt(.001/max(err,1e-14))))
  except RuntimeError as exc:
   rejected+=1;step*=.25
   if step<1e-11:reason=str(exc);break
 if history[-1]['N']!=N:history.append(model.rate(N,y,True))
 return snapshot(reason)

def main(out,Tend):
 start=time.monotonic();Tend=float(Tend);source=HERE/'run_leading_two_001/result.json';old=json.loads(source.read_text())['case'];p=dict(json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][1]);s=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][1]['spins'][0];packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet'];r=packet['global_profile'];p.update(grid=r['grid'],T0_potential_mu4=r['V0_origin_subtracted_mu4'],origin_force=r['origin_force'],origin_curvature=r['origin_curvature'],mu_GeV=packet['mu_GeV']);model=Finite(p,s,bins=24,orbitn=16,absorbing=True,angular=12);model.v=LocalPotential(model.v,packet['local_profile']);model.grid=np.unique(np.r_[0,np.linspace(.001,10,100),np.linspace(10,40,180)]);model.setup();h=old['history'][-1];N=h['N'];fF=np.array(old['final_f_F']);fS=np.array(old['final_f_S_number_normalization']);work=(model.E0+h['energy_ledger_error']*model.scale-h['energy']-h['radiation_energy_mu4'])/model.scale;y=np.r_[fF*model.W/model.norm,fS*model.W/model.norm,math.log(h['action']/model.J0),h['radiation_energy_mu4']*math.exp(4*N)/model.scale,work,h['gauge_events_per_initial_carrier']];case=run(model,N,y,math.log(s['TD_over_mu']/Tend),out);case.update(mu_GeV=p['mu_GeV'],end_Tc=Tend,early_source=str(source));result=dict(claim_id='CT09_HYBRID_FINITE_BW_CONTINUATION',partial=False,case=case,checks={'cooling_reached':case['reason']=='target cooling reached','energy_ledger':bool(max(abs(h['energy_ledger_error']) for h in case['history'])<.02),'local_averaging_hierarchy':bool(model.maxlocal<.1)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Explicit hybrid: earlycompletedall-parentNWAabsorbinghistory toTc1e-5, thenstaticcoherentfiniteBWonlyforfourconstantneutralparents nearpole. Switchingkernelchangescollisionmodel; notfullBWfrominitialstate andnotanupperboundonallhistories. Emptygaugino/inverse/Pauliomissions, neutraldaughterforce andtime-dependentmemory unresolved. Durablepartialstatewritteneach20acceptedsteps, finalcasecontainsfullstateforboundedcontinuation.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));print(case['reason'],case['history'][-1]);assert all(result['checks'].values())
if __name__=='__main__':main(*sys.argv[1:])
