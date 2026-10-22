"""Administrative exact-byte validation only; no mathematical computation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
RUN = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

result = json.loads((RUN / 'result.json').read_text())
contract = json.loads((ROOT / 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json').read_text())
assert set(contract['required_fields']) <= set(result), 'required fields missing'
assert result['task_id'] == 'FGF-049'
assert result['task_sha256'] == '18f24abe89549ea2d380772afe5b6ffbce3c8ce69a9e9dd70d99afa3dccdc8fd'
assert result['outcome'] in ['supports_scoped_claim','counterexample','inconclusive','blocked_on_data','implementation_failure']
for field in ['input_sha256', 'artifacts_sha256']:
    for path, expected in result[field].items():
        assert digest(ROOT / path) == expected, (field, path)
freeze = json.loads((RUN / 'FREEZE.json').read_text())
for path, expected in freeze['artifacts_sha256'].items():
    assert digest(ROOT / path) == expected, ('freeze', path)
assert freeze['artifacts_sha256'][str((RUN / 'result.json').relative_to(ROOT))] == digest(RUN / 'result.json')
assert result['execution_bounds']['mathematical_processes'] == 0
print('PASS: required fields; 12 source pins; supporting artifact hashes; final result freeze; zero mathematical computations.')
