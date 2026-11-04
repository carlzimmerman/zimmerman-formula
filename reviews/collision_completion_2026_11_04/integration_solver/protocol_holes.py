"""Explicit-availability solver adapter for exact-angular number operators.

Backend protocol (all flat physical node arrays):
  number_rhs(f, availability) -> dY/dtau
  number_jacobian(f, availability) -> CSR d(dY/dtau)/dY
  number_gross(f, availability) -> sum |stoich| k(F+R), nonnegative
plus measure and eta. Jacobians are with respect to physical NUMBER Y,
not occupation f. This distinction removes an erroneous extra 1/measure.
No ReactionEvents.index/S/flux interface is required of such a backend.
"""
import sys
from pathlib import Path
import numpy as np
from scipy.sparse import diags,eye
from scipy.sparse.linalg import spsolve
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'integration'))
from holes_v2 import QuantumState as BaseState

class QuantumState(BaseState):
 def copy(self):return QuantumState(self.measure,self.eta,Z=self.Z,holes=self.holes)
 def rhs(self,events):
  if hasattr(events,'number_rhs'):
   f,a=self.arrays();return np.asarray(events.number_rhs(f,a)).ravel()
  return super().rhs(events)
 def jacobian(self,events):
  if hasattr(events,'number_jacobian'):
   f,a=self.arrays();s=np.where(self.holes,-1.,1.);return diags(s)@events.number_jacobian(f,a)@diags(s)
  return super().jacobian(events)
 def gross(self,events):
  if hasattr(events,'number_gross'):
   f,a=self.arrays();return np.asarray(events.number_gross(f,a)).ravel()
  if hasattr(events,'S'):
   fwd,rev,_,_=self.products(events);return np.asarray(abs(events.S)@(events.coefficient*(fwd+rev))).ravel()
  raise TypeError('exact-number backend must supply number_gross for roundoff control')

def implicit_step(events,state,dt,tol=2e-8,maxiter=100):
 old=state.copy();new=state.copy();ferm=events.eta<0;switches=0
 for it in range(maxiter):
  z=new.Z/new.measure;switch=ferm&(z>.65)
  if np.any(switch):
   new.Z[switch]=new.measure[switch]-new.Z[switch];new.holes[switch]=~new.holes[switch]
   old.Z[switch]=old.measure[switch]-old.Z[switch];old.holes[switch]=~old.holes[switch];switches+=int(sum(switch))
  signs=np.where(new.holes,-1.,1.);rhs=signs*new.rhs(events);res=new.Z-old.Z-dt*rhs;gross=new.gross(events)
  if np.any(gross<0) or not np.all(np.isfinite(gross)):raise RuntimeError('invalid number_gross bound')
  rounding=32*np.finfo(float).eps*dt*gross;scale=1e-30*events.measure+np.maximum(abs(old.Z),abs(new.Z))+rounding/tol;scale=np.maximum(scale,1e-300);norm=float(max(abs(res)/scale))
  if norm<tol:return new,dict(iterations=it,residual=norm,coordinate_switches=switches,absolute_coordinate_residual_L1=float(sum(abs(res))),gross_roundoff_allowance_L1=float(sum(rounding)))
  delta=spsolve(eye(len(res),format='csr')-dt*new.jacobian(events),-res)
  if not np.all(np.isfinite(delta)):raise RuntimeError('protocol hole nonfinite correction')
  alpha=1.;lo=delta<0
  if np.any(lo):alpha=min(alpha,float(min(-.995*new.Z[lo]/delta[lo])))
  hi=ferm&(delta>0)
  if np.any(hi):alpha=min(alpha,float(min(.995*(new.measure[hi]-new.Z[hi])/delta[hi])))
  if alpha<=1e-18:raise RuntimeError('protocol hole boundary blocked')
  base=float(np.linalg.norm(res/scale))
  for _ in range(24):
   trial=new.copy();trial.Z+=alpha*delta;rr=trial.Z-old.Z-dt*np.where(trial.holes,-1.,1.)*trial.rhs(events);score=float(np.linalg.norm(rr/scale))
   if score<base*(1-1e-6*alpha)+1e-15:break
   alpha*=.5
  else:raise RuntimeError('protocol hole line search')
  new=trial
 raise RuntimeError('protocol hole iteration budget; worst='+str(int(np.argmax(abs(res)/scale)))+' norm='+str(norm))
