"""Second assembly history: less centrifugal support, unchanged coupling."""
import argparse
import json
from pathlib import Path
from assembly import Live,PROFILES,checks

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
ap.add_argument('--n',type=int,default=12);ap.add_argument('--nq',type=int,default=512)
ap.add_argument('--duration',type=float,default=30);ap.add_argument('--rtol',type=float,default=2e-7)
ap.add_argument('--alphas',default='.1,.3,1,3');ap.add_argument('--profiles',default='0,1,2,3')
ap.add_argument('--fs',default='.3,.95');ap.add_argument('--support',type=float,default=.1)
args=ap.parse_args();out=dict(checks=checks(),support=args.support,runs=[])
for i in map(int,args.profiles.split(',')):
    _,mass,b,_=PROFILES[i]
    for f in map(float,args.fs.split(',')):
        for alpha in map(float,args.alphas.split(',')):
            try:
                m=Live(mass,b,args.n,args.nq,f,alpha)
                m.l2*=args.support/.7
                row=m.run(args.duration,args.rtol)
            except (ValueError,RuntimeError) as err:
                row=dict(f=f,alpha=alpha,status='failed',reason=str(err))
            row.update(profile_index=i,support=args.support)
            out['runs'].append(row)
            print(json.dumps({k:v for k,v in row.items() if k not in ('history','final_radii','final_radial_v')}),flush=True)
            Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
