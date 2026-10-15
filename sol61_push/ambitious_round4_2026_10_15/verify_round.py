"""Read-only round-four integrity check; this does not verify the mathematics."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
DEFAULT_VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validator', type=Path, default=DEFAULT_VALIDATOR)
    parser.add_argument('--output', type=Path, help='Fresh optional integrity receipt')
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('Refuse to overwrite an existing receipt')
    errors, rows = [], []
    stale = {'einstein/run_v1/manifest.json', 'einstein/run_v2/manifest.json'}
    manifests = sorted(BASE.rglob('manifest.json'))
    if len(manifests) != 25:
        errors.append('Expected the frozen 25-manifest round; found %d' % len(manifests))
    for path in manifests:
        rel = str(path.relative_to(BASE))
        manifest = json.loads(path.read_text())
        check = subprocess.run([sys.executable, str(args.validator), str(path),
                                '--root', str(ROOT)], capture_output=True, text=True)
        message = (check.stdout + check.stderr).strip()
        expected_stale = rel in stale
        correct = (check.returncode == 0) if not expected_stale else (
            check.returncode != 0 and 'input changed since the run:' in message
            and 'einstein/check_einstein.py' in message)
        if not correct:
            errors.append('Unexpected validator outcome: ' + rel + ': ' + message)
        rows.append(dict(manifest=str(path.relative_to(ROOT)),
                         status=manifest['run']['status'],
                         current_root_integrity_valid=check.returncode == 0,
                         expected_stale_historical_input=expected_stale,
                         classification_matches=correct, diagnostic=message))
    if sum(r['status'] == 'completed' for r in rows) != 22:
        errors.append('Expected 22 completed manifests')
    if sum(r['status'] == 'failed' for r in rows) != 3:
        errors.append('Expected three retained failed manifests')

    recovery = json.loads((BASE / 'einstein/HISTORICAL_INPUT_RECOVERY.json').read_text())
    recovered = []
    for item in recovery['runs']:
        mp = ROOT / item['historical_manifest']
        m = json.loads(mp.read_text())
        preimage = ROOT / item['preserved_exact_code_preimage']
        if sha(mp) != item['historical_manifest_sha256']:
            errors.append('Historical manifest changed: ' + str(mp))
        if sha(preimage) != item['preserved_sha256']:
            errors.append('Historical code preimage changed: ' + str(preimage))
        for entry in m['input_artifacts']:
            actual = preimage if entry['path'] == item['recorded_original_code_path'] else ROOT / entry['path']
            if not (sha(actual) == entry['sha256'] == entry['sha256_after']):
                errors.append('Historical input preimage mismatch: ' + str(actual))
        for entry in m['outputs']:
            if sha(ROOT / entry['path']) != entry['sha256']:
                errors.append('Historical output changed: ' + entry['path'])
        recovered.append(item['preserved_exact_code_preimage'])

    snapshot_count = 0
    for path in sorted(BASE.rglob('source_manifest.json')) + sorted(BASE.rglob('ORIGINS.json')):
        data = json.loads(path.read_text())
        entries = data['sources'] if isinstance(data, dict) else data
        for entry in entries:
            snapshot = ROOT / entry.get('snapshot', entry.get('copy', ''))
            if sha(snapshot) != entry['sha256']:
                errors.append('Frozen snapshot changed: ' + str(snapshot))
            snapshot_count += 1
    proof_hashes = {
        'angular/PROOF.md': '0b9f3fdb54c22303084a43cf39354de15709995f20e2371fdd4691985e88583d',
        'einstein/PROOF.md': '8a73f618c321c7e8af1b4abe1d8bc1e4168923b42084d495e3f10d14dc97c8cf',
        'inventory_energy/PROOF.md': '27e8c237f7099c25cd6cb908ca829fb1b5016caf3bda54ba7e972e266e34c16b',
    }
    for path, expected in proof_hashes.items():
        if sha(BASE / path) != expected:
            errors.append('Audited proof changed: ' + path)
    checkpoint = json.loads((BASE / 'source_checkpoint.json').read_text())
    for entry in checkpoint['sources']:
        blob = subprocess.run(['git', 'show', entry['revision'] + ':' + entry['path']],
                              cwd=ROOT, capture_output=True, check=True).stdout
        if hashlib.sha256(blob).hexdigest() != entry['sha256']:
            errors.append('Pinned Git source mismatch: ' + entry['path'])
    json_count = 0
    for path in BASE.rglob('*.json'):
        json.loads(path.read_text())
        json_count += 1
    receipt = dict(scope='Artifact integrity and failure classification only; not a mathematical verdict.',
                   observed_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                   manifests=rows, recovered_historical_code=recovered,
                   source_snapshots_checked=snapshot_count, audited_proof_hashes=proof_hashes,
                   pinned_git_sources_checked=len(checkpoint['sources']), json_files_parsed=json_count,
                   errors=errors, integrity_and_classification_passed=not errors)
    if args.output:
        with args.output.open('x') as stream:
            stream.write(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(manifests=len(rows), completed=22, retained_failed=3,
                          current_hash_valid=sum(r['current_root_integrity_valid'] for r in rows),
                          expected_stale_historical=len(stale), source_snapshots=snapshot_count,
                          errors=errors, passed=not errors), indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
