"""Verify live checkpoint hashes and manifests without rewriting original evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
inventory = json.loads((HERE / 'CERTIFIED_CLAIMS.json').read_text())
checks = []
for module in inventory['modules']:
    for field in ['source', 'main_log']:
        assert sha(ROOT / module[field]) == module[field + '_sha256'], module[field]
    assert len(module['entries']) == module['theorem_count']
    log = (ROOT / module['main_log']).read_text()
    source = (ROOT / module['source']).read_text()
    assert 'error:' not in log and 'warning:' not in log
    assert not re.search(r'\b(sorry|native_decide)\b|^\s*axiom\s', source, re.M)
    for entry in module['entries']:
        assert entry['exact_statement'] in source
        assert hashlib.sha256(entry['exact_statement'].encode()).hexdigest() == entry['statement_sha256']
        assert set(entry['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert entry['name'] in log
    checks.append({'source': module['source'], 'statements': module['theorem_count'], 'hashes_match': True})
assert sum(x['statements'] for x in checks) == inventory['theorem_count']
assert inventory['theorem_count'] >= 79
review_hashes = 0
historical_review_pins = {}
historical_file = HERE / 'transport_audit/HISTORICAL_REVIEW_PINS.json'
if historical_file.exists():
    for item in json.loads(historical_file.read_text())['records']:
        historical_review_pins[(item['review'], item['path'])] = item
historical_review_hashes = 0
for folder in ['architecture_review', 'transport_audit', 'kinetic_route_audit']:
    for p in (HERE / folder).glob('*.json'):
        obj = json.loads(p.read_text())
        if not isinstance(obj, dict):
            continue
        hashes = obj.get('source_sha256', {})
        if isinstance(hashes, dict):
            for path, expected in hashes.items():
                actual = sha(ROOT / path)
                if actual == expected:
                    review_hashes += 1
                else:
                    key = (str(p.relative_to(ROOT)), path)
                    assert key in historical_review_pins, (p.name, path)
                    pin = historical_review_pins[key]
                    assert expected == pin['recorded_sha256'] == sha(ROOT / pin['historical_copy'])
                    assert actual == pin['current_sha256']
                    assert (ROOT / pin['reviewed_in']).is_file()
                    historical_review_hashes += 1

records = []
historical = {
    'local_power/run/manifest.json': 'historical failed warning gate; exact old source retained; excluded from current positive evidence',
    'local_interaction/run/manifest.json': 'historical contextual input; exact old context retained; superseded for current freshness by run_reconciled',
    'carrier_kinetic_reduction/run/manifest.json': 'historical failed symbolic sign predicate; original run/source preserved; superseded by run_v2'
}
for path in sorted(HERE.rglob('*manifest.json')):
    rel = path.relative_to(HERE)
    if any(x in {'snapshots', 'artifacts', 'inputs', 'source_snapshot'} for x in rel.parts):
        continue
    obj = json.loads(path.read_text())
    if 'schema_version' not in obj:
        continue
    result = subprocess.run([sys.executable, str(VALIDATOR), str(path), '--root', str(ROOT)], capture_output=True, text=True)
    classification = historical.get(str(rel), 'current claim-support provenance')
    records.append({'path': str(path.relative_to(ROOT)), 'exit_status': result.returncode,
                    'validator_output': result.stdout + result.stderr,
                    'schema_version': obj['schema_version'], 'classification': classification})
current = [x for x in records if x['classification'] == 'current claim-support provenance']
valid = all(x['exit_status'] == 0 for x in current)
report = {'checked_utc': datetime.now(timezone.utc).isoformat(),
          'all_current_claim_support_records_valid': valid,
          'checked_modules': checks, 'review_current_pinned_hashes_matched': review_hashes,
          'review_historical_pins_verified': historical_review_hashes,
          'records': records,
          'meaning': 'Provenance validity, not physical proof. Two historical records preserved and excluded from current freshness; legacy-v1 limitations remain.'}
(HERE / 'MANIFEST_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'valid': valid, 'modules': len(checks), 'theorems': inventory['theorem_count'],
                  'review_current_hashes': review_hashes, 'review_historical_pins': historical_review_hashes,
                  'current_manifests': len(current),
                  'historical_manifests': len(records) - len(current)}))
if not valid:
    raise SystemExit(1)
