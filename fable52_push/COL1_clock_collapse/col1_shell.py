"""COL1 solver (amendment A3): exact thin shells for the clock of action (A), spherical, Newtonian order, gamma_L = 0.

Shells j = 1 .. J-1 carry the conserved clock charge m_j; node 0 is the centre (no charge); node J is the prescribed outer
boundary (h = h_b). The law sector is solved in its dual (flux) form. Q_j is the polarization charge enclosed in gap j
(between shells j and j+1), Q_0 = 0. In the gap, K P = G Q_j / r^2 exactly (Gauss), A = U(G Q_j / r^2) with
U(y) = a0 y/(a0 - |y|) (X14's flux-capped map). The dust charge on shell k is d_k = m_k - (Q_k - Q_{k-1}), spread over its
Lagrangian cell volume V_k, with h_k = d_k / (mu_K^2 V_k / K). The internal energy is

    U(r) = min_Q  sum_gaps Int W(G|Q_j|/r^2) 4 pi r^2 dr  +  sum_k d_k^2 / (2 (mu_K^2/K) V_k)  +  h_b Q_{J-1},

convex in Q with a log barrier at the flux cap. Its stationarity is h_j - h_{j+1} = Int_gap A dr. Forces follow from the
envelope theorem. The law part on shell j is 4 pi r_j^2 [W(G Q_j/r_j^2) - W(G Q_{j-1}/r_j^2)] = Int A dQ over the shell's own
polarization charge, which is X14's exact finite-shell force. The pressure part is 4 pi r_j^2 [alpha_j (p_j - p_{j+1}) +
(1 - alpha_{j-1})(p_{j-1} - p_j)]. Gravity is thin-shell, G (M_b(<r) + M_<j + m_j/2)/r^2, variational and exact for the
uniform state with the recursive faces. Faces: b_{j+1/2}^3 = alpha_j r_j^3 + (1 - alpha_j) r_{j+1}^3, with alpha_j fixed at
the start from the recursion b_{j+1/2}^3 = 2 r_j^3 - b_{j-1/2}^3, b_{1/2} = 0, so that M_<j + m_j/2 = (4 pi/3) n r_j^3
holds exactly for any uniform state and under homologous motion.

Units kpc, km/s, Msun. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import math
import numpy as np
from scipy.linalg import solve_banded
import col1_lib as L

G, K, PI, TU = L.G, L.K, L.PI, L.TU
_TG, _TW = np.polynomial.legendre.leggauss(24)


class HSolveError(RuntimeError):
    pass


def recursive_faces(r):
    """Faces b_{j+1/2} (j = 0 .. J-1) for nodes r (r[0] = 0, r[J] the boundary): b_{1/2} = 0 (centre node has no cell),
    b_{j+1/2}^3 = 2 r_j^3 - b_{j-1/2}^3 for j = 1 .. J-1; returns b3 (cubes) of length J+1 with b3[j] = face above node j,
    b3[J] = r_J^3, and alpha_j such that b3[j] = alpha_j r_j^3 + (1 - alpha_j) r_{j+1}^3."""
    J = len(r) - 1
    b3 = np.zeros(J + 1)
    for j in range(1, J):
        b3[j] = 2 * r[j] ** 3 - b3[j - 1]
    b3[J] = r[J] ** 3
    alpha = np.zeros(J + 1)
    alpha[0] = 1.0                                 # b_{1/2} = 0 does not move with r_1
    r3 = r ** 3
    alpha[1:J] = (r3[2:J + 1] - b3[1:J]) / (r3[2:J + 1] - r3[1:J])
    if not (np.all(alpha[1:J] > 0) and np.all(alpha[1:J] < 1)):
        bad = np.where((alpha[1:J] <= 0) | (alpha[1:J] >= 1))[0] + 1
        raise ValueError(f'recursive faces leave their gaps at nodes {bad[:5]}')
    return b3, alpha


class Law2:
    """kind: law, off (M1, Pi = 0), neg (M2, Pi enters N with the opposite sign and its stress with the opposite sign),
    flip (M2a, the P.A sign flip: the same Legendre maximum, the same code path), lin (M3, U(y) -> y)."""

    def __init__(self, a0, kind='law'):
        self.a0, self.kind = a0, kind
        self.sgn = -1.0 if kind == 'neg' else 1.0

    def W(self, p):                 # p = K|P| = G|Q|/r^2 (acceleration); returns energy density
        a0 = self.a0
        p = np.abs(p)
        if self.kind == 'lin':
            return p * p / (2 * K)
        x = p / a0
        with np.errstate(invalid='ignore', divide='ignore'):
            out = (a0 * a0 / K) * np.where(x < 1e-4, x * x / 2 + x ** 3 / 3 + x ** 4 / 4, -x - np.log1p(-x))
        return np.where(x < 1, out, np.inf)

    def I(self, c, a, b):
        """Int_a^b U(c/r^2) dr, c = G Q (signed)."""
        a0 = self.a0
        if self.kind == 'lin':
            return c * (1 / a - 1 / b)
        out = np.empty_like(c)
        y = np.abs(c) / (a0 * a * a)
        small = y < 1e-3
        cs = c[small]; as_, bs = a[small], b[small]
        sg = np.sign(cs)
        out[small] = (cs * (1 / as_ - 1 / bs) + sg * cs * cs / (3 * a0) * (as_ ** -3 - bs ** -3)
                      + cs ** 3 / (5 * a0 * a0) * (as_ ** -5 - bs ** -5) + sg * cs ** 4 / (7 * a0 ** 3) * (as_ ** -7 - bs ** -7))
        big = ~small
        cb, ab, bb = c[big], a[big], b[big]
        s = math.sqrt(a0)
        pos = cb > 0
        q = np.sqrt(np.abs(cb))
        with np.errstate(invalid='ignore', divide='ignore'):
            Lp = np.log((s * bb - q) / (s * bb + q)) - np.log((s * ab - q) / (s * ab + q))
            vpos = 0.5 * s * q * Lp
            vneg = -s * q * (np.arctan(s * bb / q) - np.arctan(s * ab / q))
        out[big] = np.where(pos, vpos, vneg)
        cap = (np.abs(c) >= a0 * a * a)
        out[cap] = np.inf * np.sign(c[cap])
        return out

    def EW(self, c, a, b):
        """Int_a^b W(|c|/r^2) 4 pi r^2 dr by Gauss-Legendre in t = 1/r."""
        ta, tb = 1 / a, 1 / b
        tq = 0.5 * (ta + tb)[:, None] + 0.5 * (tb - ta)[:, None] * _TG[None, :]
        wq = 0.5 * (ta - tb)[:, None] * _TW[None, :]
        Wv = self.W(np.abs(c)[:, None] * tq * tq)
        return (wq * Wv * 4 * PI / tq ** 4).sum(axis=1)


def volumes(r, alpha):
    J = len(r) - 1
    r3 = r ** 3
    b3 = np.zeros(J + 1)
    b3[1:J] = alpha[1:J] * r3[1:J] + (1 - alpha[1:J]) * r3[2:J + 1]
    b3[J] = r3[J]
    V = np.zeros(J + 1)
    V[1:] = (4 * PI / 3) * (b3[1:] - b3[:-1])
    return V, b3


def qsolve(r, m, hb, mu2K, law, alpha, Q0, tol=1e-11, maxit=80):
    """Polarization charges Q_1 .. Q_{J-1} (Q_0 = 0). Returns Q (len J), h (len J+1), d (len J+1)."""
    J = len(r) - 1
    V, _ = volumes(r, alpha)
    if law.kind == 'off':
        Q = np.zeros(J)
        d = m.copy(); d[0] = 0.0
        h = np.zeros(J + 1); h[1:J] = d[1:J] / (mu2K * V[1:J]); h[J] = hb; h[0] = h[1]
        return Q, h, d, 0, 0.0
    a, b = r[1:J], r[2:J + 1]                     # gaps 1 .. J-1
    if mu2K == 0.0:
        Q = np.concatenate([[0.0], np.cumsum(m[1:J])])
        Ig = law.I(G * Q[1:], a, b)
        if not np.all(np.isfinite(Ig)):
            raise HSolveError('flux cap exceeded (mu_K = 0): no h solution')
        h = np.zeros(J + 1); h[J] = hb
        h[1:J] = hb + np.cumsum(Ig[::-1])[::-1]
        h[0] = h[1]
        return Q, h, np.zeros(J + 1), 0, 0.0
    sgn = law.sgn
    Q = Q0.copy(); Q[0] = 0.0
    k = 1.0 / (mu2K * V)                           # dh_k/dd_k

    def hvals(Q):
        d = np.zeros(J + 1)
        pi = np.zeros(J + 1); pi[1:J] = Q[1:J] - Q[0:J - 1]
        d[1:J] = m[1:J] - sgn * pi[1:J]
        h = np.zeros(J + 1); h[1:J] = d[1:J] * k[1:J]; h[J] = hb; h[0] = h[1]
        return h, d

    def obj(Q):
        h, d = hvals(Q)
        ew = law.EW(G * Q[1:], a, b)
        return sgn * ew.sum() + 0.5 * (d[1:J] ** 2 * k[1:J]).sum() + hb * sgn * Q[J - 1]

    prev = np.inf
    for it in range(maxit):
        h, d = hvals(Q)
        Ig = law.I(G * Q[1:], a, b)
        if not np.all(np.isfinite(Ig)):
            raise HSolveError('iterate outside the flux cap')
        R = Ig - (h[1:J] - h[2:J + 1])               # j = 1 .. J-1
        S = np.abs(Ig) + np.abs(h[1:J]) + np.abs(h[2:J + 1])
        err = float(np.max(np.abs(R) / np.maximum(S, 1e-300)))
        if err < tol:
            return Q, h, d, it, err
        if it > 3 and err < 1e-6 and err >= 0.5 * prev:
            return Q, h, d, it, err
        prev = err
        dq = 1e-7 * np.maximum(np.abs(Q[1:]), 1e-3 * np.abs(m[1:J]).max() + 1e-300)
        dI = (law.I(G * (Q[1:] + dq), a, b) - law.I(G * (Q[1:] - dq), a, b)) / (2 * dq)
        if not np.all(np.isfinite(dI)):
            dI = (law.I(G * Q[1:], a, b) - law.I(G * (Q[1:] - dq), a, b)) / dq
        # d(h_j - h_{j+1})/dQ: h_k = (m_k - sgn (Q_k - Q_{k-1})) k_k
        kk = k[1:J + 1].copy(); kk[-1] = 0.0           # h_J fixed
        diag = dI + sgn * k[1:J] + sgn * kk[1:]
        off = -sgn * k[2:J]                             # coupling Q_j, Q_{j+1} through h_{j+1}
        ab = np.zeros((3, J - 1))
        ab[0, 1:] = off; ab[1] = diag; ab[2, :-1] = off
        try:
            du = solve_banded((1, 1), ab, -R, check_finite=False)
        except Exception as e:
            raise HSolveError(f'banded solve failed: {e}')
        lam = 1.0
        f0 = obj(Q) if law.kind != 'neg' else None
        for _ in range(60):
            Qn = Q.copy(); Qn[1:] = Q[1:] + lam * du
            Ik = law.I(G * Qn[1:], a, b)
            ok = np.all(np.isfinite(Ik))
            if ok and (f0 is None or err < 1e-4 or obj(Qn) <= f0 + 1e-13 * abs(f0)):
                break
            lam *= 0.5
        Q = Qn
    raise HSolveError(f'Newton did not converge (err {err:.3e})')


def forces(r, Q, h, d, mu2K, law, alpha):
    """Law + pressure force on every node."""
    J = len(r) - 1
    F = np.zeros(J + 1)
    rr = r[1:J]
    if law.kind != 'off':
        Wp = law.W(G * Q[1:J] / rr ** 2)            # just outside shell j (gap j), j = 1 .. J-1
        Wm = law.W(G * Q[0:J - 1] / rr ** 2)        # just inside shell j (gap j-1)
        F[1:J] += law.sgn * 4 * PI * rr ** 2 * (Wp - Wm)
    if mu2K > 0:
        p = 0.5 * mu2K * h ** 2
        p[0] = 0.0
        F[1:J] += 4 * PI * rr ** 2 * (alpha[1:J] * (p[1:J] - p[2:J + 1]) + (1 - alpha[0:J - 1]) * (p[0:J - 1] - p[1:J]))
    return F


class ShellModel(L.Model):
    """Same driver API as col1_lib.Model (run, step_dt, caustic, reads); the field solve and forces are the thin-shell ones."""

    def __init__(self, *args, alpha=None, **kw):
        super().__init__(*args, **kw)
        self.law = Law2(self.a0, args[2])
        self.alpha = alpha
        self.Q = np.zeros(len(self.r) - 1)
        self.d = None

    def accel(self, t, r, v, want=False):
        hb = self.hb_fn(t)
        Q, h, d, its, err = qsolve(r, self.m, hb, self.mu2K, self.law, self.alpha, self.Q)
        self.Q, self.h, self.d = Q, h, d
        self.newton_its += its; self.nsolve += 1
        F = forces(r, Q, h, d, self.mu2K, self.law, self.alpha)
        ah = np.zeros_like(r)
        ah[1:-1] = F[1:-1] / self.m[1:-1]
        rr = r[1:-1]
        ag = np.zeros_like(r)
        Mb = self.Mb_t(t)
        ag[1:-1] = -G * Mb * rr / (rr * rr + self.eps ** 2) ** 1.5 - G * self.Mlag[1:-1] / rr ** 2
        if self.mode == 'hubble':
            a = self.cosmo.a_of_t(t)
            ag[1:-1] += (-(4 * PI / 3) * G * self.cosmo.rhob0 * a ** -3 + self.cosmo.OL * self.cosmo.H0 ** 2) * rr
        elif self.mode == 'rest':
            ag[1:-1] += (4 * PI / 3) * G * self.nbar_sw * rr
        av = np.zeros_like(r)
        if self.visc > 0:
            dv = np.diff(v)
            V, _ = volumes(r, self.alpha)
            a_, b_ = r[:-1], r[1:]
            Vg = 4 * PI * (b_ ** 3 - a_ ** 3) / 3
            rho = 0.5 * (self.m[:-1] + self.m[1:]) / Vg
            q = np.where(dv < 0, self.visc * rho * dv * dv, 0.0)
            Fv = np.zeros_like(r)
            Fv[:-1] -= 4 * PI * a_ * a_ * q
            Fv[1:] += 4 * PI * b_ * b_ * q
            av[1:-1] = Fv[1:-1] / self.m[1:-1]
        acc = ah + ag + av
        acc[0] = 0.0; acc[-1] = 0.0
        if want:
            return acc, ah, ag, av
        return acc

    def energy(self, t):
        r, v, m = self.r, self.v, self.m
        J = len(r) - 1
        V, _ = volumes(r, self.alpha)
        a, b = r[1:J], r[2:J + 1]
        U = 0.0
        if self.law.kind != 'off':
            U += self.law.sgn * self.law.EW(G * self.Q[1:], a, b).sum()
        if self.mu2K > 0:
            U += 0.5 * (self.d[1:J] ** 2 / (self.mu2K * V[1:J])).sum() + self.hb_fn(t) * self.law.sgn * self.Q[J - 1]
        KE = 0.5 * (m[1:-1] * v[1:-1] ** 2).sum()
        rr = r[1:-1]
        W = -(G * self.Mb_t(t) * m[1:-1] / np.sqrt(rr * rr + self.eps ** 2)).sum() - (G * self.Mlag[1:-1] * m[1:-1] / rr).sum()
        return KE, U, W

    def Md_nodes(self):
        """Cumulative dust charge at the nodes (sum of d_k for k <= j)."""
        d = self.d if self.d is not None else np.zeros_like(self.r)
        return np.cumsum(d)


# ---------------- builders ----------------

def charges_uniform(X, nbar):
    b3, alpha = recursive_faces(X)
    m = np.zeros(len(X))
    m[1:] = nbar * (4 * PI / 3) * (b3[1:] - b3[:-1])
    Mlag = np.concatenate([[0.0], np.cumsum(m)[:-1]]) + 0.5 * m
    return m, Mlag, alpha


def charges_profile(X, Mf):
    b3, alpha = recursive_faces(X)
    b = np.cbrt(b3)
    Mb_ = Mf(b)
    Mb_[0] = 0.0
    m = np.zeros(len(X))
    m[1:] = Mb_[1:] - Mb_[:-1]
    Mlag = np.concatenate([[0.0], np.cumsum(m)[:-1]]) + 0.5 * m
    return m, Mlag, alpha


def hubble_model(mu_Mpc, footing, logMb, J, kd1, lawkind='law', Xin=20.0, Xout=8000.0, zi=10.0, eps=1.0,
                 ramp_gyr=1.0, visc=0.0):
    s = kd1['footings'][footing]['setting']
    cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = L.a0_of(footing)
    X = L.log_nodes(Xin, Xout, J)
    m, Mlag, alpha = charges_uniform(X, cos.nbar0)
    ai = 1.0 / (1.0 + zi)
    ti = cos.t_of_a(ai)
    r0 = ai * X
    v0 = cos.H_of_a(ai) * r0
    mu = mu_Mpc / 1000.0
    hb_fn = (lambda t: K * cos.nbar0 * cos.a_of_t(t) ** -3 / mu ** 2) if mu > 0 else (lambda t: 0.0)
    rout = lambda t: cos.a_of_t(t) * X[-1]
    dX = np.diff(X)
    gref = lambda t: cos.a_of_t(t) * dX
    mdl = ShellModel(mu_Mpc, a0, lawkind, r0, v0, m, Mlag, hb_fn, 'hubble', Mb=10 ** logMb, eps=eps, cosmo=cos,
                     ramp=(ti, ramp_gyr / TU), rout_fn=rout, visc=visc, gap_ref=gref, alpha=alpha)
    mdl.h = np.full(len(r0), hb_fn(ti))
    mdl.X = X
    return mdl, ti, cos.t_of_a(1.0), cos


def rest_model(mu_Mpc, footing, logMb, J, kd1, lawkind='law', Xin=20.0, Xout=8000.0, eps=1.0, ramp_gyr=1.0, visc=0.0):
    s = kd1['footings'][footing]['setting']
    cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = L.a0_of(footing)
    X = L.log_nodes(Xin, Xout, J)
    m, Mlag, alpha = charges_uniform(X, cos.nbar0)
    mu = mu_Mpc / 1000.0
    hb = K * cos.nbar0 / mu ** 2
    dX = np.diff(X)
    mdl = ShellModel(mu_Mpc, a0, lawkind, X.copy(), np.zeros_like(X), m, Mlag, lambda t: hb, 'rest', Mb=10 ** logMb,
                     eps=eps, ramp=(0.0, ramp_gyr / TU), rout_fn=lambda t: X[-1], visc=visc, nbar_swindle=cos.nbar0,
                     gap_ref=lambda t: dX, alpha=alpha)
    mdl.h = np.full(len(X), hb)
    mdl.X = X
    return mdl, 0.0, 10.0 / TU, cos


def static_model(X, Mf, mu_Mpc, a0, kind, hb, Mb=0.0, eps=1.0, rout=None):
    m, Mlag, alpha = charges_profile(X, Mf)
    md = ShellModel(mu_Mpc, a0, kind, X.copy(), np.zeros_like(X), m, Mlag, (lambda t: hb) if not callable(hb) else hb,
                    'static', Mb=Mb, eps=eps, rout_fn=rout or (lambda t: X[-1]), gap_ref=lambda t: np.diff(X), alpha=alpha)
    md.h = np.full(len(X), hb if not callable(hb) else hb(0.0))
    md.X = X
    return md
