#!/usr/bin/env python3
"""Check the bounded clock-tilt proof, exact controls and contract binding."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAL = HERE.parent
ROOT = HERE.parents[3]
CRITERIA_SHA = '60b24d49f7e17f6780279aa80ce792af0222eba0a6266975fc64b7becdc3f80a'
CASES = {
    'final_tilt': (0, 7),
    'final_normal': (0, 0),
    'final_stable_MUTATE': (1, 0),
    'final_quarter_MUTATE': (1, 0),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(HERE / 'FROZEN_CRITERIA.md') == CRITERIA_SHA
    rows = []
    for case, (expected, count) in CASES.items():
        directory = HERE / 'runs' / case
        manifest = directory / 'manifest.json'
        data = json.loads(manifest.read_text())
        assert data['run']['exit_status'] == expected, case
        assert data['run']['workers'] == 1, case
        assert data['run']['lean_memory_limit_mib'] == 1024, case
        assert data['run']['cpu_limit_seconds'] == 30, case
        assert data['run']['wall_limit_seconds'] == 45, case
        assert data['run']['children_maxrss_bytes'] < 1024 * 1024 ** 2, case
        assert data['inputs_unchanged'], case
        assert data['admission_token_scan_passed'], case
        assert data['only_standard_printed_axioms'], case
        assert data['toolchain'] == 'leanprover/lean4:v4.34.0-rc2', case
        assert data['mathlib_revision'] == '85e3a25e006c35636f0e53b0e9296caca2685bc0', case
        assert len(data['printed_axioms']) == count, case
        for axiom_list in data['printed_axioms']:
            assert set(axiom_list.replace('\n', ' ').split(', ')) <= {
                'propext', 'Classical.choice', 'Quot.sound'}, case
        for name, digest in data['input_sha256'].items():
            assert sha(ROOT / name) == digest, (case, name)
        for name, digest in data['logs'].items():
            assert sha(directory / name) == digest, (case, name)
        stdout = (directory / 'stdout.txt').read_text()
        assert not (directory / 'stderr.txt').read_text(), case
        if expected:
            lines = stdout.strip().splitlines()
            assert len(lines) == 2 and lines[0].endswith('error: unsolved goals'), case
            assert lines[1] == '⊢ False', case
        else:
            assert 'error' not in stdout and 'warning' not in stdout, case
            relative = Path(data['source']).relative_to(FORMAL.relative_to(ROOT))
            obj = FORMAL / 'build' / relative.with_suffix('.olean')
            assert sha(obj) == data['object_sha256'], case
        rows.append({'case': case, 'expected_exit': expected,
                     'critical_theorems': count, 'manifest_sha256': sha(manifest)})
    result = {
        'original_goal_achieved': False,
        'scope': 'One partial clock/static algebra module; true controls and two False controls',
        'criteria_commit': '609570aa2', 'criteria_sha256': CRITERIA_SHA,
        'criteria_binding': 'This record binds selected raw runner manifests to the additional clock/flux contract',
        'validator_sha256': sha(Path(__file__)), 'cases': rows,
        'analytic_sha256': {name: sha(HERE / name) for name in ['RESULT.md', 'SOURCES.md']},
        'not_formalized': ['Component and clock projection dictionaries',
                           'Auxiliary branch existence and eliminated asymptotics',
                           'Retained-mode Routh reduction and PDE interpretation',
                           'Top-form ensemble and source/flux derivations',
                           'Actual pi bounds, microscopic health and gravitating vacuum'],
    }
    (HERE / 'VERIFIED.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: one new module, seven critical standard-axiom prints, true controls, two False controls')
    print('Original goal open; the conditional static ratio is not a healthy gravitational prediction')


if __name__ == '__main__':
    main()
