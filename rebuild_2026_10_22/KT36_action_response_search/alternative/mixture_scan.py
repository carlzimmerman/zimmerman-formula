#!/usr/bin/env python3
"""Finite-support positive-action-mixture LP; no baryon or cut changes."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time
import numpy as np

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'rebuild_2026_10_22'
spec = importlib.util.spec_from_file_location('cassini_kt33', BASE / 'KT33_reciprocal_filter/cassini/cassini_v2.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
INPUTS = [BASE / 'KT34_reciprocal_epsilon_scan/mw/low_run/results.json',
          BASE / 'KT34_reciprocal_epsilon_scan/mw/high_run/results.json']


def vertices(q):
    """All vertices of w>=0, sum(w)=1, sum(q*w)<=1 for q>=0."""
    out = [(i, i, 1.) for i, x in enumerate(q) if x <= 1]
    for i, x in enumerate(q):
        if x <= 1:
            continue
        for j, y in enumerate(q):
            if y < 1:
                w = (1 - y) / (x - y)
                assert 0 < w < 1
                assert abs(w*x + (1-w)*y - 1) < 1e-13
                out.append((i, j, w))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    started = time.monotonic()
    data = [json.loads(p.read_text()) for p in INPUTS]
    assert data[0]['cells'] == data[1]['cells']
    cells = data[0]['cells']
    assert len(cells) == 1375
    result = dict(model='N rho + sum_j w_j S_j Phi_ph[S_j rho]',
                  weight_domain='w_j >=0, sum_j w_j=1',
                  assertion_tested='For each of all 1375 stored cells per footing, maximize local vc^2 over every normalized positive mixture supported on the 15 stored widths under the matching Cassini constraint.',
                  outcome='conditional on numerical resolution; finite support only',
                  local_speed_min_km_s=219.9, footings={})
    for foot, a0 in C.A0.items():
        scans = sorted([s for d in data for s in d['footings'][foot]['scans']], key=lambda s:s['epsilon'])
        eps = [s['epsilon'] for s in scans]
        assert len(eps) == len(set(eps)) == 15
        assert all([r['index'] for r in s['rows']] == list(range(1375)) for s in scans)
        assert all([r['cell'] for r in s['rows']] == cells for s in scans)
        cassini = []
        for e in eps:
            q = C.physical(C.quadrupole(C.GEXT/a0, e, e, nr=20000, nm=400, rmin=1e-8, rmax=1e6), a0)
            q['epsilon'] = e
            cassini.append(q)
        assert all(r['Q2_signed_s_minus_2'] < 0 for r in cassini)
        q = np.array([r['x_ceiling'] for r in cassini])
        vc2 = np.array([[r['corrected']['vc']**2 for r in s['rows']] for s in scans])
        verts = vertices(q)
        scores = np.array([w*vc2[i] + (1-w)*vc2[j] for i,j,w in verts])
        best_v = scores.argmax(axis=0)
        best_cell = int(np.max(scores, axis=0).argmax())
        best_vertex = int(best_v[best_cell])
        i,j,w = verts[best_vertex]
        best_speed = float(np.sqrt(scores[best_vertex,best_cell]))
        # A looser relaxation may independently choose a different cell for
        # each component; agreement is a useful invariant, not a premise.
        relaxed = max(w*vc2[i].max()+(1-w)*vc2[j].max() for i,j,w in verts)
        maxima = np.sqrt(np.max(scores, axis=0))
        out = dict(widths=eps, n_cells=1375, n_vertices=len(verts),
                   n_cell_vertex_evaluations=int(scores.size), cassini=cassini,
                   component_max_vc=[float(np.sqrt(x.max())) for x in vc2],
                   component_tail_gate=[s['summary']['numerical_tail_gate_passed'] for s in scans],
                   n_cells_reaching_necessary_speed=int(np.count_nonzero(maxima>=219.9)),
                   maximum_vc=best_speed, deficit_km_s=219.9-best_speed,
                   relaxed_independent_cell_maximum_vc=float(np.sqrt(relaxed)),
                   maximizer=dict(index=best_cell, cell=cells[best_cell],
                                  epsilon_1=eps[i], epsilon_2=eps[j], weight_1=w,
                                  weight_2=1-w, cassini_ratio=float(w*q[i]+(1-w)*q[j]),
                                  component_vc=[float(np.sqrt(vc2[i,best_cell])),float(np.sqrt(vc2[j,best_cell]))]),
                   per_cell_maximum_vc=maxima.tolist())
        result['footings'][foot] = out
        print(foot, 'max_vc', best_speed, 'deficit',219.9-best_speed,'maximizer',out['maximizer'],flush=True)
    result['runtime_seconds'] = time.monotonic()-started
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__ == '__main__':
    main()
