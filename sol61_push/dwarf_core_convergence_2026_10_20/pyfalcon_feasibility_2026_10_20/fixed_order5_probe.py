"""Bounded patched-order5 full3D Plummer theta .3/.2/.1 probe, no evolution."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import numpy as np
import falcon_native
from benchmark_falcon import sample_full3D,direct_targets,metric,direct_gravity,HERE


def main():
    p=argparse.ArgumentParser();p.add_argument('--library',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();os.environ['FALCON_NATIVE_LIBRARY']=str(Path(a.library).resolve())
    start=time.monotonic();rng=np.random.default_rng(71506)
    state=np.load(HERE.parent/'run_pilot_gpu8k_iso'/'final.npz')
    metadata=json.loads((HERE.parent/'run_pilot_gpu8k_iso'/'results.json').read_text())
    cases=[('actual8k',state['x'],state['m'],np.array(metadata['snapshots'][-1]['centre']))]
    far=state['x'].copy();dense=3*len(far)//4
    far[:dense]=rng.normal(size=(dense,3))*2.+[80000.,-50000.,3000.]
    far[dense:]=rng.normal(size=(len(far)-dense,3))*50000.+[-450000.,180000.,60000.]
    cases.append(('synthetic_2pc_dense_500kpc_tails',far,state['m'],np.array([80000.,-50000.,3000.])))
    for count in (65536,262144):
        xx,mm=sample_full3D(count,rng);cases.append((f'synthetic{count}',xx,mm,np.zeros(3)))
    patch=HERE.parent/'vendor/pyfalcon_d2e2e05_order5fix/PATCH_PROVENANCE.json'
    output=dict(backend=falcon_native.backend_metadata(),seed=71506,results=[],
        vendor_patch=json.loads(patch.read_text()),vendor_patch_sha256=hashlib.sha256(patch.read_bytes()).hexdigest(),
        nonclaims=['No productionadmissionor evolvedconvergence','Not a rigorous thetaerrorcertificate',
                   'LargeN only128directreference targets; no exactglobalU',
                   'Treeapproximateforces need not deriveexactlyfrom reportedhalf-mass-weightedphi'])
    target=Path(a.output)
    for name,x,m,centre in cases:
        if len(m)<10000:
            ar,Ur,pr=direct_gravity(x,m,10.,threads=1);ids=np.arange(len(m))
        else:
            ids=np.unique(np.r_[0,np.linspace(1,len(m)-1,127,dtype=int)])
            ar,pr=direct_targets(x,m,10.,ids);Ur=None
        for theta in (.3,.2,.1):
            tick=time.monotonic();aa,U,pp=falcon_native.gravity(x,m,10.,theta=theta)
            row=dict(case=name,N=len(m),theta=theta,seconds=time.monotonic()-tick,
                **metric(aa,pp,U,x,m,ids,ar,pr,Ur,centre))
            row['force_L2_le_1e_minus5']=bool(row['force_L2_error']<=1.e-5)
            output['results'].append(row);output['wall_seconds']=time.monotonic()-start
            output['observed_peak_RSS_bytes']=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(output,indent=2)+'\n')
            print(json.dumps(row),flush=True)


if __name__=='__main__':main()
