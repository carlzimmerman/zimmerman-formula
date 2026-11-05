#!/usr/bin/env python3
"""All eight pilot mock identities and live stage restart; no fit-based grading."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path
import numpy as np
import model as M
import raw_cube as R
import io_beam as B
parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);args=parser.parse_args()
root=R.HERE/args.tag
if root.exists():raise RuntimeError('Fresh tag required')
root.mkdir(parents=True);checks=[];reports={}
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
def command(case,weight='NA',foot='canonical',mock='law',extra=()):
 return [sys.executable,'-W','error',str(R.HERE/'mock_cube.py'),'--prepared',f'prepare_verified/baseline/{weight}_bin8','--tag',str((root/case).relative_to(R.HERE)),'--foot',foot,'--mock',mock,*extra]
def run(case,weight='NA',foot='canonical',mock='law',extra=()):
 with (root/(case+'.log')).open('a') as log:return subprocess.run(command(case,weight,foot,mock,extra),stdout=log,stderr=subprocess.STDOUT,env=env).returncode
for wi,weight in enumerate(['NA','R']):
 P=M.load_prepared(f'prepare_verified/baseline/{weight}_bin8')
 observed=(P['cube']*P['mask']).sum(0)
 for fi,foot in enumerate(['canonical','alt']):
  for mi,mock in enumerate(['law','slow']):
   case=f'{weight}_{foot}_{mock}';code=run(case,weight,foot,mock);check(case+'_completes',code==0)
   obj=json.loads((root/case/'mock_manifest.json').read_text());reports[case]=obj
   valid=all(R.sha(root/case/name)==h for stage in obj['stages'].values() for name,h in stage['outputs'].items())
   check(case+'_output_hashes',valid)
   signal_cube=np.load(root/case/'signal.npy',mmap_mode='r');noise=np.load(root/case/'noise.npy',mmap_mode='r');cube=np.load(root/case/'cube.npy',mmap_mode='r')
   check(case+'_exact_sum',np.array_equal(cube,signal_cube+noise) and np.all(np.isfinite(cube)))
   check(case+'_rms',abs(noise.std()/P['noise']-1)<=1e-12)
   meta=obj['stages']['noise']['scientific']
   check(case+'_seed_and_beam',meta['seed']==[20261105,46,wi,fi,mi] and meta['beam']==P['beam'])
   check(case+'_conditional_intensity',np.max(abs((signal_cube*P['mask']).sum(0)-np.maximum(observed,0)))<=1e-10)
   print('checked',case,flush=True)
 for foot in ['canonical','alt']:
  law=reports[f'{weight}_{foot}_law']['stages']['signal']['scientific'];slow=reports[f'{weight}_{foot}_slow']['stages']['signal']['scientific']
  check(weight+'_'+foot+'_slow_rotation_factor',abs(slow['rotation_at_2kpc']-.505*law['rotation_at_2kpc'])<=1e-12 and law['vc_at_2kpc']==slow['vc_at_2kpc'])
 check(weight+'_footings_not_pooled',reports[f'{weight}_canonical_law']['stages']['signal']['outputs']!=reports[f'{weight}_alt_law']['stages']['signal']['outputs'])
with (root/'interrupted.log').open('w') as log:
 child=subprocess.Popen(command('interrupted'),stdout=log,stderr=subprocess.STDOUT,env=env);deadline=time.monotonic()+60;observed=False
 while child.poll() is None and time.monotonic()<deadline:
  path=root/'interrupted/checkpoint.json'
  if path.exists() and json.loads(path.read_text()).get('status')=='noise':observed=True;break
  time.sleep(.01)
 if child.poll() is None:child.send_signal(signal.SIGTERM)
 code=child.wait(timeout=60)
check('live_noise_stage_observed',observed);check('SIGTERM_exit75',code==75)
check('resume_complete',run('interrupted',extra=['--resume'])==0)
a=(root/'NA_canonical_law/mock_manifest.json').read_bytes();b=(root/'interrupted/mock_manifest.json').read_bytes()
check('resumed_science_byte_identical',a==b)
check('completed_resume_idempotent',run('interrupted',extra=['--resume'])==0 and (root/'interrupted/mock_manifest.json').read_bytes()==b)
check('fresh_repeat_complete',run('repeat')==0)
check('fresh_repeat_byte_identical',(root/'repeat/mock_manifest.json').read_bytes()==a)
check('stale_footing_rejected',run('interrupted',foot='alt',extra=['--resume'])!=0)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in [Path(__file__),R.HERE/'mock_cube.py',R.HERE/'mock_noise.py',R.HERE/'model.py',R.HERE/'fitting.py']},scope='All eight bin8 mock construction identities and restart only; full rungs and fit-based KA1/KA2 pending')
B.atomic(root/'checks.json',obj);print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
