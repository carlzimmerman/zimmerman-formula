"""Route A: axisymmetric nonlinear AQUAL / QUMOND solver for a point mass in a uniform external field
(lane E2_field_equation).

Units: a0 = 1, r_M = sqrt(GM/a0) = 1, so the Newtonian point field is r_hat / r^2.
F = grad(Phi) is minus the physical acceleration (the sign does not enter mu(|F|)).
Phi = -1/r + g_e z + psi;  external Newtonian field y_e, total g_e = nu(y_e) y_e (same in AQUAL and QUMOND).

AQUAL (the action's equation, see derivation):  div[mu(|F|) F] = div F_N
    <=>  L psi = D[ (1 - mu(|F|)) F - (F_a - F_N) ],  F = F_a + grad psi,  F_a = r_hat/r^2 + g_e z_hat
QUMOND (phantom-as-gravity):                     div F = div[nu(|F_N|) F_N]
    <=>  L psi = D[ w(|F_N|) F_N - (F_a - F_N) ]     (one linear solve)
Finite volume on (ln r, theta); L = discrete Laplacian (LU once); AQUAL by Anderson-accelerated fixed point.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from numpy.polynomial import legendre as npleg

np.seterr(all='ignore')  # macOS Accelerate emits spurious matmul warnings; results are checked by K2-K8


def _trap(f, x):
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(x)))


# ----------------------------------------------------------------------------- laws
class Law:
    """A law nu(y) = 1 + w(y) (y = |g_N|/a0) and its AQUAL form 1 - mu(x) (x = |g|/a0), x = y nu(y)."""

    def __init__(self, w, one_minus_mu=None, name=""):
        self.w = w
        self.name = name
        self._omm = one_minus_mu
        ly = np.linspace(-46.0, 46.0, 92001)
        y = np.exp(ly)
        self._ly = ly
        self._lx = ly + np.log1p(w(y))

    def y_of_x(self, x):
        lx = np.log(np.maximum(x, 1e-300))
        ly = np.interp(lx, self._lx, self._ly)
        for _ in range(3):                       # Newton on ln y: f = ly + log1p(w) - lx
            y = np.exp(ly)
            h = 1e-6
            f0 = ly + np.log1p(self.w(y)) - lx
            f1 = (ly + h) + np.log1p(self.w(y * np.exp(h))) - lx
            ly = ly - f0 * h / (f1 - f0)
        return np.exp(ly)

    def one_minus_mu(self, x):
        if self._omm is not None:
            return self._omm(x)
        y = self.y_of_x(x)
        wy = self.w(y)
        return wy / (1.0 + wy)

    def nu(self, y):
        return 1.0 + self.w(y)

    def dlnmu_dlnx(self, x, h=1e-5):
        m = lambda t: np.log1p(-self.one_minus_mu(t))
        return (m(x * np.exp(h)) - m(x * np.exp(-h))) / (2 * h)

    def dlnnu_dlny(self, y, h=1e-5):
        n = lambda t: np.log1p(self.w(t))
        return (n(y * np.exp(h)) - n(y * np.exp(-h))) / (2 * h)

    def total_from_newton(self, y):
        return y * self.nu(y)

    def newton_from_total(self, x):
        return self.y_of_x(x)


def _y(y):
    return np.maximum(np.asarray(y, float), 1e-300)


def w_cap(n):
    """capacity family u^2 + n g_N u = a0 g_N; n = 1 is the canonical law."""
    def w(y):
        y = _y(y)
        return 2.0 / (y * (np.sqrt(n * n + 4.0 / y) + n))
    return w


def omm_cap(n):
    def f(x):
        x = np.asarray(x, float)
        return 2.0 / ((n * x + 1.0) + np.sqrt((n * x - 1.0) ** 2 + 4.0 * x))
    return f


def w_beta(b):
    def w(y):
        y = _y(y)
        return np.expm1(np.log1p(y ** (-b)) / (2.0 * b))
    return w


def w_standard(y):
    y = _y(y)
    return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y ** 2))) - 1.0


def omm_standard(x):
    x = np.asarray(x, float)
    s = np.sqrt(1.0 + x * x)
    return 1.0 / (s * (s + x))


def w_turnoff(base_w, yt):
    if yt is None:
        return base_w
    return lambda y: base_w(y) / (1.0 + (np.asarray(y, float) / yt) ** 2)


def law_canonical(yt=None):
    if yt is None:
        return Law(w_cap(1.0), omm_cap(1.0), "n=1")
    return Law(w_turnoff(w_cap(1.0), yt), None, f"n=1,yt={yt}")


# ----------------------------------------------------------------------------- grid + solver
class AxiSolver:
    def __init__(self, law, y_e, Nr_per_dec=40, Nt=64, r_in=1e-5, r_out=1e4, Lmax_bc=16, mode="AQUAL"):
        self.law, self.mode = law, mode
        self.y_e = float(y_e)
        self.g_e = float(law.total_from_newton(y_e)) if y_e > 0 else 0.0
        ndec = np.log10(r_out / r_in)
        Nr = int(round(Nr_per_dec * ndec))
        self.Nr, self.Nt = Nr, Nt
        dxi = np.log(r_out / r_in) / (Nr - 1)
        xi = np.log(r_in) + dxi * np.arange(Nr)
        r = np.exp(xi)
        self.r, self.dxi = r, dxi
        rf = np.exp(xi[:-1] + 0.5 * dxi)                        # radial faces between i and i+1
        dth = np.pi / Nt
        th = (np.arange(Nt) + 0.5) * dth
        thf = np.arange(1, Nt) * dth                            # interior theta faces between j and j+1
        self.th, self.dth, self.rf, self.thf = th, dth, rf, thf
        ct_lo, ct_hi = np.cos(th - 0.5 * dth), np.cos(th + 0.5 * dth)
        self.Ar = 2 * np.pi * rf[:, None] ** 2 * (ct_lo - ct_hi)[None, :]               # (Nr-1, Nt)
        rlo = np.exp(xi - 0.5 * dxi)
        rhi = np.exp(xi + 0.5 * dxi)
        self.At = 2 * np.pi * np.sin(thf)[None, :] * (0.5 * (rhi ** 2 - rlo ** 2))[:, None]  # (Nr, Nt-1)
        self.dr = r[1:] - r[:-1]
        # Legendre BC matrices
        mu_c = np.cos(th)
        Lb = min(Lmax_bc, Nt - 1)
        P = np.stack([npleg.legval(mu_c, np.eye(Lb + 1)[l]) for l in range(Lb + 1)], axis=1)  # (Nt, Lb+1)
        self.Pfit = P
        pinv = np.linalg.pinv(P)
        ratio = (r[0] / r[1]) ** np.arange(Lb + 1)
        self.M_in = P @ np.diag(ratio) @ pinv                   # psi_0 = M_in (psi_1 - d0) + (l=0 shift)
        # isolated l=0 increment psi0(r1) - psi0(r0) = int w(1/r^2)/r^2 dr  (anomalous radial field)
        rr = np.exp(np.linspace(np.log(r[0]), np.log(r[1]), 2001))
        f = law.w(1.0 / rr ** 2) / rr ** 2 * rr
        self.d0 = float(_trap(f, np.log(rr)))
        self._build_L()
        self._outer()

    # index helpers
    def idx(self, i, j):
        return i * self.Nt + j

    def _build_L(self):
        Nr, Nt = self.Nr, self.Nt
        rows, cols, vals = [], [], []
        I = np.arange(1, Nr - 1)
        for j in range(Nt):
            pass
        # interior cells i=1..Nr-2
        ii, jj = np.meshgrid(np.arange(1, Nr - 1), np.arange(Nt), indexing="ij")
        ii, jj = ii.ravel(), jj.ravel()
        k = ii * Nt + jj
        diag = np.zeros_like(k, dtype=float)
        # radial faces
        cp = self.Ar[ii, jj] / self.dr[ii]            # face i+1/2
        cm = self.Ar[ii - 1, jj] / self.dr[ii - 1]    # face i-1/2
        rows += [k, k]; cols += [k + Nt, k - Nt]; vals += [cp, cm]
        diag -= cp + cm
        # theta faces
        has_p = jj < Nt - 1
        has_m = jj > 0
        tp = np.where(has_p, self.At[ii, np.minimum(jj, Nt - 2)] / (self.r[ii] * self.dth), 0.0)
        tm = np.where(has_m, self.At[ii, np.maximum(jj - 1, 0)] / (self.r[ii] * self.dth), 0.0)
        rows += [k[has_p], k[has_m]]; cols += [k[has_p] + 1, k[has_m] - 1]; vals += [tp[has_p], tm[has_m]]
        diag -= tp + tm
        rows.append(k); cols.append(k); vals.append(diag)
        # inner BC rows: psi_0 - M_in psi_1 = -(M_in applied to l=0 shift) handled in rhs
        for j in range(Nt):
            rows.append(np.array([j])); cols.append(np.array([j])); vals.append(np.array([1.0]))
            rows.append(np.full(Nt, j)); cols.append(Nt + np.arange(Nt)); vals.append(-self.M_in[j])
        # outer Dirichlet
        ko = (Nr - 1) * Nt + np.arange(Nt)
        rows.append(ko); cols.append(ko); vals.append(np.ones(Nt))
        A = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(Nr * Nt, Nr * Nt))
        self.Lmat = A
        self.lu = spla.splu(A)

    def _outer(self):
        r, th = self.r[-1], self.th
        law = self.law
        if self.y_e <= 0:
            self.psi_out = np.zeros(self.Nt)  # isolated: anomalous potential ~ ln r (deep), set below
            # isolated deep-MOND tail: psi = ln r + const relative to -1/r; use exact algebraic integral
            rr = np.exp(np.linspace(np.log(self.r[0]), np.log(r), 20001))
            f = law.w(1.0 / rr ** 2) / rr ** 2 * rr
            self.psi_out[:] = float(_trap(f, np.log(rr)))
            self.outer_absolute = True
            return
        self.outer_absolute = False
        if self.mode == "AQUAL":
            x_e = self.g_e
            mu_e = 1.0 - float(law.one_minus_mu(np.array([x_e]))[0])
            L0 = float(law.dlnmu_dlnx(np.array([x_e]))[0])
            R = r * np.sqrt(np.sin(th) ** 2 + np.cos(th) ** 2 / (1.0 + L0))
            phi = -1.0 / (mu_e * np.sqrt(1.0 + L0) * R)
        else:
            nu_e = float(law.nu(np.array([self.y_e]))[0])
            K = float(law.dlnnu_dlny(np.array([self.y_e]))[0])
            phi = nu_e * (-1.0 / r - K * np.sin(th) ** 2 / (2.0 * r))
        self.psi_out = phi + 1.0 / r

    # ---- face fields
    def _face_fields(self, psi):
        """Return (F_r, F_t) at radial faces (Nr-1,Nt) and at theta faces (Nr,Nt-1), F = F_a + grad psi."""
        Nr, Nt, r, th = self.Nr, self.Nt, self.r, self.th
        P = psi.reshape(Nr, Nt)
        ge = self.g_e
        # centred derivatives at cell centres
        dpt = np.empty_like(P)
        dpt[:, 1:-1] = (P[:, 2:] - P[:, :-2]) / (2 * self.dth)
        dpt[:, 0] = (P[:, 1] - P[:, 0]) / (2 * self.dth)
        dpt[:, -1] = (P[:, -1] - P[:, -2]) / (2 * self.dth)
        dpt /= r[:, None]
        dpr = np.empty_like(P)
        dpr[1:-1] = (P[2:] - P[:-2]) / (r[2:] - r[:-2])[:, None]
        dpr[0] = (P[1] - P[0]) / (r[1] - r[0])
        dpr[-1] = (P[-1] - P[-2]) / (r[-1] - r[-2])
        # radial faces
        rf = self.rf[:, None]
        Fr_r = 1.0 / rf ** 2 + ge * np.cos(th)[None, :] + (P[1:] - P[:-1]) / self.dr[:, None]
        Ft_r = -ge * np.sin(th)[None, :] + 0.5 * (dpt[1:] + dpt[:-1])
        # theta faces
        rc = r[:, None]
        thf = self.thf[None, :]
        Fr_t = 1.0 / rc ** 2 + ge * np.cos(thf) + 0.5 * (dpr[:, 1:] + dpr[:, :-1])
        Ft_t = -ge * np.sin(thf) + (P[:, 1:] - P[:, :-1]) / (rc * self.dth)
        return Fr_r, Ft_r, Fr_t, Ft_t

    def _T(self, psi):
        """T = (1-mu)F - (F_a - F_N)  [AQUAL]  or  w(|F_N|)F_N - (F_a - F_N)  [QUMOND], normal comps at faces."""
        th, thf = self.th[None, :], self.thf[None, :]
        dg = self.g_e - self.y_e
        if self.mode == "AQUAL":
            Fr_r, Ft_r, Fr_t, Ft_t = self._face_fields(psi)
            m_r = self.law.one_minus_mu(np.sqrt(Fr_r ** 2 + Ft_r ** 2))
            m_t = self.law.one_minus_mu(np.sqrt(Fr_t ** 2 + Ft_t ** 2))
            Tr = m_r * Fr_r - dg * np.cos(th)
            Tt = m_t * Ft_t + dg * np.sin(thf)
        else:
            rf, rc = self.rf[:, None], self.r[:, None]
            Nr_r = 1.0 / rf ** 2 + self.y_e * np.cos(th)
            Nt_r = -self.y_e * np.sin(th) * np.ones_like(Nr_r)
            Nr_t = 1.0 / rc ** 2 + self.y_e * np.cos(thf)
            Nt_t = -self.y_e * np.sin(thf) * np.ones_like(Nr_t)
            w_r = self.law.w(np.sqrt(Nr_r ** 2 + Nt_r ** 2))
            w_t = self.law.w(np.sqrt(Nr_t ** 2 + Nt_t ** 2))
            Tr = w_r * Nr_r - dg * np.cos(th)
            Tt = w_t * Nt_t + dg * np.sin(thf)
        return Tr, Tt

    def _rhs(self, psi):
        Nr, Nt = self.Nr, self.Nt
        Tr, Tt = self._T(psi)
        fr = Tr * self.Ar              # (Nr-1, Nt) outward for cell i at face i+1/2
        ft = Tt * self.At              # (Nr, Nt-1)
        D = np.zeros((Nr, Nt))
        D[:-1] += fr
        D[1:] -= fr
        D[:, :-1] += ft
        D[:, 1:] -= ft
        b = D.ravel().copy()
        # inner BC rows: psi_0 - M_in psi_1 = -d0  (l=0 shift: psi_0 = psi_1 - d0 in the l=0 mode; M_in keeps l=0 with ratio 1)
        b[:Nt] = -self.d0
        b[(Nr - 1) * Nt:] = self.psi_out
        return b

    def G(self, psi):
        return self.lu.solve(self._rhs(psi))

    def solve(self, tol=1e-13, maxit=400, m=6, psi0=None, verbose=False):
        if self.mode == "QUMOND":
            self.psi = self.G(np.zeros(self.Nr * self.Nt))
            self.iters, self.last_rel = 1, 0.0
            return self.psi
        x = self.G(np.zeros(self.Nr * self.Nt)) if psi0 is None else psi0
        X, Fh = [], []
        hist = []
        for it in range(maxit):
            g = self.G(x)
            f = g - x
            X.append(x.copy()); Fh.append(f.copy())
            if len(X) > m + 1:
                X.pop(0); Fh.pop(0)
            nrm = np.max(np.abs(f)) / max(1.0, np.max(np.abs(x[self.Nt:])))
            hist.append(nrm)
            if verbose and it % 10 == 0:
                print(it, nrm)
            if nrm < tol:
                x = g
                break
            if len(X) > 1:
                dF = np.stack([Fh[k + 1] - Fh[k] for k in range(len(Fh) - 1)], axis=1)
                dX = np.stack([X[k + 1] - X[k] for k in range(len(X) - 1)], axis=1)
                gam, *_ = np.linalg.lstsq(dF, f, rcond=None)
                x = x + f - (dX + dF) @ gam
            else:
                x = g
        self.psi = x
        self.iters, self.last_rel = it + 1, hist[-1]
        self.hist = hist
        return x

    # ---- outputs
    def legendre_modes(self, psi=None, L=8):
        psi = self.psi if psi is None else psi
        P = psi.reshape(self.Nr, self.Nt)
        B = np.stack([npleg.legval(np.cos(self.th), np.eye(L + 1)[l]) for l in range(L + 1)], axis=1)
        c, *_ = np.linalg.lstsq(B, P.T, rcond=None)
        return c.T                    # (Nr, L+1)

    def q2(self, rfit=(1e-3, 3e-2), r_eval=None):
        """dimensionless Q2 (units a0/r_M), BN11 sign: dU = (1/2)Q2(z^2 - r^2/3), U = -Phi."""
        c = self.legendre_modes()
        r = self.r
        sel = (r >= rfit[0]) & (r <= rfit[1])
        yv = c[sel, 2] / r[sel] ** 2
        A = np.stack([np.ones(sel.sum()), r[sel], r[sel] ** 2], axis=1)
        co, *_ = np.linalg.lstsq(A, yv, rcond=None)
        q0 = -3.0 * co[0]
        if r_eval is not None:
            qe = -3.0 * np.interp(r_eval, r, c[:, 2] / r ** 2)
            return q0, qe
        return q0

    def field_at(self, rr, tt):
        """anomalous field F - F_N,pt - g_e z_hat = grad psi at (r, theta) by bilinear interpolation of centred derivs."""
        Nr, Nt = self.Nr, self.Nt
        P = self.psi.reshape(Nr, Nt)
        from scipy.interpolate import RectBivariateSpline
        # extend theta to include poles by symmetry
        th = np.concatenate([[-self.th[0]], self.th, [2 * np.pi - self.th[-1]]])
        PP = np.concatenate([P[:, :1], P, P[:, -1:]], axis=1)
        S = RectBivariateSpline(np.log(self.r), th, PP, kx=3, ky=3)
        lr = np.log(rr)
        dr_ = S(lr, tt, dx=1, grid=False) / rr
        dt_ = S(lr, tt, dy=1, grid=False) / rr
        return dr_, dt_

    def transverse_fraction(self, r_probe=1.0):
        """C = mu(|F|)F - F_N on the radial faces nearest r_probe (AQUAL: div C = 0 but C != 0; QUMOND's
        assumption is the curl-free h). Returns max|C| / max|F - F_N| on that shell, and max|F - F_N|."""
        Fr_r, Ft_r, Fr_t, Ft_t = self._face_fields(self.psi)
        i = int(np.argmin(np.abs(np.log(self.rf) - np.log(r_probe))))
        th = self.th
        Fr, Ft = Fr_r[i], Ft_r[i]
        x = np.sqrt(Fr ** 2 + Ft ** 2)
        mu = 1.0 - self.law.one_minus_mu(x)
        Nr_ = 1.0 / self.rf[i] ** 2 + self.y_e * np.cos(th)
        Nt_ = -self.y_e * np.sin(th)
        C = np.sqrt((mu * Fr - Nr_) ** 2 + (mu * Ft - Nt_) ** 2)
        An = np.sqrt((Fr - Nr_) ** 2 + (Ft - Nt_) ** 2)
        return float(np.max(C) / np.max(An)), float(np.max(An))
