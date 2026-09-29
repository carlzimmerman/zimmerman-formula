# CFG77 own implementation (see CFG77_FROZEN.md).  No import/exec of CFG61/CFG67 code.
import math, os
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
DATA = REPO + "/real_research/data/lensing_rar"
BR = DATA + "/brouwer2021_rar"
G_MPC = 4.30091727e-9            # Mpc (km/s)^2 / Msun
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M             # (km/s)^2/Mpc -> m/s^2
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {k: v / SI_ACC for k, v in A0_SI.items()}
OM, H = 0.3153, 0.6736
H0 = 100 * H
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G_MPC)     # Msun/Mpc^3

# ---------------------------------------------------------------- kernel nu_mono (own re-implementation of FP1's construction)
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

# ---------------------------------------------------------------- top-hat turnaround contrast (own solver)
def one_plus_delta_ta(a, Om=OM, H0_=H0):
    OL = 1 - Om
    t_a = 2.0 / (3 * H0_ * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om) * a ** 1.5) if OL > 0 else 2.0 / (3 * H0_) * a ** 1.5 / math.sqrt(Om)
    L = OL * H0_ ** 2
    def tint(w):
        f = lambda p: 2 * math.sin(p) ** 2 / math.sqrt(2 * w - L * math.sin(p) ** 2 * (1 + math.sin(p) ** 2))
        return quad(f, 0, math.pi / 2, epsabs=1e-13, epsrel=1e-12)[0]
    wlo = L * (1 + 1e-5) if L > 0 else 1e-4 * H0_ ** 2
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
    f = lambda lr: math.log(Mb * float(nu_mono(G_MPC * Mb / math.exp(2 * lr) / a0)) / (4 * math.pi / 3 * math.exp(3 * lr) * rho / 1.0)) \
        if False else math.log(Mb * float(nu_mono(G_MPC * Mb / math.exp(2 * lr) / a0))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho)
    return math.exp(brentq(f, math.log(1e-5), math.log(1e3), xtol=1e-12))

# ---------------------------------------------------------------- projector: DeltaSigma of a spherical shell-decomposed profile
def dsigma(R, r_edges, M_edges, m0=0.0):
    """DeltaSigma [Msun/Mpc^2] at R [Mpc] (array) for an enclosed dark mass M(<r) given at r_edges (piecewise-constant density
    per shell in r-space) plus a central point mass m0 (Msun). Exact shell integrals."""
    R = np.atleast_1d(np.asarray(R, float))[:, None]
    r1 = r_edges[None, :-1]; r2 = r_edges[None, 1:]
    m = np.diff(M_edges)[None, :]; dr = np.diff(r_edges)[None, :]
    a1 = np.maximum(r1, R); a2 = np.maximum(r2, R)
    F = lambda r: np.sqrt(np.maximum(r * r - R * R, 0.0)) - R * np.arccos(np.minimum(R / r, 1.0))
    Ac = lambda r: np.arccos(np.minimum(R / r, 1.0))
    Mtot = M_edges[-1] + m0
    Mcyl = Mtot - (m / dr * (F(a2) - F(a1))).sum(1)
    dMc = (m / dr * (Ac(a2) - Ac(a1))).sum(1)                      # dM_cyl/dR = R * int M'/(r sqrt(r^2-R^2)) dr
    Rr = R[:, 0]
    Sig = dMc / (2 * math.pi * Rr)
    return Mcyl / (math.pi * Rr ** 2) - Sig

def make_grid(rmin, rmax, n):
    return np.geomspace(rmin, rmax, n)

# ---------------------------------------------------------------- data
def load_data(kind="Color"):
    ess = []
    for b in (1, 2):
        arr = np.loadtxt(f"{BR}/Fig-8_RAR-KiDS-isolated_{kind}bin_{b}.txt")
        ess.append(arr)
    late, early = ess
    cov = np.loadtxt(f"{BR}/Fig-8_RAR-KiDS-isolated_{kind}bins_covmatrix.txt")
    mins = cov[:, 0]
    C = (cov[:, 4] / cov[:, 6]).reshape(2, 2, 15, 15).transpose(0, 2, 1, 3).reshape(30, 30)
    d = np.concatenate([late[:, 1] / late[:, 4], early[:, 1] / early[:, 4]])
    err = np.concatenate([late[:, 3] / late[:, 4], early[:, 3] / early[:, 4]])
    gb = late[:, 0]; gb2 = early[:, 0]
    return dict(d=d, err=err, C=C, g=gb, g2=gb2, mins=np.unique(mins))

def diff_stat(dat, K, model_late=None, model_early=None, swap=False):
    """chi2 of D_obs - D_model on bin index list K; returns chi2, D_obs, C_D."""
    d, C = dat["d"].copy(), dat["C"].copy()
    if swap:
        perm = np.concatenate([np.arange(15, 30), np.arange(0, 15)])
        d = d[perm]; C = C[np.ix_(perm, perm)]
    K = np.asarray(K)
    l, e = K, K + 15
    D = d[e] - d[l]
    CD = C[np.ix_(e, e)] + C[np.ix_(l, l)] - C[np.ix_(e, l)] - C[np.ix_(l, e)]
    Dm = np.zeros(len(K)) if model_late is None else (model_early[K] - model_late[K])
    r = D - Dm
    return float(r @ np.linalg.solve(CD, r)), D, CD, r

# ---------------------------------------------------------------- lenses, groups, stacking
GEDGE = np.logspace(math.log10(1e-15), math.log10(5e-12), 16)      # m/s^2
GEDGE_K = GEDGE / SI_ACC                                            # (km/s)^2/Mpc
_GL_X, _GL_W = np.polynomial.legendre.leggauss(6)

