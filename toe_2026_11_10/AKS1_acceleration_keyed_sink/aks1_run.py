#!/usr/bin/env python3
"""AKS1 rows (FROZEN_CRITERIA.md s. 3): writes runs/<name>.json (grading summaries). Resumable: a row whose JSON exists is
skipped, so a SIGTERM loses at most the rows in flight. Snapshots go to $AKS1_SNAP (outside the repo) if set.

    nice python3 aks1_run.py [--workers 5] [--only NAME,NAME]
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, math, os, sys, time
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import aks1_lib as L

RD = os.path.join(HERE, 'runs')
SNAP = os.environ.get('AKS1_SNAP', '')
MASSES = (9.0, 10.5, 11.5)


def specs():
    S = []
    both = ('canonical', 'alt')
    for f in both:
        for lM in MASSES:
            S.append((f'P_{f}_{lM:g}', dict(footing=f, lM=lM, key='A')))
            S.append((f'MU1_{f}_{lM:g}', dict(footing=f, lM=lM, key='off')))
            S.append((f'Pc_{f}_{lM:g}', dict(footing=f, lM=lM, key='A', cfac=2.0)))
            S.append((f'MU2_{f}_{lM:g}', dict(footing=f, lM=lM, key='rho')))
            S.append((f'B1_{f}_{lM:g}', dict(footing=f, lM=lM, key='gpec')))
    S.append(('P_canonical_10.5_N1000', dict(footing='canonical', lM=10.5, key='A', N=1000)))
    S.append(('HOM_canonical', dict(footing='canonical', hom=True)))
    S.append(('HOM_alt', dict(footing='alt', hom=True)))
    for lM in MASSES:
        for C in (10.0, 100.0, 1000.0):
            S.append((f'B2_C{int(C)}_canonical_{lM:g}', dict(footing='canonical', lM=lM, key='gpec', C=C)))
        S.append((f'B3_canonical_{lM:g}', dict(footing='canonical', lM=lM, key='A', mu_Mpc=L.MU_W['canonical'])))
        S.append((f'B4_canonical_{lM:g}', dict(footing='canonical', lM=lM, key='gpec', fshape='x2')))
    return S


def do(spec):
    name, kw = spec
    path = os.path.join(RD, name + '.json')
    if os.path.exists(path):
        return name, 'skip', 0.0
    T = time.time()
    kw = dict(kw)
    if kw.pop('hom', False):
        f = kw['footing']
        oP = L.run(f, 10.5, key='A', homogeneous=True)
        oM = L.run(f, 10.5, key='off', homogeneous=True)
        a = oM['a_end']
        out = {'name': name, 'footing': f, 'max_rel_P_vs_MU1': float(np.max(np.abs(oP['_r'] / oM['_r'] - 1))),
               'max_rel_MU1_vs_FRW': float(np.max(np.abs(oM['_r'] / (a * oM['_X']) - 1))),
               'NG_max_P': float(oP['_NG'].max()), 'Ediss_P': float(oP['_Ediss'].sum()),
               'steps': [oP['steps'], oM['steps']], 'wall_s': time.time() - T,
               'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
    else:
        f, lM = kw.pop('footing'), kw.pop('lM')
        sp = os.path.join(SNAP, name + '.npz') if SNAP else None
        o = L.run(f, lM, snap_path=sp, **kw)
        S = L.summarize(o, f, lM)
        meta = {k: v for k, v in o.items() if not k.startswith('_')}
        out = {'name': name, **meta, 'summary': S}
    tmp = path + '.tmp'
    json.dump(out, open(tmp, 'w'), indent=0, default=float)
    os.replace(tmp, path)
    return name, 'done', time.time() - T


def init():
    try:
        os.nice(10)
    except OSError:
        pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=5); ap.add_argument('--only', default='')
    a = ap.parse_args()
    os.makedirs(RD, exist_ok=True)
    if SNAP:
        os.makedirs(SNAP, exist_ok=True)
    S = specs()
    if a.only:
        keep = set(a.only.split(',')); S = [s for s in S if s[0] in keep]
    with mp.Pool(a.workers, initializer=init) as pool:
        for name, st, w in pool.imap_unordered(do, S):
            print(f'{name}: {st} {w:.0f}s', flush=True)
