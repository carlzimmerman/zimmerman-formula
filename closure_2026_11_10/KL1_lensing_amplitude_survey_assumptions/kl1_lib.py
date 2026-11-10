#!/usr/bin/env python3
"""KL1 (FROZEN_CRITERIA.md 99a42c78ef) shared library: CO2's shear path (co2_shear.py above its response section, executed
unchanged, which executes CFG592's library part unchanged), KL1's copy of CFG592's fit (alignment variants, a replaced inverse
covariance), the scan rule, and the Gaussian covariance at the model (row A2).
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize
from scipy.special import j0, jv
from scipy.stats import chi2 as CH
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO2 = os.path.join(REPO, "closure_2026_11_09", "CO2_form_b_amplitude_pinned")
_src = open(os.path.join(CO2, "co2_shear.py")).read(); _cut = _src.index("# ------------------------------------------------------------------ the response and KA5")
NS = {"__file__": os.path.join(CO2, "co2_shear.py"), "__name__": "co2_shear_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "co2_shear.py", "exec"), NS)      # CFG592 library, S0 nodes, response, run_of, fitp, lab, DS
G, K, SN, HM, ROWS, CO1S, SURV, DS, ONE, BASE, KH, S0J = (NS[k] for k in ("G", "K", "SN", "HM", "ROWS", "CO1S", "SURV", "DS", "ONE", "BASE", "KH", "S0J"))
Pmat, run_of, support_mask, subset, lab, S8E = (NS[k] for k in ("Pmat", "run_of", "support_mask", "subset", "lab", "S8E"))
PZ0 = {z: p.copy() for z, p in NS["PZ"].items()}
FOOTS = ("canonical", "alt")
def setP(pz): NS["PZ"].update({z: np.asarray(v, float).copy() for z, v in pz.items()})

# ------------------------------------------------------------------ KL1's copy of CFG592's fit (identical when nothing is replaced)
def nuis(S, widen, ia):
    if S["name"] == "KiDS" and ia == "eta":
        mu = S["mu_u"]; x0 = np.r_[mu, 0.5, 0.0]; lo = np.r_[mu - 5 * widen, -6.0, -5.0]; hi = np.r_[mu + 5 * widen, 6.0, 5.0]
        unpack = lambda x: dict(dz=S["L"] @ x[:5], A=float(x[5]), eta=float(x[6]))
        prior = lambda x: float(np.sum(((x[:5] - mu) / widen) ** 2))
        return x0, lo, hi, unpack, prior, [x0, np.r_[mu, -0.5, 0.0]]
    on = ia != "off"; x0, lo, hi, unpack, prior = G["nuis_spec"](S, widen, on)
    starts = [x0] + ([np.r_[x0[:-2], -0.5, 0.0] if S["name"] == "DES" else np.r_[x0[:-1], -0.5]] if on else [])
    return x0, lo, hi, unpack, prior, starts
def fit(S, D, Pm, widen=1.0, ia="nla", Cinv=None, bg="PM"):
    x0, lo, hi, unpack, prior, starts = nuis(S, widen, ia); d = D["d"]; Ci = D["Cinv"] if Cinv is None else Cinv
    def f(x):
        r = d - G["theory"](S, D, unpack(x), Pm, bg); return float(r @ Ci @ r) + prior(x)
    best = None
    for xs in starts:
        r = minimize(f, xs, method="L-BFGS-B", bounds=[(a, b) for a, b in zip(lo, hi)], options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
        if best is None or r.fun < best.fun: best = r
    par = unpack(best.x); t = G["theory"](S, D, par, Pm, bg); r_ = d - t; c2d = float(r_ @ Ci @ r_)
    out = dict(chi2=float(best.fun), chi2_data=c2d, N=D["N"], p=float(CH.sf(c2d, D["N"])), A_IA=par["A"], x=[float(v) for v in best.x])
    out["label"] = lab(out["p"])
    if S["name"] == "KiDS": out["dz_pulls"] = [float(v) for v in (best.x[:5] - S["mu_u"]) / widen]
    if "eta" in par: out["eta"] = par["eta"]
    return out

# ------------------------------------------------------------------ point selections
RUN1 = run_of(ONE); PS0 = Pmat(RUN1, "S0")
SUP = {sn: support_mask(S, RUN1, PS0) for sn, S in SURV.items()}
_run_half = dict(RUN1, k_hi=RUN1["k_hi"] / 2.0)
SUP_HALF = {sn: support_mask(S, _run_half, PS0) for sn, S in SURV.items()}
def keep_mask(sn, thr=0.9, khalf=False):
    S = SURV[sn]; return S["pubkeep"] & ((SUP_HALF if khalf else SUP)[sn] >= thr)
def dsub(sn, thr=0.9, khalf=False): return subset(SURV[sn], keep_mask(sn, thr, khalf))

# ------------------------------------------------------------------ the Gaussian covariance at a model (row A2)
ARC = math.pi / (180 * 60)
LF, DLF, TAPER, MI, LN = (G[k] for k in ("LF", "DLF", "TAPER", "MI", "LN"))
WL = LF * DLF * TAPER / (2 * math.pi)                       # / A applied later
def _jbar(S, nsub=40):
    Jp, Jm, Om = [], [], []
    for lo, hi in S["edges"]:
        th = np.linspace(lo, hi, nsub) * ARC; wt = th / th.sum(); x = LF[None, :] * th[:, None]
        Jp.append((wt[:, None] * j0(x)).sum(0)); Jm.append((wt[:, None] * jv(4, x)).sum(0)); Om.append(math.pi * ((hi * ARC) ** 2 - (lo * ARC) ** 2))
    return np.array(Jp), np.array(Jm), np.array(Om)
def _noise_meta(S):
    import astropy.io.fits as fits
    if S["name"] == "KiDS":
        import glob
        fn = glob.glob(os.path.join(G["WORK"], "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]; h = fits.open(fn)["NZ_SOURCE"].header
    else:
        h = fits.open(os.path.join(G["WORK"], "2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits"))["nz_source"].header
    nb = S["nbin"]; sig = np.array([h[f"SIG_E_{i+1}"] for i in range(nb)], float); ng = np.array([h[f"NGAL_{i+1}"] for i in range(nb)], float)
    return sig, ng
for _S in SURV.values():
    _S["Jp_raw"], _S["Jm_raw"], _S["Om_bin"] = _jbar(_S); _S["sig_e"], _S["ngal"] = _noise_meta(_S)
def cell_full(S, Pm):
    """symmetric [nb, nb, LF] C_ell at nominal delta-z, no alignment (as the support mask's nominal nuisances)."""
    x0, _, _, unpack, _ = G["nuis_spec"](S, 1.0, False); par = unpack(x0)
    Cp = G["C_ell"](S, par, Pm, "PM")                         # [npair, LN]
    CL = Cp @ MI.T                                             # [npair, LF]
    nb = S["nbin"]; C = np.zeros((nb, nb, len(LF)))
    for n, (a, b) in enumerate(S["pairs"]): C[a - 1, b - 1] = CL[n]; C[b - 1, a - 1] = CL[n]
    return C
def gauss_cov(S, idx, C, ng_scale=1.0):
    """Gaussian covariance at area A = 1 sr for the points idx; returns (total, noise-only part). Every term scales as 1 / A."""
    idx = np.asarray(idx); nb = S["nbin"]
    sig = S["sig_e"]; n = S["ngal"] * ng_scale / ARC ** 2       # per steradian
    Nn = sig ** 2 / n
    Ch = C.copy()
    for i in range(nb): Ch[i, i] = Ch[i, i] + Nn[i]
    b1 = S["b1_all"][idx]; b2 = S["b2_all"][idx]; isp = S["isp_all"][idx]; ia = S["ia_all"][idx]
    J = np.where(isp[:, None], S["Jp_raw"][ia], S["Jm_raw"][ia]) * np.sqrt(WL)[None, :]
    i_, j_ = np.minimum(b1, b2), np.maximum(b1, b2); pk = i_ * nb + j_
    cov = np.zeros((len(idx), len(idx))); NNs = np.zeros_like(cov)
    groups = {}
    for m, key in enumerate(pk): groups.setdefault(int(key), []).append(m)
    for P, mp in groups.items():
        i, j = divmod(P, nb); Jp = J[mp]
        for Q, mq in groups.items():
            k, l = divmod(Q, nb)
            M = Ch[i, k] * Ch[j, l] + Ch[i, l] * Ch[j, k]
            nn = (Nn[i] * Nn[j]) * ((i == k) * (j == l) + (i == l) * (j == k))
            M = M - nn                                         # the pure-noise part goes in by the pair formula below
            cov[np.ix_(mp, mq)] = (Jp * M[None, :]) @ J[mq].T
    same = (ia[:, None] == ia[None, :]) & (isp[:, None] == isp[None, :]) & (pk[:, None] == pk[None, :])
    fac = np.where(i_ == j_, 2.0, 1.0)
    om = S["Om_bin"][ia]
    NNs = np.where(same, (fac * 2 * sig[i_] ** 2 * sig[j_] ** 2 / (n[i_] * n[j_] * om))[:, None] * np.ones(len(idx))[None, :], 0.0)
    return cov + NNs, NNs
def xi_nominal(S, Pm):
    x0, _, _, unpack, _ = G["nuis_spec"](S, 1.0, False); D = subset(S, np.ones(len(S["rows"]), bool))
    return G["theory"](S, D, unpack(x0), Pm, "PM")

# ------------------------------------------------------------------ the scan rule (CO2's, with an optional covariance per sigma8)
GRID = np.arange(0.70, 0.9001, 0.0125)
def scan(evalf, grid=None):
    """evalf(s8) -> fit dict. CO2's parabola rule; the grid is extended by 0.0125 at an edge minimum (0.60 to 1.00 at most)."""
    g = list(GRID if grid is None else grid); res = {round(s, 6): evalf(float(s)) for s in g}
    while True:
        ss = sorted(res); c2 = np.array([res[s]["chi2"] for s in ss]); i = int(np.argmin(c2))
        if i == 0 and ss[0] > 0.60 + 1e-9: s = round(ss[0] - 0.0125, 6); res[s] = evalf(s); continue
        if i == len(ss) - 1 and ss[-1] < 1.00 - 1e-9: s = round(ss[-1] + 0.0125, 6); res[s] = evalf(s); continue
        break
    ss = np.array(sorted(res)); c2 = np.array([res[s]["chi2"] for s in ss]); i = int(np.argmin(c2))
    lo_, hi_ = max(i - 2, 0), min(i + 3, len(ss)); co = np.polyfit(ss[lo_:hi_], c2[lo_:hi_], 2)
    sb = float(-co[1] / (2 * co[0])) if co[0] > 0 else float(ss[i]); wid = 1 / math.sqrt(co[0]) if co[0] > 0 else float("nan")
    return dict(sigma8=ss.tolist(), chi2=c2.tolist(), p=[res[s]["p"] for s in ss], best_sigma8=sb, width=wid, edge_hit=bool(i in (0, len(ss) - 1)))
