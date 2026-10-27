"""Bounded tile-v1 accuracy/speed audit; failed gates remain failed."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
from fast_gravity import gravity as cpu
from metal_gravity import gravity as ds,backend_metadata as ds_metadata
from mixed_gravity import gravity as mixed,backend_metadata as mixed_metadata
from tile_gravity import gravity as tile,backend_metadata


def measure(a,U,phi,x,m,reference):
    b,V,psi=reference
    err=np.linalg.norm(a-b,axis=1)/np.maximum(np.linalg.norm(b,axis=1),1.e-100)
    force=m[:,None]*a;r=x-np.average(x,weights=m,axis=0)
    values=dict(force_L2=float(np.linalg.norm(a-b)/np.linalg.norm(b)),force_max=float(max(err)),
        phi_max=float(np.max(abs((phi-psi)/psi))),U_error=float(abs(U/V-1.)),
        normalized_P=float(np.linalg.norm(force.sum(0))/np.linalg.norm(force,axis=1).sum()),
        normalized_J=float(np.linalg.norm(np.cross(r,force).sum(0))/np.sum(np.linalg.norm(r,axis=1)*np.linalg.norm(force,axis=1))))
    values['gate_pass']=bool(values['force_L2']<5.e-7 and values['force_max']<2.e-6
        and max(values['phi_max'],values['U_error'])<5.e-7
        and max(values['normalized_P'],values['normalized_J'])<1.e-8)
    return values


def main():
    p=argparse.ArgumentParser();p.add_argument('--library',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();os.environ['TILE_GRAVITY_LIBRARY']=str(Path(a.library).resolve())
    start=time.monotonic();rng=np.random.default_rng(19876);here=Path(__file__).resolve().parent
    output=dict(backend=backend_metadata(),DS_reference=ds_metadata(),mixed_baseline=mixed_metadata(),
        seed=19876,gates=dict(force_L2=5.e-7,force_max=2.e-6,phi_U=5.e-7,normalized_P_J=1.e-8),rows=[],
        nonclaims=['Not admitted under nativeDS1e-11roundoffgate','No evolvedprofile,core,or remnantconvergence',
                   'SamephysicalPlummerpairlaw; lowerprecisionarithmeticrequiresseparatecontrols',
                   'OtherGPUprocessesnotstopped; timingsarenot anisolatedhardwareguarantee'])
    cases=[]
    for n in (1024,8192,32768,65536,262144):
        x=rng.normal(size=(n,3))*[1200,700,400]+[80000,-30000,1000]
        m=rng.uniform(.3,3,n)*4000.;cases.append(('Gaussian_'+str(n),x,m,10.))
    r=np.random.default_rng(19873);x=r.normal(size=(513,3))*[500,100,30];x[1]=x[0]
    cases.append(('anisotropic_unequal_513_unit_torque_failure',x,r.uniform(.1,5,len(x))*1000.,5.))
    r=np.random.default_rng(19874)
    x=np.r_[[[-4.e5,5.e5,-2.e5]],r.normal(size=(256,3))*[2,3,1]+[80000.12345,-30000.9876,2000.42]]
    cases.append(('compact_2pc_far_first_tail',x,r.uniform(.1,5,len(x))*1000.,2.))
    for directory in ('run_pilot_gpu8k_iso','run_q08_iso_c'):
        z=np.load(here/directory/'final.npz');cases.append((directory+'_endpoint',z['x'],z['m'],10.))
    target=Path(a.output)
    for label,x,m,eps in cases:
        tick=time.perf_counter();reference=cpu(x,m,eps,threads=4) if len(m)<=32768 else ds(x,m,eps)
        reference_seconds=time.perf_counter()-tick
        tile(x,m,eps) # Warm candidate independently of measured calls.
        ticks=[]
        for _ in range(3):
            tick=time.perf_counter();aa,U,phi=tile(x,m,eps);ticks.append(time.perf_counter()-tick)
        row=dict(case=label,N=len(m),epsilon_pc=eps,seconds=float(np.median(ticks)),
            reference='CPUbinary64' if len(m)<=32768 else 'DSdirect1e-11admittedreference',
            reference_seconds=reference_seconds,**measure(aa,U,phi,x,m,reference))
        if len(m)>=65536:
            ticks=[]
            for _ in range(3):
                tick=time.perf_counter();mixed(x,m,eps);ticks.append(time.perf_counter()-tick)
            row['mixed_median_seconds']=float(np.median(ticks))
            row['speedup_over_mixed']=row['mixed_median_seconds']/row['seconds']
            row['speedup_over_DS_reference']=reference_seconds/row['seconds']
        output['rows'].append(row);output['wall_seconds']=time.monotonic()-start
        output['observed_peak_RSS_bytes']=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        output['all_declared_benchmark_gates_pass']=all(r['gate_pass'] for r in output['rows'])
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
        print(json.dumps(row),flush=True)
    if not output['all_declared_benchmark_gates_pass']:
        raise AssertionError('tile-v1 has failed declared empirical gate(s); candidate not admitted')


if __name__=='__main__':main()
