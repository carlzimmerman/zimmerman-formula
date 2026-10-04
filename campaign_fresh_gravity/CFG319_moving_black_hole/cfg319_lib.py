# -*- coding: utf-8 -*-
"""
CFG319 numerical library: truncated power series (TPS), Frobenius tools, the static test-khronon background, and the
local-Taylor marching of the O(v) Ostrogradsky system. Imported by cfg319_moving_bh.py; it has no side effects.

Conventions: Schwarzschild, M = 1, ingoing EF; e = 1 - 2/r; Y = -u.chi (khronon lapse in the BH frame); W = -u^r =
sqrt(Y^2 - e). O(v) khronon: T = v + H(r) + v F(r) cos(theta). Ostrogradsky vector X = (F, F', p1, p2) with
p2 = dL/dF'', p1 = dL/dF' - p2'. lam_b = lambda + beta enters the static background.
"""
import mpmath as mp
import sympy as sp

# ============================================================================================ truncated power series
class T:
    __slots__ = ('c',)
    N = 30

    def __init__(self, c):
        c = list(c)[:T.N]
        self.c = c + [mp.mpf(0)] * (T.N - len(c))

    @staticmethod
    def const(a):
        return T([mp.mpf(a)])

    @staticmethod
    def var(a0):
        return T([mp.mpf(a0), mp.mpf(1)])

    def _co(self, o):
        return o if isinstance(o, T) else T.const(o)

    def __add__(self, o):
        o = self._co(o)
        return T([a + b for a, b in zip(self.c, o.c)])
    __radd__ = __add__

    def __neg__(self):
        return T([-a for a in self.c])

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        if not isinstance(o, T):
            return T([a * o for a in self.c])
        a, b, n = self.c, o.c, T.N
        return T([mp.fsum(a[i] * b[k - i] for i in range(k + 1)) for k in range(n)])
    __rmul__ = __mul__

    def inv(self):
        a = self.c
        if a[0] == 0:
            raise ZeroDivisionError('TPS inverse with zero constant term')
        b = [1 / a[0]]
        for k in range(1, T.N):
            b.append(-mp.fsum(a[i] * b[k - i] for i in range(1, k + 1)) / a[0])
        return T(b)

    def __truediv__(self, o):
        if not isinstance(o, T):
            return T([a / o for a in self.c])
        return self * o.inv()

    def __rtruediv__(self, o):
        return self._co(o) * self.inv()

    def __pow__(self, p):
        pf = float(p)
        if pf.is_integer():
            p = int(pf)
            if p < 0:
                return self.inv() ** (-p)
            res, base = T.const(1), self
            while p:
                if p & 1:
                    res = res * base
                base = base * base
                p >>= 1
            return res
        if abs(pf - 0.5) < 1e-15:
            return tsqrt(self)
        raise ValueError('non-integer TPS power %r' % p)

    def deriv(self):
        return T([k * self.c[k] for k in range(1, T.N)] + [mp.mpf(0)])

    def __call__(self, x):
        return mp.fsum(self.c[k] * x ** k for k in range(T.N))


def tsqrt(s):
    if not isinstance(s, T):
        return mp.sqrt(s)
    a = s.c
    b = [mp.sqrt(a[0])]
    for k in range(1, T.N):
        b.append((a[k] - mp.fsum(b[i] * b[k - i] for i in range(1, k))) / (2 * b[0]))
    return T(b)


def lam_tps(expr, args):
    """lambdify a sympy expression so that it accepts TPS (or mpf) arguments."""
    return sp.lambdify(args, expr, modules=[{'sqrt': tsqrt}, 'mpmath'])


