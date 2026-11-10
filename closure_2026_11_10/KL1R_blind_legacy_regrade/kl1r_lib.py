"""KL1R library (FROZEN_CRITERIA.md 1792bd07ea). Written for this lane; KL1's code is not used.
- CFG592's library part executed unchanged (as CO2's co2_shear.py executes it).
- CO2's model: CFG596's S0 run x R, moved from 0.811 to a target sigma8 by the run's own response (re-written from CO2's text).
- My loader for KiDS-like releases (KiDS-Legacy, and KiDS-1000 for KB2), my KiDS-like nuisance block and fit (N bins).
- My Gaussian covariance and the covariance at the model (Part A's A2 as section 2.3 reads it).
Untrusted data are read only (astropy / numpy); nothing from the release is executed.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, glob, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
_code = open(SRC).read(); _cut = _code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_code[:_cut], SRC, "exec"), G)
import numpy as np
from scipy.optimize import minimize
from scipy.special import j0, jv
from scipy.stats import chi2 as CH
import astropy.io.fits as fits

Pmat, lib_fit, support_mask, subset, SURV, theory, C_ell, hankel = (G[k] for k in ("Pmat", "fit", "support_mask", "subset", "SURV", "theory", "C_ell", "hankel"))
LF, DLF, TAPER, MI, LN = (G[k] for k in ("LF", "DLF", "TAPER", "MI", "LN"))
EXT = G["EXT"]; S8E = 0.811
LEGACY = os.path.join(EXT, "kl1_kids_legacy_2026_11_10", "KiDS_Legacy_cosmic_shear_data_release")
CO1D = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed"); CO2D = os.path.join(REPO, "closure_2026_11_09", "CO2_form_b_amplitude_pinned")
HM = json.load(open(os.path.join(CO1D, "co1_hm.json"))); KH = np.array(HM["k"])

# ------------------------------------------------------------------ CO2's model (S0 nodes, response, amplitude move)
S0J = json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "P0", "cfg596_*.json"))[0])); SN = S0J["snap"]
K = np.array(SN["z0"]["k"]); NP_, LBOX = int(S0J["np"]), float(S0J["L"])
PZ0 = {0.0: np.array(SN["z0"]["P"]), 0.5: np.array(SN["z0.5"]["P"]), 1.0: np.array(SN["z1"]["P"])}
PZ = dict(PZ0)
BASE = dict(N=NP_, L=LBOX, k=K, k_lo=float(K[0]), k_hi=float(math.pi * NP_ / (4 * LBOX)))
def _araw(early, late): return np.log(np.array(SN[late]["P"]) / np.array(SN[early]["P"])) / (2 * math.log(SN[late]["D"] / SN[early]["D"]))
ARAW = {0.0: _araw("x0.2562", "z0"), 0.5: _araw("x0.7548", "x0.2562"), 1.0: _araw("z1", "x0.7548")}
def _runmed5(a):
    n = len(a); return np.array([np.median(a[max(0, i - 2):min(n, i + 3)]) for i in range(n)])
ALPHA = {z: np.clip(_runmed5(a), 1.0, 3.0) for z, a in ARAW.items()}
def ka4():
    out = {}
    for z in (0.0, 0.5, 1.0):
        m = K < 0.12; med = float(np.median(ARAW[z][m])); out[str(z)] = dict(n=int(m.sum()), median_alpha=med, pass_=bool(abs(med - 1) <= 0.15))
    return out
def onk(R): return np.interp(np.log(np.clip(K, KH[0], KH[-1])), np.log(KH), np.asarray(R, float))
def run_of(R, s8):
    f = (s8 / S8E) ** 2
    nodes = {z: ((PZ[z] * f ** ALPHA[z],) * 2) for z in PZ}
    return dict(BASE, name="x", foot="-", B=onk(R), nodes=nodes)
def Pm_of(R, s8): return Pmat(run_of(R, s8), "F")
ONE = np.ones_like(KH)

# A5a: CO2's post hoc R2 splice (L 200 S0 run below k 0.5) plus the box deficit factor above k 0.5
def a5a_nodes(rel):
    J2 = json.load(open(os.path.join(EXT, *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"]); out = {}
    for z, key in ((0.0, "z0"), (0.5, "z0.5"), (1.0, "z1")):
        p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"]))))
        m = (K >= 0.5) & (K <= 1.0); fac = float(np.median(p2[m] / PZ0[z][m]))
        o = PZ0[z] * fac; lo = K < 0.5; o[lo] = p2[lo]; out[z] = o
    return out
A5A_RUNS = {"A5a_CFG411": ("cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"),
            "A5a_CFG424_seed360": ("cfg424_work", "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json")}
def set_nodes(pz): PZ.clear(); PZ.update(pz)

# ------------------------------------------------------------------ KiDS-like loader (N bins)
def load_kidslike(name, fn, edges, cut_p, cut_m, Lchol, mu_u):
    F = fits.open(fn); cov = np.array(F["COVMAT"].data, float); nzt = F["NZ_SOURCE"].data; hd = F["NZ_SOURCE"].header
    rows = [(s, int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"])) for s, ext in (("+", "xiP"), ("-", "xiM")) for r in F[ext].data]
    keep = np.array([(cut_p[0] <= r[4] <= cut_p[1]) if r[0] == "+" else (cut_m[0] <= r[4] <= cut_m[1]) for r in rows])
    nb = len(mu_u)
    S = dict(name=name, cov=cov, rows=rows, pubkeep=keep, zmid=np.array(nzt["Z_MID"], float), nz=[np.array(nzt[f"BIN{i+1}"], float) for i in range(nb)],
             nbin=nb, edges=list(zip(edges[:-1], edges[1:])), angbin0=min(r[3] for r in rows), L=np.asarray(Lchol, float), mu_u=np.asarray(mu_u, float),
             sig_e=np.array([float(hd[f"SIG_E_{i+1}"]) for i in range(nb)]), ngal=np.array([float(hd[f"NGAL_{i+1}"]) for i in range(nb)]))
    _finish(S); return S
def _finish(S):
    S["Hp"], S["Hm"], S["Ap"], S["Am"] = hankel(S["edges"])
    nb = S["nbin"]; S["pairs"] = [(a, b) for a in range(1, nb + 1) for b in range(a, nb + 1)]; pid = {p: i for i, p in enumerate(S["pairs"])}
    S["ip_all"] = np.array([pid[(min(r[1], r[2]), max(r[1], r[2]))] for r in S["rows"]]); S["ia_all"] = np.array([r[3] - S["angbin0"] for r in S["rows"]])
    S["isp_all"] = np.array([r[0] == "+" for r in S["rows"]]); S["b1_all"] = np.array([r[1] for r in S["rows"]]) - 1; S["b2_all"] = np.array([r[2] for r in S["rows"]]) - 1
    S["d_all"] = np.array([r[5] for r in S["rows"]])
def legacy_mu():
    txt = open(os.path.join(LEGACY, "chains_and_config_files", "xipm", "KiDS_Legacy_priors.ini")).read().split("[nofz_shifts]")[1]
    mu = {}
    for line in txt.splitlines():
        if line.strip().startswith("["): break
        if line.startswith("uncorr_bias_"):
            k, v = line.split("="); mu[int(k.strip().split("_")[-1])] = float(v.split()[1])
    return np.array([mu[i] for i in sorted(mu)])
def load_legacy(mu=None):
    Ncov = np.loadtxt(os.path.join(LEGACY, "data", "Nz_covariance.txt"))
    return load_kidslike("Legacy", os.path.join(LEGACY, "data", "KiDS_Legacy_xipm.fits"), np.geomspace(2.0, 300.0, 10), (2.0, 300.0), (4.0, 300.0),
                         np.linalg.cholesky(Ncov), legacy_mu() if mu is None else mu)
def load_k1000():
    fn = glob.glob(os.path.join(G["WORK"], "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]
    K0 = SURV["KiDS"]
    return load_kidslike("KiDS1000", fn, np.geomspace(0.5, 300.0, 10), (0.5, 300.0), (4.0, 300.0), K0["L"], K0["mu_u"])
def des():
    S = SURV["DES"]
    if "sig_e" not in S:
        fn = os.path.join(G["WORK"], "2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits"); hd = fits.open(fn)["nz_source"].header
        S["sig_e"] = np.array([float(hd[f"SIG_E_{i+1}"]) for i in range(4)]); S["ngal"] = np.array([float(hd[f"NGAL_{i+1}"]) for i in range(4)])
    return S

# ------------------------------------------------------------------ KiDS-like nuisances and fit (N decorrelated shifts + one NLA amplitude)
def fit_k(S, D, Pm, ia=True, Cinv=None, mu=None):
    mu = S["mu_u"] if mu is None else mu; nb = S["nbin"]; Ci = D["Cinv"] if Cinv is None else Cinv; d = D["d"]
    x0 = np.r_[mu, 0.5 if ia else 0.0]; lo = np.r_[mu - 5, -6.0 if ia else 0.0]; hi = np.r_[mu + 5, 6.0 if ia else 0.0]
    unpack = lambda x: dict(dz=S["L"] @ x[:nb], A=float(x[nb]))
    def f(x):
        r = d - theory(S, D, unpack(x), Pm, "PM"); return float(r @ Ci @ r) + float(np.sum((x[:nb] - mu) ** 2))
    starts = [x0] + ([np.r_[x0[:-1], -0.5]] if ia else [])
    best = None
    for xs in starts:
        r = minimize(f, xs, method="L-BFGS-B", bounds=[(a, b) for a, b in zip(lo, hi)], options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
        if best is None or r.fun < best.fun: best = r
    par = unpack(best.x); t = theory(S, D, par, Pm, "PM"); r_ = d - t
    return dict(chi2=float(best.fun), chi2_data=float(r_ @ Ci @ r_), A_IA=par["A"], pulls=[float(v) for v in best.x[:nb] - mu], x=[float(v) for v in best.x])
def fit_any(S, D, Pm, ia=True, Cinv=None, mu=None):
    if S["name"] == "DES":
        DD = D if Cinv is None else dict(D, Cinv=Cinv)
        r = lib_fit(S, DD, Pm, ia=ia); r = {k: v for k, v in r.items() if k != "t"}
        r["pulls"] = [float(v / s) for v, s in zip(r["x"][:4], G["DES_DZ_SIG"])]; return r
    return fit_k(S, D, Pm, ia=ia, Cinv=Cinv, mu=mu)

def support_k(S, run, Pm0):
    """CFG592's support_mask, with the nominal nuisances of a KiDS-like survey (dz = L mu, no IA); DES goes through the library's."""
    if S["name"] == "DES": return support_mask(S, run, Pm0)
    q, I, wchi = G["kernels"](S, S["L"] @ S["mu_u"], "PM"); chi = G["BG"]["PM"][0]; KK = (LN[:, None] + 0.5) / chi[None, :]
    inside = (KK >= run["k_lo"]) & (KK <= run["k_hi"]); PW = Pm0 * wchi[None, :]
    tot = np.einsum("lj,aj,bj->abl", PW, q, q); ins = np.einsum("lj,aj,bj->abl", PW * inside, q, q)
    Ct = np.array([tot[a - 1, b - 1] for a, b in S["pairs"]]); Ci = np.array([ins[a - 1, b - 1] for a, b in S["pairs"]])
    fp = (Ci @ S["Ap"].T) / (Ct @ S["Ap"].T); fm = (Ci @ S["Am"].T) / (Ct @ S["Am"].T)
    return np.where(S["isp_all"], fp[S["ip_all"], S["ia_all"]], fm[S["ip_all"], S["ia_all"]])

# ------------------------------------------------------------------ Gaussian covariance (Part A A2, section 2.3)
ARC = math.pi / (180 * 60)
def jbar(S, nsub=40):
    Jp, Jm = [], []
    for lo, hi in S["edges"]:
        th = np.linspace(lo, hi, nsub) * ARC; wt = th / th.sum(); x = LF[None, :] * th[:, None]
        Jp.append((wt[:, None] * j0(x)).sum(0) * TAPER); Jm.append((wt[:, None] * jv(4, x)).sum(0) * TAPER)
    return np.array(Jp), np.array(Jm)
def nominal(S):
    return dict(dz=S["L"] @ S["mu_u"], A=0.0) if S["name"] != "DES" else dict(dz=np.zeros(4), A=0.0)
def Cfull(S, Pm):
    """model GG C^ab on the fine ell grid at nominal nuisances, no alignment: [nb, nb, nLF]"""
    Cp = C_ell(S, nominal(S), Pm, "PM"); nb = S["nbin"]; Cf = Cp @ MI.T
    out = np.zeros((nb, nb, len(LF)))
    for i, (a, b) in enumerate(S["pairs"]): out[a - 1, b - 1] = Cf[i]; out[b - 1, a - 1] = Cf[i]
    return out
def gauss_parts(S, Pm, nscale=1.0):
    """G at area 1 sr, split into (total, pure noise) for all published points. nscale multiplies every n_i (MA2 / MA2b)."""
    if "_J" not in S: S["_J"] = jbar(S)
    Jp, Jm = S["_J"]; nt = len(S["edges"]); Jall = np.vstack([Jp, Jm])         # rows: (+, t) then (-, t)
    n_sr = S["ngal"] * nscale / ARC ** 2; s2 = S["sig_e"] ** 2; N = np.diag(s2 / n_sr)
    C = Cfull(S, Pm); Ct = C + N[:, :, None]; w = LF * DLF          # sum ell dell; the 1 / (2 pi A) is applied once below
    pairs = S["pairs"]; npr = len(pairs); blocks = {}
    for P_, (i, j) in enumerate(pairs):
        for Q_, (k, l) in enumerate(pairs):
            if Q_ < P_: continue
            i_, j_, k_, l_ = i - 1, j - 1, k - 1, l - 1
            T = Ct[i_, k_] * Ct[j_, l_] + Ct[i_, l_] * Ct[j_, k_] - (N[i_, k_] * N[j_, l_] + N[i_, l_] * N[j_, k_])
            blocks[(P_, Q_)] = (Jall * (w * T)[None, :]) @ Jall.T
    npt = len(S["rows"]); Gm = np.zeros((npt, npt)); Nz = np.zeros((npt, npt))
    ip, ia, isp = S["ip_all"], S["ia_all"], S["isp_all"]; row = np.where(isp, 0, nt) + ia
    for p in range(npt):
        for q in range(p, npt):
            P_, Q_ = ip[p], ip[q]
            v = blocks[(P_, Q_)][row[p], row[q]] if P_ <= Q_ else blocks[(Q_, P_)][row[q], row[p]]
            Gm[p, q] = Gm[q, p] = v
    # pure noise: same theta bin, same sign; (d_ik d_jl + d_il d_jk) 2 s_i^2 s_j^2 / (n_i n_j A Omega_bin)
    om = np.array([math.pi * ((hi * ARC) ** 2 - (lo * ARC) ** 2) for lo, hi in S["edges"]])
    for p in range(npt):
        for q in range(p, npt):
            if ia[p] != ia[q] or isp[p] != isp[q]: continue
            i, j = pairs[ip[p]]; k, l = pairs[ip[q]]
            dd = (i == k and j == l) + (i == l and j == k)
            if dd:
                v = dd * 2 * s2[i - 1] * s2[j - 1] / (n_sr[i - 1] * n_sr[j - 1] * om[ia[p]])
                Nz[p, q] = Nz[q, p] = v
    return Gm / (2 * math.pi) + Nz, Nz
def ka2(S, Pm_fid, nscale=1.0):
    G1, N1 = gauss_parts(S, Pm_fid, nscale); pub = np.diag(S["cov"]); dg = np.diag(G1); nf = np.diag(N1) / dg
    k = S["pubkeep"]; noise = k & (nf >= 0.8); sig = k & (nf < 0.5)
    A = 1.0 / float(np.median(pub[noise] / dg[noise])) if noise.sum() > 0 else float("nan")
    r = pub / (dg / A)
    out = dict(area_sr=A, area_deg2=A / (math.pi / 180) ** 2, n_noise=int(noise.sum()), n_signal=int(sig.sum()))
    if noise.sum() >= 5:
        lo, hi = np.percentile(r[noise], [16, 84]); out.update(i_p16=float(lo), i_p84=float(hi), i_pass=bool(lo >= 0.85 and hi <= 1.15), i_eval=True)
    else: out.update(i_eval=False, i_pass=None)
    if sig.sum() >= 5:
        med = float(np.median(r[sig])); mn = float(np.min(r[sig])); out.update(ii_median=med, ii_min=mn, ii_pass=bool(0.95 <= med <= 1.6 and mn >= 0.80), ii_eval=True)
    else: out.update(ii_eval=False, ii_pass=None)
    # (iii) correlation coefficients over kept points
    Gs = G1 / A; kk = k
    rp = S["cov"][np.ix_(kk, kk)] / np.sqrt(np.outer(pub[kk], pub[kk])); rm = Gs[np.ix_(kk, kk)] / np.sqrt(np.outer(np.diag(Gs)[kk], np.diag(Gs)[kk]))
    iu = np.triu_indices(int(kk.sum()), 1); out["iii_median_abs_dr"] = float(np.median(np.abs(rp[iu] - rm[iu])))
    out["pass_"] = bool(out["i_pass"] is True and out["ii_pass"] is True)
    out["G_area1"] = G1; out["N_area1"] = N1
    return out
def all_D(S):
    k = np.ones(len(S["rows"]), bool)
    return dict(keep=k, d=S["d_all"], ip=S["ip_all"], ia=S["ia_all"], isp=S["isp_all"], b1=S["b1_all"], b2=S["b2_all"], N=len(k))
class CovModel:
    """C(model) = G(model) + R (s_p s_q)^(gamma/2), R = C_pub - G(fid); A fitted at the fiducial."""
    def __init__(self, S, Pm_fid, keep):
        self.S = S; k2 = ka2(S, Pm_fid); self.ka2 = {a: b for a, b in k2.items() if a not in ("G_area1", "N_area1")}
        self.A = k2["area_sr"]; self.Gfid = k2["G_area1"] / self.A; self.R = S["cov"] - self.Gfid
        self.Dall = all_D(S); self.xfid = theory(S, self.Dall, nominal(S), Pm_fid, "PM"); self.keep = keep
    def cov(self, Pm, gamma=2.0):
        G1, _ = gauss_parts(self.S, Pm); Gm = G1 / self.A
        s = np.clip(theory(self.S, self.Dall, nominal(self.S), Pm, "PM") / self.xfid, 0.5, 3.0)
        C = Gm + self.R * np.outer(s, s) ** (gamma / 2.0)
        return C[np.ix_(self.keep, self.keep)]
    def cinv(self, Pm, gamma=2.0):
        C = self.cov(Pm, gamma)
        try:
            Lc = np.linalg.cholesky(C)
        except np.linalg.LinAlgError:
            return None, None
        return np.linalg.inv(C), 2 * float(np.sum(np.log(np.diag(Lc))))

def lab(p): return "CONSISTENT" if p >= 0.05 else ("TENSION" if p >= 0.0027 else "EXCLUDED AT 3 SIGMA")
def pval(c2, N): return float(CH.sf(c2, N))
def parabola(grid, c2):
    i = int(np.argmin(c2)); lo_, hi_ = max(i - 2, 0), min(i + 3, len(grid)); co = np.polyfit(grid[lo_:hi_], c2[lo_:hi_], 2)
    sb = float(-co[1] / (2 * co[0])); wid = 1 / math.sqrt(co[0]) if co[0] > 0 else float("nan"); return sb, wid, float(np.polyval(co, sb)), i
def scan(chi2_at, lo=0.70, hi=0.90, step=0.0125):
    grid = list(np.round(np.arange(lo, hi + 1e-9, step), 6)); vals = {g: chi2_at(g) for g in grid}
    while True:
        gs = sorted(vals); c2 = np.array([vals[g] for g in gs]); i = int(np.argmin(c2))
        if i == 0 and gs[0] > 0.60 + 1e-9: g = round(gs[0] - step, 6); vals[g] = chi2_at(g); continue
        if i == len(gs) - 1 and gs[-1] < 1.00 - 1e-9: g = round(gs[-1] + step, 6); vals[g] = chi2_at(g); continue
        break
    gs = sorted(vals); c2 = np.array([vals[g] for g in gs]); sb, wid, cmin, i = parabola(np.array(gs), c2)
    return dict(grid=gs, chi2=c2.tolist(), best=sb, width=wid, chi2_min=cmin, at_edge=bool(i in (0, len(gs) - 1)))
