#!/usr/bin/env python3
"""Reproduction check R (FROZEN_CRITERIA.md section 1) + provenance.
Compares repro/spatial_expansion_2026_10_23/<run>/result.json (made by repro/run_repro.sh from byte copies of SE's code)
with the recorded files in sol61_push/spatial_expansion_2026_10_23/ (read only). Writes PROVENANCE.json and
REPRO_RESULT.json (or REPRO_RESULT_MUTATE.json with --mutate, which perturbs one recorded leaf in memory by 1e-6
relative and must be caught)."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / 'sol61_push' / 'spatial_expansion_2026_10_23'
PARENT = ROOT / 'sol61_push' / 'fragment_radiation_2026_10_22' / 'model.py'
COPY = HERE / 'repro' / 'spatial_expansion_2026_10_23'
RUNS = ['base', 'space', 'time', 'strong', 'strong_space', 'strong_fine', 'strong_time', 'early', 'earlier', 'check', 'force', 'summary']
CODE = ['model.py', 'run_v2.py', 'check.py', 'force_check.py', 'summarize.py', 'CONTRACT.md']
READ_ONLY = ['HANDOFF.md', 'DERIVATION.md', 'RESULT.md', 'AUDIT.md', 'CONTRACT.md', 'SOURCES.md', 'CHECKPOINT.sha256', 'run.py', 'plot.py']


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(x, path=''):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, f'{path}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, f'{path}[{i}]')
    else:
        yield path, x


def numeric_equal(a, b):
    la, lb = dict(leaves(a)), dict(leaves(b))
    if la.keys() != lb.keys(): return False, 'key sets differ'
    worst = 0.
    scale = max((abs(v) for v in la.values() if isinstance(v, float)), default=1.)
    for k in la:
        u, v = la[k], lb[k]
        if isinstance(u, bool) or isinstance(u, int) or isinstance(u, str) or u is None:
            if u != v: return False, f'{k}: {u!r} != {v!r}'
        else:
            d = abs(u - v); r = d / max(abs(u), abs(v), 1e-15 * scale) if d else 0.
            worst = max(worst, r)
            if r > 1e-9: return False, f'{k}: rel {r:.3e}'
    return True, f'max rel {worst:.3e}'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--mutate', action='store_true'); a = ap.parse_args()
    prov = dict(note='sha256 of every SE-20261023 file read or copied; copies must equal sources. sol61_push is never written.',
                code=[], parent=dict(source=str(PARENT.relative_to(ROOT)), sha256_source=sha(PARENT),
                                     copy=str((HERE / 'repro/fragment_radiation_2026_10_22/model.py').relative_to(ROOT)),
                                     sha256_copy=sha(HERE / 'repro/fragment_radiation_2026_10_22/model.py')),
                read_only=[dict(path=str((SRC / f).relative_to(ROOT)), sha256=sha(SRC / f)) for f in READ_ONLY],
                recorded_results=[])
    prov['parent']['equal'] = prov['parent']['sha256_source'] == prov['parent']['sha256_copy']
    for f in CODE:
        prov['code'].append(dict(source=str((SRC / f).relative_to(ROOT)), sha256_source=sha(SRC / f), sha256_copy=sha(COPY / f), equal=sha(SRC / f) == sha(COPY / f)))
    out = dict(criteria='FROZEN_CRITERIA.md section 1', runs=[])
    for r in RUNS:
        rec, rep = SRC / r / 'result.json', COPY / r / 'result.json'
        prov['recorded_results'].append(dict(path=str(rec.relative_to(ROOT)), sha256=sha(rec)))
        A, B = rec.read_bytes(), rep.read_bytes()
        ja, jb = json.loads(A), json.loads(B)
        if a.mutate:
            ja = json.loads(A)
            if 'rows' in ja and 'contrast_c_max' in ja['rows'][-1]: ja['rows'][-1]['contrast_c_max'] *= 1 + 1e-6
            elif 'checks' in ja: ja['checks'][0]['value'] *= 1 + 1e-6
            else: ja['max_work_error'] *= 1 + 1e-6
            A = json.dumps(ja, indent=2).encode()
        byte = A == B
        ok, why = numeric_equal(ja, jb)
        row = dict(run=r, sha256_recorded=hashlib.sha256(A).hexdigest(), sha256_reproduced=sha(rep), byte_identical=byte, numeric_ok=ok, detail=why)
        if 'rows' in jb and 'z' in jb['rows'][-1]:
            f = jb['rows'][-1]; row.update(steps=jb['steps'], z_final=f['z'], peak_c=f['contrast_c_max'], rms_c=f['rms_c'], max_work_error=jb['max_work_error'])
        out['runs'].append(row)
    byte_all = all(x['byte_identical'] for x in out['runs']); num_all = all(x['numeric_ok'] for x in out['runs'])
    out['verdict'] = 'R-PASS' if byte_all else ('R-PASS (numeric)' if num_all else 'R-FAIL')
    out['provenance_copies_equal'] = all(c['equal'] for c in prov['code']) and prov['parent']['equal']
    if a.mutate:
        out['mutate_detected'] = out['verdict'] != 'R-PASS'
        (HERE / 'REPRO_RESULT_MUTATE.json').write_text(json.dumps(out, indent=1) + '\n')
    else:
        (HERE / 'REPRO_RESULT.json').write_text(json.dumps(out, indent=1) + '\n')
        (HERE / 'PROVENANCE.json').write_text(json.dumps(prov, indent=1) + '\n')
    print(out['verdict'], 'copies equal:', out['provenance_copies_equal'], ('mutate detected: %s' % out.get('mutate_detected')) if a.mutate else '')


if __name__ == '__main__':
    main()
