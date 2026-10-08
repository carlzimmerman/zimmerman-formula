#!/usr/bin/env python3
"""CFG499: option A of CFG469 as a full track -- lenient black holes on the C-H/K khronon chassis.

Criteria: FROZEN_CRITERIA.md in this folder (3b820a1ec), committed alone before any script.
(1) metric-coupled moving black hole (O(v), l = 1, beta = 0; first metric-khronon round trip, local at the universal
    horizon (UH), plus the count); (2) collapse (cfg499_collapse.py); (3) every CFG467 gate on the no-constant sliver.
Theory plus offline numerics; no downloads; read-only on every other lane. kappa = 1/2 is FITTED and plays no role.

    python3 campaign_fresh_gravity/CFG499_chassis_option_A/cfg499_option_a.py
    CFG499_MUTATE=1 python3 campaign_fresh_gravity/CFG499_chassis_option_A/cfg499_option_a.py
Symbolic caches go to the system temp directory (never the repo).
"""
import os
import sys
import json
import time
import math
import tempfile
import itertools
import mpmath as mp
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import cfg499_lib as LB
from cfg499_lib import GS, LGS, el_equations, gs_sqrt, lam_gs

MUTATE = os.environ.get('CFG499_MUTATE', '0') == '1'
SUF = '_MUTATE' if MUTATE else ''
OUT_TXT = os.path.join(HERE, f'cfg499_option_a{SUF}.out')
OUT_JSON = os.path.join(HERE, f'cfg499_results{SUF}.json')
CACHE = os.path.join(tempfile.gettempdir(), 'cfg499_cache')
os.makedirs(CACHE, exist_ok=True)
T0 = time.time()
mp.mp.dps = 60
GS.N = 22
GS.ZTOL = mp.mpf('1e-40')

LINES = []


def P(s=''):
    print(s, flush=True)
    LINES.append(str(s))


def banner(s):
    P('')
    P('=' * 118)
    P(s)
    P('=' * 118)


CHECKS = {}


def check(name, measured, ok, load_bearing=True, note=''):
    CHECKS[name] = {'ok': bool(ok), 'measured': str(measured), 'load_bearing': load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f'         measured: {measured}')
    if note:
        P(f'         note: {note}')


def load(p):
    with open(os.path.join(REPO, p)) as f:
        return json.load(f)


OUT = {'lane': 'CFG499', 'mutate': MUTATE, 'frozen_criteria_commit': '3b820a1ec'}
J319 = load('campaign_fresh_gravity/CFG319_moving_black_hole/cfg319_moving_bh_results.json')
J467 = load('campaign_fresh_gravity/CFG467_alpha_c_sign_tension/cfg467_results.json')
J320 = load('campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability_results.json')
FOOTINGS = {'canonical': 9.36e-11, 'alt': 1.13e-10}

banner('CFG499  option A (lenient black holes) as a full track on the C-H/K chassis' +
       ('   *** MUTATE: alpha_c outside the window; strong UH branch s- ***' if MUTATE else ''))
P('Action: sqrt(-g)[R - lambda K^2 + alpha a.a], 16 pi G = 1, beta = 0, lambda = c_2, alpha = alpha_c.')
P('Scope of test (1): O(v), l = 1, Schwarzschild + the test-khronon background; first metric-khronon round trip')
P('F0 -> h1 -> F1, local at the UH (generalised Frobenius in x = r - r_UH) plus the boundary-condition count.')

# ================================================================================================ derivation
banner('S0  the angle-integrated quadratic Lagrangian of the full action for the l = 1 sector (sympy)')
r, P0, P1, P2, N0, N1, N2 = sp.symbols('r P0 P1 P2 N0 N1 N2')
al, la = sp.symbols('alpha lambda')
Ys, Ws, Y1s, W1s = sp.symbols('Y W Y1 W1')
cpath = os.path.join(CACHE, 'l1PN.srepr')
if os.path.exists(cpath):
    with open(cpath) as f:
        DER, OPS = eval(f.read(), sp.__dict__.copy())
    P(f'    loaded the cached derivation ({cpath.split(os.sep)[-1]} in the system temp dir)')
else:
    DER, OPS, _ = LB.derive_l1_PN(log=P)
    with open(cpath, 'w') as f:
        f.write(sp.srepr((DER, OPS)))
P('    background khronon kept as P = H\'(r) and lapse N0 (identity N0^-2 = -2P - eP^2); bilinear terms: ' +
  ', '.join(f'{k} {len(v)}' for k, v in DER.items()))
CURV, (rc_, thc_) = LB.derive_curvature_l1()
P(f'    linear curvature of the l = 1 metric perturbation: Kretschmann_0 = {CURV["K0"]}, {len(CURV["riem"])} Riemann components')

# ================================================================================================ K1 flat dispersion
banner('K1  flat-space khronon dispersion WITH metric mixing, from the same Lagrangian engine')


def k1_flat():
    t, x, y, z = sp.symbols('t x y z')
    X = [t, x, y, z]
    fl = [sp.Function(n)(t, z) for n in ('htt', 'htz', 'hzz', 'hp', 'pi', 'hxy')]
    htt, htz, hzz, hp, pi_, hxy = fl
    g0 = sp.diag(-1, 1, 1, 1)
    g1 = sp.Matrix([[htt, 0, 0, htz], [0, hp, hxy, 0], [0, hxy, hp, 0], [htz, 0, 0, hzz]])
    G = LB.Geometry(X, g0, g1, sp.Integer(1))
    R = G.ricci_scalar()
    K, a2, *_ = G.khronon(Tser=(t, pi_, 0))
    L = LB.s_add(LB.s_mul(G.sqrtg, R), LB.s_mul(G.sqrtg, LB.s_add(LB.s_scale(-la, LB.s_mul(K, K)), LB.s_scale(al, a2))))
    eqs = euler_equations(sp.expand(L[2]), fl, [t, z])
    w, k = sp.symbols('omega k')
    Am = sp.symbols('a0:6')
    sub = {fi: Am[i] * sp.exp(sp.I * (k * z - w * t)) for i, fi in enumerate(fl)}
    rows = []
    for e_ in eqs:
        ex = sp.simplify(e_.lhs.subs(sub).doit() * sp.exp(-sp.I * (k * z - w * t)))
        rows.append([sp.expand(sp.diff(ex, a_)) for a_ in Am])
    M = sp.Matrix(rows)
    tens = sp.factor(M[5, 5])
    Ms = M[0:5, [0, 2, 3]]                       # gauge pi = 0, htz = 0
    g = 0
    for c in itertools.combinations(range(5), 3):
        g = sp.gcd(g, sp.expand(Ms.extract(list(c), [0, 1, 2]).det()))
    g = sp.factor(g)
    w2 = sp.solve(sp.Eq([f for f in sp.factor_list(g)[1] if f[0].has(w) and f[0].has(al)][0][0], 0), w**2)
    return tens, g, w2


tens, gscal, w2 = k1_flat()
cS2 = la * (2 - al) / (al * (2 + 3 * la))
okK1 = len(w2) == 1 and sp.simplify(w2[0] - cS2 * sp.Symbol('k')**2) == 0 and sp.factor(tens + (sp.Symbol('k') - sp.Symbol('omega')) *
                                                                                          (sp.Symbol('k') + sp.Symbol('omega'))) == 0
