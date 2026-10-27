"""Resolve mode quadrature separately from ODE and energy-ledger accuracy."""
import argparse,json
from prepare import prepare
from autonomous import run
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
prep=[prepare(N,1000.,.05,.1,1.,'angular') for N in [384,768]]
auto=[run(N,100.,1e-10) for N in [128,256]]
with open(a.output,'w') as f:json.dump(dict(preparation=prep,autonomous=auto),f,indent=2,allow_nan=False)
print(json.dumps(dict(preparation=prep,autonomous=[{k:v for k,v in r.items() if k!='trace'} for r in auto])))
