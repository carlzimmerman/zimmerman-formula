"""Warm-window full25-population quantum/field averaging, all energy retained.

The total energy equation has no collision sink because every phase-local
event retains its parent and daughters. This is a declared orbit-averaged
diagonal-species closure, separately tested against direct early dynamics.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from consistent_background_frozen import ConsistentVertexBackground as VertexBackground
from averaged import averaged_events,grid,covariance,number_rhs
from coupled_v4 import collision_step
from orbit_frozen_cc10 import GenericOrbit,T0,MU,XI

def work(orbit):
 g=orbit['gas'];return 3*float(orbit['weights']@(orbit['kin2']+g['rho']+g['pressure']))

def evolve(output,Nend,maxstep,order,phases,angles,seed=1e-35,resume=None):
 start=time.monotonic();bgpath=ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json'
 bg=VertexBackground(bgpath);q,W=grid(order);model=GenericOrbit(bg,q,W,phases)
 Y,orb=model.initial(seed);E=orb['E'];N=0.;E0=E;J0=orb['J'];gas0=orb['gas']['rho']@orb['weights'];initialY=Y.copy()
 accepted=rejected=0;step=min(1e-6,maxstep);history=[];maxcov=0.;maxlocalenergy=0.;maxomit=0.;maxfermstep=0.;maxseed=seed;hwork=0.;maxentropy_drop=0.
 if resume is not None:
  prior=json.loads(Path(resume).read_text());state=prior['state'];Y=np.array(state['Y']);E=state['E'];N=state['N'];E0=state['E0'];J0=state['J0'];gas0=state['gas0'];hwork=state['work'];initialY=np.array(state['initialY']);model.J0=J0;model.last_x=state['xmid'];orb=model.orbit(N,Y,E=E,commit=True)
 Nstart=N;proper_time=0.
 def details():
  h=model.summary(N,Y,orb);h.update(time_mu=proper_time,f=(Y/model.measure).tolist(),energy_work_ledger=(E+hwork-E0)/gas0,charged_fraction=float(Y.reshape(model.ns,model.n).sum(axis=1)@model.charged/(initialY.reshape(model.ns,model.n).sum(axis=1)@model.charged)))
  return h
 history.append(details());reason='target cooling reached'
 def snapshot(partial):
  return dict(claim_id='CC10_AVERAGED_QUANTUM_FIELD_NETWORK',partial=partial,case=dict(reason=reason,accepted=accepted,rejected=rejected,history=history,mu_GeV=MU,phase_nodes=phases,momentum_order_per_panel=order,angles=angles,q=q.tolist(),W=W.tolist(),groups=[g['id'] for g in model.groups],max_action_covariance_step_error=maxcov,max_phase_energy_residual=maxlocalenergy,max_occupied_forward_omission=maxomit,max_fermionic_change_per_orbit=maxfermstep,max_entropy_decrease=maxentropy_drop,seed_occupation=seed),state=dict(Y=Y.tolist(),E=E,N=N,E0=E0,J0=J0,gas0=gas0,work=hwork,initialY=initialY.tolist(),xmid=orb['xmid']),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 while N<Nend-1e-14:
  step=min(step,maxstep,Nend-N)
  try:
   ev=averaged_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W,angles)
   maxlocalenergy=max(maxlocalenergy,ev.local_energy_residual)
   f=Y/ev.measure;om=float(ev.omitted_by_parent@f);inc=float(ev.included_by_parent@f);maxomit=max(maxomit,om/max(om+inc,1e-300))
   C=number_rhs(ev,Y);maxfermstep=max(maxfermstep,float(max(abs(C[ev.eta<0]/ev.measure[ev.eta<0])))*orb['period'])
   H=model.hubble(N+step/2);Yn,iterations=collision_step(ev,Y,step/H,tol=2e-8)
   # Compare action at fixedN,E with the collision covariance before expansion.
   coll=model.orbit(N,Yn,E=E);pred=-(T0*math.exp(-N))**3*float(ev.energy_average@(Yn-Y))/orb['omega'];actual=coll['J']-orb['J']
   cov_err=abs(actual-pred)/max(abs(actual),abs(pred),orb['J']*1e-6,1e-30)
   oldwork=work(orb);Ep=E-step*oldwork;neworb=model.orbit(N+step,Yn,E=Ep)
   En=E-step*(oldwork+work(neworb))/2;neworb=model.orbit(N+step,Yn,E=En)
   relative_number_change=float(sum(abs(Yn-Y)))/max(float(sum(Y)),1e-300)
   if relative_number_change>.04 and step>1e-10:raise RuntimeError('number-change step control')
   # Every accepted implicit collision step is checked for entropy increase.
   from quantum import entropy
   dS=entropy(Yn/ev.measure,ev.measure,ev.eta)-entropy(Y/ev.measure,ev.measure,ev.eta)
   maxentropy_drop=max(maxentropy_drop,-dS)
   if dS<-1e-9:raise RuntimeError('quantum entropy decreased')
   hwork+=E-En;proper_time+=step/H;N+=step;Y=Yn;E=En;orb=neworb;model.last_x=orb['xmid'];accepted+=1;maxcov=max(maxcov,cov_err)
   if accepted==1 or N-history[-1]['N']>max((Nend-Nstart)/24,1e-12) or N>=Nend-1e-14:history.append(details())
   if accepted%5==0:Path(output).write_text(json.dumps(snapshot(True),indent=2)+'\n')
   step=min(maxstep,step*1.5)
  except RuntimeError as exc:
   rejected+=1;step*=.25
   if step<1e-12:reason=str(exc);break
  if time.monotonic()-start>205:reason='bounded checkpoint before wall cap';break
  if accepted>5000:reason='step count checkpoint';break
 if abs(history[-1]['N']-N)>1e-14:history.append(details())
 result=snapshot(False);result['case']['reason']=reason
 result['checks']=dict(reached_requested_N=N>=Nend-1e-12,positive_populations=float(min(Y))>=0,fermionic_bound=float(max((Y/model.measure)[model.eta<0]))<=1+1e-9,local_event_energy=maxlocalenergy<1e-11,nondecreasing_quantum_entropy=maxentropy_drop<1e-9,retained_orbit=orb['x_inner']>=model.xlo and orb['x_outer']<=model.xhi)
 result['checks']={key:bool(value) for key,value in result['checks'].items()}
 result['scope']='All25physicaltreeFFS/SSSgroups, inverse/Pauli/Bose terms and actualmassivegasforce onleadingprofile; diagonalgroup andsloworbitaverage closure, no2to2/noVector/no4singletmemoryhere. Allparticleenergyretained. Warmwindow energy-basedorbit with exacteventenergy and conserved entropyprojection; notfullcosmologicalcandidate.'
 Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=result['checks'],reason=reason,last=history[-1],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])));assert all(result['checks'].values()),result['checks']

if __name__=='__main__':
 evolve(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),float(sys.argv[7]) if len(sys.argv)>7 else 1e-35,sys.argv[8] if len(sys.argv)>8 else None)
