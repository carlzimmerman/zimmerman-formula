#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG469 option B library: the slowly moving black hole of the khronon (test-khronon limit, as CFG319) with ONE
lowest-order Horava-type UV operator added, and the local (Frobenius / Newton-polygon) analysis of the resulting
order-6 Euler-Lagrange equation at the universal horizon (UH) and at infinity.
Criteria: campaign_fresh_gravity/CFG469_chassis_options/FROZEN_CRITERIA.md (fd00569e9).

Khronon on fixed Schwarzschild, ingoing EF (v, r, theta, phi), M = 1:
    T = v + H(r) + eps F(r) cos(theta),  H' = -1/(Y (Y + W)),  W = sqrt(Y^2 - e),  e = 1 - 2/r
    L = sqrt(-g) [ -lambda K^2 + alpha a.a + UV ]
    arm 'A':  UV = + alpha * epsUV * (D_m a^m)^2,      D_m a^m = grad_m a^m - a.a
    arm 'K':  UV = - lambda * epsUV * h^{mn} d_m K d_n K,  h^{mn} = g^{mn} + u^m u^n
epsUV = 1/(M_* r_g)^2. The radius is eliminated with r = 2/(1 - Y^2 + W^2) (exact on the khronon background), so every
coefficient is a rational function of (Y0, Y1, ..., W, cos, sin). Perturbations are carried as jets: order-0
expression, order-1 linear form in f_k = F^(k), order-2 quadratic form.
"""
import math
import sympy as sp

Ys = sp.symbols('Y0:9')
Y0 = Ys[0]
Wsym = sp.Symbol('W', positive=True)
cS, sS = sp.symbols('c s')
al, la, epsUV = sp.symbols('alpha lambda epsilon_UV', positive=True)
fs = sp.symbols('f0:9')
R_OF = 2 / (1 - Y0**2 + Wsym**2)          # r on the background
E_OF = Y0**2 - Wsym**2                    # e = 1 - 2/r
WP = (Y0 * Ys[1] - (1 - Y0**2 + Wsym**2)**2 / 4) / Wsym   # dW/dr from W^2 = Y^2 - 1 + 2/r


def red_s(ex):
    """reduce powers of sin: s^2 -> 1 - c^2 (s only appears polynomially in numerators)"""
    ex = sp.together(ex)
    num, den = sp.fraction(ex)
    num = sp.expand(num)
    if num.has(sS):
        p = sp.Poly(num, sS)
        out = 0
        for (k,), cc in p.terms():
            out += cc * (1 - cS**2)**(k // 2) * sS**(k % 2)
        num = sp.expand(out)
    return num / den


def simp(ex):
    if ex == 0:
        return sp.Integer(0)
    return sp.cancel(red_s(ex))


def Dr0(ex):
    """total r-derivative of a background coefficient (function of Y_k, W, c, s)"""
    out = sp.diff(ex, Wsym) * WP
    for k in range(len(Ys) - 1):
        if ex.has(Ys[k]):
            out += sp.diff(ex, Ys[k]) * Ys[k + 1]
    return out


def Dth0(ex):
    return -sS * sp.diff(ex, cS) + cS * sp.diff(ex, sS)


class J:
    """jet: c0 + eps * sum_k c1[k] f_k + eps^2 * sum_{i<=j} c2[(i,j)] f_i f_j"""
    __slots__ = ('c0', 'c1', 'c2')

    def __init__(self, c0=0, c1=None, c2=None):
        self.c0 = sp.sympify(c0)
        self.c1 = dict(c1 or {})
        self.c2 = dict(c2 or {})

    def map(self, fn):
        return J(fn(self.c0), {k: fn(v) for k, v in self.c1.items()}, {k: fn(v) for k, v in self.c2.items()})

    def simp(self):
        o = self.map(simp)
        o.c1 = {k: v for k, v in o.c1.items() if v != 0}
        o.c2 = {k: v for k, v in o.c2.items() if v != 0}
        return o

    def __add__(self, o):
        o = o if isinstance(o, J) else J(o)
        c1 = dict(self.c1)
        for k, v in o.c1.items():
            c1[k] = c1.get(k, 0) + v
        c2 = dict(self.c2)
        for k, v in o.c2.items():
            c2[k] = c2.get(k, 0) + v
        return J(self.c0 + o.c0, c1, c2)
    __radd__ = __add__

    def __neg__(self):
        return self.map(lambda z: -z)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, J) else J(o)))

    def __rsub__(self, o):
        return J(o) - self

    def __mul__(self, o):
        if not isinstance(o, J):
            o = sp.sympify(o)
            return self.map(lambda z: z * o)
        c1 = {}
        for k, v in self.c1.items():
            c1[k] = c1.get(k, 0) + v * o.c0
        for k, v in o.c1.items():
            c1[k] = c1.get(k, 0) + v * self.c0
        c2 = {}
        for k, v in self.c2.items():
            c2[k] = c2.get(k, 0) + v * o.c0
        for k, v in o.c2.items():
            c2[k] = c2.get(k, 0) + v * self.c0
        for i, vi in self.c1.items():
            for j, vj in o.c1.items():
                key = (min(i, j), max(i, j))
                c2[key] = c2.get(key, 0) + vi * vj
        return J(self.c0 * o.c0, c1, c2)
    __rmul__ = __mul__

    def inv(self):
        """1/self, needs c0 != 0"""
        a0 = self.c0
        c1 = {k: -v / a0**2 for k, v in self.c1.items()}
        c2 = {k: -v / a0**2 for k, v in self.c2.items()}
        for i, vi in self.c1.items():
            for j, vj in self.c1.items():
                if i <= j:
                    key = (i, j)
                    fac = 1 if i == j else 2
                    c2[key] = c2.get(key, 0) + fac * vi * vj / a0**3
        return J(1 / a0, c1, c2)

    def __truediv__(self, o):
        if not isinstance(o, J):
            return self * (1 / sp.sympify(o))
        return self * o.inv()

    def Dr(self):
        c1 = {}
        for k, v in self.c1.items():
            c1[k] = c1.get(k, 0) + Dr0(v)
            c1[k + 1] = c1.get(k + 1, 0) + v
        c2 = {}
        for (i, j), v in self.c2.items():
            c2[(i, j)] = c2.get((i, j), 0) + Dr0(v)
            k1 = (min(i + 1, j), max(i + 1, j)); c2[k1] = c2.get(k1, 0) + v
            k2 = (min(i, j + 1), max(i, j + 1)); c2[k2] = c2.get(k2, 0) + v
        return J(Dr0(self.c0), c1, c2)

    def Dth(self):
        return self.map(Dth0)


def inv_sqrt(n2):
    """n2^(-1/2) for a jet whose background n2.c0 = 1/Y0^2 (Y0 > 0 outside the UH)"""
    a0 = n2.c0
    z1 = {k: v / a0 for k, v in n2.c1.items()}
    z2 = {k: v / a0 for k, v in n2.c2.items()}
    c1 = {k: -v / 2 for k, v in z1.items()}
    c2 = {k: -v / 2 for k, v in z2.items()}
    for i, vi in z1.items():
        for j, vj in z1.items():
            if i <= j:
                fac = 1 if i == j else 2
                c2[(i, j)] = c2.get((i, j), 0) + sp.Rational(3, 8) * fac * vi * vj
    return J(Y0, {k: Y0 * v for k, v in c1.items()}, {k: Y0 * v for k, v in c2.items()})


def build(arm=None, log=print):
    """returns dict with jets K, a2, Da, DK2 and the angle-integrated quadratic form M[(i,j)]"""
    rr, ee = R_OF, E_OF
    Hp = -1 / (Y0 * (Y0 + Wsym))
    dTv = J(1)
    dTr = J(Hp, {1: cS})
    dTt = J(0, {0: -sS})
    n2 = -(2 * dTv * dTr + ee * dTr * dTr + dTt * dTt / rr**2)
    n2 = n2.simp()
    assert simp(n2.c0 * Y0**2 - 1) == 0, n2.c0
    N = inv_sqrt(n2).simp()
    uv, ur, ut = -N * dTv, (-N * dTr).simp(), (-N * dTt).simp()
    Uv, Ur, Ut = ur, (uv + ee * ur).simp(), (ut / rr**2).simp()
    # K = (1/r^2) d_r (r^2 u^r) + (1/s) d_th (s u^th)
    K = ((rr**2 * Ur).Dr() / rr**2 + Ut.Dth() + (Ut * (cS / sS))).simp()
    log('      [uv_bh] K built')
    Ninv = N.inv().simp()
    dlr = (N.Dr() * Ninv).simp()
    dlt = (N.Dth() * Ninv).simp()
    udl = (Ur * dlr + Ut * dlt).simp()
    av, ar, at = (uv * udl).simp(), (dlr + ur * udl).simp(), (dlt + ut * udl).simp()
    Av, Ar, At = ar, (av + ee * ar).simp(), (at / rr**2).simp()
    a2 = (av * Av + ar * Ar + at * At).simp()
    log('      [uv_bh] a.a built')
    out = {'K': K, 'a2': a2, 'N': N, 'ur': ur, 'Ur': Ur, 'Ut': Ut}
    L = rr**2 * (-la * K * K + al * a2)
    if arm == 'A':
        divA = ((rr**2 * Ar).Dr() / rr**2 + At.Dth() + At * (cS / sS)).simp()
        Da = (divA - a2).simp()
        out['Da'] = Da
        log('      [uv_bh] D.a built')
        L = L + rr**2 * al * epsUV * Da * Da
    elif arm == 'K':
        Kr, Kt = K.Dr().simp(), K.Dth().simp()
        hrr = (ee + Ur * Ur).simp(); hrt = (Ur * Ut).simp(); htt = (1 / rr**2 + Ut * Ut).simp()
        DK2 = (hrr * Kr * Kr + 2 * hrt * Kr * Kt + htt * Kt * Kt).simp()
        out['DK2'] = DK2
        log('      [uv_bh] (DK)^2 built')
        L = L - rr**2 * la * epsUV * DK2
    M = {}
    for key, v in L.c2.items():
        vv = sp.expand(sp.numer(sp.together(red_s(v))))
        den = sp.denom(sp.together(red_s(v)))
        assert not den.has(cS) and not den.has(sS), key
        assert not vv.has(sS), ('odd sin power', key)
        Ic = sp.integrate(sp.Poly(vv, cS).as_expr(), (cS, -1, 1))
        M[key] = sp.factor(sp.cancel(Ic / den))
        log(f'      [uv_bh] M{key} integrated')
    out['M'] = M
    return out


def falling(s, k):
    out = sp.Integer(1)
    for q in range(k):
        out *= (s - q)
    return out


# ------------------------------------------------------------------------------------------- numeric Laurent series
import mpmath as mp


class LS:
    """truncated Laurent series sum_{n=val}^{val+N-1} c[n-val] t^n with mpmath coefficients"""
    __slots__ = ('val', 'c', 'N')

    def __init__(self, val, c, N):
        self.val, self.N = val, N
        c = list(c)[:N]
        self.c = c + [mp.mpf(0)] * (N - len(c))

    @staticmethod
    def const(a, N):
        return LS(0, [mp.mpf(a)], N)

    def norm(self, tol):
        """drop leading coefficients that are zero to tolerance (relative to the largest), shifting val"""
        big = max([abs(z) for z in self.c] + [mp.mpf(0)])
        k = 0
        while k < self.N and abs(self.c[k]) <= tol * big:
            k += 1
        if k == self.N:
            return LS(self.val + self.N, [], self.N)
        return LS(self.val + k, self.c[k:], self.N - k)

    def __add__(self, o):
        if not isinstance(o, LS):
            o = LS.const(o, self.N)
        v = min(self.val, o.val)
        top = min(self.val + self.N, o.val + o.N)
        n = top - v
        c = [mp.mpf(0)] * n
        for k in range(n):
            p = v + k
            if self.val <= p < self.val + self.N:
                c[k] += self.c[p - self.val]
            if o.val <= p < o.val + o.N:
                c[k] += o.c[p - o.val]
        return LS(v, c, n)
    __radd__ = __add__

    def __neg__(self):
        return LS(self.val, [-z for z in self.c], self.N)

    def __sub__(self, o):
        return self + (-o if isinstance(o, LS) else LS.const(-o, self.N))

    def __mul__(self, o):
        if not isinstance(o, LS):
            o = mp.mpf(o) if not isinstance(o, mp.mpc) else o
            return LS(self.val, [z * o for z in self.c], self.N)
        n = min(self.N, o.N)
        c = [mp.mpf(0)] * n
        for i in range(n):
            ai = self.c[i]
            if ai == 0:
                continue
            for j in range(n - i):
                c[i + j] += ai * o.c[j]
        return LS(self.val + o.val, c, n)
    __rmul__ = __mul__

    def inv(self, tol):
        s = self.norm(tol)
        a0 = s.c[0]
        n = s.N
        b = [mp.mpf(0)] * n
        b[0] = 1 / a0
        for k in range(1, n):
            acc = mp.mpf(0)
            for j in range(1, k + 1):
                acc += s.c[j] * b[k - j]
            b[k] = -acc / a0
        return LS(-s.val, b, n)

    def deriv(self):
        """d/dt"""
        c = [(self.val + k) * self.c[k] for k in range(self.N)]
        return LS(self.val - 1, c, self.N)

    def lead(self, tol):
        s = self.norm(tol)
        if s.N == 0:
            return None, mp.mpf(0)
        return s.val, s.c[0]

    def coeff(self, p):
        k = p - self.val
        return self.c[k] if 0 <= k < self.N else mp.mpf(0)


TOL = mp.mpf('1e-45')


def series_point(kind, N, bg=None):
    """background series. kind 'uh': t = x = r - r_U (stealth unless bg gives y-list/W0); kind 'inf': t = z = 1/r.
    returns (dict Ys[k], W -> LS, derivative operator d/dr on LS, info)"""
    if kind == 'uh':
        NN = N + 10
        if bg is None:
            # stealth: Y = (2r - 3) sqrt(4r^2 + 4r + 3)/(4 r^2), r = 3/2 + x, built with series arithmetic (no numerics)
            two_x = LS(1, [2], NN)
            rad = LS(0, [18, 16, 4], NN)
            r2 = LS(0, [mp.mpf(9) / 4, 3, 1], NN)
            Yser0 = two_x * _ls_sqrt(rad) * (r2 * 4).inv(TOL)
            yc = [Yser0.coeff(k) for k in range(NN)]
            rU = mp.mpf(3) / 2
        else:
            yc = ([mp.mpf(0)] + [mp.mpf(z) for z in bg['y']] + [mp.mpf(0)] * NN)[:NN]
            rU = mp.mpf(bg['rU'])
        Yser = LS(0, yc, NN)
        dr = lambda s: s.deriv()
        # W^2 = Y^2 - 1 + 2/(rU + x)
        inv_r = LS(0, [(-1)**k / rU**(k + 1) for k in range(NN)], NN)
        W2 = Yser * Yser + (-1) + inv_r * 2
        w2c = W2.c
        # sqrt of a series with nonzero constant term
        W = _ls_sqrt(W2)
        sub = {Ys[0]: Yser}
        cur = Yser
        for k in range(1, len(Ys)):
            cur = dr(cur)
            sub[Ys[k]] = cur
        sub[Wsym] = W
        return sub, dr, {'rU': rU, 'y1': yc[1], 'W0': W.c[0] if W.val == 0 else None}
    if kind == 'inf':
        C = 3 * mp.sqrt(3) / 4 if bg is None else mp.mpf(bg['C'])
        # Y = sqrt(1 - 2 z + C^2 z^4)
        inner = LS(0, [1, -2, 0, 0, C**2], N + 10)
        Yser = _ls_sqrt(inner)
        W = LS(2, [C], N + 10)
        dr = lambda s: _mul_z2(s.deriv()) * (-1)      # d/dr = -z^2 d/dz
        sub = {Ys[0]: Yser}
        cur = Yser
        for k in range(1, len(Ys)):
            cur = dr(cur)
            sub[Ys[k]] = cur
        sub[Wsym] = W
        return sub, dr, {'C': C}
    raise ValueError(kind)


def _mul_z2(s):
    return LS(s.val + 2, s.c, s.N)


def _ls_sqrt(s):
    s = s.norm(TOL)
    assert s.val % 2 == 0
    a0 = s.c[0]
    n = s.N
    b = [mp.mpf(0)] * n
    b[0] = mp.sqrt(a0)
    for k in range(1, n):
        acc = s.c[k]
        for j in range(1, k):
            acc -= b[j] * b[k - j]
        b[k] = acc / (2 * b[0])
    return LS(s.val // 2, b, n)


_GENS = list(Ys[:8]) + [Wsym]


def eval_ls(ex, sub, N, cache):
    """evaluate a rational function of (Y_k, W) (no other symbols) on the background series"""
    num, den = sp.fraction(sp.together(ex))
    return _eval_poly(num, sub, N, cache) * _eval_poly(den, sub, N, cache).inv(TOL)


def _eval_poly(p, sub, N, cache):
    p = sp.expand(p)
    if p.is_number:
        assert p.is_Rational, p
        return LS.const(mp.mpf(int(p.p)) / int(p.q), N)
    P = sp.Poly(p, *_GENS)
    acc = None
    for mon, co in P.terms():
        assert co.is_Rational, co
        term = LS.const(mp.mpf(int(co.p)) / int(co.q), N)
        for g, e in zip(_GENS, mon):
            if e:
                key = (str(g), e)
                if key not in cache:
                    base = sub[g]
                    pw = LS.const(1, base.N)
                    for _ in range(e):
                        pw = pw * base
                    cache[key] = pw
                term = term * cache[key]
        acc = term if acc is None else acc + term
    return acc


def split_couplings(ex):
    """ex linear in the couplings alpha, lambda, alpha*eps, lambda*eps -> dict coupling-key -> background expression"""
    ex = sp.expand(sp.numer(sp.together(ex))) / sp.denom(sp.together(ex))
    out = {}
    e1 = sp.expand(sp.numer(sp.together(ex)))
    den = sp.denom(sp.together(ex))
    P = sp.Poly(e1, al, la, epsUV)
    for mon, co in P.terms():
        out[mon] = co / den
    return out


def el_components(M, kind, N, bg=None):
    """EL coefficients split by coupling monomial (exponents of alpha, lambda, eps): comps[k][mon] = LS (O(1) sizes)"""
    sub, dr, info = series_point(kind, N, bg)
    cache = {}
    Mt = {}
    for (i, j), v in M.items():
        Mt[(i, j)] = v * (2 if i == j else 1)
        if i != j:
            Mt[(j, i)] = v
    ser = {}
    for key, v in Mt.items():
        for mon, ex in split_couplings(v).items():
            ser[(key, mon)] = eval_ls(ex, sub, N, cache)
    comps = {}
    for ((i, j), mon), v in ser.items():
        for m in range(i + 1):
            d = v
            for _ in range(i - m):
                d = dr(d)
            k = j + m
            term = d * (mp.mpf(-1)**i * math.comb(i, m))
            comps.setdefault(k, {})
            comps[k][mon] = term if mon not in comps[k] else comps[k][mon] + term
    return comps, sub, dr, info


def combine(comps, alpha_v, lam_v, eps_v, tol_abs):
    """numeric a_k (LS) and, separately, the leading power and coefficient decided component-wise
    (a component's coefficient is zero if |c| <= tol_abs; components are O(1))"""
    w = lambda mon: mp.mpf(alpha_v)**mon[0] * mp.mpf(lam_v)**mon[1] * (mp.mpf(eps_v)**mon[2] if mon[2] else 1)
    a, lead = {}, {}
    for k, cd in comps.items():
        acc = None
        best = None
        for mon, ls in cd.items():
            if mon[2] and mp.mpf(eps_v) == 0:
                continue
            ww = w(mon)
            acc = ls * ww if acc is None else acc + ls * ww
            for p in range(ls.val, ls.val + ls.N):
                if abs(ls.coeff(p)) > tol_abs:
                    if best is None or p < best:
                        best = p
                    break
        if acc is None or best is None:
            continue
        for mon, ls in cd.items():
            if mon[2] and mp.mpf(eps_v) == 0:
                continue
            if ls.val + ls.N - 1 < best + 3:
                raise RuntimeError(f'series window too short for a_{k} component {mon}: ends at {ls.val + ls.N - 1}, lead {best}')
        co = mp.mpf(0)
        for mon, ls in cd.items():
            if mon[2] and mp.mpf(eps_v) == 0:
                continue
            c_ = ls.coeff(best)
            if abs(c_) > tol_abs:
                co += c_ * w(mon)
        top = acc.val + acc.N
        a[k] = LS(best, [acc.coeff(p) for p in range(best, top)], top - best)   # window starts at the true leading power
        lead[k] = (best, co)
    return a, lead


def ops_numeric(jet_c1, kind, N, bg=None):
    """first-order operator coefficients c_k (functions of background, angle factor removed) as LS"""
    sub, dr, info = series_point(kind, N, bg)
    cache = {}
    out = {}
    for k, v in jet_c1.items():
        out[k] = eval_ls(v, sub, N, cache)
    return out


def _fall(s, k):
    out = 1
    for q in range(k):
        out = out * (s - q)
    return out


def newton(lead, where):
    """Newton polygon of sum_k a_k(t) d^k F/dr^k. where='uh' (t = x -> 0+, power of x = val) or 'inf' (t = z = 1/r,
    power of r = -val). Returns leading data, the Frobenius indicial polynomial (as mp coefficient list in s via
    falling factorials) and the exponential edges with their characteristic polynomials in b."""
    info = {}
    for k, (val, A) in lead.items():
        m = val if where == 'uh' else -val
        info[k] = (m, A, m - k)
    if where == 'uh':
        Pext = min(t[2] for t in info.values())
    else:
        Pext = max(t[2] for t in info.values())
    kset = [k for k, t in info.items() if t[2] == Pext]
    k2 = max(kset)
    edges = []
    cur = (k2, Pext)
    while True:
        cand = [(k, info[k][2]) for k in info if k > cur[0]]
        if not cand:
            break
        sl = [(sp.Rational(P - cur[1], k - cur[0]), k) for k, P in cand]
        best = min(z for z, _ in sl) if where == 'uh' else max(z for z, _ in sl)
        kend = max(k for z, k in sl if z == best)
        onedge = sorted([cur[0]] + [k for z, k in sl if z == best])
        edges.append({'k_a': cur[0], 'k_b': kend, 'slope': best, 'onedge': onedge,
                      'charA': {k: info[k][1] for k in onedge}})
        cur = (kend, info[kend][2])
    return {'info': info, 'Pext': Pext, 'kset': sorted(kset), 'k2': k2, 'edges': edges}


def indicial_roots(nw):
    """roots of sum_{k in kset} A_k [s]_k, built in mpmath (falling factorials expanded exactly)"""
    deg = max(nw['kset'])
    co = [mp.mpf(0)] * (deg + 1)          # co[j] = coefficient of s^j
    for k in nw['kset']:
        A = nw['info'][k][1]
        poly = [mp.mpf(1)]                # [s]_k coefficients, lowest first
        for q in range(k):
            new = [mp.mpf(0)] * (len(poly) + 1)
            for j, c_ in enumerate(poly):
                new[j + 1] += c_
                new[j] -= q * c_
            poly = new
        for j, c_ in enumerate(poly):
            co[j] += A * c_
    roots = mp.polyroots(list(reversed(co)), maxsteps=2000, extraprec=4 * mp.mp.dps)
    return roots, co


def edge_roots(edge):
    """nonzero roots b of sum_{k on edge} A_k b^(k - k_a)"""
    ka, kb = edge['k_a'], edge['k_b']
    co = [mp.mpf(0)] * (kb - ka + 1)
    for k, A in edge['charA'].items():
        co[kb - k] = A           # highest power first
    return mp.polyroots(co, maxsteps=2000, extraprec=4 * mp.mp.dps)


def _phi_series(where, bvec, N, lead_pow):
    """Phi' as LS in t: UH t = x, Phi' = sum_j b_j x^(-mu + j); infinity t = z, Phi' = sum_j b_j r^(nu - j) = b_j z^(j - nu)"""
    return LS(lead_pow, list(bvec), N)


def wkb_transport(a, lead, dr, where, edge, b0, N=12):
    """Solve Phi' = b0 t^p0 + b1 t^(p0+1) + ... up to the coefficient of 1/r (infinity) or 1/x (UH), order by order.
    Returns the list of b_j and beta (the 1/r or 1/x coefficient). F = exp(int Phi' dr)."""
    if where == 'uh':
        mu = int(edge['slope'] + 1)
        p0 = -mu                      # Phi' ~ x^-mu
        nsteps = mu - 1               # coefficients up to x^-1
    else:
        nu = int(-1 - edge['slope'])
        p0 = -nu                      # Phi' ~ r^nu = z^-nu
        nsteps = nu + 1               # up to r^-1 = z^1
    bs = [b0]

    def resid(bvec):
        Phi = LS(p0, bvec + [mp.mpf(0)] * (N - len(bvec)), N)
        G = LS.const(1, N)
        E = None
        for k in range(max(a.keys()) + 1):
            if k in a:
                term = a[k] * G
                E = term if E is None else E + term
            G = dr(G) + Phi * G
        return E
    E0 = resid(bs)
    # leading power (should cancel): find the power where the edge balance sits
    base = None
    for k in edge['onedge']:
        val = lead[k][0]
        pw = val + k * p0
        base = pw if base is None else min(base, pw)
    lead_coeff = E0.coeff(base)
    for j in range(1, nsteps + 1):
        target = base + j
        e0 = resid(bs + [mp.mpf(0)]).coeff(target)
        e1 = resid(bs + [mp.mpf(1)]).coeff(target)
        bj = -e0 / (e1 - e0)
        bs.append(bj)
    check = resid(bs).coeff(base + nsteps)
    return bs, {'base_power': base, 'lead_residual': lead_coeff, 'next_residual': check}


# ------------------------------------------------------------------------------------------- classification
def _round_int(s, tol=mp.mpf('1e-40')):
    if isinstance(s, mp.mpc) and abs(s.imag) > tol * (1 + abs(s)):
        return s
    re = s.real if isinstance(s, mp.mpc) else s
    n = mp.nint(re)
    if abs(re - n) < tol * (1 + abs(re)):
        return int(n)
    return re


def _lead_rel(ls, rel=mp.mpf('1e-30')):
    big = max([abs(z) for z in ls.c] + [mp.mpf(0)])
    if big == 0:
        return None, 0
    for k, z in enumerate(ls.c):
        if abs(z) > rel * big:
            return ls.val + k, z
    return None, 0


def frob_quantity_powers(s, ops):
    """for F = x^s at the UH: power of each quantity Q = sum_k c_k F^(k) and of its radial gradient (real parts)"""
    s = _round_int(s)
    out = {}
    for name, cks in ops.items():
        L = None
        for k, ck in cks.items():
            fk = _fall(s, k)
            if fk == 0:
                continue
            term = LS(ck.val - k, [z * fk for z in ck.c], ck.N)
            L = term if L is None else L + term
        if L is None:
            out[name] = (None, None)
            continue
        v, _ = _lead_rel(L)
        G = LS(L.val - 1, [z * s for z in L.c], L.N) + L.deriv()
        vg, _ = _lead_rel(G)
        re_s = s.real if isinstance(s, mp.mpc) else s
        out[name] = (None if v is None else v + re_s, None if vg is None else vg + re_s)
    return out


def wkb_quantity_powers(b0, beta, mu, ops):
    """UH WKB mode F ~ x^beta exp(int b0 x^-mu): power of |Q| (oscillation modulus) and of its gradient"""
    out = {}
    for name, cks in ops.items():
        best, co = None, 0
        for k, ck in cks.items():
            v, c0 = _lead_rel(ck)
            if v is None:
                continue
            pw = v - k * mu
            if best is None or pw < best:
                best, co = pw, c0 * b0**k
            elif pw == best:
                co += c0 * b0**k
        out[name] = (best + mp.re(beta), best + mp.re(beta) - mu)
    return out


def classify_uh(kind, pw, s=None, b0=None, mu=None):
    """frozen rule: regular / weak / strong"""
    if kind == 'frob':
        s = _round_int(s)
        if not isinstance(s, mp.mpc) and (s in (-1, 0) or s >= 6):
            return 'regular'
    if kind == 'wkb':
        reb = mp.re(b0); scale = abs(b0)
        if reb > mp.mpf('1e-20') * scale:
            return 'regular'          # exp(-b/x)-type with Re b > 0: super-exponentially flat (mu = 2 convention below)
        if reb < -mp.mpf('1e-20') * scale:
            return 'strong'
    bounded = all(p[0] is None or p[0] >= 0 for p in pw.values())
    integ = all(p[1] is None or p[1] > -1 for p in pw.values())
    return 'weak' if (bounded and integ) else 'strong'