def radius(t):
    """radius-of-convergence estimate min_k |c_0/c_k|^(1/k) over the upper half of the orders (scale-free: the
    overall magnitude of the series, e.g. S22 ~ Y^4 ~ delta^4 deep in the window, must not bias the step size)."""
    cs = t.c
    n = len(cs)
    c0 = abs(cs[0]) if cs[0] != 0 else max(abs(z) for z in cs[:4])
    best = mp.inf
    for k in range(max(4, n // 2), n):
        if cs[k] != 0:
            best = min(best, (c0 / abs(cs[k])) ** (mp.mpf(1) / k))
    return best


# ============================================================================================ Frobenius tools
def falling(s, k):
    p = mp.mpf(1)
    for i in range(k):
        p *= (s - i)
    return p


def scalar_coeffs(S):
    """4th-order scalar EL operator sum_k c_k F^(k) of L = sum S_ij F^(i) F^(j) (S symmetric TPS dict)."""
    d = lambda t: t.deriv()
    c4 = S[(2, 2)]
    c3 = 2 * d(S[(2, 2)])
    c2 = d(d(S[(2, 2)])) + d(S[(1, 2)]) + 2 * S[(0, 2)] - S[(1, 1)]
    c1 = d(d(S[(1, 2)])) + 2 * d(S[(0, 2)]) - d(S[(1, 1)])
    c0 = d(d(S[(0, 2)])) - d(S[(0, 1)]) + S[(0, 0)]
    return [c0, c1, c2, c3, c4]


def theta_form(c, ordc, order=4, x_check=None):
    """b_k[m] with x^shift * (sum c_k F^(k)) = sum_k x^k b_k(x) F^(k), shift = order - ordc, where ordc is the KNOWN order
    of the zero of the leading coefficient (spin-0 horizon 1, universal horizon 4, toy 2, alpha = 0 sub-equation 3).
    Returns (b, shift, dropped) with dropped = max_{j < ordc} |c_order[j]| x^j / (|c_order[ordc]| x^ordc) at x = x_check."""
    n = T.N
    shift = order - ordc
    dropped = mp.mpf(0)
    if x_check is not None:
        ref = abs(c[order].c[ordc]) * x_check ** ordc
        for jj in range(ordc):
            dropped = max(dropped, abs(c[order].c[jj]) * x_check ** jj / ref)
    b = []
    for k in range(order + 1):
        arr = []
        for m in range(n):
            idx = m - shift + k
            arr.append(c[k].c[idx] if 0 <= idx < n else mp.mpf(0))
        b.append(arr)
    return b, shift, dropped


def Pm(b, m, sig):
    return mp.fsum(b[k][m] * falling(sig, k) for k in range(len(b)))


def indicial_roots(b):
    s = sp.Symbol('s')
    poly = sum(sp.Float(mp.nstr(b[k][0], mp.mp.dps), mp.mp.dps) * sp.prod([s - i for i in range(k)]) for k in range(len(b)))
    co = [complex(z) for z in sp.Poly(sp.expand(poly), s).all_coeffs()]
    rts = mp.polyroots([mp.mpc(z) for z in co], maxsteps=400, extraprec=400)
    return sorted(rts, key=lambda z: (mp.re(z), mp.im(z)))


def frob(b, s, nterms):
    """Frobenius series F = x^s sum f_n x^n; resonant free coefficients set to zero; returns (f, resonance list)."""
    f = [mp.mpf(1)]
    res = []
    for n in range(1, nterms):
        rhs = -mp.fsum(f[n - m] * Pm(b, m, n - m + s) for m in range(1, n + 1))
        p0 = Pm(b, 0, n + s)
        p0scale = mp.fsum(abs(b[k][0]) * (abs(n + s) + 1) ** k for k in range(len(b)))   # polynomial magnitude scale
        if p0 == 0 or abs(p0) < mp.mpf(10) ** (-mp.mp.dps // 3) * p0scale:
            res.append((n, rhs))
            f.append(mp.mpf(0))
        else:
            f.append(rhs / p0)
    return f, res


def frob_derivs(s, f, x, kmax=4):
    return [mp.fsum(f[n] * falling(n + s, kk) * mp.power(x, n + s - kk) for n in range(len(f))) for kk in range(kmax)]


def ostro_from_F(S, Fk, x):
    """Ostrogradsky vector from F, F', F'', F''' at x, with S (TPS dict about the expansion point)."""
    Sv = {k: v(x) for k, v in S.items()}
    Sd = {k: v.deriv()(x) for k, v in S.items()}
    p2 = 2 * (Sv[(2, 0)] * Fk[0] + Sv[(2, 1)] * Fk[1] + Sv[(2, 2)] * Fk[2])
    p2d = 2 * (Sd[(2, 0)] * Fk[0] + Sv[(2, 0)] * Fk[1] + Sd[(2, 1)] * Fk[1] + Sv[(2, 1)] * Fk[2] + Sd[(2, 2)] * Fk[2]
               + Sv[(2, 2)] * Fk[3])
    p1 = 2 * (Sv[(1, 0)] * Fk[0] + Sv[(1, 1)] * Fk[1] + Sv[(1, 2)] * Fk[2]) - p2d
    return [Fk[0], Fk[1], p1, p2]


def F2_from_ostro(Sv, X):
    """F'' from the Ostrogradsky vector (S values at the point)."""
    return (X[3] / 2 - Sv[(2, 0)] * X[0] - Sv[(2, 1)] * X[1]) / Sv[(2, 2)]


def omega(X, Z):
    """canonical symplectic product q.p' - p.q' of two Ostrogradsky vectors."""
    return X[0] * Z[2] + X[1] * Z[3] - X[2] * Z[0] - X[3] * Z[1]


# ============================================================================================ the model
class Model:
    """Holds lambdified (TPS-capable) expressions for one (alpha, lambda, beta)."""

    def __init__(self, sym, a, l, b):
        self.a, self.l, self.b = mp.mpf(a), mp.mpf(l), mp.mpf(b)
        self.lb = self.l + self.b
        Ys, Ws, Y1s, W1s, al, la, be, rs = sp.symbols('Y W Y1 W1 alpha lambda beta r')
        loc = {'Y': Ys, 'W': Ws, 'Y1': Y1s, 'W1': W1s, 'alpha': al, 'lam': la, 'beta': be, 'r': rs}
        P = lambda s: sp.sympify(s.replace('lambda', 'lam'), locals=loc)
        sub = {al: self.a, la: self.l, be: self.b}
        self.M = {k: lam_tps(P(v).subs(sub), (Ys, Ws, Y1s, W1s)) for k, v in sym['M'].items()}
        self.K1 = [lam_tps(P(v).subs(sub), (Ys, Ws, Y1s, W1s)) for v in sym['K1']]
        self.A1 = [lam_tps(P(v).subs(sub), (Ys, Ws, Y1s, W1s)) for v in sym['A1']]
        self.Ast = lam_tps(P(sym['A_static']).subs(sub), (rs, Ys))
        self.Bst = lam_tps(P(sym['B_static']).subs(sub), (rs, Ys, Y1s))
        self.W2st = lam_tps(P(sym['W2_static']).subs(sub), (rs, Ws, W1s))

    # ---------------------------------------------------------------- static background series
    def resid_Y(self, r, Yt):
        Y1 = Yt.deriv()
        return self.Ast(r, Yt) * Y1.deriv() + self.Bst(r, Yt, Y1)

    def resid_W(self, r, Wt):
        W1 = Wt.deriv()
        return W1.deriv() - self.W2st(r, Wt, W1)

    def bgY_series(self, r0, y0, y1, N):
        r0 = mp.mpf(r0)
        c = [mp.mpf(y0), mp.mpf(y1)] + [mp.mpf(0)] * (N - 2)
        A0 = self.Ast(r0, c[0])
        for m in range(2, N):
            T.N = m + 1
            res = self.resid_Y(T.var(r0), T(c[:m]))
            c[m] = -res.c[m - 2] / (A0 * m * (m - 1))
        T.N = N
        return T(c)

    def bgW_series(self, r0, w0, w1, N):
        r0 = mp.mpf(r0)
        c = [mp.mpf(w0), mp.mpf(w1)] + [mp.mpf(0)] * (N - 2)
        for m in range(2, N):
            T.N = m + 1
            res = self.resid_W(T.var(r0), T(c[:m]))
            c[m] = -res.c[m - 2] / (m * (m - 1))
        T.N = N
        return T(c)

    def regular_data(self, rS, Y1_guess):
        """Y_S and the analytic-branch slope at the spin-0 horizon r_S (A(r_S, Y_S) = 0, B = 0)."""
        rS = mp.mpf(rS)
        e = 1 - 2 / rS
        YS = mp.sqrt(-self.a * e / (self.lb - self.a))
        q = lambda y1: self.Bst(rS, YS, y1)
        # B is quadratic in Y1: find both roots and take the one nearest the guess
        c0 = q(0); c1p = q(1); c1m = q(-1)
        A2 = (c1p + c1m) / 2 - c0; A1 = (c1p - c1m) / 2
        disc = A1 ** 2 - 4 * A2 * c0
        roots = [(-A1 + sg * mp.sqrt(disc)) / (2 * A2) for sg in (1, -1)]
        Y1 = min(roots, key=lambda z: abs(z - Y1_guess))
        return YS, Y1

    def bgY_series_rS(self, rS, YS, Y1, N):
        rS = mp.mpf(rS)
        Ax = mp.diff(lambda t: self.Ast(rS + t, YS + Y1 * t), 0)
        BY1 = mp.diff(lambda q: self.Bst(rS, YS, q), Y1)
        c = [mp.mpf(YS), mp.mpf(Y1)] + [mp.mpf(0)] * (N - 2)
        for m in range(2, N):
            T.N = m + 2
            res = self.resid_Y(T.var(rS), T(c[:m]))
            c[m] = -res.c[m - 1] / (m * (m - 1) * Ax + m * BY1)
        T.N = N
        return T(c), (Ax, BY1)

    def static_exponent_rS(self, rS, YS, Y1):
        Ax = mp.diff(lambda t: self.Ast(rS + t, YS + Y1 * t), 0)
        BY1 = mp.diff(lambda q: self.Bst(rS, YS, q), Y1)
        return 1 - BY1 / Ax

    # ---------------------------------------------------------------- O(v) system
    def S_series(self, r0, Yt=None, Wt=None):
        r = T.var(r0)
        e = 1 - 2 / r
        if Yt is not None:
            Wt = tsqrt(Yt * Yt - e); Y1 = Yt.deriv(); W1 = (Yt * Y1 - 1 / (r * r)) / Wt
        else:
            Yt = tsqrt(e + Wt * Wt); W1 = Wt.deriv(); Y1 = (Wt * W1 + 1 / (r * r)) / Yt
        S = {}
        for i in range(3):
            for j in range(i, 3):
                m = self.M[str((i, j))](Yt, Wt, Y1, W1)
                if not isinstance(m, T):
                    m = T.const(m)
                S[(i, j)] = m if i == j else m * mp.mpf('0.5')
                S[(j, i)] = S[(i, j)]
        return S, (Yt, Wt, Y1, W1)

    def ops_series(self, bgt):
        """dK = k0 F + k1 F' + k2 F''; d(a.a) = a0 F + a1 F' + a2 F'' (TPS coefficients)."""
        Yt, Wt, Y1, W1 = bgt
        kk = [f(Yt, Wt, Y1, W1) for f in self.K1]
        aa = [f(Yt, Wt, Y1, W1) for f in self.A1]
        kk = [z if isinstance(z, T) else T.const(z) for z in kk]
        aa = [z if isinstance(z, T) else T.const(z) for z in aa]
        return kk, aa


def A_series(S):
    inv22 = S[(2, 2)].inv()
    f2 = [-S[(2, 0)] * inv22, -S[(2, 1)] * inv22, T.const(0), inv22 * mp.mpf('0.5')]
    Z = T.const(0)
    A = [[Z, T.const(1), Z, Z], f2,
         [2 * (S[(0, 0)] + S[(0, 2)] * f2[0]), 2 * (S[(0, 1)] + S[(0, 2)] * f2[1]), Z, 2 * S[(0, 2)] * f2[3]],
         [2 * (S[(1, 0)] + S[(1, 2)] * f2[0]), 2 * (S[(1, 1)] + S[(1, 2)] * f2[1]), T.const(-1), 2 * S[(1, 2)] * f2[3]]]
    return A


def X_series(A, X0):
    N = T.N
    ncol = len(X0[0])
    Xc = [[list(X0[i]) for i in range(4)]]
    for k in range(N - 1):
        nxt = [[mp.mpf(0)] * ncol for _ in range(4)]
        for i in range(4):
            for j in range(4):
                Aij = A[i][j].c
                for m in range(k + 1):
                    am = Aij[k - m]
                    if am == 0:
                        continue
                    Xm = Xc[m][j]
                    for col in range(ncol):
                        nxt[i][col] += am * Xm[col]
        Xc.append([[z / (k + 1) for z in row] for row in nxt])
    return Xc


def eval_X(Xc, h):
    N = len(Xc)
    ncol = len(Xc[0][0])
    return [[mp.fsum(Xc[k][i][col] * h ** k for k in range(N)) for col in range(ncol)] for i in range(4)]


def to_W(r, Y, Y1):
    W = mp.sqrt(Y ** 2 - (1 - 2 / r))
    return [W, (Y * Y1 - 1 / r ** 2) / W]


def to_Y(r, W, W1):
    Y = mp.sqrt(1 - 2 / r + W ** 2)
    return [Y, (W * W1 + 1 / r ** 2) / Y]


def march(model, r0, r1, bg, X, form, N, rho, r_sw=mp.mpf(8), with_X=True, singular_start=None):
    """Local-Taylor march of the background (and X if with_X) from r0 to r1. bg = (Y, Y') or (W, W').
    singular_start = (YS, Y1) when r0 is the spin-0 horizon (uses the analytic-branch series there)."""
    r = mp.mpf(r0); r1 = mp.mpf(r1); bg = list(bg)
    sgn = 1 if r1 > r else -1
    n = 0
    tol = mp.mpf(10) ** (-mp.mp.dps + 4)
    while (r1 - r) * sgn > 0:
        if form == 'Y':
            if singular_start is not None and n == 0:
                bt, _ = model.bgY_series_rS(r, singular_start[0], singular_start[1], N)
            else:
                bt = model.bgY_series(r, bg[0], bg[1], N)
        else:
            bt = model.bgW_series(r, bg[0], bg[1], N)
        Rc = min(radius(bt), abs(r) * mp.mpf('0.9'))
        S = None
        if with_X:
            S, _ = model.S_series(r, Yt=bt) if form == 'Y' else model.S_series(r, Wt=bt)
            Rc = min(Rc, radius(S[(2, 2)].inv()))
        scale_b = abs(bt.c[0]) + abs(bt.c[1])
        h = min(rho * Rc, abs(r1 - r))
        for k in range(N - 3, N):
            if bt.c[k] != 0:
                h = min(h, (tol * scale_b / abs(bt.c[k])) ** (mp.mpf(1) / k))
        if with_X:
            Xc = X_series(A_series(S), X)
            for col in range(len(X[0])):
                sc_ = max(abs(Xc[0][i][col]) for i in range(4)) + mp.mpf(10) ** (-300)
                for k in range(N - 3, N):
                    ck = max(abs(Xc[k][i][col]) for i in range(4))
                    if ck != 0:
                        h = min(h, (tol * sc_ / ck) ** (mp.mpf(1) / k))
            X = eval_X(Xc, h * sgn)
        hs = h * sgn
        bg = [bt(hs), bt.deriv()(hs)]
        r += hs
        n += 1
        if form == 'Y' and r > r_sw:
            bg = to_W(r, *bg); form = 'W'
        elif form == 'W' and r < r_sw:
            bg = to_Y(r, *bg); form = 'Y'
    return bg, X, form, n


def solve_scaled(M, b):
    """Solve M x = b with row and column equilibration (the Ostrogradsky components differ by many decades)."""
    n = M.rows
    rs = [max(abs(M[i, j]) for j in range(n)) for i in range(n)]
    Ms = mp.matrix(n, n); bs = mp.matrix(n, 1)
    for i in range(n):
        for j in range(n):
            Ms[i, j] = M[i, j] / rs[i]
        bs[i] = b[i] / rs[i]
    cs = [max(abs(Ms[i, j]) for i in range(n)) for j in range(n)]
    for i in range(n):
        for j in range(n):
            Ms[i, j] = Ms[i, j] / cs[j]
    y = mp.lu_solve(Ms, bs)
    return mp.matrix([y[j] / cs[j] for j in range(n)])
