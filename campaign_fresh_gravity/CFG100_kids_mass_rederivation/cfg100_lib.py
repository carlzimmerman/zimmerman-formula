# CFG100 own implementation (frozen text: cfg100_FROZEN.txt).  Pieces adapted from CFG77's cfg77_lib.py (kernel, projector, turnaround solver,
# NFW/Mandelbaum recipe) -- copied as source, not imported.  Differences: central-mass bookkeeping in the projector (Mtot = M_edges[-1]),
# vectorised NFW, Moster+13 inversion, per-group table builder.
import math, os
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import CubicSpline


def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "real_research", "data", "lensing_rar")):
        return env
    starts = [os.path.dirname(os.path.abspath(__file__)), os.getcwd()]
    for s in starts:
        p = s
        for _ in range(12):
            if os.path.isdir(os.path.join(p, "real_research", "data", "lensing_rar")):
                return p
            p = os.path.dirname(p)
    raise RuntimeError("set ZF_REPO to the repository root (contains real_research/data/lensing_rar)")


REPO = find_repo()
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
G_MPC = 4.30091727e-9            # Mpc (km/s)^2 / Msun
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M             # (km/s)^2/Mpc -> m/s^2
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {k: v / SI_ACC for k, v in A0_SI.items()}
OM, H = 0.3153, 0.6736
H0 = 100 * H
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G_MPC)


