"""Bounded full3D falcON/P0 feasibility, without any evolution or new IC fit."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
import argparse
import json
from pathlib import Path
import resource
import sys
import time
import numpy as np
import falcon_native

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from fast_gravity import gravity as direct_gravity


def direct_targets(x,m,eps,ids):
    """Independent binary64 target-source summation, chunked bounded memory."""
    acceleration=np.zeros((len(ids),3));phi=np.zeros(len(ids))
    for tstart in range(0,len(ids),8):
        targets=ids[tstart:tstart+8]
        for sstart in range(0,len(m),8192):
            stop=min(sstart+8192,len(m));sources=np.arange(sstart,stop)
            d=x[sstart:stop][None,:,:]-x[targets][:,None,:]
            r2=np.sum(d*d,axis=2)+eps*eps
            r2[targets[:,None]==sources[None,:]]=np.inf
            inverse=1./np.sqrt(r2)
            phi[tstart:tstart+len(targets)]-=falcon_native.G*(inverse@m[sstart:stop])
            acceleration[tstart:tstart+len(targets)]+=falcon_native.G*np.sum(
                d*(inverse**3*m[sstart:stop])[...,None],axis=1)
    return acceleration,phi


def sample_full3D(count,rng):
    # Pure timing geometry: distorted Plummer bulk, a dense 50-pc component,
    # and distant full3D tails. No virial velocities or physical IC claim.
    direction=rng.normal(size=(count,3));direction/=np.linalg.norm(direction,axis=1)[:,None]
    u=rng.uniform(1.e-8,.999999,count)
    radius=300./np.sqrt(u**(-2./3.)-1.)
    x=direction*radius[:,None]*[1.,.8,1.15]
    dense=count//5;x[:dense]*=1./6.
    tail=count//20;x[-tail:]=rng.normal(size=(tail,3))*50000.+[300000.,-150000.,50000.]
    return x,np.full(count,3.1378e7/count)


def metric(a,phi,U,x,m,ids,ref_a,ref_phi,ref_U,centre):
    difference=a[ids]-ref_a
    relative=np.linalg.norm(difference,axis=1)/np.maximum(np.linalg.norm(ref_a,axis=1),1.e-100)
    force=m[:,None]*a;r=x-centre
    return dict(force_L2_error=float(np.linalg.norm(difference)/np.linalg.norm(ref_a)),
        max_relative_force_error=float(max(relative)),p99_relative_force_error=float(np.quantile(relative,.99)),
        phi_L2_error=float(np.linalg.norm(phi[ids]-ref_phi)/np.linalg.norm(ref_phi)),
        relative_U_error=abs(U/ref_U-1.) if ref_U is not None else None,
        sampled_weighted_phi_sum_error=abs(float(m[ids]@(phi[ids]-ref_phi))/float(m[ids]@ref_phi)),
        reference_target_count=len(ids),reference_covers_all_particles=bool(len(ids)==len(m)),
        normalized_momentum_force_defect=float(np.linalg.norm(force.sum(axis=0))/np.linalg.norm(force,axis=1).sum()),
        normalized_vector_torque_defect=float(np.linalg.norm(np.cross(r,force).sum(axis=0))/
            np.sum(np.linalg.norm(r,axis=1)*np.linalg.norm(force,axis=1))))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--library',required=True);p.add_argument('--output',required=True)
    p.add_argument('--large-sizes',default='65536,262144');a=p.parse_args()
    os.environ['FALCON_NATIVE_LIBRARY']=str(Path(a.library).resolve())
    rng=np.random.default_rng(71504);start=time.monotonic();cases=[]
    inputpath=HERE.parent/'run_pilot_gpu8k_iso'/'final.npz'
    state=np.load(inputpath);x,m=state['x'],state['m']
    meta=json.loads((inputpath.parent/'results.json').read_text())
    cases.append(('actual_8k_evolved_P0eps10',x,m,np.array(meta['snapshots'][-1]['centre']),10.))
    # Same particle count and total masses as the saved state; hard dynamic
    # range geometry isolates ARM double-coordinate accuracy from force order.
    far=x.copy();far[:len(x)*3//4]=rng.normal(size=(len(x)*3//4,3))*2.+[80000.,-50000.,3000.]
    far[len(x)*3//4:]=rng.normal(size=(len(x)-len(x)*3//4,3))*50000.+[-450000.,180000.,60000.]
    cases.append(('synthetic_2pc_dense_500kpc_tails',far,m,np.array([80000.,-50000.,3000.]),10.))
    for count in map(int,a.large_sizes.split(',')):
        if not 1000<=count<=262144:raise ValueError('bounded syntheticN1000..262144 only')
        xx,mm=sample_full3D(count,rng);cases.append((f'synthetic_full3D_{count}',xx,mm,np.zeros(3),10.))
    output=dict(backend=falcon_native.backend_metadata(),seed=71504,results=[],
        nonclaims=['No trajectory,physicalinitialcondition,core,remnant,or continuumconvergence result',
                   'Theta is an opening criterion,not a rigorousuniform tolerance',
                   'LargeN directreference covers only128 declared targets; no exactglobalU claim',
                   'Nativebinary64 directroundoff and treeapproximation are distinct error budgets'])
    target=Path(a.output)
    for label,xx,mm,centre,eps in cases:
        n=len(mm);reference_start=time.monotonic()
        if n<=10000:
            ar,Ur,pr=direct_gravity(xx,mm,eps,threads=1);ids=np.arange(n)
        else:
            ids=np.unique(np.r_[0,np.linspace(1,n-1,127,dtype=int)])
            ar,pr=direct_targets(xx,mm,eps,ids);Ur=None
        reference_seconds=time.monotonic()-reference_start
        for theta in (.3,.5,.7):
            tick=time.monotonic();aa,U,pp=falcon_native.gravity(xx,mm,eps,theta=theta)
            elapsed=time.monotonic()-tick
            row=dict(case=label,N=n,theta=theta,epsilon_pc=eps,seconds=elapsed,
                direct_reference_seconds=reference_seconds,**metric(aa,pp,U,xx,mm,ids,ar,pr,Ur,centre))
            row['initial_force_RMS_le_1e_minus5_gate']=bool(row['force_L2_error']<=1.e-5)
            output['results'].append(row)
            output.update(wall_seconds=time.monotonic()-start,
                observed_peak_RSS_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
            print(json.dumps(row),flush=True)


if __name__=='__main__':main()
