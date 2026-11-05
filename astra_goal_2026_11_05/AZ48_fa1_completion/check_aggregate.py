#!/usr/bin/env python3
"""Reject missing production roles, substituted pilots and broken sign twins."""
import argparse,copy,json,shutil
from pathlib import Path
import aggregate as G
import evidence as E
import audit_inputs as A
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);args=p.parse_args()
base=A.HERE/'aggregation_verified'/args.tag
if base.exists():raise RuntimeError('Fresh fixture tag required')
base.mkdir(parents=True);checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
empty=G.collect(base/'empty')
check('empty_ladders_incomplete',empty['status']=='INCOMPLETE')
for foot in ['canonical','alt']:
 r=empty['footings'][foot]
 check(foot+'_empty_no_verdict',r['main']['numerical_status']=='UNDECIDED' and r['main']['conditional_reading'] is None)
 check(foot+'_all_roles_missing',len(r['missing'])==14 and r['authenticated_main']==r['authenticated_mutate']==0)
field=A.HERE/'worker_verified/contract_d/baseline'
main,_=E.authenticate_sample(field,A.HERE/'sample_resume_verified/contract_c/baseline')
mut,_=E.authenticate_sample(field,A.HERE/'sample_resume_verified/mutation_b/mutate/baseline')
check('real_pilot_sign_pair',G.sign_twin(main,mut))
for name,change in [('field',lambda r:r.update(field_sha256='0'*64)),('mode',lambda r:r.update(mutate=False)),('threshold',lambda r:r.update(inherited_threshold=.01)),('point',lambda r:r['points']['BCG1'].update(s=.5)),('disc',lambda r:r['discs']['BCG1'][1].update(mean_s=.5))]:
 changed=copy.deepcopy(mut);change(changed);check('changed_twin_'+name+'_rejected',not G.sign_twin(main,changed))
# The artifact itself is valid, but its actual N16 identity cannot fill N128.
name=G.key_name('bullet',128,4000.,'canonical');target=base/'substituted'
(target/'fields'/name).mkdir(parents=True)
for filename in ['field.npy','result.json','checkpoint.npz']:shutil.copyfile(field/filename,target/'fields'/name/filename)
for mode,original in [('main',A.HERE/'sample_resume_verified/contract_c/baseline'),('mutate',A.HERE/'sample_resume_verified/mutation_b/mutate/baseline')]:
 out=target/'samples'/mode/name;out.mkdir(parents=True)
 for filename in ['samples.json','sampling_checkpoint.json']:shutil.copyfile(original/filename,out/filename)
rejected=G.collect(target)['footings']['canonical']
check('pilot_cannot_fill_production_role',len(rejected['errors'])==2 and rejected['authenticated_main']==rejected['authenticated_mutate']==0 and rejected['main']['numerical_status']=='UNDECIDED')
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(G.__file__).resolve(),Path(E.__file__).resolve()]},scope='Evidence-aggregation fixtures only; no physical ladder supplied. kappa=1/2 FITTED; not theory closed')
A.atomic(base/'checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
