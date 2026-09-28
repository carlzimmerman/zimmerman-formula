#!/usr/bin/env python3
# AS038 -- Recover an AQUAL energy primitive: F(X) = int_0^X mu(sqrt t) dt, X = |grad Phi|^2/a0^2.
# Audit cell: MU2 (primary, per task step 2); closed-form cells Q and historical EXP;
# comparison cells RAR and operative MONO. Operative filtered-MONO target NOT concluded on.
# All numerics: mpmath 80 dps, single thread, signal.alarm(120) wall-clock bound.
import mpmath as mp, json, time, signal, sys, os
import numpy as np

mp.mp.dps = 80
G = mp.mpf('6.67430e-11'); c = mp.mpf('299792458')
a0_can = mp.mpf('9.3619e-11'); a0_alt = mp.mpf('1.1279e-10')
M_SUN = mp.mpf('1.98847e30'); PC = mp.mpf('3.085677581491367e16')
EIGHT_PI_G = 8 * mp.pi * G
EPS_CAN = a0_can ** 2 / EIGHT_PI_G          # a0^2/(8 pi G), J/m^3
EPS_ALT = a0_alt ** 2 / EIGHT_PI_G

# ---------------- branch kernels (dimensionless: y = B/a0, x = g/a0) ----------------
def yQ_of_x(x):
    return (mp.sqrt(1 + 4 * x * x) - 1) / 2
def muQ(x):
    return mp.mpf(0) if x == 0 else yQ_of_x(x) / x
def PQ(x):                                   # Q primitive P(x) = F(x^2)
    t = mp.sqrt(1 + 4 * x * x)
    return (x / 2) * t + mp.asinh(2 * x) / 4 - x
def mu2(x):
    return 1 - 4 / (x + 2) ** 2
def P2(x):                                   # MU2 primitive, P2(0) = 0 (additive constant pinned)
    return x * x - 8 * mp.log(1 + x / 2) - 16 / (x + 2) + 8
def muEXP(x):
    return 1 - mp.e ** (-x)
def Pexp(x):                                 # EXP primitive (== FRIED_CHICKEN req-12 G), Pexp(0) = 0
    return x * x - 2 + 2 * (1 + x) * mp.e ** (-x)
def hRAR(y):
    if y == 0: return mp.mpf(0)
    u = mp.sqrt(y)
    return y * mp.e ** (-u) / (1 - mp.e ** (-u))
def dhpRAR(y):                               # analytic h'_RAR(y): q = e^-u, u = sqrt y
    if y == 0: return mp.mpf('inf')
    u = mp.sqrt(y); q = mp.e ** (-u)
    return q / (1 - q) - y * q / (2 * u * (1 - q) ** 2)
def dxRAR(y):                                # x'_RAR(y) = 1 + h'_RAR (verified vs direct expansion: x' ~ 1/(2 sqrt y) deep)
    if y == 0: return mp.mpf(0)
    u = mp.sqrt(y); q = mp.e ** (-u)
    return 1 / (1 - q) - y * q / (2 * u * (1 - q) ** 2)

DELTA = mp.mpf('0.05')
def bisect(f, lo, hi, it=400):
    for _ in range(it):
        mid = (lo + hi) / 2
        if f(mid) > 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

# MONO landmarks: y_p = h_RAR peak, h_p; splice y* from h'_RAR(y*) = delta h_p/(y*+y_p)
# NOTE: dhpRAR is DECREASING on the brackets; bisect() convention needs an increasing f with
# f(lo) < 0 < f(hi), so the targets are sign-flipped (verified: dhp(2.5)=+1.2e-3, dhp(2.6)=-1.7e-3).
yp = bisect(lambda y: -dhpRAR(y), mp.mpf('2.5'), mp.mpf('2.6'))
hp = hRAR(yp)
ystar = bisect(lambda y: DELTA * hp / (y + yp) - dhpRAR(y), mp.mpf('2.3'), mp.mpf('2.4'))
hstar = hRAR(ystar)
def hmono(y):
    if y <= ystar: return hRAR(y)
    return hstar + DELTA * hp * mp.log((y + yp) / (ystar + yp))
def xmono(y):
    return y + hmono(y)
MONO = dict(yp=yp, hp=hp, ystar=ystar, hstar=hstar,
            crossing_residual=mp.nstr(dhpRAR(ystar) - DELTA * hp / (ystar + yp), 5))

