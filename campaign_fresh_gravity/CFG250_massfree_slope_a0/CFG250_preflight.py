#!/usr/bin/env python3
r"""CFG250 pre-flight -- the mass-free slope estimator of a0 run on MOCK KURVS-like discs ONLY.  PHASE 1.

NO measured KURVS velocity or dispersion is read.  Columns read, and nothing else:
  kurvs2023_integrated.csv      kurvs_id, z_halpha, logMstar, reff_kpc, inc_sfr_deg, inc_star_deg
  kurvs2023_fdm.csv             kurvs_id, flag_star                     (which ten discs; the f_DM values are NOT read)
  kurvs2023_kinematics.csv      kurvs_id, flag_star                     (sigma0 / V/sigma0 are NOT read)
  kurvs_rc_points.csv           kurvs_id, R_kpc, err_up_kms, err_lo_kms, clipped_white_marker     (v_obs_kms is NOT read)
  kurvs_sigma_profiles.csv      kurvs_id, R_kpc, err_up_kms, err_lo_kms, clipped_white_marker     (sigma_obs_kms is NOT read)
The mock discs take M*, R_d = R_eff/1.68, z and inclination from the catalogue, the marker radii and error bars from the figures'
digitisation, and velocities/dispersions from the LAWS: g = nu(g_N/a) g_N in the plane of thin exponential discs (stars R_d, gas
mu M* at R_gas), a = a0 (flat) or a0 E(z) (rival), a constant intrinsic sigma with a declared pressure law, a Gaussian-PSF x box-bin
beam-smearing forward model (CFG184's geometry, re-implemented), correlated marker noise, and a +-5 deg inclination error.

The estimator is the one frozen in ../CFG250_FROZEN_CRITERIA.md: window |R| >= max(2 R_d, FWHM), both sides pooled, V = v sgn(R)/sin i,
sigma_win = weighted mean of the window's sigma markers, V_c^2 = V^2 + 2 sigma_win^2 |R|/R_d, a weighted fit of ln V_c^2 on ln|R|
(formal errors x sqrt 6), g_obs at the weighted pivot; the stacked common-a0 chi^2 over the sample with the slope predicted by the
same fit applied to the law's curve for a declared baryon SHAPE (DS, primary: stars R_d + gas mu = 0.67 at 2 R_d; no mass enters) or
for a point mass (PM, the idea as stated).  Statistic Lambda = log10 a0_hat, flat Lambda_F = log10 a0, rival Lambda_F + log10 E(z_med).
Sections: G geometry; C noise-free controls; B the slope bias beam smearing alone produces in the frozen window; P the frozen primary
on SEEING-LIMITED mocks (the H0 gate); I/S/H the SMEARING-FREE track (the limit an AO or smearing-forward-modelled analysis would
approach): recovery, coverage, the systematic axes A (pressure truth x sigma), B (baryon shape), D (inclination), the separation and
the decision rule; V variants and remedies (cold tracer, AO through the forward model, radii to 10 R_d, gas shape measured).
MUTATE=1 multiplies every mock analyst velocity by (|R|/1 kpc)^0.1 and writes *_MUTATE outputs; the recovery control must then fail.
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour any law; this is a feasibility study on mocks.
Run: python3 campaign_fresh_gravity/CFG250_massfree_slope_a0/CFG250_preflight.py      (about a minute)
"""
import os
import sys
import csv
import math
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.special import erf
from scipy.integrate import quad
from scipy.stats import chi2 as CHI2
import cfg250_common as C
import warnings
# numpy's Accelerate BLAS on this platform raises spurious 'divide by zero / overflow / invalid value encountered in matmul'
# warnings inside the smearing forward model (the same artefact CFG189 disclosed); every result is checked finite downstream.
warnings.filterwarnings("ignore", message=".*encountered in matmul")

T0 = time.time()
T = C.Tee("CFG250_preflight")
print(__doc__.split("Run: python3")[0].strip())
MUT = C.MUTATE
KER = {n: C.Kernel(n) for n in ("P2", "nu_mono")}
A0C = C.A0["canonical"]
LN10 = math.log(10)
NR = 150                                                      # mock realisations per cell
GRID = np.arange(-1.5, 1.5 + 1e-9, 0.01)                      # Lambda offsets from log10 a0 (canonical)
F_INF = math.sqrt(6.0)                                        # declared correlated-marker inflation (0.6'' bins / 0.1'' sampling)
DI_DEG = 5.0                                                  # declared inclination error
FWHM0, BIN0 = 0.57, 0.6
MU_DECL, RG_DECL = 0.67, 2.0                                  # the DS estimator's declared baryon shape


# ================================================================================================ inputs (allowed columns only)
def rcsv(path, cols):
    out = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            out.append({c: r[c] for c in cols})
    return out


integ = {int(r["kurvs_id"]): r for r in rcsv(os.path.join(C.AT, "kurvs2023_integrated.csv"),
                                             ["kurvs_id", "z_halpha", "logMstar", "reff_kpc", "inc_sfr_deg", "inc_star_deg"])}
fdm = rcsv(os.path.join(C.AT, "kurvs2023_fdm.csv"), ["kurvs_id", "flag_star"])
kin = rcsv(os.path.join(C.AT, "kurvs2023_kinematics.csv"), ["kurvs_id", "flag_star"])
TEN = sorted(int(r["kurvs_id"]) for r in fdm)
STAR = {int(r["kurvs_id"]) for r in fdm + kin if r["flag_star"].strip() == "*"}
MK = {}
for r in rcsv(os.path.join(C.AT, "kurvs_rc_profiles", "kurvs_rc_points.csv"),
              ["kurvs_id", "R_kpc", "err_up_kms", "err_lo_kms", "clipped_white_marker"]):
    MK.setdefault(int(r["kurvs_id"]), []).append((float(r["R_kpc"]), 0.5 * (float(r["err_up_kms"]) + float(r["err_lo_kms"])),
                                                  int(float(r["clipped_white_marker"]))))
SK = {}
for r in rcsv(os.path.join(C.AT, "kurvs_sigma_profiles", "kurvs_sigma_profiles.csv"),
              ["kurvs_id", "R_kpc", "err_up_kms", "err_lo_kms", "clipped_white_marker"]):
    SK.setdefault(int(r["kurvs_id"]), []).append((float(r["R_kpc"]), 0.5 * (float(r["err_up_kms"]) + float(r["err_lo_kms"])),
                                                  int(float(r["clipped_white_marker"]))))


