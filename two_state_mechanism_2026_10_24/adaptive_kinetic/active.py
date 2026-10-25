import json,argparse
from pathlib import Path
import numpy as np
from kinetic import Kinetic
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'runs':[]}
    for spacing in (1.5,.75):
        s=Kinetic(6e10,3,spacing=spacing);ids=np.arange(s.n,2*s.n);chosen=ids[np.argsort(np.linalg.norm(s.x[ids],axis=1))[:2]]
        s.state[chosen]=True;e,_,_=s.energy_force(s.x,s.state);s.initialE=e+s.kinetic(s.v);s.norm=max(abs(e),abs(s.initialE))
        r=s.run(.1,.01);r['purpose']='Seeded nonzero field control, excluded from formation';out['runs'].append(r)
        Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps({k:r[k] for k in ('status','final','max_energy_error','spacing')}),flush=True)
