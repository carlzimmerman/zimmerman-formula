import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import numpy as np,json
from sphere_v3 import Sphere
s=Sphere(12,8,8,eta=.2);rng=np.random.default_rng(275);u=rng.normal(size=(len(s.r),s.nt,s.nf))+1j*rng.normal(size=(len(s.r),s.nt,s.nf));u/=np.linalg.norm(u);m0=np.sum(abs(u)**2,axis=(1,2));b=s.transform(u);j0=s.eta*np.sum(abs(b)**2*s.m[None,None,:],axis=(1,2));v=s.kinetic(u,.013);m1=np.sum(abs(v)**2,axis=(1,2));b=s.transform(v);j1=s.eta*np.sum(abs(b)**2*s.m[None,None,:],axis=(1,2));em=float(np.max(abs(np.cumsum(m1-m0)[:-1]+s.transport_mass)));ej=float(np.max(abs(np.cumsum(j1-j0)[:-1]+s.transport_Jz)));assert em<1e-13 and ej<1e-13;print(json.dumps(dict(seed=275,mass_interface_residual=em,matter_Jz_interface_residual=ej),indent=2))
