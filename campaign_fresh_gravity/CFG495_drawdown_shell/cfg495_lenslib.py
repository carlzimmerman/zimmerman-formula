"""CFG495 lens-model library (Steps 2 and 3). Source copies (not imports) of CFG377's cfg100_lib pieces + the engine's drawdown rule
written for one isolated lens. Used by cfg495_predict.py and cfg495_test.py.

Per lens (M_gal = lens baryons, z, log M*), every mass profile is truncated at the LCDM-equivalent turnaround radius r_ta:
  LCDM-equivalent matter   rho_m = NFW(M200c = Moster+13^-1(M*, z), c = Duffy+08)      [(U): literature relations recalled, not read from disk]
  r_ta                     mean density inside r_ta = (1 + delta_ta(z)) rho_bar_m(z)   (CFG100's delta_ta)
  f_ret = min(M_gal / (f_b M_ta), 1);  r_M = sqrt(G M_gal / a0);  r_edge = min(r_M / ln(1 + f_ret f_b / (1 - f_b)), r_ta)   (engine / CFG423 edge)
  cold  rho_c = (1 - f_b) rho_m;  phantom rho_ph from the law M_ph(r) = M_gal (nu_mono(G M_gal / r^2 / a0) - 1)
  LCDM    : M_gal (point) + (1 - f_b f_ret) rho_m                                   (all non-galaxy matter NFW)
  F_nodd  : M_gal + f_b (1 - f_ret) rho_m + [r < r_edge] max(rho_ph, rho_c) + [r > r_edge] rho_c      (= engine with the draw OFF, NOCOMP)
  drawdown: M_e = int_{r<r_edge} max(rho_ph - rho_c, 0) dV  (the engine's e)
            PROP (engine): - q rho_c on r < r_ta,  q = M_e / M_c(<r_ta)           -> F_dd = F_nodd + PROP   (mass inside r_ta = M_ta exactly)
            SHELL (variant): - q_sh rho_c on r_edge < r < r_ta, q_sh = M_e / M_c(r_edge..r_ta)
"""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

G_MPC = 4.30091727e-9            # Mpc (km/s)^2 / Msun
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {k: v / SI_ACC for k, v in A0_SI.items()}
OM, H = 0.3153, 0.6736
H0 = 100 * H
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G_MPC)
FB = 0.02237 / (0.02237 + 0.1200)  # the engine's f_b

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

def dsigma(R, r_edges, M_edges):
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

GEDGE = np.logspace(math.log10(1e-15), math.log10(5e-12), 16)      # m/s^2
GEDGE_K = GEDGE / SI_ACC
_GL_X, _GL_W = np.polynomial.legendre.leggauss(6)
def _nodes():
    lo, hi = np.log(GEDGE_K[:-1]), np.log(GEDGE_K[1:])
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    g = np.exp(mid[:, None] + half[:, None] * _GL_X[None, :])
    w = half[:, None] * _GL_W[None, :]
    return g, w / g
GN, WN = _nodes()
def finish(ds_fn, Mg):
    """15-bin pair-averaged ESD [Msun/pc^2] of ds_fn(R [Mpc]) [Msun/Mpc^2] (CFG377's _finish)."""
    R = np.sqrt(G_MPC * Mg / GN)
    ds = ds_fn(R.ravel()).reshape(GN.shape) * 1e-12
    return (WN * ds).sum(1) / WN.sum(1)
def node_R(Mg):
    return np.sqrt(G_MPC * Mg / GN)

# ---------------------------------------------------------------- LCDM-equivalent halo (U)
def moster_ms(lMh, z):
    s = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * s); Nn = 0.0351 - 0.0247 * s; be = 1.376 - 0.826 * s; ga = 0.608 + 0.329 * s
    Mh = 10 ** lMh
    return math.log10(2 * Nn * Mh / ((Mh / M1) ** -be + (Mh / M1) ** ga))
def inv_moster(lMs, z):
    return brentq(lambda x: moster_ms(x, z) - lMs, 9.0, 16.0)
def Ez2(z): return OM * (1 + z) ** 3 + 1 - OM
def nfw(M200, z):
    c = 5.71 * (M200 / (2e12 / H)) ** -0.084 * (1 + z) ** -0.47
    r200 = (3 * M200 / (4 * math.pi * 200 * RHOC0 * Ez2(z))) ** (1 / 3)
    mc = math.log(1 + c) - c / (1 + c)
    def Menc(r):
        x = c * np.asarray(r, float) / r200
        return M200 * (np.log1p(x) - x / (1 + x)) / mc
    def rho(r):
        x = c * np.asarray(r, float) / r200
        return M200 / (4 * math.pi * (r200 / c) ** 3 * mc) / (x * (1 + x) ** 2)
    return Menc, rho, c, r200

