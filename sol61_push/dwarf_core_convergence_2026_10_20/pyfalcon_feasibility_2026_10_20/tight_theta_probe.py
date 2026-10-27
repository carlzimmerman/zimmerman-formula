"""<=60s follow-up: can stock order3 reach force RMS1e-5 by tightertheta?"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import argparse
import json
from pathlib import Path
import time
import numpy as np
import falcon_native
from benchmark_falcon import sample_full3D,direct_targets,metric,direct_gravity,HERE


def main():
    p=argparse.ArgumentParser();p.add_argument('--library',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();os.environ['FALCON_NATIVE_LIBRARY']=str(Path(a.library).resolve())
    start=time.monotonic();rng=np.random.default_rng(71505)
    state=np.load(HERE.parent/'run_pilot_gpu8k_iso'/'final.npz')
    metadata=json.loads((HERE.parent/'run_pilot_gpu8k_iso'/'results.json').read_text())
    cases=[('actual8k',state['x'],state['m'],np.array(metadata['snapshots'][-1]['centre']),(.15,.1,.07,.05,.03))]
    xx,mm=sample_full3D(262144,rng);cases.append(('synthetic262k',xx,mm,np.zeros(3),(.15,.1)))
    output=dict(backend=falcon_native.backend_metadata(),seed=71505,results=[],
        nonclaims=['No evolvedconvergence,not a rigorous theta error bound',
                   'LargeN only128 directreference targets; no exactglobalU'])
    target=Path(a.output)
    for name,x,m,centre,thetas in cases:
        if len(m)<10000:
            ar,Ur,pr=direct_gravity(x,m,10.,threads=1);ids=np.arange(len(m))
        else:
            ids=np.unique(np.r_[0,np.linspace(1,len(m)-1,127,dtype=int)])
            ar,pr=direct_targets(x,m,10.,ids);Ur=None
        for theta in thetas:
            tick=time.monotonic();aa,U,pp=falcon_native.gravity(x,m,10.,theta=theta)
            row=dict(case=name,N=len(m),theta=theta,seconds=time.monotonic()-tick,
                **metric(aa,pp,U,x,m,ids,ar,pr,Ur,centre))
            output['results'].append(row);output['wall_seconds']=time.monotonic()-start
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(output,indent=2)+'\n')
            print(json.dumps(row),flush=True)


if __name__=='__main__':main()
