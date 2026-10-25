import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from lean import Sphere as Old
from memory_gauss import Sphere
rng=np.random.default_rng(279);rows=[]
for ne,nt,nf in [(8,8,8),(16,12,16)]:
 a=Old(ne,nt,nf);b=Sphere(ne,nt,nf)
 for signed in [False,True]:
  m=rng.normal(size=(len(a.r),nt,nf));m=m if signed else abs(m);m/=np.sum(abs(m));p=a.poisson_mass(m);q=b.poisson_mass(m);err=float(np.max(abs(p-q)));assert err<1e-12 and q.flags.owndata and q.dtype==np.float64;rows.append(dict(ne=ne,signed=signed,max_error=err,W_difference=float(.5*np.sum(m*(q-p)))))
print(json.dumps(rows,indent=2))