def kpc_per_arcsec(z, H0=70.0, om=0.3):                       # the paper's cosmology, as CFG184
    dc = quad(lambda zz: 1.0 / math.sqrt(om * (1 + zz) ** 3 + 1 - om), 0, z)[0] * 299792.458 / H0 * 1e3
    return dc / (1 + z) * math.pi / (180 * 3600)


class Gal:
    def __init__(self, kid, window="primary", extend_to=None, fwhm=FWHM0):
        it = integ[kid]
        self.id = kid
        self.z = float(it["z_halpha"])
        self.Ms = 10 ** float(it["logMstar"])
        self.Reff = float(it["reff_kpc"])
        self.Rd = self.Reff / 1.68
        self.inc = {"sfr": float(it["inc_sfr_deg"]), "star": float(it["inc_star_deg"])}
        self.scale = kpc_per_arcsec(self.z)
        self.fwhm_kpc = fwhm * self.scale
        if window == "primary":
            self.Rin = max(2 * self.Rd, self.fwhm_kpc)
        elif window == "3Rd":
            self.Rin = 3 * self.Rd
        elif window == "2Rd":
            self.Rin = 2 * self.Rd
        elif window == "1.5fwhm":
            self.Rin = max(2 * self.Rd, 1.5 * self.fwhm_kpc)
        else:
            raise ValueError(window)
        pts = [(R, e) for R, e, cl in MK[kid] if (not cl) and abs(R) >= self.Rin]
        if extend_to is not None:                              # scenario: markers continued to extend_to x R_d (declared errors)
            add = []
            for sgn in (+1, -1):
                side = sorted([abs(R) for R, e in pts if np.sign(R) == sgn])
                if not side:
                    continue
                e_med = float(np.median([e for R, e in pts])) * 2.0
                r = side[-1] + 0.845
                while r <= extend_to * self.Rd:
                    add.append((sgn * r, e_med))
                    r += 0.845
            pts = pts + add
        pts.sort(key=lambda p: (np.sign(p[0]), abs(p[0])))
        self.R = np.array([p[0] for p in pts])
        self.e = np.array([p[1] for p in pts])
        self.aR = np.abs(self.R)
        self.lnR = np.log(np.maximum(self.aR, 1e-6))
        sp = [e for R, e, cl in SK.get(kid, []) if (not cl) and abs(R) >= self.Rin]
        self.sig_err_km = (1.0 / math.sqrt(sum(1.0 / e ** 2 for e in sp))) * F_INF if sp else None
        self.ok_radii = len(self.R) >= 5 and (self.lnR.max() - self.lnR.min()) >= 0.25


# ================================================================================================ truth curves
RT = np.concatenate([np.linspace(0.01, 30, 1500), np.linspace(30.5, 250, 300)])


def truth_Vc2(g, law, ker, mu, rg, newton=False, point=False):
    a = A0C * (float(C.E(g.z)) if law == "rival" else 1.0)
    geom = "point" if point else "disc"
    gN = C.gN_baryons(RT, g.Ms, mu, g.Rd, rg, geom)
    gobs = gN if newton else KER[ker].Phi(gN / a) * a
    return gobs * RT * C.KPC / 1e6                             # (km/s)^2


# ================================================================================================ beam smearing (CFG184's geometry)
XG = np.arange(-4.0, 4.0001, 0.03)
YG = np.arange(-3.0, 3.0001, 0.03)
XX, YY = np.meshgrid(XG, YG)
YS = (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3)


def k1d(u, fwhm, b):
    sg = max(fwhm, 1e-4) / 2.3548
    return (erf((u + b / 2) / (math.sqrt(2) * sg)) - erf((u - b / 2) / (math.sqrt(2) * sg))) / (2 * b)


def forward(g, Vrot_tab, sig, inc_deg, bs):
    """(V_bs, sigma_obs) at the window markers' |R| (V is the deprojection-ready rotation, i.e. V_los/sin i)."""
    if bs is None:
        V = np.interp(g.aR, RT, Vrot_tab)
        return V, np.full_like(V, sig)
    fwhm, b = bs[0], bs[1]
    hx = bs[2] if len(bs) > 2 else 1.0                          # H-alpha scale = hx x R_d (declared primary 1)
    ci, si = math.cos(math.radians(inc_deg)), math.sin(math.radians(inc_deg))
    Ras = np.sqrt(XX ** 2 + (YY / ci) ** 2)
    Rk = Ras * g.scale
    cphi = np.where(Ras > 0, XX / np.maximum(Ras, 1e-12), 0.0)
    Vl = np.interp(Rk, RT, Vrot_tab) * si * cphi
    I = np.exp(-Rk / (hx * g.Rd))
    IV, IV2 = I * Vl, I * Vl * Vl
    xs = np.unique(np.round(g.aR / g.scale, 6))
    hw = 0.3 * fwhm / FWHM0                                     # pseudo-slit half-width = the paper's 0.3'' scaled with the PSF
    wys = [k1d(YG - ys * hw / 0.3, fwhm, b) for ys in YS]
    vb, sb = {}, {}
    for x in xs:
        wx = k1d(XG - x, fwhm, b)
        m0 = np.array([wy @ I @ wx for wy in wys]); m1 = np.array([wy @ IV @ wx for wy in wys])
        m2 = np.array([wy @ IV2 @ wx for wy in wys])
        M0, M1, M2 = m0.sum(), m1.sum(), m2.sum()               # flux-weighted over the +-0.3'' pseudo-slit
        vb[x] = float(M1 / M0) / si
        sb[x] = float(max(M2 / M0 - (M1 / M0) ** 2, 0.0))
    key = np.round(g.aR / g.scale, 6)
    V = np.array([vb[k] for k in key])
    S = np.sqrt(sig ** 2 + np.array([sb[k] for k in key]))
    return V, S


# ================================================================================================ the frozen estimator
def fit_slope(lnR, lnVc2, w):
    """weighted LSQ of lnVc2 on lnR (rows = realisations): slope, intercept at the weighted mean, pivot, formal errors."""
    sw = w.sum(1)
    lb = (w * lnR).sum(1) / sw
    d = lnR[None, :] - lb[:, None]
    sxx = (w * d * d).sum(1)
    s = (w * d * lnVc2).sum(1) / sxx
    A = (w * lnVc2).sum(1) / sw
    return s, A, lb, 1.0 / np.sqrt(sxx), 1.0 / np.sqrt(sw)


