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
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--snapshot');p.add_argument('--ncold',type=int)
    p.add_argument('--nmax',default='16,32,64');p.add_argument('--lmax',default='4,6,8');p.add_argument('--eta',type=float,default=1.)
    p.add_argument('--r0',type=float,default=300.);args=p.parse_args()
    if args.snapshot:
        d=np.load(ROOT/args.snapshot);x=d['x'];m=d['m'];cold=d['cold'];source=args.snapshot
    else:
        from probe_performance import generated_initial
        if not args.ncold:raise ValueError('literal saved snapshot or generated ncold required')
        x,m=generated_initial(args.ncold);cold=np.arange(len(m))<args.ncold;source='labelled generated initial positions PCG64seed20261022; not evolvedhighN'
    com=np.average(x,axis=0,weights=m);y=x-com
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
    inside=np.sum((points@rot/np.array([2000.,1600.,1200.]))**2,axis=1)<1.
    truthrho=inside*3*float(m[cold].sum())/(4*np.pi*2000*1600*1200)
    truthrho+=(r<1500.)*3*ms/(4*np.pi*astar**3*fmax)*(1+r*r/astar**2)**-2.5
    agama=load_agama();start=time.monotonic();source_radius=np.linalg.norm(y,axis=1)
    result=dict(kind='literal saved initial particle projection vs analytic diffuse density; no evolved-density inference',
        snapshot=source,N_total=len(m),N_cold=int(cold.sum()),actual_nice=os.getpriority(os.PRIO_PROCESS,0),native_threads=2,
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
        rho=pot.density(points-com)/G
        row=dict(nmax=n,lmax=l,full_m=True,seconds=time.monotonic()-t,
            all_points=force_metrics(a,truth),at_radius={},chain_acceleration=chain.tolist(),density_negative_any=bool(np.any(rho<0)),density_relative_rms=float(np.linalg.norm(rho-truthrho)/np.linalg.norm(truthrho)))
        # r equality varies by roundoff along random directions; use construction
        # indices for all radial summaries, not a numerical radius filter.
        for k,v in enumerate(radii):
            row['at_radius'][str(v)]=force_metrics(a[8*k:8*k+8],truth[8*k:8*k+8])
            row['at_radius'][str(v)]['density_absolute_max']=float(np.max(np.abs(rho[8*k:8*k+8]-truthrho[8*k:8*k+8])))
            row['at_radius'][str(v)]['density_relative_rms']=(float(np.linalg.norm(rho[8*k:8*k+8]-truthrho[8*k:8*k+8])/np.linalg.norm(truthrho[8*k:8*k+8])) if np.linalg.norm(truthrho[8*k:8*k+8]) else None)
        result['cases'].append(row);result['elapsed_seconds']=time.monotonic()-start
        result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(row),flush=True)


if __name__=='__main__':main()
