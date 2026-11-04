"""Final bounded shape-edge discriminator, conditional on simultaneous MW tests."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from response import Response,finite_admissibility
from cassini_response import physical


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    rows=[];edges=[];admissibility={}
    for p in [6,6.1,6.2,6.3,6.4,6.5,6.6]:
        scales=list(np.linspace(1.5,1.75,11))
        adms=[finite_admissibility(Response('cutoff',scale=float(t),power=p)) for t in scales]
        for t,adm in zip(scales,adms):admissibility[f'{p:g}|{t:g}']=adm
        for e in [.24,.25,.26,.27,.28,.29,.30]:
            local=[]
            def evaluate(t):return physical(Response('cutoff',scale=float(t),power=p),'canonical',e,nr=4000,nm=160)
            for t,adm in zip(scales,adms):
                if adm['minimum_total_slope']<=.01:continue
                r=evaluate(t);r.update(scale=float(t),power=p,minimum_total_slope=adm['minimum_total_slope'])
                local.append(r);rows.append(r)
            good=[r for r in local if r['x_ceiling']<=.99]
            if not good:continue
            best=max(good,key=lambda r:r['scale']);higher=[r for r in local if r['scale']>best['scale']]
            if higher:
                nxt=min(higher,key=lambda r:r['scale'])
                if nxt['x_ceiling']>.99:
                    t=brentq(lambda t:evaluate(t)['x_ceiling']-.99,best['scale'],nxt['scale'],xtol=2e-7)
                    adm=finite_admissibility(Response('cutoff',scale=t,power=p))
                    best=evaluate(t);best.update(scale=t,power=p,minimum_total_slope=adm['minimum_total_slope'])
            edges.append(best)
            print('p',p,'eps',e,'edge_t',best['scale'],'ratio',best['x_ceiling'],'min_slope',best['minimum_total_slope'],flush=True)
    out=dict(rows=rows,edges=edges,admissibility=admissibility,
             bounds=dict(scale=[1.5,1.75,11],power=[6,6.1,6.2,6.3,6.4,6.5,6.6],epsilon=[.24,.25,.26,.27,.28,.29,.30]),
             targets=dict(cassini_ratio=.99,minimum_sampled_total_slope=.01),
             qualification='Exploratory finite grid and detected-crossing roots, no global optimum or MW pass')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
