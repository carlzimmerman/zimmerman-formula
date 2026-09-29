#!/usr/bin/env python3
"""CFG151 -- referee: independent re-derivation of CFG120's door-1 headline.

Frozen criteria: ../CFG151_FROZEN_CRITERIA.md (its sha256 is printed first).  Written from those
criteria, CFG120's frozen criteria and README, the shared ten-door gates, and CFG44's README and
Bcommon docstrings only.  Nothing is imported from the repository.  numpy + scipy, one process,
one BLAS thread.

Modes (environment variable MUTATE):
  unset  main run
  a      the normalisation scales as 1/M_b: N(M) = N0 M0/M, N0 = the point-mass best fit at M0
  b      the kernel keyed to each mass: K0 with r0 = r_M(M) and N = 1; RM and PL with lambda0 = r_M(M)
Outputs, next to this file: cfg151_kernel_referee[_MUTATE_x].out and ..._results.json.

The algebra (my derivation)
---------------------------
Model (CFG120's Reading P): rho_D(x) = int d^3x' K(|x - x'|) rho_b(x'), K = N k(s), fixed constants.
C_model = rho_D r^3 g_tot = G r rho_D (M_b + M_D);  C_target = (a0/4 pi) M_b(<r);  R = C_model/C_target.

Spherical convolution: s^2 = r^2 + r'^2 - 2 r r' mu gives s ds = -r r' dmu, so
    int_{-1}^{1} k(s) dmu = [Q(r + r') - Q(|r - r'|)] / (r r'),   Q(s) = int^s s' k(s') ds',
    rho_D(r) = (2 pi / r) int_0^inf r' rho_b(r') [Q(r + r') - Q(|r - r'|)] dr'.
Point mass: rho_D = N M k(r) and M_D = N M m(r), m(r) = 4 pi int_0^r k s^2 ds, hence
    R(r; M) = (4 pi G M / a0) r N k(r) [1 + N m(r)].
At fixed r and a fixed kernel R is proportional to M exactly (C_model ~ M^2, C_target ~ M).  For any
profile at fixed shape and size, rho_b -> lam rho_b gives rho_D -> lam rho_D and M_D -> lam M_D, so
C_model -> lam^2 C_model.  On the overlap r in [0.1 r_M(1e12), 30 r_M(1e9)] every grid mass is in
range, so the spread S = max_M R / min_M R = 1000 and the mass spread F = sqrt(S) = 31.6228 for
EVERY fixed kernel.  Realisability: B(r) = r N k [1 + N m] can be any positive function, because
(1 + m)^2 = 1 + 8 pi int_0^r r' B dr'.  A constant B (K0 frozen at M0 = 10^10.5 with N = 1) gives
R = M/M0 at every x and attains the floor.  The target needs B_req = a0/(4 pi G M) = 1/(4 pi r_M^2),
exactly 1/M.  The amplitude N enters C_model quadratically (the phantom's own mass is in g_tot), so
the best-fit N goes as 1/M where N m << 1 and as M^-1/2 where N m >> 1; its ratio across masses is
reported, not pinned.

Closed-form Q (unit N):  K0: asinh(s/r0)/(4 pi r0);  RM: -[E1(mu s) + exp(-mu s)]/(4 pi);
PL: ln(s)/(4 pi).  Differences are evaluated in forms free of cancellation, using
(r + r') - |r - r'| = 2 min(r, r').
Target for extended baryons (control C2): dM_c/dr = (a0/G) r M_b/(M_b + M_c), from
rho_c r^3 g_tot = (a0/4 pi) M_b(<r); leading order near the centre M_c = sqrt(a0 M r^5/(15 G h^3)).
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import hashlib
import json
import math
import sys
import time
import warnings
from pathlib import Path

import numpy as np
from scipy import integrate, interpolate, special

T_START = time.time()
HERE = Path(__file__).resolve().parent
REPO = Path(os.environ["ZF_REPO"]).resolve() if os.environ.get("ZF_REPO") else HERE.parents[1]
SPEC = REPO / "campaign_fresh_gravity" / "CFG151_FROZEN_CRITERIA.md"

MODE = os.environ.get("MUTATE", "").strip().lower()
if MODE not in ("", "a", "b"):
    print("MUTATE must be unset, 'a' or 'b'")
    sys.exit(2)
STEM = "cfg151_kernel_referee" + (f"_MUTATE_{MODE}" if MODE else "")

LINES = []


def out(s=""):
    print(s, flush=True)
    LINES.append(s)


# ----------------------------------------------------------------------------- constants
GM_SUN = 1.3271244e20            # m^3 s^-2, IAU 2015 nominal
KPC = 3.0856775814913673e19      # m
G = GM_SUN / (KPC * 1.0e6)       # kpc (km/s)^2 / Msun
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}           # m s^-2 (CFG120's values)
A0 = {k: v * KPC / 1.0e6 for k, v in A0_SI.items()}           # (km/s)^2 / kpc
FOOTINGS = ("canonical", "alt")
FOUR_PI = 4.0 * math.pi

MASSES = 10.0 ** (9.0 + 0.25 * np.arange(13))                 # 13 point masses, 0.25 dex
XGRID = np.logspace(-1.0, math.log10(30.0), 200)               # G1 x-grid
M0 = 10.0 ** 10.5                                              # the grid's ln-centre
SPHERE_MASSES = (1.0e9, 1.0e10, 1.0e11, 1.0e12)
H_ASSIGN = {"h(M)=2,3,4,5": (2.0, 3.0, 4.0, 5.0), "h=2 at every mass": (2.0, 2.0, 2.0, 2.0)}
PM_SLOTS = ("K0@10.5", "K0@9", "K0@12", "RM0.06", "RM0.10", "PL")
SP_SLOTS = ("K0@10.5", "RM0.06", "RM0.10", "PL")
RECALLED = ((3.0, 0.06), (3.0, 0.10), (10.0, 0.06), (10.0, 0.10))   # (lambda0 kpc, mu0 /kpc), A = 1

CFG120 = {"F": 31.6228, "ov_lo": 3.87, "ov_hi": 36.55, "window": 1.222, "lin_dev": 0.998,
          "rm_fit": 3.97, "Kstar_grid": 3.74, "Rlo": 0.032, "Rhi": 31.6}
FLOOR = 0.5 * math.log(1000.0)                                 # ln sqrt(1000) = 3.4539

QUAD_EPSREL = 1.0e-10
NGRID = 1200
WARN = {"n": 0}


def r_M(M, a0):
    return math.sqrt(G * M / a0)


# ----------------------------------------------------------------------------- kernels (unit N)
_GLX, _GLW = np.polynomial.legendre.leggauss(20)


def eint_diff(x, y):
    """int_x^y exp(-t)/t dt for 0 < x <= y, without cancellation."""
    if y <= x:
        return 0.0
    if x <= 0.0:
        return math.inf
    L = y - x
    if L < min(0.5 * x, 2.0):
        t = 0.5 * L * _GLX + 0.5 * (x + y)
        return 0.5 * L * float(np.sum(_GLW * np.exp(-t) / t))
    return float(special.exp1(x)) - float(special.exp1(y))


def _q(f, lo, hi, epsrel=1.0e-13):
    val, _err = integrate.quad(f, lo, hi, epsabs=0.0, epsrel=epsrel, limit=200)
    return val


class K0:
    """CFG120's closed-form kernel with its length frozen: k = 1/[4 pi s r0 sqrt(s^2 + r0^2)]."""

    def __init__(self, r0):
        self.r0 = float(r0)
        self.key = ("K0", round(self.r0, 12))

    def k(self, s):
        s = np.asarray(s, float)
        return 1.0 / (FOUR_PI * s * self.r0 * np.sqrt(s * s + self.r0 * self.r0))

    def qdiff(self, r, rp):
        r0 = self.r0
        a = (r + rp) / r0
        b = abs(r - rp) / r0
        d = 2.0 * min(r, rp) / r0
        sa = math.sqrt(1.0 + a * a)
        sb = math.sqrt(1.0 + b * b)
        return math.log1p(d * (1.0 + (a + b) / (sa + sb)) / (b + sb)) / (FOUR_PI * r0)

    def m_closed(self, r):
        q = (np.asarray(r, float) / self.r0) ** 2
        return q / (np.sqrt(1.0 + q) + 1.0)

    def m_quad(self, r):
        r0 = self.r0
        return _q(lambda s: s / (r0 * math.sqrt(s * s + r0 * r0)), 0.0, float(r))


