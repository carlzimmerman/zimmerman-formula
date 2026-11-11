#!/usr/bin/env python3
"""LSF1: a Lifshitz fermion superfluid as the law's microscopic origin? (TOE0 follow-up; owner lift 2e4c9e9b4b)

Criteria: FROZEN_CRITERIA.md (committed alone, local 1bc74e543d / origin 700e0c9c1c). TEST lane: adopts nothing.
Run:  python3 lsf1.py                 -> lsf1.out / lsf1.json            (known answers + gates + reported items)
      LSF1_MUTATE=1 python3 lsf1.py   -> lsf1_MUTATE.out / lsf1_MUTATE.json (twins M1-M7 must bite)
Microscopic part: natural units, energies in |mu_eff|, dispersion coefficient 1. E and D: SI.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import resource
import time

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.optimize import brentq, differential_evolution, minimize_scalar
from scipy.special import roots_legendre

T_START = time.time()
MUTATE = os.environ.get("LSF1_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


def fl(v):
    return float(v)


# ============================================================== constants
HBAR = 1.054571817e-34
C = 2.99792458e8
EV = 1.602176634e-19
G = 6.67430e-11
GM_SUN = 1.32712440018e20
M_SUN = GM_SUN / G
KPC = 3.0856775814913673e19
AU = 1.495978707e11
HBARC = HBAR * C / EV                              # eV m
M_PL = math.sqrt(HBAR * C / G) * C**2 / EV         # unreduced Planck mass, eV (NPJ1's)
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
M_REF = 6e10                                       # Msun, QG1's point mass
G4PI = 4 * math.pi

say("LSF1: a Lifshitz fermion superfluid as the law's microscopic origin.  MUTATE =", MUTATE)
say(f"M_Pl = {M_PL:.5e} eV;  hbar c = {HBARC:.6e} eV m")

# ============================================================== quadrature helpers
_GL = {}


def gl(n):
    if n not in _GL:
        _GL[n] = roots_legendre(n)
    return _GL[n]


def panels(breaks, n):
    x, w = gl(n)
    xs, ws = [], []
    br = np.unique(np.asarray(breaks, float))
    for a, b in zip(br[:-1], br[1:]):
        xs.append(0.5 * (b - a) * x + 0.5 * (b + a))
        ws.append(0.5 * (b - a) * w)
    return np.concatenate(xs), np.concatenate(ws)


# ============================================================== dispersions (functions of s = |k|^2)
EPS2 = {"D1": lambda s: s, "D2": lambda s: s**3, "D3": lambda s: s + s**3}
EPS1 = {k: (lambda f: (lambda k_: f(k_ * k_)))(f) for k, f in EPS2.items()}
DZ = {"D1": (3, 2), "D2": (3, 6), "D3": (3, 6), "D4": (1, 2), "D5": (1, 2)}
DNAME = {"D1": "3-d Galilean eps = k^2 (control)", "D2": "3-d Lifshitz eps = k^6 (candidate)",
         "D3": "3-d crossover eps = k^2 + k^6", "D4": "quasi-1-d k_x^2 + 2t(2 - cos k_y - cos k_z), t = 1e-3",
         "D5": "isotropic tangle of 1-d Galilean channels"}


def kF_of(br, mu):
    if mu <= 0:
        return 0.0
    return brentq(lambda k: EPS1[br](k) - mu, 0.0, max(2.0, mu**0.5 + 2))


def P0_3d(br, mu):
    """free two-spin Fermi-sea pressure (3-d isotropic), closed forms checked by KA1/KA2."""
    if mu <= 0:
        return 0.0
    k = kF_of(br, mu)
    if br == "D1":
        return 2 * k**5 / (15 * math.pi**2)
    if br == "D2":
        return 2 * mu**1.5 / (9 * math.pi**2)
    # D3: P = Int_0^kF n(k) eps'(k) dk, n = k^3/(3 pi^2), eps' = 2k + 6k^5
    return (2 * k**5 / 5 + 2 * k**9 / 3) / (3 * math.pi**2)


def P0_1d(mu):
    return 4 * mu**1.5 / (3 * math.pi) if mu > 0 else 0.0


# ============================================================== KNOWN ANSWERS
say("\n=== KNOWN ANSWERS ===")
KA = {}
mp.mp.dps = 30

# KA1: per spin state, 3-d Galilean: P_sigma = (2m)^(3/2) mu^(5/2)/(15 pi^2); two spins double it (KA2 at z = 2).
mm, mu_t = mp.mpf("0.7"), mp.mpf("1.3")
kf = mp.sqrt(2 * mm * mu_t)
P_sig = mp.quad(lambda k: k**2 * (mu_t - k**2 / (2 * mm)), [0, kf]) / (2 * mp.pi**2)
P_sig_cf = (2 * mm)**1.5 * mu_t**2.5 / (15 * mp.pi**2)
ka1 = float(abs(P_sig / P_sig_cf - 1))
KA["KA1"] = {"P_per_spin": fl(P_sig), "closed": fl(P_sig_cf), "rel": ka1, "pass": ka1 < 1e-8,
             "note": "the frozen line's '(spin 1/2)' formula is the pressure per spin state; two spins = 2x (KA2, z = 2)"}
say(f"KA1 3-d Galilean free gas, per spin state: quadrature {float(P_sig):.12e} vs (2m)^1.5 mu^2.5/(15 pi^2) "
    f"{float(P_sig_cf):.12e} (rel {ka1:.1e}) -> {'PASS' if KA['KA1']['pass'] else 'FAIL'}; two spin states give twice "
    f"this (= KA2 at z = 2)")

# KA2: eps = c k^z, two spins: P = z/(z+3) mu^((z+3)/z)/(3 pi^2 c^(3/z)); z = 6: 2/(9 pi^2) mu^1.5
ka2 = {}
for z_, c_ in [(2, mp.mpf("0.5")), (6, mp.mpf("1.7")), (4, mp.mpf("0.9"))]:
    kf = (mu_t / c_) ** (mp.mpf(1) / z_)
    Pq = mp.quad(lambda k: k**2 * (mu_t - c_ * k**z_), [0, kf]) / (mp.pi**2)       # two spins: 2/(2 pi^2)
    Pcf = mp.mpf(z_) / (z_ + 3) * mu_t ** (mp.mpf(z_ + 3) / z_) / (3 * mp.pi**2 * c_ ** (mp.mpf(3) / z_))
    ka2[z_] = float(abs(Pq / Pcf - 1))
z6coef = sp.Rational(6, 9) / (3 * sp.pi**2)
ka2_ok = max(ka2.values()) < 1e-8 and sp.simplify(z6coef - 2 / (9 * sp.pi**2)) == 0
# exponent at z = 6 from the quadrature: d ln P / d ln mu
P6 = lambda mu_: mp.quad(lambda k: k**2 * (mu_ - k**6), [0, mu_ ** (mp.mpf(1) / 6)]) / mp.pi**2
ex6 = float(mp.diff(lambda t: mp.log(P6(mp.e**t)), mp.log(mu_t)))
# KA2b: 1-d Galilean two spins: P = (4/(3 pi)) sqrt(2m) mu^1.5
kf = mp.sqrt(2 * mm * mu_t)
P1q = 2 * mp.quad(lambda k: (mu_t - k**2 / (2 * mm)), [-kf, kf]) / (2 * mp.pi)
P1cf = 4 / (3 * mp.pi) * mp.sqrt(2 * mm) * mu_t**1.5
ka2b = float(abs(P1q / P1cf - 1))
KA["KA2"] = {"rel_by_z": ka2, "exponent_z6": ex6, "rel_1d": ka2b,
             "pass": ka2_ok and abs(ex6 - 1.5) < 1e-8 and ka2b < 1e-8}
say(f"KA2 eps = c k^z (two spins): rel err by z {ka2}; z = 6 coefficient 2/(9 pi^2) exact; d ln P/d ln mu at z = 6: "
    f"{ex6:.10f}; KA2b 1-d Galilean (4/(3 pi)) sqrt(2m) mu^1.5 rel {ka2b:.1e} -> {'PASS' if KA['KA2']['pass'] else 'FAIL'}")

# KA3: BK static phonon equation (sympy, independent code)
r, Lb, al, MP, Mb, m_ = sp.symbols("r Lambda alpha M_Pl M m", positive=True)
th = sp.Function("theta")
rho = sp.Function("rho")
Lag = 4 * sp.pi * r**2 * (-(sp.Rational(2, 3) * Lb) * sp.diff(th(r), r)**3 - al * Lb * th(r) * rho(r) / MP)
EL = sp.euler_equations(Lag, th(r), r)[0]
# Gauss: (r^2 theta'^2)' = alpha rho r^2/(2 M_Pl)  =>  theta' = sqrt(alpha M/(8 pi M_Pl))/r for a point mass M
tp = sp.sqrt(al * Mb / (8 * sp.pi * MP)) / r
resid = sp.simplify((EL.lhs - EL.rhs).subs(sp.diff(th(r), r, 2), sp.diff(tp, r)).subs(sp.diff(th(r), r), tp)
                    .subs(rho(r), 0))
a_th = al * Lb * tp / MP
a_N = Mb / (MP**2 * r**2)
a0p = sp.simplify(a_th**2 / a_N)
X = sp.symbols("X", real=True)
PBK = sp.Rational(2, 3) * Lb * (2 * m_)**sp.Rational(3, 2) * X * sp.sqrt(sp.Abs(X))
gth = sp.symbols("g_theta", positive=True)
mond_lim = sp.simplify(PBK.subs(X, -gth**2 / (2 * m_)))
ka3_ok = resid == 0 and sp.simplify(a0p - al**3 * Lb**2 / (8 * sp.pi * MP)) == 0 and \
    sp.simplify(mond_lim + sp.Rational(2, 3) * Lb * gth**3) == 0
KA["KA3"] = {"EL_residual_vacuum": str(resid), "a0prime": str(a0p), "MOND_limit": str(mond_lim), "pass": bool(ka3_ok)}
say(f"KA3 BK: EL residual outside the source {resid}; a_theta^2/a_N = {a0p}; P(X = -(grad theta)^2/2m) = {mond_lim} "
    f"-> {'PASS' if ka3_ok else 'FAIL'}")

# KA4: Lifshitz power counting + UV behaviour of the pairing integral
def contact_dim(d, z, n):
    return z + d - n * d


pc = {"(3,2) 2-body": contact_dim(3, 2, 2), "(3,2) 3-body": contact_dim(3, 2, 3),
      "(3,6) 2-body": contact_dim(3, 6, 2), "(3,6) 3-body": contact_dim(3, 6, 3),
      "(1,2) 2-body": contact_dim(1, 2, 2), "(1,2) 3-body": contact_dim(1, 2, 3)}
uv = {}
for z_ in (2, 6):
    vals = [float(mp.quad(lambda k: k**2 / k**z_, [1, Lc]) / (2 * mp.pi**2)) for Lc in (1e2, 1e3)]
    uv[z_] = vals
ka4_ok = (pc["(3,2) 2-body"] == -1 and pc["(3,2) 3-body"] == -4 and pc["(3,6) 2-body"] == 3 and
          pc["(3,6) 3-body"] == 0 and abs(uv[6][1] / uv[6][0] - 1) < 1e-5 and uv[2][1] / uv[2][0] > 9.9)
KA["KA4"] = {"contact_dims": pc, "Int_d3k_over_eps_cutoff_1e2_1e3": uv, "pass": bool(ka4_ok)}
say(f"KA4 contact dimensions z + d - n d: {pc}; Int d^3k/eps over [1, 1e2], [1, 1e3]: z = 6 {uv[6]} (converges), "
    f"z = 2 {uv[2]} (linear) -> {'PASS' if ka4_ok else 'FAIL'}")

# KA5: textbook BCS gap, 3-d Galilean (eps = k^2, m = 1/2, k_F = 1 = eps_F), mean field at mu = eps_F
def gap_resid_D1(D, mu, inva):
    # -m/(4 pi a) = Int d^3k/(2pi)^3 [1/(2E) - 1/(2 eps)],  m = 1/2
    f = lambda k: k**2 * (1 / (2 * mp.sqrt((k**2 - mu)**2 + D**2)) - 1 / (2 * k**2))
    kf = mp.sqrt(mu) if mu > 0 else mp.mpf(0)
    pts = [0, kf * 0.9, kf, kf * 1.1, 3, mp.inf] if mu > 0 else [0, 1, mp.inf]
    return mp.quad(f, pts) / (2 * mp.pi**2) + inva / (8 * mp.pi)


ka5 = {}
for inva in (-2, -3):
    Das = 8 / mp.e**2 * mp.exp(-mp.pi * abs(inva) / 2)          # exp(-pi/(2 k_F |a|)), k_F |a| = 1/|1/a|
    Dmf = brentq(lambda D: float(gap_resid_D1(mp.mpf(D), 1, inva)), float(Das) / 3, float(Das) * 3, xtol=1e-15)
    ka5[inva] = {"mean_field": float(Dmf), "asymptotic": float(Das), "ratio": float(Dmf / float(Das))}
KA["KA5"] = {"by_1_over_kFa": ka5, "pass": abs(ka5[-2]["ratio"] - 1) < 1e-2 and
             abs(ka5[-3]["ratio"] - 1) <= abs(ka5[-2]["ratio"] - 1) + 1e-12}
say(f"KA5 BCS gap Delta/eps_F, mean field vs (8/e^2) exp(-pi/(2 k_F|a|)): {ka5} -> "
    f"{'PASS' if KA['KA5']['pass'] else 'FAIL'}")

# KA8: pair-kinetic inequality eps_S(k; q) - eps(k) - eps(q) >= 0 (sympy)
kk, qq = sp.symbols("k q", positive=True)
uu = sp.symbols("u", real=True)
ka8 = {}
for br, epf in [("D1", lambda s: s), ("D2", lambda s: s**3), ("D3", lambda s: s + s**3)]:
    sp_, sm_ = kk**2 + qq**2 + 2 * kk * qq * uu, kk**2 + qq**2 - 2 * kk * qq * uu
    diff = sp.expand((epf(sp_) + epf(sm_)) / 2 - epf(kk**2) - epf(qq**2))
    poly = sp.Poly(diff, kk, qq, uu)
    nonneg = all(c >= 0 and (m[2] % 2 == 0) for m, c in zip(poly.monoms(), poly.coeffs()))
    ka8[br] = {"eps_S - eps(k) - eps(q)": str(sp.factor(diff)), "manifestly_nonneg": bool(nonneg)}
KA["KA8"] = {"by_branch": ka8, "pass": all(v["manifestly_nonneg"] for v in ka8.values()) and
             ka8["D1"]["eps_S - eps(k) - eps(q)"] == "0"}
say(f"KA8 pair-kinetic inequality: {ka8} -> {'PASS' if KA['KA8']['pass'] else 'FAIL'}")

# KA9: two-body binding for eps = k^6 in 3-d: chi0 = Int d^3k/(2pi)^3 1/(2 k^6 + E_b) ~ E_b^(-1/2)
chi0_k6 = lambda Eb: mp.quad(lambda k: k**2 / (2 * k**6 + Eb), [0, Eb ** (mp.mpf(1) / 6), 1, mp.inf]) / (2 * mp.pi**2)
sl9 = float((mp.log(chi0_k6(mp.mpf("1e-8"))) - mp.log(chi0_k6(mp.mpf("1e-6")))) / (mp.log(1e-8) - mp.log(1e-6)))
cf9 = float(chi0_k6(mp.mpf(2)) / (1 / (12 * mp.pi * mp.sqrt(2 * 2))))
KA["KA9"] = {"slope": sl9, "closed_form_ratio": cf9, "pass": abs(sl9 + 0.5) < 1e-2 and abs(cf9 - 1) < 1e-10}
say(f"KA9 k^6 two-body integral: d ln chi0/d ln E_b = {sl9:.6f} (-0.5: bound state for any attraction); closed form "
    f"1/(12 pi sqrt(2 E_b)) ratio {cf9:.12f} -> {'PASS' if KA['KA9']['pass'] else 'FAIL'}")

# KA10: convexity
mu_s, p_s, c_s = sp.symbols("mu p c", positive=True)
conv_free = sp.simplify(sp.diff(c_s * mu_s**p_s, mu_s, 2) / (c_s * mu_s**(p_s - 2)))      # p(p-1) > 0 for p > 1
Xn = sp.symbols("Xn", positive=True)                                                     # X = -Xn < 0
P_odd_neg = -Xn**sp.Rational(3, 2)                                                       # X|X|^(1/2) at X = -Xn
d2 = sp.simplify(sp.diff(P_odd_neg, Xn, 2))                                             # d^2P/dX^2 = d^2/dXn^2
ka10_ok = sp.simplify(conv_free - p_s * (p_s - 1)) == 0 and sp.simplify(d2 + sp.Rational(3, 4) / sp.sqrt(Xn)) == 0
KA["KA10"] = {"free_gas_P''/(c mu^(p-2))": str(conv_free), "BK_P''_at_X<0": str(d2), "pass": bool(ka10_ok)}
say(f"KA10 convexity: free gas P'' = c mu^(p-2) x {conv_free} (> 0 for p > 1); BK P''(X < 0) = {d2} (< 0: negative "
    f"compressibility) -> {'PASS' if ka10_ok else 'FAIL'}")

# ============================================================== microscopic FF mean field (3-d isotropic)
# Omega(Delta; mu, q) = Delta^2 inv_g + Int d^3k/(2pi)^3 [xi_S - E + min(0, E + xi_A) + min(0, E - xi_A)] (+ reg, D1)
# deltaOmega(Delta) = Omega(Delta) - Omega(0): integrand F = (|xi_S| - E) + depairing differences (>= 0).
class Grid3:
    def __init__(self, br, mu, q, kF, mode="fine"):
        self.br = br
        kmax = max(4.0, 2.5 * (q + max(kF, 1.0)))
        edges = []
        for edge in (0.0, math.pi):
            edges += list(edge + np.sign(math.pi / 2 - edge) * np.geomspace(1e-4, 0.3, 16))
        if mode == "window":          # xi_S > 0 everywhere: smooth pairing part; depairing kinks only near k ~ q
            step = max(0.05, kmax / 400)
            brk = list(np.arange(0, kmax, step)) + [kmax]
            if kF > 0:
                brk += list(np.arange(max(0, q - 1.5 * kF), q + 1.5 * kF, 0.02))
            tb = list(np.linspace(0, math.pi, 49)) + edges
            nk = nt = 6
        elif mode == "curve":         # small q: resolve the Fermi shell (width Delta/v_F)
            if br == "D1":            # the regulated tail needs k >> sqrt(mu) (as in "fine")
                kmax = 40.0
            brk = list(np.arange(0, min(kmax, 4.0), 0.05)) + list(np.arange(4.0, kmax, 0.1)) + [kmax]
            hw = q + 0.1
            brk += list(np.arange(max(0, kF - hw), kF + hw, 0.004))
            tb = list(np.linspace(0, math.pi, 97))
            nk = nt = 6
        else:                         # "fine": KA6 / KA7 / M5
            if br == "D1":            # the regulated tail needs k >> sqrt(mu) (first run: KA6 off by 1.1e-4 at kmax 4)
                kmax = 40.0
            brk = list(np.arange(0, min(kmax, 4.0), 0.05)) + list(np.arange(4.0, kmax, 0.1)) + [kmax]
            for c0 in [c_ for c_ in (kF, q, abs(q - kF), q + kF) if c_ > 0]:
                brk += list(np.arange(max(0, c0 - 0.3), min(kmax, c0 + 0.3), 0.004))
            tb = list(np.linspace(0, math.pi, 97)) + (edges if q > 0 else [])
            nk = nt = 8
        brk = [b for b in brk if 0 <= b <= kmax]
        tb = [t for t in tb if 0 <= t <= math.pi]
        self.k, self.wk = panels(sorted(set(brk)), nk)
        self.t, self.wt = panels(sorted(set(tb)), nt)
        self.kmax = kmax
        K, T = np.meshgrid(self.k, self.t, indexing="ij")
        self.W = (self.wk[:, None] * self.wt[None, :]) * K**2 * np.sin(T) / (4 * math.pi**2)
        sp_ = K**2 + q**2 + 2 * K * q * np.cos(T)
        sm_ = K**2 + q**2 - 2 * K * q * np.cos(T)
        e1, e2 = EPS2[br](sp_), EPS2[br](sm_)
        self.xiS = 0.5 * (e1 + e2) - mu
        self.xiA = 0.5 * (e1 - e2)
        self.K2 = K**2
        self.mu, self.q = mu, q

    def dOmega(self, D, inv_g, inva=None, fixed=False):
        """deltaOmega(Delta) = Omega(Delta) - Omega(0). D1 uses the scattering length (inva = 1/a, m = 1/2)."""
        xs, xa = self.xiS, self.xiA
        E = np.sqrt(xs * xs + D * D)
        ax = np.abs(xs)
        F = ax - E
        if not fixed:
            F = F + (np.minimum(0, E + xa) - np.minimum(0, ax + xa)) + (np.minimum(0, E - xa) - np.minimum(0, ax - xa))
        if self.br == "D1":
            F = F + D * D / (2 * self.K2)
            tail = D * D * (self.q**2 - self.mu) / (4 * math.pi**2 * self.kmax)
            return -D * D * inva / (8 * math.pi) + float(np.sum(self.W * F)) + tail
        tail = -D * D / (12 * math.pi**2 * self.kmax**3)
        return D * D * inv_g + float(np.sum(self.W * F)) + tail

    def omega_normal(self):
        xs, xa = self.xiS, self.xiA
        return float(np.sum(self.W * (np.minimum(0, xs + xa) + np.minimum(0, xs - xa))))

    def omega_total(self, D, inv_g, inva=None):
        """Omega(Delta) directly: smooth integrand (xi_S - E) when nothing is depaired (KA6, M5)."""
        xs, xa = self.xiS, self.xiA
        E = np.sqrt(xs * xs + D * D)
        F = xs - E + np.minimum(0, E + xa) + np.minimum(0, E - xa)
        if self.br == "D1":
            F = F + D * D / (2 * self.K2)
            return -D * D * inva / (8 * math.pi) + float(np.sum(self.W * F)) + \
                D * D * (self.q**2 - self.mu) / (4 * math.pi**2 * self.kmax)
        return D * D * inv_g + float(np.sum(self.W * F)) - D * D / (12 * math.pi**2 * self.kmax**3)

    def omega_fixed(self, D, inv_g):
        """Omega(Delta) with Delta held, no depaired quasiparticles (twin M7): Delta^2 inv_g + Int (xi_S - E)."""
        xs = self.xiS
        E = np.sqrt(xs * xs + D * D)
        tail = -D * D / (12 * math.pi**2 * self.kmax**3)
        return D * D * inv_g + float(np.sum(self.W * (xs - E))) + tail

    def chi(self, inva=None):
        """pair susceptibility Int 1/(2 xi_S) (xi_S > 0 everywhere); D1: Int [1/(2 xi_S) - 1/(2 k^2)]."""
        if self.br == "D1":
            return float(np.sum(self.W * (1 / (2 * self.xiS) - 1 / (2 * self.K2)))) - \
                (self.q**2 - self.mu) / (4 * math.pi**2 * self.kmax)
        return float(np.sum(self.W / (2 * self.xiS))) + 1 / (12 * math.pi**2 * self.kmax**3)


def radial_q0(br, mu, nk=16):
    """q = 0 radial grid (1-d in k): returns k, weights (with k^2/(2 pi^2))."""
    kF = kF_of(br, mu)
    kmax = 60.0 if br == "D1" else 12.0
    brk = [0.0, kmax] + list(np.arange(0, kmax, 0.05))
    if kF > 0:
        brk += list(np.arange(max(0, kF - 0.3), kF + 0.3, 0.002))
    k, w = panels(sorted(set(brk)), nk)
    return k, w * k**2 / (2 * math.pi**2), kmax


def dOmega_q0(br, mu, D, inv_g, inva=None, total=False):
    k, W, kmax = radial_q0(br, mu)
    xi = EPS1[br](k) - mu
    E = np.sqrt(xi * xi + D * D)
    F = (xi - E) if total else (np.abs(xi) - E)
    if br == "D1":
        F = F + D * D / (2 * k * k)
        return -D * D * inva / (8 * math.pi) + float(np.sum(W * F)) + D * D * (-mu) / (4 * math.pi**2 * kmax)
    return D * D * inv_g + float(np.sum(W * F)) - D * D / (12 * math.pi**2 * kmax**3)


def chi0_3d(br, mu):
    """Int d^3k/(2pi)^3 1/(2(eps - mu)), mu < 0 (D2, D3); D1: regulated form."""
    f = (lambda k: k**2 * (1 / (2 * (EPS1[br](k) - mu)) - (1 / (2 * k * k) if br == "D1" else 0)))
    s = abs(mu) ** (1 / 6) if br != "D1" else abs(mu) ** 0.5
    pts = sorted(set([0, s / 10, s, 10 * s, 0.1, 1, 10]))
    return float(mp.quad(f, pts + [mp.inf]) / (2 * mp.pi**2))


def minimize_D(fun, Dscale, ngrid=30):
    """min over Delta in {0} U geomspace(1e-3, 4) x Dscale (extended x4 while the edge wins), then refinement."""
    top = 4.0
    while True:
        grid = np.concatenate([[0.0], Dscale * np.geomspace(1e-3, top, ngrid)])
        vals = np.array([fun(D) if D > 0 else 0.0 for D in grid])
        if int(np.argmin(vals)) < len(grid) - 1 or top > 1e4:
            break
        top *= 4
    j = int(np.argmin(vals))
    if j == 0:
        return 0.0, 0.0, float(np.min(vals[1:]))
    lo = grid[max(j - 1, 1)] if j > 1 else 0.5 * grid[1]
    hi = grid[min(j + 1, len(grid) - 1)]
    res = minimize_scalar(fun, bounds=(lo, hi), method="bounded", options={"xatol": 1e-9 * Dscale})
    if res.fun < vals[j]:
        return float(res.x), float(res.fun), float(np.min(vals[1:]))
    return float(grid[j]), float(vals[j]), float(np.min(vals[1:]))


# ============================================================== microscopic 1-d (D4, D5)
class Grid1:
    def __init__(self, mu_list, q, n=16):
        mu_list = np.atleast_1d(np.asarray(mu_list, float))
        kF = math.sqrt(max(mu_list.max(), 0.0))
        kmax = max(8.0, 3 * (q + kF) + 4)
        brk = [-kmax, kmax] + list(np.arange(-kmax, kmax, 0.05))
        fstep = 0.002 if q < 1 else 0.01            # large q: no Fermi-shell pairing to resolve (xi_S > 0)
        for c0 in (kF - q, kF + q, -kF - q, -kF + q, q, -q, kF, -kF):
            brk += list(np.arange(c0 - 0.3, c0 + 0.3, fstep))
        brk = [b for b in brk if -kmax <= b <= kmax]
        self.k, w = panels(sorted(set(brk)), n)
        self.W = (w / (2 * math.pi))[:, None]
        k = self.k[:, None]
        self.xiS = k * k + q * q - mu_list[None, :]
        self.xiA = 2 * k * q                        # broadcasts against xi_S
        self.kmax, self.nmu = kmax, len(mu_list)

    def dOmega(self, D, inv_g, fixed=False):
        xs, xa = self.xiS, self.xiA
        E = np.sqrt(xs * xs + D * D)
        ax = np.abs(xs)
        F = ax - E
        if not fixed:
            F = F + (np.minimum(0, E + xa) - np.minimum(0, ax + xa)) + (np.minimum(0, E - xa) - np.minimum(0, ax - xa))
        tail = -D * D / (2 * math.pi * self.kmax)
        return D * D * inv_g + float(np.sum(self.W * F)) / self.nmu + tail

    def chi(self):
        return float(np.sum(self.W / (2 * self.xiS))) / self.nmu + 1 / (2 * math.pi * self.kmax)


# transverse energies of D4 (t = 1e-3), 16 x 16 Brillouin-zone grid (midpoints)
T_PERP = 1e-3
kyz = 2 * math.pi * (np.arange(16) + 0.5) / 16
EPERP = (2 * T_PERP * (2 - np.cos(kyz)[:, None] - np.cos(kyz)[None, :])).ravel()


def chi0_1d_exact(mu):
    # (1/2pi) Int dk 1/(2(k^2 - mu)) = 1/(4 sqrt(-mu)), mu < 0
    return 1 / (4 * math.sqrt(-mu))


# ============================================================== KA6 / KA7 (FF machinery checks)
say("\n=== KA6 / KA7: the Fulde-Ferrell machinery ===")
# KA6: D1 Galilean invariance below depairing; weak coupling 1/a = -1.5, mu = 1
inva_w = -1.5
D0_D1 = brentq(lambda D: float(gap_resid_D1(mp.mpf(D), 1, inva_w)), 0.01, 0.5, xtol=1e-15)
q6 = 0.005
g6 = Grid3("D1", 1.0, q6, 1.0)
lhs = g6.omega_total(D0_D1, None, inva_w)
rhs = dOmega_q0("D1", 1.0 - q6**2, D0_D1, None, inva_w, total=True)
ka6 = abs(lhs / rhs - 1)
# no depaired quasiparticles at this q (check)
Echk = np.sqrt(g6.xiS**2 + D0_D1**2)
nodep = bool(np.all(Echk > np.abs(g6.xiA)))
KA["KA6"] = {"Omega(mu,q;D)": lhs, "Omega(mu-q^2,0;D)": rhs, "rel": ka6, "no_depairing_at_q": nodep,
             "pass": ka6 < 1e-6 and nodep}
say(f"KA6 D1 (Delta {D0_D1:.6f}, q {q6}): Omega_FF(mu, q) = {lhs:.12e}, Omega_BCS(mu - q^2) = {rhs:.12e}, rel "
    f"{ka6:.2e}; no depaired quasiparticles: {nodep} -> {'PASS' if KA['KA6']['pass'] else 'FAIL'}")
# KA7: Delta = 0 gives the normal state, independent of q (D2, mu = 1, q = 0.5; D1, q = 0.3)
ka7 = {}
for br, qv in (("D2", 0.5), ("D1", 0.3), ("D3", 0.4)):
    g7 = Grid3(br, 1.0, qv, kF_of(br, 1.0))
    on = g7.omega_normal()
    ka7[br] = {"q": qv, "Omega(0)": on, "minus_P0": -P0_3d(br, 1.0), "rel": abs(on / -P0_3d(br, 1.0) - 1)}
KA["KA7"] = {"by_branch": ka7, "pass": all(v["rel"] < 1e-4 for v in ka7.values())}
del g6, g7, Echk                     # free the large KA grids (peak memory)
say(f"KA7 Delta = 0 at q > 0 equals the normal state: " +
    "; ".join(f"{b} q {v['q']}: {v['Omega(0)']:.8e} vs -P0 {v['minus_P0']:.8e} (rel {v['rel']:.1e})"
              for b, v in ka7.items()) + f" -> {'PASS' if KA['KA7']['pass'] else 'FAIL'}")

KA_ALL = all(v["pass"] for v in KA.values())
OUT["known_answers"] = KA
say(f"KNOWN ANSWERS ALL PASS: {KA_ALL}")

# ============================================================== couplings per branch
say("\n=== COUPLINGS (weak: Delta(q = 0) = 0.05 at mu_eff = 1 above the vacuum threshold; strong: E_b = 10) ===")
COUP = {}


def setup_3d(br):
    out = {}
    if br == "D1":
        for name, inva in (("weak", -1.5), ("strong", 1.5)):
            muv = 0.0 if inva < 0 else -inva**2       # E_b = 2/a^2, mu_vac = -1/a^2
            out[name] = dict(inva=inva, inv_g=None, mu_vac=muv, E_b=(2 * inva**2 if inva > 0 else 0.0))
        return out
    # weak: inv_g from the gap equation at Delta = 0.05, mu = 1, q = 0  (1/|g| = Int 1/(2E))
    kF = kF_of(br, 1.0)
    f = lambda k: k**2 / (2 * mp.sqrt((EPS1[br](k) - 1)**2 + mp.mpf("0.0025")))
    inv_g_w = float(mp.quad(f, [0, kF * 0.9, kF, kF * 1.1, 3, mp.inf]) / (2 * mp.pi**2))
    # its vacuum threshold: chi0(mu_vac) = inv_g (bound state) if inv_g < chi0(0^-)
    chi_at0 = chi0_3d(br, -1e-14)
    if inv_g_w < chi_at0:
        Eb = brentq(lambda lE: chi0_3d(br, -10**lE / 2) - inv_g_w, -30, 3)
        Eb = 10**Eb
    else:
        Eb = 0.0
    out["weak"] = dict(inv_g=inv_g_w, mu_vac=-Eb / 2, E_b=Eb)
    inv_g_s = chi0_3d(br, -5.0)
    out["strong"] = dict(inv_g=inv_g_s, mu_vac=-5.0, E_b=10.0)
    return out


for br in ("D1", "D2", "D3"):
    COUP[br] = setup_3d(br)
# 1-d channel (D5) and D4: weak |g| from Delta = 0.05 at mu = 1; E_b from 1/|g| = 1/(4 sqrt(E_b/2))
f1 = lambda k: 1 / (2 * mp.sqrt((k**2 - 1)**2 + mp.mpf("0.0025")))
inv_g1w = float(mp.quad(f1, [-mp.inf, -3, -1.1, -1, -0.9, 0, 0.9, 1, 1.1, 3, mp.inf]) / (2 * mp.pi))
Eb1w = 2 * (1 / (4 * inv_g1w))**2
COUP["D5"] = {"weak": dict(inv_g=inv_g1w, mu_vac=-Eb1w / 2, E_b=Eb1w),
              "strong": dict(inv_g=chi0_1d_exact(-5.0), mu_vac=-5.0, E_b=10.0)}
# D4: transverse average of the 1-d channel
f4 = lambda mu0: float(np.mean([mp.quad(lambda k: 1 / (2 * mp.sqrt((k**2 + e - mu0)**2 + mp.mpf("0.0025"))),
                                        [-mp.inf, -3, -1, 0, 1, 3, mp.inf]) / (2 * mp.pi) for e in EPERP[::17]]))
inv_g4w = f4(1.0)
chi4 = lambda muv: float(np.mean([1 / (4 * math.sqrt(e - muv)) for e in EPERP]))
Eb4w = 2 * (-brentq(lambda m0: chi4(m0) - inv_g4w, -50, -1e-12))
COUP["D4"] = {"weak": dict(inv_g=inv_g4w, mu_vac=-Eb4w / 2, E_b=Eb4w),
              "strong": dict(inv_g=chi4(-5.0), mu_vac=-5.0, E_b=10.0)}
for br in ("D1", "D2", "D3", "D4", "D5"):
    say(f"  {br}: " + "; ".join(f"{k}: " + ", ".join(f"{a} {v:.6g}" for a, v in d.items() if v is not None)
                              for k, d in COUP[br].items()))
OUT["couplings"] = COUP


# ============================================================== G0 (micro) per branch
def Eq_of(br, q):
    if br in EPS1:
        return EPS1[br](q)
    return q * q                              # D4 along x, D5 aligned channel


def q_a_of(br, mu_eff):
    target = 10 * abs(mu_eff)
    return brentq(lambda q: Eq_of(br, q) - target, 1e-6, 100)


def slope_test(qs, dL):
    dL = np.asarray(dL, float)
    if np.all(np.abs(dL) < 1e-300):
        return dict(slope=float("nan"), cost=False, growing=False, zero=True, PASS=False)
    s = float(np.polyfit(np.log(qs), np.log(np.abs(dL)), 1)[0])
    cost = bool(np.all(dL < 0))
    growing = bool(abs(dL[-1]) > abs(dL[0]))
    return dict(slope=s, cost=cost, growing=growing, zero=False,
                PASS=bool(cost and growing and 2.9 <= s <= 3.1))


say("\n=== G0 (graded): MICROSCOPIC free energy of the paired gas in the gradient-dominated window ===")
say("    window: 16 log-spaced q in [q_a, 10 q_a], E_{q_a} = 10 |mu_eff|; Delta L = L(mu, q) - L(mu, 0); PASS iff cost "
    "sign, growing, slope in [2.9, 3.1]")
G0 = {}
NQ = 16


def cell_3d(br, cname, sgn):
    cp = COUP[br][cname]
    mu = cp["mu_vac"] + sgn * 1.0
    inv_g, inva = cp["inv_g"], cp.get("inva")
    # q = 0 reference: condensation energy
    Dscale = 0.05 if cname == "weak" else 2.0
    f0 = lambda D: dOmega_q0(br, mu, D, inv_g, inva)
    D0, dO0, _ = minimize_D(f0, Dscale)
    Pn = P0_3d(br, mu)
    L0 = Pn - dO0
    qa = q_a_of(br, sgn)
    qs = qa * np.geomspace(1, 10, NQ)
    margins, checks = [], []
    for j, qv in enumerate(qs):
        g = Grid3(br, mu, qv, kF_of(br, mu), mode="window")
        assert np.all(g.xiS > 0), "xi_S must be positive in the window"
        if br == "D1":
            margins.append((-inva / (8 * math.pi)) - g.chi())
        else:
            margins.append(inv_g - g.chi())
        if j in (0, NQ // 2, NQ - 1):
            fq = lambda D: g.dOmega(D, inv_g, inva)
            Dm, dOm, dmin_pos = minimize_D(fq, max(D0, Dscale), ngrid=20)
            checks.append(dict(q=float(qv), Delta_min=Dm, dOmega_min=dOm, min_dOmega_over_Delta_gt_0=dmin_pos))
    # every margin > 0 and every direct check at Delta = 0  =>  L(mu, q) = P_normal(mu) in the window
    certified = bool(all(m_ > 0 for m_ in margins) and all(c_["Delta_min"] == 0.0 for c_ in checks))
    Lq = np.full(NQ, Pn)
    dL = Lq - L0
    st = slope_test(qs, dL)
    return dict(mu=mu, mu_eff=sgn, Delta_q0=D0, E_cond=-dO0, P_normal=Pn, L_q0=L0, q_window=[float(qs[0]), float(qs[-1])],
                margin_min=float(min(margins)), margin_max=float(max(margins)), direct_checks=checks,
                certified_no_condensate=certified, dL_window=[float(dL[0]), float(dL[-1])], **st)


def L1d_channel(mu, qpar, inv_g, Dscale, mu_perp=None):
    """L = P_normal - min_Delta dOmega for a 1-d channel (or D4 transverse average) at twist qpar."""
    mus = np.array([mu]) if mu_perp is None else mu - mu_perp
    g = Grid1(mus, qpar)
    D, dO, _ = minimize_D(lambda D_: g.dOmega(D_, inv_g), Dscale, ngrid=24)
    Pn = float(np.mean([P0_1d(m_) for m_ in mus]))
    return Pn - dO, D, g


def cell_1d(br, cname, sgn):
    cp = COUP[br][cname]
    mu = cp["mu_vac"] + sgn * 1.0
    inv_g = cp["inv_g"]
    Dscale = 0.05 if cname == "weak" else 2.0
    mperp = EPERP if br == "D4" else None
    L0, D0, _ = L1d_channel(mu, 0.0, inv_g, Dscale, mperp)
    qa = q_a_of(br, sgn)
    qs = qa * np.geomspace(1, 10, NQ)
    margins = []
    Lq = []
    for qv in qs:
        if br == "D4":
            g = Grid1(mu - EPERP, qv)
            margins.append(inv_g - g.chi())
            Lq.append(float(np.mean([P0_1d(m_) for m_ in mu - EPERP])))
        else:
            # tangle: average over channel orientation c = |cos|, uniform on [0, 1]
            cstar = math.sqrt(max(sgn, 0) * 1.0) / qv
            cb = sorted(set([0.0, 1.0] + ([cstar] if 0 < cstar < 1 else [])
                            + ([0.5 * cstar, 2 * cstar] if 0 < 2 * cstar < 1 else [])))
            cn, cw = panels(cb, 8)
            vals = []
            for c_ in cn:
                qp = qv * c_
                if qp * qp > 10 * abs(sgn):        # inside the window for that channel: certified below
                    g = Grid1([mu], qp)
                    margins.append(inv_g - g.chi())
                    vals.append(P0_1d(mu))
                else:
                    vals.append(L1d_channel(mu, qp, inv_g, max(D0, Dscale))[0])
            Lq.append(float(np.sum(cw * np.array(vals))))
    dL = np.array(Lq) - L0
    st = slope_test(qs, dL)
    return dict(mu=mu, mu_eff=sgn, Delta_q0=D0, L_q0=L0, q_window=[float(qs[0]), float(qs[-1])],
                margin_min=float(min(margins)) if margins else None, certified_no_condensate=bool(
                    (min(margins) > 0) if margins else True),
                dL_window=[float(dL[0]), float(dL[-1])], **st)


for br in ("D1", "D2", "D3", "D4", "D5"):
    G0[br] = {}
    for cname in ("weak", "strong"):
        for sgn in (+1, -1):
            key = f"{cname},mu_eff{'+' if sgn > 0 else '-'}1"
            res = cell_3d(br, cname, sgn) if br in ("D1", "D2", "D3") else cell_1d(br, cname, sgn)
            G0[br][key] = res
            sl = "n/a (Delta L = 0)" if res["zero"] else f"{res['slope']:.4f}"
            mm_ = "n/a" if res["margin_min"] is None else f"{res['margin_min']:.3e}"
            say(f"  {br} {key:18s} Delta(q=0) {res['Delta_q0']:.4g}; window q {res['q_window'][0]:.3g}-"
                f"{res['q_window'][1]:.3g}; condensate certified absent {res['certified_no_condensate']} (min margin "
                f"{mm_}); Delta L {res['dL_window'][0]:.4e} -> {res['dL_window'][1]:.4e}; slope {sl} "
                f"-> {'PASS' if res['PASS'] else 'FAIL'}")
    if br in ("D1", "D2", "D3"):
        for key, res in G0[br].items():
            for c_ in res["direct_checks"]:
                say(f"      {br} {key} direct minimization at q {c_['q']:.3g}: Delta_min {c_['Delta_min']}, "
                    f"min over Delta > 0 of deltaOmega = {c_['min_dOmega_over_Delta_gt_0']:.3e} (> 0)")
# D4 along y: the window does not exist
Eqy_max = 4 * T_PERP
G0["D4"]["y_direction"] = dict(E_q_max=Eqy_max, window_exists=bool(Eqy_max >= 10), PASS=False)
say(f"  D4 twist along y: E_q = 2t(1 - cos q) <= 4t = {Eqy_max:.1e} < 10 |mu_eff| = 10: no gradient-dominated window "
    f"along y -> FAIL (isotropy clause)")

G0_PASS = {}
for br in G0:
    cells = [v for k, v in G0[br].items() if k != "y_direction"]
    ok = any(v["PASS"] for v in cells)
    if br == "D4":
        ok = ok and G0[br]["y_direction"]["PASS"]
    G0_PASS[br] = ok
say(f"G0 by branch: {G0_PASS}")
OUT["G0"] = G0
OUT["G0_pass"] = G0_PASS

# ---------------------------------------------------------- reported: the full curve Delta L(q), D2 and D1 weak, mu_eff = +1
say("\n--- reported: the full curve Delta L(q) at mu_eff = +1, weak pairing (stiffness, depairing, saturation) ---")
CURVE = {}
for br in ("D2", "D1"):
    cp = COUP[br]["weak"]
    mu = cp["mu_vac"] + 1.0
    D0 = G0[br]["weak,mu_eff+1"]["Delta_q0"]
    L0 = G0[br]["weak,mu_eff+1"]["L_q0"]
    Pn = P0_3d(br, mu)
    kF = kF_of(br, mu)
    qa = q_a_of(br, 1)
    qs = np.concatenate([np.geomspace(1e-3, 0.3, 18) * kF, qa * np.geomspace(1, 10, 4)])
    rows = []
    for qv in qs:
        g = Grid3(br, mu, qv, kF, mode="window" if qv >= qa * 0.999 else "curve")
        Dm, dOm, _ = minimize_D(lambda D: g.dOmega(D, cp["inv_g"], cp.get("inva")), D0, ngrid=24)
        Lq = Pn - dOm                      # Omega(Delta = 0) = -P_normal at every q (KA7)
        rows.append(dict(q=float(qv), Delta=Dm, dL=float(Lq - L0)))
    dLs = np.array([r_["dL"] for r_ in rows])
    Ecd = G0[br]["weak,mu_eff+1"]["E_cond"]
    qdep = next((r_["q"] for r_ in rows if r_["Delta"] == 0.0), None)
    # stiffness from the two smallest q (difference cancels any constant grid offset): dL = -(rho/2) q^2
    rho_q = -2 * (rows[1]["dL"] - rows[0]["dL"]) / (rows[1]["q"]**2 - rows[0]["q"]**2)
    lsl = np.diff(np.log(np.abs(dLs[:18] + 1e-300))) / np.diff(np.log(qs[:18]))
    CURVE[br] = dict(rows=rows, E_cond=Ecd, q_depair=qdep, stiffness_per_q2=rho_q,
                     bound_holds=bool(np.all(np.abs(dLs) <= Ecd * (1 + 1e-3) + 1e-15)),
                     max_local_slope_below_window=float(np.nanmax(lsl)))
    say(f"  {br}: E_cond {Ecd:.4e}; small-q stiffness d2L/dq2 = {-rho_q:.4e} (|Delta L| = rho q^2/2, analytic in q^2); "
        f"Delta first zero at q = {qdep}; |Delta L| <= E_cond everywhere: {CURVE[br]['bound_holds']}; max local "
        f"log-slope below the window {CURVE[br]['max_local_slope_below_window']:.3f}")
    for r_ in rows[::3] + rows[-2:]:
        say(f"      q {r_['q']:.4e}: Delta {r_['Delta']:.4e}, Delta L {r_['dL']:.5e}")
OUT["curve_reported"] = CURVE
del g

# ============================================================== reading F (formal continuation; reported)
say("\n=== READING F (BK's formal odd continuation of each branch's EOS; reported, never the lane label) ===")


def P_odd(P0fun, X):
    return np.sign(X) * P0fun(abs(X))


def P0_D4(mu):
    return float(np.mean([P0_1d(mu - e) for e in EPERP]))


def LF(br, mu_eff, q, direction="x"):
    if br in ("D1", "D2", "D3"):
        P0f = lambda m: P0_3d(br, m)
        return P_odd(P0f, mu_eff - EPS1[br](q)) - P_odd(P0f, mu_eff)
    if br == "D4":
        Eq = q * q if direction == "x" else 2 * T_PERP * (1 - math.cos(q))
        return P_odd(P0_D4, mu_eff - Eq) - P_odd(P0_D4, mu_eff)
    # D5: orientation average
    cn, cw = panels([0, 0.25, 0.5, 0.75, 1.0], 24)
    return float(np.sum(cw * np.array([P_odd(P0_1d, mu_eff - (q * c_)**2) - P_odd(P0_1d, mu_eff) for c_ in cn])))


GF = {}
for br in ("D1", "D2", "D4", "D5"):
    GF[br] = {}
    for sgn in (+1, -1):
        qa = q_a_of(br, sgn)
        qs = qa * np.geomspace(1, 10, NQ)
        st = slope_test(qs, [LF(br, sgn, qv) for qv in qs])
        GF[br][f"mu_eff{'+' if sgn > 0 else '-'}1"] = st
GF["D4"]["y_direction"] = dict(window_exists=False, saturates_at=float(LF("D4", 1.0, math.pi, "y")), PASS=False)
# D3: scan mu_eff over 1e-3 .. 1e3
GF["D3"] = {}
for lm in (-3, -2, -1, 0, 1, 2, 3):
    for sgn in (+1, -1):
        me = sgn * 10.0**lm
        qa = brentq(lambda q: EPS1["D3"](q) - 10 * abs(me), 1e-9, 1e3)
        qs = qa * np.geomspace(1, 10, NQ)
        GF["D3"][f"mu_eff {me:+.0e}"] = slope_test(qs, [LF("D3", me, qv) for qv in qs])
d3sl = [v["slope"] for v in GF["D3"].values()]
GF_PASS = {br: any(v.get("PASS", False) for k, v in GF[br].items() if k != "y_direction") and
           (br != "D4" or GF["D4"]["y_direction"]["PASS"]) for br in GF}
for br in ("D1", "D2", "D3", "D4", "D5"):
    if br == "D3":
        say(f"  D3 crossover: formal slopes over mu_eff 1e-3..1e3 (both signs) range {min(d3sl):.3f} - {max(d3sl):.3f} "
            f"-> {'PASS' if GF_PASS['D3'] else 'FAIL'}")
        continue
    say(f"  {br}: " + "; ".join(f"{k}: slope {v['slope']:.4f}, cost {v['cost']}" for k, v in GF[br].items()
                               if k != "y_direction") + f" -> {'PASS' if GF_PASS[br] else 'FAIL'}")
say(f"  D4 along y: the formal L saturates at {GF['D4']['y_direction']['saturates_at']:.3e} (bounded by the "
    f"transverse band): anisotropic")
# the dimensional rule
d_, z_ = sp.symbols("d z", positive=True, integer=True)
sol = sp.solve([sp.Eq(d_ + z_, 3), sp.Eq(2 * (d_ + z_), 3 * z_)], [d_, z_], dict=True)
say(f"  dimensional rule: gradient-dominated L ~ c q^(d+z); q^3 and P_0 ~ mu^(3/2) [(d+z)/z = 3/2] solve to {sol}")
OUT["reading_F"] = {"cells": GF, "pass": GF_PASS, "dimensional_rule_solution": str(sol),
                    "formal_exponents": {"D1": 5, "D2": 9, "D3": [min(d3sl), max(d3sl)], "D4x": 3, "D5": 3}}

# ============================================================== S
say("\n=== S: shape of the point-mass force law a = a_N + a_theta, a_theta = (a_*^(p-2) a_N)^(1/(p-1)) ===")
XG = np.logspace(-2, 2, 41)
MU_LAW = XG / (1 + XG)
SLOPE_LAW = 1 / (1 + 0.01)
YG = np.logspace(-60, 6, 13201)


def mu_of_x(p, lA, xv):
    A = 10.0**lA
    if p is None:
        return np.ones_like(xv)
    xs = YG + A**((p - 2) / (p - 1)) * YG**(1 / (p - 1))
    return np.exp(np.interp(np.log(xv), np.log(xs), np.log(YG / xs)))


def shape_stats(p, lA):
    mu = mu_of_x(p, lA, XG)
    band = float(np.max(np.abs(mu - MU_LAW)))
    h = 1e-3
    m1 = mu_of_x(p, lA, np.array([0.01 * math.exp(h)]))[0]
    m2 = mu_of_x(p, lA, np.array([0.01 * math.exp(-h)]))[0]
    slope = (math.log(m1) - math.log(m2)) / (2 * h)
    return band, slope, max(band / 0.1, abs(slope - SLOPE_LAW) / 0.1)


def fitS(p):
    if p is None:
        b, s, _ = shape_stats(None, 0.0)
        return dict(p=None, lA=None, max_dmu=b, deep_slope=s, S="FAIL")
    res = differential_evolution(lambda v: shape_stats(p, v[0])[2], [(-3, 3)], seed=0, tol=1e-10, maxiter=300,
                                 popsize=30, polish=True)
    b, s, _ = shape_stats(p, res.x[0])
    ok = b <= 0.1 and abs(s - SLOPE_LAW) <= 0.1
    return dict(p=p, lA=float(res.x[0]), A=float(10**res.x[0]), max_dmu=b, deep_slope=s, S="PASS" if ok else "FAIL")


S = {"micro (no gradient energy: a_theta = 0)": fitS(None)}
for p in (3, 5, 9):
    S[f"p = {p}"] = fitS(p)
for k_, v in S.items():
    say(f"  {k_:42s} max |dmu| {v['max_dmu']:.4f}, deep slope {v['deep_slope']:.4f}"
        + (f", a_*/a0 {v['A']:.4f}" if v.get('A') else "") + f" -> S {v['S']}")
S_BRANCH_F = {"D1": S["p = 5"]["S"], "D2": S["p = 9"]["S"], "D3": "FAIL (formal slope 5-9, between p = 5 and 9)",
              "D4": "FAIL (anisotropic: flux only along x)", "D5": S["p = 3"]["S"]}
OUT["S"] = {"fits": S, "by_branch_reading_F": S_BRANCH_F, "micro": S["micro (no gradient energy: a_theta = 0)"]["S"]}
A_FIT = S["p = 3"]["A"]

# ============================================================== C (for the reading-F survivor D5; D2 reported)
say("\n=== C: size and locality (rule H; the reading-F survivor D5, tangle) ===")
# tangle normalisation: L = nu_s <P_1d(mu - (n.q)^2/2m_f)>, gradient-dominated -> -nu_s |grad theta|^3/(48 pi m_f)
nus, mf, qq_ = sp.symbols("nu_s m_f q", positive=True)
cc = sp.symbols("c", positive=True)
P1d_sym = lambda Xv: sp.Rational(4, 3) / sp.pi * sp.sqrt(2 * mf) * Xv**sp.Rational(3, 2)
Ltan = -nus * sp.integrate(P1d_sym((qq_ * cc)**2 / (2 * mf)), (cc, 0, 1))
Ltan_theta = sp.simplify(Ltan.subs(qq_, sp.Symbol("gt", positive=True) / 2))
Lam_eff = sp.simplify(-Ltan_theta / (sp.Rational(2, 3) * sp.Symbol("gt", positive=True)**3))
say(f"  tangle, gradient-dominated (formal): L = {Ltan_theta}  =>  BK's Lambda_eff = {Lam_eff}")
CRES = {}


def r_of_x(xv, a0, Mb=M_REF):
    return math.sqrt(GM_SUN * Mb * (1 + xv) / (xv**2 * a0))


for f, a0 in FOOT.items():
    E_a0 = HBAR * a0 / C / EV
    a0p = A_FIT * E_a0
    vf = (M_REF * GM_SUN * a0) ** 0.25
    row = {}
    for aname, alpha in (("alpha 4 pi", G4PI), ("alpha 1", 1.0)):
        Lam = math.sqrt(8 * math.pi * M_PL * a0p / alpha**3)
        # D1: superflow / Fermi speed at x = 1 of the reference galaxy
        y1 = brentq(lambda y: y + math.sqrt(A_FIT * y) - 1.0, 1e-9, 1.0)
        a_th_SI = (1.0 - y1) * a0
        grad_th = (HBAR * a_th_SI / C / EV) * M_PL / (alpha * Lam)          # eV
        v_esc = 2 * vf / C
        mf_min = grad_th / (2 * v_esc)
        nu_s = Lam / float((Lam_eff / nus).subs(mf, mf_min))                 # eV^2 (= 32 pi m_f Lambda)
        spacing = HBARC / math.sqrt(nu_s)                                    # m
        kF_r001 = None
        y001 = brentq(lambda y: y + math.sqrt(A_FIT * y) - 0.01, 1e-14, 0.01)
        gth001 = (HBAR * (0.01 - y001) * a0 / C / EV) * M_PL / (alpha * Lam)
        lam_F = 2 * math.pi * HBARC / (gth001 / 2)                          # channel Fermi wavelength (k_F = |q_par|)
        r001 = r_of_x(0.01, a0)
        amp = max(math.log10(nu_s / M_PL**2), math.log10(mf_min / M_PL), math.log10(Lam / M_PL), math.log10(alpha / G4PI))
        loc = max(math.log10(spacing / r001), math.log10(lam_F / r001))
        rho_de = 4 * a0**2 / (C**2 * G)
        rho_de_eV4 = rho_de * C**2 / EV * HBARC**3
        Ts_max = rho_de_eV4 / nu_s                                          # tension (eV^2) at which nu_s T_s = rho_DE
        row[aname] = dict(Lambda_eV=Lam, grad_theta_eV=grad_th, mf_min_eV=mf_min, nu_s_eV2=nu_s, spacing_m=spacing,
                          lambda_F_r001_m=lam_F, r001_m=r001, log10R_amp=amp, log10R_loc=loc,
                          C_H="PASS" if (amp <= 0 and loc <= 0) else "FAIL", tension_max_eV=math.sqrt(Ts_max))
        say(f"  [{f}] {aname}: Lambda {Lam:.3e} eV; |grad theta| at x = 1 {grad_th:.3e} eV; m_f >= {mf_min:.3e} eV "
            f"(superflow <= 2 v_f); nu_s = 32 pi m_f Lambda = {nu_s:.3e} eV^2 (spacing {spacing:.3e} m); "
            f"C-amp log10 R {amp:.2f}, C-loc {loc:.2f} -> C_H {row[aname]['C_H']}; string tension <= "
            f"({math.sqrt(Ts_max):.3e} eV)^2 for nu_s T_s <= rho_DE")
    CRES[f] = row
C_D5 = {f: ("PASS" if all(v["C_H"] == "PASS" for v in CRES[f].values()) else "FAIL") for f in FOOT}
# R3: the k^6 scale that reproduces BK's EOS amplitude at QX28's implied (m, Lambda)
csym, mB, LB = sp.symbols("c_6 m_B Lambda_B", positive=True)
muf = sp.symbols("mu_f", positive=True)
eq = sp.Eq(2 * muf**sp.Rational(3, 2) / (9 * sp.pi**2 * sp.sqrt(csym)),
           sp.Rational(2, 3) * LB * (2 * mB)**sp.Rational(3, 2) * (2 * muf)**sp.Rational(3, 2))
c6sol = sp.solve(eq, csym)[0]
R3 = {}
for f, (mBv, LBv) in {"canonical": (0.57, 0.11e-3), "alt": (0.55, 0.15e-3)}.items():
    c6 = float(c6sol.subs({mB: mBv, LB: LBv}))
    R3[f] = dict(c6_eV_minus5=c6, M6_eV=c6 ** (-1 / 5))
say(f"  R3 k^6 scale for BK's EOS amplitude at QX28's (m, Lambda): c_6 = {c6sol}; " +
    "; ".join(f"[{f}] M_6 = c_6^(-1/5) = {v['M6_eV']:.3e} eV" for f, v in R3.items()))
OUT["C"] = {"D5_reading_F": CRES, "C_D5": C_D5, "Lambda_eff_tangle": str(Lam_eff), "R3_k6_scale": R3}

# ============================================================== U
say("\n=== U: action ===")
U = {}
for br in ("D1", "D2", "D3", "D4", "D5"):
    d, z = DZ[br]
    g2 = contact_dim(d, z, 2)
    U1 = "PASS" if g2 >= 0 else "FAIL"
    U[br] = dict(d=d, z=z, two_body_dim=g2, three_body_dim=contact_dim(d, z, 3), U1=U1)
# U2: theta = arg(psi_d psi_u): not a polynomial in the pair field
Dre, Dim = sp.symbols("D_re D_im", real=True)
theta_expr = sp.atan2(Dim, Dre)
try:
    sp.Poly(theta_expr, Dre, Dim)
    is_poly = not theta_expr.has(sp.atan2, sp.atan, sp.log)
except sp.PolynomialError:
    is_poly = False
# the polynomial alternative: -lambda n_B (psi psi + h.c.) -> -2 lambda n_B |<psi psi>| cos(theta)
thv, lam_, nB, A_ = sp.symbols("theta lambda n_B A", real=True)
Lalt = -2 * lam_ * nB * A_ * sp.cos(thv)
src_alt = sp.diff(Lalt, thv)
src_BK = sp.diff(-al * Lb * thv * nB / MP, thv)
U2 = dict(theta_is_polynomial_in_pair_field=bool(is_poly), U2="FAIL" if not is_poly else "PASS",
          BK_static_source=str(src_BK), polynomial_alternative_source=str(src_alt),
          polynomial_alternative_dim_at_z6=9 - 3 - 3,
          note="the polynomial alternative's source is proportional to sin(theta): theta-dependent and bounded, so "
               "Gauss's law does not give the enclosed baryon mass (KA3's BK law does not follow)")
for br in U:
    U[br]["U2"] = U2["U2"]
    U[br]["U"] = "PASS" if (U[br]["U1"] == "PASS" and U2["U2"] == "PASS") else "FAIL"
    say(f"  {br} (d, z) = ({U[br]['d']}, {U[br]['z']}): 2-body {U[br]['two_body_dim']:+d}, 3-body "
        f"{U[br]['three_body_dim']:+d} -> U1 {U[br]['U1']}; U2 {U2['U2']} -> U {U[br]['U']}")
say(f"  U2: theta = atan2(Im, Re) of the pair field is polynomial: {is_poly}; BK source dL/dtheta = {src_BK}; the "
    f"polynomial alternative -lambda n_B (psi psi + h.c.) has dimension {9 - 3 - 3} at z = 6 and source {src_alt}")
OUT["U"] = {"by_branch": U, "U2": U2}

# ============================================================== E
say("\n=== E: equivalence principle and fifth force (inputs PROVISIONAL, the record's CFG122 values) ===")
GM_E, R_E, H_MIC = 3.986004418e14, 6.371e6, 7.1e5
g_sun = GM_SUN / AU**2
g_mic = GM_E / (R_E + H_MIC)**2
ISO = {"48Ti": (48, 47.94794), "195Pt": (195, 194.96479)}
dBmu = abs(ISO["48Ti"][0] / ISO["48Ti"][1] - ISO["195Pt"][0] / ISO["195Pt"][1])
B_CAS, B_MIC, S_EPH = 2.3e-5, 1e-15, 1.27e-5
E = {}
for f, a0 in FOOT.items():
    a0p = A_FIT * a0
    out = {}
    for rd, fa in (("F (unscreened)", lambda g_: math.sqrt(a0p * g_)), ("micro (depaired)", lambda g_: 0.0)):
        aS, aE = fa(g_sun), fa(g_mic)
        eps = aS / g_sun
        gm1 = 2 * eps / (1 + eps)
        eta = dBmu * aE / g_mic
        anom = aS / a0
        ok = gm1 <= B_CAS and eta <= B_MIC and anom <= S_EPH
        out[rd] = dict(a_1AU=aS, gamma_minus_1=gm1, x_Cassini=gm1 / B_CAS, eta=eta, x_MICROSCOPE=eta / B_MIC,
                       anomaly_over_a0=anom, x_ephemeris=anom / S_EPH, E="PASS" if ok else "FAIL")
        say(f"  [{f}] {rd}: a_theta(1 AU) {aS:.3e} m/s^2; |gamma-1| {gm1:.3e} ({gm1 / B_CAS:.3g} x Cassini); "
            f"eta(Ti-Pt, baryon number) {eta:.3e} ({eta / B_MIC:.3g} x MICROSCOPE); anomaly {anom:.3g} a0 "
            f"({anom / S_EPH:.3g} x ceiling) -> E {out[rd]['E']}")
    out["mass_coupling_eta"] = 0.0
    E[f] = out
say(f"  Delta(B/mu) Ti-Pt = {dBmu:.4e} (recalled isotope masses, PROVISIONAL); a coupling to mass instead gives eta = 0 "
    f"at MICROSCOPE but leaves Cassini and the ephemeris unchanged")
OUT["E"] = E

# ============================================================== D
say("\n=== D: the particle's own bounds (reported items) ===")
D = {}
# D1: Pauli / superflow (D5 under F, from C's numbers)
D["D1"] = {f: {a: dict(mf_min_eV=v["mf_min_eV"], excluded=bool(v["mf_min_eV"] > M_PL)) for a, v in CRES[f].items()}
           for f in FOOT}
# D2 forest: quoted caveat
D["D2"] = "record: undecided on raw forest data; a 1-D proxy against a LCDM yardstick falls 1000-5000x short (FOREST_KILL_AUDIT); no flag"
# D3 clusters: inherited QX28
D["D3"] = "QX28 (BK class, normal phase in clusters): G4, G5 FAIL on both footings -> excluded (inherited) for BK-class branches"
# D4: P = K rho^3 with QX28's K: w(1089), stiff kinetic energy vs radiation
omega_b = 0.02238                            # PROVISIONAL, measured baryon density
rho_b0 = omega_b * 1.87834e-26               # kg/m^3
kB = 1.380649e-23
T0 = 2.7255
rho_gam0 = (math.pi**2 / 15) * (kB * T0)**4 / (HBAR * C)**3 / C**2        # kg/m^3 equivalent
rho_rad0 = rho_gam0 * (1 + 0.2271 * 3.044)
K_SI = {f: K * 1e6 * KPC**6 / M_SUN**2 for f, K in {"canonical": 1.585e-6, "alt": 1.0e-6}.items()}   # m^8 s^-2 kg^-2
D4 = {}
zBBN = 1e5 / (8.617333e-5 * T0) - 1          # T = 0.1 MeV
for f in FOOT:
    K = K_SI[f]
    row = {}
    for zz, nm in ((1089, "z1089"), (zBBN, "BBN")):
        rc = 5.41 * rho_b0 * (1 + zz)**3
        w = K * rc**2 / C**2
        u = 0.5 * K * rc**3 / C**2           # kinetic energy density, mass units (P = K rho^3, u = P/2)
        rr = rho_rad0 * (1 + zz)**4
        row[nm] = dict(w=w, u_over_rho_rad=u / rr, f_max_for_u_le_0p1_rad=(0.1 * rr / u)**(1 / 3))
    row["must_sit_beside"] = bool(row["z1089"]["w"] > 0.01)
    D4[f] = row
    say(f"  [{f}] D4 P = K rho^3, K = QX28's K_min: w(1089) = {row['z1089']['w']:.3e}, kinetic/radiation at 1089 "
        f"{row['z1089']['u_over_rho_rad']:.3e}, at BBN {row['BBN']['u_over_rho_rad']:.3e}; largest share of 5.41 rho_b "
        f"with kinetic <= 0.1 radiation: {row['z1089']['f_max_for_u_le_0p1_rad']:.3e} (1089), "
        f"{row['BBN']['f_max_for_u_le_0p1_rad']:.3e} (BBN) -> must sit beside: {row['must_sit_beside']}")
D["D4"] = D4
for f in FOOT:
    for a, v in D["D1"][f].items():
        say(f"  [{f}] D1 {a}: m_f >= {v['mf_min_eV']:.3e} eV (superflow and channel Fermi speed <= escape speed); "
            f"excluded: {v['excluded']}")
say(f"  D2: {D['D2']}")
say(f"  D3: {D['D3']}")
OUT["D"] = D
D_EXCLUDED = True    # D3 inherited for every BK-class branch

# ============================================================== labels
say("\n=== LABELS ===")


def branch_label(g0, s, c, u, e, d_excl):
    if not g0:
        return "KILLED AT G0"
    if s != "PASS":
        return "NONE"
    if c == "PASS" and u == "PASS" and e == "PASS" and not d_excl:
        return "CANDIDATE PASSES"
    return "SHAPE ONLY"


LAB = {}
for f in FOOT:
    LAB[f] = {}
    for br in ("D1", "D2", "D3", "D4", "D5"):
        micro = branch_label(G0_PASS[br], OUT["S"]["micro"], "n/a", U[br]["U"], "n/a", D_EXCLUDED)
        sF = S_BRANCH_F[br] if S_BRANCH_F[br] in ("PASS", "FAIL") else "FAIL"
        cF = C_D5[f] if br == "D5" else "n/a"
        eF = E[f]["F (unscreened)"]["E"]
        LAB[f][br] = dict(lane=micro, reading_F=branch_label(GF_PASS[br], sF, cF, U[br]["U"], eF, D_EXCLUDED),
                          renormalizable=U[br]["U1"] == "PASS")
        say(f"  [{f}] {br} {DNAME[br]:52s} G0 {'PASS' if G0_PASS[br] else 'FAIL'} -> {LAB[f][br]['lane']:14s} | "
            f"reading F: G0F {'PASS' if GF_PASS[br] else 'FAIL'} -> {LAB[f][br]['reading_F']}")
ORDER = ["KILLED AT G0", "NONE", "SHAPE ONLY", "CANDIDATE PASSES"]
renorm = [br for br in U if U[br]["U1"] == "PASS"]
lane_by_foot = {f: max((LAB[f][br]["lane"] for br in renorm), key=ORDER.index) for f in FOOT}
lane_F = {f: max((LAB[f][br]["reading_F"] for br in renorm), key=ORDER.index) for f in FOOT}
LANE = lane_by_foot["canonical"] if lane_by_foot["canonical"] == lane_by_foot["alt"] else \
    min(lane_by_foot.values(), key=ORDER.index)
if not KA_ALL:
    LANE = "OPEN (a known answer failed)"
say(f"LSF1 LANE LABEL: {LANE}   (by footing {lane_by_foot}; reading F, reported only: {lane_F})")
OUT["labels"] = {"by_footing": LAB, "lane": LANE, "lane_by_footing": lane_by_foot, "reading_F_lane": lane_F}

# ============================================================== reported
say("\n=== REPORTED (not graded) ===")
REP = {}
REP["R1"] = ("BK's Solar-System argument (flow above a critical velocity near the Sun, condensate loses coherence) uses "
             "the same criterion G0 computes: once E_q > mu_eff the pair band at twist q lies above the chemical "
             "potential (KA8) and no condensate exists at any coupling. That is the gradient-dominated condition "
             "itself, so it holds wherever BK's MOND regime is used, not only near the Sun.")
REP["R2"] = {f: {a: dict(spacing_m=v["spacing_m"], nu_s_eV2=v["nu_s_eV2"], tension_max_eV=v["tension_max_eV"])
                 for a, v in CRES[f].items()} for f in FOOT}
REP["R4"] = ("kappa: a0' = alpha^3 Lambda^2/(8 pi M_Pl) with Lambda_eff = nu_s/(32 pi m_f) (tangle) or c_6 (k^6): every "
             "branch carries a free dimensionful input, not tied to rho_DE. The 5.41 is untouched.")
# R5: strong pairing EOS exponent (D2, from the q = 0 mean field at mu_eff = 0.5, 1, 2)
r5 = {}
for br in ("D2", "D5"):
    cp = COUP[br]["strong"]
    Ls = []
    for me in (0.5, 1.0, 2.0):
        mu = cp["mu_vac"] + me
        if br == "D2":
            D0, dO0, _ = minimize_D(lambda D_: dOmega_q0(br, mu, D_, cp["inv_g"]), 2.0)
            Ls.append(P0_3d(br, mu) - dO0)
        else:
            Ls.append(L1d_channel(mu, 0.0, cp["inv_g"], 2.0)[0])
    r5[br] = dict(L=Ls, exponent=float(np.polyfit(np.log([0.5, 1, 2]), np.log(Ls), 1)[0]))
REP["R5"] = r5
say(f"  R1: {REP['R1']}")
say(f"  R4: {REP['R4']}")
say(f"  R5 strong pairing (BEC side, E_b = 10): d ln P/d ln mu_eff = " +
    ", ".join(f"{b} {v['exponent']:.3f}" for b, v in r5.items()) + " (a Bose gas of pairs, not the Fermi sea's 3/2)")
OUT["reported"] = REP

# ============================================================== MUTATE
if MUTATE:
    say("\n=== MUTATE TWINS ===")
    TW = {}
    # M1: BK formal P(X) = X|X|^(1/2) with Galilean kinematics through the G0 window test
    qa = math.sqrt(10)
    qs = qa * np.geomspace(1, 10, NQ)
    PBKf = lambda Xv: np.sign(Xv) * abs(Xv)**1.5
    st = slope_test(qs, [PBKf(1 - q_**2) - PBKf(1) for q_ in qs])
    TW["M1"] = dict(**st, bites=st["PASS"])
    # M2: S detector
    TW["M2"] = dict(p3=S["p = 3"], p9=S["p = 9"], bites=bool(S["p = 3"]["S"] == "PASS" and
                                                             abs(S["p = 3"]["max_dmu"] - 0.0946) < 1e-3 and
                                                             S["p = 9"]["S"] == "FAIL"))
    # M3: U1 counter
    TW["M3"] = dict(d3z2_3body=contact_dim(3, 2, 3), d1z2_2body=contact_dim(1, 2, 2), d3z6_2body=contact_dim(3, 6, 2),
                    bites=bool(contact_dim(3, 2, 3) == -4 and contact_dim(1, 2, 2) == 1 and contact_dim(3, 6, 2) == 3))
    # M4: E with alpha -> 0 (a_theta = 0) passes; formal force fails
    TW["M4"] = dict(zero_force=E["canonical"]["micro (depaired)"]["E"], formal=E["canonical"]["F (unscreened)"]["E"],
                    bites=bool(E["canonical"]["micro (depaired)"]["E"] == "PASS" and
                               E["canonical"]["F (unscreened)"]["E"] == "FAIL"))
    # M5: the Galilean identity applied to eps = k^6 must fail
    cp = COUP["D2"]["weak"]
    mu = cp["mu_vac"] + 1
    D0 = G0["D2"]["weak,mu_eff+1"]["Delta_q0"]
    q5 = 0.002
    g5 = Grid3("D2", mu, q5, kF_of("D2", mu))
    lhs5 = g5.omega_total(D0, cp["inv_g"])
    rhs5 = dOmega_q0("D2", mu - q5**6, D0, cp["inv_g"], total=True)
    base5 = dOmega_q0("D2", mu, D0, cp["inv_g"], total=True)
    shift_FF = lhs5 - base5                                   # measured: Omega(mu, q) - Omega(mu, 0)
    n5 = (P0_3d("D2", mu * (1 + 1e-6)) - P0_3d("D2", mu * (1 - 1e-6))) / (2e-6 * mu)
    shift_gal = n5 * q5**6                                    # the Galilean identity's prediction, Omega shift = n E_q
    del g5
    TW["M5"] = dict(lhs=lhs5, rhs=rhs5, shift_measured=shift_FF, shift_if_Galilean=shift_gal,
                    bites=bool(abs(shift_FF) > 1e-8 and abs(shift_FF) > 100 * abs(shift_gal)))
    # M6: convexity detector
    TW["M6"] = dict(free_gas_stable=True, BK_odd_unstable=bool(sp.simplify(d2).subs(Xn, 1) < 0),
                    bites=bool(sp.simplify(d2).subs(Xn, 1) < 0 and sp.simplify(conv_free.subs(p_s, sp.Rational(3, 2)))
                               > 0))
    # M7: forced superfluid (Delta held, no depairing), D2 weak mu_eff = +1, in the window
    qa = q_a_of("D2", 1)
    qs = qa * np.geomspace(1, 10, NQ)
    O0 = dOmega_q0("D2", mu, D0, cp["inv_g"], total=True)
    dLf = []
    for q_ in qs:
        g7 = Grid3("D2", mu, q_, kF_of("D2", mu), mode="window")
        dLf.append(-(g7.omega_fixed(D0, cp["inv_g"]) - O0))
    st7 = slope_test(qs, dLf)
    TW["M7"] = dict(**st7, dL_window=[float(dLf[0]), float(dLf[-1])], bites=bool(st7["growing"]))
    for k_, v in TW.items():
        say(f"  {k_}: bites {v['bites']}  " + json.dumps({a: b for a, b in v.items() if a != 'bites'}, default=str)[:400])
    OUT["MUTATE"] = TW
    say(f"ALL TWINS BITE: {all(v['bites'] for v in TW.values())}")

# ============================================================== write
OUT["runtime_s"] = time.time() - T_START
OUT["max_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
say(f"\nruntime {OUT['runtime_s']:.1f} s; max RSS {OUT['max_rss_GB']:.2f} GB")
tag = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"lsf1{tag}.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
with open(os.path.join(HERE, f"lsf1{tag}.out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
