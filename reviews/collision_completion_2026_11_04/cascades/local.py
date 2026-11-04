"""Bounded full-network quantum local populations, delay and force tests."""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from network import ROOT,table
from reaction import full_events,moments,thermal,serial_moments

def grid(bulk=14):
 q=np.unique(np.r_[1e-4,np.geomspace(.001,.3,5),np.linspace(.5,20.,bulk),30.,50.,80.]);edges=np.r_[0.,(q[:-1]+q[1:])/2,q[-1]+(q[-1]-q[-2])/2];return q,np.diff(edges**3)/3

def evolve(ev,f0,duration,scale):
 # BDF resolves the complete gain/loss system. The RHS is quantum-clipped for
 # nonlinear trial states by ReactionEvents; accepted bounds are audited.
 sol=solve_ivp(lambda z,f:ev.rhs(f)/scale,(0,duration*scale),f0,method='BDF',jac=lambda z,f:ev.rhs_jacobian(f)/scale,rtol=3e-5,atol=1e-11,t_eval=np.linspace(0,duration*scale,31))
 rows=[];initial=moments(ev,f0);norm=initial['total_energy'];n0=initial['charged_number']
 for z,f in zip(sol.t,sol.y.T):
  m=serial_moments(ev,f);m.update(time_mu=float(z/scale),time_B_lifetimes=float(z),energy_relative_error=(m['total_energy']-norm)/max(norm,1e-300),charged_fraction=m['charged_number']/max(n0,1e-300),min_f=float(f.min()),max_fermion_f=float(f[ev.eta<0].max()));rows.append(m)
 return dict(success=bool(sol.success),message=sol.message,nfev=sol.nfev,njev=sol.njev,history=rows,final_f=sol.y[:,-1].tolist(),initial_f=f0.tolist())

def main(out,bulk='14'):
 start=time.monotonic();q,W=grid(int(bulk));cases=[]
 for x in (3.,5.,25.4000254000381):
  data=table(x);ev=full_events(data,.004,q,W,angles=4);feq=thermal(ev,.008)
  audit=ev.audit(feq);species,chs=__import__('network').signed_lift(data);signed=full_events(data,.004,q,W,angles=4,signed=True);sfeq=thermal(signed,.008,.001);signed_audit=signed.audit(sfeq);charge=np.repeat([g['charge'] for g in signed.groups],len(q));charge_res=float(np.max(abs(np.sum(signed.stoich*charge[signed.index],axis=1))))
  n=len(q);f0=np.zeros(len(ev.measure));f0[ev.by['Fc_0']*n:(ev.by['Fc_0']+1)*n]=1/(np.exp(q)+1)
  B=next(g for g in data['groups'] if g['id']=='S8_1');scale=B['width']
  run=evolve(ev,f0,10/scale,scale);cases.append(dict(x=x,groups=[g['id'] for g in ev.groups],audit=audit,signed_audit=signed_audit,signed_charge_event_residual=charge_res,scale_width=scale,run=run))
  print(x,audit,run['success'],run['history'][-1]['charged_fraction'],run['history'][-1]['neutral_force'],flush=True)
 # A dilute parent pulse directly measures the delayed and returning cascade.
 data=table(3.);ev=full_events(data,.004,q,W,angles=6);n=len(q);f0=np.zeros(len(ev.measure));f0[ev.by['S8_1']*n:(ev.by['S8_1']+1)*n]=1e-5/(np.exp(q)+1);scale=next(g for g in data['groups'] if g['id']=='S8_1')['width'];pulse=evolve(ev,f0,40/scale,scale)
 last=pulse['history'][-1];initial=moments(ev,f0);pulse['terminal_charged_per_parent']=last['charged_number']/initial['number'][ev.by['S8_1']];pulse['terminal_prediction']=next(g for g in data['groups'] if g['id']=='S8_1')['terminal_charged']
 checks=dict(event_energy=max(c['audit']['energy_residual'] for c in cases)<1e-11,thermal_detailed_balance=max(c['audit']['detailed_balance_relative'] for c in cases)<1e-9,signed_thermal_detailed_balance=max(c['signed_audit']['detailed_balance_relative'] for c in cases)<1e-9,signed_charge=max(c['signed_charge_event_residual'] for c in cases)<1e-12,evolutions_completed=all(c['run']['success'] for c in cases) and pulse['success'],energy_conserved=max(abs(r['energy_relative_error']) for c in cases for r in c['run']['history'])<1e-7,fermion_bounds=max(r['max_fermion_f'] for c in cases for r in c['run']['history'])<=1+1e-7,positive=max(-r['min_f'] for c in cases for r in c['run']['history'])<1e-7)
 result=dict(claim_id='CC10_QUANTUM_FULL_CASCADE_LOCAL',cases=cases,pulse=pulse,q=q.tolist(),W=W.tolist(),checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='All physical tree FFS/SSS groups with inverse, Pauli/Bose factors and explicit massive neutral energy/force. Static background tests, not cosmological history; diagonal four-singlet approximation and omitted vectors/loops remain.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,result['runtime_seconds']);assert all(checks.values()),checks
if __name__=='__main__':main(*sys.argv[1:])
