"""Extend checkpoint verification without rewriting previously pinned verifier sources."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
base = subprocess.run([sys.executable, str(HERE / 'verify_checkpoint.py')], cwd=HERE, capture_output=True, text=True)
if base.returncode:
    print(base.stdout + base.stderr)
    raise SystemExit(base.returncode)
base_counts = json.loads(base.stdout)
records = []
for review in sorted((HERE / 'nonspherical_flux/audit').glob('*.json')):
    obj = json.loads(review.read_text())
    if not isinstance(obj, dict):
        continue
    pins = obj.get('source_sha256', obj.get('source_hashes', {}))
    if not isinstance(pins, dict):
        continue
    for path, expected in pins.items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        assert actual == expected, ('Fullflux review source changed', path)
        records.append({'review': str(review.relative_to(ROOT)), 'source': path, 'sha256': actual})
report = json.loads((HERE / 'nonspherical_flux/audit/results.json').read_text())
assert report['formal_review_pending'] is False
assert records, 'No final fullflux source review pins'
result = {'checked_utc': datetime.now(timezone.utc).isoformat(),
          'valid': True, 'base_verification': base_counts,
          'additional_review_reference_hashes': len(records), 'additional_review_pins': records,
          'meaning': 'Scoped kernel and exact provenance verification. Source/host/model admission and empirical/whole-theory closure are separate.'}
(HERE / 'FULLFLUX_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'valid': True, 'theorems': base_counts['theorems'], 'modules': base_counts['modules'],
                  'base_review_reference_hashes': base_counts['review_current_hashes'],
                  'additional_review_reference_hashes': len(records),
                  'historical_review_pins': base_counts['review_historical_pins'],
                  'current_manifests': base_counts['current_manifests'],
                  'historical_manifests': base_counts['historical_manifests']}))
