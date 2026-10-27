"""Copy exact original8k initial file bytes; derive metadata without regeneration."""
import hashlib,json,shutil
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
old=HERE/'run_pilot_gpu8k_iso';out=HERE/'initial_reference_old8k'
out.mkdir(parents=True,exist_ok=True)
if any((out/name).exists() for name in ('initial.npz','initial_metadata.json')):raise FileExistsError('fresh initial files required')
source=old/'initial.npz';result=json.loads((old/'results.json').read_text())
with np.load(source,allow_pickle=False) as z:
    x,v,m,cold=(z[k] for k in ('x','v','m','cold'))
    digest=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
ic=dict(result['initial_conditions'])
if digest!=ic['relative_state_sha256']:raise ValueError('original relative phase-space digest mismatch')
if result['args']['eps']!=10. or result['args']['ncold']!=8192:raise ValueError('wrong reference')
shutil.copyfile(source,out/'initial.npz')
file_digest=hashlib.sha256(source.read_bytes()).hexdigest()
if hashlib.sha256((out/'initial.npz').read_bytes()).hexdigest()!=file_digest:raise ValueError('copy changed')
ic.update(reference_softening_pc=10.,backend=result['backend'],common_initial_state=True,
    original_reference_label='exact original run_pilot_gpu8k_iso DSnormalization at eps10; copied bytes, not regenerated',
    original_file_sha256=file_digest,original_file=str(source),
    original_results_sha256=hashlib.sha256((old/'results.json').read_bytes()).hexdigest(),
    control_convention='load fixed arrays; do not renormalize velocities for backend, epsilon, host or scattering controls')
metadata=dict(initial_conditions=ic,args=dict(ncold=8192,seed=87319,reference_eps=10.),
    provenance='Derived from original completed result and exact initial NPZ bytecopy; no IC sampling or gravity call')
(out/'initial_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(dict(relative_state_sha256=digest,original_file_sha256=file_digest,output=str(out))),flush=True)
