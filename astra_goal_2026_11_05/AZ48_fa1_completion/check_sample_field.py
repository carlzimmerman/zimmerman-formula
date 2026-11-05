#!/usr/bin/env python3
"""Bounded saved-field integration checks, including provenance rejection."""
import argparse,json,os,shutil,subprocess,sys
from pathlib import Path
import audit_inputs as A
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);args=p.parse_args()
base=A.HERE/'sampling_verified'/args.tag
if base.exists():raise RuntimeError('Fresh test tag required')
base.mkdir(parents=True);checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
source=A.HERE/'worker_verified/contract_d/baseline'
for name in ['field.npy','result.json','checkpoint.npz']:shutil.copyfile(source/name,base/name)
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
def run(tag,mutate=False):
 command=[sys.executable,str(A.HERE/'sample_field.py'),'--field',str(base.relative_to(A.HERE)),'--tag',str((base/tag).relative_to(A.HERE))]
 if mutate:command.append('--mutate')
 if (base/tag/'sampling_checkpoint.json').exists():command.append('--resume')
 return subprocess.run(command,env=env,capture_output=True,text=True,timeout=30)
for tag,mutation in [('main',False),('mutate',True)]:
 r=run(tag,mutation);check(tag+'_executes',r.returncode==0)
 if r.returncode:raise RuntimeError(r.stderr)
main=json.loads((base/'main/samples.json').read_text());mut=json.loads((base/'mutate/samples.json').read_text())
check('same_field_both_outputs',main['field_sha256']==mut['field_sha256'])
check('independent_residual',main['residual_eligible'] and main['residual']==mut['residual'])
check('pilot_cannot_be_physical_verdict',main['status']==mut['status']=='PILOT ONLY')
check('point_sign_twin',all(main['points'][k]['s']==-mut['points'][k]['s'] for k in main['points']))
check('disc_mean_sign_twin',all(main['discs'][k][i]['mean_s']==-mut['discs'][k][i]['mean_s'] for k in main['discs'] for i in [0,1]))
for tag,mutation in [('main',False),('mutate',True)]:
 before=(base/tag/'samples.json').read_bytes();r=run(tag,mutation)
 check(tag+'_exact_repeat',r.returncode==0 and before==(base/tag/'samples.json').read_bytes())
r=run('wrong_output',True);check('mutation_tree_enforced',r.returncode!=0)
field=base/'field.npy';saved=field.read_bytes();field.write_bytes(saved+b'changed');r=run('tampered');check('changed_field_rejected',r.returncode!=0);field.write_bytes(saved)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),A.HERE/'sample_field.py',A.HERE/'sampling3d.py']},outputs={tag:A.sha(base/tag/'samples.json') for tag in ['main','mutate']},scope='N16 saved-field integration only; no physical convergence. kappa=1/2 FITTED; not theory closed')
A.atomic(base/'checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
