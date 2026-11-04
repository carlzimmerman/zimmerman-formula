from control_v2 import *
from scipy.sparse import eye
from scipy.sparse.linalg import spsolve
def traced_step(events,state,dt,tol=2e-9,maxiter=30):
 old=state.copy();new=state.copy();ferm=events.eta<0;switches=0
 for it in range(maxiter):
  # Switch coordinates before approaching either representational boundary.
  zz=new.Z/new.measure
  tohole=ferm&(~new.holes)&(zz>.65);tonumber=new.holes&(zz>.65);switch=tohole|tonumber
  if np.any(switch):
   new.Z[switch]=new.measure[switch]-new.Z[switch];new.holes[switch]=~new.holes[switch]
   old.Z[switch]=old.measure[switch]-old.Z[switch];old.holes[switch]=~old.holes[switch];switches+=int(sum(switch))
  signs=np.where(new.holes,-1.,1.);rhs=signs*new.rhs(events);res=new.Z-old.Z-dt*rhs
  # Scaling by the represented coordinate retains tiny holes rather than
  # declaring them accurate merely because total fermion number is order one.
  forward,reverse,_,_=new.products(events)
  gross=np.asarray(abs(events.S)@(events.coefficient*(forward+reverse))).ravel()
  # Roundoff in subtracting balanced event fluxes is distinct from physical
  # holes. Permit only a small multiple of that computed floating error.
  rounding=32*np.finfo(float).eps*dt*gross
  scale=1e-30*events.measure+np.maximum(abs(old.Z),abs(new.Z))+rounding/tol
  norm=float(max(abs(res)/np.maximum(scale,1e-300)))
  print('trace_pre',it,'worst',int(np.argmax(abs(res)/np.maximum(scale,1e-300))),'norm',norm,'res',float(res[np.argmax(abs(res)/np.maximum(scale,1e-300))]),'Z',float(new.Z[np.argmax(abs(res)/np.maximum(scale,1e-300))]),flush=True)
  if norm<tol:return new,dict(iterations=it,residual=norm,coordinate_switches=switches)
  delta=spsolve(eye(len(res),format='csr')-dt*new.jacobian(events),-res)
  if not np.all(np.isfinite(delta)):raise RuntimeError('hole Newton nonfinite correction')
  alpha=1.;lo=delta<0
  if np.any(lo):alpha=min(alpha,float(min(-.995*new.Z[lo]/delta[lo])))
  hi=ferm&(delta>0)
  if np.any(hi):alpha=min(alpha,float(min(.995*(new.measure[hi]-new.Z[hi])/delta[hi])))
  if alpha<=1e-18:raise RuntimeError('hole Newton boundary blocked')
  base=float(np.linalg.norm(res/np.maximum(scale,1e-300)))
  for _ in range(24):
   trial=new.copy();trial.Z+=alpha*delta;rr=trial.Z-old.Z-dt*np.where(trial.holes,-1.,1.)*trial.rhs(events)
   score=float(np.linalg.norm(rr/np.maximum(scale,1e-300)))
   if score<base*(1-1e-6*alpha)+1e-15:break
   alpha*=.5
  else:raise RuntimeError('hole Newton line search')
  print('trace_step',it,'alpha',alpha,'delta_worst',float(delta[np.argmax(abs(res)/np.maximum(scale,1e-300))]),'min_boundary_idx',int(np.argmin(np.where(delta<0,-.995*new.Z/np.minimum(delta,-1e-300),np.inf))),'relative_min',float(np.min(delta/np.maximum(new.Z,1e-300))),'score',score,'base',base,flush=True)
  new=trial
 raise RuntimeError('hole Newton iteration budget; worst='+str(int(np.argmax(abs(res)/np.maximum(scale,1e-300))))+' norm='+str(norm)+' availability='+str(float(new.arrays()[1][np.argmax(abs(res)/np.maximum(scale,1e-300))])))

def main_trace(out):
 start=time.monotonic();prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_warm001/result.json').read_text());c=prior['case'];st=prior['state'];Y=np.array(st['Y']);q=np.array(c['q']);W=np.array(c['W']);N=st['N'];bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];orb=model.orbit(N,Y,E=st['E']);ev=averaged_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W,2);H=model.hubble(N);state=QuantumState(ev.measure,ev.eta,Y=Y);state,_=implicit_step(ev,state,1e-5/H,tol=2e-9)
 try:
  new,d=traced_step(ev,state,1e-5/H)
  result=dict(completed=True,diagnostics=d)
 except RuntimeError as exc:result=dict(completed=False,reason=str(exc))
 result.update(claim_id='CC10_NEWTON_TRACE_V1',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main_trace(sys.argv[1])
