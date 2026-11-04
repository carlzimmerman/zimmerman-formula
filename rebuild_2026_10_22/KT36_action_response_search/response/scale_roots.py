"""Resolve sampled scale crossings in the declared continuation rectangle."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from response import Response
from cassini_response import physical


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    output=[]
    for e in [.18,.20,.22,.25,.28,.30]:
        def value(t):return physical(Response('cutoff',scale=float(t),power=6),'canonical',e,nr=4000,nm=160)['x_ceiling']
        ts=np.linspace(1.5,1.7,21);rs=[value(t) for t in ts];roots=[]
        for lo,hi,rl,rh in zip(ts[:-1],ts[1:],rs[:-1],rs[1:]):
            if (rl-1)*(rh-1)<0:
                t=brentq(lambda x:value(x)-1,float(lo),float(hi),xtol=1e-7)
                roots.append(dict(scale=t,bracket=[float(lo),float(hi)],ratio=value(t)))
        output.append(dict(epsilon=e,scale_samples=list(map(float,ts)),ratios=rs,roots=roots))
        print('epsilon',e,'crossings',roots,'sampled passing max',max((float(t) for t,r in zip(ts,rs) if r<=1),default=None),flush=True)
    result=dict(rows=output,footing='canonical',power=6,settings=dict(nr=4000,nm=160),
                qualification='All observed crossings on this 21-point scale grid were refined; no continuum uniqueness or absence of smaller unsampled islands claimed')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
