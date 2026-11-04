"""Calibrated physical hole-coordinate reference and actual warm multisteps.

This controls immutable integration/holes_v2.py. It does not modify a solver
under a recorded run, and does not turn flux-roundoff tolerance into an energy
conservation proof. Physical number and energy errors are recorded separately.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,math,resource
import numpy as np
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/statistics'))
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/integration'))
from quantum import ReactionEvents
from averaged import averaged_events
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0
from log_holes import QuantumState,implicit_step

def toy_control(small,dt):
 ev=ReactionEvents([[0,1,1,2,2]],[[1,1,0,1,0]],[1.],[1.,1.,small],[2.,1.,1.],[-1.,1.,-1.]);old=QuantumState(ev.measure,ev.eta,Y=np.array([.5,1e-30,0.]));new,diag=implicit_step(ev,old,dt,tol=2e-10);f,a=new.arrays()
 mp.mp.dps=100;m=mp.mpf(str(small));D=mp.mpf(str(dt));c0=mp.mpf('1e-30');F0=mp.mpf('.5')
 def residual_h(h):
  x=1-h;F=F0-m*x;C=c0+m*x
  return m*x-D*(F*(1+C)*h-(1-F)*C*x)
 # At small m and fixed dt, h~m*(2/dt+1)+c0. Bracket a
 # positive high-precision physical root instead of demanding equilibrium.
 lo=mp.mpf(0);hi=mp.mpf(1)
 for _ in range(380):
  mid=(lo+hi)/2
  if residual_h(mid)>0:lo=mid
  else:hi=mid
 href=(lo+hi)/2;h=float(a[2]);extent=float(new.numbers()[2]);dn=new.numbers()-old.numbers();escale=float(ev.energy@abs(old.numbers()))
 return dict(lambda_measure=small,dt=dt,f=f.tolist(),availability=a.tolist(),newton=diag,hole_coordinate=bool(new.holes[2]),reference_hole=str(href),relative_hole_error=float(abs(mp.mpf(h)-href)/href),reference_BE_residual=str(residual_h(href)),reconstructed_number_delta=dn.tolist(),reconstructed_energy_delta=float(ev.energy@dn),number_roundoff_scale=float(np.finfo(float).eps*sum(abs(old.numbers()))),energy_roundoff_scale=float(np.finfo(float).eps*escale),reaction_extent_from_lambda=extent,analytic_event_energy_residual=ev.energy_residual)

def main(out):
 start=time.monotonic();toy=[toy_control(s,dt) for s,dt in [(1e-12,1.),(1e-20,1.),(1e-24,1.),(1e-24,1e-21)]]
 prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_warm001/result.json').read_text());c=prior['case'];st=prior['state'];Y=np.array(st['Y']);q=np.array(c['q']);W=np.array(c['W']);N=st['N']
 bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];orb=model.orbit(N,Y,E=st['E']);ev=averaged_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W,2);H=model.hubble(N);state=QuantumState(ev.measure,ev.eta,Y=Y);runs=[];oldcounts=Y.reshape((-1,len(q))).sum(axis=1);physical_energy0=float(ev.energy_average@Y);total_dN=5e-5
 for step in [1e-5,5e-6]:
  current=state.copy();steps=round(total_dN/step);history=[];max_relative_balance=0.;max_localenergy=0.;worst_roundoff=0.
  for j in range(steps):
   old=current.copy();current,diag=implicit_step(ev,current,step/H,tol=2e-9);f,a=current.arrays();F,R,_,_=current.products(ev);flux=current.flux(ev);rhs=np.asarray(ev.S@flux).ravel();dn=current.numbers()-old.numbers();signed=np.where(current.holes,-1.,1.);coordinate_old=np.where(current.holes==old.holes,old.Z,old.measure-old.Z);balance=current.Z-coordinate_old-step/H*signed*rhs
   # Absolute number residual and reconstructed energy are independent of
   # the Newton stopping norm's gross-flux roundoff allowance.
   l1=float(sum(abs(balance)));gross=np.asarray(abs(ev.S)@(ev.coefficient*(F+R))).ravel();rounding=float(32*np.finfo(float).eps*step/H*sum(gross));worst_roundoff=max(worst_roundoff,rounding);max_relative_balance=max(max_relative_balance,l1/max(sum(abs(current.numbers())),1e-300));local=[float(aev.energy@np.asarray(aev.S@(current.flux(aev))).ravel()) for aev in ev.local_events];max_localenergy=max(max_localenergy,float(np.max(abs(np.asarray(local)),initial=0.)))
   print('step',step,j+1,diag,'availability',float(min(a[ev.eta<0])),flush=True);history.append(dict(step=j+1,dN=(j+1)*step,newton=diag,min_f=float(min(f)),max_fermion_f=float(max(f[ev.eta<0])),minimum_fermion_availability=float(min(a[ev.eta<0])),hole_nodes=int(sum(current.holes)),entropy=current.entropy(),absolute_coordinate_balance_L1=l1,gross_flux_roundoff_allowance_L1=rounding,reconstructed_particle_energy_change=float(ev.energy_average@(current.numbers()-Y)),max_local_collision_energy=float(np.max(abs(np.asarray(local)),initial=0.))))
  counts=current.numbers().reshape((-1,len(q))).sum(axis=1);runs.append(dict(step_dN=step,total_dN=total_dN,history=history,final_Z=current.Z.tolist(),hole_flags=current.holes.tolist(),final_numbers=current.numbers().tolist(),final_group_comoving_numbers=counts.tolist(),max_relative_coordinate_balance=max_relative_balance,max_local_collision_energy=max_localenergy,max_roundoff_allowance_L1=worst_roundoff,entropy_gain=current.entropy()-state.entropy()))
  print('warm',step,history[-1],flush=True)
 coarse=np.array(runs[0]['final_numbers']);fine=np.array(runs[1]['final_numbers']);relative_number=float(sum(abs(coarse-fine))/sum(abs(fine)));species=[g['id'] for g in ev.groups];u1=ev.by['F1_1'];p=ev.t*q
 def metrics(run):
  yy=np.array(run['final_numbers']).reshape((-1,len(q)));counts=yy.sum(axis=1);charged=np.array([g['charged'] for g in ev.groups]);return dict(charged_comoving=float(counts@charged),U1_comoving=float(counts[u1]),U1_mean_p_over_mu=float(yy[u1]@p/counts[u1]),groups=species)
 for r in runs:r['metrics']=metrics(r)
 comparisons={k:runs[1]['metrics'][k]/runs[0]['metrics'][k]-1 for k in ['charged_comoving','U1_comoving','U1_mean_p_over_mu']};checks=dict(toy_reference=max(t['relative_hole_error'] for t in toy)<1e-7,sub_ulp_holes=0<toy[2]['availability'][2]<1e-18 and toy[2]['hole_coordinate'],warm_bounds=all(h['min_f']>=0 and h['max_fermion_f']<=1 and h['minimum_fermion_availability']>0 for r in runs for h in r['history']),warm_entropy=min(r['entropy_gain'] for r in runs)>=0,warm_number_balance=max(r['max_relative_coordinate_balance'] for r in runs)<1e-8,warm_local_energy=max(r['max_local_collision_energy'] for r in runs)<1e-20,step_comparison=relative_number<1e-4)
 result=dict(claim_id='CC10_WARM_HOLE_SOLVER_CONTROL_V3',checks=checks,float64_mantissa_bits=int(np.finfo(float).nmant),longdouble_mantissa_bits=int(np.finfo(np.longdouble).nmant),toy=toy,warm=runs,step_relative_number_L1=relative_number,step_relative_observable_changes=comparisons,initial_N=N,physical_averaged_particle_energy0=physical_energy0,scope='Fixed actualwarm orbit collision operator, stable hole coordinates; 5e-5 collision-equivalent dN only. Averagedparticle energy need not conserve: localenergy does, while covariance exchangesaction. No newcoupledbackgroundhistory orphysicalenergyproof fromNewtonroundoffallowance.',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,toy=toy,relative_number_L1=relative_number,observable_changes=comparisons,runtime=result['runtime_seconds'])),flush=True);assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
