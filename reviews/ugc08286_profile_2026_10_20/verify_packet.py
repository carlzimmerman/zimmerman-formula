#!/usr/bin/env python3
"""Read-only evidence/preservation checks; --write saves closeout records only."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')
PRIOR = ['final_closure_push', 'novel_closure_routes', 'attraction_from_existing',
         'conversion_dynamics', 'polarization_link', 'collective_state_door']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pin(path, expected):
    actual = sha(path) if path.is_file() else None
    return {'path': str(path.relative_to(ROOT)), 'expected_sha256': expected,
            'actual_sha256': actual, 'passed': actual == expected}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    runs, excluded, acquisitions = [], [], []
    # Exact filename: a source MANIFEST.json is not a computation-run manifest.
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or p.name.lower() != 'manifest.json':
            continue
        d = json.loads(p.read_text())
        rel = str(p.relative_to(ROOT))
        if d.get('schema_version') != 2 or 'run' not in d:
            acquisitions.append({'path': rel, 'sha256': sha(p), 'schema': d.get('schema'),
                                 'classification': 'source acquisition; not runner schema'})
            continue
        if d['run']['status'] != 'completed':
            excluded.append({'path': rel, 'sha256': sha(p), 'status': d['run']['status'],
                             'classification': 'historical failed attempt; excluded from scientific evidence; current inputs may differ'})
            continue
        argv = [sys.executable, str(VALIDATOR), str(p), '--root', str(ROOT)]
        q = subprocess.run(argv, capture_output=True, text=True, timeout=20)
        runs.append({'path': rel, 'sha256': sha(p), 'run_status': d['run']['status'],
                     'exit_status': q.returncode, 'stdout': q.stdout.strip(),
                     'stderr': q.stderr.strip(), 'passed': q.returncode == 0})
    prior = []
    for prefix in PRIOR:
        packet = ROOT / 'reviews' / (prefix + '_2026_10_20')
        inventory = packet / 'PACKET_SHA256.json'
        d = json.loads(inventory.read_text())
        checks = [check_pin(packet / name, checksum) for name, checksum in d['files'].items()]
        prior.append({'inventory': str(inventory.relative_to(ROOT)), 'inventory_sha256': sha(inventory),
                      'files_checked': len(checks), 'all_passed': all(c['passed'] for c in checks),
                      'checks': checks})
    reviews = []
    for name in ['audit/PROVENANCE.json', 'audit/EXTENT_PROVENANCE.json']:
        p = HERE / name
        d = json.loads(p.read_text())
        checks = [check_pin(HERE / n, v['sha256']) for n, v in d['artifacts'].items()]
        reviews.append({'provenance': str(p.relative_to(ROOT)), 'sha256': sha(p),
                        'all_passed': all(c['passed'] for c in checks), 'checks': checks})
    source_checks = []
    data = json.loads((HERE / 'data/MANIFEST.json').read_text())
    for v in data['input_files'] + [data['verification_script']]:
        source_checks.append(check_pin(HERE / 'data' / v['path'], v['sha256']))
    for v in json.loads((HERE / 'stellar/retrieval_manifest.json').read_text()):
        source_checks.append(check_pin(ROOT / v['path'], v['sha256']))
    q = subprocess.run([sys.executable, str(HERE / 'data/verify_inputs.py')],
                       capture_output=True, text=True, timeout=20)
    auth = json.loads(q.stdout)
    old_auth = json.loads((HERE / 'data/INPUT_VERIFICATION.json').read_text())
    auth_record = {'exit_status': q.returncode, 'all_checks_passed': auth['all_checks_pass'],
                   'check_count': len(auth['checks']), 'matches_saved_record': auth == old_auth,
                   'checks': auth['checks']}
    run_record = {'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'validator': str(VALIDATOR), 'validator_sha256': sha(VALIDATOR),
                  'completed_records': runs, 'completed_count': len(runs),
                  'all_completed_records_valid': len(runs) == 9 and all(v['passed'] for v in runs),
                  'historical_failed_excluded': excluded, 'source_manifests': acquisitions,
                  'classification_note': 'Only completed v2 runner records are checked against current execution inputs. Historical failures are preserved without refreshing their input hashes.'}
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True,
                          text=True, check=True, timeout=10).stdout.strip()
    passed = (run_record['all_completed_records_valid'] and len(excluded) == 2
              and all(v['all_passed'] for v in prior + reviews)
              and all(v['passed'] for v in source_checks)
              and auth_record['all_checks_passed'] and auth_record['matches_saved_record'])
    verification = {'recorded_utc': run_record['recorded_utc'], 'assessment_base': 'e8bb2ae70ad6b2c86790b9312861ac2269227f71',
                    'observed_head_at_verification': head, 'all_checks_passed': passed,
                    'prior_packet_files_preserved': sum(v['files_checked'] for v in prior),
                    'prior_packets': prior, 'independent_review_freshness': reviews,
                    'retained_source_hash_checks': source_checks,
                    'primary_input_authentication': auth_record,
                    'run_validation': 'RUN_VALIDATION.json',
                    'limitations': ['Hash checks verify artifact identity, not scientific interpretation.',
                                    'Nonretained web-source versions remain source records, not freshly redownloaded raw files.',
                                    'No scientific computation repeated by this bookkeeping verification.',
                                    'No hard memory cap or CPU affinity claimed.']}
    if args.write:
        (HERE / 'RUN_VALIDATION.json').write_text(json.dumps(run_record, indent=2) + '\n')
        (HERE / 'VERIFICATION.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps({'all_checks_passed': passed, 'completed_runner_records': len(runs),
                      'historical_failed_records_excluded': len(excluded),
                      'prior_files_preserved': verification['prior_packet_files_preserved'],
                      'review_pins_checked': sum(len(v['checks']) for v in reviews),
                      'source_pins_checked': len(source_checks), 'primary_authentication': auth_record,
                      'observed_head': head}, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