P(f'    tensor: {tens}; scalar-sector determinant gcd: {gscal}')
check('K1 flat space: omega^2 = c_S^2 k^2 with c_S^2 = lambda (2 - alpha)/(alpha (2 + 3 lambda)) exactly, tensor speed 1',
      f'omega^2 = {w2}', okK1)

# ================================================================================================ L assembly, K2
LAG = {}
for nm, co in (('EH', 1), ('KK', -la), ('AA', al)):
    for k_, v in DER[nm].items():
        LAG[k_] = LAG.get(k_, 0) + co * v
P0v = -1 / (Ys * (Ys + Ws))
P1v = sp.diff(P0v, Ys) * Y1s + sp.diff(P0v, Ws) * W1s
BGS = {P0: P0v, P1: P1v, N0: Ys, N1: Y1s}
lam_x, be_ = sp.symbols('lam_x beta')
loc = {'Y': Ys, 'W': Ws, 'Y1': Y1s, 'alpha': al, 'beta': be_, 'lam_x': la, 'r': r}
S22c = sp.sympify(J319['numbers']['symbolic']['S22'].replace('lambda', 'lam_x'), locals=loc).subs(be_, 0)
S22m = LAG[('F2', 'F2')].subs(BGS).subs(r, 2 / (1 - Ys**2 + Ws**2))
d22 = sp.simplify(sp.factor(S22m - S22c))
devops = []
f0s, f1s, f2s = sp.symbols('F0 F1 F2')
W1rel = (Ys * Y1s - 1 / r**2) / Ws
for nm, key in (('K1', 'dK_ops'), ('A1', 'daa_ops')):
    co = [sp.diff(OPS[nm], z) for z in (f0s, f1s, f2s)]
    ref = [sp.sympify(s_, locals=loc) for s_ in J319['numbers']['symbolic'][key]]
    for a_, b_ in zip(co, ref):
        a2_ = a_.subs(BGS).subs(W1s, W1rel).subs(r, 2 / (1 - Ys**2 + Ws**2))
        devops.append(sp.simplify(a2_ - b_))
banner('K2  the khronon block at h = 0 against CFG319\'s committed S22, dK and d(a.a) operators')
check('K2 h = 0: S22 equals CFG319\'s committed S22 exactly; the O(v) dK and d(a.a) operator coefficients equal CFG319\'s',
      f'S22 difference {d22}; operator differences {devops}', d22 == 0 and all(z == 0 for z in devops))

# ================================================================================================ K3 and 1c(i)
banner('K3  Einstein-Hilbert block gauge invariance, and 1c(i) the homogeneous Einstein l = 1 solutions')
FN = ('A', 'B', 'C', 'D', 'E', 'Kf', 'F')
ff = {n: sp.Function(n)(r) for n in FN}


def jetf(sym):
    n, k = str(sym)[:-1], int(str(sym)[-1])
    return ff[n].diff(r, k) if k else ff[n]


LEH = sum(v * jetf(sp.Symbol(a_)) * jetf(sp.Symbol(b_)) for (a_, b_), v in DER['EH'].items())
eqsEH = euler_equations(LEH, [ff[n] for n in FN[:6]], r)
x0f, x1f, x2f = [sp.Function(n)(r) for n in ('xi0', 'xi1', 'xi2')]
e_r = 1 - 2 / r
GAUGE = {'A': 2 * (-r * x0f - (r - 2) * x1f) / r**3, 'B': x0f.diff(r) + 2 * x1f / r**2, 'C': 2 * x1f.diff(r), 'D': x0f,
         'E': x1f + x2f.diff(r) - 2 * x2f / r, 'Kf': 2 * (r * x0f + (r - 2) * x1f - x2f) / r**2}
gres = [sp.simplify(eq.lhs.subs({ff[n]: GAUGE[n] for n in FN[:6]}).doit()) for eq in eqsEH]
check('K3 a pure-gauge l = 1 h = L_xi g (xi = (xi0 cos, xi1 cos, -xi2 sin, 0)) annihilates all six Einstein-Hilbert '
      'Euler-Lagrange equations identically', f'residuals {gres}', all(z == 0 for z in gres))
# 1c(i): gauge C = E = Kf = 0, vacuum
E6 = [sp.factor(sp.simplify(eq.lhs.subs({ff['C']: 0, ff['E']: 0, ff['Kf']: 0}).doit())) for eq in eqsEH]
b_, p_, q_ = sp.symbols('b p q')
Bsol = sp.dsolve(sp.Eq(E6[0], 0), ff['B']).rhs                       # E_A: B' = 0
Dsol = sp.solve(E6[4], ff['D'])[0].subs(ff['B'], Bsol).doit()        # E_E: algebraic in D
EB = sp.simplify(E6[1].subs({ff['D']: Dsol, ff['B']: Bsol}).doit())
Ah = sp.dsolve(sp.numer(sp.together(EB)), ff['A']).rhs
sol_v = {ff['A']: Ah, ff['B']: Bsol, ff['D']: Dsol.subs(ff['A'], Ah).doit()}
rest = [sp.simplify(e_.subs(sol_v).doit()) for e_ in E6]
consts = sorted(set().union(*[z.free_symbols for z in sol_v.values()]) - {r}, key=str)
cons_eqs = [z for z in rest if z != 0]
free = sp.solve(cons_eqs, consts, dict=True) if cons_eqs else [{}]
dim = len(consts) - (len(free[0]) if free else 0)
# residual gauge preserving C = E = Kf = 0: xi1 = c1, xi2 = c2 r^2 + c1 r, xi0 = c2 r + 2 c1/r
c1_, c2_ = sp.symbols('c1 c2')
resg = {x1f: c1_, x2f: c2_ * r**2 + c1_ * r, x0f: c2_ * r + 2 * c1_ / r}
gchk = [sp.simplify(GAUGE[n].subs(resg).doit()) for n in ('C', 'E', 'Kf')]
P(f'    gauge C = E = Kf = 0 vacuum system: E_A -> B = {Bsol}; E_E -> D = {sp.simplify(Dsol)}; E_B -> A = {Ah}')
P(f'    remaining equations after substitution: {rest}; constants {consts}, constraint solution {free}')
P(f'    residual gauge (C, E, Kf preserved: {gchk}) is 2-dimensional (c1, c2): A = {sp.simplify(GAUGE["A"].subs(resg).doit())}, '
  f'B = {sp.simplify(GAUGE["B"].subs(resg).doit())}, D = {sp.simplify(GAUGE["D"].subs(resg).doit())}')
ok_ci = dim == 2 and all(z == 0 for z in gchk)
check('1c(i) every homogeneous solution of the gauge-fixed Einstein l = 1 block is pure gauge: solution-space dimension '
      '= residual-gauge dimension = 2 (no physical l = 1 constant, none excluded anywhere, so no condition is added)',
      f'dimension {dim} vs residual gauge 2', ok_ci)
OUT['count_1c_i'] = {'vacuum_dim': dim, 'residual_gauge_dim': 2}

