#!/usr/bin/env python3
"""Enumerate the complete frozen grid; long execution requires heavyq."""
import argparse,hashlib,itertools,json,os,platform,signal,subprocess,sys,time
from pathlib import Path
import engine as E
import numpy,scipy,psutil
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='grid');ap.add_argument('--max-cases',type=int,default=0)
ap.add_argument('--resume',action='store_true');ap.add_argument('--plan',action='store_true');args=ap.parse_args()
def cases():
    for tid,foot,hi,rung in itertools.product(range(12),E.FOOTS,['free','fixed'],[1,2]):
        for mode,step in [('reference',.01),('double',.01),('plus',.01),('minus',.01),('plus',.005),('minus',.005)]:
            yield dict(template=tid,foot=foot,hi=hi,rung=rung,mode=mode,step=step,replicate=0,scenario='flat',snr=30)
    for tid,rep,snr,foot,hi,rung,scenario in itertools.product(range(12),range(3),[30,60,120,240],E.FOOTS,['free','fixed'],[1,2],['flat','rise']):
        for mode in (['main','mutate'] if scenario=='flat' else ['main']):
            yield dict(template=tid,foot=foot,hi=hi,rung=rung,mode=mode,step=.01,replicate=rep,scenario=scenario,snr=snr)
def key(c):return f"t{c['template']:02d}_r{c['rung']}_{c['foot']}_n{c['replicate']}_{c['scenario']}_s{c['snr']}_{c['hi']}_{c['mode']}_{c['step']}"
worker=E.HERE/'worker.py';wh=hashlib.sha256(worker.read_bytes()).hexdigest()
versions=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__)
allcases=list(cases());keys=[key(c) for c in allcases]
if len(set(keys))!=4032 or len(keys)!=4032:raise RuntimeError('Frozen grid coverage mismatch')
plan=dict(cases=len(keys),noiseless=sum(c['mode'] not in ['main','mutate'] for c in allcases),
          noisy_main=sum(c['mode']=='main' for c in allcases),noisy_mutate=sum(c['mode']=='mutate' for c in allcases),
          source_hashes=E.hashes(),worker=wh,versions=versions)
if args.plan:
    E.atomic(E.HERE/'grid_plan.json',plan);print(json.dumps(plan,indent=2));raise SystemExit(0)
if not os.environ.get('HEAVYQ_JOB_ID') and not 0<args.max_cases<=2:raise RuntimeError('Full grid requires heavyq; outside queue only max-cases1 or2 pilot is allowed')
stop=False;child=None
def stopping(*_):
    global stop
    stop=True
    if child is not None and child.poll() is None:child.send_signal(signal.SIGTERM)
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
out=E.HERE/args.tag;out.mkdir(parents=True,exist_ok=True);done=0;new=0;peaks=[]
for c in allcases:
    file=out/c['mode']/(key(c)+'.json')
    identity=dict(sources=E.hashes(),worker=wh,arguments=c,versions=versions)
    if file.exists():
        old=json.loads(file.read_text())
        if old['identity']!=identity:raise RuntimeError('Stale completed case '+key(c))
        done+=1;continue
    if stop or (args.max_cases and new>=args.max_cases):break
    cmd=[sys.executable,str(worker),'--tag',args.tag,'--resume']
    for k,v in c.items():cmd+=['--'+k,str(v)]
    log=out/(key(c)+'.log');peak=0;memory_limit=False
    with log.open('w') as f:
        child=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
        proc=psutil.Process(child.pid)
        while child.poll() is None:
            try:
                rss=proc.memory_info().rss;peak=max(peak,rss)
                if rss>1_000_000_000:
                    memory_limit=True;child.terminate()
            except psutil.NoSuchProcess:pass
            time.sleep(.05)
        code=child.returncode
    rec=dict(case=key(c),exit_code=code,peak_rss_bytes=peak,memory_limit=memory_limit);peaks.append(rec);print(json.dumps(rec),flush=True)
    E.atomic(out/'batch_checkpoint.json',dict(plan=plan,completed=done,last_runs=peaks,status='in progress'))
    if code==75 or stop:raise SystemExit(75)
    if code!=0 or memory_limit:raise SystemExit(2)
    new+=1;done+=1
complete=done==len(allcases)
E.atomic(out/'batch_checkpoint.json',dict(plan=plan,completed=done,last_runs=peaks,status='complete' if complete else 'in progress'))
if complete:E.atomic(out/'COMPUTE_DONE.json',dict(plan=plan,completed=done,scope='Computations complete; scientific grading remains separate'))
raise SystemExit(0 if complete else 75)
