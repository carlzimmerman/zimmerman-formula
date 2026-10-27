import argparse,json
from pathlib import Path
from alignment import Align,PROFILES,checks
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for i,rj in [(1,1),(2,5),(2,8)]:
        _,mass,b,_=PROFILES[i]
        for eta in [10,30,100]:
            m=Align(mass,b,256,rj,eta);r=m.solve('all');r['profile']=i;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force','gravity','kappa']},flush=True)