def analyst(g, V, e_V, sig_win, i_an, presc="k2", mutate=False):
    """V (rows x markers), sig_win (rows), i_an in deg (rows) -> slope, g_obs and their errors; weights and pivot."""
    if mutate:
        V = V * (g.aR[None, :] / 1.0) ** 0.1
    P = C.pressure_term(g.aR[None, :], sig_win[:, None], g.Rd, presc, Reff=g.Reff)
    Vc2 = V * V + P
    Vc2 = np.maximum(Vc2, 1e-6)
    sl = 2.0 * np.abs(V) * e_V / Vc2
    w = 1.0 / np.maximum(sl, 1e-6) ** 2
    s, A, lb, es, eA = fit_slope(g.lnR, np.log(Vc2), w)
    # sigma_win uncertainty (numerical derivative, declared propagation)
    P2_ = C.pressure_term(g.aR[None, :], (sig_win * 1.01)[:, None], g.Rd, presc, Reff=g.Reff)
    s2, A2, _, _, _ = fit_slope(g.lnR, np.log(np.maximum(V * V + P2_, 1e-6)), w)
    rel = (g.sig_err_km / np.maximum(sig_win, 1.0)) if g.sig_err_km else 0.2
    ds_sig = (s2 - s) / 0.00995 * rel
    dA_sig = (A2 - A) / 0.00995 * rel
    fbar = (w * P / Vc2).sum(1) / w.sum(1)
    e_s = np.sqrt((F_INF * es) ** 2 + ds_sig ** 2)
    e_lng = np.sqrt((F_INF * eA) ** 2 + dA_sig ** 2 + (2.0 / np.tan(np.radians(i_an)) * math.radians(DI_DEG) * (1 - fbar)) ** 2)
    gobs = 1e6 * np.exp(A) / (np.exp(lb) * C.KPC)
    return dict(s=s, A=A, gobs=gobs, e_s=e_s, e_lng=e_lng, w=w, lb=lb, fbar=fbar)


def s_pred_grid(g, fit, ker, est, grid):
    """the predicted window slope on the Lambda grid (rows x grid): the same weighted fit applied to ln[Phi(y(R)) R]."""
    K = KER[ker]
    aG = A0C * 10 ** grid
    t = fit["gobs"][:, None] / aG[None, :]
    lnypiv = np.log(np.maximum(K.Phi_inv(t), 1e-300))
    Rpiv = np.exp(fit["lb"])
    if est == "PM":
        lnu = -2.0 * g.lnR
        lnupiv = -2.0 * fit["lb"]
    else:
        lnu = np.log(C.shape_unit(g.aR, g.Rd, MU_DECL, RG_DECL))
        lnupiv = np.log(C.shape_unit(Rpiv, g.Rd, MU_DECL, RG_DECL))
    w = fit["w"][:, None, :]
    wn = w / w.sum(2, keepdims=True)
    # the normalisation is matched to the fitted INTERCEPT A (the weighted mean of ln V_c^2), not to the curve at the pivot,
    # so the curvature of ln V_c^2 across the window cannot bias it: Newton iterations on ln y_piv
    target = fit["A"][:, None] - np.log(aG[None, :] * C.KPC / 1e6)          # weighted mean of ln[Phi(y) R] required
    for _ in range(6):
        lny = lnypiv[:, :, None] + (lnu[None, None, :] - lnupiv[:, None, None])
        if ker == "P2":
            y = np.exp(lny)
            lnPhi = 0.5 * (lny + np.log1p(y))
            D = (2 * y + 1) / (2 * (y + 1))
        else:
            lnPhi = np.interp(lny, K.lny, K.lnPhi)
            D = np.interp(lny, K.lny, K.dlnPhi)
        L = lnPhi + g.lnR[None, None, :]
        lnypiv = lnypiv + (target - (wn * L).sum(2)) / (wn * D).sum(2)
    lny = lnypiv[:, :, None] + (lnu[None, None, :] - lnupiv[:, None, None])
    if ker == "P2":
        lnPhi = 0.5 * (lny + np.log1p(np.exp(lny)))
    else:
        lnPhi = np.interp(lny, K.lny, K.lnPhi)
    L = lnPhi + g.lnR[None, None, :]
    d = g.lnR[None, None, :] - fit["lb"][:, None, None]
    return (w * d * L).sum(2) / (w * d * d).sum(2)


def stacked(fits, gals, ker, est):
    """common-a0 chi^2 on the grid; returns Lambda_hat, sigma (Delta chi2 = 1, inflated), edge flag, chi2_min, p, n."""
    def chi_on(grid):
        ch = np.zeros((NR_now, grid.size))
        for g, f in zip(gals, fits):
            sp = s_pred_grid(g, f, ker, est, grid)
            dsdl = -np.gradient(sp, grid * LN10, axis=1)       # d s_pred / d ln g_obs = - d s_pred / d ln a
            var = f["e_s"][:, None] ** 2 + (dsdl * f["e_lng"][:, None]) ** 2
            ch += (f["s"][:, None] - sp) ** 2 / var
        return ch
    chi = chi_on(GRID)
    n = len(gals)
    j = np.argmin(chi, axis=1)
    edge = (j == 0) | (j == GRID.size - 1)
    jj = np.clip(j, 1, GRID.size - 2)
    r = np.arange(chi.shape[0])
    c0, cm, cp = chi[r, jj], chi[r, jj - 1], chi[r, jj + 1]
    den = cm - 2 * c0 + cp
    off = np.where(den > 0, 0.5 * (cm - cp) / np.where(den > 0, den, 1), 0.0)
    lam = np.where(edge, GRID[j], GRID[jj] + np.clip(off, -1, 1) * 0.01)
    cmin = np.where(edge, chi[r, j], c0 - 0.25 * (cm - cp) * np.clip(off, -1, 1))
    sig = np.full(chi.shape[0], np.nan)
    for i in range(chi.shape[0]):
        if edge[i]:
            continue
        ci = chi[i] - cmin[i]
        lo = np.where(ci[: j[i]] > 1.0)[0]
        hi = np.where(ci[j[i]:] > 1.0)[0]
        if lo.size == 0 or hi.size == 0:
            edge[i] = True
            continue
        a1 = lo[-1]; b1 = j[i] + hi[0]
        xl = GRID[a1] + (1.0 - ci[a1]) * (GRID[a1 + 1] - GRID[a1]) / (ci[a1 + 1] - ci[a1])
        xh = GRID[b1 - 1] + (1.0 - ci[b1 - 1]) * (GRID[b1] - GRID[b1 - 1]) / (ci[b1] - ci[b1 - 1])
        sig[i] = 0.5 * (xh - xl)
    if NR_now == 1 and not edge[0]:                            # noise-free controls: refine the minimum on a fine local grid
        fine = lam[0] + np.arange(-0.02, 0.02 + 1e-12, 1e-4)
        cf = chi_on(fine)[0]
        lam = np.array([fine[int(np.argmin(cf))]])
        cmin = np.array([float(cf.min())])
    dof = max(n - 1, 1)
    infl = np.sqrt(np.maximum(1.0, cmin / dof))
    p = CHI2.sf(cmin, dof)
    return dict(lam=lam, sig=sig * infl, edge=edge, cmin=cmin, p=p, n=n)


