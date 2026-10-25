import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,resource,time,numpy as np
from lean import Sphere
from flux import flux
from budget import shells
start=time.time();s=Sphere(256,40,64,eta=.0509374,phase=lambda r,der=0:.13*r if der==0 else np.full_like(r,.13));r=s.r[:,None,None];u=np.exp(-r*r/2)*(1+.1*(1-s.mu[None,:,None]**2)*np.cos(2*s.phi[None,None,:]))*s.sr[:,None,None]*s.sa[None,:,:];u=np.asarray(u,complex);u/=np.linalg.norm(u);p=s.poisson(u);h0=s.moments(u,p)
u,p=s.step(u,p,.02);h=s.moments(u,p);f=flux(s,u,p);b=shells(s,u,p,[1,2,4,8,12,16]);rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
assert abs(h['M']-h0['M'])<1e-12 and len(s.cache)==0 and rss<750_000_000
print(json.dumps(dict(ne=256,nt=40,nf=64,seconds=time.time()-start,peak_RSS_bytes=rss,norm_residual=h['M']-h0['M'],persistent_LU_cache_entries=len(s.cache),scope='full-geometry allocation and method exercise; not physical collapse acceptance'),indent=2))
