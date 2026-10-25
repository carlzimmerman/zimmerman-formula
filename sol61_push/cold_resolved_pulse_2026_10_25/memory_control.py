import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from lean import Sphere as Old
from memory_gauss_v2 import Sphere
from inventory import shells as original
from inventory_memory import shells
rng=np.random.default_rng(280);rows=[]
for ne,nt,nf in [(8,8,8),(16,12,16)]:
 a=Old(ne,nt,nf);b=Sphere(ne,nt,nf);u=rng.normal(size=(len(a.r),nt,nf))+1j*rng.normal(size=(len(a.r),nt,nf));u/=np.linalg.norm(u);pot=a.poisson(u)
 for tau in [.03,-.05]:
  err=float(np.max(abs(a.angular(u,tau)-b.angular(u,tau))));assert err<1e-12;rows.append(dict(check='angular',ne=ne,tau=tau,error=err))
 x=original(a,u,pot);y=shells(a,u,pot)
 for k in ['M','Jz','E_half','E_canonical','K_global_SEM','W_global_SEM']:
  err=float(np.max(abs(np.asarray(x[k])-y[k])));assert err==0;rows.append(dict(check=k,ne=ne,error=err))
print(json.dumps(rows,indent=2))