# ------------------------------------------------------------------ kernel nu_mono
def _h(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def _dh(y, e=1e-6):
    return (_h(y * (1 + e)) - _h(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(_dh(y)), 1.0, 5.0)
H_P = float(_h(Y_P))
LYG = np.linspace(-14, 14, 280001)
_YG = 10 ** LYG
_DH = np.maximum(_dh(_YG), 0.05 * H_P / (_YG + Y_P))
_HM = float(_h(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), LYG, _HM) / y


# ------------------------------------------------------------------ turnaround
def one_plus_delta_ta(a, Om=OM, H0_=H0):
    OL = 1 - Om
    t_a = 2.0 / (3 * H0_ * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om) * a ** 1.5)
    L = OL * H0_ ** 2
    def tint(w):
        f = lambda p: 2 * math.sin(p) ** 2 / math.sqrt(2 * w - L * math.sin(p) ** 2 * (1 + math.sin(p) ** 2))
        return quad(f, 0, math.pi / 2, epsabs=1e-13, epsrel=1e-12)[0]
    wlo = L * (1 + 1e-5)
    w = brentq(lambda w: tint(w) - t_a, wlo, 1e3 * H0_ ** 2, xtol=1e-16 * H0_ ** 2, rtol=1e-13)
    return 2 * w * a ** 3 / (Om * H0_ ** 2)
_DTA = None
def dta(z):
    global _DTA
    if _DTA is None:
        zs = np.linspace(-0.05, 1.0, 43)
        lna = np.log(1 / (1 + zs))[::-1]
        vals = np.array([math.log(one_plus_delta_ta(1 / (1 + zz))) for zz in zs])[::-1]
        _DTA = CubicSpline(lna, vals)
    return math.exp(float(_DTA(-math.log1p(z))))
def r_ta_law(Mb, a0, z):
    a = 1 / (1 + z)
    rho = OM * RHOC0 / a ** 3 * dta(z)
    f = lambda lr: math.log(Mb * float(nu_mono(G_MPC * Mb / math.exp(2 * lr) / a0))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho)
    return math.exp(brentq(f, math.log(1e-5), math.log(1e3), xtol=1e-12))


# ------------------------------------------------------------------ projector
def dsigma(R, r_edges, M_edges):
    """DeltaSigma [Msun/Mpc^2] at R [Mpc] of a spherical profile with ENCLOSED mass M_edges (Msun) at r_edges (Mpc): a central point mass
    M_edges[0] plus shells of constant density between edges; total mass M_edges[-1].  Excludes any extra baryon point mass."""
    R = np.atleast_1d(np.asarray(R, float))[:, None]
    r1 = r_edges[None, :-1]; r2 = r_edges[None, 1:]
    m = np.diff(M_edges)[None, :]; dr = np.diff(r_edges)[None, :]
    a1 = np.maximum(r1, R); a2 = np.maximum(r2, R)
    F = lambda r: np.sqrt(np.maximum(r * r - R * R, 0.0)) - R * np.arccos(np.minimum(R / r, 1.0))
    Ac = lambda r: np.arccos(np.minimum(R / r, 1.0))
    Mtot = M_edges[-1]
    Mcyl = Mtot - (m / dr * (F(a2) - F(a1))).sum(1)
    dMc = (m / dr * (Ac(a2) - Ac(a1))).sum(1)
    Rr = R[:, 0]
    return Mcyl / (math.pi * Rr ** 2) - dMc / (2 * math.pi * Rr)


def nfw_ds_wb(R, rs, rhos):
    """Wright & Brainerd (2000) DeltaSigma of an untruncated NFW, rho_s [Msun/Mpc^3], r_s [Mpc]."""
    x = np.asarray(R, float) / rs
    x = np.where(np.abs(x - 1) < 1e-9, 1 + 1e-9, x)
    lo = x < 1
    s = np.sqrt(np.abs(1 - x * x))
    arc = np.where(lo, np.arccosh(1 / np.minimum(x, 1 - 1e-15)), np.arccos(1 / np.maximum(x, 1 + 1e-15)))
    h = np.log(x / 2) + arc / s
    f = (1 - arc / s) / (x * x - 1)
    return rhos * rs * (4 * h / x ** 2 - 2 * f)


# ------------------------------------------------------------------ grids of pair radii
GEDGE = np.logspace(math.log10(1e-15), math.log10(5e-12), 16)      # m/s^2
GEDGE_K = GEDGE / SI_ACC
_GL_X, _GL_W = np.polynomial.legendre.leggauss(6)
def _nodes():
    lo, hi = np.log(GEDGE_K[:-1]), np.log(GEDGE_K[1:])
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    g = np.exp(mid[:, None] + half[:, None] * _GL_X[None, :])
    w = half[:, None] * _GL_W[None, :]
    return g, w / g
GN, WN = _nodes()          # (15,6) each; WN = quadrature weight / g


# ------------------------------------------------------------------ LCDM comparators
RHOC_H674 = 3 * 67.4 ** 2 / (8 * math.pi * G_MPC)
OM_M16 = 0.315
def _nfw_m(x):
    x = np.asarray(x, float)
    return np.log1p(x) - x / (1 + x)
def conc(M200c):
    return 10 ** (0.905 - 0.101 * (math.log10(M200c * 0.674) - 12.0))
def m200c_from_m200m(M200m):
    def m200m_of(M200c):
        c = conc(M200c)
        R200 = (3 * M200c / (4 * math.pi * 200 * RHOC_H674)) ** (1 / 3)
        f = lambda lx: M200c * float(_nfw_m(c * math.exp(lx) / R200)) / float(_nfw_m(c)) / (4 * math.pi / 3 * math.exp(3 * lx)) - 200 * OM_M16 * RHOC_H674
        rr = math.exp(brentq(f, math.log(R200), math.log(10 * R200), xtol=1e-13))
        return M200c * float(_nfw_m(c * rr / R200)) / float(_nfw_m(c))
    lm = brentq(lambda t: m200m_of(10 ** t) - M200m, math.log10(M200m) - 1, math.log10(M200m), xtol=1e-12)
    return 10 ** lm
def mand_tab():
    rows = [l.split("\t") for l in open(os.path.join(REPO, "real_research", "data", "mandelbaum2016_lbg_halo_mass.tsv")) if l.strip() and not l.startswith("#")][1:]
    return {c: np.array([[float(r[1]), float(r[3])] for r in rows if r[0] == c]) for c in ("red", "blue")}
_CGRID = {}
def collapse_grid(colour):
    if colour not in _CGRID:
        t = mand_tab()[colour]
        lg = np.linspace(8.0, 12.2, 421)
        lx = np.interp(lg, t[:, 0], t[:, 1])
        _CGRID[colour] = (lg, np.array([m200c_from_m200m(10 ** x / 0.673) for x in lx]))
    return _CGRID[colour]
def collapse(logMs, colour):
    lg, M = collapse_grid(colour)
    return float(np.exp(np.interp(logMs, lg, np.log(M))))

# Moster+13 z=0: M*/Mh = 2 N [ (Mh/M1)^-beta + (Mh/M1)^gamma ]^-1
_MO = dict(lM1=11.590, N=0.0351, beta=1.376, gamma=0.608)
_LMH = np.linspace(9.0, 16.0, 7001)
def _mo_lmstar(lmh):
    mh = 10 ** np.asarray(lmh, float); M1 = 10 ** _MO["lM1"]
    return np.log10(mh * 2 * _MO["N"] / ((mh / M1) ** (-_MO["beta"]) + (mh / M1) ** _MO["gamma"]))
_LMS_G = _mo_lmstar(_LMH)
assert np.all(np.diff(_LMS_G) > 0)
def moster_mh(logMs):
    return 10 ** float(np.interp(logMs, _LMS_G, _LMH))
_MOM = {}
def moster_m200c_from_m200m(logMs):
    lm = round(float(logMs), 3)
    if lm not in _MOM:
        _MOM[lm] = m200c_from_m200m(moster_mh(lm))
    return _MOM[lm]


# ------------------------------------------------------------------ per-object profile vector v(15): pair-averaged DeltaSigma [Msun/pc^2] in each g bin
def _finish(ds_fn, Mg):
    R = np.sqrt(G_MPC * Mg / GN)
    ds = ds_fn(R.ravel()).reshape(GN.shape) * 1e-12
    return (WN * ds).sum(1) / WN.sum(1)

def v_law(Mg, z, foot):
    a0 = A0[foot]
    re = 0.4 * r_ta_law(Mg, a0, z)
    r = np.geomspace(1e-4, re, 1500)
    Md = Mg * (nu_mono(G_MPC * Mg / r ** 2 / a0) - 1.0)
    return _finish(lambda R: dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)

def _nfw_v(Mg, M200):
    c = conc(M200)
    R200 = (3 * M200 / (4 * math.pi * 200 * RHOC_H674)) ** (1 / 3)
    r = np.geomspace(1e-4, 5 * R200, 2500)
    Mn = M200 * _nfw_m(c * r / R200) / float(_nfw_m(c))
    return _finish(lambda R: dsigma(R, r, Mn) + Mg / (math.pi * R ** 2), Mg)

def v_lcdm(Mg, logMs, colour, dlogM=0.0):
    return _nfw_v(Mg, collapse(logMs + dlogM, colour))
def v_moster(Mg, logMs, dlogM=0.0, mode="c"):
    if mode == "c":
        return _nfw_v(Mg, moster_mh(logMs + dlogM))
    return _nfw_v(Mg, moster_m200c_from_m200m(logMs + dlogM))

def v_one(kind, Mg, logMs, z, colour):
    """kind: 'B_canonical','B_alt','L','Mo','Mo_m', with optional suffix '+' / '-' for a +-0.1 dex M_* shift (L, Mo only)."""
    dl = 0.0
    if kind.endswith("+"): dl, kind = 0.1, kind[:-1]
    elif kind.endswith("-"): dl, kind = -0.1, kind[:-1]
    if kind.startswith("B_"): return v_law(Mg, z, kind[2:])
    if kind == "L": return v_lcdm(Mg, logMs, "red" if colour == 1 else "blue", dl)
    if kind == "Mo": return v_moster(Mg, logMs, dl, "c")
    if kind == "Mo_m": return v_moster(Mg, logMs, dl, "m")
    raise ValueError(kind)
