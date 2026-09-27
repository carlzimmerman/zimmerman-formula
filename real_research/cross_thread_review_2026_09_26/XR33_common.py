#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR33_common -- shared machinery for the XR33 lane: galaxy-scale strong lensing (SLACS, S4TM, BELLS, SNELLS) in the
derivation chain's static law.  Units: kpc, Msun, km/s.  Nothing in this module is fitted.

THE CHAIN'S LAW AT LENS SCALES (read from the chain's committed lanes, not re-derived here):
  FP7 R7d  the static law of the AQUAL-type root: psi = Phi, Phi = Phi_N + S phi, div(mu_s(|grad phi|/a0) grad phi) =
           4 pi G S rho with J' = mu_s(x) = x/(1 - 2x) (J = J_P2).  In spherical symmetry the scalar's first integral
           mu_s(x) x = y gives g = g_N + a0 x_P2(y), x_P2(y) = sqrt(y^2 + y) - y: P2, g = sqrt(g_N^2 + g_N a0), EXACTLY.
  FP9 R9e  the yield floor J_Y = J_P2 + 2 y_th sqrt(Y): in spherical symmetry phi' = a0 x_P2(y - y_th) above the yield.
  FP9 R9h  y_th = y_Lambda Omega_L^(-p'), L = L_Lambda Omega_L^(n/2); headline constants read from FP9's results JSON.
  FP2 L6a, FP7 R7p  PPN gamma = 1: light bends in Phi (= Psi); the lensing mass is the dynamical mass.
  FP1 L4e/B3  the heat filter (xi >= 0.024-0.027 pc, FP7 R7f) moves the galaxy-scale law by <= 3e-5 even at xi = 1 pc.
The record's other kernels are carried as labelled sensitivities, never pooled with the chain's P2:
  nu_RAR = 1/(1 - exp(-sqrt y)) (the hunt's Route A kernel, used by the committed h53/h54 SLACS lane) and
  nu_mono (XC4's splice of nu_RAR at y* = 2.3374 onto a logarithmic phantom floor; the 09-26 standing kernel decision).
"""
import os, math, json
import numpy as np
from scipy.special import gammainc, gammaincinv, gamma as GammaF
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import rice

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("XR33_REPO_ROOT", os.path.dirname(os.path.dirname(HERE)))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
DATA = os.path.join(REPO, "real_research", "data")
LANE = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")

# ------------------------------------------------------------------------------------------------ constants (SI -> astro)
G_SI, C_SI = 6.67430e-11, 299792458.0
MSUN_KG = 1.3271244e20 / G_SI                      # IAU 2015 nominal GM_sun / G
KPC_M = 3.0856775814913673e19
G = G_SI * MSUN_KG / (KPC_M * 1e6)                 # kpc (km/s)^2 / Msun  (= 4.30092e-6)
C_KMS = C_SI / 1e3
ARCSEC = math.pi / 648000.0
A_UNIT = KPC_M / 1e6                               # a [m/s^2] * A_UNIT = a [(km/s)^2/kpc]


def a0_footings():
    """both a0 footings from FP0's committed results (canonical 9.3603e-11, alt 1.1312e-10 m/s^2)."""
    A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
    fp0 = os.path.join(CHAIN, "FP0_core_postulates_results.json")
    if os.path.exists(fp0):
        n0 = json.load(open(fp0))["numbers"]
        A0 = {"canonical": float(n0["a0_canonical"]), "alt": float(n0["a0_rho_total"])}
    return A0


# ------------------------------------------------------------------------------------------------ cosmology (flat LCDM background)
class Cosmo:
    """flat FRW with matter + Lambda; the chain's background is GR (FP3 G1a) with a cold dark component (FP3 G1c)."""

    def __init__(self, Om=0.3, h=0.7):
        self.Om, self.h = Om, h
        self.H0 = 100.0 * h                                  # km/s/Mpc
        self._cache = {}

    def E(self, z):
        return math.sqrt(self.Om * (1 + z) ** 3 + 1 - self.Om)

    def DC(self, z):                                          # comoving distance [kpc]
        if z not in self._cache:
            self._cache[z] = (C_KMS / self.H0) * 1e3 * quad(lambda x: 1.0 / self.E(x), 0.0, z, epsabs=0, epsrel=1e-11, limit=200)[0]
        return self._cache[z]

    def DA(self, z):
        return self.DC(z) / (1 + z)

    def DL(self, z):
        return self.DC(z) * (1 + z)

    def DA12(self, z1, z2):
        return (self.DC(z2) - self.DC(z1)) / (1 + z2)

    def Sigma_cr(self, zl, zs):                               # Msun/kpc^2
        return C_KMS ** 2 * self.DA(zs) / (4 * math.pi * G * self.DA(zl) * self.DA12(zl, zs))

    def rho_crit(self, z):                                    # Msun/kpc^3
        Hz = self.H0 * self.E(z) / 1e3                          # km/s/kpc
        return 3 * Hz ** 2 / (8 * math.pi * G)

    def distmod(self, z):
        return 5 * math.log10(self.DL(z) * 1e3 / 10.0)          # DL in pc / 10 pc


# ------------------------------------------------------------------------------------------------ Sersic light, exact deprojection
class Sersic:
    """Sersic index n, unit total luminosity, projected half-light radius R_e = 1.  M2D is the exact incomplete-gamma law;
    rho(x) is the exact Abel deprojection rho(r) = -(1/pi) int_0^inf I'(r cosh t) dt, integrated numerically once."""

    def __init__(self, n=4.0, nx=2400, xmin=1e-6, xmax=3e3, nt=6000):
        self.n = float(n)
        self.b = float(gammaincinv(2 * n, 0.5))
        self.I0 = self.b ** (2 * n) / (2 * math.pi * n * GammaF(2 * n))
        x = np.geomspace(xmin, xmax, nx)
        Xhi = (400.0 / self.b) ** n                              # exp(-400) cut
        rho = np.empty_like(x)
        for i0 in range(0, nx, 200):
            xs = x[i0:i0 + 200][:, None]
            tmax = np.arccosh(np.maximum(Xhi / xs, 1.0 + 1e-12))
            tt = np.linspace(0.0, 1.0, nt)[None, :] * tmax
            X = xs * np.cosh(tt)
            f = (self.b / (self.n * math.pi)) * self.I0 * X ** (1.0 / self.n - 1.0) * np.exp(-self.b * X ** (1.0 / self.n))
            rho[i0:i0 + 200] = np.trapz(f, tt, axis=1)
        self.x, self.rho_t = x, rho
        lnx = np.log(x)
        integrand = 4 * math.pi * x ** 3 * rho
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lnx))])
        slope = 3.0 - (1.0 - 1.0 / self.n)                       # inner M3D ~ x^(2 + 1/n)
        cum = cum + integrand[0] / slope
        self.M3D_t = cum
        self.lnx = lnx
        self.lnrho = np.log(rho)

    def M2D(self, X):
        return gammainc(2 * self.n, self.b * np.asarray(X, dtype=float) ** (1.0 / self.n))

    def I(self, X):                                            # surface brightness, unit total light, R_e = 1
        return self.I0 * np.exp(-self.b * np.asarray(X, dtype=float) ** (1.0 / self.n))

    def rho(self, X):
        X = np.asarray(X, dtype=float)
        lx = np.log(np.clip(X, self.x[0], self.x[-1]))
        out = np.exp(np.interp(lx, self.lnx, self.lnrho))
        return np.where(X > self.x[-1], 0.0, out)

    def M3D(self, X):
        X = np.asarray(X, dtype=float)
        lx = np.log(np.clip(X, self.x[0], self.x[-1]))
        out = np.interp(lx, self.lnx, self.M3D_t)
        inner = self.M3D_t[0] * (np.clip(X, 1e-300, None) / self.x[0]) ** (3.0 - (1.0 - 1.0 / self.n))
        return np.where(X < self.x[0], inner, np.where(X > self.x[-1], self.M3D_t[-1], out))