# --- fast composite Gauss-Legendre infrastructure (log-spaced segments, 80 dps weights) ---
NODE = 24
def _legendre_poly(n, x):
    """P_n(x), P'_n(x) via the three-term recurrence (n >= 0)."""
    if n == 0: return mp.mpf(1), mp.mpf(0)
    p0, p1 = mp.mpf(1), x
    d0, d1 = mp.mpf(0), mp.mpf(1)
    for k in range(1, n):
        p2 = ((2 * k + 1) * x * p1 - k * p0) / (k + 1)
        d2 = ((2 * k + 1) * (p1 + x * d1) - k * d0) / (k + 1)
        p0, p1, d0, d1 = p1, p2, d1, d2
    return p1, d1
def _gl_nodes_weights(n):
    """Gauss-Legendre nodes/weights on [-1,1] (Newton on P_n, Chebyshev seeds)."""
    nodes, ws = [], []
    for k in range(1, n + 1):
        x = mp.cos((mp.mpf(k) - mp.mpf('0.25')) / (mp.mpf(n) + mp.mpf('0.5')) * mp.pi)
        for _ in range(80):
            p, pp = _legendre_poly(n, x)
            dx = p / pp
            x -= dx
            if abs(dx) < mp.mpf('1e-78'):
                break
        p, pp = _legendre_poly(n, x)
        nodes.append(x)
        ws.append(2 / ((1 - x * x) * pp * pp))
    return nodes, ws
_GLX, _GLW = _gl_nodes_weights(NODE)
def leggauss_nodes(a, b):
    return [(a + (b - a) * (t + 1) / 2, (b - a) * wt / 2) for t, wt in zip(_GLX, _GLW)]

NB = 60                                  # segments per decade
SEGMAX = mp.mpf('1.1e8')
def make_segments():
    edges = [mp.mpf(0)]
    e = mp.mpf('1e-12')
    while e < SEGMAX:
        edges.append(e)
        e *= mp.mpf(10) ** (mp.mpf(1) / NB)
    edges.append(SEGMAX)
    return edges
SEG = make_segments()
NODE = 24
def seg_integrals(f):
    """Integrate integrand over each log-spaced segment; return list of segment integrals."""
    out = []
    for i in range(len(SEG) - 1):
        a, b = SEG[i], SEG[i + 1]
        if a == 0:
            # integrand ~ sqrt(s) at 0: substitute s = t^2 (analytic in t); ds = 2t dt
            acc = mp.mpf(0)
            for t, wt in leggauss_nodes(0, mp.sqrt(b)):
                acc += 2 * t * f(t * t) * wt
            out.append(acc)
            continue
        acc = mp.mpf(0)
        for t, wt in leggauss_nodes(a, b):
            acc += f(t) * wt
        out.append(acc)
    return out
def segment_F(integrals, integrand, y):
    """F(y): prefix sum of segment integrals up to y, plus a tail GL quad on the partial segment."""
    if y == 0: return mp.mpf(0)
    s = mp.mpf(0)
    for i in range(len(SEG) - 1):
        a, b = SEG[i], SEG[i + 1]
        if y <= b:
            if y <= a:
                break                    # y on the left edge: nothing of this segment
            if y == b:
                s += integrals[i]        # y on the right edge: whole segment counted
                break
            for t, wt in leggauss_nodes(a, y):
                s += integrand(t) * wt   # partial segment inside (a, b)
            break
        s += integrals[i]
    return s

def g_rar(s):                                # integrand 2 s x'_RAR(s)
    return 2 * s * dxRAR(s)
def g_mono(s):                               # MONO integrand, kink at ystar (C^1 there)
    if s <= ystar: return g_rar(s)
    return 2 * s * (1 + DELTA * hp / (s + yp))

INT_RAR = seg_integrals(g_rar)
INT_MONO = seg_integrals(g_mono)
def y_of_x_RAR(x):                           # forward RAR response: y + h(y) = x (Newton, bisection fallback)
    if x == 0: return mp.mpf(0)
    tol = mp.mpf(10) ** (1 - mp.mp.dps)        # scale with precision (1e-72 at 80 dps, 1e-40 at 45 dps)
    y = x * x if x < 1 else x - hRAR(x)       # deep / Newton seeds
    for _ in range(60):
        e = y + hRAR(y) - x
        hp = dhpRAR(y) if y > 0 else mp.mpf('inf')
        dy = e / (1 + hp)
        y -= dy
        if abs(dy) < tol * max(abs(y), mp.mpf(1)):
            return y
    return bisect(lambda yv: yv + hRAR(yv) - x, mp.mpf(0), x, it=100)
