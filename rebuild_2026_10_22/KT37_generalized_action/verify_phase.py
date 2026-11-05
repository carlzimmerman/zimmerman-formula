"""Validate retained records and the accepted, corrected KT37 MW checkpoint."""
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def read(name):
    return json.loads((HERE/name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = []
    for path in sorted(HERE.rglob('manifest.json')):
        check = subprocess.run([sys.executable,str(VALIDATOR),str(path),'--root',str(ROOT)],
                               capture_output=True,text=True)
        records.append(dict(path=str(path.relative_to(HERE)),
                            status=json.loads(path.read_text())['run']['status'],
                            valid=check.returncode==0, sha256=sha(path),
                            validation=check.stdout.strip(), error=check.stderr.strip()))
    assert len(records)==19 and all(r['valid'] for r in records)
    scan = read('mw/full_002/results.json')
    refinement = read('mw/refine_002/results.json')
    assert refinement['complete'] and refinement['all_checks_pass']
    selected = {}
    count = 0
    for foot, index, expected in [('canonical',1317,22),('alt',1206,50)]:
        for s in scan['footings'][foot]['scans']:
            assert len(s['rows'])==1375
            good = [r for r in s['rows'] if r['corrected']['all_four']]
            assert len(good)==s['summary']['n_pass']==(expected if s['ell_kpc']==3 else 0)
            assert not any(r['corrected']['Lh'] for r in good)
            count += len(s['rows'])
        rows = [r for r in refinement['footings'][foot] if r['ell_kpc']==3 and r['index']==index]
        assert len(rows)==6 and all(r['score']['all_four'] and not r['score']['Lh'] for r in rows)
        selected[foot] = next(r for r in rows if r['refine']==5)
    assert count==16500
    assert read('cassini/run_002/results.json')['all_checks_pass']
    assert read('dwarfs/run_001/results.json')['all_checks_pass']
    files = ['README.md','PLAN.md','mw/README.md','mw/full_002/results.json',
             'mw/refine_002/results.json','cassini/README.md','cassini/run_002/results.json',
             'cassini/REGULARIZATION_PROOF.md','dwarfs/README.md','dwarfs/run_001/results.json',
             'analytic/LINEAR_RESPONSE.md','analytic/GAUSSIAN_LIMIT_REVIEW.md']
    out = dict(records=records,manifest_count=len(records),
               statuses=dict(Counter(r['status'] for r in records)),
               all_manifest_hash_checks_valid=True, accepted_mw_population_states=count,
               selected_refinement5_witnesses=selected,
               withdrawn_empirical_records=['mw/pilot_001','mw/full_001','mw/refine_001'],
               accepted_operator='mw/generalized_v3.py; controls invariants_004 and covariance_green_002',
               qualification='A completed manifest alone is not scientific acceptance. The old angular operator is withdrawn. Primary MW/Cassini success does not remove strict Lh, isolated dwarf or static tidal-response limitations.',
               sha256={name:sha(HERE/name) for name in files})
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:out[k] for k in ['manifest_count','statuses','all_manifest_hash_checks_valid','accepted_mw_population_states']}))


if __name__=='__main__':
    main()