# ------------------------------------------------------------------------------------------------ kernels: phantom acceleration h(y) = (g - g_N)/a0
def _p2(y, yth=0.0):
    D = np.maximum(np.asarray(y, dtype=float) - yth, 0.0)
    s = np.sqrt(D * D + D)
    h = np.where(D > 0, D / np.maximum(s + D, 1e-300), 0.0)
    ds = np.where(D > 0, (2 * D + 1) / (2 * np.maximum(s, 1e-300)), 0.0)
    dh = np.where(D > 0, ((s + D) - D * (ds + 1)) / np.maximum((s + D) ** 2, 1e-300), 0.0)
    return h, dh


def _hR(y):
    z = np.sqrt(np.maximum(np.asarray(y, dtype=float), 1e-300))
    em = np.expm1(z)
    h = y / em
    dh = (2 * em - z * (1 + em)) / (2 * em ** 2)
    return h, dh


def _mono_constants():
    dhR = lambda y: float(_hR(np.array([y]))[1][0])
    yp = brentq(dhR, 1.5, 4.0, xtol=1e-15)
    hp = float(_hR(np.array([yp]))[0][0])
    delta = 0.05
    ys = brentq(lambda y: dhR(y) - delta * hp / (y + yp), 1.5, yp - 1e-9, xtol=1e-15)
    return yp, hp, delta, ys


