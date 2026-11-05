#!/usr/bin/env python3
"""Bounded stand-in child verifies actual batch signal forwarding and resume."""
import argparse,ast,hashlib,json,os,shutil,signal,subprocess,sys,time
from pathlib import Path
import psutil
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);args=parser.parse_args()
base=HERE/'batch_verified'/args.tag
if base.exists():raise RuntimeError('Fresh verification tag required')
base.mkdir(parents=True);checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
tree=ast.parse((HERE/'batch_small.py').read_text())
handler=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='handler')
check('handler_flag_only',not any(isinstance(n,ast.Call) for n in ast.walk(handler)))
worker='''import argparse,hashlib,json,os,signal,time
from pathlib import Path
import engines as E
p=argparse.ArgumentParser();p.add_argument('--index');p.add_argument('--rung');p.add_argument('--mutate',action='store_true');args=p.parse_args()
here=Path(__file__).parent;stop=[False]
def handler(s,f):stop[0]=True
signal.signal(signal.SIGTERM,handler);signal.signal(signal.SIGINT,handler)
(here/'child_ready.json').write_text(json.dumps(dict(pid=os.getpid())))
for i in range(60):
 if stop[0]:raise SystemExit(75)
 time.sleep(.01)
expected=E.hashes()
for name in ['small_worker.py','engines.py','FROZEN_CRITERIA.md']:expected[name]=hashlib.sha256((here/name).read_bytes()).hexdigest()
out=here/('mutate' if args.mutate else 'main')/'small'/('p%03d_r%d.json'%(int(args.index),int(args.rung)))
result=dict(source_hashes=expected,value=sum(i*i for i in range(100)),rung=int(args.rung))
tmp=out.with_suffix('.tmp')
with tmp.open('w') as f:json.dump(result,f,sort_keys=True);f.flush();os.fsync(f.fileno())
os.replace(tmp,out)
'''
for name in ['baseline','interrupted']:
 d=base/name;d.mkdir();shutil.copyfile(HERE/'batch_small.py',d/'batch_small.py')
 (d/'engines.py').write_text('def hashes():return {}\ndef points():return [(0.25,1.)]\n')
 (d/'FROZEN_CRITERIA.md').write_text('Process-control fixture only. No scientific grade.\n')
 (d/'small_worker.py').write_text(worker)
def command(name):return [sys.executable,str(base/name/'batch_small.py'),'--max-tasks','2','--resume']
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
r=subprocess.run(command('baseline'),env=env,capture_output=True,text=True,timeout=15);check('baseline_exit0',r.returncode==0)
with (base/'interrupt.log').open('w') as log:
 child=subprocess.Popen(command('interrupted'),env=env,stdout=log,stderr=log)
 deadline=time.monotonic()+10;worker_pid=None
 while time.monotonic()<deadline and child.poll() is None:
  ready=base/'interrupted/child_ready.json'
  if ready.exists():
   try:worker_pid=json.loads(ready.read_text())['pid']
   except json.JSONDecodeError:time.sleep(.001);continue
   child.send_signal(signal.SIGTERM);break
  time.sleep(.005)
 code=child.wait(timeout=15)
 check('live_child_observed',worker_pid is not None)
 check('parent_exit75',code==75)
 check('forwarded_child_terminated',worker_pid is not None and not psutil.pid_exists(worker_pid))
r=subprocess.run(command('interrupted'),env=env,capture_output=True,text=True,timeout=15);check('resumed_exit0',r.returncode==0)
for rung in [1,2]:
 f='main/small/p000_r%d.json'%rung
 check('exact_rung_'+str(rung),(base/'baseline'/f).read_bytes()==(base/'interrupted'/f).read_bytes())
previous={p.name:p.read_bytes() for p in (base/'interrupted/main/small').glob('*.json')}
r=subprocess.run(command('interrupted'),env=env,capture_output=True,text=True,timeout=15)
check('idempotent_completed_resume',r.returncode==0 and previous=={p.name:p.read_bytes() for p in (base/'interrupted/main/small').glob('*.json')})
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'batch_small.py',HERE/'AMENDMENTS.md']},scope='Bounded process-control fixture; no scientific engine modification or physical grade. kappa=1/2 FITTED; not theory closed')
(base/'checks.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
