"""EUC5R model machinery (own code; nothing imported from EUC1/EUC4/EUC5/EUC7).

Units: kpc, km/s, Msun.  g in (km/s)^2/kpc.
Spherical Sersic body (Prugniel-Simien deprojection), law S / law B, constant-beta Jeans,
luminosity-weighted second moment through a circular fibre after a Gaussian PSF,
projected lensing mass M_2D(<R) = (R^2/G) int_R^rmax g dr / sqrt(r^2-R^2).
"""
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul")
from scipy.special import gammainc, i0e
from scipy.integrate import quad
from scipy.optimize import brentq

G = 4.300917270e-6            # kpc (km/s)^2 / Msun
C_KMS = 299792.458
KPC_M = 3.0856775814913673e19
ARCSEC = math.pi / (180.0 * 3600.0)
A0_CANON = 9.3603e-11
A0_ALT = 1.132e-10


def a0_units(a0_si):
    """m/s^2 -> (km/s)^2/kpc"""
    return a0_si * KPC_M / 1.0e6


# ------------------------------------------------------------------ cosmology (flat, radiation neglected)
class Cosmo:
    def __init__(self, H0, Om):
        self.H0, self.Om = H0, Om
        self._cache = {}

    def DC(self, z):
        key = round(float(z), 10)
        if key not in self._cache:
            f = lambda x: 1.0 / math.sqrt(self.Om * (1 + x) ** 3 + 1 - self.Om)
            if z > 20:
                v = quad(f, 0, 20, limit=400)[0] + quad(f, 20, z, limit=400)[0]
            else:
                v = quad(f, 0, z, limit=400)[0]
            self._cache[key] = (C_KMS / self.H0) * 1e3 * v      # kpc
        return self._cache[key]

    def DA(self, z):
        return self.DC(z) / (1 + z)

    def DL(self, z):
        return self.DC(z) * (1 + z)

    def DAls(self, zl, zs):
        return (self.DC(zs) - self.DC(zl)) / (1 + zs)

    def sigcr(self, zl, zs):
        """Msun / kpc^2"""
        return C_KMS ** 2 / (4 * math.pi * G) * self.DA(zs) / (self.DA(zl) * self.DAls(zl, zs))


ECLIPSE_COSMO = Cosmo(67.74, 0.3089)
AUGER_COSMO = Cosmo(70.0, 0.3)


# ------------------------------------------------------------------ Sersic / Prugniel-Simien
def b_ser(n):
    return 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n) + 131.0 / (1148175.0 * n ** 3)


def p_ps(n):
    return 1.0 - 0.6097 / n + 0.05463 / (n * n)


def nu_ps(r, Re, n):
    x = np.asarray(r, float) / Re
    return x ** (-p_ps(n)) * np.exp(-b_ser(n) * x ** (1.0 / n))


def m3frac(r, Re, n):
    x = np.asarray(r, float) / Re
    return gammainc(n * (3.0 - p_ps(n)), b_ser(n) * x ** (1.0 / n))


# ------------------------------------------------------------------ laws
def law(gN, a0u, which="S"):
    gN = np.maximum(np.asarray(gN, float), 1e-300)
    if which == "S":
        return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0u / gN))
    if which == "B":
        return np.sqrt(gN * gN + a0u * gN)
    if which == "N":
        return gN
    raise ValueError(which)


# ------------------------------------------------------------------ PSF-convolved circular aperture weight
_GLx, _GLw = np.polynomial.legendre.leggauss(200)


def aperture_weight(R, Rap, s):
    """fraction of light emitted at projected radius R that lands inside a circle of radius Rap
    after a circular Gaussian PSF of dispersion s."""
    R = np.atleast_1d(np.asarray(R, float))
    if s <= 0:
        return (R < Rap).astype(float)
    xp = 0.5 * (_GLx + 1) * Rap
    wp = 0.5 * _GLw * Rap
    RR, XP = np.meshgrid(R, xp, indexing="ij")
    integ = XP / s ** 2 * np.exp(-(RR - XP) ** 2 / (2 * s * s)) * i0e(RR * XP / s ** 2)
    return integ @ wp


