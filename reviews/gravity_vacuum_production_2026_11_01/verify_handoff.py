"""Read-only provenance audit; write a new handoff report, never old records.

Usage: python3 reviews/gravity_vacuum_production_2026_11_01/verify_handoff.py
Requires the installed mathbox manifest validator. This checks saved evidence,
not the truth of a physics claim and not a new numerical experiment.
"""
import ast
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'HANDOFF_VERIFICATION.json'
NAMES = ('three_priorities', 'quantum_matching', 'finite_matching',
         'radial_ir_cold', 'gravity_vacuum_production')
DIRS = [ROOT / 'reviews' / (n + '_2026_11_01') for n in NAMES]
VALIDATOR = (Path.home() / '.codex/plugins/cache/openai-curated-remote/mathbox/'
             '4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


files = sorted(p for d in DIRS for p in d.rglob('*') if p.is_file() and p != OUT)
hashes = {p: sha(p) for p in files}
by_hash = collections.defaultdict(list)
for p, h in hashes.items():
    by_hash[h].append(str(p.relative_to(ROOT)))

syntax = []
for p in files:
    if p.suffix == '.py':
        ast.parse(p.read_text(), filename=str(p))
        syntax.append(str(p.relative_to(ROOT)))
    elif p.suffix == '.json':
        json.loads(p.read_text())

records = []
inputs = set()
for p in files:
    if p.name != 'manifest.json':
        continue
    m = json.loads(p.read_text())
    if m.get('schema_version') != 2:
        records.append({'path': str(p.relative_to(ROOT)),
                        'schema': m.get('schema_version'),
                        'note': 'Legacy adapter record; preserved, not a v2 numerical record.'})
        continue
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(p), '--root', str(ROOT)],
                          cwd=ROOT, capture_output=True, text=True)
    mismatches = []
    for item in m.get('input_artifacts', []):
        path = Path(item['path'])
        path = path if path.is_absolute() else ROOT / path
        inputs.add(path)
        expected = item['sha256']
        actual = sha(path) if path.is_file() else None
        if actual != expected:
            mismatches.append({'path': item['path'], 'expected_sha256': expected,
                               'current_sha256': actual,
                               'preserved_exact_sources': by_hash.get(expected, [])})
    records.append({'path': str(p.relative_to(ROOT)), 'schema': 2,
                    'sha256': hashes[p], 'recorded_status': m['run']['status'],
                    'validator_exit': proc.returncode,
                    'validator_output': (proc.stdout + proc.stderr).strip(),
                    'historical_input_differences': mismatches})

external = []
for p in sorted(inputs):
    if any(d == p or d in p.parents for d in DIRS):
        continue
    relative = str(p.relative_to(ROOT)) if ROOT in p.parents else str(p)
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', relative],
                             cwd=ROOT, capture_output=True).returncode == 0
    current = sha(p) if p.is_file() else None
    head_hash = hashlib.sha256(git('show', 'HEAD:' + relative)).hexdigest() if tracked else None
    external.append({'path': relative, 'exists_locally': p.is_file(),
                     'bytes': p.stat().st_size if p.is_file() else None,
                     'sha256': current, 'tracked': tracked,
                     'head_sha256': head_hash, 'current_matches_HEAD': current == head_hash if tracked else None,
                     'portability': 'Tracked input' if tracked else 'Local raw dependency excluded from this checkpoint'})

# Recheck every pinned artifact from TP04's frozen inventory without rewriting it.
prior = DIRS[3] / 'VERIFICATION.json'
pins = json.loads(prior.read_text())['artifact_pins']
pin_failures = []
for pin in pins:
    p = DIRS[3] / pin['path']
    if not p.is_file() or sha(p) != pin['sha256']:
        pin_failures.append(pin['path'])
assert not pin_failures, pin_failures

counts = collections.Counter(r.get('recorded_status', 'legacy') for r in records)
report = {
    'checkpoint': 'Claude handoff, unfinished TP05',
    'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'assessment_head': git('rev-parse', 'HEAD').decode().strip(),
    'scope': 'Fresh saved-file syntax, JSON, exact artifact pins and manifest provenance. No science rerun or claim of full physics validation.',
    'python_sources_parsed': len(syntax), 'prior_TP04_artifact_pins_rechecked': len(pins),
    'prior_TP04_artifact_pin_failures': pin_failures,
    'recorded_status_counts': dict(counts),
    'manifest_validator_current_successes': sum(r.get('validator_exit') == 0 for r in records),
    'manifest_validator_historical_or_other_differences': sum(r.get('validator_exit', 0) != 0 for r in records),
    'manifest_records': records, 'external_inputs': external,
    'portable_clone_limits': [
        'Raw spin/contraction snapshots and SL1 pickle cache are local dependencies, not committed.',
        'Historical failed/superseded manifests retain original bytes and statuses; changed-source entries may fail current-input validation.',
        'Only the TP01 dated erratum is staged in the active frozen verdict. Its full reviewed working copy is saved under handoff_reviewed_sources.',
        'Legacy adapter records are preserved separately from v2 numerical evidence.',
        'Production and protected gravity remain incomplete; consult each subroute STATUS.md.'
    ],
    'validator_sha256': sha(VALIDATOR),
    'artifact_inventory': [{'path': str(p.relative_to(ROOT)), 'sha256': hashes[p]} for p in files]
}
OUT.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ('python_sources_parsed', 'prior_TP04_artifact_pins_rechecked',
      'recorded_status_counts', 'manifest_validator_current_successes',
      'manifest_validator_historical_or_other_differences')}, indent=2))
print('External inputs:', len(external), 'not tracked:', sum(not e['tracked'] for e in external))
print('Saved', OUT.relative_to(ROOT))
