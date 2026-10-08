#!/usr/bin/env python3
"""CFG499 library: a second-order (in eps) Lagrangian engine for khronometric gravity
    L = sqrt(-g) [ R - lambda K^2 + alpha a.a ]      (16 pi G = 1, signature -+++, beta = 0)
with g = g0 + eps g1 and T = T0 + eps T1. Every quantity is a truncated series (c0, c1, c2) in eps.
No khronon terms need Christoffel symbols: u_m = -N d_m T, N = (-g^{ab} dT dT)^(-1/2), K = (1/sqrt-g) d_m(sqrt-g u^m),
a_m = h_m^n d_n ln N. R is built from the Christoffel symbols of the truncated metric.
"""
import sympy as sp

ORDER = 2


def s_add(*xs):
    return tuple(sum(x[i] for x in xs) for i in range(ORDER + 1))


def s_scale(c, a):
    return tuple(c * a[i] for i in range(ORDER + 1))


def s_mul(a, b):
    return tuple(sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(ORDER + 1))


def s_const(c):
    return (c,) + (0,) * ORDER


def s_func(a, f0, f1, f2):
    """f(a) for a series a with f, f', f'' evaluated at a0 (given as callables on a0)."""
    a0, a1, a2 = a
    return (f0(a0), f1(a0) * a1, f1(a0) * a2 + f2(a0) * a1**2 / 2)


def s_inv(a):
    return s_func(a, lambda z: 1 / z, lambda z: -1 / z**2, lambda z: 2 / z**3)


def s_pow(a, p):
    return s_func(a, lambda z: z**p, lambda z: p * z**(p - 1), lambda z: p * (p - 1) * z**(p - 2))


def s_log(a):
    return s_func(a, lambda z: sp.log(z), lambda z: 1 / z, lambda z: -1 / z**2)


def s_diff(a, x):
    return tuple(sp.diff(a[i], x) for i in range(ORDER + 1))


def s_simp(a, f=None):
    f = f or (lambda z: z)
    return tuple(f(z) for z in a)


