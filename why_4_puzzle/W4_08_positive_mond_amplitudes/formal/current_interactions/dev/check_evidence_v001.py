#!/usr/bin/env python3
"""Validate the selected bounded current proofs, controls and criteria binding."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAL = HERE.parent
ROOT = HERE.parents[3]
CRITERIA_SHA = 'ea6bb346feee335c4bf5b8851dd38cee133da938034f9b3563c4e9c230ed47dd'
CASES = {
    'final_current': (0, 6),
    'final_flux': (0, 3),
    'final_normal_v2': (0, 0),
    'final_wrong_current_v2': (1, 0),
    'final_occupied_vacuum_v2': (1, 0),
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
        assert data['inputs_unchanged'], case
        assert data['admission_token_scan_passed'], case
        assert data['only_standard_printed_axioms'], case
        assert data['toolchain'] == 'leanprover/lean4:v4.34.0-rc2', case
        assert data['mathlib_revision'] == '85e3a25e006c35636f0e53b0e9296caca2685bc0', case
        assert len(data['printed_axioms']) == count, case
        for axiom_list in data['printed_axioms']:
            assert set(axiom_list.replace('\n', ' ').split(', ')) == {
                'propext', 'Classical.choice', 'Quot.sound'}, case
        for name, digest in data['input_sha256'].items():
            assert sha(ROOT / name) == digest, (case, name)
        for name, digest in data['logs'].items():
            assert sha(directory / name) == digest, (case, name)
        stdout = (directory / 'stdout.txt').read_text()
        stderr = (directory / 'stderr.txt').read_text()
        assert not stderr, case
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
        'scope': 'Two new partial algebra modules, true controls, two false controls only',
        'criteria_commit': '33e139648', 'criteria_sha256': CRITERIA_SHA,
        'criteria_binding': 'This record binds the selected runner manifests to the additional current contract',
        'validator_sha256': sha(Path(__file__)), 'cases': rows,
        'analytic_sha256': {name: sha(HERE / name) for name in ['RESULT.md', 'SOURCES.md']},
        'not_formalized': ['Microscopic Gauss/current derivation', 'Field trial admissibility and integration',
                           'Variational infimum and asymptotic limit', 'Quantum health and vacuum selection'],
    }
    (HERE / 'VERIFIED.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: two new modules, nine critical standard-axiom theorem prints, normal controls, two False controls')
    print('Original goal remains open; this is not a microscopic MOND normalization proof')


if __name__ == '__main__':
    main()
