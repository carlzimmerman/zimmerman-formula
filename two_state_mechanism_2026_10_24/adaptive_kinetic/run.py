import argparse,json
from pathlib import Path
from kinetic import Kinetic,PROFILES
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--suite',choices=['base','space','velocity','cell','time','seed'],required=True);ap.add_argument('--duration',type=float,default=2);a=ap.parse_args()
    nspace=64 if a.suite=='space' else 32;nvel=4 if a.suite=='velocity' else 2
    max_width=1. if a.suite=='cell' else 2.;dt=.01 if a.suite=='time' else .02;seed=29 if a.suite=='seed' else 11
    out={'runs':[]}
    profiles=range(4) if a.suite in ('base','space','velocity') else (1,2)
    for p in profiles:
        _,mass,b,_=PROFILES[p]
        for f in (0.,.95):
            s=Kinetic(mass,b,nspace,nvel,max_width,f=f,seed=seed);s.progress_path=str(Path(a.output).parent/'progress.json')
            row=s.run(a.duration,dt);row['profile_index']=p;out['runs'].append(row)
            Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
            print(json.dumps({k:row[k] for k in ('profile_index','f','status','reason','final','stats')}),flush=True)
