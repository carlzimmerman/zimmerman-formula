#!/usr/bin/env python3
"""Audit all frozen retained sets, without treating unfinished prefixes as pairs."""
import argparse,hashlib,itertools,json,math,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()
def audit(tag='census',repeat='census_repeat'):
    checks=[];sets=[];pending=[];hashes={}
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    def read(p):
        if not p.exists():pending.append(str(p.relative_to(HERE)));return None
        obj=json.loads(p.read_text())
        for name,expected in obj['identity']['files'].items():
            if name not in hashes:hashes[name]=digest(ROOT/name)
            check(str(p.relative_to(HERE))+':source:'+name,hashes[name]==expected)
        if obj['scientific']['status']!='complete retained-hit census':
            pending.append(str(p.relative_to(HERE))+': incomplete');return None
        return obj
    for level,foot,mode in itertools.product(['L1','L2'],['canonical','alt'],['real','control']):
        name=f'{level}_{foot}_{mode}';rows={};allpair=True;allrepeat=True
        for tree in ['main','mutate']:
            paths=[HERE/tag/name/f'chunk{c}'/tree/'result.json' for c in [1000,2000]]
            objs=[read(p) for p in paths]
            rr=read(HERE/repeat/name/'chunk2000'/tree/'result.json')
            if any(x is None for x in objs):allpair=False
            else:
                a,b=objs;sa,sb=a['scientific'],b['scientific']
                ia={k:v for k,v in a['identity'].items() if k!='chunk'}
                ib={k:v for k,v in b['identity'].items() if k!='chunk'}
                check(name+':'+tree+':pair_identity',ia==ib)
                for key in ['rows','unique_valid_formulas','unique_covariance_err','unique_stable_covariance_err']:
                    check(name+':'+tree+':'+key,sa[key]==sb[key])
                for key,value in sa['statistics'].items():
                    other=sb['statistics'][key]
                    ok=(value==other) if not isinstance(value,float) else math.isclose(value,other,rel_tol=1e-10,abs_tol=0)
                    check(name+':'+tree+':statistics:'+key,ok)
                rows[tree]=dict(rows=sb['rows'],unique_valid=sb['unique_valid_formulas'],
                                covariance=sb['unique_covariance_err'],stable=sb['unique_stable_covariance_err'],statistics=sb['statistics'])
            if rr is None or objs[1] is None:allrepeat=False
            else:
                check(name+':'+tree+':repeat_identity',rr['identity']==objs[1]['identity'])
                check(name+':'+tree+':repeat_scientific_bytes',
                      json.dumps(rr['scientific'],sort_keys=True)==json.dumps(objs[1]['scientific'],sort_keys=True))
        sets.append(dict(set=name,complete_pair=allpair,complete_repeat=allrepeat,results=rows))
    failed=[c['name'] for c in checks if not c['passed']]
    return dict(status='UNDECIDED: failed validation' if failed else ('IN PROGRESS: missing full census/pairs/repeats' if pending else 'full census validation passed'),
                sets=sets,checks=checks,failed=failed,pending=pending,
                verifier_sha256=digest(Path(__file__)),
                scope='Conditional G3 bookkeeping only; calibrated population inference NO VERDICT; kappa=1/2 FITTED; not theory closed')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--tag',default='census');ap.add_argument('--repeat',default='census_repeat');a=ap.parse_args()
    out=audit(a.tag,a.repeat);p=HERE/'census_checks.json';tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(out,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
    print(json.dumps(dict(status=out['status'],failed=len(out['failed']),pending=len(out['pending']),complete_pairs=[r['set'] for r in out['sets'] if r['complete_pair']]),indent=2))
    raise SystemExit(1 if out['failed'] else (75 if out['pending'] else 0))
