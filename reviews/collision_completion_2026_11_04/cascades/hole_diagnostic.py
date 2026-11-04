"""Observe conditioning/roundoff scales in actual warm mixed-hole Newton step."""
import sys,json,time,resource,math
from pathlib import Path
import numpy as np
from scipy.sparse import eye
from scipy.sparse.linalg import spsolve
from network import ROOT
from vertices import VertexBackground
from averaged import averaged_events
from orbit_frozen_cc10 import GenericOrbit,T0
from holes_frozen001 import QuantumState

def main(out):
 start=time.monotonic();data=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/warm_checkpoint001.json').read_text());c=data['case'];st=data['state'];q=np.array(c['q']);W=np.array(c['W']);Y=np.array(st['Y']);N=st['N'];bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];orb=model.orbit(N,Y,E=st['E']);ev=averaged_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W,2);dt=1e-7/model.hubble(N);old=QuantumState(ev.measure,ev.eta,Y=Y);new=old.copy();iterations=[];reason='iteration budget'
 for it in range(100):
  signs=np.where(new.holes,-1.,1.);rhs=signs*new.rhs(ev);res=new.Z-old.Z-dt*rhs;scale=1e-30*ev.measure+np.maximum(abs(old.Z),abs(new.Z));relative=abs(res)/np.maximum(scale,1e-300);f,av=new.arrays();a,b,_,_=new.products(ev);noise=dt*np.asarray(abs(ev.S)@(ev.coefficient*(a+b))).ravel()*np.finfo(float).eps/np.maximum(scale,1e-300);order=np.argsort(relative)[-4:][::-1];J=new.jacobian(ev)
  top=[]
  for j in order:top.append(dict(group=model.groups[j//len(q)]['id'],q=float(q[j%len(q)]),hole=bool(new.holes[j]),occupation=float(f[j]),availability=float(av[j]),coordinate=float(new.Z[j]),scaled_residual=float(relative[j]),roundoff_scale_estimate=float(noise[j]),dt_diagonal_stiffness=float(abs(dt*J[j,j]))))
  iterations.append(dict(iteration=it,max_residual=float(relative.max()),max_roundoff_scale=float(noise.max()),top=top))
  if it%10==0:print(iterations[-1],flush=True)
  if relative.max()<2e-8:reason='converged';break
  delta=spsolve(eye(len(Y),format='csr')-dt*J,-res);alpha=1.;lo=delta<0
  if np.any(lo):alpha=min(alpha,float(min(-.995*new.Z[lo]/delta[lo])))
  hi=(ev.eta<0)&(delta>0)
  if np.any(hi):alpha=min(alpha,float(min(.995*(new.measure[hi]-new.Z[hi])/delta[hi])))
  if alpha<=1e-18:reason='boundary blocked';break
  base=float(np.linalg.norm(res/np.maximum(scale,1e-300)))
  for ls in range(24):
   trial=new.copy();trial.Z+=alpha*delta;rr=trial.Z-old.Z-dt*np.where(trial.holes,-1.,1.)*trial.rhs(ev);score=float(np.linalg.norm(rr/np.maximum(scale,1e-300)))
   if score<base*(1-1e-6*alpha)+1e-15:break
   alpha*=.5
  else:reason='line search';break
  new=trial
 result=dict(claim_id='CC10_WARM_HOLE_NEWTON_DIAGNOSTIC',reason=reason,dt=dt,iterations=iterations,checks=dict(finite_record=all(math.isfinite(i['max_residual']) for i in iterations)),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual frozen warm orbit Newton diagnostic. Roundoff estimates are first-order operation-scale diagnostics, not rigorous numerical error bounds. No accepted state or coupled history claimed; this instrumented path holds initial coordinate flags fixed and does not reproduce dynamic switching exactly.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(reason,len(iterations))
if __name__=='__main__':main(sys.argv[1])
