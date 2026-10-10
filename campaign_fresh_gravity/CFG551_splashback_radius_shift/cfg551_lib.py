"""CFG551 shared code: nonlinear noiseless DK14 fits and splashback radii (FROZEN_CRITERIA.md, b1b7c9e08).

Builds on ../CFG546_drained_shell_cluster_lensing/cfg546_lib.py (imported unedited: fiducial, drho, rta_of, project, Template,
constructed_cov). Comoving h-units: r, R in h^-1 Mpc; rho in h^2 Msun Mpc^-3.
"""
import os, sys, math
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CFG, "CFG546_drained_shell_cluster_lensing"))
import cfg546_lib as LB                                        # noqa: E402

trapz = LB.trapz
FREE = ["lnrhos", "lnrs", "lnalpha", "lnrt", "lnbeta", "lngamma", "be", "se"]
XS = {"lnrhos": 0.1, "lnrs": 0.1, "lnalpha": 0.1, "lnrt": 0.1, "lnbeta": 0.1, "lngamma": 0.1, "be": 0.1, "se": 0.1}
PRI = {"lnalpha": 0.6, "lnbeta": 0.2, "lngamma": 0.2}          # frozen: More+16 / Baxter+17 / Chang+18 practice


def dk14(p, r, R200):
    """3D Delta rho of DK14 at radii r (analytic, any grid)."""
    rs, a, rt, b, g = (math.exp(p[k]) for k in ("lnrs", "lnalpha", "lnrt", "lnbeta", "lngamma"))
    inner = math.exp(p["lnrhos"]) * np.exp(-2 / a * ((r / rs) ** a - 1)) * (1 + (r / rt) ** b) ** (-g / b)
    return inner + LB.RHOM * p["be"] * (r / (5 * R200)) ** (-p["se"])


def sigma_proj(dr):
    """Sigma(R) on LB.RP for a 3D Delta rho on LB.RG (line of sight +-40 h^-1 Mpc), h Msun / pc^2."""
    rr = np.sqrt(LB.RP[:, None] ** 2 + LB.LG[None, :] ** 2)
    f = np.interp(np.log(rr), np.log(LB.RG), dr)
    return 2 * trapz(f, LB.LG, axis=1) * 1e-12


def binavg(f, edges):
    out = np.zeros(len(edges) - 1)
    for i in range(len(edges) - 1):
        rr = np.geomspace(edges[i], edges[i + 1], 9)
        v = np.interp(np.log(rr), np.log(LB.RP), f)
        out[i] = trapz(v * rr, rr) / trapz(rr, rr)
    return out


def observe(tot, method, edges):
    return binavg(LB.project(tot) if method == "L" else sigma_proj(tot), edges)


def framework_tot(p0, info, tmpl):
    tot = LB.drho(p0, info["r200m"])["tot"]
    if tmpl is None:
        return tot
    ra = LB.rta_of(tot, info["z"])
    return tot * (1 + tmpl(LB.RG / ra))


def fit(data, p0, info, method, edges, sig_bin=0.05, cov=None, starts=None):
    """least-squares DK14 fit (free FREE, priors PRI centred on the fiducial); ln residuals / sig_bin, or a covariance."""
    R200 = info["r200m"]
    Li = np.linalg.inv(np.linalg.cholesky(cov)) if cov is not None else None
    ld = np.log(np.maximum(data, 1e-30))

    def res(v):
        p = dict(p0); p.update(zip(FREE, v))
        m = observe(LB.drho(p, R200)["tot"], method, edges)
        r = (Li @ (m - data)) if Li is not None else (np.log(np.maximum(m, 1e-30)) - ld) / sig_bin
        return np.concatenate([r, [(p[k] - p0[k]) / s for k, s in PRI.items()]])

    v0 = np.array([p0[k] for k in FREE])
    if starts is None:
        starts = []
        for frt, dse in ((1.0, 0.0), (1.3, 0.3), (1 / 1.3, -0.3)):
            v = v0.copy(); v[FREE.index("lnrt")] += math.log(frt); v[FREE.index("se")] += dse; starts.append(v)
    best = None
    for v in starts:
        sol = least_squares(res, v, x_scale=np.array([XS[k] for k in FREE]), max_nfev=3000, xtol=1e-10, ftol=1e-12)
        if best is None or sol.cost < best.cost:
            best = sol
    p = dict(p0); p.update(zip(FREE, best.x))
    return p, float(2 * best.cost)


def rsp(p, R200, lo=0.5, hi=3.0, n=3000):
    """radius of the steepest log slope of rho_m + Delta rho (3D), over lo..hi r200m, parabolic refinement; (r_sp, edge_flag)."""
    r = np.geomspace(lo * R200, hi * R200, n); lr = np.log(r)
    s = np.gradient(np.log(LB.RHOM + dk14(p, r, R200)), lr)
    i = int(np.argmin(s))
    if i == 0 or i == n - 1:
        return float(r[i]), True
    a, b, c = s[i - 1], s[i], s[i + 1]
    d = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) != 0 else 0.0
    return float(math.exp(lr[i] + d * (lr[1] - lr[0]))), False


def edges_for(rmin, rmax, n=20):
    return np.geomspace(rmin, rmax, n + 1)


def predicted_ratio(M200m, z, method, tmpl, rng=(0.2, 10.0), sig_bin=0.05, cov_par=None):
    """R_pred = r_sp(fit to framework profile) / r_sp(fit to LCDM fiducial), same pipeline. Returns dict."""
    p0, info = LB.fiducial(M200m, z)
    e = edges_for(*rng)
    cov_L = cov_F = None
    d0 = observe(framework_tot(p0, info, None), method, e)
    dF = observe(framework_tot(p0, info, tmpl), method, e)
    if cov_par is not None:                                          # V5: constructed covariance (per profile, built on LCDM)
        cov_L = LB.constructed_cov(d0, e, cov_par); cov_F = cov_L
    pL, cL = fit(d0, p0, info, method, e, sig_bin, cov_L)
    pF, cF = fit(dF, p0, info, method, e, sig_bin, cov_F)
    rL, eL = rsp(pL, info["r200m"]); rF, eF = rsp(pF, info["r200m"])
    r0, _ = rsp(p0, info["r200m"])
    return dict(R=rF / rL, rsp_F=rF, rsp_L=rL, rsp_fid=r0, chi2_F=cF, chi2_L=cL, edge=bool(eL or eF), r200m=info["r200m"],
                rta=LB.rta_of(LB.drho(p0, info["r200m"])["tot"], z), rt_F=math.exp(pF["lnrt"]), rt_L=math.exp(pL["lnrt"]),
                se_F=pF["se"], se_L=pL["se"], nbins=len(e) - 1)
