"""EP1 runner: AC13's ac13.py executed from its committed file with three exact, asserted text edits:
(1) output dir -> EP1 parts, (2) POL gains kind 'plantR' (= main's pol_on), (3) kind 'plantR' replaces the stiffness
S by -(2H)^2 K (PW-R); every other kind is AC13's code unchanged (KA1 checks this against AC13's committed parts).
Criteria: CRITERIA.md (d8fc918584). Kappa = 1/2 FITTED; not theory closed. Run from the repo root."""
import argparse, json, math, sys
from multiprocessing import Pool
from pathlib import Path
import numpy as np

D = Path('closure_2026_11_06/EP1_decelerating_slow_roots')
src = Path('action_search_2026_11_05/AC13_slow_root_closure/ac13.py').read_text()
EDITS = [("OUT = Path('action_search_2026_11_05/AC13_slow_root_closure/parts')", "OUT = Path('closure_2026_11_06/EP1_decelerating_slow_roots/parts')"),
         ("'stress': 0.64}", "'stress': 0.64, 'plantR': (1 - 2 * GS2_PHYS) ** 2}"),
         ("plant = kind == 'plant'", "plant = kind in ('plant', 'plantR'); repl = kind == 'plantR'"),
         ("        if plant:\n            S = S - 4 * H * H * K", "        if repl:\n            S = -4 * H * H * K\n        elif plant:\n            S = S - 4 * H * H * K")]
for a, b in EDITS:
    assert src.count(a) == 1, a
    src = src.replace(a, b)
src = src.split("\nif __name__ == '__main__':")[0]
ac13 = {'__name__': 'ep1_ac13'}; exec(compile(src, 'ac13.py[EP1 edits]', 'exec'), ac13)
N_OBS = ac13['N_OBS']


def setout(sub):
    ac13['OUT'] = D / sub


def runj(j):
    sub, job = j
    setout(sub)
    return ac13['run'](job)


def diag(c):
    """Reported only: min eigenvalue of K^-1 S / H^2 along main's background at N = 0..7 (background only)."""
    from scipy.integrate import solve_ivp
    es, ms, ls, ks = c; eps, em, Ls, k = map(float, c); lam = math.sqrt(2 * eps); on = ac13['POL']['main']
    fn = ac13['fn_for']('main')

    def bg(t, y):
        a, H, v, ep = y
        Hd = -ep * H * H - v * v / 2; Vb = (3 - ep) * H * H - v * v / 2
        return [a * H, Hd, -3 * H * v, 2 * ep * (-3 * H + lam * Vb / (math.sqrt(2 * ep) * H) - Hd / H)]
    out = []
    for N in range(0, 8):
        if N == 0:
            y = [1.0, 1.0, math.sqrt(2 * em), eps]
        else:
            ev = lambda t, y: y[0] - math.exp(N); ev.terminal = True
            s = solve_ivp(bg, (0, 1e14), [1.0, 1.0, math.sqrt(2 * em), eps], method='DOP853', rtol=1e-12, atol=1e-300, events=ev)
            y = s.y_events[0][0]
        K, Kd, A, S, B = fn(*y, k, Ls, on, lam)
        ev_ = np.linalg.eigvals(np.linalg.solve(K, S))
        out.append(dict(N=N, H=float(y[1]), eps_phi=float(y[3]), k_over_aH=float(k / (y[0] * y[1])),
                        min_eig_KinvS_over_H2=float(np.min(ev_.real) / y[1] ** 2), max_eig_KinvS_over_H2=float(np.max(ev_.real) / y[1] ** 2)))
    return dict(case=list(c), rows=out)


def jobs():
    W = json.loads((D / 'witnesses.json').read_text())
    cases = [(w['epsilon_phi'], w['epsilon_m'], w['Lstar'], w['k']) for w in W['witnesses']]
    if W['add_AC13_fixtures']:
        cases += [('2', '.9', '.001', '10'), ('2', '.9', '.001', '100')]
    J = []
    for c in cases:
        for rtol in (1e-9, 1e-11):
            for kind in ('gr', 'main', 'm2', 'plantR'):
                J.append(('parts', c + (kind, rtol, N_OBS)))
        J.append(('parts', c + ('plant', 1e-11, N_OBS)))
    for c in [('2', '.9', '.001', '10'), ('2', '.9', '.001', '100')]:          # KA1
        for kind in ('main', 'gr', 'plant', 'm2'):
            J.append(('ka1', c + (kind, 1e-9, N_OBS)))
    J.append(('ka2', ('0.25', '0.6', '0.0003', '3', 'main', 1e-9, N_OBS)))     # KA2b
    for c in [('2', '.9', '.001', '10'), ('2', '.9', '.001', '100')]:          # PW-R on AC13's fixtures (reported)
        for rtol in (1e-9, 1e-11):
            J.append(('ac13fix', c + ('plantR', rtol, N_OBS)))
    J.sort(key=lambda j: -float(j[1][3]))
    return cases, J


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    cases, J = jobs()
    if a.list:
        for j in J: print(j)
        sys.exit()
    dg = [diag(c) for c in cases + [('2', '.9', '.001', '10'), ('2', '.9', '.001', '100')]]
    (D / 'diag_KinvS.json').write_text(json.dumps(dict(rows=dg, note='reported only; kappa = 1/2 FITTED; not theory closed'), indent=1) + '\n')
    print('diag done', flush=True)
    with Pool(a.workers) as p:
        for _ in p.imap_unordered(runj, J):
            pass
    print('all done', len(J), flush=True)