# ================================================================================================ one mock cell
BS_PRIMARY = (FWHM0, BIN0)
BASE = dict(sample="ten", window="primary", ker="P2", mu=0.67, rg=2.0, presc_true="k2", presc_an="k2", sigma=45.0,
            bs=BS_PRIMARY, inc_true="sfr", w=6, noise=True, newton=False, point=False, di=True, extend=None, fwhm_win=FWHM0)
GAL_CACHE = {}


def gals_for(cfg):
    key = (cfg["sample"], cfg["window"], cfg["extend"], cfg["fwhm_win"])
    if key not in GAL_CACHE:
        if cfg["sample"] == "ten":
            ids = TEN
        elif cfg["sample"] == "ten_no21":
            ids = [k for k in TEN if k != 21]
        elif cfg["sample"] == "all22":
            ids = [k for k in sorted(integ) if k not in STAR]
        else:
            raise ValueError(cfg["sample"])
        GAL_CACHE[key] = [Gal(k, cfg["window"], cfg["extend"], cfg["fwhm_win"]) for k in ids]
    return GAL_CACHE[key]


NR_now = NR


def run_cell(cfg, law, seed):
    global NR_now
    rng = np.random.default_rng(seed)
    NR_now = NR if cfg["noise"] else 1
    gals_all = [g for g in gals_for(cfg) if g.ok_radii]
    used, fits_by_est, dropped_pts, total_pts, s_ge0 = [], [], 0, 0, 0
    fits = []
    for g in gals_all:
        Vc2 = truth_Vc2(g, law, cfg["ker"], cfg["mu"], cfg["rg"], cfg["newton"], cfg["point"])
        Pt = C.pressure_term(RT, cfg["sigma"], g.Rd, cfg["presc_true"], Reff=g.Reff)
        Vrot2 = Vc2 - Pt
        Vrot = np.sqrt(np.maximum(Vrot2, 0.0))
        inc_t = g.inc[cfg["inc_true"]]
        V_bs, S_obs = forward(g, Vrot, cfg["sigma"], inc_t, cfg["bs"])
        keep = np.interp(g.aR, RT, Vrot2) >= 0.1 * np.interp(g.aR, RT, Vc2)
        total_pts += g.R.size
        dropped_pts += int((~keep).sum())
        if keep.sum() < 5 or (g.lnR[keep].max() - g.lnR[keep].min()) < 0.25:
            continue
        # a reduced galaxy view with the kept markers
        h = Gal.__new__(Gal)
        h.__dict__.update(g.__dict__)
        h.R, h.e, h.aR, h.lnR = g.R[keep], g.e[keep], g.aR[keep], g.lnR[keep]
        V_bs, S_obs = V_bs[keep], S_obs[keep]
        si_t = math.sin(math.radians(inc_t))
        vlos = np.sign(h.R) * V_bs * si_t
        n = h.R.size
        if cfg["noise"]:
            noise = np.zeros((NR_now, n))
            for sgn in (+1, -1):
                idx = np.where(np.sign(h.R) == sgn)[0]
                if idx.size == 0:
                    continue
                wv = cfg["w"]
                z = rng.standard_normal((NR_now, idx.size + wv - 1))
                cs = np.cumsum(np.concatenate([np.zeros((NR_now, 1)), z], axis=1), axis=1)
                noise[:, idx] = (cs[:, wv:] - cs[:, :-wv]) / math.sqrt(wv)
            vobs = vlos[None, :] + h.e[None, :] * noise
            sw_true = float(np.mean(S_obs))
            rel = (h.sig_err_km / sw_true) if h.sig_err_km else 0.2
            sig_win = sw_true * (1.0 + rel * rng.standard_normal(NR_now))
            i_an = np.clip(g.inc["sfr"] + (DI_DEG * rng.standard_normal(NR_now) if cfg["di"] else 0.0), 12.0, 89.0)
        else:
            vobs = vlos[None, :]
            sig_win = np.array([float(np.mean(S_obs))])
            i_an = np.array([g.inc["sfr"] if cfg["inc_true"] == "sfr" else g.inc["sfr"]])
        V = vobs * np.sign(h.R)[None, :] / np.sin(np.radians(i_an))[:, None]
        e_V = h.e[None, :] / np.sin(np.radians(i_an))[:, None]
        f = analyst(h, V, e_V, sig_win, i_an, cfg["presc_an"], mutate=MUT)
        s_ge0 += int((f["s"] >= 0).sum())
        used.append(h)
        fits.append(f)
    out = dict(n_gal=len(used), frac_dropped=dropped_pts / max(total_pts, 1),
               frac_s_ge0=s_ge0 / max(1, NR_now * len(used)), zmed=float(np.median([g.z for g in used])) if used else float("nan"))
    if len(used) < 3:
        out["fail"] = True
        return out
    for est in ("DS", "PM"):
        st = stacked(fits, used, cfg["ker"], est)
        good = ~st["edge"]
        out[est] = dict(
            mean=float(np.mean(st["lam"][good])) if good.any() else float("nan"),
            sd=float(np.std(st["lam"][good])) if good.sum() > 1 else float("nan"),
            med_sig=float(np.nanmedian(st["sig"][good])) if good.any() else float("nan"),
            frac_edge=float(np.mean(st["edge"])), frac_upper_edge=float(np.mean(st["edge"] & (st["lam"] > 0))),
            frac_reject=float(np.mean(st["p"] < 0.01)), med_chi2dof=float(np.median(st["cmin"] / max(st["n"] - 1, 1))),
            lam=st["lam"], sig=st["sig"], edge=st["edge"], p=st["p"])
    return out


