#!/usr/bin/env python3
"""Validate current TP01 artifacts without rerunning production calculations."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifests = [
        'run_reconciliation/manifest.json',
        'law_dictionary/run_002/manifest.json',
        'law_dictionary/adapter_004/manifest.json',
        'spin_contraction/run_002/manifest.json',
        'spin_contraction/run_004/manifest.json',
        'spectrum_pressure/run_diagnostic/manifest.json',
        'spectrum_pressure/run_diagnostic_supported/manifest.json',
        'spectrum_pressure/run_blocks/manifest.json',
        'spectrum_pressure/run_pressure/manifest.json',
        'spectrum_pressure/run_exact_gap/manifest.json',
        'spectrum_pressure/run_density/manifest.json',
    ]
    records = []
    for relative in manifests:
        path = HERE/relative
        result = subprocess.run([sys.executable, str(VALIDATOR), str(path),
                                 '--root', str(ROOT)], capture_output=True, text=True)
        data = json.loads(path.read_text())
        record = {'path': relative, 'sha256': sha(path),
                  'run_status': data['run']['status'],
                  'current_hash_validation_exit': result.returncode,
                  'validator_output': (result.stdout+result.stderr).strip()}
        records.append(record)
        print(relative, record['run_status'], 'validation_exit', result.returncode)
    assert all(v['current_hash_validation_exit'] == 0 for v in records)
    assert sum(v['run_status'] == 'completed' for v in records) == 9
    assert records[2]['run_status'] == 'failed'
    assert records[5]['run_status'] == 'launch-failed'

    inputs = json.loads((HERE/'law_dictionary/INPUTS.json').read_text())['inputs']
    preserved = []
    for item in inputs[2:]:
        assert sha(ROOT/item['path']) == item['sha256']
        preserved.append(item['path'])
    edits = json.loads((HERE/'law_dictionary/EDIT_RECORD.json').read_text())['files']
    for item in edits:
        assert sha(ROOT/item['path']) == item['after_sha256']
    frozen = ROOT/'covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md'
    before = HERE/'initial_sources/covariant_push_2026_10_22__V3S_FINAL_VERDICT_2026-10-24.md'
    assert frozen.read_bytes().startswith(before.read_bytes())
    snapshot = json.loads((HERE/'INPUT_SNAPSHOT.json').read_text())
    for item in snapshot['inputs']:
        assert sha(ROOT/item['snapshot']) == item['sha256']
        if not item['path'].startswith('covariant_push_'):
            assert sha(ROOT/item['path']) == item['sha256']

    adapter = json.loads((HERE/'law_dictionary/adapter_004/result.json').read_text())
    assert adapter['returncode'] == 0 and adapter['checks']['no_sorryAx']
    assert adapter['stdout'].count('depends on axioms:') == 5
    assert adapter['checks']['observed_RSS_below_1GB'] is False

    reviewed = [
        'README.md', 'HANDOFF.md', 'SPIN_REVIEW.md', 'SOURCE_CHECKS.md',
        'COORDINATOR_DICTIONARY_AUDIT.md', 'PRESSURE_MAPPING_REVIEW.md',
        'spectrum_pressure/INDEPENDENT_REVIEW.md',
        'spectrum_pressure/INDEPENDENT_REVIEW_INPUTS.json',
    ]
    links = []
    for relative in reviewed:
        path = HERE/relative
        assert path.is_file(), relative
        if path.suffix != '.md':
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('http:', 'https:', '#')):
                continue
            local = (path.parent/target.split('#')[0]).resolve()
            assert local.is_file() or local == HERE/'VERIFICATION.json', (relative, target)
            links.append({'from': relative, 'target': target})
    review_pins = [{'path': p, 'sha256': sha(HERE/p)} for p in reviewed]
    result = {
        'checkpoint': 'TP01',
        'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'base_head': snapshot['base_head'],
        'assessment_head': subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                         capture_output=True, text=True, check=True).stdout.strip(),
        'scope': 'Current-input provenance, preserved source bytes, correction hunks, adapter output and links; mathematical interpretation remains in the linked reviews.',
        'manifest_records': records,
        'completed_numerical_records': 9,
        'lean_adapter': {'compiler_exit': 0, 'theorems': 5, 'sorryAx': False,
                         'wrapper_status': 'failed',
                         'reason': 'Observed compiler RSS 1542733824 bytes exceeds its explicit 1 GB target'},
        'historical_failures': 'Earlier launch, aperture, serialization and adapter attempts remain in each route; successful source versions are pinned separately. They are not additional mathematical failures or successful evidence.',
        'original_solver_certificate_inputs_unchanged': preserved,
        'all_initial_snapshots_match': True,
        'frozen_verdict_initial_bytes_preserved_as_prefix': True,
        'current_summary_matches_reviewed_edit_hashes': True,
        'review_pins': review_pins,
        'local_links_checked': links,
        'no_production_simulation_or_external_write_by_TP01': True,
        'overall': 'Three bounded research priorities executed; correction complete, physical completion remains open.'}
    (HERE/'VERIFICATION.json').write_text(json.dumps(result, indent=2)+'\n')
    print('TP01 artifact verification completed; nine completed numerical records and documented resource/launch failures.')


if __name__ == '__main__':
    main()
