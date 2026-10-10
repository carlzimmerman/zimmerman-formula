"""CFG546 shared library: DK14 baseline, drained-shell template, projection, constructed covariances, Fisher.

Frozen in FROZEN_CRITERIA.md (baf7e3dd4). Comoving h-units throughout: r, R in h^-1 Mpc; rho in h^2 Msun Mpc^-3; DeltaSigma in h Msun pc^-2.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
import json, math
import numpy as np
from scipy import special

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
trapz = getattr(np, "trapezoid", None) or np.trapz
OM = 0.30966                      # Planck18 (DESI release cosmology)
RHOM = 2.775e11 * OM              # comoving mean matter density, h^2 Msun / Mpc^3
DTA_TAB = {"z": [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0], "D": [11.805621559499393, 8.892905179986965, 7.536874143053635,
                                                             6.8224726795637585, 6.41190935473136, 5.997145249276129, 5.810864374327593]}
PNAMES = ["A", "lnrhos", "lnrs", "lnalpha", "lnrt", "lnbeta", "lngamma", "be", "se", "m0", "m1"]
SPLASH = ["lnrt", "lnbeta", "lngamma"]


def delta_ta(z):
    return float(np.interp(z, DTA_TAB["z"], DTA_TAB["D"]))


def chi_com(z, n=2000):
    zz = np.linspace(0, z, n)
    return 2997.92458 * trapz(1 / np.sqrt(OM * (1 + zz) ** 3 + 1 - OM), zz)


# ---------------------------------------------------------------- templates
class Template:
    """rel(x), x = r/r_ta; zero for x < 0.2 and x > 4; lognormal r_ta smoothing sigma_ln = 0.2; optional position scale."""
    def __init__(self, xc, rel, sig_ln=0.2, xscale=1.0):
        xc = np.asarray(xc, float); rel = np.nan_to_num(np.asarray(rel, float))
        rel = np.where((xc >= 0.2) & (xc <= 4.0), rel, 0.0)
        self.lx = np.log(np.geomspace(0.02, 20, 1200))
        base = np.interp(np.exp(self.lx), xc, rel, left=0.0, right=0.0)
        base = np.where((np.exp(self.lx) >= 0.2) & (np.exp(self.lx) <= 4.0), base, 0.0)
        if sig_ln > 0:
            dl = self.lx[1] - self.lx[0]; u = np.arange(-int(4 * sig_ln / dl), int(4 * sig_ln / dl) + 1) * dl
            w = np.exp(-0.5 * (u / sig_ln) ** 2); w /= w.sum()
            base = np.convolve(base, w, mode="same")
        self.val = base; self.xscale = xscale

    def __call__(self, x):
        return np.interp(np.log(np.maximum(x / self.xscale, 1e-6)), self.lx, self.val, left=0.0, right=0.0)


# ---------------------------------------------------------------- DK14
RG = np.geomspace(1e-4, 300.0, 900)        # 3D grid
RP = np.geomspace(1e-3, 120.0, 260)        # projected grid
LG = np.concatenate([[0.0], np.geomspace(1e-4, 40.0, 420)])


def r200m(M):
    return (3 * M / (4 * np.pi * 200 * RHOM)) ** (1 / 3)


def fiducial(M200m, z):
    """DK14 fiducial (frozen): c from colossus diemer19, alpha Gao+08, r_t (1.9-0.18 nu) r200m, beta 4, gamma 6, b_e 1, s_e 1.5."""
    from colossus.cosmology import cosmology
    from colossus.halo import concentration
    from colossus.lss import peaks
    cosmology.setCosmology("planck18")
    c = float(concentration.concentration(M200m, "200m", z, model="diemer19"))
    nu = float(peaks.peakHeight(M200m, z))
    R = r200m(M200m); rs = R / c
    alpha = 0.155 + 0.0095 * nu ** 2
    p = dict(A=0.0, lnrhos=0.0, lnrs=math.log(rs), lnalpha=math.log(alpha), lnrt=math.log((1.9 - 0.18 * nu) * R),
             lnbeta=math.log(4.0), lngamma=math.log(6.0), be=1.0, se=1.5, m0=0.0, m1=0.0)
    # normalise rho_s: M(<r200m) of (rho_m + Delta rho) = M200m
    dr = drho(p, R, unit_rhos=True)
    m = RG <= R
    Min = trapz(4 * np.pi * RG[m] ** 2 * dr["inner"][m], RG[m]); Mout = trapz(4 * np.pi * RG[m] ** 2 * dr["outer"][m], RG[m])
    Mtot = M200m - RHOM * 4 / 3 * np.pi * R ** 3
    p["lnrhos"] = math.log((Mtot - Mout) / Min)
    return p, dict(c=c, nu=nu, r200m=R, M200m=M200m, z=z)


def drho(p, R200, unit_rhos=False):
    rs, a, rt, b, g = (math.exp(p[k]) for k in ("lnrs", "lnalpha", "lnrt", "lnbeta", "lngamma"))
    rhos = 1.0 if unit_rhos else math.exp(p["lnrhos"])
    inner = rhos * np.exp(-2 / a * ((RG / rs) ** a - 1)) * (1 + (RG / rt) ** b) ** (-g / b)
    outer = RHOM * p["be"] * (RG / (5 * R200)) ** (-p["se"])
    return dict(inner=inner, outer=outer, tot=inner + outer)


def rta_of(dtot, z):
    M = np.concatenate([[0.0], np.cumsum(0.5 * (dtot[1:] * RG[1:] ** 2 + dtot[:-1] * RG[:-1] ** 2) * np.diff(RG))]) * 4 * np.pi
    mean = RHOM + M / (4 / 3 * np.pi * RG ** 3)
    ok = np.where(mean >= delta_ta(z) * RHOM)[0]
    return float(RG[ok.max()]) if len(ok) else float("nan")


def rsp_of(dtot):
    lr = np.log(RG); ld = np.log(RHOM + dtot)
    s = np.gradient(ld, lr); m = (RG > 0.2) & (RG < 20)
    return float(RG[m][np.argmin(s[m])])


def project(dr):
    """DeltaSigma(R) on RP for a 3D Delta rho on RG (h Msun / pc^2, comoving)."""
    rr = np.sqrt(RP[:, None] ** 2 + LG[None, :] ** 2)
    f = np.interp(np.log(rr), np.log(RG), dr)
    Sig = 2 * trapz(f, LG, axis=1)
    cum = np.concatenate([[Sig[0] * RP[0] ** 2 / 2], Sig[0] * RP[0] ** 2 / 2 + np.cumsum(0.5 * (Sig[1:] * RP[1:] + Sig[:-1] * RP[:-1]) * np.diff(RP))])
    mean_in = 2 * cum / RP ** 2
    return (mean_in - Sig) * 1e-12


def model(p, info, tmpl, edges):
    """bin-averaged DeltaSigma_obs for parameters p (dict), template tmpl (or None), radial bin edges (comoving h^-1 Mpc)."""
    d = drho(p, info["r200m"])
    tot = d["tot"]
    if tmpl is not None and p["A"] != 0.0:
        ra = rta_of(tot, info["z"])
        tot = tot * (1 + p["A"] * tmpl(RG / ra))
    ds = project(tot)
    out = np.zeros(len(edges) - 1)
    for i in range(len(edges) - 1):
        rr = np.geomspace(edges[i], edges[i + 1], 9)
        v = np.interp(np.log(rr), np.log(RP), ds)
        out[i] = trapz(v * rr, rr) / trapz(rr, rr)
    rc = np.sqrt(edges[1:] * edges[:-1])
    return out * (1 + p["m0"] + p["m1"] * np.log(rc))


def priors(p0, desi=False):
    """Gaussian prior sigmas (frozen); None = flat."""
    return {"lnalpha": 0.6, "lnbeta": 0.2, "lngamma": 0.2, "m0": 0.03, "m1": (1.0 if desi else 0.03)}


STEP = {"A": 0.05, "lnrhos": 0.01, "lnrs": 0.01, "lnalpha": 0.01, "lnrt": 0.01, "lnbeta": 0.01, "lngamma": 0.01,
        "be": 0.01, "se": 0.01, "m0": 0.005, "m1": 0.005}


def jacobian(p0, info, tmpl, edges, names=PNAMES, ntile=1):
    J = []
    for k in names:
        pp = dict(p0); pm = dict(p0); pp[k] += STEP[k]; pm[k] -= STEP[k]
        J.append((model(pp, info, tmpl, edges) - model(pm, info, tmpl, edges)) / (2 * STEP[k]))
    J = np.array(J).T
    return np.tile(J, (ntile, 1)) if ntile > 1 else J


def fisher(J, Cinv, pri, names=PNAMES, fixed=()):
    F = J.T @ Cinv @ J
    for i, k in enumerate(names):
        if k in pri and pri[k] is not None: F[i, i] += 1 / pri[k] ** 2
    keep = [i for i, k in enumerate(names) if k not in fixed]
    return F[np.ix_(keep, keep)], [names[i] for i in keep]


def fisher_summary(J, Cinv, pri, dmodel_template=None):
    F, nm = fisher(J, Cinv, pri)
    Ci = np.linalg.inv(F)
    iA = nm.index("A")
    sA = math.sqrt(Ci[iA, iA])
    corr = lambda k: float(Ci[iA, nm.index(k)] / math.sqrt(Ci[iA, iA] * Ci[nm.index(k), nm.index(k)]))
    Ff, nmf = fisher(J, Cinv, pri, fixed=SPLASH)
    sAf = math.sqrt(np.linalg.inv(Ff)[nmf.index("A"), nmf.index("A")])
    out = dict(sigma_A=sA, Z=1 / sA, Z_fixed_splash=1 / sAf, cost=sA / sAf, corr_A_lnrt=corr("lnrt"), corr_A_se=corr("se"),
               corr_A_be=corr("be"))
    return out


def bias_baseline(J, Cinv, pri, delta):
    """linear parameter bias of the baseline (A fixed at 0) when the data carry delta (template, A = 1)."""
    F, nm = fisher(J, Cinv, pri, fixed=("A",))
    Jn = J[:, 1:]
    return dict(zip(nm, np.linalg.solve(F, Jn.T @ Cinv @ delta)))


# ---------------------------------------------------------------- constructed covariance
def sigma_crit_com(zl, zs):
    Dl = chi_com(zl) / (1 + zl); Ds = chi_com(zs) / (1 + zs); Dls = (chi_com(zs) - chi_com(zl)) / (1 + zs)
    return 1.6625e6 * Ds / (Dl * Dls) / (1 + zl) ** 2      # comoving convention: Sigma_crit,phys / (1+z_l)^2


_PK = {}


def ckk(zs, ell):
    if zs not in _PK:
        import camb
        pars = camb.CAMBparams()
        pars.set_cosmology(H0=67.66, ombh2=0.02242, omch2=0.11933, mnu=0.06)
        pars.InitPower.set_params(As=2.105e-9, ns=0.9665)
        pars.set_matter_power(redshifts=[0.0], kmax=50.0)
        pars.NonLinear = camb.model.NonLinear_both
        PK = camb.get_matter_power_interpolator(pars, nonlinear=True, hubble_units=True, k_hunit=True, kmax=50.0, zmax=zs + 0.1)
        chis = chi_com(zs)
        cc = np.linspace(1.0, chis - 1.0, 300)
        zz = np.array([np.interp(c, [chi_com(z) for z in np.linspace(0, zs + 0.05, 200)], np.linspace(0, zs + 0.05, 200)) for c in cc])
        _PK[zs] = (PK, cc, zz, chis)
    PK, cc, zz, chis = _PK[zs]
    W = 1.5 * OM / 2997.92458 ** 2 * cc * (chis - cc) / chis * (1 + zz)
    out = np.zeros(len(ell))
    for i, l in enumerate(ell):
        k = (l + 0.5) / cc
        pk = np.array([PK.P(z, kk) if kk < 50 else 0.0 for z, kk in zip(zz, k)])
        out[i] = trapz(W ** 2 / cc ** 2 * pk, cc)
    return out


def constructed_cov(ds, edges, ds_par, f_lss=1.0, f_int=0.25):
    """shape noise + LSS (per sight line / N) + intrinsic halo-to-halo; returns C (h Msun/pc^2)^2."""
    N, zl, zs, neff, se = ds_par["N"], ds_par["zl"], ds_par["zs"], ds_par["neff"], ds_par["se"]
    chil = chi_com(zl); Sc = sigma_crit_com(zl, zs)
    th = edges / chil * 180 / np.pi * 60          # arcmin
    area = np.pi * (th[1:] ** 2 - th[:-1] ** 2)
    C = np.diag(Sc ** 2 * se ** 2 / (N * neff * area))
    ell = np.geomspace(10, 1e5, 220)
    ck = ckk(zs, ell)
    thr = edges / chil
    Jb = np.zeros((len(edges) - 1, len(ell)))
    for i in range(len(edges) - 1):
        t = np.linspace(thr[i], thr[i + 1], 24)
        Jb[i] = trapz(special.jv(2, np.outer(ell, t)) * t, t, axis=1) / trapz(t, t)
    nb = len(edges) - 1
    CL = np.array([[trapz(ell * ck / (2 * np.pi) * Jb[i] * Jb[j], ell) for j in range(nb)] for i in range(nb)]) * Sc ** 2
    C = C + f_lss * CL / N
    lr = np.log(np.sqrt(edges[1:] * edges[:-1]))
    Ci = np.outer(f_int * ds, f_int * ds) * np.exp(-np.abs(lr[:, None] - lr[None, :]) / 1.0)
    return C + Ci / N