def cfgp(**kw):
    c = dict(BASE)
    c.update(kw)
    return c


def lam_R(zmed):
    return math.log10(float(C.E(zmed)))


def fmt_est(o, est):
    if o.get("fail"):
        return "   (fewer than 3 discs survive)"
    q = o[est]
    return (f"mean {q['mean']:+.3f}  sd {q['sd']:.3f}  med sigma {q['med_sig']:.3f}  edge {q['frac_edge']:.2f}  "
            f"reject {q['frac_reject']:.2f}  chi2/dof {q['med_chi2dof']:.2f}")


RES = {}


def run(name, cfg, seed):
    RES[name] = {law: run_cell(cfg, law, seed + (0 if law == "flat" else 7919)) for law in ("flat", "rival")}
    return RES[name]


def show(name):
    o = RES[name]
    zm = o["flat"].get("zmed", float("nan"))
    for law in ("flat", "rival"):
        q = o[law]
        print(f"   {name:26s} {law:5s} n_disc {q['n_gal']:2d}  dropped {q['frac_dropped']:.2f} | DS {fmt_est(q, 'DS')}")
        if not q.get("fail"):
            print(f"   {'':26s} {'':5s} {'':18s}| PM {fmt_est(q, 'PM')}   (s>=0 per-disc {q['frac_s_ge0']:.2f})")


# ================================================================================================ geometry summary
T.banner("G  the mock discs: catalogue values, windows and marker counts (radii and error bars only)")
print(f"  primary sample: the ten f_DM discs {TEN};  '*'-flagged rows in the f_DM/kinematics tables: {sorted(STAR)}")
print("   id   z      logM*  R_d   FWHM_kpc  R_in   n_win  lnR span  med e_los  sigma-mean err (km/s)")
geo = []
for g in gals_for(BASE):
    geo.append(dict(id=g.id, z=g.z, Rd=g.Rd, fwhm_kpc=g.fwhm_kpc, Rin=g.Rin, n=int(g.R.size),
                    span=float(g.lnR.max() - g.lnR.min()) if g.R.size else 0.0, ok=g.ok_radii))
    print(f"   {g.id:3d} {g.z:.3f}  {math.log10(g.Ms):5.2f}  {g.Rd:4.2f}  {g.fwhm_kpc:5.2f}    {g.Rin:5.2f}  {g.R.size:3d}    "
          f"{(g.lnR.max() - g.lnR.min()) if g.R.size else 0:.2f}     {np.median(g.e) if g.R.size else float('nan'):5.1f}      "
          f"{g.sig_err_km if g.sig_err_km else float('nan'):.1f}   {'' if g.ok_radii else 'EXCLUDED (radius rule)'}")
T.numbers["geometry"] = geo
zmed10 = float(np.median([g.z for g in gals_for(BASE)]))
print(f"  sample median z = {zmed10:.3f}: rival - flat = log10 E = {lam_R(zmed10):+.4f} dex")

# ================================================================================================ controls
T.banner("C  controls (noise-free unless stated)")
c1 = run("C1_pointmass_noiseless", cfgp(point=True, presc_true="none", presc_an="none", bs=None, noise=False, di=False), 11)
e1 = [c1[l]["PM"]["lam"][0] - (0.0 if l == "flat" else math.log10(float(C.E(c1[l]["zmed"])))) for l in ("flat", "rival")]
T.check("C1 CONTROL: a noise-free POINT-MASS mock (no pressure, no smearing) is recovered by the PM estimator (|dLambda| < 2e-3 dex)",
        f"flat {e1[0]:+.1e}, rival (vs log10 E(z_med)) {e1[1]:+.1e} dex -- the rival's per-disc E(z_i) spread makes the rival residual "
        f"non-zero by construction; flat is the exact test", abs(e1[0]) < 2e-3)
c1b = run("C1b_disc_declared_noiseless", cfgp(presc_true="none", presc_an="none", bs=None, noise=False, di=False), 12)
e1b = c1b["flat"]["DS"]["lam"][0]
T.check("C1b CONTROL: a noise-free DISC mock with the declared shape (mu 0.67, R_gas 2 R_d) is recovered by the DS estimator "
        "(|dLambda| < 2e-3 dex)", f"flat {e1b:+.1e} dex; the PM estimator on the same mock gives {c1b['flat']['PM']['lam'][0]:+.3f} "
        f"(edge {bool(c1b['flat']['PM']['edge'][0])})", abs(e1b) < 2e-3)
c2 = run("C2_newton_noiseless", cfgp(point=True, newton=True, presc_true="none", presc_an="none", bs=None, noise=False, di=False), 13)
lamN = c2["flat"]["PM"]["lam"][0]
T.check("C2 CONTROL: a pure-Newtonian point-mass mock gives s = -1, y -> infinity, i.e. only an UPPER limit on a0: the PM stack sits "
        "at the grid's lower edge (Lambda <= -1.49)", f"Lambda_hat {lamN:+.3f}, edge {bool(c2['flat']['PM']['edge'][0])}",
        lamN <= -1.49 and bool(c2['flat']['PM']['edge'][0]))
c2b = run("C2b_newton_disc_noiseless", cfgp(newton=True, presc_true="none", presc_an="none", bs=None, noise=False, di=False), 14)
print(f"  reported: a pure-Newtonian DISC mock (declared shape) -> DS Lambda_hat {c2b['flat']['DS']['lam'][0]:+.3f} "
      f"(edge {bool(c2b['flat']['DS']['edge'][0])}); PM Lambda_hat {c2b['flat']['PM']['lam'][0]:+.3f} "
      f"(edge {bool(c2b['flat']['PM']['edge'][0])}): the point-mass form reads a spurious finite a0 off a Newtonian disc")
T.numbers["C2b_newton_disc"] = dict(DS=c2b["flat"]["DS"]["lam"][0], PM=c2b["flat"]["PM"]["lam"][0])