YP_MONO, HP_MONO, DELTA_MONO, YS_MONO = _mono_constants()


def _mono(y, yth=0.0):
    y = np.asarray(y, dtype=float)
    hR, dhR = _hR(y)
    hs = float(_hR(np.array([YS_MONO]))[0][0])
    h = np.where(y <= YS_MONO, hR, hs + DELTA_MONO * HP_MONO * np.log((y + YP_MONO) / (YS_MONO + YP_MONO)))
    dh = np.where(y <= YS_MONO, dhR, DELTA_MONO * HP_MONO / (y + YP_MONO))
    return h, dh


def _rar(y, yth=0.0):
    return _hR(y)


KERNELS = {"P2": _p2, "nu_RAR": _rar, "nu_mono": _mono}


# ------------------------------------------------------------------------------------------------ NFW (LCDM control; dark-fluid bracket)
def nfw_m(x):
    return np.log1p(x) - x / (1 + x)


def nfw_M3D(r, rs, rhos):
    return 4 * math.pi * rhos * rs ** 3 * nfw_m(np.asarray(r, dtype=float) / rs)


def nfw_M2D(R, rs, rhos):
    X = np.asarray(R, dtype=float) / rs
    out = np.empty_like(X)
    lo, hi, eq = X < 1 - 1e-8, X > 1 + 1e-8, np.abs(X - 1) <= 1e-8
    out[lo] = np.log(X[lo] / 2) + np.arccosh(1 / X[lo]) / np.sqrt(1 - X[lo] ** 2)
    out[hi] = np.log(X[hi] / 2) + np.arccos(1 / X[hi]) / np.sqrt(X[hi] ** 2 - 1)
    out[eq] = 1 - math.log(2)
    return 4 * math.pi * rhos * rs ** 3 * out


def nfw_rho(r, rs, rhos):
    x = np.asarray(r, dtype=float) / rs
    return rhos / (x * (1 + x) ** 2)


def c200_DM14(M200, z, h):
    """Dutton & Maccio 2014 (MNRAS 441, 3359) NFW c200-M200 relation, M200 in Msun (converted to h^-1 Msun)."""
    b = -0.101 + 0.026 * z
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21)
    return 10 ** (a + b * math.log10(M200 * h / 1e12))


def nfw_from_M200(M200, z, cosmo, c=None):
    c = c200_DM14(M200, z, cosmo.h) if c is None else c
    r200 = (3 * M200 / (4 * math.pi * 200 * cosmo.rho_crit(z))) ** (1 / 3)
    rs = r200 / c
    rhos = M200 / (4 * math.pi * rs ** 3 * nfw_m(c))
    return rs, rhos, c, r200


def moster13_mstar(M200, z):
    """Moster, Naab & White 2013 (MNRAS 428, 3121) stellar-to-halo relation: Chabrier IMF, M200c, masses in Msun."""
    a = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * a)
    N = 0.0351 - 0.0247 * a
    beta = 1.376 - 0.826 * a
    gam = 0.608 + 0.329 * a
    return 2 * N * M200 / ((M200 / M1) ** (-beta) + (M200 / M1) ** gam)


def moster13_halo(mstar_chab, z):
    f = lambda lm: math.log10(moster13_mstar(10 ** lm, z)) - math.log10(mstar_chab)
    return 10 ** brentq(f, 10.5, 16.5, xtol=1e-10)


