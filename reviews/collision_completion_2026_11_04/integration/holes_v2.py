"""Quantum implicit step retaining sub-ulp fermion holes explicitly.

Each fermion cell is represented by number or hole number, selected while
its occupancy is moderate. Availability is never obtained by subtracting a
rounded f=1 from one. Bosons always use number. No accepted state is clipped.
"""
import numpy as np
from scipy.sparse import coo_matrix,diags,eye
from scipy.sparse.linalg import spsolve

class QuantumState:
 def __init__(self,measure,eta,Y=None,Z=None,holes=None):
  self.measure=np.asarray(measure);self.eta=np.asarray(eta)
  if Z is None:
   self.holes=(self.eta<0)&(np.asarray(Y)/self.measure>.5)
   self.Z=np.where(self.holes,self.measure-np.asarray(Y),np.asarray(Y)).copy()
  else:self.Z=np.array(Z,float).copy();self.holes=np.array(holes,bool).copy()
 def arrays(self):
  z=self.Z/self.measure;f=np.where(self.holes,1-z,z);available=np.where(self.holes,z,1+self.eta*f)
  return f,available
 def numbers(self):return np.where(self.holes,self.measure-self.Z,self.Z)
 def copy(self):return QuantumState(self.measure,self.eta,Z=self.Z,holes=self.holes)
 def products(self,events):
  f,a=self.arrays();v=f[events.index];av=a[events.index]
  with np.errstate(divide='ignore',invalid='ignore'):
   lf=np.log(v);la=np.log(av);ww=events.weights[:,1:]
   forward=np.exp(lf[:,0]+np.sum(np.where(ww>0,ww*la[:,1:],0.),axis=1))
   reverse=np.exp(la[:,0]+np.sum(np.where(ww>0,ww*lf[:,1:],0.),axis=1))
  return forward,reverse,v,av
 def flux(self,events):
  a,b,_,_=self.products(events);return events.coefficient*(a-b)
 def rhs(self,events):return np.asarray(events.S@self.flux(events)).ravel()
 def jacobian(self,events):
  a,b,v,av=self.products(events);tiny=1e-280
  deriv=np.empty_like(v)
  deriv[:,0]=a/np.maximum(v[:,0],tiny)-b*events.eta[events.index[:,0]]/np.maximum(av[:,0],tiny)
  deriv[:,1:]=events.weights[:,1:]*(a[:,None]*events.eta[events.index[:,1:]]/np.maximum(av[:,1:],tiny)-b[:,None]/np.maximum(v[:,1:],tiny))
  D=coo_matrix(((events.coefficient[:,None]*deriv).ravel(),(np.repeat(np.arange(len(a)),5),events.index.ravel())),shape=(len(a),len(self.Z))).tocsr()
  signs=np.where(self.holes,-1.,1.)
  return diags(signs)@events.S@D@diags(signs/self.measure)
 def entropy(self):
  f,a=self.arrays()
  with np.errstate(divide='ignore',invalid='ignore'):
   s=-np.where(f>0,f*np.log(f),0)+np.where(a>0,a*np.log(a)/self.eta,0)
  return float(self.measure@s)

def implicit_step(events,state,dt,tol=2e-8,maxiter=100):
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
  new=trial
 raise RuntimeError('hole Newton iteration budget; worst='+str(int(np.argmax(abs(res)/np.maximum(scale,1e-300))))+' norm='+str(norm)+' availability='+str(float(new.arrays()[1][np.argmax(abs(res)/np.maximum(scale,1e-300))])))