# ================================================================================================ beam-smearing diagnostic
T.banner("B  what seeing does to the SLOPE: noise-free, no pressure, flat law, declared shape; the frozen window")
print("  ds_bs = slope of ln V_bs^2 minus slope of ln V_c^2 over each disc's frozen window (smearing only; the pressure term is off)")
BSCFG = (("primary: FWHM 0.57'', bin 0.6'', H-alpha R_d", (0.57, 0.6, 1.0)),
         ("bin 0.1'' (no adaptive binning)", (0.57, 0.1, 1.0)),
         ("bin 0.1'', H-alpha 1.5 R_d (optimistic)", (0.57, 0.1, 1.5)),
         ("pessimistic: FWHM 0.82'', bin 0.9''", (0.82, 0.9, 1.0)),
         ("AO-like: FWHM 0.15'', bin 0.15''", (0.15, 0.15, 1.0)))
BSD = {}
for label, bs in BSCFG:
    vals = []
    for g in [g for g in gals_for(BASE) if g.ok_radii]:
        Vc2 = truth_Vc2(g, "flat", "P2", MU_DECL, RG_DECL)
        Vb, _ = forward(g, np.sqrt(Vc2), 0.0, g.inc["sfr"], bs)
        st = np.polyfit(g.lnR, np.log(np.interp(g.aR, RT, Vc2)), 1)[0]
        sb = np.polyfit(g.lnR, np.log(Vb ** 2), 1)[0]
        vals.append(float(sb - st))
    BSD[label] = vals
    print(f"   {label:42s}: per disc " + " ".join(f"{v:+.2f}" for v in vals) + f" | mean {np.mean(vals):+.3f}")
T.numbers["beam_smearing_slope_bias"] = BSD
print("  (compare: a coherent slope error of about +0.1 equals the whole flat -> rival separation; CFG250_slope_theory T5)")

# ================================================================================================ the frozen primary, seeing-limited
T.banner("P  the FROZEN primary on seeing-limited mocks: truth k = 2 (matched), declared shape, sigma 45 km/s, smearing 0.57''/0.6'', "
         "noise correlated over 6 markers, +-5 deg inclination error")
print(f"  N = {NR} realisations per law per cell; Lambda = log10(a0_hat / 9.3603e-11); flat 0, rival {lam_R(zmed10):+.3f}")
run("P_primary", cfgp(), 22)
run("P_bs_optimistic", cfgp(bs=(0.57, 0.1, 1.5)), 23)
run("P_bs_pessimistic", cfgp(bs=(0.82, 0.9, 1.0)), 24)
run("P_sigma20", cfgp(sigma=20.0), 25)
run("P_window_1.5fwhm", cfgp(window="1.5fwhm"), 26)
for nm in ("P_primary", "P_bs_optimistic", "P_bs_pessimistic", "P_sigma20", "P_window_1.5fwhm"):
    show(nm)
pp = RES["P_primary"]
sl_fail = {law: pp[law]["DS"]["frac_edge"] + (1 - pp[law]["DS"]["frac_edge"]) * pp[law]["DS"]["frac_reject"] for law in ("flat", "rival")}

# ================================================================================================ the ideal (smearing-free) track
T.banner("I  the SMEARING-FREE track (bs = None: the limit an AO or forward-modelled analysis would approach); the analyst is "
         "otherwise the frozen primary")
BI = dict(bs=None)
run("I_matched", cfgp(**BI), 31)
show("I_matched")
m = RES["I_matched"]["flat"]["DS"]
T.check("C3 RECOVERY [MUTATE must fail it]: smearing-free matched mock, flat truth: the DS stack is unbiased, "
        "|mean Lambda_hat| < 0.25 x sd", f"mean {m['mean']:+.3f}, sd {m['sd']:.3f}", abs(m["mean"]) < 0.25 * m["sd"])
cov = m["sd"] / m["med_sig"]
T.check("C4 COVERAGE: smearing-free matched cell, flat truth: the scatter of Lambda_hat over mocks agrees with the median reported "
        "sigma within a factor [0.67, 1.5] (reported: made non-load-bearing after the first mock run, disclosed in the README)",
        f"sd/median sigma = {cov:.2f} (sd {m['sd']:.3f}, median sigma {m['med_sig']:.3f}); below 1 = the reported sigma is conservative",
        0.67 <= cov <= 1.5, load_bearing=False)

AX_A = ("k1", "k2", "K21x0.6", "K21x1", "K21x1.4")
SIGS = (20.0, 30.0, 45.0, 60.0)
SHAPES_B = ((0.25, 2.0), (1.5, 2.0), (4.0, 2.0), (0.67, 1.0), (0.67, 3.0))
seed = 100
for sg in SIGS:
    for pt in AX_A:
        seed += 1
        run(f"A_{pt}_s{int(sg)}", cfgp(presc_true=pt, sigma=sg, **BI), seed)
run("A_none_s45", cfgp(presc_true="none", **BI), 190)
for mu, rg in SHAPES_B:
    seed += 1
    run(f"B_mu{mu}_rg{rg}", cfgp(mu=mu, rg=rg, **BI), seed)
run("D_inc_star_truth", cfgp(inc_true="star", **BI), 202)
print("\n  axis A (pressure truth; analyst k = 2), per sigma:")
for sg in SIGS:
    for pt in AX_A:
        show(f"A_{pt}_s{int(sg)}")
print("  scenario: no pressure support at all (truth 'none', analyst k = 2), sigma 45:")
show("A_none_s45")
print("  axis B (baryon shape truth; DS declares mu 0.67, R_gas 2 R_d):")
for mu, rg in SHAPES_B:
    show(f"B_mu{mu}_rg{rg}")
print("  axis D (truth inclination = i*, analyst i_SFR):")
show("D_inc_star_truth")


def half_spread(names, est):
    out = {}
    for law in ("flat", "rival"):
        vals = [RES[n][law][est]["mean"] for n in names if not RES[n][law].get("fail") and np.isfinite(RES[n][law][est]["mean"])]
        out[law] = 0.5 * (max(vals) - min(vals)) if len(vals) > 1 else float("nan")
    return max(out["flat"], out["rival"]), out


def n_finite(names, est):
    return sum(1 for n in names for law in ("flat", "rival")
               if not RES[n][law].get("fail") and np.isfinite(RES[n][law][est]["mean"]))