def lens_model(Mg, z, lMs, foot, nr=2500, dlogM=0.0):
    """returns dict with radial grid r [Mpc] (to r_ta) and enclosed-mass profiles [Msun] of the distributed parts (point mass Mg separate)."""
    a0 = A0[foot]
    M200 = 10 ** (inv_moster(lMs, z) + dlogM)
    Menc, rho, c, r200 = nfw(M200, z)
    rho_ta = OM * RHOC0 * (1 + z) ** 3 * dta(z)
    rta = math.exp(brentq(lambda lr: math.log(float(Menc(math.exp(lr)))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho_ta),
                          math.log(r200 * 0.5), math.log(r200 * 50)))
    Mta = float(Menc(rta))
    fret = min(Mg / (FB * Mta), 1.0)
    rM = math.sqrt(G_MPC * Mg / a0)
    redge = min(rM / math.log(1 + fret * FB / (1 - FB)), rta)
    r = np.geomspace(1e-4, rta, nr)
    Mph = Mg * (nu_mono(G_MPC * Mg / r ** 2 / a0) - 1.0)
    rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    rho_c = (1 - FB) * rho(r)
    Mc = (1 - FB) * Menc(r)
    dV = np.diff(r) * 4 * math.pi * (0.5 * (r[1:] + r[:-1])) ** 2
    def cum(dens):
        mid = 0.5 * (dens[1:] + dens[:-1])
        return np.concatenate([[0.0], np.cumsum(mid * dV)])
    inside = r <= redge
    exc = np.where(inside, np.maximum(rho_ph - rho_c, 0.0), 0.0)
    Mexc = cum(exc)                                   # = M_e(<r), frozen beyond r_edge
    Me = float(Mexc[-1])
    Mc_ta = float(Mc[-1]); Mc_e = float(np.interp(redge, r, Mc))
    q = Me / Mc_ta; qsh = Me / (Mc_ta - Mc_e) if Mc_ta - Mc_e > 1e-6 * Mc_ta else float('inf')   # inf: edge at r_ta, no shell
    M_lcdm = (1 - FB * fret) * Menc(r)
    M_nodd = FB * (1 - fret) * Menc(r) + Mc + Mexc          # max(rho_ph, rho_c) = rho_c + max(rho_ph - rho_c, 0)
    D_prop = -q * Mc
    D_shell = -qsh * np.maximum(Mc - Mc_e, 0.0) if np.isfinite(qsh) else np.zeros_like(Mc)
    return dict(r=r, rta=rta, Mta=Mta, M200=M200, c=c, r200=r200, fret=fret, rM=rM, redge=redge, Me=Me, q=q, qsh=qsh,
                M_lcdm=M_lcdm, M_nodd=M_nodd, D_prop=D_prop, D_shell=D_shell, Mc=Mc, Mph_edge=float(np.interp(redge, r, Mph)))

def esd_vectors(Mg, z, lMs, foot, extra_R=None, dlogM=0.0):
    """15-bin pair-averaged ESDs [Msun/pc^2] for LCDM, F_nodd, drawdown (PROP, SHELL); plus the model dict."""
    m = lens_model(Mg, z, lMs, foot, dlogM=dlogM)
    r = m["r"]
    pm = lambda R: Mg / (math.pi * R ** 2)
    out = dict(
        lcdm=finish(lambda R: dsigma(R, r, m["M_lcdm"]) + pm(R), Mg),
        nodd=finish(lambda R: dsigma(R, r, m["M_nodd"]) + pm(R), Mg),
        prop=finish(lambda R: dsigma(R, r, m["D_prop"]), Mg),
        shell=finish(lambda R: dsigma(R, r, m["D_shell"]), Mg))
    if extra_R is not None:
        out["R_lcdm"] = (dsigma(extra_R, r, m["M_lcdm"]) + pm(extra_R)) * 1e-12
        out["R_nodd"] = (dsigma(extra_R, r, m["M_nodd"]) + pm(extra_R)) * 1e-12
        out["R_prop"] = dsigma(extra_R, r, m["D_prop"]) * 1e-12
        out["R_shell"] = dsigma(extra_R, r, m["D_shell"]) * 1e-12
    return out, m

