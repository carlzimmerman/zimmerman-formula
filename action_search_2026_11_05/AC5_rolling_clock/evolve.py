"""AC5: AC4's integrator on a rolling-clock exponential-potential background (lambda = sqrt(2 eps0)).

Criteria: FROZEN_CRITERIA.md (commit 63b0c9ca2c). Kappa = 1/2 FITTED; not theory closed.
Modes: main (candidate + GR control), m1 (drop Kdot), m2 (source's flipped stiffness sign).
Run from the repository root.
"""
import argparse, itertools, json, math, sys, time
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True)
ap.add_argument('--mode', choices=['main', 'm1', 'm2'], default='main')
ap.add_argument('--only-witnesses', action='store_true')
ap.add_argument('--lam0', action='store_true', help='known answer: lambda = 0 (AC4 flow)')
ap.add_argument('--cases', default='')
ap.add_argument('--stream', action='store_true')
args = ap.parse_args()

SOURCE = Path('action_scale_investigation_2026_11_05/single_clock.py')
AC3 = Path('action_search_2026_11_05/AC3_matter_gradients/evidence/finite_v3/result.json')


def build(flip):
    """Exec the pinned source up to its fixture run; same substitutions as AC3 finite_v3."""
    saved = sys.argv
    sys.argv = ['single_clock.py', '--out', '/dev/null'] + (['--mutate'] if flip else [])
    ns = {}
    try:
        exec(compile(SOURCE.read_text().split('# Independent constraint Hessian')[0], str(SOURCE), 'exec'), ns)
    finally:
        sys.argv = saved
    a, H, k, ep, cY, m2, v, F1, Rm = [ns[x] for x in ('a', 'H', 'k', 'ep', 'cY', 'm2', 'v', 'F1', 'Rm')]
    Z, Zd, C, Cd = [ns[x] for x in ('Z', 'Zd', 'C', 'Cd')]
    Ls = s.Symbol('Lstar', positive=True)
    on = s.Symbol('pol_on', real=True)
    lam = s.Symbol('lam', real=True)  # 1 = candidate, 0 = GR control (cY = 0)
    cy = on / (1 + Ls ** 2 * k * k / (2 * a * a))
    L = s.expand(ns['Lred'].subs({F1: 1, Rm: 1, ns['F0']: v * v / 2, m2: 1}).subs(cY, cy))
    q = s.Matrix([Z, C]); qd = s.Matrix([Zd, Cd])
    K = s.hessian(L, qd)
    B = s.Matrix(2, 2, lambda i, j: s.diff(L, qd[i], q[j]))
    P = s.hessian(L, q)
    for M in (K, B, P):  # quadratic: no residual q dependence
        assert not any(x.has(Z, Zd, C, Cd) for x in M)
    Hd = -ep * H ** 2 - v ** 2 / 2
    Vb = (3 - ep) * H ** 2 - v ** 2 / 2
    flow = {a: a * H, H: Hd, v: -3 * H * v, ep: 2 * ep * (-3 * H + lam * Vb / (s.sqrt(2 * ep) * H) - Hd / H)}
    dt = lambda x: sum(s.diff(x, y) * dy for y, dy in flow.items())
    # Same equation; the large k^2 a cancellations in Bdot - P are done exactly,
    # since the GR control's K11 -> 0 otherwise turns rounding into noise.
    Kd = K.applyfunc(lambda x: s.simplify(dt(x)))
    S = (B.applyfunc(dt) - P).applyfunc(s.simplify)
    A = (B - B.T).applyfunc(s.simplify)
    f = s.lambdify((a, H, v, ep, k, Ls, on, lam), (K, Kd, A, S, B), 'numpy', cse=True)
    return lambda *x: [np.array(M, dtype=float) for M in f(*x)]


