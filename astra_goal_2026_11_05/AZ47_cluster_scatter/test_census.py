#!/usr/bin/env python3
"""Known fixtures and deliberately corrupted outputs for the census auditor."""
import copy,hashlib,itertools,json,tempfile
from pathlib import Path
import check_census as C
checks=[]
def check(n,ok):checks.append(dict(name=n,passed=bool(ok)))
with tempfile.TemporaryDirectory(prefix='az47_auditor_') as d:
    C.ROOT=Path(d);C.HERE=C.ROOT/'lane';C.HERE.mkdir()
    source=C.ROOT/'input.dat';source.write_text('fixed fixture\n')
    base=dict(scientific=dict(status='complete retained-hit census',rows=20,unique_valid_formulas=20,
                             unique_covariance_err=3,unique_stable_covariance_err=2,statistics=dict(valid=20,min_Z_cov=1.)),
              identity=dict(files={'input.dat':C.digest(source)},chunk=1000))
    for level,foot,mode,tree in itertools.product(['L1','L2'],['canonical','alt'],['real','control'],['main','mutate']):
        for tag,chunk in [('census',1000),('census',2000),('census_repeat',2000)]:
            p=C.HERE/tag/f'{level}_{foot}_{mode}'/f'chunk{chunk}'/tree/'result.json';p.parent.mkdir(parents=True,exist_ok=True)
            obj=copy.deepcopy(base);obj['identity']['chunk']=chunk;p.write_text(json.dumps(obj))
    o=C.audit();check('complete_fixture',not o['failed'] and not o['pending'])
    p=C.HERE/'census/L1_canonical_real/chunk1000/main/result.json';original=p.read_text()
    obj=json.loads(original);obj['scientific']['unique_covariance_err']=4;p.write_text(json.dumps(obj))
    check('changed_count_detected',bool(C.audit()['failed']));p.write_text(original)
    obj=json.loads(original);obj['scientific']['statistics']['min_Z_cov']+=1e-11;p.write_text(json.dumps(obj))
    check('within_frozen_tolerance',not C.audit()['failed'])
    obj['scientific']['statistics']['min_Z_cov']=1+1e-8;p.write_text(json.dumps(obj))
    check('outside_frozen_tolerance_detected',bool(C.audit()['failed']));p.write_text(original)
    source.write_text('changed fixture\n');check('stale_source_detected',bool(C.audit()['failed']));source.write_text('fixed fixture\n')
    obj=json.loads(original);obj['scientific']['status']='INCOMPLETE PREFIX ONLY';p.write_text(json.dumps(obj))
    o=C.audit();check('prefix_never_full_pair',bool(o['pending']) and not o['sets'][0]['complete_pair']);p.write_text(original)
    repeat=C.HERE/'census_repeat/L1_canonical_real/chunk2000/main/result.json';saved=repeat.read_text();obj=json.loads(saved)
    obj['scientific']['rows']=19;repeat.write_text(json.dumps(obj));check('repeat_difference_detected',bool(C.audit()['failed']))
    repeat.unlink();check('missing_repeat_pending',bool(C.audit()['pending']))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
         source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(C.__file__)]},
         scope='Synthetic audit fixtures, including corrupt-output mutation; not a physical census result')
Path(__file__).with_name('census_auditor_checks.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