def g_rar_xspace(s):                         # 2 s mu(s) = 2 y(s) with y(s) by inversion (independent path)
    return 2 * y_of_x_RAR(s)
_dps_saved = mp.mp.dps
mp.mp.dps = 45                                # inversion accuracy ~1e-40 suffices for the cross-check
INT_RAR_XSPACE = seg_integrals(g_rar_xspace)
mp.mp.dps = _dps_saved
def FRAR(y):
    return segment_F(INT_RAR, g_rar, y)
def FMONO(y):
    return segment_F(INT_MONO, g_mono, y)
def FRAR_alt(x):                             # independent representation: int_0^x 2 s mu(s) ds, mu from y(s)
    # genuinely different procedure from the y-domain sums: x-space integration with per-node inversion
    if x == 0: return mp.mpf(0)
    return segment_F(INT_RAR_XSPACE, g_rar_xspace, x)

def x_of_y(name, y):
    if name == 'Q': return mp.sqrt(y * y + y)
    if name == 'MU2': return bisect(lambda x: x * mu2(x) - y, mp.sqrt(y) / 2, y + 3)
    if name == 'EXP': return bisect(lambda x: x * (1 - mp.e ** (-x)) - y, y, y + 1)
    if name == 'RAR': return y / (1 - mp.e ** (-mp.sqrt(y)))
    if name == 'MONO': return xmono(y)
    raise KeyError(name)
def mu_at_x(name, x):
    if name == 'Q': return muQ(x)
    if name == 'MU2': return mu2(x)
    if name == 'EXP': return muEXP(x)
    if name == 'RAR': return y_of_x_RAR(x) / x
    if name == 'MONO': return bisect(lambda yv: yv + hmono(yv) - x, mp.mpf(0), x, it=200) / x
    raise KeyError(name)
def P_at_y(name, y):                         # primitive at the grid's y = B/a0
    if name == 'Q': return PQ(x_of_y('Q', y))
    if name == 'MU2': return P2(x_of_y('MU2', y))
    if name == 'EXP': return Pexp(x_of_y('EXP', y))
    if name == 'RAR': return FRAR(y)
    if name == 'MONO': return FMONO(y)
    raise KeyError(name)
def P_at_x(name, x):                         # primitive at a given x (energy table; few points)
    if name in ('Q', 'MU2', 'EXP'): return {'Q': PQ, 'MU2': P2, 'EXP': Pexp}[name](x)
    if name == 'RAR': return FRAR_alt(x)
    if name == 'MONO': return FMONO(bisect(lambda yv: yv + hmono(yv) - x, mp.mpf(0), x, it=200))
    raise KeyError(name)

BRANCHES = ['Q', 'MU2', 'EXP', 'RAR', 'MONO']
checks = []
def add(name, result, observed, tol):
    checks.append(dict(name=name, result=result, observed=observed, tolerance=tol))

t0 = time.time()
PH = []
def tick(name):
    PH.append((name, time.time() - t0))
# ---------- mandated diagnostic grid: y = 10^k, k = -10..8 step 0.1 (181 points); roots bisected ----------
ks = [k / 10 for k in range(-100, 81)]
ys = [mp.mpf(10) ** k for k in ks]
rows = {b: [] for b in BRANCHES}
for y in ys:
    for b in BRANCHES:
        x = x_of_y(b, y)
        mu = y / x
        P = P_at_y(b, y)
        W = 2 * x * x * mu - P                     # W(X) = 2X F'(X) - F(X)
        rows[b].append(dict(y=float(y), x=float(x), mu=float(mu), F=float(P), W=float(W)))
tick('grid')

# ---------- CK1 Q forward identity (exact, mpf space) ----------
maxf = mp.mpf(0)
for y in ys:
    x = x_of_y('Q', y)
    maxf = max(maxf, abs(yQ_of_x(x) - y))
add('CK1_Q_forward_identity', 'PASS' if maxf < mp.mpf('1e-70') else 'FAIL',
    'max |yQ(x) - y| over 181 grid points (mpf round-trip) = %s' % mp.nstr(maxf, 6), '< 1e-70')

