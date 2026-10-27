import argparse,json
from pathlib import Path
import numpy as np
from curvature import Curvature
from recovery import tpotential
from continue_front import evolve
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_curvature').joinpath('results.json').read_text())['runs'];row=next(r for r in rows if r['profile']==2 and r['ell4']==10 and r['start']=='front');m=Curvature(6e10,3,128,10);m.eta=0;m.tpotential=lambda x:tpotential(m,x);r=evolve(m,np.array(row['x']),10000);r['ell4']=10;Path(a.output).write_text(json.dumps(dict(runs=[r]),indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','history','force','gravity']},flush=True)
