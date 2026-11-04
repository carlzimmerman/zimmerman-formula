"""Direct actual warm-checkpoint bridge across F/C crossing, no phase averaging."""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
from network import ROOT
from vertices import VertexBackground
from reaction import full_events
from coupled_v4 import collision_step
from orbit_frozen_cc10 import GenericOrbit,MASS,T0

def main(out,checkpoint,periods='3',steps_per_period='256'):
 start=time.monotonic();saved=json.loads(Path(checkpoint).read_text());s=saved['state'];case=saved.get('case',{});q=np.array(s.get('q',case.get('q')));W=np.array(s.get('W',case.get('W')));N=float(s['N']);Y=np.array(s['Y']);E=float(s['E']);bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,phase_nodes=24);model.J0=float(s.get('J0',1));model.last_x=float(s['xmid']) if 'xmid' in s else None;orb=model.orbit(N,Y,E=E,commit=True);x=orb['x_inner'];v=0.;time_mu=0.;work=0.;E0=E;N0=N;end=float(periods)*orb['period'];dt0=orb['period']/int(steps_per_period);dt=dt0;accepted=rejected=0;history=[];max_ce=0.;max_omit=0.;steps_f=0.
 def obs(xx,nn,yy,vv):
  g=model.gas(xx,nn,yy);rho=float(g['rho'][0]);p=float(g['pressure'][0]);force=float(g['force'][0]);kin=MASS*vv*vv/2;et=float(model.v(xx))+rho+kin
  return dict(rho=rho,pressure=p,force=force,kin=kin,E=et,force_by=g['force_by'][0])
 old=obs(x,N,Y,v);initial_offset=old['E']-E0;initial_counts=Y.reshape(model.ns,model.n).sum(axis=1);initial_charged=float(initial_counts@model.charged)
 def record(o):
  current=model.orbit(N,Y,E=o['E'],commit=True);counts=Y.reshape(model.ns,model.n).sum(axis=1);f=Y/model.measure;physical=(T0*math.exp(-N))**3;entropy=2*math.pi**2/45*106.75*(T0*math.exp(-N)/.02)**3;history.append(dict(time_mu=time_mu,N=N,Tc=T0*math.exp(-N),x=x,velocity=v,action=current['J'],energy=o['E'],energy_ledger_error=(o['E']+work-E0)/max(abs(E0),1e-300),charged_fraction=float(counts@model.charged/initial_charged),Y_charged=float(counts@model.charged*physical/entropy),yields_by_group=(counts*physical/entropy).tolist(),number_comoving=counts.tolist(),force_by_group=o['force_by'].tolist(),neutral_force=float(o['force_by']@(~model.charged)),charged_force=float(o['force_by']@model.charged),f=f.tolist(),groups=[g['id'] for g in model.groups],min_f=float(f.min()),max_fermion_f=float(f[model.eta<0].max())))
 record(old)
 reason='requested proper-time duration reached'
 while time_mu<end*(1-1e-14):
  dt=min(dt,dt0,end-time_mu);H=model.hubble(N);a0=(float(model.v(x,1))+old['force'])/MASS;vh=(v-.5*dt*a0)*math.exp(-1.5*H*dt);xm=x+.5*dt*vh;Nm=N+.5*H*dt
  try:
   d=bg.at(xm);ev=full_events(d,T0*math.exp(-Nm),q,W,angles=2,source=d['current_source']);before=float(ev.energy@Y);Yn,it=collision_step(ev,Y,dt);after=float(ev.energy@Yn);max_ce=max(max_ce,abs(after-before)/max(abs(before),1e-300));ff=Y/ev.measure;om=float(ev.omitted_by_parent@ff);inc=float(ev.included_by_parent@ff);max_omit=max(max_omit,om/max(om+inc,1e-300));steps_f=max(steps_f,float(np.max(abs((Yn-Y)/ev.measure))));newN=N+model.hubble(Nm)*dt;newx=xm+.5*dt*vh;o=obs(newx,newN,Yn,vh);an=(float(model.v(newx,1))+o['force'])/MASS;newv=vh*math.exp(-1.5*model.hubble(newN)*dt)-.5*dt*an;o=obs(newx,newN,Yn,newv);w0=3*H*(2*old['kin']+old['rho']+old['pressure']);w1=3*model.hubble(newN)*(2*o['kin']+o['rho']+o['pressure']);work+=dt*(w0+w1)/2;x,v,N,Y,old=newx,newv,newN,Yn,o;time_mu+=dt;accepted+=1;dt=min(dt0,dt*1.5)
   if accepted%32==0 or time_mu>=end*(1-1e-14):record(o)
  except RuntimeError as exc:
   rejected+=1;dt*=.25
   if dt<.1:reason=str(exc);break
  if accepted>6000:reason='step budget';break
 completed=time_mu>=end*(1-1e-14);checks=dict(reached_duration=completed,collision_energy=max_ce<1e-8,energy_ledger=max(abs(h['energy_ledger_error']) for h in history)<2e-4,positive=min(h['min_f'] for h in history)>=0,fermion_bound=max(h['max_fermion_f'] for h in history)<=1+1e-8)
 result=dict(claim_id='CC10_WARM_DIRECT_QUANTUM_BRIDGE',completed=completed,reason=reason,checks=checks,history=history,q=q.tolist(),W=W.tolist(),initial_N=N0,requested_duration_mu=end,initial_period_mu=orb['period'],steps_per_period=int(steps_per_period),initial_energy_offset=initial_offset,accepted=accepted,rejected=rejected,max_collision_energy_relative=max_ce,max_population_weighted_forward_omission=max_omit,max_occupation_change_per_step=steps_f,state=dict(N=N,E=old['E'],Y=Y.tolist(),q=q.tolist(),W=W.tolist(),J0=model.J0),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual all25group warm checkpoint direct scalar+quantum1<->2 evolution across ordering crossing; finite projected momentum support; SSS/FFS only, loop gaugino kinematic masses/current conversions. No phase averaging inside this test.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,reason,'initial',history[0]['action'],'last',history[-1]['action'],'chargedratio',history[-1]['charged_fraction'],'N',N,'runtime',result['runtime_seconds']);assert all(checks.values()),checks

if __name__=='__main__':main(*sys.argv[1:])