# ------------------------------------------------------------------------------------------------ the lens model
class LensModel:
    """stars (Sersic, total mass Mstar, R_e) + gas (fraction of the stellar profile) + the chain's phantom (kernel, a0, y_th,
    line-of-sight cut rcut) + optional Newtonian-only extra component (NFW: LCDM halo, or the kernel-invisible retained dark
    fluid).  All radii in kpc, masses in Msun."""

    NU = 3000

    def __init__(self, prof, Re, Mstar, a0_si=0.0, kernel="P2", yth=0.0, gasfrac=0.0, rcut=1e4, extra=None, extra_in_y=False):
        self.prof, self.Re, self.Mstar = prof, Re, Mstar
        self.a0 = a0_si * A_UNIT
        self.kernel, self.yth, self.gasfrac, self.rcut = KERNELS[kernel], yth, gasfrac, rcut
        self.extra, self.extra_in_y = extra, extra_in_y             # extra = (rs, rhos) NFW-shaped

    # baryons
    def Mb(self, r):
        return self.Mstar * (1 + self.gasfrac) * self.prof.M3D(np.asarray(r) / self.Re)

    def rhob(self, r):
        return self.Mstar * (1 + self.gasfrac) * self.prof.rho(np.asarray(r) / self.Re) / self.Re ** 3

    def Mx(self, r):
        return 0.0 if self.extra is None else nfw_M3D(r, *self.extra)

    def rhox(self, r):
        return 0.0 if self.extra is None else nfw_rho(r, *self.extra)

    def g(self, r):
        r = np.asarray(r, dtype=float)
        Mn = self.Mb(r) + (self.Mx(r) if self.extra_in_y else 0.0)
        gN = G * Mn / r ** 2
        out = G * (self.Mb(r) + self.Mx(r)) / r ** 2
        if self.a0 > 0:
            h, _ = self.kernel(gN / self.a0, self.yth)
            out = out + self.a0 * h * (r <= self.rcut)
        return out

    def M2D_star(self, R):
        return self.Mstar * self.prof.M2D(np.atleast_1d(np.asarray(R, dtype=float)) / self.Re)

    def M2D_phantom(self, R):
        """projected phantom mass in the cylinder R (spherical, u-substitution r = R cosh u; cut at rcut)."""
        R = np.atleast_1d(np.asarray(R, dtype=float))
        if self.a0 <= 0:
            return np.zeros_like(R)
        out = np.empty_like(R)
        for i, Ri in enumerate(R):
            umax = math.acosh(max(self.rcut / Ri, 1.0 + 1e-12))
            u = np.linspace(0.0, umax, self.NU)
            r = Ri * np.cosh(u)
            Mn = self.Mb(r) + (self.Mx(r) if self.extra_in_y else 0.0)
            rhon = self.rhob(r) + (self.rhox(r) if self.extra_in_y else 0.0)
            y = G * Mn / (r ** 2 * self.a0)
            h, dh = self.kernel(y, self.yth)
            dy = (G / self.a0) * (4 * math.pi * rhon - 2 * Mn / r ** 3)
            dM = (self.a0 / G) * (2 * r * h + r ** 2 * dh * dy)
            f = dM * (1 - np.tanh(u)) * Ri * np.sinh(u)
            yR = G * (self.Mb(Ri) + (self.Mx(Ri) if self.extra_in_y else 0.0)) / (Ri ** 2 * self.a0)
            hR, _ = self.kernel(np.array([yR]), self.yth)
            Msph = (self.a0 / G) * Ri ** 2 * float(hR[0]) if Ri <= self.rcut else 0.0
            out[i] = Msph + np.trapz(f, u)
        return out

    def M2D_extra(self, R):
        return 0.0 if self.extra is None else nfw_M2D(np.atleast_1d(R), *self.extra)

    def M2D(self, R):
        R = np.atleast_1d(np.asarray(R, dtype=float))
        return self.M2D_star(R) * (1 + self.gasfrac) + self.M2D_phantom(R) + self.M2D_extra(R)


def solve_alpha(prof, Re, Mref, RE, ME, a0_si, kernel="P2", yth=0.0, gasfrac=0.0, rcut=1e4, extra=None, extra_in_y=False,
                lo=-2.0, hi=2.0):
    """IMF normalisation alpha (stellar mass = alpha * Mref) at which the model's projected mass inside the observed
    Einstein radius equals the lensing mass.  Returns nan if no root in [10^lo, 10^hi]."""
    def f(la):
        m = LensModel(prof, Re, 10 ** la * Mref, a0_si, kernel, yth, gasfrac, rcut, extra, extra_in_y)
        return math.log10(float(m.M2D(RE)[0])) - math.log10(ME)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return float("nan")
    return 10 ** brentq(f, lo, hi, xtol=1e-9)


