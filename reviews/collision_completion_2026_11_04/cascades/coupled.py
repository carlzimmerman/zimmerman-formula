"""Early finite direct scalar/25-population history with quantum return channels.

Leapfrog scalar drift/kick, conservative implicit quantum collisions at midpoint,
and explicit FRW work ledger. Number coordinates are evolved, not tiny f tails.
"""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.sparse import diags,eye
from scipy.sparse.linalg import spsolve
from network import ROOT
from background import Background
from reaction import full_events,moments
from local import grid

T0=.004657258204883617;MU=2e6;XI=.02;MASS=62.
def hubble(N):return math.sqrt(math.pi**2*106.75/90)*(T0*math.exp(-N))**2*MU/(2.435e18*XI**2)

def collision_step(ev,Y,dt,tol=2e-9):
 old=Y.copy();new=Y.copy();ferm=ev.eta<0;m=ev.measure
 for it in range(30):
  f=new/m;rhs=np.asarray(ev.S@ev.flux(f)).ravel();res=new-old-dt*rhs
  norm=float(np.max(abs(res)/(1e-13+np.maximum(abs(old),abs(new)))))
  if norm<tol:return new,it
  J=diags(m)@ev.rhs_jacobian(f)@diags(1/m);delta=spsolve(eye(len(Y),format='csr')-dt*J,-res);alpha=1.
  if not np.all(np.isfinite(delta)):raise RuntimeError('nonfinite number Newton correction')
  lo=delta<0
  if np.any(lo):alpha=min(alpha,float(np.min(-.995*new[lo]/delta[lo])))
  hi=ferm&(delta>0)
  if np.any(hi):alpha=min(alpha,float(np.min(.995*(m[hi]-new[hi])/delta[hi])))
  if alpha<=1e-15:raise RuntimeError('number Newton boundary blocked')
  base=float(np.linalg.norm(res))
  for ls in range(20):
   trial=new+alpha*delta;r=trial-old-dt*np.asarray(ev.S@ev.flux(trial/m)).ravel()
   if np.linalg.norm(r)<base*(1-1e-6*alpha)+1e-24:break
   alpha*=.5
  else:raise RuntimeError('number Newton line search')
  new=trial
 raise RuntimeError('number Newton iteration budget')