# ================================================================================================ series machinery
ARGS = (r, P0, P1, P2, N0, N1, N2, al, la)
LAMM = {part: {k_: lam_gs(v, ARGS) for k_, v in DER[part].items()} for part in DER}
Ast = sp.sympify(J319['numbers']['symbolic']['A_static'].replace('lambda', 'lam_x'), locals=loc).subs(be_, 0)
Bst = sp.sympify(J319['numbers']['symbolic']['B_static'].replace('lambda', 'lam_x'), locals=loc).subs(be_, 0)
Y2RHS = sp.lambdify((r, Ys, Y1s, al, la), -Bst / Ast, 'mpmath')
JETS = sp.symbols('A0 A1 A2 B0 B1 B2 C0 C1 C2 D0 D1 D2 E0 E1 E2 Kf0 Kf1 Kf2')
THETA0 = mp.mpf('0.7')
CURVF = {'dR': sp.lambdify((r,) + JETS, CURV['dR'], 'mpmath'), 'dKr': sp.lambdify((r,) + JETS, CURV['dKr'], 'mpmath')}
RIEMF = {k_: sp.lambdify((r, thc_) + JETS, v, 'mpmath') for k_, v in CURV['riem'].items()}


def background(r0, Y0, Yp0, a, l, perturbY2=0):
    x = GS.x()
    rr = r0 + x
    XS = GS.XS
    Yser = GS([Y0, Yp0 * XS])
    for _ in range(GS.N + 2):
        rhs = Y2RHS(rr, Yser, Yser.deriv(), a, l) + perturbY2
        rs = rhs.strip()
        cs = [mp.mpf(0)] * rs.v + rs.c
        Yp = [Yp0] + [XS * cs[k] / (k + 1) for k in range(GS.N - 1)]
        Yser = GS([Y0] + [XS * Yp[k] / (k + 1) for k in range(GS.N - 1)])
    W = gs_sqrt(Yser * Yser - (1 - 2 / rr))
    Pp = -1 / (Yser * (Yser + W))
    return dict(r=rr, P0=Pp, P1=Pp.deriv(), P2=Pp.deriv().deriv(), N0=Yser, N1=Yser.deriv(), N2=Yser.deriv().deriv(),
                Y=Yser, W=W)


def coeffs(bg, a, l, parts=(('EH', 1), ('KK', None), ('AA', None))):
    M = {}
    for part, w in parts:
        ww = w if w is not None else (-l if part == 'KK' else a)
        for k_, f in LAMM[part].items():
            val = f(bg['r'], bg['P0'], bg['P1'], bg['P2'], bg['N0'], bg['N1'], bg['N2'], a, l)
            val = val if isinstance(val, GS) else GS.const(val)
            M[k_] = M.get(k_, GS.const(0)) + val * ww
    return M


def split_M(M):
    MFF = {k_: v for k_, v in M.items() if k_[0][0] == 'F' and k_[1][0] == 'F'}
    MhF = {k_: v for k_, v in M.items() if (k_[0][0] == 'F') != (k_[1][0] == 'F')}
    return MFF, MhF


def coeff_at(s_, p):
    i = p - s_.v
    return s_.c[i] if 0 <= i < GS.N else mp.mpf(0)


def lead(g, nlook=10, thr=mp.mpf('1e-18')):
    """leading power of a GS (or LGS: (power, 'log'|'pow')) using a noise floor relative to the window maximum."""
    parts = [('pow', g)] if isinstance(g, GS) else [('pow', g.a), ('log', g.b)]
    best = None
    sc = mp.mpf(0)
    for _, s_ in parts:
        st = s_
        vals = [abs(z) for z in st.c[:GS.N - 6]]
        sc = max([sc] + vals)
    for kind, s_ in parts:
        for k in range(GS.N - 6):
            if abs(s_.c[k]) > thr * sc:
                pw = s_.v + k
                if best is None or pw < best[0] or (pw == best[0] and kind == 'log'):
                    best = (pw, kind, s_.c[k])
                break
    return best


def qr_lstsq(rows, rhs):
    gmax = max([abs(z) for row in rows for z in row] + [abs(z) for z in rhs])
    R2, H2 = [], []
    for i in range(len(rows)):
        sc = max([abs(z) for z in rows[i]] + [abs(rhs[i])])
        if sc > gmax * mp.mpf('1e-30'):
            R2.append([z / sc for z in rows[i]])
            H2.append(rhs[i] / sc)
    A = mp.matrix(R2)
    b = mp.matrix(H2)
    cs = [max(abs(A[i, j]) for i in range(A.rows)) or mp.mpf(1) for j in range(A.cols)]
    for j in range(A.cols):
        for i in range(A.rows):
            A[i, j] /= cs[j]
    try:
        if A.rows >= A.cols:
            x, _ = mp.qr_solve(A, b)
            return [x[j] / cs[j] for j in range(A.cols)]
    except (ZeroDivisionError, ValueError):
        pass
    U, S, V = mp.svd_r(A)
    smax = max(S)
    x = [mp.mpf(0)] * A.cols
    for k in range(len(S)):
        if S[k] > smax * mp.mpf('1e-40'):
            coef = mp.fsum(U[i, k] * b[i] for i in range(A.rows)) / S[k]
            for j in range(A.cols):
                x[j] += coef * V[k, j]
    return [x[j] / cs[j] for j in range(A.cols)]


def solve_metric(Msrc, F0, sigma, nwin, logs):
    """h1 in the gauge C = E = Kf = 0 (unknowns A, B, D) from all six Einstein equations with the khronon source F0.
    Unknown powers from 3 below the source's lead; equations from 2 below the lowest unknown, so that every unknown is
    constrained from its first appearance (the Einstein operator is second order); the residual is checked on all but
    the top two powers of the window."""
    src = el_equations(Msrc, {'F': LGS(F0)}, which=['A', 'B', 'C', 'D', 'E', 'Kf'])
    slo = min(lead(src[q])[0] for q in src if src[q] is not None and lead(src[q]) is not None)
    m0 = slo - 3                  # lowest unknown power
    plo = m0 - 2                  # equations start where the lowest unknown first appears (second-order operator)
    nwin = nwin + 5
    nco = nwin + 2
    cols, colE = [], []
    for n in ('A', 'B', 'D'):
        for kind in (('a', 'b') if logs else ('a',)):
            for j in range(nco):
                g = GS([1], m0 + j, sigma)
                f = LGS(g) if kind == 'a' else LGS(GS([0], m0 + j, sigma), g)
                cols.append((n, kind, m0 + j))
                colE.append(el_equations(Msrc, {n: f}, which=['A', 'B', 'C', 'D', 'E', 'Kf']))
    rows, rhs = [], []
    for q in ('A', 'B', 'C', 'D', 'E', 'Kf'):
        for part in (('a', 'b') if logs else ('a',)):
            for p in range(plo, plo + nwin):
                rows.append([coeff_at(getattr(E[q], part), p) if E[q] is not None else mp.mpf(0) for E in colE])
                rhs.append(-coeff_at(getattr(src[q], part), p) if src[q] is not None else mp.mpf(0))
    sol = qr_lstsq(rows, rhs)
    H = {}
    for n in ('A', 'B', 'D'):
        a_ = [sol[i] for i, c in enumerate(cols) if c[0] == n and c[1] == 'a']
        b_ = [sol[i] for i, c in enumerate(cols) if c[0] == n and c[1] == 'b'] if logs else [0]
        H[n] = LGS(GS(a_, m0, sigma), GS(b_, m0, sigma) if logs else GS([0], m0, sigma))
    Eh = el_equations(Msrc, {'A': H['A'], 'B': H['B'], 'D': H['D'], 'F': LGS(F0)}, which=['A', 'B', 'C', 'D', 'E', 'Kf'])
    ssc = max(abs(coeff_at(getattr(src[q], pt_), p)) for q in src if src[q] is not None for pt_ in ('a', 'b')
              for p in range(plo, plo + nwin))
    res = max(abs(coeff_at(getattr(Eh[q], pt_), p)) for q in Eh if Eh[q] is not None for pt_ in ('a', 'b')
              for p in range(plo, plo + nwin - 2)) / ssc
    # keep only the coefficients validated by the residual window (unknowns above it are not constrained)
    ptop = plo + nwin - 3
    for n in H:
        for part in (H[n].a, H[n].b):
            for k in range(GS.N):
                if part.v + k > ptop:
                    part.c[k] = mp.mpf(0)
    return H, res, plo, src


