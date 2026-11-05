#!/usr/bin/env python3
"""One restartable nonlinear fit case; production grid must use heavyq."""
import argparse,hashlib,platform,resource,signal,time
from pathlib import Path
import engine as E
import numpy,scipy
ap=argparse.ArgumentParser()
ap.add_argument('--template',type=int,choices=range(12),required=True)
ap.add_argument('--rung',type=int,choices=[1,2],required=True)
ap.add_argument('--foot',choices=E.FOOTS,required=True)
ap.add_argument('--replicate',type=int,choices=range(3),default=0)
ap.add_argument('--scenario',choices=['flat','rise'],default='flat')
ap.add_argument('--snr',type=int,choices=[30,60,120,240],default=30)
ap.add_argument('--hi',choices=['free','fixed'],default='free')
ap.add_argument('--mode',choices=['main','mutate','reference','double','plus','minus'],default='main')
ap.add_argument('--step',type=float,choices=[.01,.005],default=.01)
ap.add_argument('--tag',default='pilot');ap.add_argument('--resume',action='store_true')
args=ap.parse_args();stop=False
def stopping(*_):
    global stop
    stop=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
key=f't{args.template:02d}_r{args.rung}_{args.foot}_n{args.replicate}_{args.scenario}_s{args.snr}_{args.hi}_{args.mode}_{args.step}'
out=E.HERE/args.tag/args.mode/(key+'.json');checkpoint=out.with_suffix('.checkpoint.json')
identity=dict(sources=E.hashes(),worker=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              arguments={k:v for k,v in vars(args).items() if k not in ['tag','resume']},
              versions=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__))
if out.exists():
    import json
    old=json.loads(out.read_text())
    if old['identity']!=identity:raise RuntimeError('Existing result identity changed')
    if args.resume:print('Verified completed case',key);raise SystemExit(0)
    raise RuntimeError('Use a fresh tag or --resume; refusing overwrite')
start=time.time()
try:
    result=E.fit_case(args.template,args.rung,args.foot,args.replicate,args.scenario,args.snr,args.hi,args.mode,args.step,lambda:stop)
except E.YieldRequested:
    E.atomic(checkpoint,dict(identity=identity,status='interrupted case; resume restarts this deterministic case'))
    print('Checkpoint',key,flush=True);raise SystemExit(75)
E.atomic(out,dict(identity=identity,scientific=result))
E.atomic(out.with_suffix('.runtime.json'),dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(key,'resolved',result['resolved'],'delta',result['delta'],flush=True)
# An unresolved scientific fit is a completed computation, not a crash.
