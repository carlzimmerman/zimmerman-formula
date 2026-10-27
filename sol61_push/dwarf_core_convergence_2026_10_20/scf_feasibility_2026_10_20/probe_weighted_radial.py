"""Finite literal-particle BSE snapshot comparison. No density-fit inference."""
import os
for k in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,json,resource,time
from pathlib import Path
import numpy as np
from scf_backend import load_agama,diagonal,G
from scf_weighted import gravity,centre_and_chain
from probe_helpers import direct_sample,force_metrics,unit_check

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--centre-results');p.add_argument('--host-centre',action='store_true')
    p.add_argument('--Rcent',type=float,default=300.);p.add_argument('--eta',type=float,default=1.);p.add_argument('--nmax',default='16,32');p.add_argument('--lmax',default='4,6')
    p.add_argument('--r0',default='100,300');args=p.parse_args()
    d=np.load(ROOT/args.snapshot);x=d['x'];m=d['m'];cold=d['cold'];n=len(m)
    com=np.average(x,axis=0,weights=m)
    if args.host_centre:
        import sys
        sys.path.insert(0,str(ROOT/'sol61_push/isolated_host_dwarf_2026_10_19'))
        from remnant import remnant_centre
        centre=remnant_centre(x,m,cold,40.)
        centre_method='posthoc local all-member Plummer40 self-potential minimum; diagnostic reference only'
    elif args.centre_results:
        centre=np.array(json.loads((ROOT/args.centre_results).read_text())['snapshots'][-1]['centre'])
        centre_method='recorded Plummer evolution diagnostic centre; not a SCF evolution centre'
    else:centre=com;centre_method='all-member mass COM'
    radius=np.linalg.norm(x-centre,axis=1);rng=np.random.default_rng(20261022)
    ids=list(np.flatnonzero(cold)[np.argsort(radius[cold])[:64]])+list(np.flatnonzero(~cold)[np.argsort(radius[~cold])[:32]])
    for lo,hi in [(0,25),(25,75),(75,100),(100,200),(200,300),(300,np.inf)]:
        available=np.flatnonzero((radius>=lo)&(radius<hi))
        ids+=list(rng.choice(available,min(48,len(available)),replace=False))
    ids=np.unique(ids).astype(int)
    refs={eps:direct_sample(x,m,ids,eps)[0] for eps in (0.,5.,10.,40.)}
    agama=load_agama();start=time.monotonic();previous={};reference_scf=None
    result=dict(kind='literal saved particle projection; no evolution or profile convergence claim',snapshot=args.snapshot,
        N_total=n,N_cold=int(cold.sum()),actual_nice=os.getpriority(os.PRIO_PROCESS,0),units=unit_check(agama),native_threads=2,
        seed=20261022,reference_centre=centre.tolist(),centre_method=centre_method,COM=com.tolist(),
        centre_COM_distance_pc=float(np.linalg.norm(centre-com)),Rcent_fixed_pc=args.Rcent,expansion_centre=centre_and_chain(x,m,args.Rcent)[0].tolist(),
        literal_cold_counts={str(r):int(np.count_nonzero(cold&(radius<=r))) for r in (10,25,50,75,100,300)},
        reference_sample_count=len(ids),reference_sample_ids=ids.tolist(),reference_sample_radii_pc=radius[ids].tolist(),reference_sample_acceleration={str(k):v.tolist()for k,v in refs.items()},
        reference_convention='point Newton and finite Plummer self-excluded references; SCF is a distinct continuum regularization',cases=[])
    for r0 in map(float,args.r0.split(',')):
      for nmax in map(int,args.nmax.split(',')):
       for lmax in map(int,args.lmax.split(',')):
        t=time.monotonic();a,U,phi=gravity(x,m,nmax=nmax,lmax=lmax,r0=r0,eta=args.eta,Rcent=args.Rcent)
        C,chainfun=centre_and_chain(x,m,args.Rcent);y=x-C;rad=np.linalg.norm(y,axis=1)
        native=agama.Potential(type='BasisSet',particles=(y,G*m),symmetry='None',lmax=lmax,mmax=lmax,nmax=nmax,eta=args.eta,r0=r0)
        afixed=native.force(y);_,dk=diagonal(rad,nmax,lmax,args.eta,r0)
        afixed+=.5*(G*m*dk/rad)[:,None]*y
        correction=chainfun(np.sum(m[:,None]*afixed,axis=0))
        if not np.allclose(a,afixed-correction,rtol=2e-12,atol=1e-12):raise AssertionError('diagnostic chain rebuild differs')
        row=dict(chain_L2_fraction=float(np.sqrt(np.sum(m[:,None]*correction**2)/np.sum(m[:,None]*afixed**2))),chain_max_absolute=float(np.linalg.norm(correction,axis=1).max()),eta=args.eta,r0=r0,nmax=nmax,lmax=lmax,full_m=True,N_total=n,seconds_including_second_diagnostic_rebuild=time.monotonic()-t,U_selfexcluded=U,
            direct_reference={str(eps):force_metrics(a[ids],b) for eps,b in refs.items()})
        for lo,hi in [(0,25),(25,75),(75,100),(100,200),(200,300),(300,np.inf)]:
            keep=(radius[ids]>=lo)&(radius[ids]<hi)
            row.setdefault('reference_by_radius',{})[str((lo,hi))]=dict(count=int(keep.sum()),
                plummer10=force_metrics(a[ids][keep],refs[10.][keep]) if np.any(keep) else None)
        scale=np.sum(m*np.linalg.norm(a,axis=1));jscale=np.sum(m*np.linalg.norm(x-com,axis=1)*np.linalg.norm(a,axis=1))
        row['P_residual']=float(np.linalg.norm(np.sum(m[:,None]*a,axis=0))/scale) if scale else None
        row['J_residual']=float(np.linalg.norm(np.sum(m[:,None]*np.cross(x-com,a),axis=0))/jscale) if jscale else None
        # These are basis-to-basis force differences on the same literal N.
        # They are not an N-convergence result and have no declared admission gate.
        for key,prior in previous.items():
            if key[0]==r0 and ((key[1]==nmax and key[2]==4 and lmax==6) or (key[1]==16 and nmax==32 and key[2]==lmax)):
                row.setdefault('previous_basis_difference',{})[str(key)]=force_metrics(a[ids],prior[ids])
        row['sample_acceleration']=a[ids].tolist()
        previous[(r0,nmax,lmax)]=a
        result['cases'].append(row);result['elapsed_seconds']=time.monotonic()-start
        result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(row),flush=True)


if __name__=='__main__':main()
