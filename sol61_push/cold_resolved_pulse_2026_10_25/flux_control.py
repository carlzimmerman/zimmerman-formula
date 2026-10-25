import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from lean import Sphere
from fast_flux import flux
from flux import flux as original
rng=np.random.default_rng(278);rows=[]
for ne,nt,nf in [(8,8,8),(16,12,16)]:
 s=Sphere(ne,nt,nf,eta=.17,phase=lambda r,der=0:.13*r+.02*r*r if der==0 else .13+.04*r);u=rng.normal(size=(len(s.r),nt,nf))+1j*rng.normal(size=(len(s.r),nt,nf));u/=np.linalg.norm(u);p=s.poisson(u);a=flux(s,u,p);b=original(s,u,p);err={key:float(np.max(abs(np.array(a[key])-b[key]))) for key in ['mass','energy','Jz']};assert max(err.values())<1e-10;rows.append(dict(ne=ne,nt=nt,nf=nf,errors=err))
print(json.dumps(rows,indent=2))
