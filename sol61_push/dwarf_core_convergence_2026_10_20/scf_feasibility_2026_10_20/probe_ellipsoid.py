"""Literal-N full3D particle projection against an independently integrated initial density.

This is a finite force/statistical control of a known diffuse ellipsoid plus
truncated stellar Plummer density. It is not an evolved profile or core claim.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,json,resource,time
from pathlib import Path
import numpy as np
from scf_backend import gravity,diagonal,load_agama,G
from probe_helpers import ellipsoid_field,force_metrics,unit_check

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--nmax',default='16,32,64');p.add_argument('--lmax',default='4,6,8');p.add_argument('--eta',type=float,default=1.)
    p.add_argument('--r0',type=float,default=300.);args=p.parse_args()
    d=np.load(ROOT/args.snapshot);x=d['x'];m=d['m'];cold=d['cold'];com=np.average(x,axis=0,weights=m);y=x-com
    # This analytic comparison is authorized only for the literally centred,
    # unshifted initial files. An evolved state must not be silently compared.
    if np.linalg.norm(com)>1e-8:raise ValueError('analytic initial reference requires centred saved initial coordinates')
    rng=np.random.default_rng(20261022);directions=rng.normal(size=(8,3));directions/=np.linalg.norm(directions,axis=1)[:,None]
    radii=np.array([5.,10.,25.,50.,75.,100.,300.,1000.,1500.,2000.])
    points=(radii[:,None,None]*directions[None,:,:]).reshape(-1,3)
    ang=np.deg2rad(37.);rot=np.array([[np.cos(ang),-np.sin(ang),0],[np.sin(ang),np.cos(ang),0],[0,0,1]])
    truth,_=ellipsoid_field(points@rot,float(m[cold].sum()),np.array([2000.,1600.,1200.]))
    truth=truth@rot.T
    r=np.linalg.norm(points,axis=1);ms=float(m[~cold].sum());astar=193.22
    fmax=(1500./np.sqrt(1500.**2+astar**2))**3
    enclosed=np.where(r<1500.,ms/fmax*r**3/(r*r+astar*astar)**1.5,ms)
    truth-=G*(enclosed/r**3)[:,None]*points
    agama=load_agama();start=time.monotonic();source_radius=np.linalg.norm(y,axis=1)
    result=dict(kind='literal saved initial particle projection vs analytic diffuse density; no evolved-density inference',
        snapshot=args.snapshot,N_total=len(m),N_cold=int(cold.sum()),actual_nice=os.getpriority(os.PRIO_PROCESS,0),native_threads=2,
        seed=20261022,units=unit_check(agama),r0_fixed_pc=args.r0,eta=args.eta,
        quadrature='independent uniform ellipsoid confocal integral scipyquad epsabs/rel2e-12; sphere identity unit tested',
        analytic_stars='exact enclosed mass of truncated Plummer a193.22/rmax1500',
        truth_points=points.tolist(),truth_acceleration=truth.tolist(),literal_cold_counts={str(v):int(np.count_nonzero(cold&(source_radius<=v))) for v in (10,25,50,75,100,300)},cases=[])
    for n in map(int,args.nmax.split(',')):
      for l in map(int,args.lmax.split(',')):
        t=time.monotonic();pot=agama.Potential(type='BasisSet',particles=(y,G*m),symmetry='None',lmax=l,mmax=l,nmax=n,eta=args.eta,r0=args.r0)
        # Test-point acceleration of the same selfexcluded COM energy: the
        # infinitesimal test mass shifts the expansion COM, giving the same
        # chain-rule constant as the finite physical particle acceleration.
        afixed=pot.force(y);_,dk=diagonal(source_radius,n,l,args.eta,args.r0)
        afixed+=.5*(G*m*dk/source_radius)[:,None]*y
        chain=np.average(afixed,axis=0,weights=m)
        a=pot.force(points-com)-chain
        row=dict(nmax=n,lmax=l,full_m=True,seconds=time.monotonic()-t,
            all_points=force_metrics(a,truth),at_radius={},chain_acceleration=chain.tolist())
        # r equality varies by roundoff along random directions; use construction
        # indices for all radial summaries, not a numerical radius filter.
        for k,v in enumerate(radii):row['at_radius'][str(v)]=force_metrics(a[8*k:8*k+8],truth[8*k:8*k+8])
        result['cases'].append(row);result['elapsed_seconds']=time.monotonic()-start
        result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(row),flush=True)


if __name__=='__main__':main()