def f0_series(MFF, sigma, nstart, NF=12):
    """Frobenius recursion for the test-khronon mode x^(sigma + nstart); resonant orders are set to zero and the
    solvability (log-freeness) residual is reported."""
    cols = {n: el_equations(MFF, {'F': GS([1], n, sigma)}, which=['F'])['F'] for n in range(nstart, nstart + NF)}
    f = {nstart: mp.mpf(1)}
    logres = []
    scale = max(abs(coeff_at(cols[n], n)) for n in range(nstart, nstart + NF))
    for n in range(nstart + 1, nstart + NF):
        acc = mp.fsum(f[j] * coeff_at(cols[j], n) for j in f)
        dia = coeff_at(cols[n], n)
        if abs(dia) < mp.mpf('1e-25') * scale:
            logres.append((n, acc / scale))
            f[n] = mp.mpf(0)
        else:
            f[n] = -acc / dia
    F0 = GS([f[n] for n in range(nstart, nstart + NF)], nstart, sigma)
    EF = el_equations(MFF, {'F': F0}, which=['F'])['F']
    resid = max(abs(coeff_at(EF, p)) for p in range(nstart, nstart + NF - 1)) / scale
    return F0, resid, logres, cols


def curvature_of(H, bg, sigma):
    zero = LGS(GS([0], 0, sigma))
    jet = {}
    for n in ('A', 'B', 'C', 'D', 'E', 'Kf'):
        h = H.get(n, zero)
        jet[n] = [h, h.deriv(), h.deriv().deriv()]
    args = [jet[n][k] for n in ('A', 'B', 'C', 'D', 'E', 'Kf') for k in range(3)]
    out = {nm: f(bg['r'], *args) for nm, f in CURVF.items()}
    riem = {k_: f(bg['r'], THETA0, *args) for k_, f in RIEMF.items()}
    return out, riem


def analyze_mode(name, bg, MFF, MhF, MEH, sigma_kind, s_value):
    """sigma_kind: 'frac' (sector sigma = s_value) or 'int' (sector 0, start power s_value)."""
    if sigma_kind == 'frac':
        sigma, nstart, logs = s_value, 0, False
    else:
        sigma, nstart, logs = mp.mpf(0), int(s_value), True
    F0, fres, logres, cols = f0_series(MFF, sigma, nstart)
    Msrc = dict(MEH)
    Msrc.update(MhF)
    H, hres, plo, src = solve_metric(Msrc, F0, sigma, 8, logs)
    hl = {n: lead(H[n]) for n in H}
    srcl = {q: lead(src[q]) for q in src if src[q] is not None}
    curv, riem = curvature_of(H, bg, sigma)
    cl = {k_: lead(v) for k_, v in curv.items()}
    rl = {str(k_): lead(v) for k_, v in riem.items() if lead(v) is not None}
    S = el_equations(MhF, {n: H[n] for n in H}, which=['F'])['F']
    Sl = lead(S)
    # feedback F1: E_FF[F1] = -S, order by order (logs where resonant)
    fb = {'S_lead': Sl}
    shift = None
    if Sl is not None:
        q0 = Sl[0]
        dia = coeff_at(cols[q0], q0) if q0 in cols else None
        if q0 < nstart:
            fb['F1_lead'] = 'BELOW the mode (feedback dominates)'
        else:
            # resonance at the mode's own power n = nstart (non-integer sector) or at roots -1, 0 (integer sector)
            res_pows = [p for p in range(q0, q0 + 4) if p in cols and abs(coeff_at(cols[p], p)) <
                        mp.mpf('1e-25') * max(abs(coeff_at(cols[n], n)) for n in cols)]
            fb['resonant_powers_in_reach'] = res_pows
            if sigma_kind == 'frac' and q0 == nstart:
                # exponent shift: P(sigma + d) + S0 = 0
                Pp = mp.diff(lambda s_: coeff_at(el_equations(MFF, {'F': GS([1], 0, s_)}, which=['F'])['F'], 0), sigma)
                shift = -coeff_at(S.a if isinstance(S, LGS) else S, q0) / Pp
            fb['F1_lead_power'] = q0
    fb['exponent_shift'] = shift
    return dict(mode=name, sigma=sigma, nstart=nstart, F0_resid=fres, logres=logres, h_resid=hres, h_lead=hl,
                src_lead=srcl, curv_lead=cl, riem_lead=rl, feedback=fb, H=H, F0=F0)


def fmt_lead(l_):
    if l_ is None:
        return '0'
    return f"{'ln.' if l_[1] == 'log' else ''}x^(s+{l_[0]})"


# ================================================================================================ K4
banner('K4  joint gauge invariance of the khronon cross terms on an on-shell background (regular point r = 3)')
GS.XS = mp.mpf(1)
k4 = {}
for tag, pert in (('on-shell', 0), ('off-shell control (Y\'\' + 1e-3)', mp.mpf('1e-3'))):
    a_k, l_k = mp.mpf('1e-3'), mp.mpf('0.05')
    bgk = background(mp.mpf(3), mp.mpf('0.7'), mp.mpf('0.2'), a_k, l_k, perturbY2=pert)
    Mk = coeffs(bgk, a_k, l_k, parts=(('KK', None), ('AA', None)))
    xi0 = GS([mp.mpf('0.3'), mp.mpf('0.1'), mp.mpf('-0.2')])
    xi1 = GS([mp.mpf('-0.5'), mp.mpf('0.4'), mp.mpf('0.15')])
    xi2 = GS([mp.mpf('0.25'), mp.mpf('-0.3'), mp.mpf('0.2')])
    rr = bgk['r']
    flds = {'A': 2 * (-rr * xi0 - (rr - 2) * xi1) / rr**3, 'B': xi0.deriv() + 2 * xi1 / rr**2, 'C': 2 * xi1.deriv(),
            'D': xi0, 'E': xi1 + xi2.deriv() - 2 * xi2 / rr, 'Kf': 2 * (rr * xi0 + (rr - 2) * xi1 - xi2) / rr**2,
            'F': xi1 + bgk['P0'] * (xi0 + (1 - 2 / rr) * xi1)}
    EFg = el_equations(Mk, flds, which=['F'])['F']
    EFf = el_equations(Mk, {'F': flds['F']}, which=['F'])['F']
    rel = max(abs(coeff_at(EFg, p)) for p in range(0, 8)) / max(abs(coeff_at(EFf, p)) for p in range(0, 8))
    k4[tag] = rel
    P(f'    {tag}: |E_F(pure gauge)| / |E_F(F part alone)| over x^0..x^7 = {mp.nstr(rel, 3)}')