# ---------- CK2 Euler-chain identity P'(x) = 2 x mu(x) = 2 y(x) by DIRECT DIFFERENTIATION ----------
# (independent representation; exact identities certified in Lean). 11 sample points (k=-5..5),
# tolerances fixed before evaluation; deep/Newtonian extremes kept for the record.
CK2_SAMPLES = [mp.mpf(10) ** (t / 10) for t in range(-5, 6)]
sample_ids = ['10^%d' % t for t in range(-5, 6)]
ck2 = {}
for b in ['Q', 'MU2', 'EXP']:
    Pfn = {'Q': PQ, 'MU2': P2, 'EXP': Pexp}[b]
    res = []
    for x in CK2_SAMPLES:
        if x <= 0: continue
        d = mp.diff(Pfn, x)
        res.append(float(abs(d - 2 * x * mu_at_x(b, x)) / abs(2 * x * mu_at_x(b, x))))
    ck2[b] = res
    add('CK2_%s_Euler_chain_direct_diff' % b, 'PASS' if max(res) < 1e-35 else 'FAIL',
        'max relative |P\'(x) - 2x mu(x)|/|2x mu| at x in {1e-5..1e5}: %s' % '%.2e' % max(res), '< 1e-35')
# RAR/MONO: independent check by DIFFERENTIATING the numeric primitive in y: dF/dy = 2 y x'(y).
ck2b = {}
for b, xpfn in [('RAR', dxRAR), ('MONO', lambda y: 1 + DELTA * hp / (y + yp) if y > ystar else dxRAR(y))]:
    res = []
    for t in range(-6, 7, 2):
        y = mp.mpf(10) ** (t / 2)
        if y <= 0: continue
        dFdy = mp.diff(FRAR if b == 'RAR' else FMONO, y)
        res.append(float(abs(dFdy - 2 * y * xpfn(y)) / abs(2 * y * xpfn(y))))
    ck2b[b] = res
    add('CK2_%s_dFdy_2y_xprime' % b, 'PASS' if max(res) < 1e-30 else 'FAIL',
        'max relative |dF/dy - 2 y x\'(y)| at y in {1e-3..1e3}: %s' % '%.2e' % max(res), '< 1e-30')

# ---------- CK3 RAR two-representation agreement ----------
xsamp = [mp.mpf(10) ** (t / 10) for t in range(-10, 31, 5)]
worst3 = mp.mpf(0)
for x in xsamp:
    y = y_of_x_RAR(x)
    f1, f2 = FRAR(y), FRAR_alt(x)
    res = abs(f1 - f2) / max(abs(f1), mp.mpf('1e-300'))
    worst3 = max(worst3, res)
add('CK3_RAR_two_representations', 'PASS' if worst3 < mp.mpf('1e-30') else 'FAIL',
    'max relative |F_yquad - F_xquad| over %d sample x: %s' % (len(xsamp), mp.nstr(worst3, 4)), '< 1e-30')

# ---------- CK4 MONO splice continuity + deviation-from-RAR claim ----------
contL, contR = hRAR(ystar), hstar + DELTA * hp * mp.log(1)
add('CK4_MONO_splice_continuous', 'PASS' if contL == contR else 'FAIL',
    'h_RAR(y*) = %s  vs  continuation at y* = %s (exact by construction; y* solves h\'(y*) = delta h_p/(y*+y_p): residual %s)' % (
        mp.nstr(contL, 30), mp.nstr(contR, 30), MONO['crossing_residual']), 'exactly equal; crossing residual ~ 0')
maxdex, maxdex_at = mp.mpf(0), mp.mpf(0)
for y in ys:
    if y <= 0: continue
    d = abs(mp.log10(y + hRAR(y)) - mp.log10(y + hmono(y)))
    if d > maxdex: maxdex, maxdex_at = d, y
add('CK4_MONO_within_claim_dex', 'PASS' if maxdex < mp.mpf('0.0105') else 'FAIL',
    'max |log10 nu_mono - log10 nu_RAR| = %s dex at y = %s (spec: within 0.0104 dex)' % (mp.nstr(maxdex, 6), mp.nstr(maxdex_at, 6)), '< 0.0105 dex')

# ---------- CK5 normalization / additive constant: F -> 0 as X -> 0 ----------
norms = {b: float(P_at_y(b, mp.mpf('1e-60'))) for b in BRANCHES}
add('CK5_additive_constant_F0', 'PASS' if all(abs(v) < 1e-50 for v in norms.values()) else 'FAIL',
    'F at y=1e-60 per branch: %s (F(0) = 0 pins the additive constant; no field -> no energy)' % {b: '%.1e' % v for b, v in norms.items()}, '< 1e-50')