def run(bg,potential,dtbase,Nend,neutral_force=True,bulk=12,angles=2):
 q,W=grid(bulk);n=len(q);x=.18444259422092926;v=0.;N=0.;clock=0.;work=0.;accepted=0;rejected=0;history=[];max_collision_energy=0.;max_inverse_return=0.;max_omitted_fraction=0.;max_vector_parent_energy=0.;minimum_f=0.;maximum_fermion_f=0.;dt=dtbase
 d=bg.at(x);ev=full_events(d,T0,q,W,angles=angles,source=d['current_source']);f=np.zeros(len(ev.measure));f[ev.by['Fc_0']*n:(ev.by['Fc_0']+1)*n]=1/(np.exp(q)+1);Y=ev.measure*f
 # Tiny positive roundoff seed regularizes fractional entropy interpolation at
 # empty cells; its actual total number and energy are separately recorded.
 seed=1e-35*ev.measure;Y+=seed;seednumber=float(seed.sum()*T0**3);seedenergy=float((seed@ev.energy)*T0**3)
 def obs(xx,NN,YY,vv):
  dd=bg.at(xx);t=T0*math.exp(-NN);mm=np.array([g['mass'] for g in dd['groups']]);slope=np.array([g['dm2_dx'] for g in dd['groups']]);ener=np.sqrt(mm[:,None]**2+(t*q[None,:])**2);nums=YY.reshape((-1,n))*t**3;charged=np.array([g['charged'] for g in dd['groups']]);force=np.sum(nums*slope[:,None]/(2*np.maximum(ener,1e-300)),axis=1);rho=float(np.sum(nums*ener));pressure=float(np.sum(nums*(t*q[None,:])**2/(3*np.maximum(ener,1e-300))));kin=MASS*vv*vv/2;ng=np.sum(nums,axis=1)
  return dict(force=float(force.sum() if neutral_force else force@charged),neutral_force=float(force@(~charged)),charged_force=float(force@charged),rho=rho,pressure=pressure,E=float(potential(xx))+kin+rho,kinetic=kin,number=ng,neutral_massive_energy=float(np.sum(nums*ener,axis=1)@((~charged)&(mm>1e-12))),group_force=force,masses=mm,groups=dd['groups'])
 initial=obs(x,N,Y,v);E0=initial['E'];scale=initial['rho'];n0=float(initial['number']@np.array([g['charged'] for g in initial['groups']]))
 def record(o):
  qch=np.array([g['charged'] for g in o['groups']]);h=dict(time_mu=clock,N=N,Tc=T0*math.exp(-N),x=x,velocity=v,charged_fraction=float(o['number']@qch/n0),charged_force=o['charged_force'],neutral_force=o['neutral_force'],neutral_massive_energy=o['neutral_massive_energy'],total_energy=o['E'],energy_ledger_error=(o['E']+work-E0)/scale,number=o['number'].tolist(),force=o['group_force'].tolist(),groups=[g['id'] for g in o['groups']]);history.append(h)
 record(initial);old=initial
 while N<Nend-1e-15:
  dt=min(dt,dtbase,(Nend-N)/hubble(N));a0=(float(potential(x,1))+old['force'])/MASS;vh=(v-.5*dt*a0)*math.exp(-1.5*hubble(N)*dt);xm=x+.5*dt*vh;Nm=N+.5*hubble(N)*dt
  try:
   dd=bg.at(xm);ev=full_events(dd,T0*math.exp(-Nm),q,W,angles=angles,source=dd['current_source']);fn=Y/ev.measure;before=float(ev.energy@Y);Yn,its=collision_step(ev,Y,dt);after=float(ev.energy@Yn);max_collision_energy=max(max_collision_energy,abs(after-before)/max(abs(before),1e-300));newN=N+hubble(Nm)*dt;newx=xm+.5*dt*vh;o=obs(newx,newN,Yn,vh);an=(float(potential(newx,1))+o['force'])/MASS;newv=vh*math.exp(-1.5*hubble(newN)*dt)-.5*dt*an;o=obs(newx,newN,Yn,newv)
   rates=ev.coefficient*ev.products(fn)[0];reverse=ev.coefficient*ev.products(fn)[1];ret=np.array([sum(ev.groups[k]['charged'] for k in lab[1:3])-ev.groups[lab[0]]['charged'] for lab in ev.labels]);max_inverse_return=max(max_inverse_return,float(sum(rates*np.maximum(ret,0))));om=float(ev.omitted_by_parent@fn);inc=float(ev.included_by_parent@fn);max_omitted_fraction=max(max_omitted_fraction,om/max(om+inc,1e-300));ff=Yn/ev.measure;minimum_f=min(minimum_f,float(ff.min()));maximum_fermion_f=max(maximum_fermion_f,float(ff[ev.eta<0].max()))
   # Total FRW energy equation; neutral-force suppression deliberately violates
   # scalar+gas energy exchange and exposes the missing-force inconsistency.
   w0=3*hubble(N)*(2*old['kinetic']+old['rho']+old['pressure']);w1=3*hubble(newN)*(2*o['kinetic']+o['rho']+o['pressure']);work+=dt*(w0+w1)/2
   x,v,N,Y,old=newx,newv,newN,Yn,o;clock+=dt;accepted+=1
   if accepted%20==0 or N>=Nend-1e-15:record(o)
   dt=min(dtbase,dt*1.5)
  except RuntimeError as exc:
   rejected+=1;dt*=.25
   if dt<1.:return dict(completed=False,reason=str(exc),accepted=accepted,rejected=rejected,history=history)
  if accepted>5000:return dict(completed=False,reason='step budget',accepted=accepted,rejected=rejected,history=history)
 return dict(completed=True,accepted=accepted,rejected=rejected,history=history,final_number=Y.tolist(),final_f=(Y/ev.measure).tolist(),q=q.tolist(),W=W.tolist(),dtbase=dtbase,bulk=bulk,angles=angles,neutral_force=neutral_force,seed_physical_number_mu3=seednumber,seed_energy_mu4=seedenergy,max_collision_energy_relative=max_collision_energy,max_omitted_occupied_forward_fraction=max_omitted_fraction,max_charged_return_rate_comoving=max_inverse_return,min_f=minimum_f,max_fermion_f=maximum_fermion_f)

def main(out,dt='100000',Nend='0.00001',mode='both',bulk='12',stride='1'):
 start=time.monotonic();bg=Background(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_background001/result.json',int(stride));packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet'];r=packet['global_profile'];potential=CubicSpline(r['grid'],r['V0_origin_subtracted_mu4'],bc_type=((1,r['origin_force']),(2,0)));cases=[]
 for force in ([True,False] if mode=='both' else [mode=='full']):
  c=run(bg,potential,float(dt),float(Nend),force,int(bulk));cases.append(c);print('force',force,'completed',c['completed'],'steps',c['accepted'],'last',c['history'][-1],flush=True)
 checks=dict(reached_end=all(c['completed'] for c in cases),quantum_bounds=all(c.get('min_f',-1)>=0 and c.get('max_fermion_f',2)<=1+1e-8 for c in cases),collision_energy=all(c.get('max_collision_energy_relative',1)<1e-8 for c in cases),full_force_energy_ledger=all(max(abs(h['energy_ledger_error']) for h in c['history'])<.01 for c in cases if c.get('neutral_force',False)))
 result=dict(claim_id='CC10_EARLY_COUPLED_QUANTUM_CASCADE',cases=cases,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='First N<=declared endpoint, actual leading gravity global potential and initial FD packet, all25 physical FFS/SSS groups with quantum gains/inverses and massive neutral force. Direct scalar dynamics; empty-node seed quantified. SSS/FFS-only, diagonal parent block approximation, no gauge2<->2, no late resonance or cold photino conclusion. Suppressed-neutral-force run is an intentional energy-violating diagnostic.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,result['runtime_seconds']);assert all(checks.values()),checks
if __name__=='__main__':main(*sys.argv[1:])