SYS = {}
for est in ("DS", "PM"):
    SYS[est] = {}
    for sg in SIGS:
        nms = [f"A_{pt}_s{int(sg)}" for pt in AX_A]
        SYS[est][f"A_s{int(sg)}"] = half_spread(nms, est)[0]
        SYS[est][f"A_s{int(sg)}_nfinite"] = n_finite(nms, est)
    nmsB = ["A_k2_s45"] + [f"B_mu{mu}_rg{rg}" for mu, rg in SHAPES_B]
    SYS[est]["B"] = half_spread(nmsB, est)[0]
    SYS[est]["B_nfinite"] = n_finite(nmsB, est)
    SYS[est]["D"] = half_spread(["A_k2_s45", "D_inc_star_truth"], est)[0]
    SYS[est]["total"] = {int(sg): math.sqrt(SYS[est][f"A_s{int(sg)}"] ** 2 + SYS[est]["B"] ** 2 + SYS[est]["D"] ** 2)
                         for sg in SIGS}
T.numbers["sigma_sys_smearing_free"] = SYS
print("\n  sigma_sys (smearing-free track) = quadrature sum over the axes of half the spread of the mock-mean Lambda_hat "
      "(the larger of flat/rival; 'nan' = fewer than two finite cells):")
for est in ("DS", "PM"):
    print(f"   {est}: A (pressure) " + ", ".join(f"sigma {sg:.0f}: {SYS[est][f'A_s{int(sg)}']:.3f} ({SYS[est][f'A_s{int(sg)}_nfinite']}/10 finite)"
                                          for sg in SIGS)
          + f" | B (shape) {SYS[est]['B']:.3f} ({SYS[est]['B_nfinite']}/12) | D (inclination) {SYS[est]['D']:.3f}")
    print(f"       total: " + ", ".join(f"sigma {sg}: {v:.3f} dex" for sg, v in SYS[est]["total"].items()))

# ================================================================================================ separation and the decision rule
T.banner("H  expected separation between the laws, and the frozen decision rule on mocks")


def separation(name, est, sig_sys):
    o = RES[name]
    if o["flat"].get("fail") or o["rival"].get("fail"):
        return None
    f, r = o["flat"][est], o["rival"][est]
    if not (np.isfinite(f["mean"]) and np.isfinite(r["mean"]) and np.isfinite(f["sd"]) and np.isfinite(r["sd"])):
        return None
    d = r["mean"] - f["mean"]
    sst = math.sqrt(0.5 * (f["sd"] ** 2 + r["sd"] ** 2))
    sig_sys = sig_sys if np.isfinite(sig_sys) else 0.0
    return dict(delta=d, s_stat=d / sst, s_tot=d / math.sqrt(sst ** 2 + sig_sys ** 2), sd=sst, sig_sys=sig_sys,
                bias_flat=f["mean"], bias_rival=r["mean"] - lam_R(o["flat"]["zmed"]),
                usable_flat=1 - f["frac_edge"], usable_rival=1 - r["frac_edge"])


def classify(lam, sig, edge, p, sig_sys, zmed):
    lr = lam_R(zmed)
    st = np.sqrt(np.nan_to_num(sig, nan=1e9) ** 2 + (sig_sys if np.isfinite(sig_sys) else 0.0) ** 2)
    zf, zr = lam / st, (lam - lr) / st
    cls = np.where((np.abs(zf) <= 2) & (np.abs(zr) > 2), "lean flat",
                   np.where((np.abs(zr) <= 2) & (np.abs(zf) > 2), "lean rival",
                            np.where((np.abs(zf) <= 2) & (np.abs(zr) <= 2), "both allowed", "neither")))
    cls = np.where(edge | (p < 0.01), "non-diag (limit or model rejected)", cls)
    return cls


KEYS = ("lean flat", "lean rival", "both allowed", "neither", "non-diag (limit or model rejected)")


def class_freq(names, law, est, sig_sys):
    allc = []
    for nm in names:
        q = RES[nm][law]
        if q.get("fail"):
            continue
        allc.append(classify(q[est]["lam"], q[est]["sig"], q[est]["edge"], q[est]["p"], sig_sys, zmed10))
    cc = np.concatenate(allc) if allc else np.array([])
    return {k: float(np.mean(cc == k)) if cc.size else float("nan") for k in KEYS}


SEP = {}
sp_sl = separation("P_primary", "DS", SYS["DS"]["total"][45])
SEP["seeing_limited_primary_DS"] = sp_sl
print("  (1) the FROZEN primary, seeing-limited (P_primary):")
for law in ("flat", "rival"):
    q = pp[law]["DS"]
    print(f"      {law:5s} truth: DS stack at a grid edge (a0 limit) in {q['frac_edge']:.2f} of mocks, model rejected (p < 0.01) in "
          f"{q['frac_reject']:.2f}; median chi2/dof {q['med_chi2dof']:.1f}")
DEC = {}
for law in ("flat", "rival"):
    DEC[f"seeing-limited primary | {law} truth"] = class_freq(["P_primary"], law, "DS", SYS["DS"]["total"][45])
    print(f"      decision rule, {law} truth: " + "; ".join(f"{k} {v:.2f}" for k, v in DEC[f'seeing-limited primary | {law} truth'].items()))
print("\n  (2) the smearing-free track (truth k = 2 matched), per sigma:")
for est in ("DS", "PM"):
    for sg in SIGS:
        sp_ = separation(f"A_k2_s{int(sg)}", est, SYS[est]["total"][int(sg)])
        SEP[f"smearing_free_{est}_s{int(sg)}"] = sp_
        if sp_ is None:
            print(f"   {est} sigma {sg:4.0f}: no finite separation (a stack at a grid edge / too few discs under one law)")
            continue
        print(f"   {est} sigma {sg:4.0f}: rival - flat = {sp_['delta']:+.3f} dex (expected {lam_R(zmed10):+.3f}); flat bias "
              f"{sp_['bias_flat']:+.3f}, rival bias {sp_['bias_rival']:+.3f}; usable {sp_['usable_flat']:.2f}/{sp_['usable_rival']:.2f}; "
              f"S_stat {sp_['s_stat']:.2f}; S_tot (sigma_sys {sp_['sig_sys']:.3f}) {sp_['s_tot']:.2f}")
T.numbers["separation"] = SEP
print("\n  (3) the frozen decision rule on smearing-free mocks (DS, sigma 45):")
for label, names in (("smearing-free, truth k = 2, declared shape", ["A_k2_s45"]),
                     ("smearing-free, marginal over axes A and B", [f"A_{pt}_s45" for pt in AX_A] + [f"B_mu{mu}_rg{rg}" for mu, rg in SHAPES_B])):
    for law in ("flat", "rival"):
        DEC[f"{label} | {law} truth"] = class_freq(names, law, "DS", SYS["DS"]["total"][45])
        print(f"   {label}, {law} truth: " + "; ".join(f"{k} {v:.2f}" for k, v in DEC[f'{label} | {law} truth'].items()))
