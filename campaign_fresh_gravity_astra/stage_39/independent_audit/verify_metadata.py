"""Read-only FGF052 reviewer ancestry, freeze and optional comparison verifier."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(mapping):
    for name, expected in mapping.items():
        actual = sha(ROOT / name)
        assert actual == expected, (name, expected, actual)

ancestry = json.loads((HERE / 'ANCESTRY_VERIFICATION.json').read_text())
assert len(ancestry['checks']) == 10
for record in ancestry['checks']:
    assert record['passed'] and record['expected'] == record['actual']
    assert sha(ROOT / record['path']) == record['expected']
verify(json.loads((HERE / 'input_sha256.json').read_text()))
freeze = json.loads((HERE / 'independent_freeze.json').read_text())
assert not freeze['author_exposure'] and not freeze['new_coordinator_proof_exposure']
verify(freeze['artifacts_sha256'])
result_path = HERE / 'audit_result.json'
if result_path.exists():
    result = json.loads(result_path.read_text())
    verify(result['artifacts_sha256'])
    verify(result['author_pins'])
    verify(result['reviewed_coordinator_pins'])
print('PASS: ten ancestry pins, independent source map and frozen derivation; optional audit outputs checked if present. Read-only metadata verification; zero mathematical computations.')