class RM:
    """Rahvar-Mashhoon form (CFG120 criteria, section 2): k = (1 + mu s) exp(-mu s)/(4 pi s^2)."""

    def __init__(self, mu):
        self.mu = float(mu)
        self.key = ("RM", self.mu)

    def k(self, s):
        s = np.asarray(s, float)
        return (1.0 + self.mu * s) * np.exp(-self.mu * s) / (FOUR_PI * s * s)

    def qdiff(self, r, rp):
        mu = self.mu
        bp = abs(r - rp)
        e = eint_diff(mu * bp, mu * (r + rp))
        x = math.exp(-mu * bp) * (-math.expm1(-mu * 2.0 * min(r, rp)))
        return (e + x) / FOUR_PI

    def m_closed(self, r):
        x = self.mu * np.asarray(r, float)
        return (-2.0 * np.expm1(-x) - x * np.exp(-x)) / self.mu

    def m_quad(self, r):
        mu = self.mu
        return _q(lambda s: (1.0 + mu * s) * math.exp(-mu * s), 0.0, float(r))


class PL:
    """Power law (mu0 -> 0): k = 1/(4 pi s^2)."""

    key = ("PL",)

    def k(self, s):
        s = np.asarray(s, float)
        return 1.0 / (FOUR_PI * s * s)

    def qdiff(self, r, rp):
        return math.log1p(2.0 * min(r, rp) / abs(r - rp)) / FOUR_PI

    def m_closed(self, r):
        return np.asarray(r, float) * 1.0

    def m_quad(self, r):
        return _q(lambda s: 1.0, 0.0, float(r))


class GaussK:
    """Control kernel: unit-integral Gaussian of dispersion sk."""

    def __init__(self, sk):
        self.sk = float(sk)
        self.norm = (2.0 * math.pi * sk * sk) ** -1.5
        self.key = ("G", self.sk)

    def qdiff(self, r, rp):
        sk2 = self.sk * self.sk
        bp = r - rp
        return self.norm * sk2 * math.exp(-bp * bp / (2.0 * sk2)) * (-math.expm1(-2.0 * r * rp / sk2))


_KC = {}


def get_kernel(kind, par=None):
    key = (kind, None if par is None else round(float(par), 12))
    if key not in _KC:
        _KC[key] = {"K0": lambda: K0(par), "RM": lambda: RM(par), "PL": lambda: PL()}[kind]()
    return _KC[key]


# ----------------------------------------------------------------------------- baryon profiles
def P3(y):
    """M_b(<r)/M of the exponential sphere: 1 - e^-y (1 + y + y^2/2), stable series for small y."""
    y = np.atleast_1d(np.asarray(y, float))
    res = np.empty_like(y)
    sm = y < 0.5
    if np.any(sm):
        ys = y[sm]
        term = ys ** 3 / 6.0
        tot = term.copy()
        for kk in range(4, 40):
            term = term * ys / kk
            tot = tot + term
        res[sm] = np.exp(-ys) * tot
    lg = ~sm
    if np.any(lg):
        yl = y[lg]
        res[lg] = 1.0 - np.exp(-yl) * (1.0 + yl + 0.5 * yl * yl)
    return res


class ExpSphere:
    """CFG44's exponential sphere: rho_b = M exp(-r/h)/(8 pi h^3)."""

    def __init__(self, M, h):
        self.M, self.h = float(M), float(h)
        self.rho0 = self.M / (8.0 * math.pi * self.h ** 3)
        self.rcut = 100.0 * self.h
        self.brk = [0.5 * self.h, self.h, 3.0 * self.h, 10.0 * self.h, 30.0 * self.h]
        self.scale = self.h

    def rho(self, r):
        return self.rho0 * math.exp(-r / self.h)

    def Mb(self, r):
        return self.M * P3(np.asarray(r, float) / self.h)


class GaussSphere:
    """Control profile: a 3-D Gaussian of dispersion s and mass M."""

    def __init__(self, M, s):
        self.M, self.s = float(M), float(s)
        self.rho0 = self.M * (2.0 * math.pi * s * s) ** -1.5
        self.rcut = 12.0 * self.s
        self.brk = [self.s, 3.0 * self.s, 6.0 * self.s]
        self.scale = self.s

    def rho(self, r):
        return self.rho0 * math.exp(-r * r / (2.0 * self.s * self.s))


# ----------------------------------------------------------------------------- my convolution
def conv_rho(kern, prof, r, N=1.0):
    """rho_D(r) = N (2 pi/r) int_0^rcut r' rho_b(r') [Q(r + r') - Q(|r - r'|)] dr', split at r' = r."""
    def f(rp):
        return rp * prof.rho(rp) * kern.qdiff(r, rp)

    segs = [(0.0, r), (r, prof.rcut)] if r < prof.rcut else [(0.0, prof.rcut)]
    total = 0.0
    for lo, hi in segs:
        if hi <= lo:
            continue
        pts = [p for p in prof.brk if lo < p < hi]
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            val, _err = integrate.quad(f, lo, hi, points=pts if pts else None, epsabs=0.0,
                                       epsrel=QUAD_EPSREL, limit=500)
        WARN["n"] += sum(1 for w in wl if issubclass(w.category, integrate.IntegrationWarning))
        total += val
    return N * 2.0 * math.pi / r * total


def cum_simpson(f, du):
    """Cumulative integral of f over a uniform grid: Simpson at even nodes, one quadratic panel at odd nodes."""
    n = len(f)
    I = np.zeros(n)
    ev = np.arange(2, n, 2)
    I[ev] = np.cumsum(du / 3.0 * (f[ev - 2] + 4.0 * f[ev - 1] + f[ev]))
    for i in range(1, n, 2):
        if i + 1 < n:
            I[i] = I[i - 1] + du / 12.0 * (5.0 * f[i - 1] + 8.0 * f[i] - f[i + 1])
        else:
            I[i] = I[i - 1] + du / 12.0 * (-f[i - 2] + 8.0 * f[i - 1] + 5.0 * f[i])
    return I


