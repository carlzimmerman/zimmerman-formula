"""Weighted exact-vs-interpolated component data and orbit covariance controls."""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
from network import ROOT,state
from vertices import VertexBackground,vertex_table,channels
from reaction import full_events,thermal,moments
from averaged import averaged_events,covariance,number_rhs

def main(out):
 start=time.monotonic();bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');record=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_coupled003/result.json').read_text())['cases'][0];q=np.array(record['q']);W=np.array(record['W']);f=np.array(record['final_f']);t=record['history'][-1]['Tc'];cases=[]
 for x in (.18444259422092926,.325,1.125,2.375,3.025,3.83742513487,4.75,7.3,12.25,25.399,25.4000254000381):
  direct=vertex_table(x);direct['channels']=channels(direct['groups'],direct['vertices']);interp=bg.at(x);a=full_events(direct,t,q,W,angles=4,source=direct['current_source']);b=full_events(interp,t,q,W,angles=4,source=interp['current_source']);ca=np.asarray(a.S@a.flux(f)).ravel();cb=np.asarray(b.S@b.flux(f)).ravel();ra=float(sum(abs(cb-ca))/max(sum(abs(ca)),1e-300));num=a.measure*f;by={g['id']:g for g in direct['groups']};step=1e-4;plus={g['id']:g for g in state(x+step,vertices=False)['groups']};minus={g['id']:g for g in state(x-step,vertices=False)['groups']}
  for g in direct['groups']:g['dm2_dx']=(plus[g['id']]['mass']**2-minus[g['id']]['mass']**2)/(2*step)
  ma=moments(a,f);mb=moments(b,f);force_relative=float(abs(np.sum(ma['force'])-np.sum(mb['force']))/max(sum(abs(ma['force'])),1e-300));eq=a.audit(thermal(a,.008));cases.append(dict(x=x,RHS_L1_relative_error=ra,force_relative_error=force_relative,exact_channel_count=len(direct['channels']),interpolated_channel_count=len(interp['channels']),thermal_balance=eq['detailed_balance_relative'],energy_event_residual=eq['energy_residual'],direct_forward_omission_fraction=ma['omitted_weighted_rate']/max(ma['omitted_weighted_rate']+ma['included_weighted_rate'],1e-300)))
  print(cases[-1],flush=True)
 phase=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_phases001/result.json').read_text())['initial'];xx=np.array(phase['quadrature_x']);ww=np.array(phase['quadrature_weights']);cdf=np.cumsum(ww)/sum(ww);pos=np.searchsorted(cdf,(np.arange(8)+.5)/8);xs=xx[pos];ev=averaged_events(bg,xs,np.ones(8)/8,t,q,W,angles=2);Y=ev.measure*f;cov,detail=covariance(ev,Y);C=number_rhs(ev,Y);check_energy=abs(detail['local_collision_energy'])/max(abs(detail['averaged_gas_energy_change']),1e-300)
 checks=dict(local_energy=max(r['energy_event_residual'] for r in cases)<1e-12,thermal_detailed_balance=max(r['thermal_balance'] for r in cases)<1e-10,covariance_local_energy=check_energy<1e-8,force_interpolation=max(r['force_relative_error'] for r in cases)<.005)
 result=dict(claim_id='CC10_VERTEX_INTERPOLATION_COVARIANCE_AUDIT',cases=cases,orbit=dict(xs=xs.tolist(),weights=(np.ones(8)/8).tolist(),covariance=cov,detail=detail,local_energy_relative_to_covariance=check_energy,events=len(ev.coefficient)),checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Weighted on recorded early distribution over eleven exact physical points; RHS norm errors are finite interpolation diagnostics, not universal bounds. Force uses rigid finite differences; loop-gaugino derivative contribution is negligible at these values but not separately matched. Orbit weights are8quantile projection of recorded dwell quadrature.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
