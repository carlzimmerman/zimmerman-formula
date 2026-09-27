"""Verify the accepted CD26-3 evidence, without rerunning completed science.

Hashes, actual successful compiler records, every printed axiom dependency,
bounded-run manifests, and frozen source snapshots are checked. This is an
evidence audit, not an additional physics proof or a data fit.
"""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return str(path.resolve().relative_to(ROOT))


def compiler_record(source):
    """Select only a recorded successful compile of these exact source bytes."""
    candidates = []
    for path in BASE.rglob('*.json'):
        if 'source_snapshots' in path.parts:
            continue
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            continue
        argv = data.get('command', data.get('child_command', []))
        code = data.get('exit_code', data.get('returncode', -1))
        sha = data.get('source_sha256', data.get('sha256'))
        if not isinstance(argv, list) or not argv or 'lean' not in argv:
            continue
        if Path(argv[-1]).resolve() != source.resolve() or code != 0 or sha != digest(source):
            continue
        if path.name == 'results.json':
            log = path.with_name('stdout.txt')
        elif data.get('log', data.get('log_path')):
            log = Path(data.get('log', data.get('log_path')))
            if not log.is_absolute():
                log = (ROOT / log) if (ROOT / log).exists() else path.parent / log
        else:
            log = path.with_suffix('.log')
        assert log.exists(), ('missing recorded log', path, log)
        if data.get('log_sha256'):
            assert digest(log) == data['log_sha256'], ('log drift', log)
        candidates.append((path, data, log))
    assert candidates, ('no successful compile for exact current source', source)
    return sorted(candidates, key=lambda item: item[0].stat().st_mtime)[-1]


def main():
    certificates = []
    for rel, expected_count in [
        ('reconstruction/InversePressure20260926.lean', 6),
        ('scales/ScalesInverse20260926.lean', 12),
        ('spectral_inverse/SpectralInverse20260926.lean', 9),
        ('gates_clock/GateClockInverse20260926.lean', 4),
    ]:
        source = BASE / rel
        record, data, log = compiler_record(source)
        source_text = source.read_text()
        clean = re.sub(r'/-.*?-/', '', source_text, flags=re.S)
        clean = re.sub(r'--[^\n]*', '', clean)
        assert not re.search(r'\b(sorry|admit)\b|^\s*axiom\s', clean, flags=re.M)
        printed = re.findall(r'^#print axioms ([A-Za-z0-9_.]+)', source_text, re.M)
        log_text = log.read_text()
        assert 'error:' not in log_text and 'sorryAx' not in log_text
        rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log_text, re.S)
        axioms = {name: [a.strip() for a in deps.split(',') if a.strip()] for name, deps in rows}
        assert len(axioms) == len(printed) == expected_count
        assert {n.rsplit('.', 1)[-1] for n in axioms} == {n.rsplit('.', 1)[-1] for n in printed}
        assert all(set(values) <= ALLOWED for values in axioms.values())
        certificates.append({
            'source': relative(source), 'source_sha256': digest(source),
            'record': relative(record), 'record_sha256': digest(record),
            'log': relative(log), 'log_sha256': digest(log),
            'theorem_count': len(axioms), 'axioms': axioms,
            'compiler_warnings': log_text.count('warning:'),
        })

    validator = Path.home() / '.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py'
    runs = ['reconstruction/run1', 'reconstruction/plot_run2', 'scales/run_005',
            'gates_clock/run1', 'spectral_inverse/run_001', 'spectral_inverse/run_lean_001']
    validations = []
    for name in runs:
        manifest = BASE / name / 'manifest.json'
        result = subprocess.run(['python3', str(validator), str(manifest), '--root', str(ROOT)],
                                capture_output=True, text=True)
        validations.append({'manifest': relative(manifest), 'sha256': digest(manifest),
                            'exit_code': result.returncode,
                            'stdout': result.stdout, 'stderr': result.stderr})
    assert all(item['exit_code'] == 0 for item in validations), validations
    inventory = json.loads((BASE / 'scales/source_snapshot_inventory.json').read_text())
    for entry in inventory['sources']:
        assert digest(ROOT / entry['snapshot_path']) == entry['sha256'], entry

    # Read-only source-review drift is reported separately from execution input
    # validation. A later live note does not change a frozen accepted source.
    provenance = json.loads((BASE / 'gates_clock/source_provenance.json').read_text())
    live_source_drift = []
    for entry in provenance['consulted_local_sources']:
        current = ROOT / entry['path']
        if not current.exists() or digest(current) != entry['sha256']:
            live_source_drift.append(entry['path'])

    spec = ROOT / 'qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md'
    recipe = ROOT / 'qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md'
    result = {
        'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Accepted mathematical evidence and hypotheses only; no full gravity or empirical certificate',
        'theorem_count': sum(x['theorem_count'] for x in certificates),
        'Lean_files': len(certificates), 'certificates': certificates,
        'accepted_manifest_count': len(validations), 'manifest_validation': validations,
        'frozen_source_count': len(inventory['sources']),
        'live_review_source_drift': live_source_drift,
        'spec_sha256': digest(spec), 'recipe_sha256_at_verification': digest(recipe),
        'repository_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'lean_version': subprocess.check_output(['/opt/homebrew/bin/lean', '--version'], text=True).strip(),
        'mathlib_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT / 'fable_independent_2026/lean_2026/.lake/packages/mathlib', text=True).strip(),
        'full_theory': 'OPEN', 'new_observational_fit': False,
    }
    (BASE / 'evidence_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in
                     ['theorem_count', 'Lean_files', 'accepted_manifest_count',
                      'frozen_source_count', 'live_review_source_drift', 'full_theory']}))


if __name__ == '__main__':
    main()
