#!/usr/bin/env python3
"""Bounded sequential children, memory guard, atomic per-point checkpoints."""
import argparse, hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path
import psutil
import engines as E
ap=argparse.ArgumentParser();ap.add_argument('--indices',default='all')
ap.add_argument('--max-tasks',type=int,default=2);ap.add_argument('--mutate',action='store_true')
ap.add_argument('--resume',action='store_true');ap.add_argument('--rungs',default='1,2')
args=ap.parse_args();HERE=Path(__file__).resolve().parent
mode='mutate' if args.mutate else 'main'
out=HERE/mode/'small';out.mkdir(parents=True,exist_ok=True)
stop=False;child=None
def handler(sig,frame):
    global stop
    stop=True
signal.signal(signal.SIGTERM,handler);signal.signal(signal.SIGINT,handler)
indices=range(len(E.points())) if args.indices=='all' else [int(i) for i in args.indices.split(',')]
count=0
expected=E.hashes()
for name in ['small_worker.py','engines.py','FROZEN_CRITERIA.md']:
    expected[name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
for index in indices:
    for rung in [int(x) for x in args.rungs.split(',')]:
        path=out/('p%03d_r%d.json'%(index,rung))
        if path.exists():
            if json.loads(path.read_text())['source_hashes']!=expected:raise RuntimeError('Checkpoint input hash mismatch')
            continue
        if stop or count>=args.max_tasks: raise SystemExit(75)
        cmd=[sys.executable,str(HERE/'small_worker.py'),'--index',str(index),'--rung',str(rung)]
        if args.mutate: cmd+=['--mutate']
        with (out/('p%03d_r%d.log'%(index,rung))).open('w') as f:
            child=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            proc=psutil.Process(child.pid);peak=0;limited=False;forwarded=False
            while child.poll() is None:
                if stop and not forwarded:
                    try:child.send_signal(signal.SIGTERM)
                    except ProcessLookupError:pass
                    forwarded=True
                try:
                    rss=proc.memory_info().rss;peak=max(peak,rss)
                    if rss>1_000_000_000:
                        limited=True;child.terminate()
                except psutil.NoSuchProcess: pass
                time.sleep(.25)
            rc=child.returncode
        print(json.dumps(dict(index=index,rung=rung,exit_code=rc,peak_rss_bytes=peak,memory_limit=limited)),flush=True)
        count+=1;child=None
        if limited: raise SystemExit(76)
        if rc not in [0,75]: raise SystemExit(rc)
        if rc==75 or stop: raise SystemExit(75)
print('All requested small-gate tasks complete',flush=True)
