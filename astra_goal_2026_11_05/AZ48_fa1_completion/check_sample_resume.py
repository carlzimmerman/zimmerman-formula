#!/usr/bin/env python3
"""Live saved-field SIGTERM test with exact resumed scientific output."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path
import audit_inputs as A
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
base=A.HERE/'sample_resume_verified'/args.tag
if args.mutate:base=base/'mutate'
if base.exists():raise RuntimeError('Use a fresh verification tag')
base.mkdir(parents=True);checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
def command(name,extra=()):return [sys.executable,str(A.HERE/'sample_field.py'),'--field','worker_verified/contract_d/baseline','--tag',str((base/name).relative_to(A.HERE)),*(['--mutate'] if args.mutate else []),*extra]
def run(name,extra=()):return subprocess.run(command(name,extra),env=env,capture_output=True,text=True,timeout=30)
r=run('baseline');check('baseline_completes',r.returncode==0)
if r.returncode:raise RuntimeError(r.stderr)
with (base/'interrupt.log').open('w') as log:
 child=subprocess.Popen(command('interrupted'),env=env,stdout=log,stderr=log)
 deadline=time.monotonic()+15;phase=None
 while time.monotonic()<deadline and child.poll() is None:
  checkpoint=base/'interrupted/sampling_checkpoint.json'
  if checkpoint.exists():
   state=json.loads(checkpoint.read_text())
   if state['status']=='sampling' and any(state['discs'].values()):phase=state['status'];child.send_signal(signal.SIGTERM);break
  time.sleep(.0005)
 code=child.wait(timeout=15)
 check('live_completed_disc_observed',phase=='sampling');check('signal_exit75',code==75)
r=run('interrupted',['--resume']);check('resume_completes',r.returncode==0)
check('scientific_output_exact',(base/'baseline/samples.json').read_bytes()==(base/'interrupted/samples.json').read_bytes())
before=(base/'interrupted/samples.json').read_bytes();r=run('interrupted',['--resume'])
check('complete_idempotent',r.returncode==0 and before==(base/'interrupted/samples.json').read_bytes())
r=run('baseline');check('existing_output_requires_resume',r.returncode!=0)
r=run('fresh',['--resume']);check('fresh_resume_starts',r.returncode==0 and (base/'fresh/samples.json').read_bytes()==before)
path=base/'interrupted/samples.json';path.write_bytes(before+b'changed');r=run('interrupted',['--resume']);check('changed_completed_result_rejected',r.returncode!=0);path.write_bytes(before)
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),observed_phase=phase,source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),A.HERE/'sample_field.py',A.HERE/'sampling3d.py']},result_sha256=A.sha(base/'baseline/samples.json'),scope='Bounded live sampling restart only; no physical convergence. kappa=1/2 FITTED; not theory closed')
A.atomic(base/'checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
