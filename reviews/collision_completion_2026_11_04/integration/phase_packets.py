"""Resolved actual initial field orbit and recorded cold harmonic packets.

This exports background replay inputs, not a new quantum coupled history.
"""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'reviews/coupled_trapping_2026_11_04'
sys.path.insert(0,str(OLD/'kinetics'))
from accurate import Accurate,LocalPotential

def main(output):
 started=time.monotonic()
 point=dict(json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][1])
 spin=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][1]['spins'][0]
 packet=json.loads((OLD/'gravity_resonance/run_leading001/result.json').read_text())['packet'];r=packet['global_profile']
 point.update(grid=r['grid'],T0_potential_mu4=r['V0_origin_subtracted_mu4'],origin_force=r['origin_force'],origin_curvature=r['origin_curvature'],mu_GeV=packet['mu_GeV'])
 model=Accurate(point,spin,bins=24,orbitn=64,absorbing=False)
 model.v=LocalPotential(model.v,packet['local_profile']);model.grid=np.unique(np.r_[0,np.linspace(.001,10,200),np.linspace(10,40,180)])
 model.setup();f=np.r_[model.f0,np.zeros(model.n)];orb=model.orbital(0,f,J=model.J0);omega=2*math.pi/orb['period']
 def rhs(u,y):return [y[1],-model.force(y[0],model.t0,f)/(62*omega**2)]
 def minimum(u,y):return y[1]
 minimum.direction=1
 sol=solve_ivp(rhs,[0,2*math.pi*1.1],[model.x0,0.],rtol=3e-11,atol=1e-12,max_step=2*math.pi/400,dense_output=True,events=minimum)
 times=[q for q in sol.t_events[0] if q>1]
 if not times:raise RuntimeError('resolved initial orbit did not return to left turning point')
 uperiod=times[0];u=np.linspace(0,uperiod,513);yy=sol.sol(u);rho=model.gas(yy[0],model.t0,f)[0]
 energy=31*(omega*yy[1])**2+model.v(yy[0])+rho
 error=float(max(abs(energy-energy[0]))/model.scale)
 direct_period=uperiod/omega
 initial=dict(Tc_over_mu=model.t0,x_initial=model.x0,mu_GeV=model.mu,
   initial_f_F=model.f0.tolist(),initial_f_C=[0.]*model.n,q_edges=model.edges.tolist(),q_centers=model.q.tolist(),W=model.W.tolist(),
   period_tau=direct_period,omega_tau=2*math.pi/direct_period,H_over_omega=model.H(0)/(2*math.pi/direct_period),
   quadrature_x=orb['xs'].tolist(),quadrature_weights=orb['weights'].tolist(),
   resolved_tau=(u/omega).tolist(),resolved_x=yy[0].tolist(),resolved_dx_dtau=(omega*yy[1]).tolist(),energy_ledger_relative=error)
 cold=[]
 for folder in ('run_leading_fine_001','run_hybrid_bw_001'):
  case=json.loads((OLD/'kinetics'/folder/'result.json').read_text())['case'];h=case['history'][-1]
  mid=(h['x_inner']+h['x_outer'])/2;amp=(h['x_outer']-h['x_inner'])/2;om=2*h['action']/(62*amp*amp)
  th=np.linspace(0,2*math.pi,513)
  cold.append(dict(source=folder,Tc_over_mu=h['Tc_over_mu'],xmid=mid,amplitude=amp,omega_tau=om,
    H_over_omega=h['H_over_oscillation'],period_tau=2*math.pi/om,
    q_edges=case['q_edges'],q_centers=case['q_centers'],fF=case['final_f_F'],fC_number_normalization=case['final_f_S_number_normalization'],
    actual_fC_multiplier=2,resolved_tau=(th/om).tolist(),resolved_x=(mid-amp*np.cos(th)).tolist(),
    resolved_dx_dtau=(amp*om*np.sin(th)).tolist(),gaugino_occupation='not saved by CT09; no empty-bath inference'))
 checks=dict(direct_orbit_completed=bool(sol.success),resolved_initial_energy=error<1e-7,
  direct_vs_action_period=abs(direct_period/orb['period']-1)<2e-3,
  positive_normalized_phase_weights=bool(min(orb['weights'])>0 and abs(sum(orb['weights'])-1)<1e-12),
  cold_frequency_matches_local_mass=all(abs(c['omega_tau']/(.04347258513104564/2e6)-1)<1e-3 for c in cold))
 result=dict(claim_id='CC10_RECORDED_PHASE_PACKETS',checks={k:bool(v) for k,v in checks.items()},initial=initial,cold=cold,
   direct_action_period_relative_difference=direct_period/orb['period']-1,
   scope='Actual conservative initial frozen-occupation orbit plus recorded harmonic cold endpoint backgrounds. These are replay inputs; quantum collisions change both occupations and field and require coupled recomputation.',
   runtime_seconds=time.monotonic()-started,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','direct_action_period_relative_difference','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
