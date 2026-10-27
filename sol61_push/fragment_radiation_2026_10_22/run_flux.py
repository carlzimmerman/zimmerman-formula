import argparse,json
from pathlib import Path
from model_flux import Model,evolve
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--n',type=int,default=32);p.add_argument('--box',type=float,default=8);p.add_argument('--side',type=int,default=10);p.add_argument('--mass',type=float,default=4);p.add_argument('--dt',type=float,default=.003);p.add_argument('--end',type=float,default=18);p.add_argument('--frozen',action='store_true');p.add_argument('--shift',type=float,default=0);args=p.parse_args()
m=Model(n=args.n,box=args.box,np_side=args.side,mass_ratio=args.mass,seed_shift=args.shift);r=evolve(m,dt=args.dt,end=args.end,frozen=args.frozen);Path(args.output).write_text(json.dumps(r,indent=2)+'\n');print(r['stop_reason'],r['stop_time'],r['max_energy_error'],r['partition'],flush=True)