check('K4 the khronon Euler-Lagrange equation annihilates the joint pure-gauge (h, F) = (L_xi g, xi.dT0) on an on-shell '
      'background (<= 1e-20 relative), and does not when the background is pushed off shell (teeth: >= 1e-6)',
      ', '.join(f'{k_}: {mp.nstr(v, 3)}' for k_, v in k4.items()),
      k4['on-shell'] <= mp.mpf('1e-20') and list(k4.values())[1] >= mp.mpf('1e-6'))

# ================================================================================================ 1c(ii) structure
banner('1c(ii)  the cross terms: analytic wherever the lapse Y != 0 (so at r_S), and decaying at infinity')
cross_keys = [k_ for k_ in LAG if (k_[0][0] == 'F') != (k_[1][0] == 'F')]
bad = []
for k_ in cross_keys:
    for part in ('KK', 'AA'):
        if k_ in DER[part]:
            den = sp.denom(sp.together(DER[part][k_]))
            fac = [f for f, m in sp.factor_list(den)[1]]
            if any(not (f.free_symbols <= {r, N0}) for f in fac):
                bad.append((k_, part, den))
P(f'    {len(cross_keys)} cross (h, F) coefficients; denominators that contain anything but r and the lapse N0: {bad or "none"}')
# infinity: stealth-type background W = C/r^2 (C = 3 sqrt3/4), Y = sqrt(e + W^2); boosted khronon F = -r.
# The metric-equation sources of F = -r are evaluated numerically (GS series about r0, exact in r0) at large r0.
Cst = 3 * mp.sqrt(3) / 4
lowest = {}
src_vals = {}
GS.XS = mp.mpf(1)
for r0 in (mp.mpf(10)**2, mp.mpf(10)**3, mp.mpf(10)**4):
    x = GS.x()
    rr = r0 + x
    Yb = gs_sqrt(1 - 2 / rr + Cst**2 / rr**4)
    Wb = Cst / rr**2
    Pb = -1 / (Yb * (Yb + Wb))
    bgi = dict(r=rr, P0=Pb, P1=Pb.deriv(), P2=Pb.deriv().deriv(), N0=Yb, N1=Yb.deriv(), N2=Yb.deriv().deriv())
    Mi = coeffs(bgi, mp.mpf('1e-9'), mp.mpf('0.05'), parts=(('KK', None), ('AA', None)))
    MhFi = {k_: v for k_, v in Mi.items() if (k_[0][0] == 'F') != (k_[1][0] == 'F')}
    Si = el_equations(MhFi, {'F': -rr}, which=['A', 'B', 'C', 'D', 'E', 'Kf'])
    for q in Si:
        src_vals.setdefault(q, []).append(abs(coeff_at(Si[q], 0)) if Si[q] is not None else mp.mpf(0))
for q, vals in src_vals.items():
    if max(vals) == 0:
        lowest[q] = None
    else:
        lowest[q] = float(-(mp.log(vals[2]) - mp.log(vals[0])) / mp.log(100))
    P(f'    E_{q} source of the boosted khronon F = -r at r = 1e2, 1e3, 1e4: ' + ', '.join(mp.nstr(v, 3) for v in vals) +
      f'  -> falls as r^-{lowest[q]:.2f}' if lowest[q] is not None else f'    E_{q} source: identically 0')
ok_cii = not bad and all(v is None or v >= 0.9 for v in lowest.values())
check('1c(ii) every cross coefficient is analytic wherever the lapse Y != 0 (denominators are powers of r and N0 only, so the '
      'option-C khronon, analytic at r_S, sources an analytic metric response and an analytic feedback there: r_S keeps '
      'one no-log condition), and the cross source of the boosted khronon F = -r decays at infinity (every Euler-Lagrange source density, which carries sqrt(-g) ~ r^2, falls at least as r^-1, i.e. the stress as r^-3; the l = 1 response of r^-3 is ~ r^-1: asymptotically flat, no new inadmissible mode)',
      f'non-(r, N0) denominators: {len(bad)}; decay powers of the sources: {lowest}', ok_cii)

# 1c(iii) reading
banner('1c(iii)  reading: the coupled spin-0 horizon (K1 c_S) vs the test-khronon one')
for a_r, l_r in ((3.2e-9, 7.2888e-3), (9.624e-14, 0.0667)):
    ratio = math.sqrt((2 + 3 * l_r) / (2 - a_r))
    P(f'    alpha {a_r:.3e}, c_2 {l_r:.4e}: c_S(test)/c_S(coupled) = sqrt((2 + 3 lambda)/(2 - alpha)) = {ratio:.5f}; '
      f'r_S - r_UH ~ 0.61 M/c_S grows by this factor (a single regular singular point, shifted)')

# ================================================================================================ W5 points
banner('1a / 1b  the five window points: F0 (test-khronon UH modes) -> h1 (Einstein response) -> F1 (feedback)')
runs = J319['numbers']['runs']
W5 = [k_ for k_ in runs if k_.startswith('W5')]
W5.sort()
POINTS = []
mode_set = [('s+', 'frac'), ('-1', 'int'), ('0', 'int')]
if MUTATE:
    mode_set = [('s-', 'frac')]
for key in W5:
    pt = runs[key]
    a = mp.mpf(pt['alpha'])
    l = mp.mpf(pt['lambda'])
    rU = mp.mpf(pt['rUH'])
    y1 = mp.mpf(pt['YU1'])
    GS.XS = mp.mpf(pt['dS'])
    tp = time.time()
    bg = background(rU, mp.mpf(0), y1, a, l)
    W0 = bg['W'].c[0]
    disc = mp.sqrt(1 + 2 * (W0**2 + 1)**2 / y1**2)
    splus, sminus = (-1 + disc) / 2, (-1 - disc) / 2
    M = coeffs(bg, a, l)
    MFF, MhF = split_M(M)
    MEH = coeffs(bg, a, l, parts=(('EH', 1),))
    P(f'  -- {key}: alpha {float(a):.4e}, c_2 {float(l):.4e}, r_UH {mp.nstr(rU, 15)}, y1 {mp.nstr(y1, 12)}, '
      f'W0 {mp.nstr(W0, 12)}; s+ {mp.nstr(splus, 12)} (CFG319 {pt["rootsU"][3]}), s- {mp.nstr(sminus, 12)}; '
      f'series variable x / {float(GS.XS):.3e}')
    res_pt = {'key': key, 'alpha': float(a), 'c2': float(l), 'splus': float(splus), 'sminus': float(sminus), 'modes': {}}
    for mname, kind in mode_set:
        sval = {'s+': splus, 's-': sminus, '-1': -1, '0': 0}[mname]
        R_ = analyze_mode(mname, bg, MFF, MhF, MEH, kind, sval)
        base = float(R_['sigma']) + R_['nstart']
        hl = R_['h_lead']
        P(f'     mode {mname:>2}: F0 residual {mp.nstr(R_["F0_resid"], 2)}; resonances in F0 {[(n, mp.nstr(z, 2)) for n, z in R_["logres"]]}; '
          f'h1 (all six Einstein eqs) residual {mp.nstr(R_["h_resid"], 2)}')
        P(f'              stress (Einstein-equation sources) lead: ' + ', '.join(f'{q} {fmt_lead(v)}' for q, v in R_['src_lead'].items()))
        P(f'              h1 lead (gauge C = E = Kf = 0): ' + ', '.join(f'{n} {fmt_lead(v)}' for n, v in hl.items()))
        P(f'              curvature lead: dR {fmt_lead(R_["curv_lead"]["dR"])}, dKretschmann {fmt_lead(R_["curv_lead"]["dKr"])}; '
          f'worst Riemann component (EF basis) ' + (min((fmt_lead(v), k_) for k_, v in R_['riem_lead'].items() if v)[0]
                                                     if R_['riem_lead'] else 'none'))
        P(f'              feedback into the khronon equation: {R_["feedback"]}')
        # physical exponents
        def ex_(l_):
            return None if l_ is None else (float(R_['sigma']) + l_[0], l_[1])
        h_exps = {n: ex_(v) for n, v in hl.items()}
        cv_exps = {k_: ex_(v) for k_, v in R_['curv_lead'].items()}
        rm_exps = [ex_(v) for v in R_['riem_lead'].values() if v is not None]
        fb = R_['feedback']
        S_exp = ex_(fb['S_lead']) if fb.get('S_lead') else None
        res_pt['modes'][mname] = dict(F0_resid=float(R_['F0_resid']), h_resid=float(R_['h_resid']),
                                      logres=[(n, float(z)) for n, z in R_['logres']],
                                      src_exps={q: ex_(v) for q, v in R_['src_lead'].items()}, h_exps=h_exps,
                                      curv_exps=cv_exps, riem_min=min(rm_exps) if rm_exps else None,
                                      feedback_S_exp=S_exp,
                                      exponent_shift=float(fb['exponent_shift']) if fb.get('exponent_shift') is not None else None,
                                      resonant=fb.get('resonant_powers_in_reach'))
    res_pt['time_s'] = time.time() - tp
    POINTS.append(res_pt)
    P(f'     [{res_pt["time_s"]:.0f}s]')