def solve_RE(model, Scr, Rlo=0.05, Rhi=200.0):
    """Einstein radius: mean convergence M2D(R)/(pi Sigma_cr R^2) = 1."""
    f = lambda lR: math.log(float(model.M2D(math.exp(lR))[0]) / (math.pi * Scr * math.exp(2 * lR)))
    a, b = math.log(Rlo), math.log(Rhi)
    if f(a) * f(b) > 0:
        return float("nan")
    return math.exp(brentq(f, a, b, xtol=1e-10))


# ------------------------------------------------------------------------------------------------ Jeans: aperture dispersion
def sigma_aperture(model, Rap_kpc, fwhm_kpc, beta=0.0, nr=1600, nu=1500):
    """luminosity-weighted line-of-sight dispersion inside a circular aperture after Gaussian seeing, for a tracer that
    follows the stellar Sersic light and the potential of `model` (spherical Jeans, constant anisotropy beta)."""
    Re = model.Re
    x = np.geomspace(1e-5, 2.0e3, nr)
    r = x * Re
    nu_t = model.prof.rho(x) / Re ** 3                       # tracer luminosity density (unit total light)
    g = model.g(r)
    f = r ** (2 * beta) * nu_t * g * r                       # integrand in d ln r
    lnr = np.log(r)
    seg = 0.5 * (f[1:] + f[:-1]) * np.diff(lnr)
    I = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    P = r ** (-2 * beta) * I                                  # nu sigma_r^2
    lnP = np.log(np.maximum(P, 1e-300))
    lnnu = np.log(np.maximum(nu_t, 1e-300))
    s = fwhm_kpc / (2 * math.sqrt(2 * math.log(2)))
    Rmax = min(Rap_kpc + 8 * s, 50 * Re)
    RR = np.geomspace(1e-4 * Re, Rmax, 260)
    num = np.empty_like(RR)
    den = np.empty_like(RR)
    umax = np.arccosh(np.maximum(r[-1] / RR, 1.0 + 1e-9))
    for i, Ri in enumerate(RR):
        u = np.linspace(0.0, umax[i], nu)
        ru = Ri * np.cosh(u)
        lru = np.log(ru)
        Pu = np.exp(np.interp(lru, lnr, lnP))
        nuu = np.exp(np.interp(lru, lnr, lnnu))
        num[i] = 2 * np.trapz((1 - beta / np.cosh(u) ** 2) * Pu * Ri * np.cosh(u), u)
        den[i] = 2 * np.trapz(nuu * Ri * np.cosh(u), u)
    w = rice.cdf(Rap_kpc / s, RR / s) if s > 0 else (RR <= Rap_kpc).astype(float)
    sig2 = np.trapz(num * w * RR * RR, np.log(RR)) / np.trapz(den * w * RR * RR, np.log(RR))
    return math.sqrt(sig2)


class Hernquist:
    """Hernquist (1990) profile with unit mass and projected half-mass radius R_e = 1 (a = R_e/1.8153), the stellar model of
    Treu+2010 / Auger+2010.  Same interface as Sersic (rho, M3D, M2D in units of R_e)."""

    def __init__(self):
        self.n = float("nan")
        self.a = 1.0 / 1.8153

    def rho(self, X):
        X = np.maximum(np.asarray(X, dtype=float), 1e-300)
        return self.a / (2 * math.pi * X * (X + self.a) ** 3)

    def M3D(self, X):
        X = np.asarray(X, dtype=float)
        return X ** 2 / (X + self.a) ** 2

    def M2D(self, X):
        s = np.atleast_1d(np.asarray(X, dtype=float)) / self.a
        out = np.empty_like(s)
        lo, hi = s < 1 - 1e-9, s > 1 + 1e-9
        Xs = np.ones_like(s)
        Xs[lo] = np.arccosh(1 / s[lo]) / np.sqrt(1 - s[lo] ** 2)
        Xs[hi] = np.arccos(1 / s[hi]) / np.sqrt(s[hi] ** 2 - 1)
        out[lo | hi] = s[lo | hi] ** 2 * (Xs[lo | hi] - 1) / (1 - s[lo | hi] ** 2)
        out[~(lo | hi)] = 1.0 / 3.0
        return out
