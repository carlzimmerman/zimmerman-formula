#!/usr/bin/env python3
"""Actual SIGTERM/resume equivalence and checkpoint identity controls."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path
import numpy as np
import audit_inputs as A
parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);parser.add_argument('--homotopy',action='store_true');args=parser.parse_args()
base=A.HERE/'worker_verified'/args.tag
if base.exists():raise RuntimeError('Use a fresh verification tag')
base.mkdir(parents=True)
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
def command(name,extra=()):return [sys.executable,str(A.HERE/'worker3d.py'),'--source','bullet','--n','16','--foot','canonical','--tag',str((base/name).relative_to(A.HERE)),*(['--homotopy'] if args.homotopy else []),*extra]
def run(name,extra=()):return subprocess.run(command(name,extra),env=env,capture_output=True,text=True,timeout=45)
r=run('baseline');check('baseline_completes',r.returncode==0)
if r.returncode:raise RuntimeError(r.stderr)
with (base/'interrupt.log').open('w') as log:
 child=subprocess.Popen(command('interrupted'),env=env,stdout=log,stderr=log)
 deadline=time.monotonic()+30;observed=None;sent=False
 while time.monotonic()<deadline and child.poll() is None:
  path=base/'interrupted/checkpoint.npz'
  if path.exists():
   with np.load(path,allow_pickle=False) as z:state=json.loads(str(z['state']))
   if state.get('history') and state['history'][-1]['step']>=1 and state['status']=='running':
    observed=state['history'][-1]['step'];child.send_signal(signal.SIGTERM);sent=True;break
  time.sleep(.001)
 code=child.wait(timeout=30)
 check('live_accepted_step_observed',observed is not None)
 check('SIGTERM_exit75',sent and code==75)
r=run('interrupted',['--resume']);check('resume_completes',r.returncode==0)
for filename in ['field.npy','result.json']:
 check('exact_'+filename,(base/'baseline'/filename).read_bytes()==(base/'interrupted'/filename).read_bytes())
before=(base/'interrupted/result.json').read_bytes();r=run('interrupted',['--resume'])
check('complete_resume_idempotent',r.returncode==0 and before==(base/'interrupted/result.json').read_bytes())
r=run('baseline');check('existing_requires_resume',r.returncode!=0)
r=run('baseline',['--resume','--foot','alt']);check('changed_foot_rejected',r.returncode!=0)
r=run('forbidden',['--n','32']);check('unqueued_production_rejected',r.returncode!=0)
r=run('resume_fresh',['--resume']);check('resume_without_checkpoint_starts',r.returncode==0 and (base/'resume_fresh/result.json').read_bytes()==(base/'baseline/result.json').read_bytes())
# Deliberate change to a completed artifact must not be silently accepted.
p=base/'interrupted/field.npy';saved=p.read_bytes();p.write_bytes(saved+b'changed')
r=run('interrupted',['--resume']);check('changed_field_rejected',r.returncode!=0);p.write_bytes(saved)
obj=dict(homotopy=args.homotopy,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),interrupted_at_step=observed,source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),A.HERE/'worker3d.py',A.HERE/'newton3d.py',A.HERE/'grid3d.py',A.HERE/'spherical_boundary.py']},result_sha256=A.sha(base/'baseline/result.json'),scope='Actual bounded N16 SIGTERM/resume; no production convergence. kappa=1/2 FITTED; not theory closed')
A.atomic(base/'checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