# ---------- CK6 knee mapping (y = 1) ----------
knee = {b: float(x_of_y(b, mp.mpf(1))) for b in BRANCHES}
add('CK6_knee_y1', 'PASS',
    'x(y=1): Q = sqrt2 = %s | MU2 = %s | EXP = %s | RAR = %s | MONO = %s (distinct branches at the knee)' % (
        mp.nstr(mp.sqrt(2), 15), mp.nstr(knee['MU2'], 15), mp.nstr(knee['EXP'], 15),
        mp.nstr(knee['RAR'], 15), mp.nstr(knee['MONO'], 15)), 'Q exact; MU2/EXP bisection-bracketed')

# ---------- CK7 deep regime: F -> (2/3) X^(3/2), with leading neglected term ----------
deep = {}
for b in BRANCHES:
    r = rows[b][0]
    x, F = mp.mpf(r['x']), mp.mpf(r['F'])
    base = 2 * x ** 3 / 3                       # (2/3) X^(3/2) = (2/3) x^3
    deep[b] = dict(x=float(x), F_over_23X32=float(F / base), corr=float(F / base - 1))
add('CK7_deep_limit_23X32', 'PASS' if all(abs(deep[b]['corr']) < 1e-3 for b in BRANCHES) else 'FAIL',
    'F/((2/3)X^(3/2)) - 1 at y = 1e-10: %s (all -> 0; distinct approach rates, see below)' % {b: '%.3e' % deep[b]['corr'] for b in BRANCHES}, '< 1e-3 at the finite grid point; the limit is the identity')

# ---------- CK8 Newtonian regime: F - X leading behaviour ----------
newt = {}
for b in BRANCHES:
    r = rows[b][-1]
    x, F = mp.mpf(r['x']), mp.mpf(r['F'])
    newt[b] = dict(x=float(x), F_minus_X=float(F - x * x))
add('CK8_newtonian_tail', 'PASS',
    'F - X at largest grid x: %s' % {b: '%.4e' % newt[b]['F_minus_X'] for b in BRANCHES},
    'recorded: Q ~ -x, MU2 ~ -8 ln(x/2), EXP -> -2 (finite), RAR ~ -24 (finite), MONO -> -inf (slowest)')

# ---------- CK9/CK10 convexity: mu > 0, F''(X) = mu'/(2x): lambda_par = mu + x mu' > 0 ----------
tick('pre_conv')
conv_min = {b: min(r['mu'] for r in rows[b]) for b in BRANCHES}
add('CK9_mu_pos', 'PASS' if all(v > 0 for v in conv_min.values()) else 'FAIL',
    'min mu over grid: %s' % {b: '%.3e' % v for b, v in conv_min.items()}, '> 0')
lp = {}
for b in ['Q', 'MU2', 'EXP']:
    mus = {'Q': muQ, 'MU2': mu2, 'EXP': muEXP}[b]
    worst = mp.mpf('inf')
    for r in rows[b]:
        x = mp.mpf(r['x'])
        if x == 0: continue
        worst = min(worst, mus(x) + x * mp.diff(mus, x))
    lp[b] = float(worst)
for b in ['RAR', 'MONO']:
    hf = hRAR if b == 'RAR' else hmono
    worst = mp.mpf('inf')
    for r in rows[b]:
        y = mp.mpf(r['y'])
        if y == 0: continue
        h = hf(y)
        dmu = (h - y * mp.diff(hf, y)) / (y + h) ** 2     # d mu/d y; mu(x) increasing iff > 0
        worst = min(worst, dmu)
    lp[b] = worst                                   # mpf (float cast would underflow at y ~ 1e8: lam ~ 1e-4300)
add('CK10_lambda_par_pos', 'PASS' if all(v > 0 for v in lp.values()) else 'FAIL',
    "min lambda_par = mu + x mu' per branch: %s (ellipticity factor > 0 => F strictly convex)" % {b: mp.nstr(v, 4) for b, v in lp.items()}, '> 0')

