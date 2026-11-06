"""AC23 runner: AC13's run() imported unchanged, output redirected. Criteria: FROZEN_CRITERIA.md (6b3a77495e).
Kappa = 1/2 FITTED; not theory closed. Run from the repo root."""
import argparse, importlib.util, json, math, sys
from multiprocessing import Pool
from pathlib import Path

D = Path('action_search_2026_11_05/AC23_fresh_slow_roots')
_spec = importlib.util.spec_from_file_location('ac13', 'action_search_2026_11_05/AC13_slow_root_closure/ac13.py')
ac13 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ac13)
ac13.OUT = D / 'parts'
N_OBS = ac13.N_OBS


def jobs():
    W = json.loads((D / 'witnesses.json').read_text())['witnesses']
    out = []
    for w in W:
        c = (w['epsilon_phi'], w['epsilon_m'], w['Lstar'], w['k'])
        for rtol in (1e-9, 1e-11):
            for kind in ('gr', 'main', 'm2'):
                out.append(c + (kind, rtol, 20.0))
            out.append(c + ('plant', rtol, N_OBS))
    return out


def run_ka1(_=None):
    ac13.OUT = D / 'ka1'
    return ac13.run(('.05', '.3', '.001', '10', 'main', 1e-9, N_OBS))


def runj(j):
    ac13.OUT = D / 'parts'
    return ac13.run(j)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); a = ap.parse_args()
    run_ka1()
    J = jobs()
    J.sort(key=lambda j: -float(j[3]))
    with Pool(a.workers) as p:
        for _ in p.imap_unordered(runj, J):
            pass
    print('all done', len(J), flush=True)
