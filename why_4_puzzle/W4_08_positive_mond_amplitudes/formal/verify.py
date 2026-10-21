#!/usr/bin/env python3
"""Compile one local proof with the installed pinned library and bounded resources."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = ROOT / 'fable_independent_2026/lean_2026'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('module', help='Lean source relative to this directory')
    parser.add_argument('output', help='New evidence directory relative to this directory')
    args = parser.parse_args()
    source = (HERE / args.module).resolve()
    out = (HERE / args.output).resolve()
    if not source.is_relative_to(HERE) or not out.is_relative_to(HERE):
        raise ValueError('Paths must remain in the local formal directory')
    out.mkdir(parents=True, exist_ok=False)
    pin = (LIB / 'lean-toolchain').read_text().strip()
    bins = Path.home() / '.elan/toolchains' / pin.replace('/', '--').replace(':', '---') / 'bin'
    query = subprocess.run([str(bins / 'lake'), 'env', 'printenv', 'LEAN_PATH'],
                           cwd=LIB, text=True, capture_output=True, timeout=15, check=True)
    env = os.environ.copy()
    paths = [str((LIB / p).resolve()) for p in query.stdout.strip().split(os.pathsep)]
    paths.append(str(HERE / 'build'))
    env['LEAN_PATH'] = os.pathsep.join(paths)
    for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
        env[key] = '1'
    obj = HERE / 'build' / Path(args.module).with_suffix('.olean')
    obj.parent.mkdir(parents=True, exist_ok=True)
    if obj.exists():
        obj.unlink()
    command = ['lean', '-j1', '-M1024', '-o', str(obj.relative_to(HERE)), args.module]
    inputs = {str(p.relative_to(ROOT)): sha(p) for p in
              [source, Path(__file__), HERE / 'FROZEN_CRITERIA.md',
               LIB / 'lean-toolchain', LIB / 'lakefile.toml', LIB / 'lake-manifest.json']}
    # A local imported object is accepted only with a matching source/object
    # stamp from this runner; source text and object are both pinned below.
    for name in re.findall(r'^(?:public |meta )?import ([\w.]+)\s*$', source.read_text(), re.M):
        local = HERE / (name.replace('.', '/') + '.lean')
        if local.is_file():
            imported = HERE / 'build' / (name.replace('.', '/') + '.olean')
            stamp = imported.with_suffix('.provenance.json')
            data = json.loads(stamp.read_text())
            if data['source_sha256'] != sha(local) or data['object_sha256'] != sha(imported):
                raise ValueError('Stale local imported object: ' + name)
            for path in [local, imported, stamp]:
                inputs[str(path.relative_to(ROOT))] = sha(path)
        elif name.startswith('Mathlib.'):
            relative = Path(name.replace('.', '/'))
            package = LIB / '.lake/packages/mathlib'
            for path in [(package / relative).with_suffix('.lean'),
                         (package / '.lake/build/lib/lean' / relative).with_suffix('.olean')]:
                inputs[str(path.relative_to(ROOT))] = sha(path)

    def cpu_limit():
        resource.setrlimit(resource.RLIMIT_CPU, (30, 31))

    start = time.monotonic()
    status = 'completed'
    with (out / 'stdout.txt').open('w') as stdout, (out / 'stderr.txt').open('w') as stderr:
        try:
            result = subprocess.run([str(bins / 'lean'), *command[1:]], cwd=HERE, env=env,
                                    stdout=stdout, stderr=stderr, timeout=45, preexec_fn=cpu_limit)
            exit_status = result.returncode
        except subprocess.TimeoutExpired:
            exit_status, status = 124, 'timeout'
    if exit_status and status == 'completed':
        status = 'failed'
    text = (out / 'stdout.txt').read_text() + (out / 'stderr.txt').read_text()
    axioms = re.findall(r'depends on axioms: \[(.*?)\]', text, flags=re.S)
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    axiom_check = all(set(x.replace('\n', ' ').split(', ')) <= allowed for x in axioms)
    admission_free = not re.search(r'\b(sorry|admit|native_decide|unsafe)\b', source.read_text())
    unchanged = all(sha(ROOT / p) == digest for p, digest in inputs.items())
    record = {
        'schema': 'W4-08-lean-bounded-v1', 'source': str(source.relative_to(ROOT)),
        'command': command, 'toolchain': pin,
        'mathlib_revision': json.loads((LIB / 'lake-manifest.json').read_text())['packages'][0].get('rev'),
        'input_sha256': inputs, 'inputs_unchanged': unchanged,
        'run': {'status': status, 'exit_status': exit_status,
                'runtime_seconds': time.monotonic() - start,
                'cpu_limit_seconds': 30, 'wall_limit_seconds': 45,
                'lean_memory_limit_mib': 1024, 'workers': 1,
                'children_maxrss_bytes': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},
        'printed_axioms': axioms, 'only_standard_printed_axioms': axiom_check,
        'admission_token_scan_passed': admission_free,
        'logs': {p.name: sha(p) for p in [out / 'stdout.txt', out / 'stderr.txt']},
        'object_sha256': sha(obj) if obj.is_file() else None,
        'scope': 'Only this Lean module under its stated hypotheses; no microscopic coefficient selection implied'
    }
    (out / 'manifest.json').write_text(json.dumps(record, indent=2) + '\n')
    if exit_status == 0 and unchanged and admission_free and axiom_check:
        obj.with_suffix('.provenance.json').write_text(json.dumps({
            'source_sha256': sha(source), 'object_sha256': sha(obj)
        }, indent=2) + '\n')
    print(json.dumps({'source': args.module, 'status': status, 'exit': exit_status,
                      'seconds': round(record['run']['runtime_seconds'], 3),
                      'standard_axioms': axiom_check, 'unchanged': unchanged}))
    return exit_status if exit_status else (0 if unchanged and admission_free and axiom_check else 2)


if __name__ == '__main__':
    sys.exit(main())