def log_grid(lo, hi, n=NGRID):
    return np.logspace(math.log10(lo), math.log10(hi), n)


class ConvResult:
    """rho_D on a log grid, M_D by cumulative Simpson in ln r, cubic splines in (ln r, ln .)."""

    def __init__(self, kern, prof, rgrid, N=1.0, diag_radii=None):
        t = time.time()
        w0 = WARN["n"]
        rho = np.array([conv_rho(kern, prof, float(r), N) for r in rgrid])
        u = np.log(rgrid)
        du = (u[-1] - u[0]) / (len(u) - 1)
        MD = cum_simpson(FOUR_PI * rho * rgrid ** 3, du) + FOUR_PI / 3.0 * rho[0] * rgrid[0] ** 3
        self.rgrid, self.rho, self.MD = rgrid, rho, MD
        self.s_rho = interpolate.CubicSpline(u, np.log(rho))
        self.s_MD = interpolate.CubicSpline(u, np.log(MD))
        self.spline_diag = None
        if diag_radii is not None:
            direct = np.array([conv_rho(kern, prof, float(r), N) for r in diag_radii])
            self.spline_diag = float(np.max(np.abs(self.rho_at(diag_radii) / direct - 1.0)))
        self.seconds = time.time() - t
        self.warnings = WARN["n"] - w0

    def rho_at(self, r):
        return np.exp(self.s_rho(np.log(np.asarray(r, float))))

    def MD_at(self, r):
        return np.exp(self.s_MD(np.log(np.asarray(r, float))))


# ----------------------------------------------------------------------------- my target (CFG44)
def target_solution(Mb_fun, a0, r_start, Mc_start, r_end, M):
    """dM_c/dln r = (a0/G) r^2 M_b/(M_b + M_c); returns the dense solution in u = ln r."""
    kk = a0 / G

    def rhs(u, y):
        r = math.exp(u)
        mb = float(Mb_fun(r))
        return [kk * r * r * mb / (mb + y[0])]

    sol = integrate.solve_ivp(rhs, (math.log(r_start), math.log(r_end) + 0.01), [Mc_start],
                              method="DOP853", rtol=1.0e-12, atol=1.0e-30 * M, dense_output=True)
    if not sol.success:
        raise RuntimeError("target ODE failed: " + sol.message)
    return sol.sol


# ----------------------------------------------------------------------------- the fitter
def lnR(a, b, lnc):
    """R = a c + b c^2 at every point, in logs: ln R = ln c + ln(a + b c)."""
    with np.errstate(divide="ignore"):
        la, lb = np.log(a), np.log(b)
    return lnc + np.logaddexp(la, lb + lnc)


