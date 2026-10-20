#!/usr/bin/env python3
"""Check the bounded gravitational algebra, controls and frozen contract binding."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAL = HERE.parent
ROOT = HERE.parents[3]
CRITERIA_SHA = '133113855fb5135de10cc66efe3aa891ffcabb3f481ce6d9e1120df4e747b9de'
CASES = {
    'final_gravity03': (0, 14),
    'final_normal': (0, 0),
    'final_boundary_MUTATE': (1, 0),
    'final_normalization_MUTATE': (1, 0),
    'final_scalar_only_MUTATE': (1, 0),
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
        'scope': 'One partial gravitational algebra module; true controls and three False controls',
        'criteria_commit': '201229b5f', 'criteria_sha256': CRITERIA_SHA,
        'criteria_binding': 'This record binds selected raw runner manifests to the additional gravitational-constraint contract',
        'validator_sha256': sha(Path(__file__)), 'cases': rows,
        'analytic_sha256': {name: sha(HERE / name) for name in ['RESULT.md', 'SOURCES.md']},
        'review_sha256': {name: sha(HERE / name) for name in ['REVIEW.md', 'REVIEW_VECTOR.md', 'REVIEW_CRITICAL.md']},
        'not_formalized': ['Covariant component expansion, ADM PDE constraints and boundary variation',
                           'Physical retained-mode identification and weak-gravity continuity',
                           'Regularity and validity cutoff of the rational component action',
                           'Matter-source, combined force and gravitating-density dictionaries',
                           'Actual pi bounds, microscopic health and amplitude selection'],
    }
    (HERE / 'VERIFIED.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: one new module, fourteen critical standard-axiom prints, true controls, three False controls')
    print('Original goal open; quadratic constraints and a target fit do not supply a microscopic selector')


if __name__ == '__main__':
    main()
