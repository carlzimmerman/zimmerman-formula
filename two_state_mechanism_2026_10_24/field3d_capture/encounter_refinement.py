"""Refine encounter intervals in the large-system cases that actually react."""
import json,argparse
from pathlib import Path
from run_exact_self import ExactSelfSimulation
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'runs':[]}
    for flat in (1.,.25):
        s=ExactSelfSimulation(6e10,3,n=64,f=.95,flat=flat,dt_motion=.1)
        r=s.run(2,.01);r['profile_index']=2;out['runs'].append(r)
        Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
        print(json.dumps({k:r[k] for k in ('flat','status','final','stats')}),flush=True)
