"""CFG653 core: spherical reimplementation of astra's variational nonlocal response (sol61_push/nonlocal_response_2026_10_12).

Equation (C = 4 pi G, a0 = 1 units; inward magnitudes):  g = g_N + H_L[ p(|zeta|) sgn zeta ],  zeta = H_L[g],
with H_L = 1 - (componentwise Gaussian smoothing of width L) acting on radial vector fields and p(g) = g - B(g).
Worked on the enclosed-'mass' function m = r^2 g, where the smoothing is exact through the analytic enclosed fraction of
a Gaussian-smoothed thin shell (FROZEN_CRITERIA.md section 2).  Local limit (H = 1): B(g) = g_N, the law.
"""
import os
for _n in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_n, "1")
import sys
import io
import contextlib
import math
import numpy as np
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C

# ------------------------------------------------------------------ the law (nu_mono, FP1's committed table), a0 = 1 units
_LY = np.linspace(-12.0, 12.0, 240001)
_Y = 10.0 ** _LY
_F = _Y * C.nu_mono(_Y)                       # g = F(y_N)
_LF = np.log10(_F)
_dF = np.gradient(_F, _Y)                     # F'(y) > 1
_P = _F - _Y                                  # p(g) = g - B(g) on the table
_PP = 1.0 - 1.0 / _dF                         # p'(g) = 1 - B'(g)
assert np.all(np.diff(_LF) > 0)


def F_law(y):
    """the local law g = F(y_N) (a0 = 1); deep analytic sqrt(y) below the table."""
    y = np.asarray(y, float)
    return np.where(y < _Y[0], np.sqrt(np.maximum(y, 0.0)), np.interp(np.log10(np.maximum(y, 1e-300)), _LY, _F))


def B_inv(g):
    """B(g) = F^{-1}(g): the Newtonian field the law maps to g."""
    g = np.asarray(g, float)
    deep = g * g
    return np.where(g < _F[0], deep, 10.0 ** np.interp(np.log10(np.maximum(g, 1e-300)), _LF, _LY))


def p_and_dp(g):
    """p(g) = g - B(g) and p'(g) for g >= 0 (deep analytic B = g^2 below the table)."""
    g = np.asarray(g, float)
    lg = np.log10(np.maximum(g, 1e-300))
    lo = g < _F[0]
    p = np.where(lo, g - g * g, np.interp(lg, _LF, _P))
    dp = np.where(lo, 1.0 - 2.0 * g, np.interp(lg, _LF, _PP))
    return p, np.clip(dp, 0.0, 1.0)


# ------------------------------------------------------------------ the Gaussian filter on enclosed-mass functions
def shell_frac(r, a, L):
    """fraction of a unit thin shell of radius a, after 3D Gaussian smoothing of width L, that lies inside radius r."""
    s = L * math.sqrt(2.0)
    t1 = 0.5 * (erfc((a - r) / s) - erfc((a + r) / s))
    ex = np.exp(-((r - a) ** 2) / (2 * L * L)) * (-np.expm1(-2.0 * r * a / (L * L)))
    return t1 - L / (np.maximum(a, 1e-300) * math.sqrt(2 * math.pi)) * ex


def point_frac(r, L):
    x = r / L
    return erfc(-x / math.sqrt(2.0)) - 1.0 - math.sqrt(2.0 / math.pi) * x * np.exp(-0.5 * x * x)


def smoothing_matrix(r, L):
    """Wt such that m_smoothed = Wt @ m (m = r^2 g on the grid r; mass beyond r[-1] is absent; m[0] is a point at 0)."""
    r = np.asarray(r, float)
    a = np.sqrt(r[1:] * r[:-1])
    Wsh = shell_frac(r[:, None], a[None, :], L)
    N = len(r)
    Wt = np.zeros((N, N))
    Wt[:, 0] = point_frac(r, L) - Wsh[:, 0]
    Wt[:, 1:-1] = Wsh[:, :-1] - Wsh[:, 1:]
    Wt[:, -1] = Wsh[:, -1]
    return Wt


def make_grid(L, r_data=None, rmin=1e-3, per_dec=40, rmax_min=1e3):
    rmax = max(rmax_min, 30.0 * L) if np.isfinite(L) else rmax_min
    n = int(math.ceil(per_dec * math.log10(rmax / rmin))) + 1
    r = np.geomspace(rmin, rmax, n)
    if r_data is not None:
        rd = np.unique(np.asarray(r_data, float))
        near = np.min(np.abs(np.log(r[:, None] / rd[None, :])), axis=1) < 0.002   # drop grid nodes within 0.2% of data
        r = np.unique(np.concatenate([r[~near], rd]))
    return r


class Filter:
    """A = I - Wt on a given grid (or the local limit A = I when L is None / infinite, or A = 0 when L == 0)."""

    def __init__(self, r, L):
        self.r = np.asarray(r, float)
        self.L = L
        N = len(self.r)
        if L is None or not np.isfinite(L):
            self.A = np.eye(N)
        elif L <= 0:
            self.A = np.zeros((N, N))
        else:
            self.A = np.eye(N) - smoothing_matrix(self.r, L)

    def solve(self, mN, m0=None, tol=1e-8, maxit=60):
        """solve m = mN + A f(A m), f(mz) = r^2 p(|z|) sgn z, z = mz / r^2.  Returns m (= r^2 g) and zeta."""
        r2 = self.r ** 2
        A = self.A
        m = np.array(mN if m0 is None else m0, float)
        for it in range(maxit):
            mz = A @ m
            z = mz / r2
            p, dp = p_and_dp(np.abs(z))
            res = m - mN - A @ (r2 * p * np.sign(z))
            floor = 1e-6 * np.abs(m).max() + 1e-300
            nr = np.max(np.abs(res) / (np.abs(m) + np.abs(mN) + floor))
            if nr < tol:
                break
            J = np.eye(len(m)) - (A * dp[None, :]) @ A
            dm = np.linalg.solve(J, -res)
            lam = 1.0
            for _ in range(30):
                mt = m + lam * dm
                zt = (A @ mt) / r2
                pt, _ = p_and_dp(np.abs(zt))
                rt = mt - mN - A @ (r2 * pt * np.sign(zt))
                if np.max(np.abs(rt) / (np.abs(mt) + np.abs(mN) + floor)) < nr or lam < 1e-6:
                    break
                lam *= 0.5
            m = mt
        mz = A @ m
        return m, mz / r2, nr, it


def mN_profile(r, r_d, gbar_d):
    """spherical-equivalent baryonic m_N = r^2 g_bar: exact at data radii, log-interpolated between, ~r^3 inside the
    first point, constant beyond the last point."""
    md = r_d ** 2 * gbar_d
    m = np.interp(np.log(r), np.log(r_d), md)
    inner = r < r_d[0]
    m[inner] = md[0] * (r[inner] / r_d[0]) ** 3
    m[r > r_d[-1]] = md[-1]
    return m
