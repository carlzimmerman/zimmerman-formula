"""AC23 witness scan: AC3 finite_v3's frozen-root algebra (same source exec, a = H = 1, m2 = 1), applied to
AC3's grid (KA2) and to AC23's fresh grids A/B. Criteria: FROZEN_CRITERIA.md (6b3a77495e).
Kappa = 1/2 FITTED; not theory closed. Run from the repo root."""
import itertools, json, sys
from pathlib import Path
import sympy as s
import mpmath as mp

source = Path('action_scale_investigation_2026_11_05/single_clock.py')
sys.argv = ['single_clock.py', '--out', '/dev/null']
ns = {}; exec(compile(source.read_text().split('# Independent constraint Hessian')[0], str(source), 'exec'), ns)
a, H, k, ep, cY, m2, v, F1, Rm = [ns[x] for x in ('a', 'H', 'k', 'ep', 'cY', 'm2', 'v', 'F1', 'Rm')]
Z, Zd, C, Cd = [ns[x] for x in ('Z', 'Zd', 'C', 'Cd')]
Ls = s.Symbol('Lstar', positive=True); cy = 1 / (1 + Ls ** 2 * k * k / (2 * a * a))
L = s.expand(ns['Lred'].subs({F1: 1, Rm: 1, ns['F0']: v * v / 2, cY: cy}))
qd = s.Matrix([Zd, Cd]); q = s.Matrix([Z, C]); K = s.simplify(s.hessian(L, qd))
B = s.Matrix(2, 2, lambda i, j: s.diff(L, qd[i], q[j])); P = s.hessian(L, q)
Hd = -ep * H ** 2 - v ** 2 / (2 * m2)
flow = {a: a * H, H: Hd, v: -3 * H * v, ep: ep * (-6 * H - 2 * Hd / H)}
dt = lambda x: sum(s.diff(x, y) * dy for y, dy in flow.items())
G = s.simplify(((B + B.T) / 2).applyfunc(dt) - P); A = s.simplify(B - B.T)
fn = s.lambdify((a, H, k, ep, m2, v, Ls), (K, G, A), 'mpmath')


def roots(es, ms, ls, ks):
    vals = []
    for prec in (40, 80):
        with mp.workdps(prec):
            e, em, l, kk = map(mp.mpf, (es, ms, ls, ks)); vv = mp.sqrt(2 * em)
            km, gm, am = fn(1, 1, kk, e, 1, vv, l)
            c2 = mp.det(km); c1 = -(km[0, 0] * gm[1, 1] + km[1, 1] * gm[0, 0] - 2 * km[0, 1] * gm[0, 1] + am[0, 1] ** 2); c0 = mp.det(gm)
            disc = c1 * c1 - 4 * c2 * c0
            big = (-c1 + mp.sqrt(disc)) / (2 * c2); small = c0 / (c2 * big)
            vals.append([small, big])
    with mp.workdps(80):
        err = max(abs(z - y) / max(1, abs(y)) for z, y in zip(vals[0], vals[1]))
        r = vals[1]
        neg = [z for z in r if mp.im(z) == 0 and mp.re(z) < 0]
        return dict(epsilon_phi=es, epsilon_m=ms, Lstar=ls, k=ks, omega2=[mp.nstr(z, 30) for z in r],
                    negative_roots=len(neg), min_neg_omega2=float(mp.re(min(neg, key=mp.re))) if neg else None,
                    complex_roots=any(mp.im(z) != 0 for z in r), prec_err=float(err))


out = {}
# KA2: AC3's grid
ac3 = json.loads(Path('action_search_2026_11_05/AC3_matter_gradients/evidence/finite_v3/result.json').read_text())['rows']
ka2_err = 0.0; ka2_wit_match = True
for r in ac3:
    m = roots(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k'])
    with mp.workdps(80):
        for z, y in zip(m['omega2'], r['omega2']):
            zz, yy = mp.mpmathify(z), mp.mpmathify(y)
            ka2_err = max(ka2_err, float(abs(zz - yy) / max(1, abs(yy))))
    ka2_wit_match &= (m['negative_roots'] > 0) == (r['negative_roots'] > 0)
out['KA2'] = dict(max_rel_err=ka2_err, witnesses_match=bool(ka2_wit_match), pass_=bool(ka2_err <= 1e-25 and ka2_wit_match))
# note: AC3 stored 35-digit strings and we compare 30-digit strings; 1e-25 is below both
grids = {'A': (['0.1', '0.25', '0.4'], ['0.2', '0.6', '0.95'], ['0.0003', '0.003', '0.03'], ['3', '30', '300']),
         'B': (['0.1', '0.25', '0.4'], ['0.45', '0.8'], ['1e-4', '0.01', '0.1'], ['1', '50', '1000'])}
rows = [roots(*c) for c in itertools.product(*grids['A'])]
out['grid_A'] = rows; wit = [r for r in rows if r['negative_roots'] > 0]
out['grid_B_used'] = len(wit) < 3
if out['grid_B_used']:
    rowsB = [roots(*c) for c in itertools.product(*grids['B'])]; out['grid_B'] = rowsB
    wit += [r for r in rowsB if r['negative_roots'] > 0]
out['prec_agree'] = all(r['prec_err'] < 1e-25 for r in rows + out.get('grid_B', []))
wit.sort(key=lambda r: r['min_neg_omega2'])
out['n_witnesses_found'] = len(wit)
out['witnesses'] = wit[:16]
out['note'] = 'kappa = 1/2 FITTED; not theory closed'
Path('action_search_2026_11_05/AC23_fresh_slow_roots/witnesses.json').write_text(json.dumps(out, indent=1) + '\n')
print('KA2', out['KA2'], 'prec_agree', out['prec_agree'], 'grid_B_used', out['grid_B_used'], 'found', len(wit))
for r in out['witnesses']:
    print(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k'], r['min_neg_omega2'])