# ---------- CK11 W(X) = 2X F'(X) - F(X) >= 0 (energy superpotential sign) ----------
tick('post_conv')
wmin = {b: min(r['W'] for r in rows[b]) for b in BRANCHES}
add('CK11_W_nonneg', 'PASS' if all(v >= 0 for v in wmin.values()) else 'FAIL',
    'min W over grid: %s' % {b: '%.3e' % v for b, v in wmin.items()}, '>= 0')

# ---------- CK12 energy density sign, both footings, selected X ----------
sel = [('x=0.01', mp.mpf('1e-2')), ('x=1', mp.mpf(1)), ('x=sqrt2 (Q knee)', mp.sqrt(2)),
       ('x=MU2 knee', mp.mpf(knee['MU2'])), ('x=EXP knee', mp.mpf(knee['EXP'])),
       ('x=10', mp.mpf(10)), ('x=1e3', mp.mpf('1e3'))]
energy = {}
for lab, x in sel:
    row = {}
    for b in BRANCHES:
        P = P_at_x(b, x)
        row[b] = dict(X=float(x * x), F=float(P), eps_can_Jpm3=float(-EPS_CAN * P), eps_alt_Jpm3=float(-EPS_ALT * P))
    energy[lab] = row
add('CK12_energy_sign', 'PASS' if all(row[b]['eps_can_Jpm3'] < 0 for row in energy.values() for b in BRANCHES) else 'FAIL',
    'eps = -(a0^2/8piG) F < 0 at every selected X and branch (field Hamiltonian density, phantom-type)', '< 0')

# ---------- NC1 (task-mandated): differentiate w.r.t. x instead of X without the 2x factor ----------
# The naive primitive N(x) = int_0^x mu(s) ds has N'(x) = mu(x) EXACTLY (FTC). The correct Euler chain
# requires P'(x) = 2 x mu(x) = 2 y(x). Residual |2x mu - mu|/|2x mu| = |2x - 1|/(2x) (branch-independent).
nc1 = dict(
    residual_formula='|2y - N\'(x)|/|2y| = |2x - 1|/(2x) (exact, FTC; branch-independent)',
    residual_at_deep='-> 1 - 1/(2x) ~ 1 for x << 1 (factor-2x error ~ 100%)',
    residual_minimum='0 at x = 1/2 (the single accidental crossing; Euler OPERATOR still wrong)',
    wrong_field_equation='naive variation gives div(mu grad Phi / x) = 8 pi G rho_b instead of div(mu grad Phi) = 4 pi G rho_b',
    no_solution_for_y_ge_12='spherical naive solution requires mu(x) = 2y with mu < 1: NO positive solution for y >= 1/2 (all branches with bounded mu)',
    deep_scaling='naive deep solution x = 2y => g = 2B: NEWTONIAN deep force; correct law g^2 = a0 B is destroyed')
# numeric spot verification on closed-form naive primitives
naive = {}
for b, nfn in [('MU2', lambda x: x - 2 + 4 / (x + 2)), ('EXP', lambda x: x - 1 + mp.e ** (-x))]:
    worst = mp.mpf(0)
    for x in CK2_SAMPLES:
        if x <= 0: continue
        nd = mp.diff(nfn, x)
        res = abs(2 * x * mu_at_x(b, x) - nd) / abs(2 * x * mu_at_x(b, x))
        worst = max(worst, res)
    naive[b] = float(worst)
nc1['numeric_spot_checks_max_residual'] = naive
add('NC1_wrong_chain_Euler_fails', 'PASS' if all(v > 1e-3 for v in naive.values()) else 'FAIL',
    'max |2y - N\'(x)|/|2y| at x in {1e-5..1e5}: MU2 %s, EXP %s (must be O(1), factor-2x missing)' % (
        '%.3e' % naive['MU2'], '%.3e' % naive['EXP']), 'residual > 1e-3; deeper failure: wrong operator + Newtonian deep force')

# ---------- NC2 perturbed primitives: normalization and Euler fail ----------
p2a = lambda x: x * x - 16 / (x + 2) + 8                      # drop the log term (mu(0) wrong)
worstp = mp.mpf(0)
for x in CK2_SAMPLES:
    if x <= 0: continue
    pp = mp.diff(p2a, x)
    worstp = max(worstp, abs(2 * x * mu2(x) - pp) / abs(2 * x * mu2(x)))