def _bisect(fun, lo=-500.0, hi=500.0, tol=1.0e-12):
    flo, fhi = fun(lo), fun(hi)
    if not (flo < 0.0 < fhi):
        raise RuntimeError("bisection bracket failed")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if fun(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def minimax(a, b):
    """The c minimising max |ln R|: the unique root of max ln R + min ln R = 0."""
    lnc = _bisect(lambda z: float(np.max(lnR(a, b, z)) + np.min(lnR(a, b, z))))
    v = lnR(a, b, lnc)
    return math.exp(lnc), float(np.max(v)), float(np.min(v))


def band(a, b):
    """Exact G1 band test: c_lo lifts min R to 0.9, c_hi caps max R at 1.1; passable iff c_lo <= c_hi."""
    lo = _bisect(lambda z: float(np.min(lnR(a, b, z))) - math.log(0.9))
    hi = _bisect(lambda z: float(np.max(lnR(a, b, z))) - math.log(1.1))
    return math.exp(lo), math.exp(hi), lo <= hi


# ----------------------------------------------------------------------------- bookkeeping
CHECKS = []
RES = {}


def check(name, ok, detail):
    CHECKS.append({"name": name, "pass": bool(ok), "detail": detail})
    out(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


# ============================================================================= main flow, part 1
import scipy as _scipy  # noqa: E402  (version string only)


def header():
    sha = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    RES["spec_sha256"] = sha
    out(f"spec sha256 {sha}  (campaign_fresh_gravity/CFG151_FROZEN_CRITERIA.md)")
    out(f"CFG151 -- referee of CFG120's door-1 headline.  Mode: {'MAIN' if not MODE else 'MUTATE=' + MODE}")
    out(f"python {sys.version.split()[0]}, numpy {np.__version__}, scipy {_scipy.__version__}; one process")
    out(f"G = {G:.8e} kpc (km/s)^2/Msun (G Msun = 1.3271244e20 m^3/s^2, 1 kpc = 3.0856775814913673e19 m)")
    RES["constants"] = {"G_kpc_kms2_Msun": G, "a0_kms2_per_kpc": A0, "a0_SI": A0_SI}
    for fk in FOOTINGS:
        a0 = A0[fk]
        lo, hi = 0.1 * r_M(1e12, a0), 30.0 * r_M(1e9, a0)
        out(f"  {fk:9s}: a0 = {A0_SI[fk]:.4e} m/s^2 = {a0:.4f} (km/s)^2/kpc;  r_M(1e9) = {r_M(1e9, a0):.6f},"
            f" r_M(10^10.5) = {r_M(M0, a0):.6f}, r_M(1e12) = {r_M(1e12, a0):.6f} kpc;  overlap [{lo:.4f}, {hi:.4f}] kpc")
    out("Grids: 13 point masses 1e9-1e12 (0.25 dex); x: 200 log points in [0.1, 30]; S(r) at 60 overlap radii;"
        f" sphere grids {NGRID} log points from 1e-4 h to 3000 kpc; quad epsrel {QUAD_EPSREL:g}")


def controls():
    out()
    out("CONTROLS")
    res = {}
    # ---- C1a: Gaussian kernel on a Gaussian sphere, closed form a Gaussian of variance sb^2 + sk^2
    sb, sk, Mg = 2.0, 3.0, 1.0e10
    st = math.hypot(sb, sk)
    cr = ConvResult(GaussK(sk), GaussSphere(Mg, sb), log_grid(1e-4 * sb, 12.0 * st))
    r = np.logspace(math.log10(0.01 * st), math.log10(5.0 * st), 100)
    z = r / (math.sqrt(2.0) * st)
    rho_ex = Mg * (2.0 * math.pi * st * st) ** -1.5 * np.exp(-z * z)
    MD_ex = Mg * (special.erf(z) - 2.0 / math.sqrt(math.pi) * z * np.exp(-z * z))
    d1 = float(np.max(np.abs(cr.rho_at(r) / rho_ex - 1.0)))
    d2 = float(np.max(np.abs(cr.MD_at(r) / MD_ex - 1.0)))
    res["C1a"] = {"rho_maxdev": d1, "MD_maxdev": d2, "quad_warnings": cr.warnings}
    check("C1a Gaussian kernel on a Gaussian sphere (rho_D, M_D vs closed form, line 1e-6)", max(d1, d2) <= 1e-6,
          f"max rel dev rho_D {d1:.2e}, M_D {d2:.2e} over r in [0.01, 5] sigma_tot; {cr.warnings} quad warnings")
    # ---- C1b: power law on a Gaussian sphere, closed form with Dawson's function (direct quadrature)
    s, Mg, Nk = 2.0, 1.0e10, 1.0
    prof = GaussSphere(Mg, s)
    r = np.logspace(math.log10(0.01 * s), math.log10(30.0 * s), 100)
    w0 = WARN["n"]
    num = np.array([conv_rho(PL(), prof, float(x), Nk) for x in r])
    ex = Nk * Mg * math.sqrt(2.0) * special.dawsn(r / (math.sqrt(2.0) * s)) / (FOUR_PI * s * r)
    d = float(np.max(np.abs(num / ex - 1.0)))
    res["C1b"] = {"rho_maxdev": d, "quad_warnings": WARN["n"] - w0}
    check("C1b power law on a Gaussian sphere (rho_D vs the Dawson closed form, line 1e-6)", d <= 1e-6,
          f"max rel dev {d:.2e} over r in [0.01, 30] sigma; {WARN['n'] - w0} quad warnings")
    # ---- C1c: K0 on a compact exponential sphere reproduces the point mass
    r0 = r_M(M0, A0["canonical"])
    kern = K0(r0)
    Mc_, hc = 1.0e10, 1.0e-5 * r0
    cr = ConvResult(kern, ExpSphere(Mc_, hc), log_grid(1e-4 * hc, 3000.0))
    r = np.logspace(math.log10(0.1 * r0), math.log10(30.0 * r0), 100)
    d1 = float(np.max(np.abs(cr.rho_at(r) / (Mc_ * kern.k(r)) - 1.0)))
    d2 = float(np.max(np.abs(cr.MD_at(r) / (Mc_ * kern.m_closed(r)) - 1.0)))
    res["C1c"] = {"rho_maxdev": d1, "MD_maxdev": d2, "h_over_r0": 1e-5, "quad_warnings": cr.warnings}
    check("C1c K0 on a compact sphere (h = 1e-5 r0) = point mass (line 1e-6; ESTIMATE finite size < 2e-8)",
          max(d1, d2) <= 1e-6, f"max rel dev rho_D {d1:.2e}, M_D {d2:.2e} at r in [0.1, 30] r0")
    # ---- C1d: point-mass kernel masses m(r) by quadrature vs closed forms
    worst = 0.0
    for fk in FOOTINGS:
        a0 = A0[fk]
        kerns = [K0(r_M(10.0 ** e, a0)) for e in (10.5, 9.0, 12.0)] + [RM(0.06), RM(0.10), PL()]
        rr = np.concatenate([XGRID * r_M(M, a0) for M in MASSES])
        for kk in kerns:
            mq = np.array([kk.m_quad(float(x)) for x in rr])
            worst = max(worst, float(np.max(np.abs(mq / kk.m_closed(rr) - 1.0))))
        if MODE == "b":
            for M in MASSES:
                kk = K0(r_M(M, a0))
                rr1 = XGRID * r_M(M, a0)
                mq = np.array([kk.m_quad(float(x)) for x in rr1])
                worst = max(worst, float(np.max(np.abs(mq / kk.m_closed(rr1) - 1.0))))
    res["C1d"] = {"maxdev": worst}
    check("C1d point-mass kernel mass m(r): quadrature vs closed forms (line 1e-10)", worst <= 1e-10,
          f"max rel dev {worst:.2e} (K0 at three M0, RM 0.06/0.10, PL; x-grids of all 13 masses; both footings)")
    # ---- C2a: my target ODE for a point mass vs the closed forms
    wM = wr = 0.0
    for fk in FOOTINGS:
        a0 = A0[fk]
        for M in MASSES:
            rm = r_M(M, a0)
            x0 = 1e-6
            sol = target_solution(lambda rr_: M, a0, x0 * rm, M * 0.5 * x0 * x0, 30.0 * rm, M)
            r = XGRID * rm
            Mc = sol(np.log(r))[0]
            Mc_ex = M * XGRID ** 2 / (np.sqrt(1.0 + XGRID ** 2) + 1.0)
            rho_c = (a0 / G) * r * M / (M + Mc) / (FOUR_PI * r * r)
            rho_ex = a0 / (FOUR_PI * G * r * np.sqrt(1.0 + XGRID ** 2))
            wM = max(wM, float(np.max(np.abs(Mc / Mc_ex - 1.0))))
            wr = max(wr, float(np.max(np.abs(rho_c / rho_ex - 1.0))))
    res["C2a"] = {"Mc_maxdev": wM, "rho_c_maxdev": wr}
    check("C2a target ODE, point mass: M_c and rho_c vs closed forms (line 1e-8)", max(wM, wr) <= 1e-8,
          f"max rel dev M_c {wM:.2e}, rho_c {wr:.2e} (13 masses, both footings, x in [0.1, 30])")
    # ---- C2b: the target's own identity on the spheres, rho_c by a 5-point finite difference
    pairs = sorted({(M, h) for hs in H_ASSIGN.values() for M, h in zip(SPHERE_MASSES, hs)})
    wC = wS = 0.0
    dl = 1e-3
    for fk in FOOTINGS:
        a0 = A0[fk]
        for M, h in pairs:
            rm = r_M(M, a0)
            mbf = (lambda M_, h_: (lambda rr_: M_ * P3(rr_ / h_)[0]))(M, h)

            def lead(rs, M=M, h=h):
                return math.sqrt(a0 * M * rs ** 5 / (15.0 * G * h ** 3))

            sol = target_solution(mbf, a0, 1e-6 * h, lead(1e-6 * h), 30.0 * rm, M)
            sol2 = target_solution(mbf, a0, 1e-7 * h, lead(1e-7 * h), 30.0 * rm, M)
            r = XGRID * rm
            u = np.log(r)
            Mc = sol(u)[0]
            dMdu = (sol(u - 2 * dl)[0] - 8 * sol(u - dl)[0] + 8 * sol(u + dl)[0] - sol(u + 2 * dl)[0]) / (12 * dl)
            rho_c = dMdu / (FOUR_PI * r ** 3)
            mb = M * P3(r / h)
            C = G * r * rho_c * (mb + Mc)
            wC = max(wC, float(np.max(np.abs(C / (a0 / FOUR_PI * mb) - 1.0))))
            wS = max(wS, float(np.max(np.abs(sol2(u)[0] / Mc - 1.0))))
    res["C2b"] = {"C_identity_maxdev": wC, "start_radius_maxdev": wS, "pairs": pairs}
    check("C2b target identity on the spheres: rho_c r^3 g_tot = (a0/4 pi) M_b(<r) (line 1e-7; start test 1e-8)",
          wC <= 1e-7 and wS <= 1e-8,
          f"max rel dev of C {wC:.2e}; start 1e-7 h vs 1e-6 h changes M_c by {wS:.2e} (7 (M, h) pairs, both footings)")
    # ---- C2c: the sphere's M_b closed form vs quadrature of rho_b; r_M(1e9) canonical
    wm = 0.0
    for fk in FOOTINGS:
        for M, h in pairs:
            prof = ExpSphere(M, h)
            r = XGRID * r_M(M, A0[fk])
            q = np.array([_q(lambda s_: FOUR_PI * s_ * s_ * prof.rho(s_), 0.0, float(x)) for x in r])
            wm = max(wm, float(np.max(np.abs(q / prof.Mb(r) - 1.0))))
    rm9 = r_M(1e9, A0["canonical"])
    res["C2c"] = {"Mb_maxdev": wm, "r_M_1e9_canonical": rm9}
    check("C2c sphere M_b closed form vs quadrature (line 1e-10); r_M(1e9) canonical = 1.2203 +- 1e-4 kpc",
          wm <= 1e-10 and abs(rm9 - 1.2203) <= 1e-4, f"max rel dev {wm:.2e}; r_M(1e9) = {rm9:.6f} kpc")
    # ---- C3: positive control -- K0 at N = 1 on a point mass of mass M0 gives R = 1; the fitter returns 1
    wR, wc = 0.0, 0.0
    for fk in FOOTINGS:
        a0 = A0[fk]
        kk = K0(r_M(M0, a0))
        r = XGRID * r_M(M0, a0)
        base = FOUR_PI * G * M0 / a0 * r * kk.k(r)
        m = np.array([kk.m_quad(float(x)) for x in r])
        a, b = base, base * m
        wR = max(wR, float(np.max(np.abs(a + b - 1.0))))
        c, _mx, _mn = minimax(a, b)
        wc = max(wc, abs(c - 1.0))
    res["C3"] = {"R_maxdev": wR, "fit_c_dev": wc}
    check("C3 positive control: K0 (N = 1) on a point mass M0 gives R = 1 (line 1e-8); fitter returns N = 1 +- 1e-6",
          wR <= 1e-8 and wc <= 1e-6, f"max |R - 1| = {wR:.2e}; |N_fit - 1| = {wc:.2e} (both footings)")
    RES["controls"] = res


# ============================================================================= main flow, part 2
N0 = {}        # MUTATE=a: the point-mass best fit at M0, per (slot, footing)
MCACHE = {}
UNIT = {}


def pm_kernel(slot, M, fk, raw=False):
    """(kernel, base normalisation) for a slot, mass and footing in this mode; raw = as in the main run."""
    a0 = A0[fk]
    mode = "" if raw else MODE
    if slot.startswith("K0"):
        r0 = r_M(M, a0) if mode == "b" else r_M(10.0 ** float(slot.split("@")[1]), a0)
        kern, nb = get_kernel("K0", r0), 1.0
    else:
        kern = get_kernel("RM", float(slot[2:])) if slot.startswith("RM") else get_kernel("PL")
        nb = 1.0 / r_M(M, a0) if mode == "b" else 1.0
    if mode == "a":
        nb = N0[(slot, fk)] * M0 / M
    return kern, nb


def m_of(kern, r):
    res = np.empty(len(r))
    for i, x in enumerate(r):
        key = (kern.key, float(x))
        if key not in MCACHE:
            MCACHE[key] = kern.m_quad(float(x))
        res[i] = MCACHE[key]
    return res


def pm_ab(slot, M, fk, r, raw=False):
    """Point mass: R = a c + b c^2, with N = c * (base normalisation)."""
    kern, nb = pm_kernel(slot, M, fk, raw)
    base = FOUR_PI * G * M / A0[fk] * r * kern.k(r)
    return base * nb, base * m_of(kern, r) * nb * nb


def unit_conv(kern, h):
    key = (kern.key, h)
    if key not in UNIT:
        diag = np.logspace(math.log10(0.05), math.log10(1500.0), 10)
        UNIT[key] = ConvResult(kern, ExpSphere(1.0, h), log_grid(1e-4 * h, 3000.0), 1.0, diag)
    return UNIT[key]


def sp_ab(slot, M, h, fk, r, raw=False):
    """Exponential sphere: R = a c + b c^2 from the unit-mass, unit-N convolution."""
    kern, nb = pm_kernel(slot, M, fk, raw)
    cr = unit_conv(kern, h)
    base = FOUR_PI * G * M / A0[fk] * r * cr.rho_at(r)
    return base * nb, base * cr.MD_at(r) / P3(r / h) * nb * nb


def in_range(r, M, a0):
    rm = r_M(M, a0)
    return 0.1 * rm * (1.0 - 1e-12) <= r <= 30.0 * rm * (1.0 + 1e-12)


def point_mass_section(fk):
    a0 = A0[fk]
    lo_end, hi_end = 0.1 * r_M(1e12, a0), 30.0 * r_M(1e9, a0)
    rov, r20 = log_grid(lo_end, hi_end, 60), log_grid(lo_end, hi_end, 20)
    if MODE == "a":
        for slot in PM_SLOTS:
            r = XGRID * r_M(M0, a0)
            N0[(slot, fk)] = minimax(*pm_ab(slot, M0, fk, r, raw=True))[0]
    out()
    out(f"POINT MASS ({fk}; overlap [{lo_end:.4f}, {hi_end:.4f}] kpc; c = the fitted multiplier of the"
        f" {'main-run N' if not MODE else 'mode-' + MODE + ' base normalisation'})")
    out(f"  {'slot':8s} {'c*(1e9)':>10s} {'c*(10^10.5)':>11s} {'c*(1e12)':>10s} {'ratio':>8s} {'res 1e9':>8s}"
        f" {'res 1e12':>8s} | {'c_common':>10s} {'res_com':>8s} {'S(r) min..max':>19s} {'F min..max':>15s}"
        f" {'expo C_model':>13s}")
    res = {"overlap": [lo_end, hi_end], "slots": {}}
    for slot in PM_SLOTS:
        per, A_all, B_all, MM = [], [], [], []
        for M in MASSES:
            r = XGRID * r_M(M, a0)
            a, b = pm_ab(slot, M, fk, r)
            c, mx, _mn = minimax(a, b)
            per.append({"M": M, "c_best": c, "N_best": c * pm_kernel(slot, M, fk)[1], "residual": mx})
            A_all.append(a)
            B_all.append(b)
            MM.append(np.full(len(r), M))
        A, B, MM = np.concatenate(A_all), np.concatenate(B_all), np.concatenate(MM)
        cc, rc, _ = minimax(A, B)
        S, nin = [], []
        for r in rov:
            Rv = []
            for M in MASSES:
                if in_range(r, M, a0):
                    a, b = pm_ab(slot, M, fk, np.array([r]))
                    Rv.append(float(a[0] * cc + b[0] * cc * cc))
            S.append(max(Rv) / min(Rv))
            nin.append(len(Rv))
        S = np.array(S)
        a9, b9 = pm_ab(slot, 1e9, fk, r20)
        a12, b12 = pm_ab(slot, 1e12, fk, r20)
        C9 = a0 / FOUR_PI * 1e9 * (a9 * cc + b9 * cc * cc)
        C12 = a0 / FOUR_PI * 1e12 * (a12 * cc + b12 * cc * cc)
        expo = np.log(C12 / C9) / math.log(1000.0)
        expo_t = math.log((a0 / FOUR_PI * 1e12) / (a0 / FOUR_PI * 1e9)) / math.log(1000.0)
        r5 = log_grid(lo_end, hi_end, 5)
        a1, b1 = pm_ab(slot, 1e10, fk, r5)
        a2, b2 = pm_ab(slot, 2e10, fk, r5)
        ratio2 = (a2 * cc + b2 * cc * cc) / (a1 * cc + b1 * cc * cc)
        d = {"per_mass": per, "c_common": cc, "residual_common": rc, "S": S, "F": np.sqrt(S),
             "n_masses_in_range": nin, "expo_Cmodel": expo, "expo_Ctarget": expo_t,
             "R2M_over_RM": ratio2, "lin_dev": (S - 1.0) / (S + 1.0),
             "Nstar_ratio_1e9_1e12": per[0]["N_best"] / per[-1]["N_best"]}
        if slot == "K0@10.5":
            d["R_over_M_over_M0_maxdev_at_c1"] = float(np.max(np.abs((A + B) / (MM / M0) - 1.0)))
            d["R_range_at_c1"] = [float(np.min(A + B)), float(np.max(A + B))]
        res["slots"][slot] = d
        out(f"  {slot:8s} {per[0]['c_best']:10.4g} {per[6]['c_best']:11.4g} {per[-1]['c_best']:10.4g}"
            f" {per[0]['c_best'] / per[-1]['c_best']:8.4g} {per[0]['residual']:8.4f} {per[-1]['residual']:8.4f} |"
            f" {cc:10.4g} {rc:8.4f} {S.min():9.4f}..{S.max():9.4f} {np.sqrt(S).min():7.4f}..{np.sqrt(S).max():7.4f}"
            f" {expo.min():6.4f}..{expo.max():6.4f}")
    # R4: the four recalled RM sets as given (A = 1, N = 1/lambda0), raw kernels
    rec = {}
    for lam, mu in RECALLED:
        slot = "RM0.06" if mu == 0.06 else "RM0.10"
        rows = []
        for M in MASSES:
            r = XGRID * r_M(M, a0)
            a, b = pm_ab(slot, M, fk, r, raw=True)
            R = a / lam + b / lam ** 2
            rows.append({"M": M, "max_abs_lnR": float(np.max(np.abs(np.log(R)))),
                         "in_band": bool(np.all((R >= 0.9) & (R <= 1.1)))})
        rec[f"lambda0={lam:g},mu0={mu:g}"] = rows
    res["recalled_RM"] = rec
    out("  recalled RM sets as given (N = 1/lambda0): max |ln R| over x, per mass, at 1e9 / 10^10.5 / 1e12;"
        " masses in the [0.9, 1.1] band")
    for k, rows in rec.items():
        out(f"    {k:22s} {rows[0]['max_abs_lnR']:8.3f} {rows[6]['max_abs_lnR']:8.3f} {rows[-1]['max_abs_lnR']:8.3f};"
            f" in band at {sum(x['in_band'] for x in rows)} of 13")
    return res


def sphere_section(fk):
    a0 = A0[fk]
    lo_end, hi_end = 0.1 * r_M(1e12, a0), 30.0 * r_M(1e9, a0)
    rov = log_grid(lo_end, hi_end, 60)
    res = {}
    for assign, hs in H_ASSIGN.items():
        out()
        out(f"SPHERES ({fk}; {assign}; masses 1e9, 1e10, 1e11, 1e12)")
        out(f"  {'slot':8s} {'c*(1e9)':>10s} {'c*(1e10)':>10s} {'c*(1e11)':>10s} {'c*(1e12)':>10s} {'ratio':>8s}"
            f" {'res per mass':>27s} | {'c_common':>10s} {'res_com':>8s} {'c_lo':>10s} {'c_hi':>10s} {'G1?':>4s}"
            f" {'S_exp min..max':>19s}")
        res[assign] = {}
        for slot in SP_SLOTS:
            per, A_all, B_all = [], [], []
            for M, h in zip(SPHERE_MASSES, hs):
                r = XGRID * r_M(M, a0)
                a, b = sp_ab(slot, M, h, fk, r)
                c, mx, _mn = minimax(a, b)
                per.append({"M": M, "h": h, "c_best": c, "N_best": c * pm_kernel(slot, M, fk)[1], "residual": mx})
                A_all.append(a)
                B_all.append(b)
            A, B = np.concatenate(A_all), np.concatenate(B_all)
            cc, rc, _ = minimax(A, B)
            clo, chi, passable = band(A, B)
            S = []
            for r in rov:
                Rv = [float(np.sum(np.array(sp_ab(slot, M, h, fk, np.array([r]))) * np.array([[cc], [cc * cc]])))
                      for M, h in zip(SPHERE_MASSES, hs) if in_range(r, M, a0)]
                S.append(max(Rv) / min(Rv))
            S = np.array(S)
            res[assign][slot] = {"per_mass": per, "c_common": cc, "residual_common": rc, "c_lo": clo,
                                 "c_hi": chi, "G1_passable": passable, "S_exp": S,
                                 "Nstar_ratio_1e9_1e12": per[0]["N_best"] / per[-1]["N_best"]}
            out(f"  {slot:8s} " + " ".join(f"{p['c_best']:10.4g}" for p in per)
                + f" {per[0]['c_best'] / per[-1]['c_best']:8.4g} "
                + " ".join(f"{p['residual']:6.3f}" for p in per)
                + f" | {cc:10.4g} {rc:8.4f} {clo:10.4g} {chi:10.4g} {'yes' if passable else 'no':>4s}"
                + f" {S.min():9.4g}..{S.max():9.4g}")
        rec = {}
        for lam, mu in RECALLED:
            slot = "RM0.06" if mu == 0.06 else "RM0.10"
            rows = []
            for M, h in zip(SPHERE_MASSES, hs):
                r = XGRID * r_M(M, a0)
                a, b = sp_ab(slot, M, h, fk, r, raw=True)
                R = a / lam + b / lam ** 2
                rows.append({"M": M, "max_abs_lnR": float(np.max(np.abs(np.log(R)))),
                             "in_band": bool(np.all((R >= 0.9) & (R <= 1.1)))})
            rec[f"lambda0={lam:g},mu0={mu:g}"] = rows
        res[assign]["recalled_RM"] = rec
        out("  recalled RM sets as given: max |ln R| per mass (1e9 .. 1e12); masses in band")
        for k, rows in rec.items():
            out(f"    {k:22s} " + " ".join(f"{x['max_abs_lnR']:8.3f}" for x in rows)
                + f"; in band at {sum(x['in_band'] for x in rows)} of 4")
    # H1a on spheres: h = 3 kpc, two separate convolution runs with M inside the quadrature
    r20s = log_grid(0.3, 300.0, 20)
    h1a = {}
    for slot in SP_SLOTS:
        cc = res["h(M)=2,3,4,5"][slot]["c_common"]
        C, Ct = {}, {}
        for M in (1e9, 1e12):
            kern, nb = pm_kernel(slot, M, fk)
            cr = ConvResult(kern, ExpSphere(M, 3.0), log_grid(1e-4 * 3.0, 3000.0), cc * nb)
            C[M] = G * r20s * cr.rho_at(r20s) * (M * P3(r20s / 3.0) + cr.MD_at(r20s))
            Ct[M] = a0 / FOUR_PI * M * P3(r20s / 3.0)
        h1a[slot] = {"expo_Cmodel": np.log(C[1e12] / C[1e9]) / math.log(1000.0),
                     "expo_Ctarget": np.log(Ct[1e12] / Ct[1e9]) / math.log(1000.0), "N_used_factor": cc}
    res["h1a_h3"] = h1a
    out(f"  H1a spheres (h = 3 kpc, separate runs at 1e9 and 1e12, 20 radii in [0.3, 300] kpc): exponent of C_model"
        f" per slot: " + "; ".join(f"{s} {d['expo_Cmodel'].min():.6f}..{d['expo_Cmodel'].max():.6f}"
                                    for s, d in h1a.items()))
    return res


# ============================================================================= main flow, part 3
def evaluate(PM, SP):
    out()
    out("HEADLINE H1 (each part on both footings; H1 passes only if all four parts pass)")
    parts = {"H1a": [], "H1b": [], "H1c": [], "H1d": []}
    for fk in FOOTINGS:
        pm, sp = PM[fk], SP[fk]
        e_pm = np.concatenate([d["expo_Cmodel"] for d in pm["slots"].values()])
        et_pm = np.array([d["expo_Ctarget"] for d in pm["slots"].values()])
        e_sp = np.concatenate([d["expo_Cmodel"] for d in sp["h1a_h3"].values()])
        et_sp = np.concatenate([d["expo_Ctarget"] for d in sp["h1a_h3"].values()])
        ok = bool(np.all(np.abs(e_pm - 2.0) <= 0.02) and np.all(np.abs(et_pm - 1.0) <= 0.02)
                  and np.all(np.abs(e_sp - 2.0) <= 0.02) and np.all(np.abs(et_sp - 1.0) <= 0.02))
        parts["H1a"].append(check(
            f"H1a scaling ({fk}): d ln C_model/d ln M_b = 2.00 +- 0.02 and C_target 1.00 +- 0.02, 1e9 vs 1e12", ok,
            f"point mass (6 slots x 20 overlap radii) {e_pm.min():.6f}..{e_pm.max():.6f}; spheres at h = 3 kpc"
            f" (4 slots x 20 radii, separate runs) {e_sp.min():.6f}..{e_sp.max():.6f}; C_target"
            f" {min(et_pm.min(), et_sp.min()):.6f}..{max(et_pm.max(), et_sp.max()):.6f}"))
        S_all = np.concatenate([d["S"] for d in pm["slots"].values()])
        F_all = np.sqrt(S_all)
        okS = bool(np.all(np.abs(S_all / 1000.0 - 1.0) <= 0.02) and np.all(np.abs(F_all / CFG120["F"] - 1.0) <= 0.02))
        lo, hi = pm["overlap"]
        if fk == "canonical":
            okE = abs(lo / CFG120["ov_lo"] - 1.0) <= 0.01 and abs(hi / CFG120["ov_hi"] - 1.0) <= 0.01
            ends = (f"ends {lo:.4f} / {hi:.4f} kpc vs CFG120's 3.87 / 36.55 ({100 * (lo / 3.87 - 1):+.2f}%,"
                    f" {100 * (hi / 36.55 - 1):+.2f}%)")
        else:
            okE = True
            ends = f"ends {lo:.4f} / {hi:.4f} kpc (reported; CFG120 did not print them)"
        parts["H1b"].append(check(
            f"H1b spread ({fk}): S(r) = 1000 +- 2% at 60 overlap radii, F within 2% of 31.6228, every slot", okS and okE,
            f"S {S_all.min():.6f}..{S_all.max():.6f}; F {F_all.min():.6f}..{F_all.max():.6f}; {ends}"))
        rcs = {s: d["residual_common"] for s, d in pm["slots"].items()}
        k0 = pm["slots"]["K0@10.5"]
        ok = bool(min(rcs.values()) >= FLOOR - 0.02 and abs(k0["residual_common"] / FLOOR - 1.0) <= 0.02
                  and abs(k0["c_common"] - 1.0) <= 0.02 and k0["R_over_M_over_M0_maxdev_at_c1"] <= 1e-8)
        parts["H1c"].append(check(
            f"H1c no single normalisation, point mass ({fk}): best common N leaves max|ln R| >= 3.434 for every slot;"
            f" K0@10.5 attains 3.4539 at N = 1", ok,
            "residuals " + ", ".join(f"{s} {v:.4f}" for s, v in rcs.items())
            + f"; K0@10.5 N_common = {k0['c_common']:.6f}, max|R/(M/M0) - 1| at N = 1: "
            f"{k0['R_over_M_over_M0_maxdev_at_c1']:.2e}, R at N = 1 spans {k0['R_range_at_c1'][0]:.5f}.."
            f"{k0['R_range_at_c1'][1]:.4f}"))
        npass = sum(bool(sp[a][s]["G1_passable"]) for a in H_ASSIGN for s in SP_SLOTS)
        rcs_sp = [sp[a][s]["residual_common"] for a in H_ASSIGN for s in SP_SLOTS]
        parts["H1d"].append(check(
            f"H1d no single normalisation, spheres ({fk}): no common N puts R in [0.9, 1.1] (4 slots x 2 h assignments)",
            npass == 0, f"G1-passable cases: {npass} of 8; best common max|ln R| {min(rcs_sp):.3f}..{max(rcs_sp):.3f}"))
    part_ok = {k: all(v) for k, v in parts.items()}
    out(f"  H1 overall: {'PASS' if all(part_ok.values()) else 'FAIL'} (" +
        ", ".join(f"{k} {'pass' if v else 'FAIL'}" for k, v in part_ok.items()) + ")")
    RES["H1_parts"] = part_ok
    return part_ok


def reported_rows(PM, SP):
    out()
    out("REPORTED ROWS (no pass line)")
    for fk in FOOTINGS:
        a0 = A0[fk]
        pm = PM[fk]
        breq = {M: a0 / (FOUR_PI * G * M) for M in (1e9, M0, 1e12)}
        out(f"  R1 ({fk}): B_req = a0/(4 pi G M) = {breq[1e9]:.5e}, {breq[M0]:.5e}, {breq[1e12]:.5e} kpc^-2 at 1e9,"
            f" 10^10.5, 1e12 (ratio {breq[1e9] / breq[1e12]:.6f})")
        for s, d in pm["slots"].items():
            out(f"      point {s:8s}: N*(1e9)/N*(1e12) = {d['Nstar_ratio_1e9_1e12']:.5g}; per-mass residual"
                f" {min(p['residual'] for p in d['per_mass']):.4f}..{max(p['residual'] for p in d['per_mass']):.4f}")
        for a in H_ASSIGN:
            for s in SP_SLOTS:
                d = SP[fk][a][s]
                out(f"      sphere [{a}] {s:8s}: N*(1e9)/N*(1e12) = {d['Nstar_ratio_1e9_1e12']:.5g}; S_exp on the overlap"
                    f" {d['S_exp'].min():.4g}..{d['S_exp'].max():.4g}")
        r2 = np.concatenate([d["R2M_over_RM"] for d in pm["slots"].values()])
        ld = np.concatenate([d["lin_dev"] for d in pm["slots"].values()])
        out(f"  R3 ({fk}): single-kernel mass window 1.1/0.9 = {1.1 / 0.9:.4f} (CFG120 1.222); R(2M)/R(M) at fixed r"
            f" {r2.min():.12f}..{r2.max():.12f} (CFG120 2.000000000000); centred residual sqrt 2 - 1 ="
            f" {math.sqrt(2) - 1:.4f}; my reading of 'linear band 0.998': (S-1)/(S+1) = {ld.min():.6f}..{ld.max():.6f}")
        out(f"  R4 ({fk}): PL best common N residual {pm['slots']['PL']['residual_common']:.4f} (factor"
            f" {math.exp(pm['slots']['PL']['residual_common']):.2f}; CFG120 RM 3-parameter fit 3.97, factor 53);"
            f" RM0.06 {pm['slots']['RM0.06']['residual_common']:.3f}, RM0.10 {pm['slots']['RM0.10']['residual_common']:.3f}")


def estimates(PM, SP):
    out()
    out("ESTIMATES written in the spec before running (hand algebra) vs results")

    def row(label, est, got):
        out(f"  {label:58s} ESTIMATE {est:>17s} | result {got}")

    pc = PM["canonical"]
    if not MODE:
        lo, hi = pc["overlap"]
        loa, hia = PM["alt"]["overlap"]
        k0, pl = pc["slots"]["K0@10.5"], pc["slots"]["PL"]
        row("overlap ends, canonical (kpc)", "3.859, 36.61", f"{lo:.4f}, {hi:.4f}")
        row("overlap ends, alt (kpc)", "3.510, 33.30", f"{loa:.4f}, {hia:.4f}")
        row("K0@10.5 point: N* at 1e9, 10^10.5, 1e12", "10.6, 1, 0.102",
            f"{k0['per_mass'][0]['N_best']:.4f}, {k0['per_mass'][6]['N_best']:.6f}, {k0['per_mass'][-1]['N_best']:.5f}")
        row("K0@10.5 point: ratio N*(1e9)/N*(1e12)", "about 104", f"{k0['Nstar_ratio_1e9_1e12']:.3f}")
        row("K0@10.5 point: residual at 1e9, 1e12", "1.09, 1.05",
            f"{k0['per_mass'][0]['residual']:.4f}, {k0['per_mass'][-1]['residual']:.4f}")
        row("PL point: ratio N*(1e9)/N*(1e12)", "31.62 exactly", f"{pl['Nstar_ratio_1e9_1e12']:.6f}")
        row("PL point: per-mass residual", "1.54 at every mass",
            f"{min(p['residual'] for p in pl['per_mass']):.5f}..{max(p['residual'] for p in pl['per_mass']):.5f}")
        row("PL point: best common N residual", "3.974 (f 53.2)",
            f"{pl['residual_common']:.4f} (factor {math.exp(pl['residual_common']):.2f})")
        row("RM point: best common N residual (mu0 = 0.06, 0.10)", "tens",
            f"{pc['slots']['RM0.06']['residual_common']:.3f}, {pc['slots']['RM0.10']['residual_common']:.3f}")
        row("K0@10.5 point: best common N and residual", "1, 3.4539", f"{k0['c_common']:.6f}, {k0['residual_common']:.5f}")
        sx = [SP[f][a][s]["S_exp"] for f in FOOTINGS for a in H_ASSIGN for s in SP_SLOTS]
        row("sphere spread S_exp on the overlap (all slots)", "100 to 1e4",
            f"{min(x.min() for x in sx):.4g}..{max(x.max() for x in sx):.4g}")
        c1c = RES["controls"]["C1c"]
        row("C1c finite-size error", "< 2e-8", f"{max(c1c['rho_maxdev'], c1c['MD_maxdev']):.2e}")
    elif MODE == "a":
        k0 = pc["slots"]["K0@10.5"]
        row("K0@10.5 point: S at the overlap ends (3.86, 36.6 kpc)", "about 5.6, 124",
            f"{k0['S'][0]:.4f}, {k0['S'][-1]:.4f}")
        row("K0@10.5 point: exponent of C_model", "about 0.30-0.75",
            f"{k0['expo_Cmodel'].min():.4f}..{k0['expo_Cmodel'].max():.4f}")
    else:
        k0, pl = pc["slots"]["K0@10.5"], pc["slots"]["PL"]
        row("K0 keyed point: S, exponent of C_model", "1, 1.00",
            f"{k0['S'].min():.8f}..{k0['S'].max():.8f}, {k0['expo_Cmodel'].min():.6f}..{k0['expo_Cmodel'].max():.6f}")
        row("PL keyed point: S on the overlap", "about 2-8", f"{pl['S'].min():.4f}..{pl['S'].max():.4f}")


def bite_summary(part_ok):
    if not MODE:
        return {}
    declared = {"a": ("H1a", "H1b"), "b": ("H1a", "H1b", "H1c")}[MODE]
    out()
    out(f"MUTATE={MODE} BITE (the declared lines must flip, i.e. fail)")
    flipped = {}
    for p in ("H1a", "H1b", "H1c", "H1d"):
        flipped[p] = not part_ok[p]
        out(f"  {p}: {'FLIPPED (fails)' if flipped[p] else 'did not flip (passes)'}"
            f"  [{'declared' if p in declared else 'not required'}]")
    allb = all(flipped[p] for p in declared)
    out(f"  bite on every declared line: {'YES' if allb else 'NO -- the control failed to bite'}")
    return {"declared": declared, "flipped": flipped, "bite_all_declared": allb}


def main():
    header()
    t = time.time()
    controls()
    out(f"  (controls {time.time() - t:.1f} s)")
    PM, SP = {}, {}
    for fk in FOOTINGS:
        t = time.time()
        PM[fk] = point_mass_section(fk)
        out(f"  (point masses, {fk}: {time.time() - t:.1f} s)")
    for fk in FOOTINGS:
        t = time.time()
        SP[fk] = sphere_section(fk)
        out(f"  (spheres, {fk}: {time.time() - t:.1f} s)")
    part_ok = evaluate(PM, SP)
    reported_rows(PM, SP)
    estimates(PM, SP)
    bite = bite_summary(part_ok)
    diag = [cr.spline_diag for cr in UNIT.values() if cr.spline_diag is not None]
    out()
    out(f"DIAGNOSTICS (added in stage 2 before the first run; no pass line): spline vs direct rho_D on {len(diag)}"
        f" unit grids at 10 radii each, max rel diff {max(diag):.2e}; quadrature warnings {WARN['n']};"
        f" {len(UNIT)} unit convolutions")
    nfail = sum(not c["pass"] for c in CHECKS)
    code = 0 if nfail == 0 else 1
    out()
    out(f"VERDICT ({'MAIN' if not MODE else 'MUTATE=' + MODE}): {len(CHECKS) - nfail} of {len(CHECKS)} checks pass;"
        f" exit {code}")
    out(f"elapsed {time.time() - T_START:.1f} s")
    RES.update({"lane": "CFG151", "mode": MODE or "main", "checks": CHECKS, "point_mass": PM, "spheres": SP,
                "bite": bite, "spline_diag_max": max(diag), "quad_warnings": WARN["n"], "exit_code": code,
                "N0_mutate_a": {f"{k[0]}|{k[1]}": v for k, v in N0.items()}})
    (HERE / f"{STEM}.out").write_text("\n".join(LINES) + "\n")
    (HERE / f"{STEM}_results.json").write_text(json.dumps(clean(RES), indent=1))
    return code


if __name__ == "__main__":
    sys.exit(main())
