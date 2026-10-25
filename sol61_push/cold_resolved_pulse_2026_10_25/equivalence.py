import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from lean import Sphere,Original
rng=np.random.default_rng(276);rows=[]
for ne,nt,nf in [(8,8,8),(16,12,16)]:
 phase=lambda r,der=0: .13*r if der==0 else np.full_like(r,.13)
 a=Original(ne,nt,nf,eta=.17,phase=phase);b=Sphere(ne,nt,nf,eta=.17,phase=phase);u=rng.normal(size=(len(a.r),nt,nf))+1j*rng.normal(size=(len(a.r),nt,nf));u/=np.linalg.norm(u)
 for dt in [.013,-.017]:
  va=a.kinetic(u,dt);vb=b.kinetic(u,dt);err=float(np.max(abs(va-vb)));mt=float(np.max(abs(a.transport_mass-b.transport_mass)));jt=float(np.max(abs(a.transport_Jz-b.transport_Jz)));assert max(err,mt,jt)<1e-12
  rows.append(dict(ne=ne,nt=nt,nf=nf,dt=dt,wave_error=err,mass_transfer_error=mt,Jz_transfer_error=jt))
 pa=a.poisson(u);pb=b.poisson(u);va,pa=a.step(u,pa,.01);vb,pb=b.step(u,pb,.01);err=float(np.max(abs(va-vb)));assert err<1e-12;rows.append(dict(ne=ne,full_step_error=err,lean_cache_entries=len(b.cache)))
print(json.dumps(rows,indent=2))
