"""CI-9: increase negative charge chemical offset while retaining area cost."""
import argparse,json
from pathlib import Path
import numpy as np
from tension_charge import TensionCharge
from tension_refine import diagnostic
from stress_test import stress_bound
from refine import polish

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_tension_refine').joinpath('results.json').read_text())['runs'];base=rows[1];out=dict(runs=[])
    for k in [120,200,300]:
        for tau in [.1,.3,1]:
            m=TensionCharge(6e10,3,256,k,1e-5,beta=1000,tau=tau);x,op=polish(m,np.array(base['x']));r=diagnostic(m,x);r.update(k=k,tau=tau,stress=stress_bound(m,x));out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force_T','force_F']},flush=True)
