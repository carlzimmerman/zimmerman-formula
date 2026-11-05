#!/usr/bin/env python3
"""Evidence provenance fixtures and deliberate field-hash bypass mutation."""
import argparse,json,shutil
from pathlib import Path
import evidence as E
import audit_inputs as A
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
base=A.HERE/'evidence_verified'/args.tag
if args.mutate:base=base/'mutate'
if base.exists():raise RuntimeError('Fresh fixture tag required')
(base/'field').mkdir(parents=True);(base/'samples').mkdir();checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
for name in ['field.npy','result.json','checkpoint.npz']:shutil.copyfile(A.HERE/'worker_verified/contract_d/baseline'/name,base/'field'/name)
for name in ['samples.json','sampling_checkpoint.json']:shutil.copyfile(A.HERE/'sample_resume_verified/contract_c/baseline'/name,base/'samples'/name)
obj,provenance=E.authenticate_sample(base/'field',base/'samples');check('valid_field_and_samples',obj['status']=='PILOT ONLY' and not obj['mutate'])
prerequisites=E.prerequisites();check('all_15_prerequisite_reports_current',prerequisites['verified'] and len(prerequisites['records'])==15)
def rejected(fn):
 try:fn()
 except (E.EvidenceError,ValueError,KeyError,OSError):return True
 return False
field=base/'field/field.npy';saved=field.read_bytes();original_sha=A.sha;digest=A.sha(field)
field.write_bytes(saved+b'changed')
if args.mutate:E.A.sha=lambda p:digest if Path(p).resolve()==field.resolve() else original_sha(p)
check('changed_raw_field_rejected',rejected(lambda:E.authenticate_sample(base/'field',base/'samples')))
E.A.sha=original_sha;field.write_bytes(saved)
samples=base/'samples/samples.json';saved=samples.read_bytes();samples.write_bytes(saved+b'changed')
check('changed_sample_report_rejected',rejected(lambda:E.authenticate_sample(base/'field',base/'samples')));samples.write_bytes(saved)
cp=base/'samples/sampling_checkpoint.json';saved=cp.read_bytes();changed=json.loads(saved);changed['status']='preparing';cp.write_text(json.dumps(changed))
check('unfinished_sampling_rejected',rejected(lambda:E.authenticate_sample(base/'field',base/'samples')));cp.write_bytes(saved)
changed=json.loads(saved);changed['identity']['mutate']=True;cp.write_text(json.dumps(changed))
check('wrong_sampling_identity_rejected',rejected(lambda:E.authenticate_sample(base/'field',base/'samples')));cp.write_bytes(saved)
check('empty_source_map_rejected',rejected(lambda:E.source_hashes({})))
check('changed_source_hash_rejected',rejected(lambda:E.source_hashes({A.relative(A.HERE/'sampling3d.py'):'0'*64})))
check('outside_source_path_rejected',rejected(lambda:E.source_hashes({'../../outside':'0'*64})))
check('changed_environment_rejected',rejected(lambda:E.versions({'numpy':'not-a-version'})))
report=base/'prerequisite.json';x=json.loads((A.HERE/'sampling_checks.json').read_text());x['checks'].pop();report.write_text(json.dumps(x))
check('missing_check_rejected',rejected(lambda:E.check_report(report,42)))
x=json.loads((A.HERE/'sampling_checks.json').read_text());x['checks'][1]=x['checks'][0];report.write_text(json.dumps(x))
check('duplicate_check_rejected',rejected(lambda:E.check_report(report,42)))
check('expected_mutation_must_bite',rejected(lambda:E.check_report(A.HERE/'sampling_checks.json',42,['isotropic_sample_invariant'])))
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),prerequisite_errors=prerequisites['errors'],source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(E.__file__).resolve()]},scope='Provenance fixture only; no production field eligibility. kappa=1/2 FITTED; not theory closed')
A.atomic(base/'checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
