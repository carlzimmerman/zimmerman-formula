#!/usr/bin/env python3
"""Live interruption/resume and identity tests for an ungraded 8x8 fit unit."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path
import io_beam as B
import raw_cube as R
parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);args=parser.parse_args()
root=R.HERE/args.tag
if root.exists():raise RuntimeError('Fresh test tag required')
root.mkdir(parents=True);checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
base=[sys.executable,'-W','error',str(R.HERE/'fit_unit.py'),'--prepared','prepare_verified/baseline/NA_bin8','--model','free','--start-inc','35','--budget','2']
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
def command(name,*extra):return base+['--tag',str((root/name).relative_to(R.HERE))]+list(extra)
def run(name,*extra):
 with (root/(name.replace('/','_')+'.log')).open('a') as log:return subprocess.run(command(name,*extra),stdout=log,stderr=subprocess.STDOUT,env=env).returncode
check('baseline_completes',run('baseline')==0)
with (root/'interrupted.log').open('w') as log:
 child=subprocess.Popen(command('interrupted'),stdout=log,stderr=subprocess.STDOUT,env=env)
 deadline=time.monotonic()+60;observed=False
 while child.poll() is None and time.monotonic()<deadline:
  path=root/'interrupted/checkpoint.json'
  if path.exists() and json.loads(path.read_text()).get('status')=='fitting':observed=True;break
  time.sleep(.01)
 if observed:child.send_signal(signal.SIGTERM)
 else:
  if child.poll() is None:child.terminate()
 code=child.wait(timeout=60)
check('live_fitting_observed_before_signal',observed)
check('SIGTERM_yields_75',code==75,code)
check('resume_completes',run('interrupted','--resume')==0)
a=(root/'baseline/result.json').read_bytes();b=(root/'interrupted/result.json').read_bytes()
check('resume_science_byte_identical',a==b)
check('complete_resume_idempotent',run('interrupted','--resume')==0 and (root/'interrupted/result.json').read_bytes()==b)
check('fresh_repeat_completes',run('repeat')==0)
check('fresh_repeat_byte_identical',(root/'repeat/result.json').read_bytes()==a)
check('stale_start_rejected',run('interrupted','--resume','--start-inc','48')!=0)
check('production_budget_unqueued_rejected',run('production_rejected','--budget','100')!=0)
check('mutation_tree_enforced',run('bad_mutation','--dataset','mutate')!=0)
fit=json.loads(a)['fit']
check('evaluation_stop_not_accepted',fit['status']==0 and not fit['optimizer_accepted'])
# Known-answer primitives have their separate checker; these only verify the unit contract.
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
 source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in [Path(__file__),R.HERE/'fit_unit.py',R.HERE/'fitting.py',R.HERE/'model.py']},
 scope='8x8 budget2 ungraded fit contract only; not production optimizer convergence or KA1/KA2')
B.atomic(root/'checks.json',obj)
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