class Geometry:
    """g0 (Matrix), g1 (Matrix) on coordinates X. Builds inverse, sqrt(-g), Christoffels and R as eps-series."""

    def __init__(self, X, g0, g1, sqrtg0, simp=None):
        self.X = X
        n = len(X)
        self.n = n
        self.simp = simp or (lambda z: z)
        g0i = g0.inv()
        g0i = g0i.applyfunc(sp.simplify)
        M = g0i * g1
        gi1 = -M * g0i
        gi2 = M * M * g0i
        self.g = [[(g0[i, j], g1[i, j], 0) for j in range(n)] for i in range(n)]
        self.gi = [[(g0i[i, j], gi1[i, j], gi2[i, j]) for j in range(n)] for i in range(n)]
        trM = M.trace()
        trM2 = (M * M).trace()
        self.sqrtg = (sqrtg0, sqrtg0 * trM / 2, sqrtg0 * (trM**2 / 8 - trM2 / 4))

    def christoffel(self):
        n, X = self.n, self.X
        dg = [[[s_diff(self.g[i][j], X[k]) for k in range(n)] for j in range(n)] for i in range(n)]
        G = [[[None] * n for _ in range(n)] for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for c in range(b, n):
                    acc = s_const(0)
                    for d in range(n):
                        if all(z == 0 for z in self.gi[a][d]):
                            continue
                        comb = s_add(dg[d][b][c], dg[d][c][b], s_scale(-1, dg[b][c][d]))
                        acc = s_add(acc, s_mul(self.gi[a][d], comb))
                    acc = s_scale(sp.Rational(1, 2), acc)
                    G[a][b][c] = acc
                    G[a][c][b] = acc
        self.G = G
        return G

    def ricci_scalar(self):
        n, X = self.n, self.X
        G = self.G if hasattr(self, 'G') else self.christoffel()
        Ric = [[None] * n for _ in range(n)]
        trG = [s_add(*[G[a][a][b] for a in range(n)]) for b in range(n)]
        for m in range(n):
            for v in range(m, n):
                acc = s_const(0)
                for a in range(n):
                    acc = s_add(acc, s_diff(G[a][m][v], X[a]))
                acc = s_add(acc, s_scale(-1, s_diff(trG[m], X[v])))
                for b in range(n):
                    acc = s_add(acc, s_mul(trG[b], G[b][m][v]))
                    for a in range(n):
                        acc = s_add(acc, s_scale(-1, s_mul(G[a][v][b], G[b][m][a])))
                Ric[m][v] = acc
                Ric[v][m] = acc
        R = s_const(0)
        for m in range(n):
            for v in range(n):
                if all(z == 0 for z in self.gi[m][v]):
                    continue
                R = s_add(R, s_mul(self.gi[m][v], Ric[m][v]))
        self.Ric = Ric
        return R

    def riemann_down(self):
        """R_abcd (all indices down) as eps-series, independent components a<b, c<d, (a,b)<=(c,d)."""
        n, X = self.n, self.X
        G = self.G if hasattr(self, 'G') else self.christoffel()
        out = {}
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
        Rud = {}
        for a in range(n):
            for b in range(n):
                for (c, d) in pairs:
                    acc = s_add(s_diff(G[a][d][b], X[c]), s_scale(-1, s_diff(G[a][c][b], X[d])))
                    for e_ in range(n):
                        acc = s_add(acc, s_mul(G[a][c][e_], G[e_][d][b]), s_scale(-1, s_mul(G[a][d][e_], G[e_][c][b])))
                    Rud[(a, b, c, d)] = acc
        for i, (a, b) in enumerate(pairs):
            for (c, d) in pairs[i:]:
                acc = s_const(0)
                for e_ in range(n):
                    if all(z == 0 for z in self.g[a][e_]):
                        continue
                    acc = s_add(acc, s_mul(self.g[a][e_], Rud[(e_, b, c, d)]))
                out[(a, b, c, d)] = acc
        return out

    def kretschmann(self):
        """R_abcd R^abcd as an eps-series (needs christoffel())."""
        n, X = self.n, self.X
        G = self.G if hasattr(self, 'G') else self.christoffel()
        Rud = {}
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(c + 1, n):
                        acc = s_add(s_diff(G[a][d][b], X[c]), s_scale(-1, s_diff(G[a][c][b], X[d])))
                        for e_ in range(n):
                            acc = s_add(acc, s_mul(G[a][c][e_], G[e_][d][b]), s_scale(-1, s_mul(G[a][d][e_], G[e_][c][b])))
                        Rud[(a, b, c, d)] = acc
                        Rud[(a, b, d, c)] = s_scale(-1, acc)
        g, gi = self.g, self.gi
        Rdn = {}
        for (a, b, c, d), v in Rud.items():
            acc = s_const(0)
            for e_ in range(n):
                if all(z == 0 for z in g[a][e_]):
                    continue
                acc = s_add(acc, s_mul(g[a][e_], Rud[(e_, b, c, d)]))
            Rdn[(a, b, c, d)] = acc
        Rup = {}
        for (a, b, c, d) in Rdn:
            acc = s_const(0)
            for p_ in range(n):
                if all(z == 0 for z in gi[a][p_]):
                    continue
                for q in range(n):
                    if all(z == 0 for z in gi[b][q]):
                        continue
                    for r_ in range(n):
                        if all(z == 0 for z in gi[c][r_]):
                            continue
                        for t in range(n):
                            if all(z == 0 for z in gi[d][t]):
                                continue
                            if (p_, q, r_, t) not in Rdn:
                                continue
                            acc = s_add(acc, s_mul(s_mul(gi[a][p_], gi[b][q]), s_mul(gi[c][r_], s_mul(gi[d][t], Rdn[(p_, q, r_, t)]))))
            Rup[(a, b, c, d)] = acc
        Kr = s_const(0)
        for k_, v in Rdn.items():
            Kr = s_add(Kr, s_mul(v, Rup[k_]))
        return Kr

    def khronon(self, Tser=None, dT=None, N0=None):
        """Tser = (T0, T1, 0), or dT = list of gradient series. Returns K, a.a, N, u_m, u^m, a_m as series.
        N0: optional closed form of the background lapse (-g0^{ab} dT0 dT0)^(-1/2), used instead of the generic power."""
        n, X = self.n, self.X
        if dT is None:
            dT = [s_diff(Tser, x) for x in X]
        n2 = s_const(0)
        for i in range(n):
            for j in range(n):
                if all(z == 0 for z in self.gi[i][j]):
                    continue
                n2 = s_add(n2, s_mul(self.gi[i][j], s_mul(dT[i], dT[j])))
        n2 = s_scale(-1, n2)
        if N0 is None:
            N = s_pow(n2, sp.Rational(-1, 2))
        else:
            N = (N0, -N0**3 * n2[1] / 2, -N0**3 * n2[2] / 2 + sp.Rational(3, 8) * N0**5 * n2[1]**2)
        self.n2 = n2
        ud = [s_scale(-1, s_mul(N, d)) for d in dT]
        uu = [s_add(*[s_mul(self.gi[i][j], ud[j]) for j in range(n)]) for i in range(n)]
        div = s_const(0)
        for i in range(n):
            div = s_add(div, s_diff(s_mul(self.sqrtg, uu[i]), X[i]))
        K = s_mul(div, s_inv(self.sqrtg))
        lnN = s_log(N) if N0 is None else (sp.log(N0), N[1] / N0, N[2] / N0 - N[1]**2 / (2 * N0**2))
        dl = [s_diff(lnN, x) for x in X]
        udl = s_add(*[s_mul(uu[i], dl[i]) for i in range(n)])
        ad = [s_add(dl[i], s_mul(ud[i], udl)) for i in range(n)]
        a2 = s_const(0)
        for i in range(n):
            for j in range(n):
                if all(z == 0 for z in self.gi[i][j]):
                    continue
                a2 = s_add(a2, s_mul(self.gi[i][j], s_mul(ad[i], ad[j])))
        return K, a2, N, ud, uu, ad


# ================================================================================================ the l = 1 BH sector
FIELDS = ('A', 'B', 'C', 'D', 'E', 'Kf', 'F')


def _red_s(p, cc, ss):
    p = sp.Poly(sp.expand(p), ss)
    ev, od = 0, 0
    for (k,), co in p.terms():
        if k % 2 == 0:
            ev += co * (1 - cc**2)**(k // 2)
        else:
            od += co * (1 - cc**2)**(k // 2)
    return sp.expand(ev), sp.expand(od)


def angint(coef, cc, ss):
    """int_0^pi coef(cos, sin) dtheta, for coef = sin(theta) x (polynomial in cos) / (polynomial in cos)."""
    t = sp.together(coef / ss)
    num, den = sp.fraction(t)
    nev, nod = _red_s(num, cc, ss)
    dev, dod = _red_s(den, cc, ss)
    assert dod == 0 and nod == 0, 'odd powers of sin(theta) survive'
    pc = sp.Poly(nev, cc)
    while dev.has(cc):
        fac = [ff for ff, mm in sp.factor_list(dev)[1] if ff.has(cc)][0]
        q, rem = sp.div(pc, sp.Poly(fac, cc))
        assert rem.is_zero, 'non-polynomial angular dependence'
        pc = q
        dev = sp.cancel(dev / fac)
    return sp.integrate(pc.as_expr(), (cc, -1, 1)) / dev


def derive_curvature_l1():
    """Linear (O(eps)) Ricci scalar, Kretschmann and every independent Riemann component R_abcd (EF coordinate basis,
    regular across the UH) for the l = 1 metric perturbation, as expressions in the jets A0.. Kf2, r and theta."""
    global ORDER
    old = ORDER
    ORDER = 1
    try:
        V, r, th, ph = sp.symbols('V r theta phi')
        X = [V, r, th, ph]
        e = 1 - 2 / r
        fs = [sp.Function(n)(r) for n in FIELDS[:6]]
        A, B, C, D, E, Kf = fs
        c, s = sp.cos(th), sp.sin(th)
        g0 = sp.Matrix([[-e, 1, 0, 0], [1, 0, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * s**2]])
        g1 = sp.Matrix([[A * c, B * c, -D * s, 0], [B * c, C * c, -E * s, 0], [-D * s, -E * s, r**2 * Kf * c, 0],
                        [0, 0, 0, r**2 * s**2 * Kf * c]])
        G = Geometry(X, g0, g1, r**2 * s)
        Rs = G.ricci_scalar()
        Kr = G.kretschmann()
        Rd = G.riemann_down()
    finally:
        ORDER = old

    def alg(ex):
        for k in (3, 2, 1):
            ex = ex.subs({f.diff(r, k): sp.Symbol(f'{n}{k}') for n, f in zip(FIELDS[:6], fs)})
        return ex.subs({f: sp.Symbol(f'{n}0') for n, f in zip(FIELDS[:6], fs)})
    res = {'K0': sp.simplify(Kr[0]), 'dR': sp.simplify(alg(Rs[1]) / c), 'dKr': sp.simplify(alg(Kr[1]) / c),
           'riem': {k: alg(v[1]) for k, v in Rd.items() if v[1] != 0}}
    return res, (r, th)


def derive_l1(log=print):
    """Angle-integrated quadratic Lagrangian of sqrt(-g)[R - lambda K^2 + alpha a.a] for the O(v), l = 1 even
    perturbation (A, B, C, D, E, Kf; F) of Schwarzschild (ingoing EF, M = 1) with the static khronon written through
    Y(r): H' = -1/(Y(Y+W)), W = sqrt(Y^2 - e), lapse N0 = Y.
    Returns dict part -> {(jet_a, jet_b): coefficient} with jets 'A0', 'A1', ..., 'F2' and coefficients in the symbols
    r, Y, W, Y1, Y2 (Y1 = Y', Y2 = Y''); also the O(eps) K and a.a at h = 0 (for control K2)."""
    import time
    t0 = time.time()
    V, r, th, ph = sp.symbols('V r theta phi')
    X = [V, r, th, ph]
    e = 1 - 2 / r
    fs = [sp.Function(n)(r) for n in FIELDS]
    A, B, C, D, E, Kf, F = fs
    c, s = sp.cos(th), sp.sin(th)
    g0 = sp.Matrix([[-e, 1, 0, 0], [1, 0, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * s**2]])
    g1 = sp.Matrix([[A * c, B * c, -D * s, 0], [B * c, C * c, -E * s, 0], [-D * s, -E * s, r**2 * Kf * c, 0],
                    [0, 0, 0, r**2 * s**2 * Kf * c]])
    G = Geometry(X, g0, g1, r**2 * s)
    R = G.ricci_scalar()
    Yf = sp.Function('Y')(r)
    Wf = sp.sqrt(Yf**2 - e)
    P1 = -1 / (Yf * (Yf + Wf))
    dT = [(1, 0, 0), (P1, sp.diff(F, r) * c, 0), (0, -F * s, 0), (0, 0, 0)]
    K, a2, N, ud, uu, ad = G.khronon(dT=dT, N0=Yf)
    chk = sp.simplify(G.n2[0] * Yf**2)
    assert chk == 1, chk
    log(f'      [derive] geometry + khronon series built {time.time() - t0:.1f}s')
    Ys, Ws, Y1, Y2, Y3 = sp.symbols('Y W Y1 Y2 Y3')
    cc, ss = sp.symbols('c s')
    jet = {}
    for n, f in zip(FIELDS, fs):
        for k in (3, 2, 1, 0):
            jet[(n, k)] = sp.Symbol(f'{n}{k}')

    def alg(ex):
        for k in (3, 2, 1):
            ex = ex.subs({f.diff(r, k): jet[(n, k)] for n, f in zip(FIELDS, fs)})
        ex = ex.subs({f: jet[(n, 0)] for n, f in zip(FIELDS, fs)})
        ex = ex.subs({Yf.diff(r, 3): Y3}).subs({Yf.diff(r, 2): Y2}).subs({Yf.diff(r): Y1}).subs({Yf: Ys})
        ex = ex.subs(sp.sqrt(Ys**2 - e), Ws)
        ex = ex.subs({sp.sin(2 * th): 2 * s * c, sp.cos(2 * th): 2 * c**2 - 1, sp.cot(th): c / s, sp.tan(th): s / c})
        return ex.subs({c: cc, s: ss})
    out = {}
    parts = {'EH': s_mul(G.sqrtg, R)[2], 'KK': s_mul(G.sqrtg, s_mul(K, K))[2], 'AA': s_mul(G.sqrtg, a2)[2]}
    for nm, ex in parts.items():
        t1 = time.time()
        ex = sp.expand(alg(ex))
        syms = sorted([z for z in ex.free_symbols if z in jet.values()], key=str)
        P = sp.Poly(ex, *syms)
        d = {}
        for mon, co in P.terms():
            assert sum(mon) == 2, 'not quadratic'
            idx = [syms[i] for i, m in enumerate(mon) for _ in range(m)]
            key = tuple(sorted(str(z) for z in idx))
            val = sp.factor(sp.cancel(angint(co, cc, ss)))
            if val != 0:
                d[key] = d.get(key, 0) + val
        out[nm] = d
        log(f'      [derive] {nm}: {len(d)} bilinear terms, {time.time() - t1:.1f}s')
    # O(eps) K and a.a at h = 0, per cos(theta)
    zero = {f: 0 for f in fs[:6]}
    K1 = alg(K[1].subs(zero) / c)
    A1 = alg(a2[1].subs(zero) / c)
    K0 = alg(K[0]); A0 = alg(a2[0])
    return out, {'K1': K1, 'A1': A1, 'K0': K0, 'A0': A0}, (r, Ys, Ws, Y1, Y2, Y3)


def derive_l1_PN(log=print):
    """As derive_l1, but with the static khronon kept as two free radial functions P = H'(r) and N0 = lapse(r)
    (identity N0^-2 = -2P - eP^2 imposed afterwards). Jets: P0, P1, P2 (P, P', P''), N0, N1, N2. Faster and exact."""
    import time
    t0 = time.time()
    V, r, th, ph = sp.symbols('V r theta phi')
    X = [V, r, th, ph]
    e = 1 - 2 / r
    fs = [sp.Function(n)(r) for n in FIELDS]
    A, B, C, D, E, Kf, F = fs
    c, s = sp.cos(th), sp.sin(th)
    g0 = sp.Matrix([[-e, 1, 0, 0], [1, 0, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * s**2]])
    g1 = sp.Matrix([[A * c, B * c, -D * s, 0], [B * c, C * c, -E * s, 0], [-D * s, -E * s, r**2 * Kf * c, 0],
                    [0, 0, 0, r**2 * s**2 * Kf * c]])
    G = Geometry(X, g0, g1, r**2 * s)
    R = G.ricci_scalar()
    Pf = sp.Function('P')(r)
    Nf = sp.Function('N')(r)
    dT = [(1, 0, 0), (Pf, sp.diff(F, r) * c, 0), (0, -F * s, 0), (0, 0, 0)]
    K, a2, N, ud, uu, ad = G.khronon(dT=dT, N0=Nf)
    n20 = sp.expand(G.n2[0])
    log(f'      [derive-PN] series built {time.time() - t0:.1f}s; n2_0 = {n20}')
    cc, ss = sp.symbols('c s')
    P0, P1, P2, N0s, N1, N2 = sp.symbols('P0 P1 P2 N0 N1 N2')
    jet = {}
    for n, f in zip(FIELDS, fs):
        for k in (3, 2, 1, 0):
            jet[(n, k)] = sp.Symbol(f'{n}{k}')

    def alg(ex):
        for k in (3, 2, 1):
            ex = ex.subs({f.diff(r, k): jet[(n, k)] for n, f in zip(FIELDS, fs)})
        ex = ex.subs({f: jet[(n, 0)] for n, f in zip(FIELDS, fs)})
        ex = ex.subs({Pf.diff(r, 2): P2, Nf.diff(r, 2): N2}).subs({Pf.diff(r): P1, Nf.diff(r): N1})
        ex = ex.subs({Pf: P0, Nf: N0s})
        ex = ex.subs({sp.sin(2 * th): 2 * s * c, sp.cos(2 * th): 2 * c**2 - 1, sp.cot(th): c / s, sp.tan(th): s / c})
        return ex.subs({c: cc, s: ss})
    out = {}
    parts = {'KK': s_mul(G.sqrtg, s_mul(K, K))[2], 'AA': s_mul(G.sqrtg, a2)[2], 'EH': s_mul(G.sqrtg, R)[2]}
    for nm, ex in parts.items():
        t1 = time.time()
        ex = sp.expand(alg(ex))
        log(f'      [derive-PN] {nm} expanded ({len(ex.args)} terms) {time.time() - t1:.1f}s')
        syms = sorted([z for z in ex.free_symbols if z in jet.values()], key=str)
        Pl = sp.Poly(ex, *syms)
        d = {}
        for mon, co in Pl.terms():
            assert sum(mon) == 2, 'not quadratic'
            idx = [syms[i] for i, m in enumerate(mon) for _ in range(m)]
            key = tuple(sorted(str(z) for z in idx))
            val = sp.factor(sp.cancel(angint(co, cc, ss)))
            if val != 0:
                d[key] = d.get(key, 0) + val
        out[nm] = d
        log(f'      [derive-PN] {nm}: {len(d)} bilinear terms, {time.time() - t1:.1f}s')
    zero = {f: 0 for f in fs[:6]}
    ops = {'K1': alg(K[1].subs(zero) / c), 'A1': alg(a2[1].subs(zero) / c), 'K0': alg(K[0]), 'A0': alg(a2[0])}
    return out, ops, (r, P0, P1, P2, N0s, N1, N2)


# ================================================================================================ generalized series
import mpmath as mp


class GS:
    """x^sigma * sum_{k} c[k] x^(v + k), k = 0..N-1 (sigma non-integer offset, v integer valuation). mp coefficients.
    Laurent series (sigma = 0) for the background; fields carry sigma."""
    N = 16
    ZTOL = mp.mpf('1e-32')
    XS = mp.mpf(1)      # x = XS * xi: the series variable is xi (O(1) coefficients inside a boundary layer of width XS)

    def __init__(self, c, v=0, sigma=0):
        c = [mp.mpf(z) if not isinstance(z, mp.mpf) else z for z in list(c)[:GS.N]]
        self.c = c + [mp.mpf(0)] * (GS.N - len(c))
        self.v = v
        self.sigma = sigma

    @staticmethod
    def const(a):
        return GS([a])

    @staticmethod
    def x():
        return GS([GS.XS], 1)

    def scale(self):
        return max([abs(z) for z in self.c] + [mp.mpf(0)])

    def strip(self):
        """drop leading coefficients that vanish to ZTOL relative (exact cancellations in mp arithmetic)."""
        s = self.scale()
        if s == 0:
            return GS([0], self.v, self.sigma)
        k = 0
        while k < GS.N - 1 and abs(self.c[k]) <= GS.ZTOL * s:
            k += 1
        return GS(self.c[k:], self.v + k, self.sigma)

    def _co(self, o):
        return o if isinstance(o, GS) else GS.const(o)

    def __add__(self, o):
        if isinstance(o, LGS):
            return o + self
        o = self._co(o)
        if self.scale() == 0:
            return o
        if o.scale() == 0:
            return self
        assert abs(self.sigma - o.sigma) < 1e-30, 'adding different sigma sectors'
        v = min(self.v, o.v)
        c = [mp.mpf(0)] * GS.N
        for k in range(GS.N):
            i = self.v + k - v
            if i < GS.N:
                c[i] += self.c[k]
            j = o.v + k - v
            if j < GS.N:
                c[j] += o.c[k]
        return GS(c, v, self.sigma)
    __radd__ = __add__

    def __neg__(self):
        return GS([-z for z in self.c], self.v, self.sigma)

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        if isinstance(o, LGS):
            return o * self
        if not isinstance(o, GS):
            return GS([z * o for z in self.c], self.v, self.sigma)
        a, b = self.c, o.c
        return GS([mp.fsum(a[i] * b[k - i] for i in range(k + 1)) for k in range(GS.N)], self.v + o.v,
                  self.sigma + o.sigma)
    __rmul__ = __mul__

    def inv(self):
        s = self.strip()
        assert s.sigma == 0
        a = s.c
        assert a[0] != 0
        b = [1 / a[0]]
        for k in range(1, GS.N):
            b.append(-mp.fsum(a[i] * b[k - i] for i in range(1, k + 1)) / a[0])
        return GS(b, -s.v, 0)

    def __truediv__(self, o):
        if not isinstance(o, GS):
            return GS([z / o for z in self.c], self.v, self.sigma)
        return self * o.inv()

    def __rtruediv__(self, o):
        return self._co(o) * self.inv()

    def __pow__(self, p):
        p = int(p) if float(p).is_integer() else p
        if isinstance(p, int):
            if p < 0:
                return self.inv() ** (-p)
            res, base = GS.const(1), self
            while p:
                if p & 1:
                    res = res * base
                base = base * base
                p >>= 1
            return res
        if abs(float(p) - 0.5) < 1e-15:
            return gs_sqrt(self)
        raise ValueError(p)

    def deriv(self):
        c = [(self.sigma + self.v + k) * self.c[k] / GS.XS for k in range(GS.N)]
        return GS(c, self.v - 1, self.sigma)

    def lead(self):
        s = self.strip()
        return s.v + s.sigma, s.c[0]

    def __call__(self, xv):
        return xv**self.sigma * mp.fsum(self.c[k] * xv**(self.v + k) for k in range(GS.N))


def gs_sqrt(s):
    s = s.strip()
    assert s.v % 2 == 0 and s.sigma == 0
    a = s.c
    b = [mp.sqrt(a[0])]
    for k in range(1, GS.N):
        b.append((a[k] - mp.fsum(b[i] * b[k - i] for i in range(1, k))) / (2 * b[0]))
    return GS(b, s.v // 2, 0)


def lam_gs(expr, args):
    return sp.lambdify(args, expr, modules=[{'sqrt': gs_sqrt}, 'mpmath'])


class LGS:
    """a + ln(x) b with a, b GS of the same sigma sector (log extension for resonant integer sectors)."""

    def __init__(self, a, b=None):
        self.a = a
        self.b = b if b is not None else GS([0], a.v, a.sigma)

    def __add__(self, o):
        if isinstance(o, LGS):
            return LGS(self.a + o.a, self.b + o.b)
        return LGS(self.a + o, self.b)
    __radd__ = __add__

    def __neg__(self):
        return LGS(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        if isinstance(o, LGS):
            raise ValueError('LGS x LGS not needed (linear theory)')
        return LGS(self.a * o, self.b * o)
    __rmul__ = __mul__

    def __truediv__(self, o):
        return LGS(self.a / o, self.b / o)

    def deriv(self):
        return LGS(self.a.deriv() + self.b * GS([1 / GS.XS], -1, 0), self.b.deriv())

    def scale(self):
        return max(self.a.scale(), self.b.scale())


def el_equations(M, fields, which=None):
    """Euler-Lagrange expressions E_n = sum_k (-D)^k dL/d(n_k) for L = sum M[(a, b)] j_a j_b, with M a dict of GS
    coefficients and fields a dict name -> GS or LGS. Jets missing from `fields` are zero."""
    jets = {}
    for n, s in fields.items():
        d = s
        for k in range(4):
            jets[f'{n}{k}'] = d
            d = d.deriv()
    names = which or list(dict.fromkeys([k[:-1] for kk in M for k in kk]))
    E = {}
    for n in names:
        tot = None
        for k in range(3):
            a = f'{n}{k}'
            acc = None
            for (p, q), m in M.items():
                if p != a and q != a:
                    continue
                other = q if p == a else p
                if other not in jets:
                    continue
                term = jets[other] * m * (2 if p == q else 1)
                acc = term if acc is None else acc + term
            if acc is None:
                continue
            for _ in range(k):
                acc = acc.deriv()
            if k % 2:
                acc = -acc
            tot = acc if tot is None else tot + acc
        E[n] = tot
    return E
