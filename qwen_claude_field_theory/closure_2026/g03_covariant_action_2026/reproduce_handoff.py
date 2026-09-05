#!/usr/bin/env python3
"""Run unchanged G02/G02b and parent tests in private, hashed snapshots.

Only this study directory receives generated evidence. Existing raw outputs
and manifests are hashed before and after, so concurrent changes are reported.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent-only', action='store_true')
    args = parser.parse_args()
    started = time.time()
    evidence = HERE / 'handoff_reproduction'
    evidence.mkdir(exist_ok=True)
    tracked = [BASE / p for p in (
        'g02_filtered_efe.py', 'g02_filtered_efe.out', 'g02_manifest.json',
        'g02b_tidal_identity_crosscheck.py', 'g02b_tidal_identity_crosscheck.out',
        'smoothed_onset_action_2026/onset_action_gate.py',
        'smoothed_onset_action_2026/test_onset_action_gate.py',
        'smoothed_onset_action_2026/CONTRACT.md',
        'smoothed_onset_action_2026/results.json',
        'smoothed_onset_action_2026/computation_manifest.json')]
    before = {str(p.relative_to(BASE)): digest(p) for p in tracked}
    for name in ('g02_filtered_efe.py', 'g02b_tidal_identity_crosscheck.py'):
        shutil.copy2(BASE / name, evidence / name)
    fixture = evidence / 'parent_fixture'
    parent = fixture / 'qwen_claude_field_theory' / 'closure_2026' / 'smoothed_onset_action_2026'
    parent.mkdir(parents=True, exist_ok=True)
    (fixture / 'hunt_2026').mkdir(exist_ok=True)
    for name in ('f29_coherence_length_law.py', 'f30_ppn_screening_door.py'):
        shutil.copy2(BASE.parents[1] / 'hunt_2026' / name, fixture / 'hunt_2026' / name)
    for name in ('onset_action_gate.py', 'test_onset_action_gate.py', 'CONTRACT.md'):
        shutil.copy2(BASE / 'smoothed_onset_action_2026' / name, parent / name)
    commands = [
        [sys.executable, str(evidence / 'g02_filtered_efe.py')],
        [sys.executable, str(evidence / 'g02b_tidal_identity_crosscheck.py')],
        [sys.executable, str(parent / 'test_onset_action_gate.py'), '-q'],
    ]
    previous = None
    if args.parent_only:
        previous = json.loads((HERE / 'handoff_reproduction.json').read_text())
        if previous['runs'][2]['exit_status'] != 0:
            failure_count = len(list(evidence.glob('run_3_initial_packaging_failure*.out')))
            shutil.copy2(evidence/'run_3.out', evidence/f'run_3_initial_packaging_failure_{failure_count+1}.out')
    runs = previous['runs'][:2] if previous else []
    for number, command in enumerate(commands, 1):
        if args.parent_only and number < 3:
            continue
        t = time.time()
        result = subprocess.run(command, capture_output=True, text=True,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        log = evidence / f'run_{number}.out'
        log.write_text(result.stdout + '\nSTDERR:\n' + result.stderr)
        runs.append(dict(command=command, exit_status=result.returncode,
                         runtime_seconds=time.time()-t, log=str(log.relative_to(HERE)),
                         sha256=digest(log)))
        print(f'[{"ok" if result.returncode == 0 else "FAIL"}] {number}: '
              f'{Path(command[1]).name}, rc={result.returncode}, {time.time()-t:.1f}s', flush=True)
    after = {str(p.relative_to(BASE)): digest(p) for p in tracked}
    unchanged = before == after
    print(f'[{"ok" if unchanged else "FAIL"}] 4: pre-existing evidence unchanged')
    payload = dict(commit=subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
                   sources_before=before, sources_after=after, unchanged=unchanged,
                   runs=runs, runtime_seconds=time.time()-started,
                   caveat='G02b resets FAILS after its imported G02 head; G02 is also run independently.')
    if previous:
        payload['previous_run'] = previous
    (HERE / 'handoff_reproduction.json').write_text(json.dumps(payload, indent=2)+'\n')
    return int(not unchanged or any(r['exit_status'] for r in runs))


if __name__ == '__main__':
    raise SystemExit(main())