T.numbers["decision_rule_DS"] = DEC
pf_bad = DEC["smearing-free, marginal over axes A and B | flat truth"]["lean rival"]
pr_bad = DEC["smearing-free, marginal over axes A and B | rival truth"]["lean flat"]

# ================================================================================================ variants and remedies
T.banner("V  variants of the smearing-free track (reported) and what would make the test work")
for nm, kw, sd in (("V_noise_w1", dict(w=1), 301), ("V_noise_w9", dict(w=9), 302), ("V_window_3Rd", dict(window="3Rd"), 303),
                   ("V_window_2Rd_nobeamguard", dict(window="2Rd"), 304), ("V_sample_no21", dict(sample="ten_no21"), 305),
                   ("V_sample_all22", dict(sample="all22"), 306), ("V_kernel_nu_mono", dict(ker="nu_mono"), 307)):
    run(nm, cfgp(**BI, **kw), sd)
    show(nm)
    q = RES[nm]["flat"]
    if not q.get("fail") and np.isfinite(q["DS"]["sd"]) and np.isfinite(q["DS"]["med_sig"]):
        print(f"   {'':26s} coverage sd/med sigma = {q['DS']['sd'] / q['DS']['med_sig']:.2f}")
print("\n  remedies (on top of the smearing-free track unless stated):")
for pt in AX_A:
    run(f"X1A_{pt}", cfgp(sigma=10.0, presc_true=pt, **BI), 410 + AX_A.index(pt))
run("X2_AO_psf0.15_forward_modelled", cfgp(bs=(0.15, 0.15, 1.0), w=2, fwhm_win=0.15), 402)
run("X4_radii_to_10Rd", cfgp(extend=10.0, **BI), 404)
run("X14_cold_radii_to_10Rd", cfgp(sigma=10.0, extend=10.0, **BI), 408)
run("X2c_AO_cold", cfgp(sigma=10.0, bs=(0.15, 0.15, 1.0), w=2, fwhm_win=0.15), 409)
for nm in ("X1A_k2", "X2_AO_psf0.15_forward_modelled", "X4_radii_to_10Rd", "X14_cold_radii_to_10Rd", "X2c_AO_cold"):
    show(nm)
sysA10 = half_spread([f"X1A_{pt}" for pt in AX_A], "DS")[0]
bsAO = abs(float(np.mean(BSD["AO-like: FWHM 0.15'', bin 0.15''"])))
B_, D_ = SYS["DS"]["B"], SYS["DS"]["D"]
REM = {}
for nm, sig_sys, note in (
        ("A_k2_s45", SYS["DS"]["total"][45], "smearing-free, sigma 45 (pressure + shape + inclination systematics)"),
        ("X1A_k2", math.sqrt(sysA10 ** 2 + B_ ** 2 + D_ ** 2), "cold tracer sigma 10 km/s (pressure axis re-run at sigma 10)"),
        ("X1A_k2", math.sqrt(sysA10 ** 2 + D_ ** 2), "cold tracer AND the gas shape measured (shape axis removed)"),
        ("X2_AO_psf0.15_forward_modelled", math.sqrt(SYS["DS"]["total"][45] ** 2), "AO-like PSF 0.15'' through the forward model, sigma 45"),
        ("X2c_AO_cold", math.sqrt(sysA10 ** 2 + D_ ** 2), "AO-like PSF, cold tracer, gas shape measured"),
        ("X4_radii_to_10Rd", SYS["DS"]["total"][45], "markers continued to 10 R_d (twice the median error), sigma 45"),
        ("X14_cold_radii_to_10Rd", math.sqrt(sysA10 ** 2 + D_ ** 2), "cold tracer, gas shape measured, radii to 10 R_d")):
    sp_ = separation(nm, "DS", sig_sys)
    key = nm + (" (shape measured)" if "shape measured" in note and nm == "X1A_k2" else "")
    REM[key] = dict(note=note, **(sp_ or {"sig_sys": sig_sys}))
    if sp_ is None:
        print(f"   {key:40s}: no finite separation")
        continue
    print(f"   {key:40s} S_stat {sp_['s_stat']:5.2f}  sigma_sys {sig_sys:.3f}  S_tot {sp_['s_tot']:5.2f}  "
          f"(flat bias {sp_['bias_flat']:+.3f}, rival bias {sp_['bias_rival']:+.3f})  -- {note}")
T.numbers["remedies_DS"] = REM
print("   (a sample three times larger scales S_stat by sqrt 3 = 1.73 and leaves sigma_sys unchanged)")

# ================================================================================================ verdict
T.banner("R  pre-flight reading")
H0 = sp_sl is not None and sp_sl["s_tot"] >= 2.0 and max(sl_fail.values()) < 0.5
sfree = SEP.get("smearing_free_DS_s45")
T.numbers["H0"] = dict(seeing_limited_S_tot=sp_sl["s_tot"] if sp_sl else None, seeing_limited_unusable=sl_fail, passes=H0,
                       smearing_free_S_stat=sfree["s_stat"] if sfree else None, smearing_free_S_tot=sfree["s_tot"] if sfree else None,
                       P_lean_rival_given_flat_marginal=pf_bad, P_lean_flat_given_rival_marginal=pr_bad)
sl_st = "n/a" if sp_sl is None else f"{sp_sl['s_tot']:.2f}"
sf_st = "n/a" if sfree is None else f"{sfree['s_stat']:.2f}"
sf_tt = "n/a" if sfree is None else f"{sfree['s_tot']:.2f}"
T.check("H0 FEASIBILITY (the frozen gate; reported, not an exit-code check): on seeing-limited KURVS-like mocks (sigma 45) the frozen "
        "primary returns a usable stack (edge or rejected in < 50%) AND separates the laws by >= 2 sigma including sigma_sys",
        f"unusable fraction flat {sl_fail['flat']:.2f}, rival {sl_fail['rival']:.2f}; S_tot {sl_st}; smearing-free S_stat {sf_st}, "
        f"S_tot {sf_tt}; P(lean rival | flat truth, smearing-free marginal) {pf_bad:.2f}", H0, load_bearing=False)
print(f"\n  wall time {time.time() - T0:.0f} s")
rc = T.finish()
sys.exit(rc)
