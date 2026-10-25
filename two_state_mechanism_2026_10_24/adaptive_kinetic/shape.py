import argparse,json
from pathlib import Path
from kinetic import Kinetic,PROFILES
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'runs':[]}
    for p in range(4):
        _,mass,b,_=PROFILES[p]
        for f in (0.,.95):
            s=Kinetic(mass,b,flat=1.,f=f);s.progress_path=str(Path(a.output).parent/'progress.json')
            r=s.run(2,.02);r['profile_index']=p;out['runs'].append(r)
            Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps({k:r[k] for k in ('profile_index','f','status','final','stats')}),flush=True)
