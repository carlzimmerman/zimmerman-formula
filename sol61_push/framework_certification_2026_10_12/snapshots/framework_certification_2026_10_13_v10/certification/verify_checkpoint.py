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
    if 'own_source_dependency' in module:
        dep = module['own_source_dependency']
        assert sha(ROOT / dep['path']) == dep['sha256']
        original = next(x for x in inventory['modules'] if x['namespace'] == dep['original_checked_module'])
        assert dep['sha256'] == original['source_sha256']
        package = (ROOT / module['source']).parent
        pinned = json.loads((package / 'PINNED_INPUTS.json').read_text())
        binary = pinned['dependency']
        assert sha(package / binary['compiled']) == binary['compiled_sha256']
        assert sha(package / binary['source']) == binary['source_sha256'] == dep['sha256']
        for item in pinned['inputs']:
            assert sha(ROOT / item['source']) == item['sha256']
            assert sha(package / item['snapshot']) == item['sha256']
    if 'PINNED_INPUTS' in module:
        rec = module['PINNED_INPUTS']
        assert sha(ROOT / rec['path']) == rec['sha256']
        package = (ROOT / module['source']).parent
        for item in json.loads((ROOT / rec['path']).read_text())['inputs']:
            assert sha(ROOT / item['source']) == item['sha256']
            assert sha(package / item['snapshot']) == item['sha256']
        cor = module['correspondence']
        assert sha(ROOT / cor['path']) == cor['sha256']
        for control in module['false_controls']:
            assert sha(ROOT / control['source']) == control['source_sha256']
            assert sha(ROOT / control['log']) == control['log_sha256']
            assert control['exit_code'] != 0
            assert '⊢ False' in (ROOT / control['log']).read_text()
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
for folder in ['architecture_review', 'transport_audit', 'kinetic_route_audit', 'resolved_resonance_audit', 'receiver_closure_audit', 'shared_phase_audit', 'gravitational_work_audit', 'minimal_metric_audit', 'metric_uniqueness_audit', 'metric_coordination']:
    for p in (HERE / folder).glob('*.json'):
        obj = json.loads(p.read_text())
        if not isinstance(obj, dict):
            continue
        hashes = obj.get('source_sha256', obj.get('source_hashes', {}))
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
    'minimal_metric_coupling/run/manifest.json': 'historical failed asymmetric vacuum substitution comparator; original source/run preserved; superseded by run_v2',
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
for rel, classification in [
    ('exact_run/manifest.json', 'current external spatial claim-support provenance'),
    ('spatial_run_portable/manifest.json', 'current external spatial claim-support provenance'),
    ('spatial_run/manifest.json', 'historical external resource-launch failure; no script execution; portable prefix-only retry retained')
]:
    path = ROOT / 'sol61_push/carrier_spatial_transport_2026_10_13' / rel
    obj = json.loads(path.read_text())
    result = subprocess.run([sys.executable, str(VALIDATOR), str(path), '--root', str(ROOT)], capture_output=True, text=True)
    records.append({'path': str(path.relative_to(ROOT)), 'exit_status': result.returncode,
                    'validator_output': result.stdout + result.stderr,
                    'schema_version': obj['schema_version'], 'classification': classification})
current = [x for x in records if x['classification'].startswith('current ')]
valid = all(x['exit_status'] == 0 for x in current)
report = {'checked_utc': datetime.now(timezone.utc).isoformat(),
          'all_current_claim_support_records_valid': valid,
          'checked_modules': checks, 'review_current_pinned_hashes_matched': review_hashes,
          'review_historical_pins_verified': historical_review_hashes,
          'records': records,
          'meaning': 'Provenance validity, not physical proof. Historical records preserved and excluded from positive current support; legacy-v1 limitations remain. Current spatial records are explicitly external-owner evidence.'}
(HERE / 'MANIFEST_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'valid': valid, 'modules': len(checks), 'theorems': inventory['theorem_count'],
                  'review_current_hashes': review_hashes, 'review_historical_pins': historical_review_hashes,
                  'current_manifests': len(current),
                  'historical_manifests': len(records) - len(current)}))
if not valid:
    raise SystemExit(1)