# ------------------------------------------------------------------ Jeans kernel
class JeansKernel:
    """sigma_ap^2 = (K . g) / D, linear in the acceleration g sampled on the radius grid self.r.

    nu_fn(r): tracer density (any normalisation).  beta: constant anisotropy.
    Rap, s: fibre radius and PSF dispersion (kpc).  If Rs is given instead, returns the point projected
    dispersion at each R in Rs (no aperture) through point_kernels().
    """

    def __init__(self, nu_fn, beta, rmin, rmax, N=1200, nu_gl=240):
        self.beta = beta
        self.r = np.logspace(math.log10(rmin), math.log10(rmax), N)
        self.lr = np.log(self.r)
        self.h = self.lr[1] - self.lr[0]
        self.nu = nu_fn(self.r)
        self.nu_fn = nu_fn
        self.rmin, self.rmax, self.N = rmin, rmax, N
        gx, gw = np.polynomial.legendre.leggauss(nu_gl)
        self.gx, self.gw = 0.5 * (gx + 1), 0.5 * gw
        # P_i = r_i^{-2b} * h * sum_{j>=i} omega_ij * nu_j g_j r_j^{2b+1}   (trapezoid in ln r)
        N_ = N
        A = np.triu(np.ones((N_, N_)))
        A[np.arange(N_), np.arange(N_)] = 0.5
        A[:, -1] = 0.5
        A[-1, -1] = 0.0
        self.A = A * self.h            # P = diag(r^-2b) A diag(nu r^{2b+1}) g

    def _proj_rows(self, R):
        """for each R: nodes r_km, weights for int_R^rmax f(r) r dr/sqrt(r^2-R^2) = int_0^U f(R cosh u) R cosh u du"""
        R = np.atleast_1d(R)
        U = np.arccosh(np.maximum(self.rmax / R, 1.0 + 1e-12))
        u = self.gx[None, :] * U[:, None]
        w = self.gw[None, :] * U[:, None]
        rk = R[:, None] * np.cosh(u)
        return rk, w, u

    def _interp_matrix_apply(self, rk, coef):
        """returns vector c over grid with sum_k coef_k * P(rk_k) = c . P (linear interp in ln r)."""
        x = (np.log(np.clip(rk, self.rmin, self.rmax)) - self.lr[0]) / self.h
        i0 = np.clip(np.floor(x).astype(int), 0, self.N - 2)
        t = x - i0
        c = np.zeros(self.N)
        np.add.at(c, i0.ravel(), (coef * (1 - t)).ravel())
        np.add.at(c, (i0 + 1).ravel(), (coef * t).ravel())
        return c

    def moments_point(self, R, g):
        """Sigma(R) and Sigma*sigma_los^2(R) at radii R for the acceleration g on the grid (direct)."""
        b = self.beta
        P = self.r ** (-2 * b) * (self.A @ (self.nu * self.r ** (2 * b + 1) * g))
        rk, w, u = self._proj_rows(R)
        Sig = 2 * np.sum(w * self.nu_fn(rk) * rk, axis=1)
        Pk = np.exp(np.interp(np.log(rk), self.lr, np.log(np.maximum(P, 1e-300))))
        SS = 2 * np.sum(w * (1 - b / np.cosh(u) ** 2) * Pk * rk, axis=1)
        return Sig, SS

    def aperture_kernel(self, Rap, s, nR=160):
        """returns (K, D): sigma_ap^2 = K.g / D."""
        b = self.beta
        Rhi = Rap + 7.0 * s if s > 0 else Rap
        Rg = np.logspace(math.log10(self.rmin * 1.0001), math.log10(min(Rhi, self.rmax / 2)), nR)
        hR = math.log(Rg[1] / Rg[0])
        wR = np.full(nR, hR)
        wR[0] *= 0.5
        wR[-1] *= 0.5
        W = aperture_weight(Rg, Rap, s)
        alpha = 2 * math.pi * wR * Rg * Rg * W         # int W(R) X(R) 2 pi R dR in ln R
        rk, w, u = self._proj_rows(Rg)
        Sig = 2 * np.sum(w * self.nu_fn(rk) * rk, axis=1)
        D = float(np.sum(alpha * Sig))
        coef = alpha[:, None] * 2 * w * (1 - b / np.cosh(u) ** 2) * rk
        c = self._interp_matrix_apply(rk, coef)          # numerator = c . P
        cP = c * self.r ** (-2 * b)
        K = (cP @ self.A) * self.nu * self.r ** (2 * b + 1)
        return K, D


# ------------------------------------------------------------------ a lens
class SersicLens:
    def __init__(self, Mstar, Re, n, beta=0.0, N=1200):
        self.M, self.Re, self.n = Mstar, Re, n
        nf = lambda r: nu_ps(r, Re, n)
        self.jk = JeansKernel(nf, beta, 1e-4 * Re, 400.0 * Re, N=N)
        self.m3 = m3frac(self.jk.r, Re, n)
        self._K = {}

    def g_grid(self, B, a0u, which):
        gN = G * B * self.M * self.m3 / self.jk.r ** 2
        return law(gN, a0u, which)

    def kernel(self, Rap, s):
        key = (round(Rap, 8), round(s, 8))
        if key not in self._K:
            self._K[key] = self.jk.aperture_kernel(Rap, s)
        return self._K[key]

    def sigma_ap(self, B, a0u, which, Rap, s):
        K, D = self.kernel(Rap, s)
        return math.sqrt(max(K @ self.g_grid(B, a0u, which) / D, 0.0))

    def b_dyn(self, sigma, a0u, which, Rap, s, lo=-1.5, hi=1.5):
        f = lambda lb: self.sigma_ap(10 ** lb, a0u, which, Rap, s) - sigma
        flo, fhi = f(lo), f(hi)
        if flo >= 0:
            return lo, "low_end"
        if fhi <= 0:
            return hi, "high_end"
        return brentq(f, lo, hi, xtol=1e-6), "ok"


# ------------------------------------------------------------------ lensing projection
_LGx, _LGw = np.polynomial.legendre.leggauss(400)
_LGx, _LGw = 0.5 * (_LGx + 1), 0.5 * _LGw


def M2D_law(R, Mtot, Re, n, a0u, which, rmax=1.0e6, m3=None):
    """projected total mass inside R (Msun) from the total acceleration (R in kpc)."""
    U = math.acosh(max(rmax / R, 1.0 + 1e-12))
    r = R * np.cosh(_LGx * U)
    mf = m3frac(r, Re, n) if m3 is None else m3(r)
    g = law(G * Mtot * mf / r ** 2, a0u, which)
    return R * R / G * float(np.sum(_LGw * g) * U)


def b_lens(Mstar, Re, n, RE, sigcr, a0u, which, lo=-3.0, hi=3.0):
    target = math.pi * RE * RE * sigcr
    f = lambda lb: M2D_law(RE, 10 ** lb * Mstar, Re, n, a0u, which) - target
    flo, fhi = f(lo), f(hi)
    if flo >= 0:
        return lo
    if fhi <= 0:
        return hi
    return brentq(f, lo, hi, xtol=1e-7)