OUT['test1_points'] = POINTS


# ------------------------------------------------------------------------------------------------ scoring of (1)
def score_point(pt, mode='s+'):
    m = pt['modes'][mode]
    s_ = pt['splus'] if mode == 's+' else pt['sminus']
    fails = []
    # weak: h C^1 (exponent > 1 or integer >= 0 with no log), curvature exponents > -1, O(v^2) 2 q_min > -1
    for n, e_ in m['h_exps'].items():
        if e_ is None:
            continue
        if not (e_[0] > 1 + 1e-9 or (abs(e_[0] - round(e_[0])) < 1e-12 and e_[0] >= 0 and e_[1] == 'pow')):
            fails.append(f'h {n} ~ {e_}')
    qs = [v[0] for v in m['curv_exps'].values() if v is not None] + ([m['riem_min'][0]] if m['riem_min'] else [])
    qmin = min(qs) if qs else None
    if qmin is not None and not qmin > -1:
        fails.append(f'curvature x^{qmin:.3f} not integrable')
    if qmin is not None and not 2 * min(qmin, 0) > -1:
        fails.append(f'O(v^2) quadratic invariants x^{2 * qmin:.3f} not integrable')
    # feedback: no exponent below the mode, shift keeps s+ in (1/2, 1)
    if m['feedback_S_exp'] is not None and m['feedback_S_exp'][0] < s_ - 1e-9:
        fails.append('feedback below the mode exponent')
    if m['exponent_shift'] is not None:
        sh = s_ + m['exponent_shift']
        if not 0.5 < sh < 1:
            fails.append(f'shifted exponent {sh}')
    weak = not fails
    # hidden: tau ~ x^(1 + s) C^1 with non-vanishing gradient, h bounded/continuous
    hidden = (1 + s_ > 1) and all(e_ is None or e_[0] > 0 for e_ in m['h_exps'].values())
    return weak, hidden, fails, qmin


def score_int(pt):
    fails = []
    for mname in ('-1', '0'):
        if mname not in pt['modes']:
            continue
        m = pt['modes'][mname]
        if any(abs(z) > 1e-20 for _, z in m['logres']):
            fails.append(f'mode {mname}: log in F0')
        for n, e_ in m['h_exps'].items():
            if e_ is not None and (e_[1] == 'log' or e_[0] < 0):
                fails.append(f'mode {mname}: h {n} ~ {e_}')
        for k_, e_ in m['curv_exps'].items():
            if e_ is not None and (e_[0] <= -1):
                fails.append(f'mode {mname}: {k_} ~ {e_}')
        if m['feedback_S_exp'] is not None:
            res = m['resonant'] or []
            if res and m['feedback_S_exp'][0] <= max(res):
                fails.append(f'mode {mname}: feedback reaches resonant powers {res} (log in F1)')
    return fails


banner('Scoring test (1) by the frozen rule')
t1_rows = []
for pt in POINTS:
    if MUTATE:
        weak, hidden, fails, qmin = score_point(pt, 's-')
        ifails = []
    else:
        weak, hidden, fails, qmin = score_point(pt, 's+')
        ifails = score_int(pt)
    t1_rows.append(dict(key=pt['key'], weak=weak and not ifails, hidden=hidden, fails=fails + ifails, qmin=qmin))
    P(f"    {pt['key']:24s}: 1a weak {weak and not ifails}; 1b hidden {hidden}; curvature exponent min {qmin}; fails {fails + ifails}")
t1_weak = all(r_['weak'] for r_ in t1_rows)
t1_hidden = all(r_['hidden'] for r_ in t1_rows)
k5 = max(m['h_resid'] for pt in POINTS for m in pt['modes'].values())
check('K5 the metric response satisfies all six Einstein equations (incl. the gauged-away components) order by order in the '
      'solved window, relative to the source (<= 1e-20)', f'max residual {k5:.2e}', k5 <= 1e-20)
f0r = max(m['F0_resid'] for pt in POINTS for m in pt['modes'].values())
check('K5b the F0 Frobenius series solve the test-khronon equation (<= 1e-30 relative) with the closed-form exponent',
      f'max residual {f0r:.2e}', f0r <= 1e-30)
ok_controls_1 = all(CHECKS[k_]['ok'] for k_ in CHECKS if k_.startswith(('K1', 'K2', 'K3', 'K4', 'K5')))
t1_count = ok_ci and ok_cii and t1_weak
if not ok_controls_1:
    T1 = 'UNDECIDED'
elif t1_weak and t1_hidden and t1_count:
    T1 = 'PASSES'
else:
    T1 = 'FAILS'
P(f'    (1) 1a weak {t1_weak}; 1b hidden {t1_hidden}; 1c count (Delta_len = 0) {t1_count}  ->  (1) {T1}')
OUT['test1'] = dict(verdict=T1, weak=t1_weak, hidden=t1_hidden, count=t1_count, rows=t1_rows)

# ================================================================================================ (2) collapse
banner('(2)  COLLAPSE (cfg499_collapse.py)')
import cfg499_collapse as CL
if MUTATE:
    P('    MUTATE run: test (2) is not re-run (it is not part of the MUTATE flips); read from the main JSON if present.')
    try:
        with open(os.path.join(HERE, 'cfg499_results.json')) as f:
            col = json.load(f)['test2']
    except Exception:
        col = None
