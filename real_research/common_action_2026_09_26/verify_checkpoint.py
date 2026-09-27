#!/usr/bin/env python3
"""Reconcile accepted evidence. This verifies records, not physical closure."""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = pathlib.Path(__file__).resolve().parent
VALIDATOR = pathlib.Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py')

RUNS = {
    'action': ['run1', 'revised_run1', 'compensated_run1', 'perspective_run1', 'pq_run1'],
    'evolution': ['run_003', 'transition_run_001', 'cp_run_001', 'carrier_run_001',
                  'perspective_run_001', 'barrier_run_001', 'frw_run_001', 'pq_run_001'],
    'assembly': ['run1', 'gate_run1', 'projection_run1'],
    'transport': ['run_001', 'run_charge_001', 'run_lean_001', 'run_spatial_001',
                  'run_spatial_energy_001', 'run_conversion_001',
                  'run_conversion_packet_001', 'run_conversion_lean_001',
                  'run_homogeneous_frw_002'],
}

LEAN = [
    ('assembly/AssemblyBridge20260926.lean', 'assembly/lean_attempt2_record.json', 'assembly/lean_attempt2.log'),
    ('assembly/CanonicalAuxiliary20260926.lean', 'assembly/canonical_lean_attempt2_record.json', 'assembly/canonical_lean_attempt2.log'),
    ('assembly/BarrierBridge20260926.lean', 'assembly/barrier_lean_attempt2_record.json', 'assembly/barrier_lean_attempt2.log'),
    ('evolution/EvolutionBridge20260926.lean', 'evolution/lean_record.json', 'evolution/lean_attempt4.log'),
    ('evolution/PQBridge20260926.lean', None, None),
    ('transport/CommonTransport20260926.lean', 'transport/run_lean_001/results.json', 'transport/run_lean_001/stdout.txt'),
    ('transport/ConversionTransport20260926.lean', 'transport/run_conversion_lean_001/results.json', 'transport/run_conversion_lean_001/stdout.txt'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    result = {'purpose': 'Evidence reconciliation, not a full-theory certificate',
              'manifests': [], 'lean': [], 'errors': []}
    for lane, names in RUNS.items():
        for name in names:
            path = BASE/lane/name/'manifest.json'
            if not path.is_file():
                result['errors'].append('Missing manifest: '+str(path.relative_to(ROOT)))
                continue
            run = subprocess.run([sys.executable, str(VALIDATOR), str(path), '--root', str(ROOT)],
                                 text=True, capture_output=True)
            row = {'path': str(path.relative_to(ROOT)), 'sha256': sha(path),
                   'exit_code': run.returncode, 'validator_output': run.stdout+run.stderr}
            result['manifests'].append(row)
            if run.returncode:
                result['errors'].append('Manifest mismatch: '+row['path'])
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for source_name, record_name, log_name in LEAN:
        source = BASE/source_name
        if not source.is_file():
            result['errors'].append('Missing Lean source: '+source_name)
            continue
        source_sha = sha(source)
        if record_name is None:
            matches = []
            for path in (BASE/'evolution').glob('pq_lean_attempt*.json'):
                obj = json.loads(path.read_text())
                if obj.get('exit_code') == 0 and obj.get('source_sha256') == source_sha:
                    matches.append((path, obj))
            if not matches:
                result['errors'].append('No accepted current compile: '+source_name)
                continue
            record, obj = sorted(matches)[-1]
            log = pathlib.Path(obj['log_path'])
            if not log.is_absolute():
                log = ROOT/log
        else:
            record, log = BASE/record_name, BASE/log_name
            obj = json.loads(record.read_text())
        text = log.read_text()
        declarations = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", text, re.S)
        axioms = {a.strip() for _, group in declarations for a in group.split(',') if a.strip()}
        print_count = len(re.findall(r'^#print axioms ', source.read_text(), re.M))
        passed = (obj.get('exit_code', obj.get('returncode')) == 0
                  and obj.get('source_sha256') == source_sha
                  and bool(declarations) and len(declarations) == print_count
                  and axioms <= allowed and 'sorryAx' not in text
                  and not re.search(r'\berror(?:\(|:)', text))
        if 'log_sha256' in obj:
            passed = passed and obj['log_sha256'] == sha(log)
        row = {'source': str(source.relative_to(ROOT)), 'source_sha256': source_sha,
               'record': str(record.relative_to(ROOT)), 'record_sha256': sha(record),
               'log': str(log.relative_to(ROOT)), 'log_sha256': sha(log),
               'declaration_count': len(declarations), 'axioms': sorted(axioms),
               'warning_count': len(re.findall(r'^.+:\d+:\d+: warning(?:\([^)]*\))?:', text, re.M)),
               'passed': passed}
        result['lean'].append(row)
        if not passed:
            result['errors'].append('Lean record mismatch: '+source_name)
    result['passed'] = not result['errors']
    result['manifest_count'] = len(result['manifests'])
    result['lean_declaration_count'] = sum(r['declaration_count'] for r in result['lean'])
    (BASE/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in
                      ['passed', 'manifest_count', 'lean_declaration_count', 'errors']}, indent=2))
    return 0 if result['passed'] else 1

if __name__ == '__main__':
    sys.exit(main())
