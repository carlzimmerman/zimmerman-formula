#!/usr/bin/env python3
"""Check completed runner records, exact audit/source pins and prior-packet preservation."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')
PRIOR=['final_closure_push','novel_closure_routes','attraction_from_existing','conversion_dynamics','polarization_link','collective_state_door','ugc08286_profile']


def sha(path,algorithm='sha256'):
    h=hashlib.new(algorithm)
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def checked(path,expected):
    actual=sha(path) if path.is_file() else None
    return {'path':str(path.relative_to(ROOT)),'expected_sha256':expected,'actual_sha256':actual,'passed':actual==expected}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    runs=[]
    for p in sorted(HERE.rglob('manifest.json')):
        d=json.loads(p.read_text())
        if d.get('schema_version')!=2:continue
        q=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True,timeout=30)
        runs.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'status':d['run']['status'],
            'validator_exit':q.returncode,'stdout':q.stdout.strip(),'stderr':q.stderr.strip(),
            'passed':q.returncode==0 and d['run']['status']=='completed'})
    old=[]
    for prefix in PRIOR:
        folder=ROOT/'reviews'/(prefix+'_2026_10_20');p=folder/'PACKET_SHA256.json';d=json.loads(p.read_text())
        cs=[checked(folder/n,h) for n,h in d['files'].items()]
        old.append({'inventory':str(p.relative_to(ROOT)),'inventory_sha256':sha(p),
                    'files_checked':len(cs),'all_passed':all(v['passed'] for v in cs),'checks':cs})
    provenance=[]
    for name,base in [('audit/METHOD_PROVENANCE.json',HERE/'audit'),
                       ('audit/PRE_RUN_PROVENANCE.json',HERE),('audit/ACTUAL_PROVENANCE.json',HERE),
                       ('warp/PROVENANCE.json',HERE/'warp')]:
        p=HERE/name;d=json.loads(p.read_text());v=d.get('artifacts',d.get('files'))
        cs=[checked(base/n, h['sha256'] if isinstance(h,dict) else h) for n,h in v.items()]
        provenance.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'all_passed':all(c['passed'] for c in cs),'checks':cs})
    acquisition=[]
    for item in json.loads((HERE/'data/ACQUISITION.json').read_text())['files']:
        p=ROOT/item['path'];c=checked(p,item['sha256'])
        c['release_md5_matches']=sha(p,'md5')==item['expected_md5'];acquisition.append(c)
    # Retained files only; failed endpoints and nonretained web responses are not
    # misclassified as missing scientific execution inputs.
    for item in json.loads((HERE/'independent/acquisition.json').read_text()):
        if 'path' in item and 'sha256' in item:
            acquisition.append(checked(ROOT/item['path'],item['sha256']))
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True,timeout=10).stdout.strip()
    passed=(len(runs)==8 and all(v['passed'] for v in runs)
        and all(v['all_passed'] for v in old+provenance)
        and all(v['passed'] and v.get('release_md5_matches',True) for v in acquisition))
    rec={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'assessment_base':'be8fc76cb0e207b88710f130abf2aa937f0895a5','observed_head':head,
      'all_checks_passed':passed,'completed_records':runs,'completed_count':len(runs),
      'earlier_files_preserved':sum(v['files_checked'] for v in old),'prior_packets':old,
      'audit_source_pin_freshness':provenance,'retained_acquisition_checks':acquisition,
      'limits':['Hashes certify identity, not interpretation or visibility independence.',
                'Verification is bookkeeping, not a new scientific experiment.',
                'No memory cap or CPU affinity is claimed enforced.']}
    if args.write:(HERE/'VERIFICATION.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'all_checks_passed':passed,'completed_runner_records':len(runs),
       'prior_files_preserved':rec['earlier_files_preserved'],
       'audit_source_pins':sum(len(v['checks']) for v in provenance),
       'retained_acquisition_pins':len(acquisition),'observed_head':head},indent=2))
    return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