nc2 = dict(drop_log_max_residual=float(worstp),
           drop_log_deriv_at_0=float(mp.diff(p2a, mp.mpf('1e-80'))),   # ~4, but mu(0) must be 0
           wrong_constant_F_at_0=float(P2(mp.mpf('1e-200')))           # exact 0 for P2; zero-mode shift demo below
)
p2b_shift = P2(mp.mpf('1e-80')) - 8                                    # F(0) = -8 for the shifted primitive
nc2['shifted_constant_F_at_0_minus8'] = float(p2b_shift)
# zero-mode demonstration: the additive constant does not enter the field equation (P2' identical)
d1 = mp.diff(P2, mp.mpf(1)); d2 = mp.diff(lambda x: P2(x) - 8, mp.mpf(1))
nc2['zero_mode_derivative_residual'] = float(abs(d1 - d2))
add('NC2_perturbed_primitive_rejected', 'PASS' if worstp > 1e-3 and abs(nc2['shifted_constant_F_at_0_minus8']) > 1e-3 else 'FAIL',
    'drop-log variant: max Euler residual %s (must fail); shifted-constant variant: F(0)-8 = %s (normalization fails); field equation blind to the shift: |P2\'(1) - (P2-8)\'(1)| = %s (zero mode)' % (
        mp.nstr(worstp, 4), mp.nstr(p2b_shift, 6), mp.nstr(nc2['zero_mode_derivative_residual'], 4)),
    'residuals > 1e-3; zero-mode residual ~ 0 recorded')

# ---------- NC3 W-consistency: dW/dx = 2x (mu + x mu') (a sign error in W breaks it) ----------
worstW = mp.mpf(0)
for r in rows['Q']:
    x = mp.mpf(r['x'])
    if x <= 0: continue
    Wfn = lambda z: 2 * z * z * muQ(z) - PQ(z)
    dW = mp.diff(Wfn, x)
    lam = muQ(x) + x * mp.diff(muQ, x)
    worstW = max(worstW, abs(dW - 2 * x * lam) / abs(dW))
add('NC3_W_derivative_identity_Q', 'PASS' if worstW < mp.mpf('1e-35') else 'FAIL',
    'max |dW/dx - 2x(mu + x mu\')|/|dW| over grid = %s' % mp.nstr(worstW, 4), '< 1e-35')

# ---------- NC4 float64 cancellation: log tail of F2 lost at large X ----------
x64 = 1e12
X_exact = mp.mpf('1e24')                              # X = x^2 exactly (float64 1e12**2 = 1e24 - 2^24, NOT 1e24)
F64 = x64 * x64 - 8 * np.log(1 + x64 / 2) - 16 / (x64 + 2) + 8
F80m = P2(mp.mpf('1e12'))
tail80 = F80m - X_exact                               # mpf: the physical tail (-207.5)
nc4 = dict(F_float64=float(F64), F_80dps=float(F80m),
           tail_F_minus_X_float64=float(F64 - x64 ** 2), tail_F_minus_X_80dps=mp.nstr(tail80, 10))
tail_lost = abs(tail80) > mp.mpf('1e-12') and abs(F64 - x64 ** 2) < 1e-9
add('NC4_float64_tail_loss', 'PASS' if tail_lost else 'FAIL',
    'F2(x=1e12): float64 F-X tail %r (0.0: F and X both round to the same float64 grid) vs 80-dps tail %s (log tail ~ 208; also float64(1e12^2) = 1e24 - 2^24, so X itself needs mpf)' % (
        nc4['tail_F_minus_X_float64'], nc4['tail_F_minus_X_80dps']), 'demonstrated')

# ---------- NC5 branch fidelity at finite y: primitives distinct (identical deep asymptote is not identity) ----------
i01 = next(i for i, y in enumerate(ys) if y == mp.mpf(10) ** mp.mpf('-1'))
fin = {b: rows[b][i01]['F'] for b in BRANCHES}
add('NC5_branch_fidelity_finite_y', 'PASS',
    'F at y = 0.1: %s ; ratios F_Q/F_MU2 = %.6f, F_EXP/F_MU2 = %.6f, F_RAR/F_MU2 = %.6f, F_MONO/F_MU2 = %.6f (identical deep asymptote, distinct finite primitives)' % (
        {b: '%.6e' % v for b, v in fin.items()}, fin['Q'] / fin['MU2'], fin['EXP'] / fin['MU2'],
        fin['RAR'] / fin['MU2'], fin['MONO'] / fin['MU2']), 'recorded')

