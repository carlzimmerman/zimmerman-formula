import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from scipy.linalg import expm
from gauss import Sphere
rng=np.random.default_rng(277);rows=[]
for tau in [.013,-.017]:
 s=Sphere(4,6,8,R=10,alpha=1,eta=.2);u=rng.normal(size=(len(s.r),s.nt,s.nf))+1j*rng.normal(size=(len(s.r),s.nt,s.nf));u/=np.linalg.norm(u);b=s.transform(u);exact=b.copy()
 for k in range(s.nf):
  for l in range(s.nt):
   H=s.H+np.diag(s.eta**2*s.lam[l,k]/(2*s.r*s.r));X=tau/s.eta*H;P=np.eye(len(s.r))-.5j*X-X@X/12;Q=np.eye(len(s.r))+.5j*X-X@X/12;exact[:,l,k]=np.linalg.solve(Q,P@b[:,l,k])
 v=s.kinetic(u,tau);err=float(np.max(abs(s.transform(v)-exact)));mass=float(np.max(abs(np.cumsum(np.sum(abs(v)**2-abs(u)**2,axis=(1,2)))[:-1]+s.transport_mass)));j0=s.eta*np.sum(abs(b)**2*s.m[None,None,:],axis=(1,2));bv=s.transform(v);j1=s.eta*np.sum(abs(bv)**2*s.m[None,None,:],axis=(1,2));spin=float(np.max(abs(np.cumsum(j1-j0)[:-1]+s.transport_Jz)));assert max(err,mass,spin)<1e-11;rows.append(dict(tau=tau,dense_Pade_error=err,mass_interface_residual=mass,Jz_interface_residual=spin))
s=Sphere(4,6,8,R=10,alpha=1,eta=2.);b=np.zeros((len(s.r),s.nt,s.nf),complex);b[:,0,0]=s.r*np.exp(-s.r*s.r/2)*np.sqrt(s.w);b/=np.linalg.norm(b);u=s.transform(b,True);be=b.copy();be[:,0,0]=expm(-1j*.2/s.eta*s.H)@b[:,0,0];exact=s.transform(be,True);errors=[]
for dt in [.02,.01,.005]:
 v=u.copy()
 for i in range(round(.2/dt)):v=s.kinetic(v,dt)
 err=float(np.linalg.norm(v-exact));errors.append(err);rows.append(dict(dt=dt,finite_H_exponential_error=err))
assert errors[0]/errors[1]>12 and errors[1]/errors[2]>12
print(json.dumps(rows,indent=2))