# ---------------------------------------------------------------- frozen two-halo (environment) term from the S0 control
def growth_D(z):
    g = lambda a: quad(lambda u: 1.0 / (u * math.sqrt(OM / u ** 3 + 1 - OM)) ** 3, 0, a)[0] * math.sqrt(OM / a ** 3 + 1 - OM)
    return g(1 / (1 + z)) / g(1.0)
def env_template(env, iso="iso1"):
    """env: list of sim-JSON env dicts (one per S0 control). Returns (log10 M_ta [Msun/h] classes, Rc [Mpc/h] centres, table [h Msun/pc^2])."""
    keys = sorted({k.split("|")[0] for e in env for k in e}, key=float)
    RB = None; lM, tab = [], []
    for k in keys:
        rows = [e[f"{k}|{iso}"] for e in env if f"{k}|{iso}" in e and e[f"{k}|{iso}"]["n"] > 0]
        if not rows: continue
        w = np.array([r_["n"] for r_ in rows], float)
        A_ = np.array([r_["mean"] for r_ in rows], float)                       # NaN = empty annulus on the lattice
        fin = np.isfinite(A_)
        t_ = np.nansum(A_ * w[:, None], 0) / np.maximum((fin * w[:, None]).sum(0), 1e-30)
        t_[~fin.any(0)] = np.nan
        tab.append(t_)
        lM.append(math.log10(rows[0]["M_ta"]))
    return np.array(lM), np.array(tab)
def two_halo_fn(lMta_hunits, z, lMcls, Rc, tab, zfac="D2"):
    """physical Delta Sigma_2h(R [Mpc]) [Msun/Mpc^2] for a lens of M_ta (Msun/h) at z, from the S0 table (z = 0, comoving h-units)."""
    i = np.clip(np.interp(lMta_hunits, lMcls, np.arange(len(lMcls))), 0, len(lMcls) - 1)
    i0 = int(math.floor(i)); i1 = min(i0 + 1, len(lMcls) - 1); f = i - i0
    prof = (1 - f) * tab[i0] + f * tab[i1]
    ok = np.isfinite(prof); Rc, prof = np.asarray(Rc)[ok], prof[ok]        # empty-annulus bins (lattice) dropped
    D = growth_D(z)
    fac = {"D2": D ** 2, "D1": D, "D0": 1.0}[zfac] * (1 + z) ** 2 * H
    R0 = 2 * 200.0 / 512                               # two 512^3 cells: below this the mesh template is not resolved
    v0 = float(np.interp(math.log(R0), np.log(Rc), prof))
    def fn(R):
        Rcom = np.asarray(R, float) * (1 + z) * H
        v = np.where(Rcom >= R0, np.interp(np.log(np.maximum(Rcom, R0)), np.log(Rc), prof), v0 * (Rcom / R0) ** 2)   # smooth-hole R^2 taper
        return v * fac * 1e12
    return fn

def group_q(Mta, z, foot, fret=1.0, nr=2500):
    """analytic engine rule for a halo of given turnaround mass M_ta [Msun] with f_ret (default 1, as in the PM engine): M200c is solved
    so that the Duffy NFW holds M_ta inside r_ta; M_gal = f_ret f_b M_ta. Returns (q, x_edge = r_edge / r_ta, M_e / M_ta)."""
    rho_ta = OM * RHOC0 * (1 + z) ** 3 * dta(z)
    rta = (3 * Mta / (4 * math.pi * rho_ta)) ** (1 / 3)
    lM200 = brentq(lambda l: float(nfw(10 ** l, z)[0](rta)) - Mta, math.log10(Mta) - 2, math.log10(Mta) + 0.5)
    Menc, rho, c, r200 = nfw(10 ** lM200, z)
    Mg = fret * FB * Mta; a0 = A0[foot]
    rM = math.sqrt(G_MPC * Mg / a0); redge = min(rM / math.log(1 + fret * FB / (1 - FB)), rta)
    r = np.geomspace(1e-4, redge, nr)
    Mph = Mg * (nu_mono(G_MPC * Mg / r ** 2 / a0) - 1.0)
    rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2); rho_c = (1 - FB) * rho(r)
    ex = np.maximum(rho_ph - rho_c, 0.0); dV = np.diff(r) * 4 * math.pi * (0.5 * (r[1:] + r[:-1])) ** 2
    Me = float((0.5 * (ex[1:] + ex[:-1]) * dV).sum())
    return Me / ((1 - FB) * Mta), redge / rta, Me / Mta
