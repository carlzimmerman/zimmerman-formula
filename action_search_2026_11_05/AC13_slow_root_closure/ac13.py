"""AC13: AC3's 8 slow-root witnesses on AC5's rolling clock, windows to N_obs = ln 1101 (graded) and beyond.

Criteria: FROZEN_CRITERIA.md (12b71c9c08). Kappa = 1/2 FITTED; not theory closed. Run from the repo root.
Reuses AC5's build() verbatim (exec of evolve.py up to run_case) and AC5's streaming measurement, with
running maxima snapshotted at checkpoints N in CHECK. One job = (case, run kind, rtol, N_end).
Kinds: gr (pol_on 0), main (AC2q, pol_on (1-2 gs2)^2 at physical gs2), m2 (flipped), plant (main plus
-(2H)^2 K q), stress (pol_on 0.64).
"""
import argparse, json, math, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from scipy.integrate import DOP853
from scipy.optimize import brentq

AC5 = Path('action_search_2026_11_05/AC5_rolling_clock')
OUT = Path('action_search_2026_11_05/AC13_slow_root_closure/parts')
N_OBS = math.log(1101.0)
CHECK = [5.0, N_OBS, 10.0, 15.0, 20.0]
GS2_PHYS = 4.0e-17                       # AC9, larger (alt) footing; canonical 2.4e-17 gives the same double
POL = {'gr': 0.0, 'main': (1 - 2 * GS2_PHYS) ** 2, 'm2': 1.0, 'plant': (1 - 2 * GS2_PHYS) ** 2, 'stress': 0.64}

_src = (AC5 / 'evolve.py').read_text().split('def run_case(')[0]
_saved = sys.argv; sys.argv = ['evolve.py', '--out', '/dev/null']
_ns = {}; exec(compile(_src, 'evolve.py[build]', 'exec'), _ns); sys.argv = _saved
build = _ns['build']
_FN = {}


def fn_for(kind):
    flip = kind == 'm2'
    if flip not in _FN:
        _FN[flip] = build(flip=flip)
    return _FN[flip]


