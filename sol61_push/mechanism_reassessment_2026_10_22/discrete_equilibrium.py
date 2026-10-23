import numpy as np,json,sys
from scipy.special import roots_legendre
from scipy.linalg import solve

def equilibrium(ng=256,order=12):
 dr=10/ng;rg=(np.arange(ng)+.5)*dr;gx,gw=roots_legendre(order)
 edges=np.r_[0,rg];left=edges[:-1];right=edges[1:]
 r=((left[:,None]+right[:,None])/2+(right-left)[:,None]/2*gx).ravel()
 weights=((right-left)[:,None]/2*gw).ravel()*r*r
 t=np.clip((r-rg[0])/dr,0,ng-1-1e-10);idx=t.astype(int);frac=t-idx
 phi=-1/np.sqrt(1+r*r)
 def deposit(v):return np.bincount(idx,weights=v*(1-frac),minlength=ng)+np.bincount(idx+1,weights=v*frac,minlength=ng)
 def state(z,ec,jac=False):
  psi=z[idx]*(1-frac)+z[idx+1]*frac-phi
  rho=10*np.maximum(psi,0)**2.5/(1+r*r);m=deposit(weights*rho);q=np.cumsum(m)/rg**2
  if q.max()>=.98:return None
  mu=np.cumsum((q*q/(1-q))[::-1])[::-1]*dr+.01*m/(rg*rg*dr)
  residual=np.r_[z+mu-ec,m.sum()-1]
  if not jac:return residual,m,q,psi
  chi=25*np.maximum(psi,0)**1.5/(1+r*r)*weights
  diag=np.bincount(idx,weights=chi*(1-frac)**2,minlength=ng)+np.bincount(idx+1,weights=chi*frac**2,minlength=ng)
  off=np.bincount(idx,weights=chi*frac*(1-frac),minlength=ng)[:-1]
  J=np.diag(diag)+np.diag(off,1)+np.diag(off,-1)
  curvature=q*(2-q)/(1-q)**2
  tail=np.cumsum((dr*curvature/rg**2)[::-1])[::-1]
  H=tail[np.maximum.outer(np.arange(ng),np.arange(ng))]+np.diag(.01/(rg*rg*dr))
  matrix=np.empty((ng+1,ng+1));matrix[:ng,:ng]=np.eye(ng)+H@J;matrix[:ng,-1]=-1;matrix[-1,:ng]=J.sum(axis=0);matrix[-1,-1]=0
  return residual,m,q,psi,matrix
 # Low-density initial state with an occupied core; cap-safe homotopy by line search.
 z=np.full(ng,-.6);ec=-.15
 history=[]
 for iteration in range(60):
  st=state(z,ec,True)
  if st is None:raise RuntimeError('initial cap')
  residual,m,q,psi,matrix=st;norm=np.max(np.abs(residual));history.append(float(norm))
  if norm<2e-12:break
  dz=solve(matrix,-residual)
  accepted=False
  for alpha in 2.**-np.arange(25):
   trial=state(z+alpha*dz[:-1],ec+alpha*dz[-1])
   if trial is not None and np.max(np.abs(trial[0]))<norm:
    z+=alpha*dz[:-1];ec+=alpha*dz[-1];accepted=True;break
  if not accepted:raise RuntimeError('line search failed')
 else:raise RuntimeError('iteration limit')
 return dict(ng=ng,order=order,rg=rg.tolist(),z=z.tolist(),ecut=float(ec),mass=float(m.sum()),max_q=float(q.max()),residual=history[-1],iterations=len(history),history=history,scope='continuous f(Q) in exact CIC-interpolated mean field, not finite-sample equilibrium')
if __name__=='__main__':
 out=equilibrium(**(json.loads(sys.argv[2]) if len(sys.argv)>2 else {}))
 open(sys.argv[1],'w').write(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ['rg','z','history']})
