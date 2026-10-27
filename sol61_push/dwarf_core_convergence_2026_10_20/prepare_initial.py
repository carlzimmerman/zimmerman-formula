"""Prepare one common quiet dwarf state for backend/epsilon/scattering controls.

All velocities are normalized ONCE with the declared nativeCPU Plummer
reference. Subsequent controls must load these arrays without renormalizing
their velocities to a different numerical kernel or softening.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from evolution import initial_conditions
from fast_gravity import gravity,backend_metadata


def prepare(args):
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    if args.backend=='metal':
        from metal_gravity import gravity as metal,backend_metadata as metadata
        reference=metal
    else:
        def reference(x,m,eps):return gravity(x,m,eps,threads=args.threads)
        metadata=backend_metadata
    x,v,m,cold,ic=initial_conditions(args.ncold,args.ncold//8,args.seed,args.reference_eps,reference)
    ic['relative_state_sha256']=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
    ic.update(reference_softening_pc=args.reference_eps,backend=metadata(),
        common_initial_state=True,control_convention='load fixed arrays; do not renormalize velocities for backend, epsilon, host or scattering controls')
    np.savez_compressed(out/'initial.npz',x=x,v=v,m=m,cold=cold)
    result=dict(args=vars(args),initial_conditions=ic,runtime_seconds=time.monotonic()-start)
    (out/'initial_metadata.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(initial_hash=ic['relative_state_sha256'],N=len(m),runtime_seconds=result['runtime_seconds'])),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--ncold',type=int,required=True)
    p.add_argument('--seed',type=int,default=87319);p.add_argument('--reference-eps',type=float,default=10.)
    p.add_argument('--threads',type=int,default=4)
    p.add_argument('--backend',choices=('cpu','metal'),default='cpu');prepare(p.parse_args())
