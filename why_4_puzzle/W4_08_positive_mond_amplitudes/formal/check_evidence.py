#!/usr/bin/env python3
"""Check the current bounded Lean evidence; no compilation or physical inference."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASES = {
    'final_stress_exported': 0,
    'final_amplitude_types': 0,
    'final_scale_audited': 0,
    'final_cones': 0,
    'final_controls_normal': 0,
    'final_controls_reverse': 1,
    'final_controls_vacuum': 1,
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = []
    for case, expected in CASES.items():
        directory = HERE / 'runs' / case
        manifest = directory / 'manifest.json'
        record = json.loads(manifest.read_text())
        assert record['run']['exit_status'] == expected, case
        assert record['inputs_unchanged'], case
        assert record['admission_token_scan_passed'], case
        assert record['only_standard_printed_axioms'], case
        assert record['toolchain'] == 'leanprover/lean4:v4.34.0-rc2', case
        assert record['mathlib_revision'] == '85e3a25e006c35636f0e53b0e9296caca2685bc0', case
        for name, digest in record['input_sha256'].items():
            assert sha(ROOT / name) == digest, (case, 'changed input', name)
        for name, digest in record['logs'].items():
            assert sha(directory / name) == digest, (case, 'changed log', name)
        if expected:
            output = (directory / 'stdout.txt').read_text()
            assert 'error: unsolved goals\n⊢ False' in output, case
            assert 'Invalid simp theorem' not in output, case
        else:
            source_relative = Path(record['source']).relative_to(HERE.relative_to(ROOT))
            obj = HERE / 'build' / source_relative.with_suffix('.olean')
            assert record['object_sha256'] == sha(obj), case
            if 'controls/' not in str(source_relative):
                assert record['printed_axioms'], (case, 'no printed axioms')
        rows.append({'case': case, 'expected_exit': expected,
                     'manifest_sha256': sha(manifest),
                     'printed_critical_theorems': len(record['printed_axioms'])})
    result = {
        'original_goal_achieved': False,
        'scope': 'Four partial Lean modules and declared mutation controls only',
        'validator_sha256': sha(Path(__file__)),
        'cases': rows,
        'analytical_artifact_sha256': {
            name: sha(HERE / name) for name in
            ['MICROSCOPIC_CONTINUATION.md', 'REGULAR_PRESSURE_PARENT.md']},
        'deferred': {'source': 'PiBridge.lean', 'source_sha256': sha(HERE / 'PiBridge.lean'),
                     'status': 'Not verified: analysis import exceeds 1024 MiB cap'},
        'non_claims': ['No physical amplitude selector', 'No complete microscopic quantum model',
                       'No formalized PDE/source theorem']
    }
    (HERE / 'VERIFIED.json').write_text(json.dumps(result, indent=2) + '\n')
    count = sum(row['printed_critical_theorems'] for row in rows)
    print(f'PASS: four proof modules, normal control, two expected False controls; {count} printed critical axioms checked')
    print('Original why-4 goal is not achieved; PiBridge and physical selection remain open')


if __name__ == '__main__':
    main()
