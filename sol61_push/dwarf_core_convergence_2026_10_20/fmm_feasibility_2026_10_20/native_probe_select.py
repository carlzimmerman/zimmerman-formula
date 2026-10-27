"""Finite raw-Laplace timings/errors: no evolution or finite-eps substitution."""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='4' if _k=='OMP_NUM_THREADS' else '1'
import argparse
import json
from pathlib import Path
import resource
import sys
import time
import numpy as np

from native_fmm import gravity, metadata, G

HERE=Path(__file__).resolve().parent


def direct_sample(x,m,ids):
    a=[]; phi=[]
    for i in ids:
        dr=x-x[i]; r2=np.einsum('ij,ij->i',dr,dr);r2[i]=np.inf
        invr=1/np.sqrt(r2)
        a.append(G*np.sum((m*invr**3)[:,None]*dr,axis=0))
        phi.append(-G*np.sum(m*invr))
    return np.array(a),np.array(phi)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--shape',choices=['gaussian','saved','resampled_saved'],required=True)
    p.add_argument('--n',type=int,required=True);p.add_argument('--tolerances',type=float,nargs='+',required=True);args=p.parse_args()
    rng=np.random.default_rng(20261021)
    if args.shape=='gaussian':
        x=rng.normal(size=(args.n,3))*1000.;m=np.full(args.n,1e8/args.n)
        domain='Generated isotropic Gaussian, 1000pc standard deviation, mass1e8Msun.'
    else:
        z=np.load(HERE.parent/'run_pilot_gpu8k_iso/final.npz');x0,m0=z['x'],z['m']
        if args.shape=='saved':
            if args.n!=len(x0):raise ValueError('saved N must match snapshot')
            x,m=x0,m0;domain='Actual saved isolation endpoint, unchanged coordinates/masses.'
        else:
            if args.n<len(x0):raise ValueError('resampled_saved requires N>=snapshot N so all original masses are retained')
            ids=np.arange(args.n)%len(x0);counts=np.bincount(ids,minlength=len(x0))
            x=x0[ids]+rng.normal(size=(args.n,3))*.05
            m=m0[ids]/counts[ids]
            domain='Synthetic scaling stress: cyclic copies of saved endpoint, Gaussian0.05pc jitter, each original particle mass divided among its copies. Not an evolved high-N snapshot.'
    # Include central near-balanced fields and distributed targets, not a random
    # sample falsely described as a complete high-N comparison.
    centre=np.median(x,axis=0)
    central=np.argsort(np.linalg.norm(x-centre,axis=1))[:32]
    ids=np.unique(np.r_[central,np.linspace(0,len(x)-1,32,dtype=int)])
    ar,pr=direct_sample(x,m,ids)
    result=dict(kind='native raw-Laplace feasibility only',domain=domain,n=len(x),
        backend=metadata(),python=sys.version,numpy=np.__version__,sample_indices=ids.tolist(),
        sample_count=len(ids),coordinate_span_pc=np.ptp(x,axis=0).tolist(),seed=20261021,cases=[])
    start=time.monotonic()
    for tol in args.tolerances:
        t=time.monotonic();a,u,phi=gravity(x,m,tolerance=tol);seconds=time.monotonic()-t
        error=np.linalg.norm(a[ids]-ar,axis=1);scale=np.linalg.norm(ar,axis=1)
        f=m[:,None]*a;xc=x-np.average(x,axis=0,weights=m);j=np.cross(xc,f)
        row=dict(requested_tolerance=tol,seconds=seconds,
            force_sample_max_vector_relative=float(np.max(error/scale)),
            force_sample_l2_relative=float(np.linalg.norm(a[ids]-ar)/np.linalg.norm(ar)),
            force_sample_max_absolute=float(error.max()),force_sample_median_magnitude=float(np.median(scale)),
            potential_sample_max_relative=float(np.max(abs((phi[ids]-pr)/pr))),
            momentum_residual_relative=float(np.linalg.norm(f.sum(0))/np.linalg.norm(f,axis=1).sum()),
            torque_residual_relative=float(np.linalg.norm(j.sum(0))/np.linalg.norm(j,axis=1).sum()),
            potential_energy=float(u))
        result['cases'].append(row);result['elapsed_seconds']=time.monotonic()-start
        result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['elapsed_scope']='FMM tolerance sweep only; runner records setup/direct-reference/serialization wall time too.'
        Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
