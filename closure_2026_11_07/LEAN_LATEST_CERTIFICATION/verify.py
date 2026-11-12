#!/usr/bin/env python3
"""Compile the latest kernel/stiffness/spherical follow-up against the pinned Lean/Mathlib revision.
Use --library-project to reuse an existing matching Mathlib build, or omit it
for lake env lean in this repository. Source and evidence hashes are checked
before/after compilation. Numerical evidence is recorded, not re-certified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT / 'fable_independent_2026/lean_2026'
SOURCES = {'LimberKernel.lean': 'LimberKernel', 'StiffnessStress.lean': 'StiffnessStress',
           'SphericalPhantom.lean': 'SphericalPhantom'}
EVIDENCE = ['closure_2026_11_07/GL1_limber_kernel_reread/RESULT.md',
            'closure_2026_11_07/GL1_limber_kernel_reread/gl1.py',
            'closure_2026_11_07/GL1_limber_kernel_reread/gl1.json',
            'closure_2026_11_07/HOLD_KERNEL_REREAD_2026_11_07.md',
            'closure_2026_11_07/GL2_limber_k4_audit/RESULT.md',
            'closure_2026_11_07/GL2_limber_k4_audit/gl2.py',
            'closure_2026_11_07/GL2_limber_k4_audit/gl2.json',
            'closure_2026_11_07/GL2_limber_k4_audit/gl2.out',
            'closure_2026_11_06/QX3_cmb_growth/iter2_kq_dust/iter2.py',
            'closure_2026_11_07/QX17D_blend_field_equations/RESULT.md',
            'closure_2026_11_07/QX17D_blend_field_equations/qx17d.py',
            'closure_2026_11_07/CK2_release_speed/RESULT.md',
            'closure_2026_11_07/CK2_release_speed/ck2.py',
            'closure_2026_11_07/CK2_release_speed/ck2.json',
            'action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/form.json']

ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--library-project', type=Path)
    args = ap.parse_args()
    env = os.environ.copy()
    command = ['lake', 'env', 'lean']
    if args.library_project:
        lib = args.library_project.resolve()
        for name in ['lean-toolchain', 'lake-manifest.json']:
            if sha(lib / name) != sha(PROJECT / name):
                raise SystemExit(f'Dependency mismatch: {name}')
        paths = sorted((lib / '.lake/packages').glob('*/.lake/build/lib/lean'))
        if not any((p / 'Mathlib.olean').is_file() for p in paths):
            raise SystemExit('No built Mathlib in library project')
        env['LEAN_PATH'] = os.pathsep.join(map(str, paths))
        command = ['lean']
    before = {p: sha(ROOT / p) for p in EVIDENCE}
    logs = HERE / 'logs'
    logs.mkdir(exist_ok=True)
    rows = []
    for name, namespace in SOURCES.items():
        src = HERE / name
        source_hash = sha(src)
        text = src.read_text()
        expected = {namespace + '.' + n for n in re.findall(r'^theorem\s+(\w+)', text, re.M)}
        r = subprocess.run(command + [str(src)], cwd=PROJECT, env=env,
                           text=True, capture_output=True, timeout=300)
        log = r.stdout + r.stderr
        log = log.replace(str(ROOT) + '/', '')
        log = '\n'.join(line.rstrip() for line in log.splitlines()) + '\n'
        out = logs / (src.stem + '.out')
        out.write_text(log)
        reports = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)
        axioms = {n: [a.strip() for a in aa.split(',') if a.strip()] for n, aa in reports}
        axioms.update({n: [] for n in re.findall(r"'([^']+)' does not depend on any axioms", log)})
        code = re.sub(r'/-.*?-/|--[^\n]*', '', text, flags=re.S)
        passed = (r.returncode == 0 and set(axioms) == expected and bool(expected)
                  and all(set(aa) <= ALLOWED for aa in axioms.values())
                  and not re.search(r'\b(sorry|admit|axiom)\b', code)
                  and sha(src) == source_hash)
        rows.append({'source': str(src.relative_to(ROOT)), 'source_sha256': source_hash,
                     'exit_code': r.returncode, 'theorems': len(expected), 'axioms': axioms,
                     'log': str(out.relative_to(ROOT)), 'log_sha256': sha(out), 'passed': passed})
        print(name, 'PASS' if passed else 'FAIL', len(expected), 'theorems', flush=True)
    after = {p: sha(ROOT / p) for p in EVIDENCE}
    prior = json.loads((ROOT / 'closure_2026_11_07/LEAN_CERTIFICATION/verification.json').read_text())
    prior_unchanged = all(sha(ROOT / row['source']) == row['sha256'] for row in prior['results'])
    memory = json.loads((ROOT / 'closure_2026_11_07/MEMORY_KERNEL_CERTIFICATION/verification.json').read_text())
    prior_unchanged = prior_unchanged and all(sha(ROOT / row['source']) == row['source_sha256'] for row in memory['results'])
    record = {'review': 'self-review; exact kernel algebra, stiffness chain-rule leaves, universal spherical theorem',
              'source_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'lean_version': subprocess.check_output(command + ['--version'], cwd=PROJECT, env=env, text=True).strip(),
              'toolchain': (PROJECT / 'lean-toolchain').read_text().strip(),
              'lake_manifest_sha256': sha(PROJECT / 'lake-manifest.json'),
              'evidence_hashes_before': before, 'evidence_hashes_after': after,
              'prior_certificate_sources_unchanged': prior_unchanged,
              'numerical_lensing_premises': 'GL2 confirmed; GL1 sector reread landed; GL3 web-side premises pending at snapshot; no numerical regrade by this verifier',
              'results': rows, 'new_theorems': sum(row['theorems'] for row in rows),
              'all_passed': all(row['passed'] for row in rows) and before == after and prior_unchanged}
    (HERE / 'verification.json').write_text(json.dumps(record, indent=2) + '\n')
    raise SystemExit(0 if record['all_passed'] else 1)


if __name__ == '__main__':
    main()
