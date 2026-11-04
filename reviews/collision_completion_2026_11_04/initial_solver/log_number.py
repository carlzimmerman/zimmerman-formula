"""Sparse log-number Newton with a declared nearly-empty absolute budget.

The positive predictor changes only the initial Newton guess. Accepted states
solve the conservative physical-number BE residual; no state is clipped.
Explicit fermion holes retain their relative accuracy scheme.
"""
import sys
from pathlib import Path
import numpy as np
from scipy.sparse import eye,diags
from scipy.sparse.linalg import spsolve
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'integration_solver'))
from protocol_holes import QuantumState

def implicit_step(events,state,dt,tol=2e-8,maxiter=60,number_floor=1e-14,predict=True):
 old=state.copy();new=state.copy();ferm=events.eta<0;switches=0;predicted=0;minimum_alpha=1.;largest_du=0.
 if predict:
  signs=np.where(new.holes,-1.,1.);gain=dt*np.maximum(signs*new.rhs(events),0.);use=(~new.holes)&(new.Z<number_floor)&(gain>0);guess=new.Z+gain;guess[ferm]=np.minimum(guess[ferm],.6*new.measure[ferm]);new.Z[use]=guess[use];predicted=int(sum(use))
 if np.any(new.Z<=0):raise RuntimeError('log-number route requires positive initial coordinates')
 for it in range(maxiter):
  z=new.Z/new.measure;change=ferm&(z>.65)
  if np.any(change):
   new.Z[change]=new.measure[change]-new.Z[change];new.holes[change]=~new.holes[change];old.Z[change]=old.measure[change]-old.Z[change];old.holes[change]=~old.holes[change];switches+=int(sum(change))
  s=np.where(new.holes,-1.,1.);res=new.Z-old.Z-dt*s*new.rhs(events);gross=new.gross(events);rounding=32*np.finfo(float).eps*dt*gross;scale=1e-30*events.measure+number_floor*(~new.holes)+np.maximum(abs(old.Z),abs(new.Z))+rounding/tol;scale=np.maximum(scale,1e-300);norm=float(max(abs(res)/scale))
  if norm<tol:return new,dict(iterations=it,residual=norm,coordinate_switches=switches,predicted_empty_coordinates=predicted,minimum_line_alpha=minimum_alpha,maximum_log_correction=largest_du,physical_coordinate_residual_L1=float(sum(abs(res))),nonrounding_number_floor_budget_L1=float(tol*number_floor*sum(~new.holes)),gross_roundoff_allowance_L1=float(sum(rounding)))
  matrix=eye(len(res),format='csr')-dt*new.jacobian(events);linear=diags(1/scale)@matrix@diags(new.Z);du=spsolve(linear,-res/scale)
  if not np.all(np.isfinite(du)):raise RuntimeError('log-number nonfinite direction')
  largest_du=max(largest_du,float(max(abs(du))));du=np.clip(du,-20.,20.);alpha=1.;base=float(np.linalg.norm(res/scale))
  for ls in range(30):
   trial=new.copy();trial.Z=new.Z*np.exp(alpha*du)
   if np.any(trial.Z[ferm]>=trial.measure[ferm]):alpha*=.5;continue
   rr=trial.Z-old.Z-dt*s*trial.rhs(events);score=float(np.linalg.norm(rr/scale))
   if score<base*(1-1e-6*alpha)+1e-15:break
   alpha*=.5
  else:raise RuntimeError('log-number line search norm='+str(norm))
  minimum_alpha=min(minimum_alpha,alpha);new=trial
 raise RuntimeError('log-number iteration budget norm='+str(norm)+' worst='+str(int(np.argmax(abs(res)/scale))))