def run(job):
    es, ms, ls, ks, kind, rtol, nend = job
    tag = f"c{es}_{ms}_{ls}_{ks}_{kind}_{rtol:g}_{nend:g}"
    path = OUT / f"{tag}.json"
    if path.exists():
        return json.loads(path.read_text())
    fn = fn_for(kind); on = POL[kind]; plant = kind == 'plant'
    eps, em, Ls, k = float(es), float(ms), float(ls), float(ks)
    lam = math.sqrt(2 * eps); v0 = math.sqrt(2 * em)
    checks = [c for c in CHECK if c <= nend + 1e-12]; aend = math.exp(nend)

    def rhs(t, y):
        a, H, v, ep = y[:4]
        K, Kd, A, S, B = fn(a, H, v, ep, k, Ls, on, lam)
        if plant:
            S = S - 4 * H * H * K
        Hd = -ep * H * H - v * v / 2
        Vb = (3 - ep) * H * H - v * v / 2
        out = [a * H, Hd, -3 * H * v, 2 * ep * (-3 * H + lam * Vb / (math.sqrt(2 * ep) * H) - Hd / H)]
        damp = Kd + A
        for o in (4, 8):
            qq = y[o:o + 2]; qv = y[o + 2:o + 4]
            acc = np.linalg.solve(K, -damp @ qv - S @ qq)
            out += [qv[0], qv[1], acc[0], acc[1]]
        return np.array(out)

    st = dict(n1=0.0, n2=0.0, om0=None, omx=0.0, scale=0.0, cnt=0, detmin=float('inf'), N1e3=None)

    def visit(Y):
        st['n1'] = max(st['n1'], float(np.max(np.abs(Y[4:6])))); st['n2'] = max(st['n2'], float(np.max(np.abs(Y[8:10]))))
        if st['N1e3'] is None:
            big = np.max(np.abs(np.vstack([Y[4:6], Y[8:10]])), axis=0)
            hit = np.nonzero(big >= 1e3)[0]
            if hit.size: st['N1e3'] = float(math.log(Y[0, hit[0]]))
        for i in range(Y.shape[1]):
            if st['cnt'] % 16 == 0:
                st['detmin'] = min(st['detmin'], float(np.linalg.det(fn(*Y[:4, i], k, Ls, on, lam)[0]) / Y[0, i] ** 6))
            if st['cnt'] % 16 == 0 and not plant:   # plant is not symplectic-conserving by design
                a, H, v, ep = Y[:4, i]
                K, Kd, A, S, B = fn(a, H, v, ep, k, Ls, on, lam)
                u, ud, w, wd = Y[4:6, i], Y[6:8, i], Y[8:10, i], Y[10:12, i]
                x1 = u @ (K @ wd + B @ w); x2 = w @ (K @ ud + B @ u); o = x1 - x2
                if st['om0'] is None: st['om0'] = o
                st['omx'] = max(st['omx'], abs(o - st['om0'])); st['scale'] = max(st['scale'], abs(x1), abs(x2))
            st['cnt'] += 1

    def snap(N, yl):
        drift = float(st['omx'] / max(abs(st['om0']), st['scale'], 1e-300)) if st['om0'] is not None else None
        return dict(N=N, max_I=st['n1'], max_II=st['n2'], omega_drift=drift, eps=float(yl[3]), a=float(yl[0]),
                    detK_over_a6_min=st['detmin'], N_first_abs_1e3=st['N1e3'])

    y0 = np.array([1.0, 1.0, v0, eps, 1, 0, 0, 0, 0, 1, 0, 0])
    sv = DOP853(rhs, 0.0, y0, 1e12, rtol=rtol, atol=1e-13)
    t0w = time.time(); snaps = []; ci = 0; steps = 1; ok = True
    while ci < len(checks):
        t0 = sv.t; sv.step(); steps += 1
        if sv.status == 'failed':
            ok = False
            yl = sv.y; fs = snap(math.log(float(yl[0])), yl); fs['failed'] = True
            K = fn(*yl[:4], k, Ls, on, lam)[0]; fs['detK'] = float(np.linalg.det(K)); fs['h'] = float(sv.step_size)
            snaps.append(fs); break
        d = sv.dense_output(); tl = t0
        while ci < len(checks) and sv.y[0] >= math.exp(checks[ci]):
            ac = math.exp(checks[ci])
            te = brentq(lambda tt: d(tt)[0] - ac, tl, sv.t, xtol=1e-14, rtol=1e-15)
            visit(d(np.linspace(tl, te, 8, endpoint=False))); yl = d(te); visit(yl.reshape(-1, 1))
            snaps.append(snap(checks[ci], yl)); tl = te; ci += 1
        if ci < len(checks):
            visit(d(np.linspace(tl, sv.t, 8, endpoint=False)))
    res = dict(job=dict(epsilon_phi=es, epsilon_m=ms, Lstar=ls, k=ks, kind=kind, rtol=rtol, N_end=nend, pol_on=on),
               ok=ok, steps=steps, seconds=time.time() - t0w, snaps=snaps)
    OUT.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(res, indent=1) + '\n')
    print(f"done {tag} ok={ok} steps={steps} {res['seconds']:.0f}s", flush=True)
    return res


def jobs():
    rows = json.loads(Path('action_search_2026_11_05/AC3_matter_gradients/evidence/finite_v3/result.json').read_text())['rows']
    wit = [(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k']) for r in rows if r['negative_roots'] > 0]
    out = []
    for c in wit:
        long_ok = float(c[0]) <= 0.5          # declared deviation (README): eps_phi = 2 long window infeasible
        for rtol in (1e-9, 1e-11):
            for kind in ('gr', 'main', 'm2'):
                out.append(c + (kind, rtol, 20.0 if long_ok else N_OBS))
            for kind in ('plant', 'stress'):
                out.append(c + (kind, rtol, N_OBS))
    # slowest first
    out.sort(key=lambda j: -(float(j[3]) * math.exp(j[6] * max(0.0, float(j[0]) - 1))))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=2); ap.add_argument('--list', action='store_true')
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    J = jobs()
    if a.only:
        J = [j for j in J if a.only in '_'.join(map(str, j))]
    if a.list:
        for j in J: print(j)
        sys.exit()
    with Pool(a.workers) as p:
        for _ in p.imap_unordered(run, J):
            pass
    print('all done', flush=True)
