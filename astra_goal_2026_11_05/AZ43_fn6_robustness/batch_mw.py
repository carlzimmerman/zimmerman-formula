#!/usr/bin/env python3
"""Sequential, memory-guarded bounded MW batches, resumable by cell."""
import argparse,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
import psutil
import engines as E
ap=argparse.ArgumentParser();ap.add_argument('--index',type=int,required=True)
ap.add_argument('--footing',choices=['canonical','alt'],required=True)
ap.add_argument('--rung',type=int,choices=[1,2],required=True)
ap.add_argument('--max-batches',type=int,default=2);ap.add_argument('--cells-per-batch',type=int,default=128)
ap.add_argument('--mutate',action='store_true');ap.add_argument('--resume',action='store_true')
args=ap.parse_args();HERE=Path(__file__).resolve().parent
out=HERE/('mutate' if args.mutate else 'main')/'mw';out.mkdir(parents=True,exist_ok=True)
tag='%s_p%03d_r%d'%(args.footing,args.index,args.rung);path=out/(tag+'.json')
stop=False;child=None
def handler(sig,frame):
    global stop
    stop=True
    if child is not None and child.poll() is None:child.terminate()
signal.signal(signal.SIGTERM,handler);signal.signal(signal.SIGINT,handler)
expected=E.hashes()
for name in ['mw_worker.py','engines.py','FROZEN_CRITERIA.md']:
    expected[name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
for batch in range(args.max_batches):
    if path.exists():
        old=json.loads(path.read_text())
        if old['source_hashes']!=expected:raise RuntimeError('Checkpoint input hash mismatch')
        if old['complete']:raise SystemExit(0)
    if stop:raise SystemExit(75)
    done=len(json.loads(path.read_text())['cells']) if path.exists() else 0
    cmd=[sys.executable,str(HERE/'mw_worker.py'),'--index',str(args.index),'--footing',args.footing,
         '--rung',str(args.rung),'--max-cells',str(args.cells_per_batch)]
    if args.mutate:cmd+=['--mutate']
    with (out/(tag+'_from%04d.log'%done)).open('w') as f:
        child=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
        proc=psutil.Process(child.pid);peak=0;limited=False
        while child.poll() is None:
            try:
                rss=proc.memory_info().rss;peak=max(peak,rss)
                if rss>1_000_000_000:limited=True;child.terminate()
            except psutil.NoSuchProcess:pass
            time.sleep(.25)
        rc=child.returncode;child=None
    print(json.dumps(dict(tag=tag,from_cell=done,exit_code=rc,peak_rss_bytes=peak,memory_limit=limited)),flush=True)
    if limited:raise SystemExit(76)
    if rc==0:raise SystemExit(0)
    if rc!=75:raise SystemExit(rc)
raise SystemExit(75)