else:
    colres = CL.run_collapse(P=P, check=check)
    a2 = colres['2a']
    frozen_2a = a2['i_exist_T40'] and a2['ii_frozen_C_increases_to_Clim'] and a2['iii_frozen_Rs_gt_1p5'] and a2['iv_kappa']
    corr_2a = a2['i_exist_T40'] and a2['ii_corrected_C_to_Clim'] and a2['iv_kappa']
    b_ok = colres['2b']['passes']
    if not (frozen_2a and b_ok):
        T2 = 'FAILS'
    else:
        T2 = 'PARTIAL'
    T2_corr = 'PARTIAL' if (corr_2a and b_ok) else 'FAILS'
    col = dict(verdict_frozen=T2, verdict_corrected_reading=T2_corr, frozen_2a=frozen_2a, corrected_2a=corr_2a,
               b=b_ok, c='ARG', details={k_: (v if k_ != '2b' else {kk: vv for kk, vv in v.items()}) for k_, v in colres.items()})
    P(f'    (2) by the frozen rule: 2a {frozen_2a} (clauses ii and iii as written), 2b {b_ok}, 2c ARG  ->  (2) {T2}')
    P(f'    (2) under the dated correction (clauses ii/iii replaced, see README): 2a {corr_2a}, 2b {b_ok}, 2c ARG  ->  {T2_corr}')
OUT['test2'] = col

# ================================================================================================ (3) the window
banner('(3)  THE WINDOW: every CFG467 gate on the no-constant sliver (and with the hierarchy)')
M_RED = 2.435e18
LHC = 1.3e4
LHL = J320['numbers']['summary']['Lambda_HL_max_GeV']
AC_MIN, AC_MAX = 9.624047966926507e-14, 3.2e-9
C2MIN, C2MAX = 7.2888e-3, 0.0667


def cs2(a_, c_):
    return c_ * (2 - a_) / (a_ * (2 + 3 * c_))


def k_sc(a_, c_):
    if a_ <= 0 or a_ >= 2:
        return 0.0
    cs = math.sqrt(cs2(a_, c_))
    return math.sqrt(a_) * M_RED * (cs**1.5 if cs < 1 else cs**-0.5)


def lam_sc(a_, c_):
    return mp.sqrt(a_) * M_RED * mp.sqrt(cs2(mp.mpf(a_), mp.mpf(c_)))**mp.mpf(-0.5)


def alpha2(a_, c_):
    return -a_ * (2 * a_ * c_ + a_ - c_) / (c_ * (a_ - 2))


def alpha_rs(c_):
    lo, hi = mp.mpf('1e-30'), mp.mpf('1e-6')
    for _ in range(200):
        mid = mp.sqrt(lo * hi)
        if lam_sc(mid, c_) > LHL:
            hi = mid
        else:
            lo = mid
    return float(lo)


def gates(a_, c_, hierarchy, t1_verdict):
    g = {}
    g['G1'] = 0 < a_ < 2 and a_ != 0.5
    g['G2'] = a_ > 0
    g['G3'] = a_ < 0 or 0 < a_ < 0.5
    g['G4'] = k_sc(a_, c_) >= 1e3 * LHC
    g['G5'] = a_ >= AC_MIN * (1 - 1e-12)
    g['G6'] = abs(alpha2(a_, c_)) <= 1.6e-9
    g['G7'] = abs(4 * a_) <= 1.1e-5
    g['G8'] = AC_MIN * (1 - 1e-12) <= a_ <= AC_MAX and C2MIN * (1 - 1e-9) <= c_ <= C2MAX * (1 + 1e-9)
    g['G9'] = abs(a_) / 2 < 0.1
    g['G10'] = a_ < 2
    g['G11'] = (AC_MIN * (1 - 1e-12) <= a_ <= AC_MAX) if hierarchy else float(lam_sc(a_, c_)) <= LHL * (1 + 1e-12)
    g['G12'] = (a_ == 0 or AC_MIN * (1 - 1e-12) <= a_ <= 1e-3) and t1_verdict != 'FAILS'
    return g


# K7, K8
ars = {c_: alpha_rs(c_) for c_ in (0.007288800437803914, 0.0383350090957384, 0.050553607913275844, 0.06666666666666665)}
okK7 = abs(ars[0.06666666666666665] / 1.1783e-13 - 1) < 1e-3 and ars[0.0383350090957384] >= AC_MIN and \
    ars[0.050553607913275844] >= AC_MIN and ars[0.007288800437803914] < AC_MIN
check('K7 alpha_rs(c_2) reproduces CFG467/CFG320 (1.1783e-13 at c_2 = 0.0667; the sliver open at the three grid points c_2 >= '
      '0.038 and closed at c_2 = 7.29e-3)', ', '.join(f'{c_:.4e}: {v:.4e}' for c_, v in ars.items()), okK7)
g467 = J467['table']
# compare G4 lower edge and G6 island position and G11 edge at c_2 = 0.0667 with CFG467's committed strings
lo4 = mp.mpf('1e-30')
hi4 = mp.mpf(0.0667) / (1 + 2 * mp.mpf(0.0667))
for _ in range(300):
    mid = mp.sqrt(lo4 * hi4)
    if k_sc(float(mid), 0.06666666666666665) >= 1e3 * LHC:
        hi4 = mid
    else:
        lo4 = mid
edge4 = float(hi4)
isl = 0.06666666666666665 / (1 + 2 * 0.06666666666666665)
ref4 = float(g467['G4']['by_c2']['6.6667e-02']['A_str'].split(',')[0].strip('['))
ref6 = float(g467['G6']['by_c2']['6.6667e-02']['A_str'].split('U')[1].split(',')[0].strip(' ['))
ref11 = float(g467['G11']['by_c2']['6.6667e-02']['A_str'].split(',')[1].strip(' ]'))
okK8 = abs(edge4 / ref4 - 1) < 1e-4 and abs(isl / ref6 - 1) < 1e-5 and abs(ars[0.06666666666666665] / ref11 - 1) < 1e-4
check('K8 the re-implemented gates reproduce CFG467\'s committed sets at c_2 = 0.0667 (G4 lower edge, G6 island, G11 edge)',
      f'G4 {edge4:.5e} vs {ref4:.5e}; G6 island {isl:.6f} vs {ref6:.6f}; G11 {ars[0.06666666666666665]:.5e} vs {ref11:.5e}', okK8)
# the sliver's lower c_2 edge
lo_c, hi_c = 0.0073, 0.0667
for _ in range(100):
    mid = (lo_c + hi_c) / 2
    if alpha_rs(mid) >= AC_MIN:
        hi_c = mid
    else:
        lo_c = mid
