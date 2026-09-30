"""zcommon: shared cosmology and law definitions for lane Z1 (causal-horizon a0(z) tests).  No results here, only definitions.

Background: flat, H(a)^2 = H0^2 [ Or a^-4 + (Om - Or) a^-3 + OL f_DE(a) ],  OL = 1 - Om (flat), f_DE = 1 for w = -1
(w0, wa CPL otherwise: f_DE = a^(-3(1+w0+wa)) exp(-3 wa (1-a))).   Om includes radiation (the p11 convention), so Om_eff = Om - Or.
Planck-2018-like default: H0 = 67.4, Om = 0.315, Or = 9.1e-5.

Declared cutoff candidates (proper lengths, evaluated at cosmic time t(z), a = 1/(1+z)):
  d_p(z)  proper particle horizon   = a c  Int_0^a   da' / (a'^2 H(a'))
  d_e(z)  proper event horizon      = a c  Int_a^inf da' / (a'^2 H(a'))
  d_H(z)  Hubble radius             = c / H(z)
  R*      = c / sqrt(G rho_Lambda)  = (c/H0) sqrt(8 pi / (3 OL))   (z-independent when w = -1)
  2 R*    (the record's premise)
Machian rule: a0 = c^2 / R_c.  Only the SHAPE a0(z)/a0(0) is a test; the level a0(0) is a separate matter (radius vs diameter, Z vs 1).
"""
import math
import numpy as np
from scipy.integrate import quad

C = 2.99792458e8
MPC = 3.0856775814913673e22
GYR = 3.15576e16
G = 6.674e-11
A0_SPARC = 1.0766e-10          # the record's SPARC value used in p11 (5.4% stat, ~12% analysis scatter)
Z_FW = math.sqrt(32 * math.pi / 3)   # 5.7888


class Cosmo:
    def __init__(self, H0=67.4, Om=0.315, Or=9.1e-5, w0=-1.0, wa=0.0, amin=1e-12):
        self.H0 = H0 * 1e3 / MPC
        self.h0kms = H0
        self.Om, self.Or, self.OL = Om, Or, 1.0 - Om
        self.w0, self.wa = w0, wa
        self.amin = amin
        self.Omeff = Om - Or

    def fde(self, a):
        if self.w0 == -1.0 and self.wa == 0.0:
            return 1.0
        return a ** (-3 * (1 + self.w0 + self.wa)) * math.exp(-3 * self.wa * (1 - a))

    def E(self, a):
        return math.sqrt(self.Or / a ** 4 + self.Omeff / a ** 3 + self.OL * self.fde(a))

    def Ez(self, z):
        return self.E(1.0 / (1.0 + z))

    # comoving horizons in units of c/H0
    def chi_p(self, a):
        f = lambda la: 1.0 / (math.exp(la) * self.E(math.exp(la)))     # da/(a^2 E) = dlna/(a E)
        return quad(f, math.log(self.amin), math.log(a), limit=400, epsabs=0, epsrel=1e-11)[0]

    def chi_e(self, a):
        f = lambda la: 1.0 / (math.exp(la) * self.E(math.exp(la)))
        head = quad(f, math.log(a), math.log(1e6), limit=400, epsabs=0, epsrel=1e-11)[0]
        tail = 1.0 / (1e6 * math.sqrt(self.OL))                          # E -> sqrt(OL) (w = -1), integrand ~ 1/(a E)... da/(a^2 sqrt OL)
        return head + tail

    def dp(self, z):     # proper, units c/H0
        a = 1.0 / (1.0 + z); return a * self.chi_p(a)

    def de(self, z):
        a = 1.0 / (1.0 + z); return a * self.chi_e(a)

    def dH(self, z):
        return 1.0 / self.Ez(z)

    def Rstar(self):     # units c/H0  (rho_Lambda constant)
        return math.sqrt(8 * math.pi / (3 * self.OL))

    def age(self, z):    # t(z) in units 1/H0
        a = 1.0 / (1.0 + z)
        f = lambda la: 1.0 / self.E(math.exp(la))
        return quad(f, math.log(self.amin), math.log(a), limit=400, epsabs=0, epsrel=1e-11)[0]


def laws(cos):
    """z -> a0(z)/a0(0) for each declared candidate (shape only)."""
    dp0, de0 = cos.dp(0.0), cos.de(0.0)
    return {
        "flat (R*, 2R*: z-independent)": lambda z: 1.0,
        "Hubble radius c/H(z)  [a0 = cH(z)/Z]": lambda z: cos.Ez(z),
        "particle horizon d_p (radius OR diameter)": lambda z: dp0 / cos.dp(z),
        "event horizon d_e at t(z)": lambda z: de0 / cos.de(z),
    }


def tratio(z, om=0.315):
    k = math.sqrt((1 - om) / om)
    return math.asinh(k * (1 + z) ** -1.5) / math.asinh(k)


# ---- the LambdaCDM-native emergent scale (L274/L276; PAPER7): E^{4/3} x [c^2/f(c)] with Dutton & Maccio 2014 c(M,z) at 1e12 h^-1 Msun
def _E_l274(z, om=0.3027):
    return math.sqrt(om * (1 + z) ** 3 + (1 - om))


def _dm14_c(z, M=1e12):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M / 1e12))


_fc = lambda c: math.log(1 + c) - c / (1 + c)


def lcdm_native(z, M=1e12, dlogc=0.0):
    c0 = _dm14_c(0.0, M) * 10 ** dlogc
    cz = _dm14_c(z, M) * 10 ** dlogc
    return _E_l274(z) ** (4.0 / 3.0) * (cz ** 2 / _fc(cz)) / (c0 ** 2 / _fc(c0))


# ---- the P2 (fixed g_obs) mapping used by the record's CFG190: g_bar^2 + g_bar a0 = g_obs^2 ;  y = g_bar/a0(0) at the LOCAL a0
def dlogM_P2(ratio, y):
    """log10 shift of the baryonic mass at fixed observed (V, R) when a0 -> ratio * a0.  y = g_bar / a0(z=0);  y = 0: deep-MOND limit."""
    if y == 0:
        return -math.log10(ratio)
    gobs2 = y * y + y
    gb = (-ratio + math.sqrt(ratio * ratio + 4 * gobs2)) / 2
    return math.log10(gb / y)


def ratio_from_dlogM(dm, y, lo=1e-3, hi=1e3):
    """inverse of dlogM_P2 in the ratio (monotone decreasing in ratio)."""
    from scipy.optimize import brentq
    return brentq(lambda r: dlogM_P2(r, y) - dm, lo, hi)


PLANCK = dict(H0=67.4, Om=0.315, Or=9.1e-5)
