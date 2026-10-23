"""Aggregate V3: TW error vs occupation (FROZEN_CRITERIA V3 + A1). Errors are max over t in [0, 500] of |TW - exact|."""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent


def errors(d):
    ex, tw, n = d['exact'], d['tw'], d['n']
    N_e = np.array(ex['N']); N_t = np.array(tw['N'])
    O1 = abs((N_t[:, 2]+N_t[:, 3])-(N_e[:, 2]+N_e[:, 3]))/n
    O2 = abs((N_t[:, 0]+N_t[:, 1])-(N_e[:, 0]+N_e[:, 1]))/n
    O3 = abs(np.array(tw['coh'])-np.array(ex['coh']))
    O4 = np.maximum(abs(np.array(tw['varX'])-np.array(ex['varX'])), abs(np.array(tw['varPhi'])-np.array(ex['varPhi'])))/n
    O5 = abs(np.array(tw['exkurt'])-np.array(ex['exkurt'])); O6 = abs(np.array(tw['skew'])-np.array(ex['skew']))
    sem = float(np.max(d['tw_sem_Ndriven']))/n
    return dict(O1=float(O1.max()), O2=float(O2.max()), O3=float(O3.max()), O4=float(O4.max()), O5=float(np.nanmax(O5)),
                O6=float(np.nanmax(O6)), sem_N=sem, dim=d['dim'], edge=float(max(ex['edge_prob'])),
                norm_drift=float(np.ptp(ex['norm'])), energy_drift=float(np.ptp(ex['energy'])/max(abs(ex['energy'][0]), 1e-300)))


def table(mode='rwa'):
    rows = []
    for sc in ('A', 'B'):
        for nu in (2, 8):
            for n in (1, 2, 4, 8, 16, 32):
                f = HERE/'validation'/f'v3_{sc}_nu{nu}_n{n}_{mode}.json'
                if not f.exists(): rows.append(dict(sc=sc, nu=nu, n=n, missing=True)); continue
                d = json.loads(f.read_text())
                if d.get('skipped'): rows.append(dict(sc=sc, nu=nu, n=n, skipped=True, dim=d['dim'])); continue
                rows.append(dict(sc=sc, nu=nu, n=n, **errors(d)))
    return rows


def nstar(rows, a=.05, b=.10):
    ok = {}
    for n in (1, 2, 4, 8, 16, 32):
        rs = [r for r in rows if r['n'] == n and 'O1' in r]
        if len(rs) < 4: ok[n] = None; continue
        ok[n] = all(max(r['O1'], r['O2'], r['O3'], r['O4']) < a and max(r['O5'], r['O6']) < b for r in rs)
    for n in (1, 2, 4, 8, 16, 32):
        if ok[n] and all(ok[k] for k in (1, 2, 4, 8, 16, 32) if k > n and ok[k] is not None):
            return n, ok
    return None, ok


if __name__ == '__main__':
    for mode in ('rwa', 'full'):
        rows = table(mode); print('mode', mode)
        for r in rows:
            if 'O1' in r:
                print(f"  {r['sc']} nu{r['nu']} n{r['n']:3d} O1 {r['O1']:.4f} O2 {r['O2']:.4f} O3 {r['O3']:.4f} O4 {r['O4']:.4f} "
                      f"O5 {r['O5']:.3f} O6 {r['O6']:.3f} sem {r['sem_N']:.4f} dim {r['dim']} edge {r['edge']:.1e}")
            else:
                print('  ', r)
        print('  n* (5%/10%)', nstar(rows), ' n*_10 (10%/20%)', nstar(rows, .10, .20))