def load_lenses(mutate=False, mgal_scale=(1.0, 1.0), logm_shift_early=0.0):
    d = np.load(DATA + "/lr_lenses.npz")
    z, logM, Mgal, typ = d["z"].copy(), d["logM"].copy(), d["Mgal"].copy(), d["typ"].copy()
    early = typ == 1
    if mutate:                                   # early lens M_* x2 (stellar and Brouwer g_bar mass)
        logM[early] += math.log10(2.0); Mgal[early] *= 2.0
    if logm_shift_early:
        logM[early] += logm_shift_early; Mgal[early] *= 10 ** logm_shift_early
    Mgal[~early] *= mgal_scale[0]; Mgal[early] *= mgal_scale[1]     # (late, early) IMF-like rescale of the baryon mass
    return dict(z=z, logM=logM, Mgal=Mgal, typ=typ, chi=d["chi"])

def make_groups(len_, sel=None, dlogm=0.01, dz=0.03):
    """groups of lenses per class on (log Mgal, z) cells; returns dict class->(n, Mgal, logM*, z)"""
    out = {}
    for c in (0, 1):
        m = (len_["typ"] == c)
        if sel is not None: m &= sel
        lm = np.log10(len_["Mgal"][m]); z = len_["z"][m]; lms = len_["logM"][m]
        key = np.floor(lm / dlogm).astype(np.int64) * 10000 + np.floor(z / dz).astype(np.int64)
        u, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
        s = lambda x: np.bincount(inv, weights=x) / cnt
        out[c] = dict(n=cnt.astype(float), Mgal=10 ** s(lm), logM=s(lms), z=s(z))
    return out

def _quad_nodes():
    """(k, node) -> ln g nodes and weights per bin; the pair weight per ln g is M/g"""
    lo, hi = np.log(GEDGE_K[:-1]), np.log(GEDGE_K[1:])
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    lng = mid[:, None] + half[:, None] * _GL_X[None, :]
    w = half[:, None] * _GL_W[None, :]
    return np.exp(lng), w                                             # g nodes (15,6) in (km/s)^2/Mpc

def stack(groups_c, prof_fn):
    """model stack (15 bins) [Msun/pc^2]: sum_i M_i int dlng (1/g) DS_i(R(g)) / sum_i M_i int dlng (1/g)."""
    g, w = _quad_nodes()
    num = np.zeros(15); den = np.zeros(15)
    for i in range(len(groups_c["n"])):
        M = groups_c["Mgal"][i]; n = groups_c["n"][i]
        R = np.sqrt(G_MPC * M / g).ravel()                            # Mpc
        ds = prof_fn(i, R).reshape(g.shape) * 1e-12                    # Msun/Mpc^2 -> Msun/pc^2
        ww = n * M * w / g
        num += (ww * ds).sum(1); den += ww.sum(1)
    return num / den

def law_profile(groups_c, foot, f_hot=0.0, r_alt=False):
    a0 = A0[foot]
    def fn(i, R):
        Mg = groups_c["Mgal"][i]; z = groups_c["z"][i]
        Mt = Mg * (1 + f_hot)
        re = 0.4 * r_ta_law(Mt, a0, z)
        r = np.geomspace(1e-4, re, 1500)
        y = G_MPC * Mt / r ** 2 / a0
        Md = Mt * (nu_mono(y) - 1.0)
        m0 = 0.0
        ds = dsigma(R, r, Md, m0=Md[0])                               # dark part (inner mass below 1e-4 Mpc as a point)
        return ds + Mt / (math.pi * R ** 2)
    return fn

# ---------------------------------------------------------------- LCDM comparator
RHOC_H674 = 3 * 67.4 ** 2 / (8 * math.pi * G_MPC)
OM_M16 = 0.315
def _nfw_m(x): return math.log1p(x) - x / (1 + x)
def m200c_from_m200m(M200m):
    def m200m_of(M200c):
        c = 10 ** (0.905 - 0.101 * (math.log10(M200c * 0.674) - 12.0))
        R200 = (3 * M200c / (4 * math.pi * 200 * RHOC_H674)) ** (1 / 3)
        f = lambda lx: M200c * _nfw_m(c * math.exp(lx) / R200) / _nfw_m(c) / (4 * math.pi / 3 * math.exp(3 * lx)) - 200 * OM_M16 * RHOC_H674
        rr = math.exp(brentq(f, math.log(R200), math.log(10 * R200), xtol=1e-13))
        return M200c * _nfw_m(c * rr / R200) / _nfw_m(c)
    lm = brentq(lambda t: m200m_of(10 ** t) - M200m, math.log10(M200m) - 1, math.log10(M200m), xtol=1e-12)
    return 10 ** lm
_TAB = None
def mand_tab():
    global _TAB
    rows = [l.split("\t") for l in open(REPO + "/real_research/data/mandelbaum2016_lbg_halo_mass.tsv") if l.strip() and not l.startswith("#")][1:]
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

def lcdm_profile(groups_c, colour):
    def fn(i, R):
        Mg = groups_c["Mgal"][i]
        M200 = collapse(groups_c["logM"][i], colour)
        c = 10 ** (0.905 - 0.101 * (math.log10(M200 * 0.674) - 12.0))
        R200 = (3 * M200 / (4 * math.pi * 200 * RHOC_H674)) ** (1 / 3)
        r = np.geomspace(1e-4, 5 * R200, 2500)
        Mn = M200 * np.array([_nfw_m(c * x / R200) for x in r]) / _nfw_m(c)
        return dsigma(R, r, Mn, m0=Mn[0]) + Mg / (math.pi * R ** 2)
    return fn
