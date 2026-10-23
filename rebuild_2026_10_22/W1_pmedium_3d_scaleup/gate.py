#!/usr/bin/env python3
"""Port gate G-P1 (and MUTATE G-P2 with --mutate): engine vs SE-20261023 evolve, same interpreter and process.
FROZEN_CRITERIA.md section 2.1/2.2. Writes gate_results.json (or gate_results_MUTATE.json).
Run: OMP_NUM_THREADS=1 nice -n 15 /usr/bin/python3 gate.py [--mutate]"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'engine')); sys.path.insert(0, str(HERE / 'repro' / 'spatial_expansion_2026_10_23'))
import pmedium3d as ENG  # noqa: E402
import model as SE  # noqa: E402

TOL = 1e-9
REL_KEYS = ('z', 'contrast_c_max', 'contrast_b_max', 'rms_c', 'Pmax', 'chi_min', 'chi_max', 'cell_kpc', 'core_radius_cells')
INT_KEYS = ('step', 'max_members', 'groups_ge32')


def rel(a, b):
    a, b = float(a), float(b)
    return 0. if a == b else abs(a - b) / max(abs(a), abs(b))


def compare(ref, eng, n):
    m = ENG.Model(n, ref['parameters']['amp'])
    out = {}
    out['a_steps_reason'] = dict(passed=ref['steps'] == eng['steps'] and ref['reason'] == eng['reason'],
                                 ref=[ref['steps'], ref['reason']], eng=[eng['steps'], eng['reason']])
    xr = np.array(ref['final_x_c']); xe = eng['_final']['xc']; pr = np.array(ref['final_pc']); pe = eng['_final']['pc']
    dxm = float(np.max(np.abs(xr - xe)) / m.dx); dpm = float(np.max(np.abs(pr - pe)) / np.max(np.abs(pr)))
    out['b_final_state'] = dict(passed=dxm <= TOL and dpm <= TOL, max_dx_over_cell=dxm, max_dpi_rel=dpm,
                                bit_identical=bool(np.array_equal(xr, xe) and np.array_equal(pr, pe)))
    worst = {}; ok = len(ref['rows']) == len(eng['rows']); bit = ok
    for r1, r2 in zip(ref['rows'], eng['rows']):
        for k in INT_KEYS:
            if r1[k] != r2[k]: ok = False; worst[k] = 'mismatch'
        for k in REL_KEYS:
            v = rel(r1[k], r2[k]); worst[k] = max(worst.get(k, 0.), v); ok &= v <= TOL
        v = abs(r1['energy'] - r2['energy']) / r1['energy_scale']; worst['energy'] = max(worst.get('energy', 0.), v); ok &= v <= TOL
        v = abs(r1['work_error'] - r2['work_error']); worst['work_error'] = max(worst.get('work_error', 0.), v); ok &= v <= TOL
        bit &= all(r1[k] == r2[k] for k in r1)
    out['c_rows'] = dict(passed=bool(ok), n_rows=[len(ref['rows']), len(eng['rows'])], worst=worst, bit_identical=bool(bit))
    v1 = abs(ref['max_work_error'] - eng['max_work_error']); v2 = max(rel(a, b) for a, b in zip(ref['initial_residuals'], eng['initial_residuals']))
    out['d_work_residuals'] = dict(passed=v1 <= TOL and v2 <= TOL, d_max_work_error=v1, initial_residual_rel=v2)
    out['passed'] = all(v['passed'] for v in out.values() if isinstance(v, dict))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--mutate', action='store_true'); a = ap.parse_args()
    mut = 'drop_h_cold' if a.mutate else None
    configs = [(8, .001), (8, .03)] if a.mutate else [(8, .001), (12, .001), (16, .001), (8, .03), (12, .03), (16, .03)]
    import hashlib
    res = dict(criteria='FROZEN_CRITERIA.md 2.1' + (' / 2.2 MUTATE drop_h_cold' if mut else ''), tolerance=TOL,
               engine_sha256=hashlib.sha256((HERE / 'engine' / 'pmedium3d.py').read_bytes()).hexdigest(),
               kernel_sha256=hashlib.sha256((HERE / 'engine' / 'tsc_kernels.c').read_bytes()).hexdigest(),
               se_model_sha256=hashlib.sha256((HERE / 'repro' / 'spatial_expansion_2026_10_23' / 'model.py').read_bytes()).hexdigest(), runs=[])
    for n, amp in configs:
        t0 = time.time(); ref = SE.evolve(n, amp, 1100, 10, .6); tse = time.time() - t0
        for th in ([1, 4] if (amp == .03 and not mut) else [1]):
            t0 = time.time(); eng = ENG.evolve(n, amp, 1100, 10, .6, 'canonical', th, mut, None, cert=False, log=lambda s: None); ten = time.time() - t0
            c = compare(ref, eng, n); c.update(n=n, amp=amp, threads=th, seconds_SE=tse, seconds_engine=ten,
                                               peak_SE=ref['rows'][-1]['contrast_c_max'], peak_engine=eng['rows'][-1]['contrast_c_max'])
            res['runs'].append(c)
            print(f"n={n} amp={amp} threads={th}: passed={c['passed']} bit={c['b_final_state']['bit_identical'] and c['c_rows']['bit_identical']} "
                  f"dx/cell={c['b_final_state']['max_dx_over_cell']:.3e} peak SE {c['peak_SE']:.6f} eng {c['peak_engine']:.6f} t {tse:.1f}/{ten:.1f}s", flush=True)
    allpass = all(r['passed'] for r in res['runs'])
    if mut:
        res['G_P2_MUTATE_breaks_gate'] = not allpass
        res['verdict'] = 'G-P2 PASS (mutated engine fails the gate)' if not allpass else 'G-P2 FAIL: gate void (mutation not detected)'
    else:
        res['G_P1'] = allpass
        res['all_bit_identical'] = all(r['b_final_state']['bit_identical'] and r['c_rows']['bit_identical'] for r in res['runs'])
        res['verdict'] = 'G-P1 PASS' if allpass else 'G-P1 FAIL'
    print(res['verdict'])
    out = HERE / ('gate_results_MUTATE.json' if mut else 'gate_results.json')
    ENG.atomic_write_bytes(out, ENG.jdump(res))


if __name__ == '__main__':
    main()