c2_edge = hi_c
P(f'    the no-constant sliver opens at c_2 >= {c2_edge:.5f} (alpha_rs(c_2) = 9.624e-14 there)')
C2_CHOSEN = [c2_edge * (1 + 1e-9), 0.0383350090957384, 0.050553607913275844, 0.06666666666666665]
t1v = OUT['test1']['verdict']
win = {}
any_ok = False
for c_ in C2_CHOSEN:
    top = min(alpha_rs(c_), AC_MAX)
    grid = [AC_MIN * (top / AC_MIN)**(i / 6) for i in range(7)] if top >= AC_MIN else []
    rows = []
    for a_ in grid:
        g = gates(a_, c_, False, t1v)
        rows.append((a_, g))
    allp = [a_ for a_, g in rows if all(g.values())]
    gh = [gates(a_, c_, True, t1v) for a_ in [AC_MIN * (AC_MAX / AC_MIN)**(i / 8) for i in range(9)]]
    allh = all(all(g.values()) for g in gh)
    # alpha-independent rows at this c_2
    track = c_ >= C2MIN * (1 - 1e-9)
    leafG = True                 # leaf-average branch: |G_cos/G_N - 1| = alpha/2 ~ 1e-13
    plain = 1.5 * c_
    gw = True                    # beta = 0
    cass = True                  # alpha-independent (CFG357)
    s_c = [pt['splus'] for pt in POINTS if abs(pt['c2'] - c_) / c_ < 1e-6]
    s_ok = all(0.5 < s_ < 1 for s_ in s_c) if s_c else None
    win[f'{c_:.5f}'] = dict(alpha_rs=alpha_rs(c_), sliver=[AC_MIN, top] if grid else None,
                           all_gate_alphas=[f'{a_:.4e}' for a_ in allp], n_grid=len(grid),
                           failing={f'{a_:.3e}': [k_ for k_, v in g.items() if not v] for a_, g in rows},
                           hierarchy_window_all_pass=allh, tracking_floor=track, cosmoG_leaf_average=leafG,
                           plain_branch_1p5c2=plain, plain_branch_excluded_by_L350=plain > 1.5 * 2.95e-3,
                           gw170817=gw, cassini=cass, test1_splus_in_window=s_ok)
    ok_here = bool(allp) and track and leafG
    any_ok = any_ok or ok_here
    P(f'    c_2 {c_:.5f}: sliver {["%.4e" % AC_MIN, "%.4e" % top] if grid else "EMPTY"}; all gates pass at {len(allp)}/{len(grid)} grid '
      f'alphas; hierarchy window [9.624e-14, 3.2e-9] all gates: {allh}; tracking floor {track}; cosmological G: leaf-average '
      f'branch passes, plain branch 1.5 c_2 = {plain:.3f} vs L350 ceilings (c_2 <= 2.9e-3) EXCLUDED; test-(1) s+ at this c_2 '
      f'{s_c} in (1/2, 1): {s_ok}')
T3 = 'PASSES' if any_ok else 'FAILS'
OUT['test3'] = dict(verdict=T3, c2_sliver_edge=c2_edge, per_c2=win,
                    condition='the sliver needs the leaf-average branch of the lambda term (L350 G5); the plain branch is '
                              'excluded at every c_2 >= 7.3e-3 by Planck-era cosmology')
P(f'    (3) {T3}  (condition: the leaf-average branch of the lambda term, as in L340/CFG467\'s window)')

# MUTATE M1
m1 = {}
if MUTATE:
    banner('MUTATE M1: alpha_c outside the window must fail (3)')
    for a_, c_, hier in ((1e-11, 0.06666666666666665, False), (1e-6, 0.06666666666666665, True)):
        g = gates(a_, c_, hier, t1v)
        failing = [k_ for k_, v in g.items() if not v]
        m1[f'{a_:.0e}, c2 {c_:.4f}, hierarchy {hier}'] = failing
        P(f'    alpha {a_:.0e}, c_2 {c_:.4f}, hierarchy {hier}: failing gates {failing} -> all-gate set at this point EMPTY: {bool(failing)}')
    OUT['mutate_M1'] = m1
    # injection s = 0.3
    inj = {'h_exps': {'A': (2.3, 'pow')}, 'curv_exps': {'dR': (0.3 - 1, 'pow')}, 'riem_min': (0.3 - 1, 'pow'),
           'feedback_S_exp': None, 'exponent_shift': None}
    fake = {'splus': 0.3, 'modes': {'s+': inj}}
    w_inj = score_point(fake, 's+')
    P(f'    injection s = 0.3 (curvature x^-0.7): weak {w_inj[0]}; fails {w_inj[2]}')
    OUT['mutate_injection'] = {'weak': w_inj[0], 'fails': w_inj[2]}

# ================================================================================================ footing, verdict
banner('K9 and the verdict')
check('K9 a0 enters no computation: the windows and exponents are identical under both footing labels (bookkeeping)',
      f'footings {FOOTINGS}: no a0 in any formula', True)
if MUTATE:
    T2v = (OUT['test2'] or {}).get('verdict_frozen', 'not re-run')
else:
    T2v = OUT['test2']['verdict_frozen']
fails = [n for n, v in (('(1)', T1), ('(2)', T2v), ('(3)', T3)) if v == 'FAILS']
partial = [n for n, v in (('(1)', T1), ('(2)', T2v), ('(3)', T3)) if v in ('PARTIAL', 'UNDECIDED', 'not re-run')]
if fails:
    VERD = 'A WEAKENED (' + ', '.join(fails) + ' FAILS)'
elif partial:
    VERD = 'A NOT DECIDED (open: ' + ', '.join(partial) + ')'
else:
    VERD = 'A STRENGTHENED'
if not MUTATE:
    T2c = OUT['test2']['verdict_corrected_reading']
    fails_c = [n for n, v in (('(1)', T1), ('(2)', T2c), ('(3)', T3)) if v == 'FAILS']
    part_c = [n for n, v in (('(1)', T1), ('(2)', T2c), ('(3)', T3)) if v in ('PARTIAL', 'UNDECIDED')]
    VERD_C = ('A WEAKENED (' + ', '.join(fails_c) + ')') if fails_c else (('A NOT DECIDED (open: ' + ', '.join(part_c) + ')')
                                                                        if part_c else 'A STRENGTHENED')
    OUT['verdict_corrected_reading'] = VERD_C
P(f'    test (1): {T1}   test (2): {T2v}   test (3): {T3}')
P(f'    VERDICT (frozen rule): {VERD}')
if not MUTATE:
    P(f'    verdict under the dated correction of clauses 2a(ii)/(iii) (post-hoc, reported separately): {OUT["verdict_corrected_reading"]}')
OUT['verdict'] = VERD
OUT['checks'] = CHECKS
nlb = [k_ for k_, v in CHECKS.items() if v['load_bearing'] and not v['ok']]
if MUTATE:
    flips = {'M1 all-gate set empty at both outside points': all(bool(v) for v in m1.values()),
             'M2 strong branch s- fails test (1)': T1 == 'FAILS',
             'injection s = 0.3 fails': not OUT['mutate_injection']['weak']}
    OUT['mutate_flips'] = flips
    for k_, v in flips.items():
        P(f'    MUTATE flip {k_}: {v}')
    rc = 1
else:
    rc = 0 if not nlb else 1
OUT['load_bearing_failures'] = nlb
OUT['runtime_s'] = time.time() - T0
P(f'    load-bearing control failures: {nlb or "none"};  runtime {OUT["runtime_s"]:.0f}s;  rc {rc}')
P('    kappa = 1/2 is FITTED; no dark-matter particle; the cold mass is still required; chassis only (B has no action);')
P('    not "theory closed".')


def _js(o):
    if isinstance(o, (mp.mpf,)):
        return float(o)
    if isinstance(o, (LGS, GS)):
        return None
    return str(o)


with open(OUT_JSON, 'w') as f:
    json.dump(OUT, f, indent=1, default=_js)
with open(OUT_TXT, 'w') as f:
    f.write('\n'.join(LINES) + '\n')
sys.exit(rc)