def run_case(fn, eps, em, Ls, k, on, rtol, drop_kdot, lam):
    v0 = math.sqrt(2 * em)
    aend = math.exp(5.0)

    def rhs(t, y):
        a, H, v, ep = y[:4]
        K, Kd, A, S, B = fn(a, H, v, ep, k, Ls, on, lam)
        Hd = -ep * H * H - v * v / 2
        Vb = (3 - ep) * H * H - v * v / 2
        out = [a * H, Hd, -3 * H * v, 2 * ep * (-3 * H + lam * Vb / (math.sqrt(2 * ep) * H) - Hd / H)]
        damp = (0 * Kd if drop_kdot else Kd) + A
        stiff = S
        for o in (4, 8):
            qq = y[o:o + 2]; qv = y[o + 2:o + 4]
            acc = np.linalg.solve(K, -damp @ qv - stiff @ qq)
            out += [qv[0], qv[1], acc[0], acc[1]]
        return out

    ev = lambda t, y: y[0] - aend
    ev.terminal = True; ev.direction = 1
    y0 = [1.0, 1.0, v0, eps, 1, 0, 0, 0, 0, 1, 0, 0]
    sol = solve_ivp(rhs, (0, 1e9), y0, method='DOP853', rtol=rtol, atol=1e-13, events=ev, dense_output=True)
    # max_t from dense output, 8 points per accepted step, so it does not depend on step placement.
    ts = sol.t
    grid = np.concatenate([np.linspace(ts[i], ts[i + 1], 8, endpoint=False) for i in range(len(ts) - 1)] + [ts[-1:]])
    Y = sol.sol(grid)
    n1 = np.max(np.abs(Y[4:6]), axis=0).max(); n2 = np.max(np.abs(Y[8:10]), axis=0).max()
    idx = np.unique(np.linspace(0, Y.shape[1] - 1, min(Y.shape[1], 4000)).astype(int))
    om = []; scale = 0.0
    for i in idx:
        a, H, v, ep = Y[:4, i]
        K, Kd, A, S, B = fn(a, H, v, ep, k, Ls, on, lam)
        u, ud, w, wd = Y[4:6, i], Y[6:8, i], Y[8:10, i], Y[10:12, i]
        x1 = u @ (K @ wd + B @ w); x2 = w @ (K @ ud + B @ u)
        om.append(x1 - x2); scale = max(scale, abs(x1), abs(x2))
    om = np.array(om)
    drift = float(np.max(np.abs(om - om[0])) / max(abs(om[0]), scale, 1e-300))
    return dict(ok=bool(sol.success and sol.status == 1), steps=int(len(ts)),
                a_end=float(Y[0, -1]), eps_end=float(Y[3, -1]), max_I=float(n1), max_II=float(n2), omega_drift=drift)


def run_case_stream(fn, eps, em, Ls, k, on, rtol, drop_kdot, lam):
    """Same measurement as run_case without storing the solution: DOP853 stepped by hand, the same 8 dense-output
    points per accepted step, the same terminal event a = e^5 (brentq on the step's interpolant). Omega is sampled
    every 16th grid point instead of 4000 evenly spaced points. Numerics only; no line changed."""
    from scipy.integrate import DOP853
    from scipy.optimize import brentq
    v0 = math.sqrt(2 * em); aend = math.exp(5.0)

    def rhs(t, y):
        a, H, v, ep = y[:4]
        K, Kd, A, S, B = fn(a, H, v, ep, k, Ls, on, lam)
        Hd = -ep * H * H - v * v / 2
        Vb = (3 - ep) * H * H - v * v / 2
        out = [a * H, Hd, -3 * H * v, 2 * ep * (-3 * H + lam * Vb / (math.sqrt(2 * ep) * H) - Hd / H)]
        damp = (0 * Kd if drop_kdot else Kd) + A
        for o in (4, 8):
            qq = y[o:o + 2]; qv = y[o + 2:o + 4]
            acc = np.linalg.solve(K, -damp @ qv - S @ qq)
            out += [qv[0], qv[1], acc[0], acc[1]]
        return np.array(out)

    y0 = np.array([1.0, 1.0, v0, eps, 1, 0, 0, 0, 0, 1, 0, 0])
    sv = DOP853(rhs, 0.0, y0, 1e9, rtol=rtol, atol=1e-13)
    n1 = n2 = 0.0; om0 = None; omx = 0.0; scale = 0.0; cnt = 0; steps = 1; done = False; yl = y0

    def visit(Y):
        nonlocal n1, n2, om0, omx, scale, cnt
        n1 = max(n1, float(np.max(np.abs(Y[4:6])))); n2 = max(n2, float(np.max(np.abs(Y[8:10]))))
        for i in range(Y.shape[1]):
            if cnt % 16 == 0:
                a, H, v, ep = Y[:4, i]
                K, Kd, A, S, B = fn(a, H, v, ep, k, Ls, on, lam)
                u, ud, w, wd = Y[4:6, i], Y[6:8, i], Y[8:10, i], Y[10:12, i]
                x1 = u @ (K @ wd + B @ w); x2 = w @ (K @ ud + B @ u); o = x1 - x2
                if om0 is None: om0 = o
                omx = max(omx, abs(o - om0)); scale = max(scale, abs(x1), abs(x2))
            cnt += 1

    while not done:
        t0 = sv.t
        msg = sv.step()
        if sv.status == 'failed':
            return dict(ok=False, steps=steps, a_end=float(sv.y[0]), eps_end=float(sv.y[3]), max_I=n1, max_II=n2, omega_drift=float('nan'))
        steps += 1
        d = sv.dense_output()
        if sv.y[0] >= aend:
            te = brentq(lambda tt: d(tt)[0] - aend, t0, sv.t, xtol=1e-14, rtol=1e-15)
            visit(d(np.linspace(t0, te, 8, endpoint=False)))
            yl = d(te); visit(yl.reshape(-1, 1)); done = True
        else:
            visit(d(np.linspace(t0, sv.t, 8, endpoint=False)))
    drift = float(omx / max(abs(om0), scale, 1e-300))
    return dict(ok=True, steps=steps, a_end=float(yl[0]), eps_end=float(yl[3]), max_I=n1, max_II=n2, omega_drift=drift)


