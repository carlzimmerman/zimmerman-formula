"""One bounded leaf-occupancy tuning experiment, unchanged raw Laplace law."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['VECLIB_MAXIMUM_THREADS']='1'
import argparse,json,time,resource
from pathlib import Path
import numpy as np
from native_fmm_ndiv import gravity
from native_probe import direct_sample

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
rng=np.random.default_rng(20261021);n=65536
x=rng.normal(size=(n,3))*1000;m=np.full(n,1e8/n)
ids=np.unique(np.r_[np.argsort(np.linalg.norm(x-np.median(x,axis=0),axis=1))[:32],np.linspace(0,n-1,32,dtype=int)])
ar,pr=direct_sample(x,m,ids)
result=dict(n=n,shape='Gaussian1000pc',seed=20261021,tolerance=1e-8,sample_indices=ids.tolist(),cases=[])
for leaf in (1000,2000,4000,8000):
    start=time.monotonic();a,u,phi=gravity(x,m,1e-8,leaf);elapsed=time.monotonic()-start
    error=np.linalg.norm(a[ids]-ar,axis=1)
    row=dict(leaf_max_occupancy_threshold=leaf,seconds=elapsed,force_sample_max_relative=float(np.max(error/np.linalg.norm(ar,axis=1))),force_sample_max_absolute=float(error.max()),potential_sample_max_relative=float(np.max(abs((phi[ids]-pr)/pr))))
    result['cases'].append(row);result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(row),flush=True)
