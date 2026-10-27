"""Bounded full-particle force costs; generated million-particle state is not evolved."""
import os
for k in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,json,resource,time
from pathlib import Path
import numpy as np
from scf_backend import gravity,load_agama
from probe_helpers import unit_check

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]


def generated_initial(ncold,seed=20261022):
    rng=np.random.default_rng(seed);ns=ncold//8
    u=rng.normal(size=(ncold//2,3));u/=np.linalg.norm(u,axis=1)[:,None]
    q=u*rng.random(ncold//2)[:,None]**(1/3)*[2000.,1600.,1200.]
    ang=np.deg2rad(37.);rot=np.array([[np.cos(ang),-np.sin(ang),0],[np.sin(ang),np.cos(ang),0],[0,0,1]])
    q=q@rot.T;q=np.r_[q,-q]
    u=rng.normal(size=(ns//2,3));u/=np.linalg.norm(u,axis=1)[:,None]
    fmax=(1500./np.sqrt(1500.**2+193.22**2))**3
    r=193.22/np.sqrt(rng.uniform(0.,fmax,ns//2)**(-2/3)-1.)
    s=u*r[:,None];s=np.r_[s,-s]
    mstar=574272.9377001019
    return np.r_[q,s],np.r_[np.full(ncold,53.64*mstar/ncold),np.full(ns,mstar/ns)]


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--ncold',type=int,required=True)
    p.add_argument('--snapshot');p.add_argument('--nmax',default='16,32');p.add_argument('--lmax',default='4,6');args=p.parse_args()
    if args.snapshot:
        d=np.load(ROOT/args.snapshot);x=d['x'];m=d['m'];source=args.snapshot
    else:x,m=generated_initial(args.ncold);source='labelled newly generated antithetic initial-position family, PCG64 seed20261022; no velocities/no evolution'
    agama=load_agama();start=time.monotonic()
    result=dict(kind='SCF full3D completeharmonic/selfexcluded force performance, not evolution',source=source,
        N_cold=args.ncold,N_total=len(m),actual_nice=os.getpriority(os.PRIO_PROCESS,0),native_threads=2,
        units=unit_check(agama),basis_r0_pc=300.,eta=1.,cases=[])
    for n in map(int,args.nmax.split(',')):
      for l in map(int,args.lmax.split(',')):
        t=time.monotonic();a,U,phi=gravity(x,m,nmax=n,lmax=l,r0=300.,eta=1.)
        row=dict(nmax=n,lmax=l,full_m=True,seconds=time.monotonic()-t,U_selfexcluded=U,
            finite=bool(np.isfinite(a).all() and np.isfinite(phi).all()))
        row['force_L2']=float(np.linalg.norm(a));row['elapsed_seconds']=time.monotonic()-start
        result['cases'].append(row);result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(row),flush=True)


if __name__=='__main__':main()