rows = json.loads(AC3.read_text())['rows']
cases = [(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k'], r['negative_roots'] > 0) for r in rows]
if args.only_witnesses or args.mode != 'main':
    cases = [c for c in cases if c[4]]
if args.cases:
    want = [tuple(x.split(',')) for x in args.cases.split(';')]
    cases = [c for c in cases if c[:4] in want]
fn = build(flip=(args.mode == 'm2'))
res = []
t0 = time.time()
for es, ms, ls, ks, wit in cases:
    row = dict(epsilon_phi=es, epsilon_m=ms, Lstar=ls, k=ks, witness=wit)
    lam = 0.0 if args.lam0 else math.sqrt(2 * float(es)); row['lambda'] = lam
    for rtol in (1e-9, 1e-11):
        rc = run_case_stream if args.stream else run_case
        cand = rc(fn, float(es), float(ms), float(ls), float(ks), 1.0, rtol, args.mode == 'm1', lam)
        gr = rc(fn, float(es), float(ms), float(ls), float(ks), 0.0, rtol, args.mode == 'm1', lam)
        R = max(cand['max_I'] / gr['max_I'], cand['max_II'] / gr['max_II'])
        row[f'rtol_{rtol:g}'] = dict(candidate=cand, gr=gr, R=R)
    r9, r11 = row['rtol_1e-09']['R'], row['rtol_1e-11']['R']
    row['R'] = r11
    row['converged'] = abs(r9 - r11) / abs(r11) <= 1e-3
    row['all_integrations_ok'] = all(row[f'rtol_{t:g}'][x]['ok'] for t in (1e-9, 1e-11) for x in ('candidate', 'gr'))
    row['omega_drift_max'] = max(row[f'rtol_{t:g}'][x]['omega_drift'] for t in (1e-9, 1e-11) for x in ('candidate', 'gr'))
    res.append(row)
    print(f"{es:>4} {ms:>4} {ls:>6} {ks:>6} wit={int(wit)} R={r11:.6g} conv={row['converged']} "
          f"drift={row['omega_drift_max']:.2e} t={time.time()-t0:.0f}s", flush=True)

Rs = [r['R'] for r in res]
summary = dict(
    mode=args.mode, n_cases=len(res), max_R=max(Rs),
    witness_max_R=max((r['R'] for r in res if r['witness']), default=None),
    all_converged=all(r['converged'] for r in res),
    all_integrations_ok=all(r['all_integrations_ok'] for r in res),
    omega_drift_max=max(r['omega_drift_max'] for r in res),
    omega_line_met=all(r['omega_drift_max'] <= 1e-6 for r in res),
)
if args.mode == 'main':
    if not (summary['all_converged'] and summary['all_integrations_ok'] and summary['omega_line_met']):
        label = 'NO VERDICT'
    elif summary['max_R'] >= 1e3:
        label = 'FAIL'
    elif summary['max_R'] <= 10:
        label = 'PASS'
    else:
        label = 'UNDECIDED'
    summary['label_before_power_gate'] = label
summary['note'] = 'kappa = 1/2 FITTED; not theory closed'
out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(dict(summary=summary, rows=res), indent=1) + '\n')
print(json.dumps(summary, indent=1))
