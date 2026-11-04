"""Absolute NUMBER error floor for nearly empty cells; explicit holes retained.

No state is clipped. The floor controls nonlinear stopping/merit for number
coordinates only, leaving tiny vacancy coordinates on the frozen relative
scheme. Its physical balance and floor sensitivity are tested separately.
"""
import sys
from pathlib import Path
import numpy as np
from scipy.sparse import diags,eye
from scipy.sparse.linalg import spsolve
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'integration_solver'))
from protocol_holes import QuantumState

def implicit_step(events,state,dt,tol=2e-8,maxiter=100,number_floor=1e-13):
 old=state.copy();new=state.copy();ferm=events.eta<0;switches=0
 for it in range(maxiter):
  z=new.Z/new.measure;switch=ferm&(z>.65)
  if np.any(switch):
   new.Z[switch]=new.measure[switch]-new.Z[switch];new.holes[switch]=~new.holes[switch]
   old.Z[switch]=old.measure[switch]-old.Z[switch];old.holes[switch]=~old.holes[switch];switches+=int(sum(switch))
  signs=np.where(new.holes,-1.,1.);rhs=signs*new.rhs(events);res=new.Z-old.Z-dt*rhs;gross=new.gross(events)
  if np.any(gross<0) or not np.all(np.isfinite(gross)):raise RuntimeError('invalid number_gross bound')
  rounding=32*np.finfo(float).eps*dt*gross;scale=1e-30*events.measure+number_floor*(~new.holes)+np.maximum(abs(old.Z),abs(new.Z))+rounding/tol;scale=np.maximum(scale,1e-300);norm=float(max(abs(res)/scale))
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
