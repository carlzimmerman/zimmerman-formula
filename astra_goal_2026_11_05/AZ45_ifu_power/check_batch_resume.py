#!/usr/bin/env python3
"""Real bounded IFU batch interruption, worker checkpoint and exact recovery."""
import argparse,ast,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
import psutil
import engine as E
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--tag',required=True);ap.add_argument('--structure-only',action='store_true');args=ap.parse_args()
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
tree=ast.parse((P/'batch.py').read_text());handler=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='stopping')
check('handler_flag_only',not any(isinstance(n,ast.Call) for n in ast.walk(handler)))
if args.structure_only:
 print(json.dumps(checks,indent=2));raise SystemExit(int(not checks[0]['passed']))
base=P/'batch_verified'/args.tag
if base.exists():raise RuntimeError('Fresh tag required')
base.mkdir(parents=True);env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
def command(name):return [sys.executable,str(P/'batch.py'),'--tag',str((base/name).relative_to(P)),'--max-cases','1','--resume']
def run(name):
 with (base/(name+'_run.log')).open('w') as log:return subprocess.run(command(name),env=env,stdout=log,stderr=log,timeout=55)
r=run('baseline');check('bounded_baseline_exit75',r.returncode==75)
key='t00_r1_canonical_n0_flat_s30_free_reference_0.01'
with (base/'interrupt.log').open('w') as log:
 parent=subprocess.Popen(command('interrupted'),env=env,stdout=log,stderr=log)
 deadline=time.monotonic()+20;worker=None;seen=None;sent=False
 while time.monotonic()<deadline and parent.poll() is None:
  active=base/'interrupted/active_child.json'
  active_state=json.loads(active.read_text()) if active.exists() else {}
  if active_state.get('parent_pid')==parent.pid and active_state.get('status')=='running':
   if worker is None:worker=psutil.Process(active_state['pid']);seen=time.monotonic()
   if time.monotonic()-seen>=1. and worker.is_running():parent.send_signal(signal.SIGTERM);sent=True;break
  time.sleep(.02)
 code=parent.wait(timeout=30)
 check('interrupted_live_worker',sent and worker is not None)
 check('parent_exit75',code==75)
 check('no_remaining_child',worker is not None and not psutil.pid_exists(worker.pid))
checkpoint=base/'interrupted/reference'/(key+'.checkpoint.json')
check('actual_worker_checkpoint',checkpoint.exists())
r=run('interrupted');check('bounded_resume_exit75',r.returncode==75)
file=base/'interrupted/reference'/(key+'.json');reference=base/'baseline/reference'/(key+'.json')
check('scientific_output_exact',file.exists() and reference.read_bytes()==file.read_bytes())
before=file.read_bytes();state=json.loads((base/'interrupted/batch_checkpoint.json').read_text())
check('one_case_completed_after_resume',state['completed']==1 and state['status']=='in progress')
r=run('interrupted');state=json.loads((base/'interrupted/batch_checkpoint.json').read_text())
check('next_batch_preserves_completed_case',r.returncode==75 and file.read_bytes()==before and state['completed']==2)
check('partial_grid_has_no_done_marker',not (base/'interrupted/COMPUTE_DONE.json').exists())
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),scientific_sha256=hashlib.sha256(before).hexdigest(),source_hashes={**E.hashes(),**{str(p.relative_to(E.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),P/'batch.py',P/'worker.py',P/'AMENDMENTS.md']}},scope='Real bounded controller/worker restart; only first two cases, not production power or convergence. kappa=1/2 FITTED; not theory closed')
E.atomic(base/'checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
