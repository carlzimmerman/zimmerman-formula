import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,resource,time
from refinement_v3 import load
from fast_flux import flux
from inventory_memory import shells
start=time.time();s,u,p,units,diag=load(nt=56,nf=64);u,p=s.step(u,p,.04);h=s.moments(u,p);f=flux(s,u,p);b=shells(s,u,p);rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;print(json.dumps(dict(seed_refinement=diag,seconds=time.time()-start,peak_RSS_bytes=rss,headroom_pass=rss<750_000_000,poststep=h),indent=2),flush=True);assert rss<750_000_000
