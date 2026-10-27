import argparse,json
from pathlib import Path
from volume_transfer import VolumeTransfer

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();old=json.loads(Path(__file__).with_name('run_warm').joinpath('results.json').read_text())['runs'];out=dict(runs=[])
    for tau in [.1,.03]:
        for source in [0,1]:
            m=VolumeTransfer(n=128,domain=4,beta=1000,k=120,tau=tau,K=3);v=m.transfer(old[source]);assert min(m.cap(v))>0
            r=m.solve_scaled(v);r['source_index']=source;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
