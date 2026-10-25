import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from lean import Sphere
from phase_energy import measure
rows=[]
for p in [0.,.13]:
 s=Sphere(32,12,16,eta=.2,phase=lambda r,der=0:p*r if der==0 else np.full_like(r,p));u=np.exp(-s.r[:,None,None]**2/2)*s.sr[:,None,None]*s.sa[None,:,:];u=np.asarray(u,complex);u/=np.linalg.norm(u);d=measure(s,u);expected=.5*p*p
 assert abs(d['K_phase']-expected)<1e-12
 rows.append(dict(p=p,expected_K_phase=expected,measurement=d))
print(json.dumps(rows,indent=2))
