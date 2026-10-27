"""Read frozen physical initial arrays without any velocity renormalization."""
import hashlib,json
from pathlib import Path
import numpy as np
from evolution import MCOLD,MSTAR

def load_initial(path,ncold,seed):
    path=Path(path)
    with np.load(path,allow_pickle=False) as z:
        x,v,m,cold=(z[k].copy() for k in ('x','v','m','cold'))
    ic=json.loads(path.with_name('initial_metadata.json').read_text())['initial_conditions']
    n=ncold+ncold//8
    if x.shape!=(n,3) or v.shape!=(n,3) or m.shape!=(n,) or cold.shape!=(n,):raise ValueError('fixed initial count/shape mismatch')
    if cold.dtype!=np.bool_ or int(cold.sum())!=ncold:raise ValueError('cold species mask mismatch')
    if ic['cold_phase_seed']!=seed:raise ValueError('fixed initial sampling seed mismatch')
    if not all(np.all(np.isfinite(a)) for a in (x,v,m)) or np.any(m<=0):raise ValueError('invalid fixed phase space')
    if not np.allclose(m[cold],MCOLD/ncold,rtol=1e-13,atol=0) or not np.allclose(m[~cold],MSTAR/(ncold//8),rtol=1e-13,atol=0):raise ValueError('physical species mass mismatch')
    digest=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
    if digest!=ic['relative_state_sha256']:raise ValueError('fixed initial content hash mismatch')
    ic.update(common_initial_state=True,loaded_from=str(path.resolve()),control_convention='fixed arrays; no backend/epsilon/scattering renormalization')
    return x,v,m,cold,ic
