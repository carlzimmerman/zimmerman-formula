"""Bounded compensated-mixed direct candidate, not a physical result."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,json,signal,time
from pathlib import Path
import numpy as np
from fast_gravity import gravity as cpu
from metal_gravity import gravity as ds
from mixed_gravity import gravity as mixed,backend_metadata

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    signal.alarm(90);rng=np.random.default_rng(19876);rows=[];start=time.monotonic()
    cases=[]
    for n in (1024,8192,32768,65536,262144):
        x=rng.normal(size=(n,3))*[1200,700,400]+[80000,-30000,1000]
        m=rng.uniform(.3,3,n)*4000;cases.append(('Gaussian_'+str(n),x,m))
    q=Path(__file__).with_name('run_q08_iso_c')/'final.npz'
    if q.exists():
        z=np.load(q);cases.append(('actual_q08_iso_c_endpoint',z['x'],z['m']))
    for label,x,m in cases:
        ref=cpu(x,m,10.,threads=4) if len(m)<=32768 else ds(x,m,10.)
        ticks=[]
        for _ in range(3):
            t=time.perf_counter();a,U,phi=mixed(x,m,10.);ticks.append(time.perf_counter()-t)
        err=np.linalg.norm(a-ref[0],axis=1)/np.maximum(np.linalg.norm(ref[0],axis=1),1e-100)
        rms=np.linalg.norm(a-ref[0])/np.linalg.norm(ref[0]);pe=np.max(abs((phi-ref[2])/ref[2]));ue=abs(U/ref[1]-1)
        f=m[:,None]*a;xx=x-np.average(x,weights=m,axis=0)
        P=np.linalg.norm(f.sum(0))/np.linalg.norm(f,axis=1).sum()
        J=np.linalg.norm(np.cross(xx,f).sum(0))/np.sum(np.linalg.norm(xx,axis=1)*np.linalg.norm(f,axis=1))
        row=dict(case=label,N=len(m),seconds=float(np.median(ticks)),reference='native CPUfloat64' if len(m)<=32768 else 'independently admitted DSdirect',force_L2=float(rms),force_max=float(err.max()),phi_max=float(pe),U_error=float(ue),normalized_P=float(P),normalized_J=float(J))
        row['gate_pass']=bool(rms<5e-7 and err.max()<2e-6 and max(pe,ue)<5e-7 and max(P,J)<1e-8)
        rows.append(row);Path(args.output).write_text(json.dumps(dict(backend=backend_metadata(),rows=rows,seconds=time.monotonic()-start),indent=2)+'\n');print(json.dumps(row),flush=True)
        if not row['gate_pass']:raise AssertionError('Mixed candidate gate failed')

if __name__=='__main__':main()