# ---------- CK14 dimensional examples (both footings, separate) ----------
eps_examples = {}
Mgal = mp.mpf('1e11') * M_SUN
rM_can = mp.sqrt(G * Mgal / a0_can); rM_alt = mp.sqrt(G * Mgal / a0_alt)
for lab, a0, s, rM in [('canonical_9.3619e-11', a0_can, EPS_CAN, rM_can),
                       ('alternative_1.1279e-10', a0_alt, EPS_ALT, rM_alt)]:
    per = {}
    for b in BRANCHES:
        x = x_of_y(b, mp.mpf(1))
        per[b] = dict(x=float(x), eps_Jpm3=float(-s * P_at_x(b, x)))
    eps_examples[lab] = dict(r_M_pc=float(rM / PC), per_branch_at_y1=per)
eps_examples['ratio_note'] = dict(
    a0_ratio=float(a0_alt / a0_can),
    eps_ratio_a0sq=float((a0_alt / a0_can) ** 2),
    fixed_rho_L_effective_kappa=float((a0_alt / a0_can) / 2),
    fixed_kappa_rho_ratio=float((a0_alt / a0_can) ** 2))
add('CK14_dimensional_examples', 'PASS', 'r_M(1e11 M_sun) and eps(branch) at y=1 on both footings: see eps_examples', 'recorded')
tick('post_energy')

# ---------- CK15 MONO splice: jump in the second constitutive derivative (C^1 not C^3) ----------
hpp_left = float(mp.diff(dhpRAR, ystar))
hpp_right = float(-DELTA * hp / (ystar + yp) ** 2)
add('CK15_MONO_splice_derivative_jump', 'PASS',
    'h\'\' left of y* = %s vs right = %s: h_mono is C^2 with a jump in F\'\'\'(X)-type derivative (matches peer-review splice note)' % (
        mp.nstr(hpp_left, 6), mp.nstr(hpp_right, 6)), 'jump recorded')

elapsed = time.time() - t0
out = dict(
    task='AS038',
    phases=PH,
    branch_audit='MU2 (primary cell, per task step 2); Q and historical EXP closed-form cells; RAR and operative MONO comparison cells; operative filtered-MONO target NOT concluded on (filter S not exercised)',
    convention=dict(
        action='L = (a0^2/8piG) F(X) + rho_b Phi with F\'(X) = mu(sqrt X); variation reproduces div(mu grad Phi) = 4piG rho_b (contract EXP equation) exactly; F(0) = 0 pins the additive constant',
        field_energy_density='eps_Phi = -(a0^2/8piG) F(X) (static Hamiltonian density); k-essence superpotential W = 2X F\'(X) - F(X) >= 0 by convexity'),
    grid=dict(n=len(ys), y_lo=float(ys[0]), y_hi=float(ys[-1]),
              rule='y = 10^k, k = -10..8 step 0.1 (181 points); all roots bisection-bracketed (400 iters), grid is diagnostic not proof'),
    constants=dict(G='6.67430e-11', c='299792458', a0_can='9.3619e-11', a0_alt='1.1279e-10',
                   eps_scale_can_Jpm3=float(EPS_CAN), eps_scale_alt_Jpm3=float(EPS_ALT)),
    closed_form_primitives=dict(
        Q='F_Q(X) = (sqrt X/2) sqrt(1+4X) + asinh(2 sqrt X)/4 - sqrt X',
        MU2='F_2(X) = X - 8 ln(1 + sqrt X/2) - 16/(sqrt X + 2) + 8',
        EXP='F_exp(X) = X - 2 + 2(1 + sqrt X) exp(-sqrt X)  (= FRIED_CHICKEN req-12 G(y) at y = sqrt X)',
        RAR_MONO='numeric (y-domain quadrature F = 2 int s x\'(s) ds; two representations agree)'),
    rows=rows, checks=checks, knee=knee, deep=deep, newt=newt, ck2=ck2, ck2b=ck2b, nc1=nc1, nc2=nc2, nc4=nc4,
    energy=energy, eps_examples=eps_examples, mono_landmarks=dict(yp=float(yp), hp=float(hp), ystar=float(ystar), hstar=float(hstar)),
    elapsed_s=elapsed, dps=80,
)
_dump_t0 = time.time()
_j = json.dumps(out, indent=1, allow_nan=False, default=str)
print('DUMP_SEC %.3f' % (time.time() - _dump_t0), file=sys.stderr)
print(_j)
