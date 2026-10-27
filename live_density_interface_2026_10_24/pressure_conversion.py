"""LD-11: finite-density pressure-driven conversion without supplied charge."""
import argparse,json
from pathlib import Path
import numpy as np
from reservoir import Reservoir
from conservative_radius import transfer_species

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();old=json.loads(Path(__file__).with_name('run_conservative_radius').joinpath('results.json').read_text())['runs'][0];out=dict(runs=[])
    for beta in [20,1000]:
        for start in ['front','seed']:
            m=Reservoir(n=96,domain=4,beta=beta,k=0,tau=0,K=3)
            if start=='front':v,transfer=transfer_species(m,old)
            else:
                v=m.start(scale=4);v[m.n:]=.01*np.exp(-m.r.numpy()/(4*m.b));transfer=dict(law_independent_Plummer_start=True)
            assert min(m.cap(v))>0
            r=m.solve_scaled(v);r.update(start=start,transfer=transfer);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
