"""Independent scalar action reconstruction from direct25group snapshots."""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
from network import ROOT
from vertices import VertexBackground
from averaged import averaged_events,covariance,number_rhs
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/integration'))
from orbit_frozen_cc10 import GenericOrbit,MASS

def main(out):
 start=time.monotonic();data=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_coupled004/result.json').read_text())['cases'][0];bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');q=np.array(data['q']);W=np.array(data['W']);model=GenericOrbit(bg,q,W,phase_nodes=24);allh=data['history'];inds=np.unique(np.arange(len(allh),dtype=int));rows=[];predlog=0.;previous=None
 for k in inds:
  h=allh[k];N=h['N'];Y=model.measure*np.array(h['f']);rho=float(model.gas(h['x'],N,Y)['rho'][0]);E=float(model.v(h['x']))+rho+MASS*h['velocity']**2/2;orb=model.orbit(N,Y,E=E,commit=True);ev=averaged_events(bg,orb['xs'],orb['weights'],h['Tc'],q,W,angles=2);cov,detail=covariance(ev,Y);lnrate=-3*model.hubble(N)+cov/(orb['omega']*orb['J']);r=dict(time_mu=h['time_mu'],N=N,x=h['x'],action=orb['J'],energy=E,omega=orb['omega'],charged_fraction=h['charged_fraction'],covariance=cov,lnJ_rate_predicted=lnrate,local_collision_energy=detail['local_collision_energy'],energy_offset_to_direct=E-h['total_energy'])
  if previous is not None:predlog+=(r['time_mu']-previous['time_mu'])*(r['lnJ_rate_predicted']+previous['lnJ_rate_predicted'])/2
  r['predicted_log_action_change']=predlog;rows.append(r);previous=r;print(k,r,flush=True)
 J0=rows[0]['action'];actual=math.log(rows[-1]['action']/J0);pred=rows[-1]['predicted_log_action_change'];offset=np.array([r['energy_offset_to_direct'] for r in rows]);checks=dict(positive_actions=min(r['action'] for r in rows)>0,energy_offset_constant=float(np.ptp(offset))<1e-14,local_collision_energy=max(abs(r['local_collision_energy']) for r in rows)<1e-25)
 checks={k:bool(v) for k,v in checks.items()}
 rr=np.array([math.log(r['action']/J0)-r['predicted_log_action_change'] for r in rows]);tt=np.array([r['time_mu'] for r in rows]);regression=np.polyfit(tt/tt[-1],rr,1)
 result=dict(residual_linear_change=float(regression[0]),residual_rms=float(np.sqrt(np.mean((rr-np.polyval(regression,tt/tt[-1]))**2))),claim_id='CC10_DIRECT_ACTION_AVERAGING_CONTROL_V3',cases=rows,checks=checks,actual_log_action_change=actual,predicted_log_action_change=pred,absolute_log_action_difference=pred-actual,relative_drift_error=(pred-actual)/actual if actual else None,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Reconstruct instantaneous adiabatic action fromall full direct snapshots and integrate the24phase averaged collision covariance along that actual occupation history. Does not evolve an averaged history; sparse time sampling and diagonal broad-parent approximation remain.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,'actual',actual,'pred',pred,'error',pred-actual);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
