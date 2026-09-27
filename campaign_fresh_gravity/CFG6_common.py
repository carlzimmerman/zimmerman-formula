#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG6_common.py -- shared machinery for lane CFG6 (should a0 follow the dark energy through cosmic time?).

Nothing here runs on import except constant loading from committed JSON files.  Every function is used by
CFG6_a0z_branches.py and CFG6_a0z_evidence.py; the checks that validate each function against the record live in
those scripts (their C-sections), not here.

Contents
  - thread limits (the machine is shared: at most 2 BLAS/OpenMP threads)
  - Tee / check / banner: the lane's output conventions (each script writes its own .out and _results.json)
  - the footings from FP0 (canonical 9.3603e-11, alt 1.1312e-10 m/s^2) and kappa on rho_Lambda for each
  - the DESI DR2 w0-wa fits (arXiv:2503.14738) and the committed thinned public chains (L275's copies)
  - L275's weighted percentile, verbatim
  - the four readings of a0 under CPL dark energy: density, potential sqrt(V), pressure, and the rival rho_total (= H(z))
  - a canonical thawing field (exponential potential; XR20's Copeland-Liddle-Wands system, frozen at z = 30)
  - the two MOND kernels of the chain in two-field form (J_P2 of FP7; nu_mono of L340/XC4), through their phantom law
    h(y) = y (nu - 1): F = 2 H(y) - y h(y), s^2 J'' = (h/2)(h/h' - y), J' = y/h, J' + 2 s J'' = 1/h'
  - the LambdaCDM-native emergent scale of PAPER7 (Dutton-Maccio 2014 c(M, z)), as L274 implements it
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import sys, re, json, math
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def rpath(*parts):
    return os.path.join(REPO, *parts)


def rd(rel):
    p = rpath(rel)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


# ================================================================================================ output conventions
class Tee:
    """everything printed goes to the terminal and to the script's own .out"""

    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


class Recorder:
    def __init__(self, out):
        self.CH = []
        self.OUT = out

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

    def check(self, name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.CH.append((name, ok, load_bearing))
        self.OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
        self.P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok


# ================================================================================================ constants and footings
c_SI, G_SI = 299792458.0, 6.67430e-11
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
AU = 1.495978707e11
MSUN = 1.98847e30
_fp0 = json.load(open(rpath("real_research", "derivation_chain_2026", "FP0_core_postulates_results.json")))
A0 = {"canonical": _fp0["numbers"]["a0_canonical"], "alt": _fp0["numbers"]["a0_rho_total"]}
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153                 # FP0's (and XR20's) Planck inputs: rho_Lambda = Omega_L rho_c
H0_SI = H0_KMS * 1e3 / MPC
RHO_C = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
RHO_L = OM_L * RHO_C
KAPPA = {f: a / (c_SI * math.sqrt(G_SI * RHO_L)) for f, a in A0.items()}   # 0.5000 / 0.6043 on rho_Lambda
EPS = {f: k ** 2 / (8 * math.pi) for f, k in KAPPA.items()}                 # kappa^2/8pi, the MOND sector's weight on rho
LEVER_FOOT = math.log10(A0["alt"] / A0["canonical"])                         # +0.0823 dex: the committed canonical->alt shift

# DESI DR2 BAO + CMB + SNe, w0waCDM (arXiv:2503.14738); the pairs L273 verified against the paper's table on 2026-09-18
DESI = {"DESY5": (-0.752, -0.86), "Pantheon+": (-0.838, -0.62), "Union3": (-0.667, -1.09)}
DESI_ORDER = ["DESY5", "Pantheon+", "Union3"]
CHAIN_FILE = {"DESY5": "desy5sn", "Pantheon+": "pantheonplus", "Union3": "union3"}
THIN_DIR = rpath("fable_independent_2026", "data", "desi_dr2_w0wa_thinned")


def desi_table_from_record():
    """(H0, Omega_m) per combination, read from L273's docstring (verified there against the paper's w0waCDM table)."""
    src = rd("fable_independent_2026/L273_desi_a0z_band.py") or ""
    m = re.search(r"Omega_m = ([0-9.]+) / ([0-9.]+) / ([0-9.]+) and H0 = ([0-9.]+) / ([0-9.]+) / ([0-9.]+) for\s+Pantheon\+ / Union3 / DESY5", src)
    if not m:
        return None
    om = [float(m.group(i)) for i in (1, 2, 3)]
    h0 = [float(m.group(i)) for i in (4, 5, 6)]
    return {"Pantheon+": dict(Om=om[0], H0=h0[0]), "Union3": dict(Om=om[1], H0=h0[1]), "DESY5": dict(Om=om[2], H0=h0[2])}


def load_chain(name):
    """the committed thinned DESI DR2 public chains (L275): columns weight, w, wa, omegam"""
    d = np.loadtxt(os.path.join(THIN_DIR, CHAIN_FILE[name] + ".txt"))
    return d[:, 0], d[:, 1], d[:, 2], d[:, 3]


def wpct(x, wt, q):
    """L275's weighted percentile, verbatim"""
    i = np.argsort(x)
    cx = np.cumsum(wt[i]) / np.sum(wt)
    return np.interp(np.asarray(q) / 100.0, cx, x[i])


# ================================================================================================ the readings under CPL
def f_DE(z, w0, wa):
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))


def w_of(z, w0, wa):
    return w0 + wa * z / (1 + z)


def R_density(z, w0, wa):            # branch B: a0 ~ sqrt(rho_DE)          (FP0 R3b; L273 Parts 1-3)
    return np.sqrt(f_DE(z, w0, wa))


def R_potential(z, w0, wa):          # branch C: a0 ~ sqrt(V), V = (rho - p)/2 (XR20 T5)
    return np.sqrt(f_DE(z, w0, wa) * (1 - w_of(z, w0, wa)) / (1 - w0))


def R_pressure(z, w0, wa):           # branch D: a0 ~ sqrt(-p)             (L273 Part 4; PAPER7 v2 note)
    return np.sqrt(w_of(z, w0, wa) * f_DE(z, w0, wa) / w0)


def R_total(z, w0, wa, om):          # the rival: a0 ~ sqrt(rho_total) = H(z)/H0 (flat, no radiation, as L273/L275)
    return np.sqrt(om * (1 + z) ** 3 + (1 - om) * f_DE(z, w0, wa))


CPL_MAPS = {"B": R_density, "C": R_potential, "D": R_pressure}


# ================================================================================================ a canonical thawing field
Z_FROZEN = 30.0


def thaw_solve(lam, yi2, z_i=Z_FROZEN):
    """XR20 E4's system: x = phidot/(sqrt6 H M_P), y = sqrt(V/3)/(H M_P); dust + field; frozen at z_i"""
    s3 = math.sqrt(1.5)

    def rhs(N, u):
        x, y = u
        com = 1.5 * (2 * x * x + (1 - x * x - y * y))
        return [-3 * x + lam * s3 * y * y + x * com, -lam * s3 * x * y + y * com]
    return solve_ivp(rhs, (-math.log(1 + z_i), 0.0), [0.0, math.sqrt(yi2)], rtol=1e-11, atol=1e-14, dense_output=True)


def thaw_shoot(lam, om_phi0):
    g_ = lambda lyi: (lambda s_: s_.y[0, -1] ** 2 + s_.y[1, -1] ** 2)(thaw_solve(lam, math.exp(lyi))) - om_phi0
    return math.exp(brentq(g_, math.log(1e-8), math.log(5e-2), xtol=1e-13))


def thaw_tracks(lam, om_m, zg):
    """log10 ratios (z)/(0) of rho_phi, V, -p and E(z) for a thawing field with Omega_phi0 = 1 - om_m; and w(z)."""
    zg = np.asarray(zg, float)
    if lam <= 0:
        E = np.sqrt(om_m * (1 + zg) ** 3 + 1 - om_m)
        zero = np.zeros_like(zg)
        return dict(dens=zero.copy(), V=zero.copy(), press=zero.copy(), logE=np.log10(E), w=-np.ones_like(zg), w0=-1.0, yi2=0.0)
    om_phi0 = 1.0 - om_m
    yi2 = thaw_shoot(lam, om_phi0)
    sol = thaw_solve(lam, yi2)
    N = -np.log(1 + zg)
    x, y = sol.sol(N)
    x0, y0 = sol.y[0, -1], sol.y[1, -1]
    om0 = x0 * x0 + y0 * y0
    H2 = (1 + zg) ** 3 * (1 - om0) / (1 - (x * x + y * y))            # H^2/H0^2 from Omega_m(z) = 1 - Omega_phi(z)
    rho = (x * x + y * y) * H2 / om0
    V = y * y * H2 / (y0 * y0)
    mp_ = (y * y - x * x) * H2 / (y0 * y0 - x0 * x0)
    w = (x * x - y * y) / (x * x + y * y)
    return dict(dens=0.5 * np.log10(rho), V=0.5 * np.log10(V), press=0.5 * np.log10(mp_), logE=0.5 * np.log10(H2), w=w,
                w0=float((x0 * x0 - y0 * y0) / om0), yi2=yi2)


def thaw_interp_w0(lams, oms, zg, w0g, track, w0s, om_s, zq):
    """per posterior sample: the thawing field with the sample's w0 (lambda interpolated at each bracketing Omega_m node,
    track interpolated in lambda and z, then linearly in Omega_m; Omega_m clipped to the grid; w0 < -1 -> Lambda)"""
    lams, oms, zg, w0g, track = (np.asarray(a, float) for a in (lams, oms, zg, w0g, track))
    w0s, om_s = np.asarray(w0s, float), np.asarray(om_s, float)
    omc = np.clip(om_s, oms[0], oms[-1])
    i0 = np.clip(np.searchsorted(oms, omc) - 1, 0, len(oms) - 2)
    fr = (omc - oms[i0]) / (oms[i0 + 1] - oms[i0])
    out = np.zeros((len(w0s), len(zq)))
    for iz, z in enumerate(zq):
        tz = np.array([[np.interp(z, zg, track[i, j]) for j in range(len(lams))] for i in range(len(oms))])
        vals = np.zeros((2, len(w0s)))
        for sidx, ii in enumerate((i0, i0 + 1)):
            for node in np.unique(ii):
                sel = ii == node
                lam_s = np.interp(np.clip(w0s[sel], -1.0, w0g[node, -1]), w0g[node], lams)
                vals[sidx, sel] = np.interp(lam_s, lams, tz[node])
        out[:, iz] = (1 - fr) * vals[0] + fr * vals[1]
    return out


def thaw_nodes_at(zg, track, zq):
    """every grid node's track at the redshifts zq: shape (nOm, nLam, len(zq))"""
    track = np.asarray(track, float)
    return np.stack([np.array([[np.interp(z, zg, track[i, j]) for j in range(track.shape[1])] for i in range(track.shape[0])])
                     for z in zq], axis=-1)


def cpl_equivalent(zg, w):
    """least-squares CPL (w0, wa) of a w(z) track over a in [1/3.5, 1] (z <= 2.5), uniform in a"""
    a = 1.0 / (1.0 + np.asarray(zg))
    sel = a >= 1 / 3.5 - 1e-12
    A = np.vstack([np.ones(sel.sum()), 1 - a[sel]]).T
    c, *_ = np.linalg.lstsq(A, np.asarray(w)[sel], rcond=None)
    return float(c[0]), float(c[1])


# ================================================================================================ MOND kernels in two-field form
mp.mp.dps = 40


class KernelP2:
    """FP7's J_P2: the P2 law g = sqrt(g_N^2 + g_N a0); phantom h(y) = sqrt(y^2 + y) - y (a0 units)"""
    name = "J_P2"

    @staticmethod
    def h(y):
        y = mp.mpf(y)
        return y / (mp.sqrt(y * y + y) + y)

    @staticmethod
    def hp(y):
        y = mp.mpf(y)
        r = mp.sqrt(y * y + y)
        return 1 / (2 * r * (2 * y + 1 + 2 * r))

    @staticmethod
    def H(y):                                                      # Int_0^y h, closed form
        y = mp.mpf(y)
        r = mp.sqrt(y * y + y)
        return (2 * y + 1) * r / 4 - mp.log(2 * y + 1 + 2 * r) / 8 - y * y / 2


class KernelNuMono:
    """L340/XC4's nu_mono: nu_RAR's phantom h_R = y/(e^sqrt(y) - 1) up to y* (where h_R' meets the floor), then
    h' = delta h_p/(y + y_p) (delta = 0.05): monotone, phantom growing logarithmically"""
    name = "nu_mono"
    DELTA = mp.mpf("0.05")

    def __init__(self):
        self.hR = lambda y: y / mp.expm1(mp.sqrt(y))
        self.dhR = lambda y: (lambda z_, em: (2 * em - z_ * (1 + em)) / (2 * em ** 2))(mp.sqrt(y), mp.expm1(mp.sqrt(y)))
        self.YP = mp.findroot(self.dhR, 2.5)
        self.HP = self.hR(self.YP)
        self.floor = lambda y: self.DELTA * self.HP / (y + self.YP)
        self.YS = mp.findroot(lambda y: self.dhR(y) - self.floor(y), 2.3)
        self.HS = self.hR(self.YS)
        self.IS = mp.quad(self.hR, [0, self.YS])

    def h(self, y):
        y = mp.mpf(y)
        return self.hR(y) if y <= self.YS else self.HS + self.DELTA * self.HP * mp.log((y + self.YP) / (self.YS + self.YP))

    def hp(self, y):
        y = mp.mpf(y)
        return self.dhR(y) if y <= self.YS else self.floor(y)

    def H(self, y):
        y = mp.mpf(y)
        if y <= self.YS:
            return mp.quad(self.hR, [0, y])
        dH, YP, YS = self.DELTA * self.HP, self.YP, self.YS
        return self.IS + self.HS * (y - YS) + dH * ((y + YP) * mp.log((y + YP) / (YS + YP)) - (y - YS))


def kernel_quantities(K, y):
    """F = sJ' - J, s^2 J'', J', J' + 2 s J'' of the two-field MOND term at y = g_N/a0, from the phantom law"""
    y = mp.mpf(y)
    h, hp, H = K.h(y), K.hp(y), K.H(y)
    return dict(F=2 * H - y * h, s2Jpp=(h / 2) * (h / hp - y), Jp=y / h, JpL=1 / hp, h=h)


# ================================================================================================ LambdaCDM-native emergent scale
OM_L274 = 0.3027                                  # L274/L276's DESI DR2 + CMB LambdaCDM Omega_m


def dm14_c(z, M=1e12):
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * np.asarray(z, float) ** 1.21)
    b = -0.101 + 0.026 * np.asarray(z, float)
    return 10 ** (a + b * np.log10(M / 1e12))


def _fc(c):
    return np.log(1 + c) - c / (1 + c)


def lcdm_emergent(z, M=1e12, dlogc=0.0, om=OM_L274):
    """PAPER7 / L274: a_s(z)/a_s(0) = E(z)^{4/3} [c^2/f(c)](z)/[c^2/f(c)](0), DM14 c(M, z)"""
    z = np.asarray(z, float)
    E = np.sqrt(om * (1 + z) ** 3 + 1 - om)
    c0 = dm14_c(0.0, M) * 10 ** dlogc
    cz = dm14_c(z, M) * 10 ** dlogc
    return E ** (4.0 / 3.0) * (cz ** 2 / _fc(cz)) / (c0 ** 2 / _fc(c0))


def lcdm_emergent_range(z):
    """L274's range: halo mass 1e11-1e13 and the 0.11 dex concentration scatter"""
    v = [np.log10(lcdm_emergent(z, M, dl)) for M in (1e11, 1e12, 1e13) for dl in (-0.11, 0.0, 0.11)]
    return float(np.min(v)), float(np.max(v))
